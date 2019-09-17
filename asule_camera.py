from asule_detection import AsuleDetection
from asule_redball_detection import AsuleRedballDetection
from asule_face_detection import AsuleFaceDetection
from asule_message import AsuleMessage, Type

from threading import Thread, Lock
from enum import Enum
import cv2
import logging
import os
import time

class AsuleCameraMode(Enum):
	_ASULE_REDBALL_DETECTION = 1
	_ASULE_FACE_DETECTION = 2

class AsuleCamera:
	_MODE = AsuleCameraMode._ASULE_FACE_DETECTION
	_X = 0
	_Y = 0
	_R = 0
	
	def __init__(self, tasks):

		self._tasks = tasks
		""" constructor, setting initial variables """
		self._sleepperiod = 1.0

		self.stream = cv2.VideoCapture(0)
		self.stream.set(cv2.CAP_PROP_FPS, 60)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
		self.read_lock = Lock()
		(self.grabbed, self.frame) = self.stream.read()
		self.started = False
		self.leftx = 320 / 4
		self.rightx = 320 / 4 * 3


	def start(self):
		if self.started:
			logging.error('already started')
			return None
		self.started = True
		self.thread = Thread(target=self.run, args = ())
		self.thread.start()
		return self
		

	def run(self):
		if self._MODE == AsuleCameraMode._ASULE_REDBALL_DETECTION:
			detection = AsuleRedballDetection(self.stream)
		elif self._MODE == AsuleCameraMode._ASULE_FACE_DETECTION:
			detection = AsuleFaceDetection(self.stream)
		
#		while not self._stopevent.isSet() and capture.isOpened():
		while self.stream.isOpened():
			x = y = r = z = 0.0
			(x, y, r, z, frame) = detection.run()
			if r != 0.0:
				logging.debug("returns {},{},{}".format(x, y, r))
				#TODO
				msg = AsuleMessage()
				msg.createSetMessage(1, Type.SERVO_MOTOR.value, 0, [1])
				self._tasks.put_nowait(msg)
				logging.debug ("added:" + str(msg))
				if x < self.leftx:
					logging.debug("left....")
				elif x > self.rightx:
					logging.debug("right...")
				else:
					logging.debug("center...")

			self.read_lock.acquire()
			self.frame = frame
			self.read_lock.release()
			time.sleep(0.01)

	def read(self):
		self.read_lock.acquire()
		frame = self.frame.copy()
		self.read_lock.release()
		return frame		

	def join(self, timeout=None):
		""" Stop the thread """
		threading.Thread.join(self, timeout)

	'''
	while True:
		tasks.put_nowait("ABCD")

	tasks.task_done()
	'''
