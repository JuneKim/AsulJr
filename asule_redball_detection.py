from asule_detection import AsuleDetection

import numpy as np
import cv2
import logging
import os

class AsuleRedballDetection(AsuleDetection):

	def run(self):
		#print ('AsuleRedballDetection running')
		ret, frame = self._capture.read()
		if not ret:
			logging.debug ('error: fail to get image')
			return (0, 0, 0, frame)
		frame = cv2.flip(frame, -1)
		frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		''' may need to modify range '''
		threshLow = cv2.inRange(frameHSV, (0, 100, 100), (10, 255, 255))
		threshHigh = cv2.inRange(frameHSV, (160, 100, 100), (179, 255, 255))
		#cv2.imshow('origin', frame)
		#cv2.imshow('hsv', frameHSV)
		#cv2.imshow('threshLow', threshLow)
		#cv2.imshow('threshHigh', threshHigh)

		frameRed = cv2.addWeighted(threshLow, 1.0, threshHigh, 1.0, 0.0)
		frameRed = cv2.GaussianBlur(frameRed, (9, 9), 3, 3)


		frameRed = cv2.dilate(frameRed, np.ones((5, 5), np.uint8))
		frameRed = cv2.erode(frameRed, np.ones((5, 5), np.uint8))
		
		#cv2.imshow('frameRed', frameRed)
		rows, cols = frameRed.shape

		circles = cv2.HoughCircles(frameRed, cv2.HOUGH_GRADIENT, 2, rows/4)
		idx = 0
		x = y = r = 0.0
		maxx = maxy = maxr = 0.0
		if circles is not None:
			for circle in circles[0]:
				''' circles found @ (x, y)'''
				x, y, r = circle
				if x !=  0.0 and y != 0.0 and r != 0.0:
					cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
					cv2.circle(frame, (x, y), r, (0, 0, 255), 3)
					logging.debug("circle({},{})".format(x, y))
					break

		return (x, y, r, frame)

	def stop(self):
		pass
