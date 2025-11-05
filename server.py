from socket import *
import threading

clients = []
client_threads = []

client_connection_lock = threading.Lock()

def client_handler(connection_socket):
    while True:
        message = connection_socket.recv(1024)
        
        # connection closed
        if len(message) == 0:
            with client_connection_lock:
                clients.remove(connection_socket)
                connection_socket.close()
                print("Client disconnected")
                break

        with client_connection_lock:
            for client_socket in clients:
                # Don't send message to self
                if client_socket != connection_socket:
                    client_socket.send(message)

def main():
    server_port = 12000
    server_IP_address = ""

    server_socket = socket(AF_INET,SOCK_STREAM) 
    server_socket.bind((server_IP_address, server_port)) 
    server_socket.listen(5) 

    print('The server is ready to receive') 
    while True:
        connection_socket, addr = server_socket.accept()
        # Not sure if this is a critical section but I assume so
        with client_connection_lock:
            clients.append(connection_socket)

        # Create thread and add it to list for management (set Daemon to true so all client threads terminate w/ main on shutdown)
        new_thread = threading.Thread(target=client_handler, args=(connection_socket,), daemon=True)
        client_threads.append(new_thread)
        new_thread.start()

if __name__ == "__main__":
    main()