import cv2
import os

roi_path = r'../CCPD2020/ccpd_green/train'
save_path = r'../CCPD2020/ccpd_green/train_lprnet'

if not os.path.exists(save_path):
    os.makedirs(save_path)

provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', 'O']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']

num = 0
for root, dirs, files in os.walk(roi_path):
    for filename in files:
        num += 1
        lpr_label = ""
        _, _, box, points, plate, brightness, blurriness = filename.split('-')
        print('plate:', plate)
        list_plate = plate.split('_')  # 读取车牌
        for i, pla in enumerate(list_plate):
            if i == 0:
                lpr_label += provinces[int(pla)]
            elif i == 1:
                lpr_label += alphabets[int(pla)]
            else:
                lpr_label += ads[int(pla)]

        print(lpr_label)
        img_path = os.path.join(roi_path, filename)
        img = cv2.imread(img_path)
        assert os.path.exists(img_path), "image file {} dose not exist.".format(img_path)

        box = box.split('_')  # 车牌边界
        box = [list(map(int, i.split('&'))) for i in box]

        xmin = box[0][0]
        xmax = box[1][0]
        ymin = box[0][1]
        ymax = box[1][1]

        crop_img = img[ymin:ymax, xmin:xmax]
        crop_img = cv2.resize(crop_img, (94, 24))

        # 保存图片
        cv2.imencode('.jpg', crop_img)[1].tofile(os.path.join(save_path, lpr_label + '.jpg'))

print("共生成{}张".format(num))
