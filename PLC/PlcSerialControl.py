'''
Class thực hiện đọc ghi qua serial, có trả về nội dung

KHÔNG THÊM NỘI DUNG VÀO FILE NÀY
'''

from time import sleep
from serial import Serial

class PlcSerialPort():
	def __init__(self, serialPortName):
		self.sr = Serial(serialPortName, 9600, timeout=1.0) # open serial port. example for serialPort: '/dev/ttyUSB0'

	def serialIn(self):
		byte = None
		buffer = b''
		while byte in [b'\n', b'']:
			sleep(0.02) # chờ đường truyền ổn định
			self.sr.flushInput()
			byte = self.sr.read()
			buffer = buffer + byte
		return buffer

	def serialOut(self, x, y, z):
		assert (type(x) is int) and (type(y) is int) and (type(y) is int),\
			"Không cho phép gửi dạng dữ liệu này qua PlcSerial. Yêu cầu dữ liệu là số nguyên."
		buffer = str.encode('{:6d}{:6d}{:6d}'.format(x, y, z))
		self.sr.write(buffer)
		self.sr.flushOutput()
		return buffer