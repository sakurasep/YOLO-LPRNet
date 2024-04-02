import os
import random
import shutil
from tqdm import tqdm

# 指定 images 文件夹路径
image_dir = "../../CCPD2020/ccpd_green/val"

# 指定 labels 文件夹路径
label_dir = "../../CCPD2020/ccpd_green/val_txt"

# 创建目标文件夹
base_dir = "../../CCPD2020/ccpd_green/Green"

for folder in ['train', 'valid', 'test']:
    os.makedirs(os.path.join(base_dir, folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, folder, 'labels'), exist_ok=True)

# 创建一个空列表来存储有效图片的路径
valid_images = []

# 创建一个空列表来存储有效 label 的路径
valid_labels = []

# 遍历 images 文件夹下的所有图片
for image_name in os.listdir(image_dir):
    # 获取图片的完整路径
    image_path = os.path.join(image_dir, image_name)

    # 获取图片文件的扩展名
    ext = os.path.splitext(image_name)[-1]

    # 根据扩展名替换成对应的 label 文件名
    label_name = image_name.replace(ext, ".txt")

    # 获取对应 label 的完整路径
    label_path = os.path.join(label_dir, label_name)

    # 判断 label 是否存在
    if not os.path.exists(label_path):
        # 删除图片
        # os.remove(image_path)
        print("deleted:", image_path)
    else:
        # 将图片路径添加到列表中
        valid_images.append(image_path)
        # 将label路径添加到列表中
        valid_labels.append(label_path)

# 创建一个副本列表用于遍历
valid_images_copy = valid_images.copy()
valid_labels_copy = valid_labels.copy()

# 遍历每个有效图片路径
for i in tqdm(range(len(valid_images_copy))):
    image_path = valid_images_copy[i]
    label_path = valid_labels_copy[i]

    # 随机生成一个概率
    r = random.random()

    # 判断图片应该移动到哪个文件夹
    # train：valid：test = 7:3:1
    if r < 0.1:
        # 移动到 test 文件夹
        destination = os.path.join(base_dir, "test")
    elif r < 0.2:
        # 移动到 valid 文件夹
        destination = os.path.join(base_dir, "valid")
    else:
        # 移动到 train 文件夹
        destination = os.path.join(base_dir, "train")

    # 生成目标文件夹中图片的新路径
    image_destination_path = os.path.join(destination, "images", os.path.basename(image_path))

    # 复制图片到目标文件夹
    shutil.copy(image_path, image_destination_path)

    # 生成目标文件夹中 label 的新路径
    label_destination_path = os.path.join(destination, "labels", os.path.basename(label_path))

    # 复制 label 到目标文件夹
    shutil.copy(label_path, label_destination_path)

print("valid images:", valid_images)
# 输出有效label路径列表
print("valid labels:", valid_labels)
