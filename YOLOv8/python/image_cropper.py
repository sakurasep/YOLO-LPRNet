import os
from PIL import Image

# # 图片和标注数据所在的文件夹路径
# image_folder = "../../CCPD2020/ccpd_green/val"
# annotation_folder = "./runs/detect/predict3/labels"
#
# # 输出文件夹路径
# output_folder = "../../CCPD2020/ccpd_green/val_lpr"

# 图片和标注数据所在的文件夹路径
image_folder = "../images"
annotation_folder = "./runs/detect/predict4/labels"

# 输出文件夹路径
output_folder = "../images_lpr"

# 创建保存切割后图片的文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历标注数据文件夹中的文件
for filename in os.listdir(annotation_folder):
    if filename.endswith(".txt"):
        # 构建图片路径和标注数据路径
        image_filename = filename[:-4] + ".jpg"
        image_path = os.path.join(image_folder, image_filename)
        txt_path = os.path.join(annotation_folder, filename)

        # 加载原始图像
        image = Image.open(image_path)
        width, height = image.size

        # 从文件中读取标注数据
        label_data = []
        with open(txt_path, "r") as file:
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
            save_path = os.path.join(output_folder, f"{image_filename[:-4]}_{i}.jpg")

            # 保存切割后的图像
            cropped_image.save(save_path)

            print(f"切割后的图像已保存至: {save_path}")
