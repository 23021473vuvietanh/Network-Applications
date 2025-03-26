from socket import *

serverName = '10.10.88.230'  # Hoặc đặt IP của server tại đây
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence: ')
clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print("From Server:", modifiedMessage.decode())

clientSocket.close()
