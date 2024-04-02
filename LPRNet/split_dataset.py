import os
import random
import shutil


def split_dataset(input_folder, output_folder, train_ratio=0.7, test_ratio=0.3, seed=42):
    # 创建输出文件夹
    train_folder = os.path.join(output_folder, 'train')
    test_folder = os.path.join(output_folder, 'test')
    for folder in [train_folder, test_folder]:
        os.makedirs(folder, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    random.seed(seed)
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)

            # 随机分配到训练集或测试集
            r = random.random()
            if r < train_ratio:
                shutil.copy(image_path, os.path.join(train_folder, filename))
            else:
                shutil.copy(image_path, os.path.join(test_folder, filename))


# 示例用法
input_folder = '../CCPD2020/ccpd_green/train_lprnet'
output_folder = '../CCPD2020/ccpd_green/train_lprnet_datasets'
split_dataset(input_folder, output_folder)
