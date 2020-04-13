import copy


# Lấy phần giao giữa 2 hình chữ nhật (HCN)
# rect1: hình chữ nhật 1
# rect2: hình chữ nhật 2
# return resultRect: hình chữ nhật là phần giao
def rectangleCollision(rect1, rect2):
    resultRect = {
        'top': max(rect1['top'], rect2['top']),
        'bottom': min(rect1['bottom'], rect2['bottom']),
        'left': max(rect1['left'], rect2['left']),
        'right': min(rect1['right'], rect2['right']),
    }
    nonCollisionRect = {
        'top': 0,
        'bottom': 0,
        'left': 0,
        'right': 0,
    }

    # Kiểm tra xem phần trùng có hợp lệ hay không
    if resultRect['top'] > resultRect['bottom'] or resultRect['left'] > resultRect['right']:
        return nonCollisionRect
    else:
        return resultRect

# Tính diễn tích hình chữ nhật
# rect: hình chữ nhật với các thuộc tính top, left, right, bottom
# return area: diện tích hình chữ nhật rect
def rectangleArea(rect):
    area = abs(rect['left'] - rect['right'])*abs(rect['top'] - rect['bottom'])
    return area

def checkPointInRectangle(point, rect):
    if point['x'] > rect['left']:
        return False
    if point['x'] < rect['right']:
        return False
    if point['y'] < rect['top']:
        return False
    if point['y'] > rect['bottom']:
        return False
    return True