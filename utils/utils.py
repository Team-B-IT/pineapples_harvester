
# Lấy phần giao giữa 2 hình chữ nhật
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
    return resultRect

# Tính diễn tích hình chữ nhật
# rect: hình chữ nhật với các thuộc tính top, left, right, bottom
# return area: diện tích hình chữ nhật rect
def rectangleArea(rect):
    area = abs(rect['left'] - rect['right'])*abs(rect['top'] - rect['bottom'])
    return area