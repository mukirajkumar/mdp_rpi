import socket
import picamera
import time
import sys
from STM import STM

camera = picamera.PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 30
camera.vflip = True
camera.hflip = True
camera.brightness = 55
camera.start_preview()

print('[RPI_INFO] Warming up camera...')
print('[RPI_INFO] Camera warmed up and ready')

picName = 'image1.jpg'
picPath = "/home/group9/taken_images"
completePath = picPath + picName
camera.capture(completePath)
print("We have taken a picture.")
camera.stop_preview()
camera.close()