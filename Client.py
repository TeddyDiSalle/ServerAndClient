##L10 Socket programming hands-on (TCP)
import threading
import GLOBALVARIABLES
from socket import *
import time
#serverName = "172.28.203.33"
serverName = "127.0.0.1"  # localhost
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

ENABLE_DELAY = GLOBALVARIABLES.DELAY;

def receive_messages(client_socket):
    latencies = []
    while True:
        message = client_socket.recv(GLOBALVARIABLES.socketBytes).decode() #receives a message up to 1024 bytes from server, and decodes it
        if message == "": #if connection is lost break out of processing loop
            break
        try:
            received_time = time.time()
            timestamp, msg = message.split("|", 1)
            sent_time = float(timestamp)
            latency = received_time - sent_time
            latencies.append(latency)

            print("\r", end="")
            print(f"{msg} (delay: {latency:.3f} sec)")

            #Running averages
            avg = sum(latencies) / len(latencies)
            print(f"[avg delay: {avg:.3f} sec]")
        except:
            print("\r", end="") #prints a carriage return to move the cursor to the beginning of the line for better formatting
            print(message) #prints the message from server
            print("> ", end="", flush=True)  # reprint the prompt


def send_messages(client_socket):
    message = ""
    while message != GLOBALVARIABLES.exitKeyword: #if user types the exit, end the sending thread
        message = input("> ") #reads a message from user input
        if ENABLE_DELAY:
            timestamp = time.time()
            message = f"{timestamp}|{message}"
        client_socket.send(message.encode()) #encodes and sends the message to server

    client_socket.close() #close socket when done sending messages


print(clientSocket.recv(GLOBALVARIABLES.socketBytes).decode())  # prints "Enter username" sent by server
username = input("> ")
clientSocket.send(username.encode())
print(clientSocket.recv(GLOBALVARIABLES.socketBytes).decode())  # prints instruction on  how to exit

receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,)) #creates a thread for receiving messages from server
send_thread = threading.Thread(target=send_messages, args=(clientSocket,)) #creates a thread for sending messages to server
receive_thread.start() #starts the receiving thread
send_thread.start() #starts the sending thread
