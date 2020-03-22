#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from PIL import Image, ImageTk #hỗ trợ xử lí khung ahrn
from tkinter import messagebox

from utils.realSenseDepth import realSenseStream #hàm tính chiều sâu camera

class App: # Giao dien hien thi

    def __init__(self, window, window_title, rs):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1920x1080")
        self.realSenseStream = rs # luồng camera
        self.background_label = tkinter.Label(window, bg='grey')
        self.background_label.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.delay = 40

        # Tạo khung xem ảnh
        self.liveStreamCanvas = tkinter.Canvas(self.background_label)
        # self.liveStreamCanvas = tkinter.Canvas(window, width=self.realSenseStream.width, height=self.realSenseStream.height)
        self.liveStreamCanvas.place(relx=0.003, rely=0.1,relheight=0.85, relwidth=0.498)
        # self.liveStreamCanvas.place(relx=0.2,rely=0,relwidth=0.6,relheight=0.6)
        self.photoCanvas = tkinter.Canvas(self.background_label)
        # self.liveStreamCanvas = tkinter.Canvas(window, width=self.realSenseStream.width, height=self.realSenseStream.height)
        self.photoCanvas.place(relx=0.502, rely=0.1,relheight=0.85, relwidth=0.497)
        # self.liveStreamCanvas.place(relx=0.2,rely=0,relwidth=0.6,relheight=0.6)

        self.label2 = tkinter.Label(self.background_label, bg='salmon3', text="Pineapples Harvesting Machine",fg='white',font = ("helvetica",60))
        self.label2.place(relx=0.003, rely=0.001, relheight=0.09, relwidth=0.996)
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self._delete_window)

    # Tắt đi
    def _delete_window(self):
        print("Tắt chương trình.")
        try:
            self.window.destroy()
        except Exception as e:
            print(e)
            pass

    # Cập nhật các frame của camera
    def update(self):
        # Lấy ảnh tử realsense
        frame = self.realSenseStream.get_frame()
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        # cập nhật lên canvas
        self.liveStreamCanvas.create_image(0, 0, image=self.photo,anchor=tkinter.NW)
        # lặp lại update để giống với video

        self.window.after(self.delay, self.update)

    def updatePhotoCanvasImage(self, boxes_photo):
        # chỉnh độ phân giải ảnh
        self.boxes_photo = boxes_photo.resize((930, 756), Image.ANTIALIAS)
        self.boxes_photo = ImageTk.PhotoImage(image=boxes_photo)
        # cập nhật lên canvas
        self.photoCanvas.create_image(0, 0, image=self.boxes_photo,anchor=tkinter.NW)