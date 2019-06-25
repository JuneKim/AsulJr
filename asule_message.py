from enum import Enum

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

class Message:
	_START = "$"
	_END = "*"

	def __init__(self):
		self.message_ = []
		self.stream_ = ""

	def createSetMessage(self, command_, type_, id1_, valList1_, id2_, valList2_):
		self.message_.append(Command(command_).name)
		self.message_.append(str(type_))
		self.message_.append(str(id1_))
		self.message_.extend([str(num) for num in valList1_])
		self.message_.append(str(id2_))
		self.message_.extend([str(num) for num in valList2_])

	def createGetMessage(self, command_, type_, id1_, id2_):
		self.message_.append(Command(command_).name)
		self.message_.append(type_)

	
	def createNotiMessage(self, command_, type_, id1_, valList1, id2_, valList2_):
		self.message_.append(Command(command_).name)
		self.message_.append(str(type_))
		self.message_.append(str(id1_))
		self.message_.extend([str(num) for num in valList1_])
		self.message_.append(str(id2_))
		self.message_.extend([str(num) for num in valList2_])


	def _calCheckSum(self, dataStr):
		csum = 0
		for ch in dataStr:
			csum += ord(ch)
		
		return 0xff - (0xff & csum) 

	def makeStream(self):
		dataStream = ",".join(self.message_)
		csum = self._calCheckSum(dataStream)
		checkSumStr = str(csum)

		self.stream_ = self._START + dataStream + self._END + checkSumStr
		return self.stream_

	def getStream(self):
		if len(self.stream_) == 0:
			self.makeStream()

		return self.stream_