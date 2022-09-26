import socket
import picamera
import time
import sys
from STM import STM

host = "192.168.9.6"  # The server's hostname or IP address 
port = 54321  # The port used by the server



def captureImage():
    # Generate the picture's name
    print('[RPI_INFO] Initializing Camera.')
    camera = picamera.PiCamera()
    camera.resolution = (2592, 1944)
    camera.framerate = 30
    camera.vflip = True
    camera.hflip = True
    camera.brightness = 55
    camera.start_preview()

    print('[RPI_INFO] Warming up camera...')
    print('[RPI_INFO] Camera warmed up and ready')

    picName = 'img_1.jpg'
    picPath = "/home/group9/taken_images/"
    completePath = picPath + picName
    camera.capture(completePath)
    print("We have taken a picture.")
    camera.stop_preview()
    camera.close()
    return completePath


def msgClient():
    newClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newClient.connect((host, port))
    if(newClient!=None):
        print('Client 2 connected to server')
    try:
        message = newClient.recv(1024)
    except Exception as exception:
        print('RPI failed read from server via wifi' + str(exception))
    else:
        if message is not None and len(message)>0:
            print('Message read from server')
            message = message.decode('utf-8')
            print('Received: ' + str(message))
            newClient.close()
            print('Client 2 received message')
            return str(message)

        

    # #message = 'halp'
    # print('received not decoded: ' +str(message))
    # message = message.decode('utf-8')
    # print('Received: ' + str(message))  # depending on the label; call for stm to do appropriate movements
    # newClient.close()
    # print('Client 2 received message')
    # return str(message)

#capture of image, automatic sending of image to server on PC
class Client():
    def imageClient(self):
        print("entering imgClient function")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("socket done")
        client.connect((host, port))
        print('Client 1 connected to server')

        captureImage()
        print("image captured")
        image = open(path, 'rb')
        imageData = image.read(2048)
        while imageData:
             client.send(imageData)
             imageData = image.read(2048)
        print('Finished sending image')
        image.close()
        client.close()
        print('Client 1 closed')
        time.sleep(3)
        msgClient()


# if __name__ == "__main__":
#     imageClient()
#     sys.exit(0)
