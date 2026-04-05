from socket import * 
import threading
import time

serverPort = 12001
serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket

serverSocket.bind(('',serverPort))  # binds to all addresses available for local testing
#serverSocket.bind(('192.168.0.35',serverPort)) #binds to one specific address for over the air
#serverSocket.bind(('TEMP',serverPort)) #binds to one specific address for over the air hot spot
serverSocket.listen(5) # server listens for up to 5 clients

username_socket = {}

def process_client(client_socket, username):
    try:
        while True:
            message = client_socket.recv(1024).decode() #receives a message up to 1024 bytes from client, and decodes it
            if message == "": #if client exits or connection is lost break out of processing loop
                break

            if str.startswith(message, "@"):
                #Feature 2: one to one
                targetUser = message[1: message.find(" ")] #finds and stores target user for direct message
                if targetUser in username_socket: #checks if target user is in the dict
                    username_socket[targetUser].send(message[message.find(" ")+1:].encode()) #Sends the message excluding the @username to the target user
                else:
                    client_socket.send("Target user not found".encode()) #tells sender that user was not found
            
            else:
                #Feature 1: Broadcast
                for user, socket in username_socket.items():
                    if username != user: #for every user but the sender send the message
                     socket.send(message.encode())
    except:
        pass #do nothing
    finally: #post processing and end client thread
        client_socket.close() #close socket
        del username_socket[username] #deletes socket and username from dict


print('The server is ready to receive')
while True:   #always welcoming
    connectionSocket, addr = serverSocket.accept()  #Makes a socket and stores address for incoming client
    
    connectionSocket.send("Enter username (no spaces)".encode()) #Requests client for username

    username = connectionSocket.recv(1024).decode() #Receives username and decodes
    username_socket[username] = connectionSocket #Stores socket and username as a pair in dict

    client_thead = threading.Thread(target=process_client, args=(connectionSocket, username)) #Starts new thread for client
    client_thead.start()

   