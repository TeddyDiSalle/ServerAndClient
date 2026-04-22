from socket import * 
import threading
import GLOBALVARIABLES
import time
import random

serverPort = 12001
serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
ENABLE_DELAY = GLOBALVARIABLES.DELAY; #Toggle for simulating delay adjust in GLOBALVARIABLES.py for toggling delay on and off

serverSocket.bind(('',serverPort))  # binds to all addresses available for local testing
#serverSocket.bind(('192.168.0.35',serverPort)) #binds to one specific address for over the air
#serverSocket.bind(('172.20.10.6',serverPort)) #binds to one specific address for over the air hot spot
serverSocket.listen(5) # server listens for up to 5 clients

username_socket = {}

def process_client(client_socket, username):
    try:
        while True:
            message = client_socket.recv(GLOBALVARIABLES.socketBytes).decode() #receives a message up to 1024 bytes from client, and decodes it

            if ENABLE_DELAY:
                delay = random.uniform(0.1, 1.0)  # Choose random delay from 100ms to 1000ms
                time.sleep(delay) # simulate delay by sleeping

            if "|" in message:
                timestamp, actual_message = message.split("|", 1) #If we are simulating delay separate the timestamp and message
            else:
                timestamp = None
                actual_message = message

            actual_message = actual_message.strip()

            if actual_message == "" or actual_message == GLOBALVARIABLES.exitKeyword: #if client exits or connection is lost break out of processing loop
                break
            
            if actual_message.startswith("@"):
                #Feature 2: one to one
                targetUser = actual_message[1: actual_message.find(" ")] #Find and store target user

                if targetUser in username_socket: #If target user exists, print in the correct format depending on whether you have simulated delay
                    if timestamp:
                        formatted = f"{timestamp}|{username}: {actual_message[actual_message.find(' ')+1:]}"
                    else:
                        formatted = username + ": " + actual_message[actual_message.find(" ")+1:]

                    username_socket[targetUser].send((formatted + "\n").encode())
                else:
                    client_socket.send("Target user not found\n".encode())

            else:
                #Feature 1: Broadcast
                for user, socket in username_socket.items(): #Broadcaste message in the correct format to everyone but the sender 
                    if username != user:
                        if timestamp:
                            formatted = f"{timestamp}|{username}: {actual_message}"
                        else:
                            formatted = username + ": " + actual_message

                        socket.send((formatted + "\n").encode())
    except:
        pass #do nothing
    finally: #post processing and end client thread
        client_socket.close() #close socket
        del username_socket[username] #deletes socket and username from dict

        #Broadcast to all users that a user has left
        for user, sock in username_socket.items():
            sock.send((username + " has left the chat\n").encode())

        print(username + " has left the chat") #Prints to server console that a user has left


print('The server is ready to receive')
print('Server IP address is: ', gethostbyname(gethostname())) #prints the server's IP address for clients to connect
while True:   #always welcoming
    connectionSocket, addr = serverSocket.accept()  #Makes a socket and stores address for incoming client
    
    connectionSocket.send("Enter username (no spaces)".encode()) #Requests client for username

    username = connectionSocket.recv(GLOBALVARIABLES.socketBytes).decode() #Receives username and decodes
    username_socket[username] = connectionSocket #Stores socket and username as a pair in dict

    connectionSocket.send(("Type:" + GLOBALVARIABLES.exitKeyword + " to leave the chat\n" ).encode()) #Requests client for username

    #Broadcast to all users that a new user has joined
    for user, socket in username_socket.items():
        if username != user: #for every user but the new user send the message
            socket.send((username + " has joined the chat\n").encode())
    print(username + " has joined the chat with IP: " + addr[0]) #Prints to server console that a new user has joined, and their IP address

    client_thread = threading.Thread(target=process_client, args=(connectionSocket, username)) #Starts new thread for client
    client_thread.start()

   