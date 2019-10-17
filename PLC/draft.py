#import numpy as np
from serial import Serial

ser = Serial('/dev/ttyUSB0', 9600)

def serialIn():
	s = str('')
	print("waiting PLC send to PC")
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



def serialOut(x=0, y=0):
	serial_string = str.encode("  1234  5768", 'ASCII')
	result = ser.write(serial_string)
	print("Output:", result)
	# while True:
		# s = ser.read().decode('ASCII')
		# print('Input:', s)
		# result = ser.write(str.encode(s))
		# print("Output:", result)
		# print("waiting PLC send to PC")
		# s = ser.readline().decode('ASCII') #doc lien tuc, dung lai khi GAP \n
		# print('Input:', s)
		# if s == "COM 8\n":
		# 	result = ser.write(serial_string)
		# 	print("Output:", result)



if __name__ == '__main__':
	while True:
		while serialIn() == False:
			continue
		serialOut()