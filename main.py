from yolo import YOLO
# from utils.serialIO import serialIn, serialOut 
from utils.PLC_IO import PLC_IO
from utils.image2coord import to_coord
from utils.realSense import realSenseStream
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from PLC.PLCASync import PLCASync
import queue
import numpy as np

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
config = tf.ConfigProto(gpu_options=gpu_options)
#config.gpu_options.allow_growth = True 
sess = tf.Session(config=config)
set_session(sess)

print("Starting...")
detect = YOLO().raw_detect_image
take_image = realSenseStream('img').take_image
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', size=32)
hand_queue = queue.Queue(0)
boxList1 = []
boxList2 = []

# PLC1
plc1 = PLC_IO("PLC 1", '/dev/ttyUSB0')
plcThread1 = PLCASync(plc1)
plcThread1.start()

# PLC2
plc2 = PLC_IO("PLC 2", '/dev/ttyUSB1')
plcThread2 = PLCASync(plc2)
plcThread2.start()

print("Camera started.")
#B1: Nhận takephoto từ PLC1
#B2: Camera chụp ảnh và detect
#B3: Chuyển sâng tọa độ cam và gửi lên PLC
#B4: Quay lại vòng lặp

while True:
	print("Wait")
	print(plcThread1.take)
	while plcThread1.take == False:	
		print(plcThread1.take)
		sleep(5)
		continue # wait for pulse
	plc1.ser.flushInput()
	print("Taking image...")
	path, _ = take_image() # chup anh
	image = Image.open(path)
	draw = ImageDraw.Draw(image) # khoi tao anh de luu
	print("Tsh! Detecting...")
	data = detect(image) # nhan dien dua'
	print("Detected.")
	count_dua = 0
	for box in data['objects']:
		if  box['class'] == 3:
			count_dua += 1 
			rx, ry = to_coord(box['box']['x'], box['box']['y']) # chuyen toa do tu anh -> thuc
			draw.rectangle([box['box']['left'], box['box']['top'], box['box']['right'], box['box']['bottom']], outline=(255,0,0), width=10)
			campov = str(rx)+' '+str(ry)
			draw.text((box['box']['left'], box['box']['top']-35), campov, fill = (255, 0, 0), font = font)
			print(box['score'], box['box']['left'], box['box']['top']-35) 
			# xep cac toa do cho 2 tay cat
			if rx>0: # PLC 1
				boxList1.append({'x': rx, 'y': ry, 'box': box}) # them vao danh sach cat PLC 1
			else:
				boxList2.append({'x': rx, 'y': ry, 'box': box}) # them vao danh sach cat PLC 1
				pass

	del draw

	print("Count ", count_dua)
	image.save('./result/' + path.split('/')[-1]) # luu anh, comment dong nay de tranh full memory
	print("Image saved.")
	
	plcThread1.ready = False
	plcThread1.take = False
	plcThread2.ready = False
	plcThread2.take = False
	while len(boxList1) != 0 or len(boxList2) != 0:
		# print('upper half', len(boxList1), 'lower half', len(boxList2))
		if (plcThread1.ready == True and len(boxList1) != 0):
			obj = boxList1[-1]
			print('Pineapple at:', obj['x'], obj['y'], 'score =', obj['box']['score'])
			plc1.ser.flushOutput()
			if plc1.serialOut(obj['x'], obj['y']) == True: # xuat toa do
				plcThread1.ready = False  # reset tay
			boxList1.pop() # loai bo qua dua da cat

		if (plcThread2.ready == True and len(boxList2) != 0):
			obj = boxList2[-1]
			print('Pineapple at:', obj['x'], obj['y'], 'score =', obj['box']['score'])
			plc2.ser.flushOutput()
			if plc2.serialOut(obj['x'], obj['y']) == True: # xuat toa do
				plcThread2.ready = False  # reset tay
			boxList2.pop() # loai bo qua dua da cat
		
	# for box in data['objects']:
	# 	if box['class'] == 2:
	# 		print('Box x/y/score:', int(box['box']['x']), int(box['box']['y']), box['score'])
	# 		rx, ry = to_coord(box['box']['x'], box['box']['y'])
	# 		serialOut(rx, ry)
	# 	while serialIn() == False:
	# 		continue # wait for pulse