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

print("Starting...")
detect = YOLO().raw_detect_image
take_image = realSenseStream('img').take_image
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', size=32)
hand_queue = queue.Queue(0)
boxList1 = []
boxList2 = []

#PLC1
plc1 = PLC_IO("PLC 1", '/dev/ttyUSB0')
plcThread1 = PLCASync(plc1)
plcThread1.start()

""" # PLC2
plc2 = PLC_IO("PLC 2", '/dev/ttyUSB1')
plcThread2 = PLCASync(plc2)
plcThread2.start()
"""

path, _ = take_image()
sleep(10)
print("Camera started.")

while True:
	while plcThread1.take == False:	
		continue # wait for pulse
	plcThread1.take = False

	print("Taking image...")
	path, _ = take_image() # chup anh
	image = Image.open(path)
	draw = ImageDraw.Draw(image) # khoi tao anh de luu
	print("Tsh! Detecting...")
	data = detect(image) # nhan dien dua'
	print("Detected.")

	for box in data['objects']:
		if box['class'] == 2: 
			rx, ry = to_coord(box['box']['x'], box['box']['y']) # chuyen toa do tu anh -> thuc

			draw.rectangle([box['box']['left'], box['box']['top'], box['box']['right'], box['box']['bottom']], outline=(255,0,0), width=10)
			campov = str(rx)+' '+str(ry)
			draw.text((box['box']['left'], box['box']['top']-35), campov, fill = (255, 0, 0), font = font)
			
			# xep cac toa do cho 2 tay cat
			if ry > 50: # PLC 1
				boxList1.append({'x': rx, 'y': ry, 'box': box}) # them vao danh sach cat PLC 1
			else:
				boxList2.append({'x': rx, 'y': ry, 'box': box}) # them vao danh sach cat PLC 1
				pass

	del draw

	image.save('./result/' + path.split('/')[-1]) # luu anh, comment dong nay de tranh full memory
	print("Image saved.")

	while len(boxList1) != 0 or len(boxList2) != 0:
		# print('upper half', len(boxList1), 'lower half', len(boxList2))
		if (plcThread1.ready == True and len(boxList1) != 0):
			obj = boxList1[-1]
			print('Pineapple at:', obj['x'], obj['y'], 'score =', obj['box']['score'])

			plc1.serialOut(obj['x'], obj['y']) # xuat toa do

			plcThread1.ready = False  # reset tay
			boxList1.pop() # loai bo qua dua da cat
		"""
		if (plcThread2.ready == True and len(boxList2) != 0):
			obj = boxList2[-1]
			print('Pineapple at:', obj['x'], obj['y'], 'score =', obj['box']['score'])

			plc2.serialOut(obj['x'], obj['y']) # xuat toa do

			plcThread2.ready = False  # reset tay
			boxList2.pop() # loai bo qua dua da cat
		"""
	# for box in data['objects']:
	# 	if box['class'] == 2:
	# 		print('Box x/y/score:', int(box['box']['x']), int(box['box']['y']), box['score'])
	# 		rx, ry = to_coord(box['box']['x'], box['box']['y'])
	# 		serialOut(rx, ry)
	# 	while serialIn() == False:
	# 		continue # wait for pulse