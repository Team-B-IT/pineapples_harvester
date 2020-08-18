#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from PIL import Image, ImageTk #hỗ trợ xử lí khung ahrn
from tkinter import messagebox


# from PLC.PLCASync import PLC1, PLC2, State #quả lí các cờ PLC
# from threading import Thread


# from utils.realSenseDepth import realSenseStream #hàm tính chiều sâu camera
# class HardwareControlThread(Thread):
#     def __init__(self):
#         super().__init__()
#         # Thiết lập 2 luồng cho 2 tay cắt
#         self.plcThread1 = PLC1('PLC 1', 'COM5', rs)
#         self.plcThread2 = PLC2('PLC 2', 'COM6')

class App: # Giao dien hien thi

    def __init__(self, window, window_title, rs):

        self.window = window
        self.window.title(window_title)
        self.window.geometry("1920x1080")  # Dinh nghia kich thuoc man hinh (Xmax=1920; Ymax=1080)
        self.realSenseStream = rs # luồng camera
        self.background_label = tkinter.Label(window, bg='grey')
        self.background_label.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.delay = 40

        # Dinh kich thuoc khung video
        self.liveStreamCanvas = tkinter.Canvas(self.background_label)
        # self.liveStreamCanvas = tkinter.Canvas(window, width=self.realSenseStream.width, height=self.realSenseStream.height)
        self.liveStreamCanvas.place(relx=0.003, rely=0.1,relheight=0.85, relwidth=0.499999)   #relx TOA DO GOC TRUC X; rely TOA DO GOC TRUC Y; relheight CHIEU CAO KHUNG VIDEO=1920*0.85; relwidth CHIEU RONG KHUNG VIDEO=1080*0.49   

        # Dinh kich thuoc khung Anh  
        # self.liveStreamCanvas.place(relx=0.2,rely=0,relwidth=0.6,relheight=0.6)
        self.photoCanvas = tkinter.Canvas(self.background_label)
        # self.liveStreamCanvas = tkinter.Canvas(window, width=self.realSenseStream.width, height=self.realSenseStream.height)
        self.photoCanvas.place(relx=0.5, rely=0.1,relheight=0.85, relwidth=0.497)
        # self.liveStreamCanvas.place(relx=0.2,rely=0,relwidth=0.6,relheight=0.6)
        # CAC CHU XUAT HIEN TREN MAN HINH
        #self.label2 = tkinter.Label(self.background_label, bg='salmon3', text="Pineapples Harvesting Machine",fg='white',font = ("helvetica",60))
        self.label2 = tkinter.Label(self.background_label, bg='salmon3', text="LIÊN HỢP MÁY THU HOẠCH KHÓM TỰ ĐỘNG",fg='white',font = ("helvetica",60))
        self.label2.place(relx=0.003, rely=0.001, relheight=0.09, relwidth=0.996)
        #cắt 1 lần
        self.btn1 = tkinter.Button(window,bg='salmon3', text="CẮT 1 LẦN", command=self.cat1,fg='yellow',)
        self.btn1.place(relx = 0.2514995, rely = 0.1 , relwidth = 0.001, relheight= 0.9)
        #cắt 2 lần
     #   self.btn2 = tkinter.Button(window,bg='salmon3', text="CẮT 2 LẦN", command=self.cat2,fg='yellow',)
       # self.btn2.place(relx = 0.249, rely = 0.67 , relwidth = 0.05, relheight= 0.1)
      #  #font dưới
      #  self.label2 = tkinter.Label(self.background_label, bg='salmon3')
     #   self.label2.place(relx=0.003, rely=0.785, relheight=0.22, relwidth=0.996)
    #    #Nút Start
     #   self.btn2 = tkinter.Button(window,bg='Blue', text="Start", command=self.start,fg='white',font = ("helvetica",40))
   #     self.btn2.place(relx = 0.2, rely = 0.825 , relwidth = 0.2, relheight= 0.1)
  #      #nút Stop
 #       self.btn2 = tkinter.Button(window,bg='Red', text="Stop", command=self.stop,fg='White',font = ("helvetica",40))
#        self.btn2.place(relx = 0.4, rely = 0.825 , relwidth = 0.2, relheight= 0.1)
#        #nút Emergency
#        self.btn2 = tkinter.Button(window,bg='yellow', text="Reset", command=self.reset,fg='white',font = ("helvetica",40))
#        self.btn2.place(relx = 0.6, rely = 0.825 , relwidth = 0.2, relheight= 0.1)
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self._delete_window)
 #   # cắt 1 lần
    def cat1(self):
        self.cutTime = 0
        print ("chon cat 1 lan")
 #   #cắt 2 lần
 #   def cat2(self):
 #       self.cutTime = 1
 #       print ("chon cat 2 lan")
 #   def start(self):
 #       # soft reset
 #       self.cutTime = 0
 #       self.plcThread1.ser.serialOut(0, 0, 6)
 #       self.plcThread2.ser.serialOut(0, 0, 6)
 #       print("start")
 #       self.plcThread1.state = State.START
 #       self.plcThread2.state = State.START
 #   def stop(self):
 #       # soft reset
 #       self.cutTime = 0
 #       self.plcThread1.ser.serialOut(0, 0, 7)
 #       self.plcThread2.ser.serialOut(0, 0, 7)
 #       print("Stop")
 #       self.plcThread1.state = State.START
 #       self.plcThread2.state = State.START
 #   def reset(self):
 #       # soft reset
 #       self.cutTime = 0
 #       self.plcThread1.ser.serialOut(0, 0, 8)
 #       self.plcThread2.ser.serialOut(0, 0, 8)
 #       print("Reset")
 #       self.plcThread1.state = State.START
 #       self.plcThread2.state = State.START

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
        self.boxes_photo = boxes_photo.resize((930, 756))   # kich thuoc o anh hien thi
        self.boxes_photo = ImageTk.PhotoImage(image=self.boxes_photo)
        # cập nhật lên canvas
        self.photoCanvas.create_image(0, 0, image=self.boxes_photo,anchor=tkinter.NW)
