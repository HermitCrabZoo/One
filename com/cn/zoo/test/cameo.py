import cv2
import time
from com.cn.zoo.test.managers import CaptureManager,WindowManager


class Cameo(object):
	def __init__(self):
		self._windowManager=WindowManager("Cameo",self.onKeypress)
		self._captureManager=CaptureManager(cv2.VideoCapture(0),self._windowManager,True)

	def run(self):
		"""Run the main loop"""
		self._windowManager.createWindow()
		while self._windowManager.isWindowCreated:
			self._captureManager.enterFrame()
			frame=self._captureManager.frame

			# TODO:Filter the frame (Chapter 3).
			self._captureManager.exitFrame()
			self._windowManager.processEvents()

	def onKeypress(self,keycode):
		"""Handle a keypress.
		space   -> Take a screenshot.
		tab     -> Start/stop recording a screencast.
		escape  -> Quit.

		"""
		if keycode == 32:#space
			imageName="E:\\images\\Cameo\\screenshot"+str(time.time())+".png"
			self._captureManager.writeImage(imageName)
			print("grabbed screenshot:"+imageName)
		elif keycode==9:#tab
			if not self._captureManager.isWritingVideo:
				videoName="E:\\images\Cameo\\record.mp4"
				self._captureManager.startWritingVideo(videoName)
				print("starting record video:"+videoName)
			else:
				self._captureManager.stopWritingVideo()
				print("stopped record video!")
		elif keycode==27:#escape
			self._windowManager.destroyWindow()
			print("exit.")

if __name__=="__main__":
	Cameo().run()