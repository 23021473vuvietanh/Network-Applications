import socket
import threading

serverIP = "0.0.0.0"  # Lắng nghe trên tất cả các địa chỉ mạng
serverPort = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

clients = set()
running = True  

print("🟢 Server đang lắng nghe (Nhập 'exit' để dừng)...")

def listen_for_exit():
    global running
    while True:
        command = input()
        if command.lower() == "exit":
            print("🛑 Server đang tắt...")
            running = False
            serverSocket.close()
            break

exit_thread = threading.Thread(target=listen_for_exit, daemon=True)
exit_thread.start()

while running:
    try:
        message, clientAddress = serverSocket.recvfrom(2048)  
        senderIP, senderPort = clientAddress
        message_text = message.decode().upper()

        if clientAddress not in clients:
            clients.add(clientAddress) 
            print(f"📌 Client mới kết nối: {clientAddress}")

        print(f"📩 [{senderIP}:{senderPort}] -> {message_text}")

        # Gửi tin nhắn đến tất cả client khác
        for otherClient in clients:
            if otherClient != clientAddress:
                serverSocket.sendto(f"Client {senderPort}: {message_text}".encode(), otherClient)

    except OSError:
        break  

print("🔴 Server đã dừng.")
