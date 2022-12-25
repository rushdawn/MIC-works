import os
import shutil

import numpy as np
import json
from glob import glob
import cv2
from sklearn.model_selection import train_test_split
from os import getcwd


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def change_2_yolo5(files, txt_Name):
    imag_name=[]
    for json_file_ in files:
        json_filename = labelme_path + json_file_ + ".json"
        json_file = json.load(open(json_filename, "r", encoding="utf-8"))
        # image_path = labelme_path + json_file['imagePath']
        for i in list(json_file.keys()):
            out_file = open('%s/%s.txt' % (labelme_path+"/label", i), 'w')
            imag_name.append(i+'.jpg')
            height, width, channels = cv2.imread(labelme_path+"/images/"+i+".jpg").shape
            for j in range(len(list(json_file[i]["bbox"]))):
                label,xmin,ymin,xmax,ymax = list(json_file[i]["bbox"][j].values())
                if xmax <= xmin:
                    pass
                elif ymax <= ymin:
                    pass
                else:
                    cls_id = classes.index(label)
                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert((width, height), b)
                    out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                    # print(json_filename, xmin, ymin, xmax, ymax, cls_id)
    return imag_name

def image_txt_copy(files,scr_path,dst_img_path,dst_txt_path):
    """
    :param files: 图片名字组成的list
    :param scr_path: 图片的路径
    :param dst_img_path: 图片复制到的路径
    :param dst_txt_path: 图片对应的txt复制到的路径
    :return:
    """
    for file in files:
        img_path=scr_path+file
        print(file)
        shutil.copy(img_path, dst_img_path+file)
        scr_txt_path=scr_path+file.split('.')[0]+'.txt'
        shutil.copy(scr_txt_path, dst_txt_path + file.split('.')[0]+'.txt')


if __name__ == '__main__':
    classes = ['polyp']
    # 1.标签路径
    labelme_path = r"D:\Postgraduate Documents\Code\Python\YOLO_polyp_detection\Kvasir-SEG"
    # 3.获取待处理文件
    # files = glob(os.join.path(labelme_path, "*.json"))
    # files = [i.split("/")[-1].split(".json")[0] for i in files]
    files = ["kavsir_bboxes"]
    for i in files:
        print(i)
    # trainval_files, test_files = train_test_split(files, test_size=0.1, random_state=55)
    # # split
    # train_files, val_files = train_test_split(trainval_files, test_size=0.1, random_state=55)
    train_name_list=change_2_yolo5(files, "train")
    # print(train_name_list)
    # val_name_list=change_2_yolo5(val_files, "val")
    # test_name_list=change_2_yolo5(test_files, "test")
    # #创建数据集文件夹。



    file_List = ["train", "val", "test"]
    for file in file_List:
        if not os.path.exists('./VOC/images/%s' % file):
            os.makedirs('./VOC/images/%s' % file)
        if not os.path.exists('./VOC/labels/%s' % file):
            os.makedirs('./VOC/labels/%s' % file)
    image_txt_copy(train_name_list, labelme_path, './VOC/images/train/', './VOC/labels/train/')
    # image_txt_copy(val_name_list, labelme_path, './VOC/images/val/', './VOC/labels/val/')
    # image_txt_copy(test_name_list, labelme_path, './VOC/images/test/', './VOC/labels/test/')

