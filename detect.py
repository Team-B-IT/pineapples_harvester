import os
from PIL import ImageDraw, ImageFont

from utils.DepthTool import DepthTool
import utils.image2coord as i2c 

# danh sách các class nhận điện được từ ảnh
pineappleClasses = open("./model_data/pineapple_classes.txt", 'r').read()
pineappleClasses = pineappleClasses.split('\n')

# danh sách các class phân chia theo mode
modeClasses = {
    0: {'full baby pineapple', 'body baby pineapple'},
    1: {'full green pineapple', 'body green pineapple'},
    2: {'full ripe pineapple', 'body ripe pineapple'},
    3: {'full green pineapple', 'body green pineapple', 'full ripe pineapple', 'body ripe pineapple'}
}

# Nhận diện dứa
# image: ảnh lấy từ camera
# return boxList: tập các box nhận diện được
# def detectPineapple(image):
#     boxList = detector.raw_detect_image(image)
#     return boxList

# Phân loại dứa theo mode
# boxList: tập các box nhận diện được
# mode: mode được chọn
# return classifiedBoxList: tập các box đã lọc
def classifyPineappleByMode(boxList, mode):
    print("Classify pineapples")
    countPineapple = 0 # Đếm số dứa sẽ cắt
    selectClasses = modeClasses[mode]
    # print(pineappleClasses)
    classifiedBoxList = []
    for box in boxList['objects']:
        if  pineappleClasses[box['class']] in selectClasses:
            # tăng đếm
            countPineapple = countPineapple + 1
            classifiedBoxList.append(box)

    return classifiedBoxList

# Chuyển tọa độ của tất các các box
# boxList: các box đã được lọc theo mode
# depthDataFile: file text chứa thông tin độ sâu (tương đương với ảnh depth)
# return pineappleCoordinateList: danh sách các tọa độ tương ứng
def boxesToCoordinates(boxList, depthDataFile):
    pineappleCoordinateList = []
    depthTool = DepthTool()
    depthTool.readCord(depthDataFile)
    bias = 0.1
    gridSize = 10
    for box in boxList:
        # lấy độ sâu
        depth = depthTool.getDepthBoundingBox([box['box']['left'], box['box']['top'], box['box']['right'], box['box']['bottom']], gridSize, bias) * 100
        # lấy tọa box trong ảnh
        x = (box['box']['left'] + box['box']['right']) / 2
        y = box['box']['bottom']
        # chuyển về tọa độ thực
        rx, ry, rz = i2c.to_coord_from_depth(x, y, depth)
        # thêm tọa độ đã chuyển vào danh sách
        pineappleCoordinateList.append({ 'real_x': rx, 'real_y': ry, 'real_z': rz })
    return pineappleCoordinateList

# Vẽ các box lên ảnh
# image: ảnh cần vẽ lên 
# boxList: danh sách các box
# coordList: danh sách các tọa độ tương ứng với các box
# return pineappleCoordinateList: danh sách các tọa độ tương ứng
def drawBoxesOnImage(image, boxList, coordList):
    # font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', size=32)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.path.normpath("fonts/FreeMono.ttf"), 24)
    for i in range(len(boxList)):
        # xét box thứ i
        box = boxList[i]
        # tọa độ tướng ứng thứ i
        coord = coordList[i]
        # tọa độ chuyển sang string để vẽ lên ảnh 
        campov = "{0} {1} {2} {3} {4:.3f}".format(coord['real_x'], coord['real_y'], coord['real_z'], box['class'], box['score'])
        # vẽ lên ảnh
        draw.rectangle([box['box']['left'], box['box']['top'], box['box']['right'], box['box']['bottom']], outline=(255,0,0), width=10)
        # viết chữ lên ảnh
        draw.text((box['box']['left'], box['box']['top']-35), campov, fill = (255, 0, 0), font=font)