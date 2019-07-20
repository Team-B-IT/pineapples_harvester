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
		self.physic = {'x': 195, 'y': 195}
		self.delta = {'x': 30, 'y': 30}

	def serialIn(self):
		s = str('')
		# while self.ser.in_waiting == False:
		# 	continue
		s = self.ser.readline().decode('ASCII') # serial read until caught '\n'
		return s

	def serialOut(self, x, y):
		# x, y = random.randrange(0,180, 1), random.randrange(0,180, 1)
		# x = physic['x']//2 - int(x)
		# y = physic['y'] - int(y)
		# print ('Machine POV:', y, x)
		# x = x - delta['x']
		# y = y - delta['y']
		x = 90 - int(x)
		y = 190 - int(y)
		# chi gui toa do trong tam cat
		if 0 <= x <= 190 and 0 <= y <= 190: 
		
			print ('Xilanh POV :', y, x)
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

if __name__ == '__main__':
	PLC_IO('/dev/ttyUSB0').serialOut()