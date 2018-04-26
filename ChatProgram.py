from socket import *
# import socket
import threading
import random


def udpServer():
    serverPort = 12000
    sequenceNum = '0'
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("The server is ready to receive")
    while True:  # loop forever
        received = random.random()  # generate a random float between 0 and 1.0
        message, clientAddress = serverSocket.recvfrom(2048)  # receive message
        message = message.decode()

        if received < 0.6:  # ignore this packet for testing timeout
            if message[0] == sequenceNum:  # if this was the sequence number we are expecting
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


def udpClient():
    sequenceNum = '0'
    # serverName = '192.168.0.11'
    serverName = input('Input server name')
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(2.0)
    while True:

        message = input('Input chat message:')  # get message
        message = sequenceNum + message  # append sequence number to beginning
        clientSocket.sendto(message.encode(), (serverName, serverPort))  # send message
        ackReceived = False
        while not ackReceived:  # repeat until we receive an acknowlegement.
            received = random.random()  # generate a random float between 0 and 1.0
            try:
                modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
                modifiedMessage = modifiedMessage.decode()
                if received < 0.6:  # ignore this packet
                    if modifiedMessage == sequenceNum:  # proper ACK received
                        ackReceived = True
                        if sequenceNum == "0":  # flip expected sequence number
                            sequenceNum = "1"
                        else:
                            sequenceNum = "0"
                    else:
                        clientSocket.sendto(message.encode(),
                                            (serverName, serverPort))  # wrong ACK received, resend message
                else:
                    print("client ignored ACK!")
            except:
                clientSocket.sendto(message.encode(), (serverName, serverPort))  # timeout encountered.  Resend.

    clientSocket.close()


def run():
    client = threading.Thread(target=udpServer)
    server = threading.Thread(target=udpClient)
    client.start()
    server.start()


run()

"""
Input chat message:test15
message from: 127.0.0.1 sequence: 0 message: test15
Input chat message:test16
server ignored message!
server ignored message!
server ignored message!
server ignored message!
message from: 127.0.0.1 sequence: 1 message: test16
client ignored ACK!
server ignored message!
client ignored ACK!
server ignored message!
Input chat message:test17
server ignored message!
message from: 127.0.0.1 sequence: 0 message: test17

"""
