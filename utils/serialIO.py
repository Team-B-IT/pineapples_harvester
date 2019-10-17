#import numpy as np
import math
from math import cos, sin
from serial import Serial
import random
import struct

ser = Serial('/dev/ttyUSB0', 9600, timeout=100)

physic = {'x': 195, 'y': 195}
delta = {'x': 30, 'y': 30}
# pulse = {'x': 160, 'y': 160}

# def serialIn():
# 	s = str('')
# 	while ser.in_waiting:
# 		s = ser.read().decode('ASCII')
# 	# print ('Hardware:', s) # each byte
# 	# return True
# 	if s == '#':
# 		print ('OK')
# 	return s == '#'

# def serialOut(x, y):
# 	# x, y = random.randrange(0,180, 1), random.randrange(0,180, 1)
# 	x = physic['x']//2 - int(x)
# 	y = physic['y'] - int(y)
# 	print ('Machine POV:', y, x)
# 	x = x - delta['x']
# 	y = y - delta['y']
# 	# chi gui toa do trong tam cat
# 	if 0 <= x <= 165 and 0 <= y <= 165: 
	

# 		print ('Xilanh POV :', y, x)
# 	# ser.write(struct.pack('>B', y - delta['y']))
# 	# ser.write(b' ')
# 	# ser.write(struct.pack('>B', x - delta['x']))
# 	# ser.write(b'\n')
# 		result_string = str(y) + ' ' + str(x) + '\n'
# 		serial_string = str.encode(result_string)
# 	# print(serial_string)
# 		ser.write(serial_string)

# ser = Serial('/dev/ttyUSB0', 9600)

def serialIn():
	s = str('')
	print("Waiting for PLC send to PC")
	# while ser.in_waiting:
	# 	s = ser.read().decode('ASCII')
	# # print ('Hardware:', s) # each byte
	# # return True
	# if s == '#':
	# 	print ('OK')
	# return s == '#'
	a = False
	while True:	
		s = ser.readline().decode('ASCII') #doc lien tuc, dung lai khi GAP \n
		print('receive from PLC:', s)
		if s == "COM 8\n":
			# return True
			print('ok')
			a = True
			break
		else:
			print('bad')
			# return False
	return a



# def serialOut(x=0, y=0):
# 	serial_string = str.encode("  1234  2323", 'ASCII')
# 	result = ser.write(serial_string)
# 	print("Output:", result)
# 	# while True:
# 		# s = ser.read().decode('ASCII')
# 		# print('Input:', s)
# 		# result = ser.write(str.encode(s))
# 		# print("Output:", result)
# 		# print("waiting PLC send to PC")
# 		# s = ser.readline().decode('ASCII') #doc lien tuc, dung lai khi GAP \n
# 		# print('Input:', s)
# 		# if s == "COM 8\n":
# 		# 	result = ser.write(serial_string)
# 		# 	print("Output:", result)

def serialOut(x, y):
	# x, y = random.randrange(0,180, 1), random.randrange(0,180, 1)
	# x = physic['x']//2 - int(x)
	# y = physic['y'] - int(y)
	# print ('Machine POV:', y, x)
	# x = x - delta['x']
	# y = y - delta['y']
	x = 90 - x
	y = 190 - y
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
		ser.write(serial_string)

		
if __name__ == '__main__':
	serialOut()