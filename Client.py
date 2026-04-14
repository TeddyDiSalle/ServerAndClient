##L10 Socket programming hands-on (TCP)
import threading
import GLOBALVARIABLES
from socket import *
serverName = "172.28.203.33"
#"192.168.1.2"
#'hostname'
#server's IP address (preciselyIPv4)'servername'
#serverName = "192.168.1.10"
#serverName = "10.128.236.24"
#serverName = "172.27.56.158"
#serverName = "192.168.194.219" #mobile hotspot IP
serverPort = 12001 #un-reserved port #

clientSocket = socket(AF_INET, SOCK_STREAM) #creates client side TCP socket
clientSocket.connect((serverName,serverPort)) # initiates TCP connection . After this line is executed, three-way handshake is performed and a

# TCP connection is established

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(GLOBALVARIABLES.socketBytes).decode() #receives a message up to 1024 bytes from server, and decodes it
        if message == "": #if connection is lost break out of processing loop
            break
        print('From Server: ', message) #prints the message from server


def send_messages(client_socket):
    while True:
        message = input() #reads a message from user input
        client_socket.send(message.encode()) #encodes and sends the message to server

import threading

clientSocket = socket(AF_INET, SOCK_STREAM) #creates client side TCP socket
clientSocket.connect((serverName,serverPort)) # initiates TCP connection
receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,)) #creates a thread for receiving messages from server
send_thread = threading.Thread(target=send_messages, args=(clientSocket,)) #creates a thread for sending messages to server
receive_thread.start() #starts the receiving thread
send_thread.start() #starts the sending thread
