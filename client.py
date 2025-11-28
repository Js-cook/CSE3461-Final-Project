from email import message
from multiprocessing.dummy.connection import Client
from socket import *
import threading

# Send a message
def messageSendHandler(message, clientSocket):
    # Send Username to server
    username = input("Enter your username: ")
    clientSocket.send(username.encode())

    while True:
        message = input("Input your message:")
        clientSocket.send(message.encode())

# Receive a message
def messageReceiveHandler(clientSocket):
    while True:
        receivedMessage = clientSocket.recv(1024).decode()

        if len(receivedMessage) == 0:
            break

        print(f"\n Received Message: {receivedMessage}")


# Want to essentially create a message sender and a message receiver
# We will have a thread to manage both
serverIp = ""
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIp, serverPort))
print(f"Client Ip: {clientSocket.getsockname()[0]} \n Client Port: {clientSocket.getsockname()[1]}")

# Create threads
sendThread = threading.Thread(target=messageSendHandler, args = (message, clientSocket), daemon = True)
receiveThread = threading.Thread(target = messageReceiveHandler, args = (clientSocket,), daemon = True)

# Start threads
sendThread.start()
receiveThread.start()

# Keep main thread running while the other threads do their work
try:
    sendThread.join()
    receiveThread.join()
except KeyboardInterrupt:
    print("\nClient shutting down...")
    clientSocket.close()