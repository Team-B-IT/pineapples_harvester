"""
	Threading for multiple PLC
"""
from threading import Thread

class PLCASync(Thread):
	def __init__(self, serialCtrl):
		super().__init__()
		self.ser = serialCtrl
		self.ready = False # flag tay cat dua
		self.take = False # flag chup anh

	def run(self):
		while True:
			s = self.ser.serialIn()
			
			

			# if len(s) != 0:
			# 	print('Received from PLC:', s)

			if s == self.ser.name + '\n':
				print('1')
				self.ready = True
				self.take = False
				
			if s == '1234567' + '\n':
				print('m')

				self.take = True
				# print (self.take)


			#print('Received from PLC:', s)