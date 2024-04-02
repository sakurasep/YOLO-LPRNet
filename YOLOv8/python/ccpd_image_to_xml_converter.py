import os
import cv2
from lxml import etree


class CCPDXMLLabeler:
    def __init__(self, folder_name, filename, path, database="Unknown"):
        self.root = etree.Element("annotation")
        # 设置文件夹名、文件名和数据库信息
        child1 = etree.SubElement(self.root, "folder")
        child1.text = folder_name
        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename
        child4 = etree.SubElement(self.root, "source")
        child5 = etree.SubElement(child4, "database")
        child5.text = database

    def set_size(self, width, height, channel):
        # 设置图像的尺寸信息
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(width)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "channel")
        channeln.text = str(channel)

    def set_segmented(self, seg_data=0):
        # 设置segmented信息
        segmented = etree.SubElement(self.root, "segmented")
        segmented.text = str(seg_data)

    def set_object(self, label, x_min, y_min, x_max, y_max,
                   pose='Unspecified', truncated=0, difficult=0):
        # 设置对象（车牌）信息
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = label
        posen = etree.SubElement(object, "pose")
        posen.text = pose
        truncatedn = etree.SubElement(object, "truncated")
        truncatedn.text = str(truncated)
        difficultn = etree.SubElement(object, "difficult")
        difficultn.text = str(difficult)
        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(x_min)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(y_min)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(x_max)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(y_max)

    def save_file(self, filename):
        # 保存XML文件
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')


def convert_to_xml(image_path, save_path):
    # 转换图片标注为XML文件
    for filename in os.listdir(image_path):
        # 遍历图片文件夹中的所有文件
        if filename.endswith('.jpg'):  # 确保只处理jpg格式的图片
            print("Processing:", filename)
            # 解析文件名获取坐标信息
            lx, ly, rx, ry = filename.split("-")[2].split("_")[0].split("&") + filename.split("-")[2].split("_")[
                1].split("&")

            # 读取图片尺寸
            img = cv2.imread(os.path.join(image_path, filename))
            if img is None:
                continue
            height, width, channel = img.shape

            # 创建XML标注对象
            xml_folder_name = "folder_name"  # 修改文件夹名
            xml_path = os.path.join("path", filename)  # 修改路径
            xml_labeler = CCPDXMLLabeler(folder_name=xml_folder_name, filename=filename, path=xml_path)
            xml_labeler.set_size(width, height, channel)
            xml_labeler.set_segmented()
            # 添加车牌对象信息
            xml_labeler.set_object(label='0', x_min=int(lx), y_min=int(ly), x_max=int(rx), y_max=int(ry))

            # 确保保存路径存在，不存在则创建
            os.makedirs(save_path, exist_ok=True)

            # 保存XML文件
            xml_filename = os.path.splitext(filename)[0] + '.xml'
            xml_labeler.save_file(os.path.join(save_path, xml_filename))


if __name__ == '__main__':
    # 输入图像文件夹路径和保存XML文件的路径
    image_path = r"../../CCPD2020/ccpd_green/val"
    save_path = r"../../CCPD2020/ccpd_green/val_xml"
    convert_to_xml(image_path, save_path)
