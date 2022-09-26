# ===============================================================
# Main script For Checklist A5 Task 
# Managing the communication between RPi and STM, RPi and Android
# ===============================================================

from multiprocessing import Process, Queue   # Manage multi-process programming
import time

from STM import STM 
# import Android
from Algo import Algo

import base64
import os
import glob
import socket

# ===============================================================================================
# Read msg frm Alg, STM or AND and put message into the queue, need to put into queue because u may receive msg frm diff devices at the same time
def readMsg(queue, interface): 
    while True: #keep trying until message is received
        try:
            msg = interface.read() #This is making use of OODP polymorphsim where the method to be called frm is based on the interface defined at runtime. Read is in all 3 files
            if msg is None: #msg is null meaning rpi didnt receive ath
                continue #The continue keyword is used to end the current iteration in a loop and continues to the next iteration. So rpi will keep trying to read until it receives sth
            if msg is not None:
                queue.put(msg) #Put item into the queue 
                return 1 #successful

        except Exception as e:
            print(f"[READ MSG ERROR]: {str(e)}")

#Passing message 
def msg_passing(msg): #pass in the message that u read frm andriod 
    if len(msg) != 0:
        message = msg.split('|', 1) #split the message into two list separated by |
        if len(message)!= 2: #Return the number of items in a list #did not split correctly
            return    

        # Msg FOR STM
        if message[0] == 'STM': #Encoded 
            print("IN STM")
            # Msg frm Android or algo to stm 
            # print('AND/ALG > %s : %s' % (str(message[0]), str(message[1])))
            print('Message from RPI: %s' % str(message[1]))
            stm_msg = message[1] #actual message            
            #print("STM MSG:", stm_msg)

            #Send the message u received frm andriod to STM so rpi main job is just in passing messages ard so it doesnt need a message script or hv its own message!!
            interfaces[0].write(stm_msg) #STM = 0 so this is calling interfaces[0] = STM() so its like calling STM().write() whr rpi will write/send the msg to STM-polymorphism 
            #print("Successful read: " , stm_msg)

            #print("Movement CMD Complete")

        # Msg for Alg (frm AND)
        if message[0] == 'ALG': 
            print("FOR ALG")
            print('FRM AND > %s : %s' % (str(message[0]), str(message[1])))
            alg_msg = message[1]            

            interfaces[ALG].write(alg_msg) #write into ALG

        # Msg for AND (frm STM)
        #if message[0] == 'AND': 
        #    print("FOR AND")
        #    # print('FRM STM > %s : %s' % (str(message[0]), str(message[1])))
        #    print('Message from RPI: %s' % str(message[1]))
        #    and_msg = message[1]            

#             interfaces[AND].write(and_msg) #write into AND
        return 1 #successful
    
# ===============================================================================================


if __name__ == '__main__':

    print("Initialistion of Multiprocessor...")
    
# Test communication with Andriod 
    interfaces = []
    interfaces.append(STM()) 
    # interfaces.append(Android())
    # interfaces.append(Algo())
    # Index of the interfaces in the list
#     STM = 0
#     AND = 1 
#     ALG = 2
    # Set up a queue to support manage messages received by the interfaces
    queue = Queue() #Constructor for a FIFO queue
    
    stm = Process(target=readMsg, args=(queue, interfaces[0])) #target = the function that u wanna run
    # algo = Process(target=readMsg, args=(queue, interfaces[ALG])) #read msg frm alg
    # stm = Process(target=readMsg, args=(queue, interfaces[STM]))
    
    for interface in interfaces:
        print(interface)
        interface.connect() # connect STM first, then Android #so this will be like calling STM.connect()
        
    #Start #need to explicitely start the process so that it will start running
    # android.start() # RPI starts to receive message from Android 
    # algo.start()
    stm.start()
    
    print("Multiprocess communication started.")

    #read msg frm andriod
    try:
        while True:
            # Read message
#             print("Awaiting Message........")
#             print("Peaking Q: ")
#             msg = queue.get() #Remove and return an item from the queue. 
#             print("Received msg: ", msg)

            # Send message
            print("Now writing message to STM........")
            msg = "STM|1"
            msg_passing(msg) 
            print("msg status:", msg)

            if msg == -1:
                break

            if msg is None: # No msg in the queue
                continue

    except Exception as e:
        print(f"[MAIN ERROR] {str(e)}")

    #finally:
#         for i in interfaces:
#             i.disconnect()
#         camera.close()
#         print("[MAIN] Camera closed.")
#         
#         print("Terminating the process")
#         stm.terminate()  # Terminate the process
#         print("STM read message process terminated.")
#         







