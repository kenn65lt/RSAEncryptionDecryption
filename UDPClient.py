import socket
import threading
import random
from socket import *


sequenceNum = '0'
#serverName = '192.168.0.11'
serverName = input('Input server name')
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2.0)
while True:


    message = input('Input chat message:') #get message
    message = sequenceNum + message #append sequence number to beginning
    clientSocket.sendto(message.encode(), (serverName, serverPort)) #send message
    ackReceived = False
    while(not ackReceived): #repeat until we receive an acknowlegement.
        received = random.random()  # generate a random float between 0 and 1.0
        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            modifiedMessage = modifiedMessage.decode()
            if(received < 0.6): #ignore this packet
                if(modifiedMessage == sequenceNum): #proper ACK received
                    ackReceived = True
                    if(sequenceNum=="0"): #flip expected sequence number
                        sequenceNum = "1"
                    else:
                        sequenceNum = "0"
                else:
                    clientSocket.sendto(message.encode(), (serverName, serverPort)) #wrong ACK received, resend message
            else:
                print("client ignored ACK!")
        except:
            clientSocket.sendto(message.encode(), (serverName, serverPort)) #timeout encountered.  Resend.

clientSocket.close()