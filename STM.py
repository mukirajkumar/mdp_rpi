# ===============================================================
# Script to manage communication with STM32F Board 
# ===============================================================
# write all the stm functions here and u can call on them frm main.py
import serial #this is used for the serial communication
import time

class STM(object):

    # Initialise the connection with STM32F Board
    # Check the connection port again, baud rate = 115200 (given)
    def __init__(self, port='/dev/ttyUSB0'): # __init__ method lets the class initialize the object's attributes #self is an instance of the class
        self.port = port
        self.baudrate = 115200 #transfering a max of 115200 bits per sec
        self.isConnected = False #at first we set that its not connected to stm

    def connect(self):
        while not self.isConnected: #while not connected to stm board
            try:
                print("Establishing connection with STM Board ...")

                # Create a Serial instance named 'ser'
                self.ser = serial.Serial(self.port, self.baudrate, timeout = 120) #Initialise serial communication #parameters: serial device name, baud rate must use the same baurd rate as stm, timeout: this is a timeout for read operations. Here we set it to 1 second. It means that when we read from Serial, the program won’t be stuck forever if the data is not coming. After 120 second or reading, if not all bytes are received, the function will return the already received bytes
                # Check if the serial instance is open
                if (self.ser.is_open): #check if the port is open
                    print("[SUCCESSFUL CONNECTION]: Successfully established connection with STM Board.")
                    self.isConnected = True

            except Exception as e:
                print(f"[ERROR] Unable to establish connection with STM32 Board: {str(e)}")
                # Retry to connect
                print("Retrying to connect with STM Board ...")
                time.sleep(1) #sleep for 1s before trying agn since this is a while loop

    def disconnect(self):
        try:
            if (self.ser): #Check there is a serial instance created #only when the is an istance created then u can close it
                print("STM: Disconnecting from STM Board ...")
                self.ser.close() #close the port
                self.isConnected = False
        except Exception as e:
            print(f"[ERROR]: Unable to disconnect from STM Board: {str(e)}") 


    # Create Getter method - to check if connection with STM32F board is established
    def getisConnected(self):
        return self.isConnected
    
    #def callForStatus(self):
        
    # Read and process message from STM
    def read(self):
        #print("STM READ")
        try:
            #print("In read STM")
            #data = ""
            #while data
         #   print("0.1 sleep")
          #  time.sleep(0.1)
            #python often defaults to using UTF-8
            data = self.ser.read(1).decode("UTF-8") #You receive bytes when you read from Serial, and you have to convert (decode) those bytes into the appropriate data type. #read(1) means read 1 byte of data
           # print("Raw Data: ", data)
            if data == '' or data is None: # No data read #None means null
                return "No reply"
            print(f"[FROM STM] {data}")
            return data
            
        except Exception as e:
            print(f"[ERROR] STM Board read error: {str(e)}")


    # Write message to STM
    def write(self, message):
        try:
            # Ensure connection is established before sending a message
            if self.isConnected:
                for char in message: #STM might receive a list of commands eg. F, F, L, R (hv a timeout function for rpi to send over what it has received so far)
                    #You can only send bytes through Serial
                    #The encode() function will take the string and encode it for Serial.
                    self.ser.write(char.encode('UTF-8')) #write() to send data to stm
                    print(f"[SENT TO STM]: {char}")
                    time.sleep(0.1) #wait for 0.1s bfr sending the nxt char over
                    
                print("Before stm read:")
                #return self.read()
                
            else:
                print("[Error]  Connection with STM board is not established")
        except Exception as e:
            print("[Error] Unable to send message from STM: %s" % str(e))






