import torch
import cv2
import numpy as np
from LPRNet_Pytorch.model.LPRNet import build_lprnet
from LPRNet_Pytorch.data.load_data import CHARS
import os

# 图片预处理
def transform(img):
    img = img.astype('float32')
    img -= 127.5
    img *= 0.0078125
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

# 预测图片
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
                if(pre_c == c) or (c == len(CHARS) - 1):
                    if c == len(CHARS) - 1:
                        pre_c = c
                    continue
                no_repeat_blank_label.append(c)
                pre_c = c
            preb_labels.append(no_repeat_blank_label)
        for preb_label in preb_labels:
            plate = ''.join([CHARS[i] for i in preb_label])
            print("Predicted plate:", plate)

if __name__ == "__main__":
    # 指定图片文件夹路径
    image_folder = '../CCPD2020/ccpd_green/val_lpr'
    # 加载模型
    model_path = "./LPRNet_Pytorch/Final_LPRNet_model.pth"
    lprnet = load_model(model_path)
    # 对图片进行预测并打印结果到控制台
    predict_images(image_folder, lprnet)
