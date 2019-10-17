#import numpy as np
import math
from math import cos, sin
from serial import Serial
import random
import struct

class PLC_IO(Serial):
	def __init__(self, PLCName, serialPort):
		self.name = PLCName
		self.ser = Serial(serialPort, 9600, timeout=100) # open serial port. example for serialPort: '/dev/ttyUSB0'
		self.physic = {'x': 200, 'y': 200}
		self.delta = {'x': 30, 'y': 30}

	def serialIn(self):
		s = str('')
		c = ''
		while c != '\n':
			c = self.ser.read().decode('ASCII')
			s = s + c
		#s = self.ser.readline().decode('ASCII') # serial read until caught '\n'	
		return s

	def serialOut(self, x1, y1):
		# x, y = random.randrange(0,180, 1), random.randrange(0,180, 1)
		# x = physic['x']//2 - int(x)
		# y = physic['y'] - int(y)
		# print ('Machine POV:', y, x)
		# x = x - delta['x']
		# y = y - delta['y']
		if self.name == "PLC 1":
			x = int(y1)-50-18    # chieu truc X cua camera# doi tu toa do cam sang toa do khung PLC1 #80
			if x < 0 and abs(x) <= 5:
				x = 0
			y = 100-19 - int(x1)   # chieu truc Y cua camera # doi tu toa do cam sang toa do khung PLC1 #184
			print ('Xilanh POV -PLC1:',x,y)
		else:
			x = int(y1)-21-50   # chieu truc X cua camera# doi tu toa do cam sang toa do khung PLC2 #80
			if x < 0 and abs(x) <= 5:
				x = 0
			y = 100-24+int(x1) # chieu truc Y cua camera # doi tu toa do cam sang toa do khung PLC2
			print ('Xilanh POV -PLC2:')

		
		# chi gui toa do trong tam cat
		if 0 <= x <= 180 and 0 <= y <= 81: #sửa lại phần này
		
			print ('POV: ', x, y)
		# ser.write(struct.pack('>B', y - delta['y']))
		# ser.write(b' ')
		# ser.write(struct.pack('>B', x - delta['x']))
		# ser.write(b'\n')
			result1 = str(y)
			result2 = str(x)
			result1 = result1.rjust(6,' ')
			result2 = result2.rjust(6,' ')
			result_string = result1 + result2
			# result_string = '   ' + str(y) + '   ' + str(x) #+ '\n'
			serial_string = str.encode(result_string)
			print(serial_string)
			self.ser.write(serial_string)
			return True
		return False

if __name__ == '__main__':
	PLC_IO('/dev/ttyUSB0').serialOut()