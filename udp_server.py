from socket import *

server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))

print('The UDP server is ready to receive')

while True:
    message, clientAddress = server_socket.recvfrom(2048)
    modified_message = message.decode().upper()
    print('Modified: ' + modified_message)
    server_socket.sendto(modified_message.encode(), clientAddress)
