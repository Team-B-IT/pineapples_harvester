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
			if s == self.ser.name + '\n':
				self.ready = True
				self.take = False
			#	print('Received from PLC:', s)
			if s == 'TAKEPHOTO' + '\n':
				self.take = True
			#print('Received from PLC:', s)