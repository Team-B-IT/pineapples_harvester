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

# thiết lập mode cắt (mặc định chỉ cắt chín)
modeConfigured = 2
# số lần cắt
limitedCutTimes = 2