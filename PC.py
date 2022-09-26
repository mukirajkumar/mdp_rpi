import time
import socket
#from socket import *

#from config import WIFI_IP, WIFI_PORT, ALGORITHM_SOCKET_BUFFER_SIZE
from colorama import *
WIFI_IP = '192.168.36.36'
WIFI_PORT = 5180
# init(autoreset=True)

class Algo (object):
    def __init__(self):
        #disconnect()
        self.ip = WIFI_IP
        self.port = WIFI_PORT
        
        self.isConnected = False
        self.server = None
        self.client = None
        self.address = None
        
        print("socket: " , socket)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(1)

    def connect(self):
        while True:
            retry = False

            try:
                print(Fore.LIGHTYELLOW_EX + '[ALG-CONN] Listening for ALG connections...')

                if self.client is None:
                    self.client, self.address = self.server.accept()
                    print(Fore.LIGHTGREEN_EX + '[ALG-CONN] Successfully connected with ALG: %s' % str(self.address))
                    retry = False

            except Exception as e:
                print(Fore.RED + '[ALG-CONN ERROR] %s' % str(e))

                if self.client is not None:
                    self.client.close()
                    self.client = None
                retry = True

            if not retry:
                break

            print(Fore.LIGHTYELLOW_EX + '[ALG-CONN] Retrying connection with ALG...')
            time.sleep(1)

    def getisConnected(self):
        return self.isConnected

    def disconnect_all(self):
        try:
            if self.server is not None:
                self.server.shutdown(socket.SHUT_RDWR)
                self.server.close()
                self.server = None
                print(Fore.LIGHTWHITE_EX + '[ALG-DCONN] Disconnecting Server Socket')

            if self.client is not None:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                self.client = None
                print(Fore.LIGHTWHITE_EX + '[ALG-DCONN] Disconnecting Client Socket')

        except Exception as e:
            print(Fore.RED + '[ALG-DCONN ERROR] %s' % str(e))

    def disconnect(self):
        try:
            if self.client is not None:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                self.client = None
                print(Fore.LIGHTWHITE_EX + '[ALG-DCONN] Disconnecting Client Socket')

        except Exception as e:
            print(Fore.RED + '[ALG-DCONN ERROR] %s' % str(e))

    def read(self):
        try:
            ALGORITHM_SOCKET_BUFFER_SIZE = 2048
            data = self.client.recv(ALGORITHM_SOCKET_BUFFER_SIZE).strip().decode('utf-8')

            if len(data) > 0:
                return data

            return None

        except Exception as e:
            print(Fore.RED + '[ALG-READ ERROR] %s' % str(e))
            self.disconnect()
            raise e

    def write(self, message):
        try:
            self.client.send(message.encode('utf-8'))

        except Exception as e:
            print(Fore.RED + '[ALG-WRITE ERROR] %s' % str(e))
            self.disconnect_all
            raise e

# 
# if __name__ == '__main__':
#     ser = Algo()
#     ser.__init__()
#     ser.connect()
#     time.sleep(3)
#     print('Connection established')
#     while True: 
#         try:
#             ser.read_from_ALG()
#             ser.write_to_ALG('Received input!'.encode())
#         except KeyboardInterrupt:
#             print('Communication interrupted')
#             ser.disconnect_ALG()
#             break
