# ===============================================================
# Script to manage communication with Android Tablet
# ===============================================================

import time
import bluetooth
import os

class Android(object):
    MAC_ADDRESS = "B8:27:EB:3A:91:84"
    RFCOMM = 1

    # Initialise the connection with the Android tablet
    def __init__(self):
        self.isConnected = False
        self.client = None
        self.server = None
        RFCOMM_channel = 4
        uuid = "00001101-0000-1000-8000-00805F9B34FB"
        os.system('sudo hciconfig hci0 piscan')
        #host_mac = 'E4:5F:01:55:A5:52'
        self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        #self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        

        # bluetooth.advertise_service(
        #         self.server,
        #         "MDP_Grp36",
        #         service_id=uuid,
        #         service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS],
        #         profiles = [bluetooth.SERIAL_PORT_PROFILE],
        #         protocols = [bluetooth.OBEX_UUID])

    # Getter method to check is connection is established
    def getisConnected(self):
        return self.isConnected

    def connect(self):
        print(f"Waiting for connection with Android Tablet on RFCOMM channel {self.RFCOMM} ...")
        while self.isConnected == False:
            try:
                if self.client is None:
                    # Accepts the connection
                    self.server.bind((self.MAC_ADDRESS, self.RFCOMM))
                    self.server.listen(self.RFCOMM)
                    # self.port = self.server.getsockname()[1]
                    self.client, address = self.server.accept()
                    print(f"[SUCCESSFUL CONNECTION]: Successfully established connection with Android Tablet from {address}.")
                    self.isConnected = True
                    self.write("STATUS Update : Status Update 1|")
                    self.write("ROBOT Update : Robot Update 1|")
                    self.write("Target Update : Target Update 1|")

            except Exception as e:
                print(f"[ERROR] Unable to establish connection with Android: {str(e)}")
                self.client.close()
                self.client = None
                # Retry to connect
                print("Retrying to connect with Android Tablet ...")
                time.sleep(1)
                self.connect()


    def disconnect(self):
        try:
            print("Android: Shutting down Bluetooth Server ...")
            self.server.shutdown(socket.SHUT_RDWR)
            self.server.close()
            self.server = None
            print("Android: Shutting down Bluetooth Client ...")
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            self.client = None
            self.isConnected = False
        except Exception as e:
            print("f[ERROR]: Unable to disconnect from Android: {str(e)}")

    def read(self):
        try:
            while True:
                msg = self.client.recv(512).strip().decode('utf-8')
                if len(msg) == 0:
                    break
                print(f"[FROM ANDROID] {msg}")
                return msg

        except Exception as e:
            print(f"[ERROR] Android read error: {str(e)}")
            # Retry connection if Android gets disconnected
            try:
                self.socket.getpeername()
            except:
                self.client.close()
                self.isConnected = False
                self.client = None
                print("Retrying to connect with Android Tablet ...")
                self.connect()
                print("Trying to read message from Android again...")
                self.read()
        return msg

    def write(self, message):
        try:
            if self.isConnected:
                self.client.send(message.encode('utf-8'))
                print(f"[SENT TO ANDROID]: {message}")
            else:
                print("[Error]  Connection with Android Tablet is not established")

        except Exception as e:
            print(f"[ERROR] Android write error: {str(e)}")
            # Retry connection if Android gets disconnected
            try:
                self.socket.getpeername()
            except:
                self.client.close()
                self.isConnected = False
                self.client = None
                print("Retrying to connect with Android Tablet...")
                self.connect()
                print("Trying to send the message to Android again...")
                write(self,message) # try writing again





