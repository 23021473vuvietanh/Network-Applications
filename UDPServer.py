from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

clients = set() 
running = True  

print("🟢 The server is ready to receive (type 'exit' to stop)")


def listen_for_exit():
    global running
    while True:
        command = input()
        if command.lower() == "exit":
            print("🛑 Server is shutting down...")
            running = False
            serverSocket.close()
            break

exit_thread = threading.Thread(target=listen_for_exit, daemon=True)
exit_thread.start()

while running:
    try:
        message, clientAddress = serverSocket.recvfrom(2048)  
        senderIP, senderPort = clientAddress
        modifiedMessage = f"Client {senderPort}: {message.decode().upper()}"

        if clientAddress not in clients:
            clients.add(clientAddress) 
            print(f"📩 New client connected: {clientAddress}")

        print(f"📨 Received from {clientAddress}: {message.decode()}")

        for otherClient in clients:
            if otherClient != clientAddress:
                serverSocket.sendto(modifiedMessage.encode(), otherClient)
    except OSError:
        break 

print("🔴 Server stopped.")