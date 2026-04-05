from asyncio.windows_events import NULL
from socket import * 
import threading
import time

serverPort = 12001
serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket

serverSocket.bind(('',serverPort))  # binds to all addresses available for local testing
#serverSocket.bind(('192.168.0.35',serverPort)) #binds to one specific address for over the air
serverSocket.listen(5) # server listens for up to 5 clients

client_username = {}

def broadcast():


def process_client(client_socket, username):
    while True:
        message = client_socket.recv(1024).decode() #receives a message up to 1024 bytes from client, and decodes it
        if str.startswith(message, "@"):
            #Feature 2: one to one
            print();
        else:
            #Feature 1: Broadcast
            broadcast()


print('The server is ready to receive')
while True:   #always welcoming
    connectionSocket, addr = serverSocket.accept()  #Makes a socket and stores address for incoming client
    
    connectionSocket.send("Enter username".encode()) #Requests client for username

    username = connectionSocket.recv(1024).decode() #Receives username and decodes
    client_username[username] = connectionSocket #Stores socket and username as a pair in dict

    client_thead = threading.Thread(target=process_client, args=(connectionSocket, username)) #Starts new thread for client

   