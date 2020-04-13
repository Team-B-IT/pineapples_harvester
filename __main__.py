from time import sleep
from tkinter import Tk
from threading import Thread
import copy

from PLC.PLCASync import PLC1, PLC2, State #quả lí các cờ PLC
from gui import App
from utils.realSenseDepth import realSenseStream
from detect import *
from PIL import Image
import operator #hỗ trợ kết nối cam và openCV

from yolo import YOLO

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

class HardwareControlThread(Thread):
    def __init__(self):
        super().__init__()
        # Thiết lập 2 luồng cho 2 tay cắt
        self.plcThread1 = PLC1('PLC 1', 'COM3', rs)
        self.plcThread2 = PLC2('PLC 2', 'COM4')
        self.cutTime = 0
        # self._stop_flag = None

    def run(self):
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
        config = tf.ConfigProto(gpu_options=gpu_options)
        # config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)
        set_session(sess)

        # bộ nhận diện
        detector = YOLO()

        print("Starting...")
        self.plcThread1.start()
        self.plcThread2.start()

        # self._stop_flag = False
        while True:
            # nếu đã quét 2 lần thì thôi, không cần quét nữa, đi tiếp
            
            # chờ lệnh chụp ảnh
            while self.plcThread1.imageInfo == None:
                continue

            imageInfo = self.plcThread1.imageInfo
            self.plcThread1.imageInfo = None
            image = Image.open(imageInfo['imagePath'])

            # cập nhật lại ảnh vừa chụp lên màn hình
            app.updatePhotoCanvasImage(image)

            # nhận diện dứa
            boxList = detector.raw_detect_image(image)

            # phân loại dứa theo mode
            boxList = classifyPineappleByMode(boxList, self.plcThread1.mode)

            # loại bỏ các box trùng lặp
            boxList = boxesAntiDuplication(boxList)

            # lấy tọa độ của cac box
            coordList = boxesToCoordinates(boxList, imageInfo['depthDataPath'])

            # vẽ box lên ảnh
            drawBoxesOnImage(image, boxList, coordList)
            # không nhận được quả nào
            # if len(coordList) == 0:
            #     self.resetPlcs()
            #     continue
            # lưu ảnh
            image.save('./result/' + imageInfo['imagePath'].split('/')[-1]) # luu anh, comment dong nay de tranh full memory]

            # cập nhật lại ảnh đã đánh box lên màn hình
            app.updatePhotoCanvasImage(image)      
            for box in coordList:
                # chia dứa ra 2 list cho 2 PLC
                if box['real_x'] < 0: # PLC 1
                    self.plcThread1.boxList.append(box) # them vao danh sach cat PLC 1
                    self.plcThread1.boxList.sort(key=operator.itemgetter('real_x'))
                else:
                    self.plcThread2.boxList.append(box) # them vao danh sach cat PLC 2
                    self.plcThread2.boxList.sort(key=operator.itemgetter('real_x'))
            
            while len(self.plcThread1.boxList) != 0 or len(self.plcThread2.boxList) != 0:
                if self.plcThread1.state == State.RESET or self.plcThread2.state == State.RESET:
                    # reset tức thời
                    self.cutTime = -1
                    break
                continue
            
            if self.cutTime < 0:
                self.cutTime = 0
                continue
            elif self.cutTime < 1:
                self.cutTime = self.cutTime + 1
                # không reset tay vội, cho nó chụp thêm xem con` dứa không
                self.plcThread1.state = State.TAKEIMAGE
                self.plcThread2.state = State.TAKEIMAGE
                continue
            else:
                self.cutTime = 0
                self.resetPlcs()
                continue

    def resetPlcs(self):
        # soft reset
        self.plcThread1.ser.serialOut(0, 0, 10)
        self.plcThread2.ser.serialOut(0, 0, 0)
        self.plcThread1.state = State.START
        self.plcThread2.state = State.START
    def join(self):
        # bật giao diện khi nhập luồng về __main__
        app.window.mainloop()
        controlThread.acquire()
        controlThread._stop()
        # tắt chương trình
        self.plcThread1.acquire()
        self.plcThread2.acquire()
        self.plcThread1._stop()
        self.plcThread2._stop()
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
