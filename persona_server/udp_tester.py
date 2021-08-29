import socket
from datetime import time
from time import sleep
import random


address = "192.168.43.130"




serverAddressPort = (address, 3002)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
while True:
    expression = random.randint(1, 1)
    msgWithExpression = str("2,") + str(expression) + ","
    bytesToSend = str.encode(msgWithExpression)
    print("Sending " + msgWithExpression + " to " + address)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    sleep(0.5)
    msgWithFacePosition = str("1,") + str(0) + "," + str(0) + "," + str(0) + "," + str(0)
    bytesToSend = str.encode(msgWithFacePosition)
    print("Sending " + msgWithFacePosition + " to " + address)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    sleep(0.5)



#print(msg)