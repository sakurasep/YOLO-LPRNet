import cv2
import os
from lxml import etree


class LabelimgAnnotationsXML:
    def __init__(self, folder_name, filename, path, database="Unknown"):
        # 创建 XML 根节点
        self.root = etree.Element("annotation")
        # 添加 folder 节点
        child1 = etree.SubElement(self.root, "folder")
        child1.text = folder_name
        # 添加 filename 节点
        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename
        # 添加 source 节点和其子节点 database
        child4 = etree.SubElement(self.root, "source")
        child5 = etree.SubElement(child4, "database")
        child5.text = database

    def set_size(self, width, height, channel):
        # 添加 size 节点及其子节点
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(width)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "channel")
        channeln.text = str(channel)

    def set_segmented(self, seg_data=0):
        # 添加 segmented 节点
        segmented = etree.SubElement(self.root, "segmented")
        segmented.text = str(seg_data)

    def set_object(self, label, x_min, y_min, x_max, y_max,
                   pose='Unspecified', truncated=0, difficult=0):
        # 添加 object 节点及其子节点
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

    def savefile(self, filename):
        # 将 XML 结构写入文件
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')


def translate(path, save_path):
    # 如果保存路径不存在，则创建保存路径
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 遍历指定文件夹中的文件
    for filename in os.listdir(path):
        # 输出当前处理的文件名
        print(filename)

        # 解析文件名获取车牌坐标信息
        list1 = filename.split("-", 3)
        subname = list1[2]
        list2 = filename.split(".", 1)
        subname1 = list2[1]
        if subname1 == 'txt':
            continue
        lt, rb = subname.split("_", 1)
        lx, ly = lt.split("&", 1)
        rx, ry = rb.split("&", 1)
        print(lx, ly, rx, ry)

        # 构建保存的 XML 文件名
        save_xml_name = filename.replace('jpg', 'xml')

        # 读取图像并获取尺寸信息
        img = cv2.imread(os.path.join(path, filename))
        if img is None:
            continue
        height, width, channel = img.shape

        # 创建 XML 实例
        anno = LabelimgAnnotationsXML('folder_name', filename + '.jpg', 'path')
        # 设置图像尺寸
        anno.set_size(width, height, channel)
        # 设置 segmented 节点
        anno.set_segmented()
        # 设置 object 节点
        label, x_min, y_min, x_max, y_max = 'green', lx, ly, rx, ry
        anno.set_object(label, x_min, y_min, x_max, y_max)
        # 保存 XML 文件
        anno.savefile(os.path.join(save_path, save_xml_name))


if __name__ == '__main__':
    # 图片存储地址
    img_path = r"../CCPD2020/ccpd_green/train"
    # 保存 XML 文件的地址
    save_path = r"../CCPD2020/ccpd_green/train_xml_lpr"
    # 执行文件转换
    translate(img_path, save_path)
