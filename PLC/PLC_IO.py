from time import sleep
import math
from math import cos, sin
from serial import Serial
import random
import struct

class PLC_IO():
	def __init__(self, PLCName, serialPort):
		self.name = PLCName
		self.ser = Serial(serialPort, 9600, timeout=2.0) # open serial port. example for serialPort: '/dev/ttyUSB0'
		self.physic = {'x': 200, 'y': 200}
		self.delta = {'x': 30, 'y': 30}

	def serialIn(self):
		c = '' # đọc vào từ serial
		t = 0 # tổng 
		a = 0 # giá trị đọc từ serial chuyển từ byte sang số nguyên
		sleep(0.02)
		buffer = b''
		while a != 10:
			c = self.ser.read()
			# if c != b'':
			# 	print(self.name, c)
			if c == b'':
				break
			buffer = buffer + c
			a = int.from_bytes(c, "big")
			t = t + a
			sleep(0.02)
		
		# print(buffer)
		self.ser.flushInput()
		return t

	def serialOut(self, x, y, z):
		self.ser.flushOutput()
		result1 = str(y)
		result2 = str(x)
		result3 = str(z)
		result1 = result1.rjust(6,' ')
		result2 = result2.rjust(6,' ')
		result3 = result3.rjust(6,' ')
		result_string = result1 + result2 + result3
		# result_string = '   ' + str(y) + '   ' + str(x) #+ '\n'
		serial_string = str.encode(result_string)
		print(self.name,'out :',serial_string)
		self.ser.write(serial_string)

if __name__ == '__main__':
	PLC_IO('/dev/ttyUSB0').serialOut()