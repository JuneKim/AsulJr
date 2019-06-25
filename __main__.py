from asule_serial import AsuleProtocol
from asule_message import Message
from asule_camera import AsuleCamera

import logging
import queue
import serial


# global setting
PORT = '/dev/ttyUSB0'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(thead)d,%(name)s %(levelname)s %(message)s')

g_tasks = queue.Queue()

def runTasks(p):
	if g_tasks.empty() == False:
		try:
			msg = g_tasks.get_nowait()
			p.write(msg.getStream())
		except:
			print ('Error:get_nowait')


def main():

	timerSec = 1
	# Run Camera / Img processing
	cam = AsuleCamera(g_tasks)
	#cam.setDaemon(True)
	cam.start()

	#if is_bt_on == True:
	#
	#else:
	try:
		ser = serial.serial_for_url(PORT, baudrate = 9600, timeout=1)
		with ReaderThread(ser, AsuleProtocol) as p:
			while p.isDone():
				# do something
				runTasks(p)
				time.sleep(timerSec)

	except serial.serialutil.SerialException:
		logging.error("fail to open serial port")

if __name__ == '__main__':
	main()