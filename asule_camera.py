from asule_detection import AsuleDetection
from asule_redball_detection import AsuleRedballDetection
from asule_face_detection import AsuleFaceDetection

import threading
from enum import Enum
import cv2

class AsuleCameraMode(Enum):
	_ASULE_REDBALL_DETECTION = 1
	_ASULE_FACE_DETECTION = 2

class AsuleCamera(threading.Thread):
	_MODE = AsuleCameraMode._ASULE_REDBALL_DETECTION
	
	def __init__(self, tasks):

		self._tasks = tasks
		""" constructor, setting initial variables """
		self._stopevent = threading.Event()
		self._sleepperiod = 1.0

		threading.Thread.__init__(self, name = 'AsuleCamera')

	def run(self):
		capture = cv2.VideoCapture(0)
		if capture.isOpened() == False:
			logging.error('error: fail to open camera')
			os.system('pause')
			return

		capture.set(cv2.CAP_PROP_FPS, 60)
		capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
		capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

		if self._MODE == AsuleCameraMode._ASULE_REDBALL_DETECTION:
			detection = AsuleRedballDetection(capture)
		elif self._MODE == _AsuleCameraMode.ASULE_FACE_DETECTION:
			detection = AsuleFaceDetection(capture)
		
		while not self._stopevent.isSet() and capture.isOpened():
			msg = detection.run()
			if not msg.isEmpty():
				self._tasks.put_nowait(msg)

	def join(self, timeout=None):
		""" Stop the thread """
		self._stopevent.set()
		threading.Thread.join(self, timeout)

	'''
	while True:
		tasks.put_nowait("ABCD")

	tasks.task_done()
	'''