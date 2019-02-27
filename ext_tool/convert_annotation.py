import xml.etree.ElementTree as ET
from os import getcwd
import os
from PIL import Image

classes = []
with open("../model_data/bkseeing_classes.txt") as f:
    classes = list(line.replace('\n', '') for line in f)
print (classes)


def convert_annotation(image_id, list_file):
    # try:
    #     print("Trying")
    #     Image.open("BKSeeing/data-ver-1.2/"+image_id+".jpg")
    #     in_file = open("BKSeeing/data-ver-1.2/%s.xml"%(image_id))
    # except:
    #     return
    in_file = open("../../../data/BKSeeing/data-ver-1.2/%s.xml"%(image_id))
    # print("Success")
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('size'):
        w = int(obj.find('width').text)
        h = int(obj.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text) + 1, int(xmlbox.find('ymin').text) + 1, int(xmlbox.find('xmax').text) + 1, int(xmlbox.find('ymax').text) + 1)
        # if (b[0] not in range(1,w) or b[2] not in range(1,w)):
        #     continue
        # if (b[1] not in range(1,h) or b[3] not in range(1,h)):
        #     continue
        for i in range(4):
            if b[i] < 1:
                b[i] = 1
            elif (i == 0 or i == 2) and (b[i] > w):
                b[i] = w
            elif (i == 1 or i == 3) and (b[i] > h):
                b[i] = h
        if b[0] > b[2]:
            temp = b[2]
            b[2] = b[0]
            b[0] = temp
        if b[1] > b[3]:
            temp = b[1]
            b[1] = b[3]
            b[3] = temp
        list_file.write("../../../data/BKSeeing/data-ver-1.9/%s.jpg"%(image_id) + " " + ",".join([str(a) for a in b]) + ',' + str(cls_id) + '\n')

list_file = open("../train.txt", "w")
images_list = open("../ID.csv", "r")

print("Checkpoint_1")

images_id = list(line.replace('\n','') for line in images_list)

print("Checkpoint_2")

for image_id in images_id:
    print("/%s.jpg"%(image_id))
    convert_annotation(image_id, list_file)
list_file.close()
