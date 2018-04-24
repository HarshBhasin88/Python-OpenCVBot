import cv2
import time
import numpy
import imutils
import picamera
import threading,Queue
import picamera.array
import Tkinter as tk
from Tkinter import *
import RPi.GPIO as gpio
from PIL import Image, ImageTk
from gpiozero import PWMOutputDevice
from picamera.array import PiRGBArray

#wheel_1A=20
#wheel_1B=26
#wheel_2A=22
#wheel_2B=23
#wheel_3A=17
#wheel_3B=18
#wheel_4A=19
#wheel_4B=16




class robot_view2:


	#gpio.setmode(gpio.BCM)
	#gpio.setup(wheel_1A,gpio.OUT)
        #gpio.setup(wheel_1B,gpio.OUT)

       # gpio.setup(wheel_2A,gpio.OUT)
       # gpio.setup(wheel_2B,gpio.OUT)

        #gpio.setup(wheel_3A,gpio.OUT)
        #gpio.setup(wheel_3B,gpio.OUT)

        #gpio.setup(wheel_4A,gpio.OUT)
        #gpio.setup(wheel_4B,gpio.OUT)




	def __init__(self,master):
		master.geometry("300x300")
		master.title("Omni Robot")


		self.btnFrame = Frame(mainwindow,width=300,height=300)
		self.btnFrame.pack()

		self.forwardBtn = Button(self.btnFrame,text="Forward",command=self. moveForward)
		self.forwardBtn.pack()
		self.forwardBtn.place(relx=.5,rely=.25,anchor="n")

		self.rightBtn = Button(self.btnFrame,text="right",command=self.goRight)
		self.rightBtn.pack()
		self.rightBtn.place(relx=.95,rely=.5,anchor="e")

		self.leftBtn = Button(self.btnFrame,text="left",command=self.goLeft)
		self.leftBtn.pack()
		self.leftBtn.place(relx=.05,rely=.5,anchor="w")

		self.RevBtn =  Button(self.btnFrame,text="Back",command=self.moveBack)
		self.RevBtn.pack()
		self.RevBtn.place(relx=.5,rely=.75,anchor="s")

		self.stopBtn = Button(self.btnFrame,text="Stop",command=self.stop)
		self.stopBtn.pack()
		self.stopBtn.place(relx=.5,rely=.5,anchor="ce")

		self.setup()

	def setup(self):

		gpio.setmode(gpio.BCM)

		self.wheel_3A = 17
               	self.wheel_3B = 18

		self.pwm_3A = PWMOutputDevice(self.wheel_3A,True,0,1000)
		self.pwm_3B = PWMOutputDevice(self.wheel_3B,True,0,1000)

               	self. wheel_2A = 22
               	self.wheel_2B = 23

		self.pwm_2A = PWMOutputDevice(self.wheel_2A,True,0,1000)
		self.pwm_2B = PWMOutputDevice(self.wheel_2B,True,0,1000)

               	self. wheel_4A = 19
               	self. wheel_4B = 16

		self.pwm_4A = PWMOutputDevice(self.wheel_4A,True,0,1000)
		self.pwm_4B = PWMOutputDevice(self.wheel_4B,True,0,1000)

                self.wheel_1A = 20
                self.wheel_1B = 26

		self.pwm_1A = PWMOutputDevice(self.wheel_1A,True,0,1000)
		self.pwm_1B = PWMOutputDevice(self.wheel_1B,True,0,1000)

                gpio.setup(self.wheel_1A,gpio.OUT)
                gpio.setup(self.wheel_1B,gpio.OUT)

                gpio.setup(self.wheel_2A,gpio.OUT)
                gpio.setup(self.wheel_2B,gpio.OUT)

                gpio.setup(self.wheel_3A,gpio.OUT)
                gpio.setup(self.wheel_3B,gpio.OUT)


		gpio.setup(self.wheel_4A,gpio.OUT)
		gpio.setup(self.wheel_4B,gpio.OUT)

	def moveForward(self):

		print "Forward"
		time.sleep(2)

		self.pwm_1A.value = 0
		self.pwm_1B.value = 1.0

		self.pwm_2A.value = 0.9
		self.pwm_2B.value = 0

		self.pwm_3A.value = 0
		self.pwm_3B.value = 0.9

		self.pwm_4A.value = 0
		self.pwm_4B.value = 0.9

	def moveBack(self):

		print ("Back")
		time.sleep(1)

		self.pwm_1A.value = 1.0
		self.pwm_1B.value = 0

                self.pwm_2A.value = 0
		self.pwm_2B.value = 0.9

                self.pwm_3A.value = 0.9
		self.pwm_3B.value = 0

                self.pwm_4A.value = 0.9
		self.pwm_4B.value = 0


	def goRight(self):

		print ("Right")
		time.sleep(1)

		self.pwm_2A.value = 0
		self.pwm_2B.value =1.0

	        self.pwm_3A.value = 0
		self.pwm_3B.value = 1.0

	        self.pwm_1A.value = 1.0
		self.pwm_1B.value = 0

	        self.pwm_4A.value = 0
		self.pwm_4B.value = 1.0

	def goLeft(self):

		print ("Left")
		time.sleep(1)

		self.pwm_2A.value = 1.0
		self.pwm_2B.value = 0

        	self.pwm_3A.value = 1.0
		self.pwm_3B.value = 0

	        self.pwm_1A.value = 0
		self.pwm_1B.value = 1.0

        	self.pwm_4A.value = 1.0
		self.pwm_4B.value = 0

	def stop(self):

		print("Stop")
		time.sleep(1)

		self.pwm_3A.value = 0
		self.pwm_3B.value = 0

		self.pwm_2A.value = 0
		self.pwm_2B.value = 0

		self.pwm_1A.value = 0
		self.pwm_1B.value = 0

		self.pwm_4A.value = 0
		self.pwm_4B.value = 0





	def ViewCam(self,qu,event):

		while event.is_set():
			#print "Inside Cam Thread \n"
			camera = picamera.PiCamera()
			camera.resolution=(640,480)
			camera.framerate = 32
			rawCapture = PiRGBArray(camera,size=(640,480))


			for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):
				global image
				image = frame.array
				qu.put(image)
				#print qu.qsize()
				self.DrawGui(qu)
				rawCapture.truncate(0)
				key = cv2.waitKey(1) & 0xFF

	def DrawGui(self,qu):

		#print  "Image size in Gui Thread \n"
		#print qu.qsize()

		image = qu.get()
		Canvas().create_window(300,150,window=cv2.imshow("camview",image))
		Canvas().pack()




event = threading.Event()
event.set()

qu = Queue.Queue()
mainwindow = Tk()
obj = robot_view2(mainwindow)
cameraProc = threading.Thread(target=obj.ViewCam, args=(qu,event))
cameraProc.start()
mainwindow.mainloop()
try:
	while event.is_set():
		#print "Thread is running"
		time.sleep(.5)
except KeyboardInterrupt:
		event.clear()
		cameraProc.join()
		print "Thread successfully closed" 
		gpio.cleanup()
#mainwindow.mainloop()
