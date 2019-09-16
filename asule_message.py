from enum import Enum
import logging

class Type(Enum):
	DC_MOTOR = 1
	SERVO_MOTOR = 2
	SUPERSONIC = 3
	IMU = 4
	MODE = 5
	BEEP = 6
	LED = 7

class Command(Enum):
	SET = 1
	GET = 2
	NOTI = 3

class AsuleMessage:
	_START = "$"
	_END = "*"

	def __init__(self):
		self.message_ = []
		self.stream_ = str()

	def createSetMessage(self, command_, type_, id1_ = -1, valList1_ = [], id2_ = -1, valList2_ = []):
		self.message_.append(Command(command_).name)
		self.message_.append(str(type_))
		if id1_ is not -1:
			self.message_.append(str(id1_))
			self.message_.extend([str(num) for num in valList1_])
		if id2_ is not -1:
			self.message_.append(str(id2_))
			sel.message_.extend([str(num) for num in valList2_])
		self._makeStream()

	def createGetMessage(self, command_, type_, id1_, id2_):
		self.message_.append(Command(command_).name)
		self.message_.append(type_)
		self._makeStream()

	
	def createNotiMessage(self, command_, type_, id1_ = -1, valList1 = [], id2_ = -1, valList2_ = []):
		self.message_.append(Command(command_).name)
		self.message_.append(str(type_))
		if id1_ is not -1:
			self.message_.append(str(id1_))
			self.message_.extend([str(num) for num in valList1_])
		if id2_ is not -1:
			self.message_.append(str(id2_))
			self.message_.extend([str(num) for num in valList2_])
		self._makeStream()


	def _calCheckSum(self, dataStr):
		csum = 0
		for ch in dataStr:
			csum += ord(ch)
		
		return 0xff - (0xff & csum) 

	def _makeStream(self):
		dataStream = ",".join(self.message_)
		csum = self._calCheckSum(dataStream)
		#logging.debug("checksum:{:#x}".format(csum))
		checkSumStr = str(hex(csum)[2:])

		self.stream_ = self._START + dataStream + self._END + checkSumStr
		return self.stream_

	def getStream(self):
		if len(self.stream_) == 0:
			self.makeStream()

		return self.stream_

	def isEmpty(self):
		return not len(self.message_)

	def __str__(self):
		return str(self.stream_)
	
	def __repr__(self):
		return self.stream_
