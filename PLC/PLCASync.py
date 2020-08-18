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
		if self.buffer == 397: #RESET
			self.boxList = []
			self.state = State.START
			print(self.ser.name, ": Reset.")

	# lệnh start chụp ảnh
	def plcStart(self):
		self.boxList = []
		self.state = State.TAKEIMAGE
		print(self.ser.name, ": Start.")

	# chụp ảnh
	def plcTakeImage(self):
		self.state = State.WAITING

	# lệnh cắt xong
	def plcCut(self):
		if self.buffer == 80: # Cắt xong
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
		# y (là độ dài từ Y^home1 đến quả dứa có tọa độ thực so với cammera)
		# - khoảng Y^cammera đến home 1, home 2 là 215 + 55 = 270 cm . trong đó 215 là từ home12 đến mép trong của khung và 55 là k/c từ cam đến mép trong
		#sai số +-5cm
		y = 260  - int(raw_y) 
		# * Khoảng cách giữa X^home1, X^home2 là 165cm / ước lượng vùng hoạt động của X^home1=85 , Xhome2= 80 
		# x (là độ dài từ X^home1 đến quả dứa có tọa độ thực so với cammera)
		x = 85 + int(raw_x)   # chieu truc Y cua camera # doi tu toa do cam sang toa do khung PLC1 #184
		if y < 0 and abs(y) <= 5:
			y = 0
		if y > 180 and y < 220 : #gán giới hạn trên trục Y
			y = 185 
		if y > 43 and y < 58 :   #gán giới hạn dưới1 trục Y
			y = 51 
		if y >=58 and y < 65 :   # gán giới hạn dưới2 trục Y
			y = 55 
		if x <=25 and x >= 0  : # gán giới hạn dưới trục X
			x = 0
		if x <=35 and x >= 26  : # gán giới hạn dưới trục X
			x = 30
		if x <=85 and x >= 75  : # gán giới hạn dưới trục X
			x = 73
		#if y > 170 and x < 30: # gán giới hạn quả ngoài cùng hàng 1( gần cammera nhất)
		#	y = 185
		#	x = 5
		#if y > 145 and y<= 166 and x <= 18: # giới hạn quả ngoài cùng hàng 2 
		#	y = 145
		#	x = 5 
		if int(raw_z) < 70 :
			z = 3
		if int(raw_z) >= 70 and int(raw_z) <= 80 :
			z = 3
		if int(raw_z) > 80:
			z = 3
		print ('Xi lanh 1 POV -PLC1 x y z:', x, y, z)
		if 51 <= y <= 185 and  20 <= x <= 73:
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
		y = 257  - int(raw_y)
		x = 90 - int(raw_x)   
		if y < 0 and abs(y) <= 5:
			y = 0
		if y > 180 and y < 220 : #gán giới hạn trên trục Y
			y = 185 
		if y > 43 and y < 58 :   #gán giới hạn dưới1 trục Y
			y = 51 
		if y >=58 and y < 65 :   # gán giới hạn dưới2 trục Y
			y = 55 
		if x <=25 and x >= 0 : # gán giới hạn dưới trục X
			x = 0
		if x <=90 and x >= 65 : # gán giới hạn dưới trục X
			x = 73
		if x <=35 and x >= 26 : # gán giới hạn dưới trục X
			x = 30
		#if y > 170 and x < 30: # gán giới hạn quả ngoài cùng hàng 1( gần cammera nhất)
		#	y = 185
		#	x = 5
		#if y > 145 and y<= 166 and x <= 18: # giới hạn quả ngoài cùng hàng 2 
		#	y = 145
		#	x = 5 
		if int(raw_z) < 70 :
			z = 3
		if int(raw_z) >= 70 and int(raw_z) <= 80 :
			z = 3
		if int(raw_z) > 80:
			z = 3
		print ('Xi lanh 2 POV -PLC2 X Y Z:', x, y, z)
		if 51 <= y <= 185 and  20 <= x <= 73:
			# Nếu nằm trong tầm cắt trả về tọa độ
			return {'x': x, 'y': y, 'z': z}
		# Không nằm trong tầm cắt thì không trả về gì
		print(self.ser.name, ": Ngoài khoảng cắt.")
		return None
