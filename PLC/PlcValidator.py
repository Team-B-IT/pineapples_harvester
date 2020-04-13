'''
File này gồm 2 hàm kiểm tra tọa độ trước khi gửi qua serial
'''
# kiểm tra tọa độ có hợp lệ không
def plc1CoordinateValidator(raw_x, raw_y, raw_z):
    #y = int(raw_y)-59-21, -59 (mép ngoài) là khoảng cách từ camera đến khung, 21 từ khung đến trục thân xilanh trục y
    #231 khoảng cách hai mép trong, 59 từ cam đến mép trong, 23 từ mép trong đến cánh tay
    y = 275  - int(raw_y)    # chieu truc X cua camera# doi tu toa do cam sang toa do khung PLC1 #80
    #x = 100-20, 100 là giới hạn một nửa khoảng thu hoạch (mép trong), 20 thân xylanh đến khung theo trục x
    #14 từ cánh tay đến mép trong
    x = 87 + int(raw_x)   # chieu truc Y cua camera # doi tu toa do cam sang toa do khung PLC1 #184
    if y < 0 and abs(y) <= 5:
        y = 0
    if y > 180 and y < 210 : #gán giới hạn trên trục Y
        y = 185
    if y > 43 and y < 58 :   #gán giới hạn dưới1 trục Y
        y = 51
    if y >=58 and y < 65 :   # gán giới hạn dưới2 trục Y
        y = 55
    if x <=10  : # gán giới hạn dưới trục X
        x = 3
    if y > 170 and x < 30: # gán giới hạn quả ngoài cùng hàng 1( gần cammera nhất)
        y = 185
        x = 5
    if y > 145 and y<= 166 and x <= 18: # giới hạn quả ngoài cùng hàng 2
        y = 145
        x = 5
    if int(raw_z) < 70 :
        z = 3
    if int(raw_z) >= 70 and int(raw_z) <= 80 :
        z = 4
    if int(raw_z) > 80:
        z = 5
    if 51 <= y <= 185 and  0 <= x <= 87:
        # Nếu nằm trong tầm cắt trả về tọa độ
        return {'x': x, 'y': y, 'z': z}
    # Không nằm trong tầm cắt thì không trả về gì
    return None

# kiểm tra tọa độ có hợp lệ không
def plc2CoordinateValidator(raw_x, raw_y, raw_z):
    #y = int(raw_y)-59-21, -59 (mép ngoài) là khoảng cách từ camera đến khung, 21 từ khung đến trục thân xilanh trục y
    #231 khoảng cách hai mép trong, 59 từ cam đến mép trong, 23 từ mép trong đến cánh tay
    y = 275  - int(raw_y)    # chieu truc X cua camera# doi tu toa do cam sang toa do khung PLC1 #80
    #x = 100-20, 100 là giới hạn một nửa khoảng thu hoạch (mép trong), 20 thân xylanh đến khung theo trục x
    #14 từ cánh tay đến mép trong
    x = 87 - int(raw_x)   # chieu truc Y cua camera # doi tu toa do cam sang toa do khung PLC1 #184
    if y < 0 and abs(y) <= 5:
        y = 0
    if y > 180 and y < 210 : #gán giới hạn trên trục Y
        y = 185
    if y > 43 and y < 58 :   #gán giới hạn dưới1 trục Y
        y = 51
    if y >=58 and y < 65 :   # gán giới hạn dưới2 trục Y
        y = 55
    if x <=10  : # gán giới hạn dưới trục X
        x = 3
    if y > 170 and x < 30: # gán giới hạn quả ngoài cùng hàng 1( gần cammera nhất)
        y = 185
        x = 5
    if y > 145 and y<= 166 and x <= 18: # giới hạn quả ngoài cùng hàng 2
        y = 145
        x = 5
    if int(raw_z) < 70 :
        z = 3
    if int(raw_z) >= 70 and int(raw_z) <= 80 :
        z = 4
    if int(raw_z) > 80:
        z = 5
    if 51 <= y <= 185 and  0 <= x <= 75:
        # Nếu nằm trong tầm cắt trả về tọa độ
        return {'x': x, 'y': y, 'z': z}
    # Không nằm trong tầm cắt thì không trả về gì
    return None