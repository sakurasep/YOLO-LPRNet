import shutil
from PIL import Image
import torch
import cv2
import numpy as np
from utils.load_data import CHARS
from utils.LPRNet import build_lprnet
from flask import Flask, request, jsonify
import os
from ultralytics import YOLO
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)


# 图片预处理
def transform(img):
    # 将图像数据类型转换为浮点型
    img = img.astype('float32')
    # 减去127.5以对图像进行归一化，将像素值范围缩放到[-1, 1]之间
    img -= 127.5
    # 乘以0.0078125以进一步缩放图像像素值，确保在较小范围内
    img *= 0.0078125
    # 调整图像的维度顺序，将通道维度置于第一维度，以匹配模型的输入格式
    img = np.transpose(img, (2, 0, 1))
    return img


# 加载模型
def load_model(model_path):
    lprnet = build_lprnet(lpr_max_len=8, phase=True, class_num=68, dropout_rate=0.5)
    device = torch.device("cpu")
    lprnet.to(device)
    print("Success to build network")
    lprnet.load_state_dict(torch.load(model_path, map_location=device))
    print("Load model successful")
    return lprnet


@app.route('/predict_plate', methods=['GET'])
def predict_plate():
    image_path = "./output_lpr"
    # 加载模型
    lprnet = load_model(model_path="./model/Final_LPRNet_model.pth")

    # 预测车牌号码
    predicted_plate = predict_images(image_path, lprnet)

    print(predicted_plate)

    return jsonify({'plate': predicted_plate})


# LPRNet 识别图像信息
def predict_images(image_folder, model):
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    for image_file in image_files:
        img_path = os.path.join(image_folder, image_file)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (94, 24))
        im = transform(img)
        im = im[np.newaxis, :]
        ims = torch.Tensor(im)
        prebs = model(ims)
        prebs = prebs.cpu().detach().numpy()
        preb_labels = list()
        for i in range(prebs.shape[0]):
            preb = prebs[i, :, :]
            preb_label = list()
            for j in range(preb.shape[1]):
                preb_label.append(np.argmax(preb[:, j], axis=0))
            no_repeat_blank_label = list()
            pre_c = preb_label[0]
            if pre_c != len(CHARS) - 1:
                no_repeat_blank_label.append(pre_c)
            for c in preb_label:
                if (pre_c == c) or (c == len(CHARS) - 1):
                    if c == len(CHARS) - 1:
                        pre_c = c
                    continue
                no_repeat_blank_label.append(c)
                pre_c = c
            preb_labels.append(no_repeat_blank_label)
        for preb_label in preb_labels:
            plate = ''.join([CHARS[i] for i in preb_label])
            print("Predicted plate:", plate)
            return plate


def crop_single_image(image_path, annotation_path):
    # 删除当前目录下的 output_lpr 文件夹，并在删除后重新创建
    output_folder = "output_lpr"
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 加载原始图像
    image = Image.open(image_path)
    width, height = image.size

    # 从文件中读取标注数据
    label_data = []
    with open(annotation_path, "r") as file:
        for line in file:
            values = line.strip().split(" ")
            label_data.append([int(values[0]), float(values[1]), float(values[2]), float(values[3]), float(values[4])])

    # 遍历每个标注数据
    for i, label in enumerate(label_data):
        # 提取标注信息
        class_label = label[0]
        x_center, y_center, box_width, box_height = label[1:]

        # 计算边界框的像素坐标
        x1 = int((x_center - box_width / 2) * width)
        y1 = int((y_center - box_height / 2) * height)
        x2 = int((x_center + box_width / 2) * width)
        y2 = int((y_center + box_height / 2) * height)

        # 切割原图
        cropped_image = image.crop((x1, y1, x2, y2))

        # 构造保存路径
        save_path = os.path.join(output_folder, f"{os.path.basename(image_path)[:-4]}_{i}.jpg")

        # 保存切割后的图像
        cropped_image.save(save_path)

        print(f"切割后的图像已保存至: {save_path}")
        return save_path


# 预测函数
def predict_image(image_path):
    # 删除当前目录下的 runs 文件夹（如果存在）
    runs_folder = "runs"
    if os.path.exists(runs_folder):
        shutil.rmtree(runs_folder)
    # 从模型文件构建YOLO模型
    model = YOLO("./model/best.pt")

    # 检查图像文件路径是否存在
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return

    # 对单张图像进行预测
    model.predict(image_path, save_txt=True, imgsz=320, conf=0.5, device='mps')


# 主要逻辑
def main(filename):
    # 调用预测函数
    predict_image(filename)
    # 获取不包含拓展名的文件名
    file_name_without_extension = os.path.splitext(os.path.basename(filename))[0]
    # 构造新的文件名（扩展名改为.txt）
    new_filename_txt = file_name_without_extension + ".txt"
    # 切割图片
    annotation_path = "./runs/detect/predict/labels/" + new_filename_txt
    crop_single_image(filename, annotation_path)


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    print("Image uploaded successfully. File path:", filename)

    # 调用main函数处理上传的文件
    main(filename)

    # 返回成功的响应
    return jsonify({'success': 'Image uploaded successfully', 'file_path': filename})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
