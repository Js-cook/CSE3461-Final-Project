from socket import *
import threading

clients = dict()

client_connection_lock = threading.Lock()

def client_handler(connection_socket):

    # Wait for username and add it to the list:
    username = connection_socket.recv(1024).decode()
    print(f"User {username} connected.")

    with client_connection_lock:
        clients[username] = connection_socket
    
    while True:
        message = connection_socket.recv(1024)
        
        # connection closed
        if len(message) == 0:
            with client_connection_lock:
                clients.pop(username)
                connection_socket.close()
                print("Client disconnected")
                break

        #If message starts with all broadcast to all clients
        if(message.decode().startswith("@ALL ")):
            broadcastMessage = message.decode()[5:].encode()
            print("Broadcasting: " + broadcastMessage.decode())

            with client_connection_lock:
                for client_socket in clients.values():
                    if client_socket != connection_socket:
                        client_socket.send(broadcastMessage)
        # Try to send private message
        elif(message.decode()[0] == '@'):
            targetUsername = message.decode().split()[0][1:]
            targetMessage = ' '.join(message.decode().split()[1:]).encode()
            print("Sending: " + targetMessage.decode())
            
            with client_connection_lock:
                if targetUsername in clients:
                    clients[targetUsername].send(targetMessage)
                else:
                    connection_socket.send("Username doesn't exist".encode())
        else:
            connection_socket.send("Use correct format: @target message".encode())

        
        

def main():
    server_port = 12000
    server_IP_address = ""

    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((server_IP_address, server_port)) 
    server_socket.listen(5) 

    print('The server is ready to receive') 
    while True:
        connection_socket, addr = server_socket.accept()

        # Create thread and add it to list for management (set Daemon to true so all client threads terminate w/ main on shutdown)
        new_thread = threading.Thread(target=client_handler, args=(connection_socket,), daemon=True)
        new_thread.start()

if __name__ == "__main__":
    main()