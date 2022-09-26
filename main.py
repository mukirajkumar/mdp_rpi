# ===============================================================
# Main script For Checklist A5 Task 
# Managing the communication between RPi and STM, RPi and Android
# ===============================================================

from multiprocessing import Process, Queue   # Manage multi-thread programming
import time

from STM import STM
from Android import Android

import base64
import os
import glob
import socket

# ===============================================================================================
# Read and put message into the queue
def readMsg(queue, interface):
    while True:
        try:
            msg = interface.read()
            if msg is None:
                continue
            if msg is not None:
                queue.put(msg)
        except Exception as e:
            print(f"[READ MSG ERROR]: {str(e)}")

def msg_passing(msg):
    if len(msg) != 0:
        message = msg.split('|', 1)
        if len(message)!= 2:
            return    

        if message[0] == 'STM':
            print("IN STM")
            print('AND/ALG > %s : %s' % (str(message[0]), str(message[1])))
            stm_msg = message[1]            
            #print("STM MSG:", stm_msg)
            interfaces[STM].write(stm_msg)
            #print("Successful read: " , stm_msg)

            #print("Movement CMD Complete")
        return 1
    
# ===============================================================================================


if __name__ == '__main__':

    print("Initialistion of Multiprocessor...")
    
    # List of Interfaces - STM32F board, Android, Algo
    interfaces = []
    interfaces.append(STM())
    interfaces.append(Android())
    # Index of the interfaces in the list
    STM = 0
    AND = 1 #1
    # Set up a queue to support manage messages received by the interfaces
    queue = Queue()
    
    # Create Process objects
    android = Process(target=readMsg, args=(queue, interfaces[AND]))
    
    # Establish connections between RPi and all other interfaces
    for interface in interfaces:
        print(interface)
        interface.connect() # connect STM first, then Android
        
    #Start
    android.start() # Starts to receive message from Android 
    
    print("Multiprocess communication started.")

    try:
        while True:
            # Retrieve messages
            print("Awaiting Message........")
            print("Peaking Q: ")
            msg = queue.get()
            print("getted msg: ", msg)
            msg = msg_passing(msg)
            print("msg_after:", msg)
            if msg == -1:
                break

            if msg is None: # No msg in the queue
                continue
                
    except Exception as e:
        print(f"[MAIN ERROR] {str(e)}")

    finally:
        for i in interfaces:
            i.disconnect()
        camera.close()
        print("[MAIN] Camera closed.")
        
        print("Terminating the process")
        android.terminate()  # Terminate the process
        print("Android read message process terminated.")
        









