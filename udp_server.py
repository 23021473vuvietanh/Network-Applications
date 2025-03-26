# chat_app/server/udp_server.py

from socket import *

server_ip = '0.0.0.0'
server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print('The server is ready to receive')

try:
    while True:
        message, clientAddress = server_socket.recvfrom(2048)
        print(message.decode())
        modified_message = message.decode().upper()
        server_socket.sendto(modified_message.encode(), clientAddress)
        
except KeyboardInterrupt:
    print("\nServer is shutting down...")
finally:
    server_socket.close()
    print("Socket closed.")