import xml.etree.ElementTree as ET
from os import getcwd
import os
from PIL import Image

classes = []
with open("./model_data/pineapple_classes.txt") as f:
    classes = list(line.replace('\n', '') for line in f)
print (classes)


def convert_annotation(img_link, xml_link, list_file):
    try:
        Image.open(img_link)
        in_file = open(xml_link)
        # print(img_link, xml_link)
    except:
        return

    if os.path.getsize(img_link) < 5000 or os.path.getsize(xml_link) < 100:
        return
    
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('size'):
        w = int(obj.find('width').text)
        h = int(obj.find('height').text)

    list_file.write(img_link)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = list((int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text)))
       
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
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

    list_file.write("\n")

os.getcwd()
list_file = open("train.txt", "w")

for i in range(1, 13):
    jpg_folder = "./data/data/jpg/data" + ("0" + str(i))[-2:]
    xml_folder = "./data/data/xml/data" + ("0" + str(i))[-2:]
    for file in os.listdir(jpg_folder):
        extension = file[-4:]
        if extension != ".jpg":
            continue
        img_link = jpg_folder + "/" + file
        xml_link = xml_folder + "/" + file[:-4] + ".xml"
        print(img_link, xml_link)
        convert_annotation(img_link, xml_link, list_file)

list_file.close()
