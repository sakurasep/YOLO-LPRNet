import os
import cv2


def batch_resize_images(input_dir, output_dir, target_size=(92, 24)):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # 仅处理图像文件
            # 构建输入和输出文件路径
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # 读取图像
            img = cv2.imread(input_path)

            # 调整图像大小
            resized_img = cv2.resize(img, target_size)

            # 保存调整大小后的图像到输出目录
            cv2.imwrite(output_path, resized_img)

    print("Batch resizing completed.")


# 示例用法
input_directory = '/Users/sakurasep/Downloads/CCPD/CCPD2020/ccpd_green/test_lpr'
output_directory = '/Users/sakurasep/Downloads/CCPD/CCPD2020/ccpd_green/test_lpr_new'
batch_resize_images(input_directory, output_directory)
