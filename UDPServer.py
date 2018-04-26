import socket
import random
from socket import *


def run():
    host = "localhost"
    port = 12000
    sequenceNum = '0'
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', port))

    while True:
        received = random.random()  # generate a random float between 0 and 1.0
        message, clientAddress = serverSocket.recvfrom(2048)
        message = message.decode()

        if received < 0.6:
            if message[0] == sequenceNum:
                print("message from: " + clientAddress[0] + " sequence: " + message[0] + " message: " + message[1:])
                ack = sequenceNum
                serverSocket.sendto(ack.encode(), clientAddress)
                if sequenceNum == "0":
                    sequenceNum = "1"
                else:
                    sequenceNum = "0"
            else:
                ack = message[0]
                serverSocket.sendto(ack.encode(), clientAddress)
        else:  # packet was ignored.  Print that
            print("server ignored message!")

if __name__ == "__main__":
    run()
