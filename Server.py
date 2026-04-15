from socket import * 
import threading
import time

import GLOBALVARIABLES

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
            message = client_socket.recv(GLOBALVARIABLES.socketBytes).decode() #receives a message up to 1024 bytes from client, and decodes it
            if message == "" or message == GLOBALVARIABLES.exitKeyword: #if client exits or connection is lost break out of processing loop
                break

            if str.startswith(message, "@"):
                #Feature 2: one to one
                targetUser = message[1: message.find(" ")] #finds and stores target user for direct message
                if targetUser in username_socket: #checks if target user is in the dict
                    username_socket[targetUser].send("From " + username + ": " + message[message.find(" ")+1:].encode()) #Sends the message excluding the @username to the target user
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

        #Broadcast to all users that a user has left
        for user, socket in username_socket.items():
            socket.send((username + " has left the chat").encode())

        print(username + " has left the chat") #Prints to server console that a user has left


print('The server is ready to receive')
print('Server IP address is: ', gethostbyname(gethostname())) #prints the server's IP address for clients to connect
while True:   #always welcoming
    connectionSocket, addr = serverSocket.accept()  #Makes a socket and stores address for incoming client
    
    connectionSocket.send("Enter username (no spaces)".encode()) #Requests client for username

    username = connectionSocket.recv(GLOBALVARIABLES.socketBytes).decode() #Receives username and decodes
    username_socket[username] = connectionSocket #Stores socket and username as a pair in dict

    connectionSocket.send(( "Type:" + GLOBALVARIABLES.exitKeyword + " to leave the chat" ).encode()) #Requests client for username

    #Broadcast to all users that a new user has joined
    for user, socket in username_socket.items():
        if username != user: #for every user but the new user send the message
            socket.send((username + " has joined the chat").encode())
    print(username + " has joined the chat with IP: " + addr[0]) #Prints to server console that a new user has joined, and their IP address

    client_thead = threading.Thread(target=process_client, args=(connectionSocket, username)) #Starts new thread for client
    client_thead.start()

   