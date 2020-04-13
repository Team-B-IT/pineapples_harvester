from time import sleep
from enum import Enum
from threading import Thread
from PLC.PlcSerialControl import PlcSerialPort
from config import config as CONFIG

class PlcState(Enum):
	PAUSE = 0
	AVAILABLE = 1
	BUSY = 2
	NOJOBS = 3

class PlcJobList():
	def __init__(self):
		self.jobs = []

	def new(self, jobsList: list):
		self.jobs = jobsList

	def empty(self):
		return len(self.jobs) == 0

	def get(self):
		assert not self.empty(), \
			"Empty list error."
		return self.jobs[-1]

	def pop(self):
		assert not self.empty(), \
			"Empty list error."
		self.jobs.pop()

class Plc():
	def __init__(self, plcName, serialPortName):
		self.initPosition = None
		self.state = PlcState.PAUSE
		self.name = plcName
		self.queue = PlcJobList()
		self.serialPort = PlcSerialPort(serialPortName)
		self.listener = PlcListener(self)
		self.responder = PlcResponder(self)
		self.runTimes = 0
		self.limitedRunTimes = CONFIG.limitedCutTimes

	def start(self):
		assert self.initPosition is not None, \
			"Chưa thiết lập lệch quay về khi cắt đủ số lần."
		self.listener.start()
		self.responder.start()

	def stop(self):
		self.listener.acquire()
		self.responder.acquire()
		self.listener._stop()
		self.responder._stop()

class PlcListener(Thread):
	def __init__(self, plcObject):
		super().__init__()
		self.plc = plcObject
		self.queue = self.plc.queue
		self.sr = self.plc.serialPort

	def run(self):
		__State = PlcState.PAUSE
		while True:
			sleep(0.001)
			stateCode = 0
			buffer = self.sr.serialIn()
			for byte in buffer:
				stateCode = stateCode + byte
			if stateCode != 0:
				print("Nhận {0}: Dữ liệu gốc {1} - mã {2}".format(self.plc.name, buffer, stateCode))
			if stateCode == 397: # 397=Reset
				__State = self.plc.state
				self.plc.state = PlcState.PAUSE
			if self.plc.state is PlcState.PAUSE and stateCode in [139, 140]:
				self.plc.state = __State
			if self.plc.state is PlcState.BUSY and stateCode in [80]: # 80=cắt xong| 81,92=chọn mode nhưng bỏ qua
				self.queue.pop()
				self.plc.state = PlcState.AVAILABLE
			if self.plc.state is PlcState.PAUSE and stateCode in [81, 92]:
				self.plc.state = PlcState.NOJOBS

class PlcResponder(Thread):
	def __init__(self, plcObject):
		super().__init__()
		self.plc = plcObject
		self.queue = self.plc.queue
		self.sr = self.plc.serialPort

	def validate(self, x, y, z):
		# hàm này sẽ được gán khi khởi tạo 2 object Plc1 Plc2
		assert False, \
			"Chưa gán hàm [PlcResponder.validate()] kiểm tra tọa độ"
		return dict()

	def run(self):
		while True:
			sleep(0.001)
			if self.plc.state is PlcState.AVAILABLE:
				if not self.queue.empty():
					box = self.queue.get()
					packetBox = self.validate(box['real_x'], box['real_y'], box['real_z'])
					if packetBox is None: # tọa độ này không cho phép cắt
						self.queue.pop()
					else: # cho phép cắt
						buffer = self.sr.serialOut(packetBox['x'], packetBox['y'], packetBox['z'])
						self.plc.state = PlcState.BUSY
						print("Gửi {0}: {1}".format(self.plc.name, buffer))
				else:
					self.plc.state = PlcState.NOJOBS
					self.plc.runTimes = (self.plc.runTimes + 1) % self.plc.limitedRunTimes
					if self.plc.runTimes == 0:
						self.plc.state = PlcState.PAUSE
						x, y, z = [self.plc.initPosition[key] for key in self.plc.initPosition.keys()]
						buffer = self.sr.serialOut(x, y, z)
						print("Hết {0} lượt cắt. Gửi {1}: {2}".format(self.plc.limitedRunTimes, self.plc.name, buffer))
