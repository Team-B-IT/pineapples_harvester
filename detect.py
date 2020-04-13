import os
from PIL import ImageDraw, ImageFont

from utils.DepthTool import DepthTool
import utils.image2coord as i2c
from utils import utils

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

        # log
        print('Depth: ', depth)
        print ('Camera POV (X,Y,Z):', rx, ry, rz)
        print('Score: ', box['score'])

    return pineappleCoordinateList

# Loại bỏ các box cùng khoanh vào 1 quả dứa
# NOTE: kỹ thuật xử lý hiện tại chỉ cho phép tránh 2 box của cùng 1 quả dứa đè lên nhau.
# boxList: danh sách các box đã phân loại
# return : danh sách các box sau khi đã loại bỏ trùng lặp
def boxesAntiDuplication(boxList):
    resultBoxList = []
    boxCount = len(boxList)
    for box1 in boxList:
        duplicated = False
        for box2 in resultBoxList:
            boxCollision = utils.rectangleCollision(box1['box'], box2['box'])

            box1Area = utils.rectangleArea(box1['box'])
            box2Area = utils.rectangleArea(box2['box'])
            boxCollisionArea = utils.rectangleArea(boxCollision)
            # 80% diện tích của box1 nằm trong box2, ta chọn box1 (box1Area < box2Area, box1 là body)
            if boxCollisionArea / box1Area >= 0.8:
                resultBoxList.remove(box2)
                break
            elif boxCollisionArea / box2Area >= 0.8:
                duplicated = True
                break
        if duplicated == False:
            resultBoxList.append(box1)
    return resultBoxList

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

if __name__ == "__main__":
    # test anti duplication
    # trường hợp đơn giản
    # print(boxesAntiDuplication([
    #     {'top':0, 'bottom': 10, 'left': 0, 'right': 10},
    #     {'top':6, 'bottom': 9, 'left': -1, 'right': 11},
    # ]))
    # trường hợp không xảy ra: 3 box đè nhau (tuy nhiên vẫn nên xét tới)
    # nó cho kết quả không mong muốn khi có > 2 box cùng khoanh vào 1 quả dứa
    # print(boxesAntiDuplication([
    #     {'top':2, 'bottom': 8, 'left': 2, 'right': 8},
    #     {'top':0, 'bottom': 10, 'left': 0, 'right': 10},
    #     {'top':6, 'bottom': 9, 'left': -1, 'right': 11},
    # ]))
    # trường hợp có thể xảy ra: quả dứa A có box body lọt vào box full của quả dứa B, song, quả dứa B cũng hiện box body
    # print(boxesAntiDuplication([
    #     {'top':1, 'bottom': 6, 'left': 2, 'right': 8},
    #     {'top':0, 'bottom': 10, 'left': 0, 'right': 10},
    #     {'top':6, 'bottom': 9, 'left': -1, 'right': 11},
    # ]))

    print(utils.rectangleCollision(
        {'top':40, 'bottom': 40, 'left': 50, 'right': 50},
        {'top':20, 'bottom': 20, 'left': 30, 'right': 30},
    ))