from time import sleep
from tkinter import Tk
from threading import Thread
import copy

from gui import App
from utils.realSenseDepth import realSenseStream
from utils.detect import *
from PLC.PlcControl import Plc, PlcState
from PIL import Image
import operator #hỗ trợ kết nối cam và openCV

from yolo import YOLO

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from PLC.PlcValidator import *

class HardwareControlThread(Thread):
    def __init__(self):
        super().__init__()
        # Thiết lập 2 luồng cho 2 tay cắt
        self.plc1 = Plc('PLC 1', 'COM3')
        self.plc1.initPosition = {'x':0, 'y':0, 'z':10}
        self.plc1.responder.validate = plc1CoordinateValidator

        self.plc2 = Plc('PLC 2', 'COM4')
        self.plc2.initPosition = {'x':0, 'y':0, 'z':10}
        self.plc2.responder.validate = plc2CoordinateValidator

    def run(self):
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
        config = tf.ConfigProto(gpu_options=gpu_options)
        # config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)
        set_session(sess)

        # bộ nhận diện
        detector = YOLO()

        print("Starting...")
        self.plc1.start()
        self.plc2.start()

        # self._stop_flag = False
        while True:
            sleep(0.002)
            # khi 2 tay hết việc
            if self.plc1.state is PlcState.NOJOBS and self.plc2.state is PlcState.NOJOBS:
                path, dataPath, _ = rs.take_image() # chup anh
                print('Chụp ảnh xong.')
                image = Image.open(path)
                app.updatePhotoCanvasImage(image) # cập nhật lại ảnh vừa chụp lên màn hình
                boxList = detector.raw_detect_image(image) # nhận diện dứa
                boxList = classifyPineappleByMode(boxList) # phân loại dứa theo mode
                boxList = boxesAntiDuplication(boxList) # loại bỏ các box trùng lặp
                coordList = boxesToCoordinates(boxList, dataPath) # lấy tọa độ của cac box
                drawBoxesOnImage(image, boxList, coordList) # vẽ box lên ảnh
                # image.save('./result/' + imageInfo['imagePath'].split('/')[-1]) # luu anh, comment dong nay de tranh full memory
                app.updatePhotoCanvasImage(image)  # cập nhật lại ảnh đã đánh box lên màn hình

                list1 = []
                list2 = []
                for box in coordList: # chia dứa ra 2 list cho 2 PLC
                    if box['real_x'] < 0: # PLC 1
                        list1.append(box) # them vao danh sach cat PLC 1
                    else:
                        list2.append(box) # them vao danh sach cat PLC 2
                list1.sort(key=operator.itemgetter('real_x'))
                list2.sort(key=operator.itemgetter('real_x'))
                self.plc1.queue.new(list1)
                self.plc2.queue.new(list2)
                self.plc1.state = PlcState.AVAILABLE
                self.plc2.state = PlcState.AVAILABLE

    def join(self):
        # bật giao diện khi nhập luồng về __main__
        app.window.mainloop()
        controlThread.acquire()
        controlThread._stop()
        # tắt chương trình
        self.plc1.stop()
        self.plc2.stop()
        sleep(0.2)
        super().join()

if __name__ == "__main__":
    global rs, app
    rs = realSenseStream('./running_data')
    # chạy luồng điều khiển
    controlThread = HardwareControlThread()
    controlThread.start()

    # khởi chạy giao diện
    app = App(Tk(), "PINEAPPLE", rs)
    app.realSenseStream = rs
