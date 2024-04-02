import os
from xml.etree import ElementTree as ET


def xml_to_yolo(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename = root.find('filename').text
    base_filename = os.path.splitext(filename)[0]  # 获取文件名部分（去除扩展名）
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)

    yolo_lines = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        xmin = float(obj.find('bndbox/xmin').text)
        ymin = float(obj.find('bndbox/ymin').text)
        xmax = float(obj.find('bndbox/xmax').text)
        ymax = float(obj.find('bndbox/ymax').text)

        # Convert bbox coordinates to YOLO format
        x_center = (xmin + xmax) / 2 / width
        y_center = (ymin + ymax) / 2 / height
        bbox_width = (xmax - xmin) / width
        bbox_height = (ymax - ymin) / height

        yolo_lines.append(f"{name} {x_center} {y_center} {bbox_width} {bbox_height}\n")

    # Write YOLO lines to TXT file
    output_file = os.path.join(output_dir, base_filename + '.txt')  # 使用文件名部分构建输出文件名
    with open(output_file, 'w') as f:
        f.writelines(yolo_lines)


def batch_convert_xml_to_yolo(xml_dir, output_dir):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 遍历目标目录中的所有 XML 文件
    for filename in os.listdir(xml_dir):
        if filename.endswith('.xml'):
            xml_file = os.path.join(xml_dir, filename)
            xml_to_yolo(xml_file, output_dir)


if __name__ == '__main__':
    # XML 文件目录和输出目录
    xml_dir = '../../CCPD2020/ccpd_green/val_xml'
    output_dir = '../../CCPD2020/ccpd_green/val_txt'

    # 批量转换 XML 文件为 YOLO 可读取的 TXT 文件
    batch_convert_xml_to_yolo(xml_dir, output_dir)
