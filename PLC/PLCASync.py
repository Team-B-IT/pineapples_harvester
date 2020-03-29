"""
	Threading for multiple PLC
	đọc dữ liệu từ 2 plc
"""
from threading import Thread
from enum import Enum

from .PLC_IO import PLC_IO

class State(Enum):
	START = 0, 		# Bước khởi động, chờ ảnh
	TAKEIMAGE = 1,		# Bước chụp ảnh
	CUTTING = 2, 		# Bước cắt, chờ cắt
	WAITING = 3, 		# Bước cắt xong
	STOP = 4, 			# Dừng chờ encoder hoặc RESET
	RESET = 5 			# Reset

class PLCASync(Thread):
	# Khởi tạo luồng chạy của một PLC
	# serialCtrl: cổng USB giao tiếp với PLC tương ứng
	def __init__(self, name, serialPort):
		super().__init__()
		self.ser = PLC_IO(name, serialPort) # bộ giao tiếp serial
		self.state = State.RESET # trạng thái ban đầu
		self.mode = None # mode cắt
		self.boxList = [] # số box còn lại cần phải cắt
		self.validator = None
		self.buffer = ''

	def run(self):
		while True:
			self.buffer = self.ser.serialIn()
			if self.buffer != 0:
				print(self.ser.name, ':', self.buffer)
			if self.state == State.RESET or self.buffer == 397:
				self.state = State.RESET
				self.plcReset()
			elif self.state == State.START:
				self.plcStart()
			elif self.state == State.TAKEIMAGE:
				self.plcTakeImage()
			elif self.state == State.CUTTING:
				self.plcCut()
			elif self.state == State.WAITING:
				self.plcWait()
			elif self.state == State.STOP:
				print(self.ser.name, ": Stop.")
				return

	# lệnh reset
	def plcReset(self):
		self.state = State.START
		self.boxList = []
		print(self.ser.name, ": Reset.")

	# lệnh start chụp ảnh
	def plcStart(self):
		self.state = State.TAKEIMAGE
		print(self.ser.name, ": Start.")

	# chụp ảnh
	def plcTakeImage(self):
		self.state = State.WAITING

	# lệnh cắt xong
	def plcCut(self):
		if self.buffer == 160: # Cắt xong
			self.state = State.WAITING
			self.boxList.pop() # loại bỏ box đã cắt
			print(self.ser.name, ": Cắt xong.")

	# chờ box để cắt
	def plcWait(self):
		if len(self.boxList) != 0:
			# xét box cuối cùng trong boxList
			box = self.boxList[-1]
			print('Pineapple at:', box['real_x'], box['real_y'], box['real_z'])# ghi chú đã bỏ hiển thị score, 'score =', obj['box']['score'])

			# chuyển tọa độ sang dạng để truyền tới PLC
			packetBox = self.validator(box['real_x'], box['real_y'], box['real_z'])

			if packetBox is None:
			# tọa độ này không cho phép cắt
				self.boxList.pop()
				return
			# cho phép cắt
			self.ser.serialOut(packetBox['x'], packetBox['y'], packetBox['z'])
			self.state = State.CUTTING
			print(self.ser.name, ": Đang cắt.")

class PLC1(PLCASync):
	def __init__(self, name, serialPort, realSense):
		super(PLC1, self).__init__(name, serialPort)
		self.validator = self.plc1CoordinateValidator
		self.rs = realSense
		self.imageInfo = None

	# lệnh reset
	def plcReset(self):
		if self.buffer == 397: #RESET
			super(PLC1, self).plcReset()

	# lệnh chụp ảnh
	def plcStart(self):
		self.mode = None
		if self.buffer == 81: #TAKEPHOTOG
			self.mode = 3
			print('Cắt: XANH, CHÍN')
		if self.buffer == 92: #TAKEPHOTOR
			self.mode = 2
			print('Cắt: CHÍN')
		if self.mode != None:
			# chuyển sang trạng thái chụp ảnh
			self.state = State.TAKEIMAGE

	# thực hiện chụp
	def plcTakeImage(self):
		print('Đang chụp ảnh.')
		print("Taking image...")
		path, dataPath, _ = self.rs.take_image() # chup anh
		self.imageInfo = {
			'imagePath': path,
			'depthDataPath': dataPath
		}
		self.state = State.WAITING
		print('Chụp xong.')

	# kiểm tra tọa độ có hợp lệ không
	def plc1CoordinateValidator(self, raw_x, raw_y, raw_z):
		#y = int(raw_y)-59-21, -59 (mép ngoài) là khoảng cách từ camera đến khung, 21 từ khung đến trục thân xilanh trục y
		y = 212-17-int(raw_y)    # chieu truc X cua camera# doi tu toa do cam sang toa do khung PLC1 #80
		if y < 0 and abs(y) <= 5:
			y = 0
		#x = 100-20, 100 là giới hạn một nửa khoảng thu hoạch (mép trong), 20 thân xylanh đến khung theo trục x
		x = 100-20 + int(raw_x)   # chieu truc Y cua camera # doi tu toa do cam sang toa do khung PLC1 #184

		if int(raw_z) < 40 :
			z = 3
		if int(raw_z) >= 40 and int(raw_z) <= 80 :
			z = 4
		if int(raw_z) > 80:
			z = 5
		print ('Xi lanh 1 POV -PLC1:', x, y, z)
		if 0 <= y <= 170 and  0 <= x <= 81:
			# Nếu nằm trong tầm cắt trả về tọa độ
			return {'x': x, 'y': y, 'z': z}
		# Không nằm trong tầm cắt thì không trả về gì
		print(self.ser.name, ": Ngoài khoảng cắt.")
		return None

class PLC2(PLCASync):
	def __init__(self, name, serialPort):
		super(PLC2, self).__init__(name, serialPort)
		self.validator = self.plc2CoordinateValidator

	# kiểm tra tọa độ có hợp lệ không
	def plc2CoordinateValidator(self, raw_x, raw_y, raw_z):
		y = 200-int(raw_y)-5   # chieu truc X cua camera# doi tu toa do cam sang toa do khung PLC2 #80
		if y < 0 and abs(y) <= 5:
			y = 0
		x = 100-26 - int(raw_x) # chieu truc Y cua camera # doi tu toa do cam sang toa do khung PLC2

		if int(raw_z) < 30 :
			z = 3
		if int(raw_z) >= 30 and int(raw_z) <= 50 :
			z = 4
		if int(raw_z) > 50 :
			z = 5
		print ('Xi lanh 2 POV -PLC2:', x, y, z)
		if 0 <= y <= 170 and  0 <= x <= 81:
			# Nếu nằm trong tầm cắt trả về tọa độ
			return {'x': x, 'y': y, 'z': z}
		# Không nằm trong tầm cắt thì không trả về gì
		print(self.ser.name, ": Ngoài khoảng cắt.")
		return None