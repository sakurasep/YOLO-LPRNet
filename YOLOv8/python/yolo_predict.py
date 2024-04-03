import os
from ultralytics import YOLO

# 从模型文件构建YOLO模型
model = YOLO("../train/best.pt")

# 指定图像文件夹路径
# image_folder = "../../CCPD2020/ccpd_green/val"
image_folder = "../images"

# 获取图像文件夹中的所有图像文件列表
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('.jpg', '.jpeg', '.png'))]

# 对每张图像进行预测
for image_file in image_files:
    # 对图像进行预测，并保存预测结果到文件夹
    model.predict(image_file, save_txt=True, imgsz=320, conf=0.5, device='mps')
