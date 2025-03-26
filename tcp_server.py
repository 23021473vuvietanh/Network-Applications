import socket
import threading

SERVER_IP = "192.168.114.1"  # Thay đổi theo địa chỉ mạng của bạn
SERVER_PORT = 12000

clients = set()  # Danh sách các client đang kết nối

def handle_client(client_socket, client_address):
    """Xử lý tin nhắn từ một client cụ thể"""
    print(f"[NEW CONNECTION] {client_address} connected.")
    clients.add(client_socket)

    try:
        while True:
            message = client_socket.recv(2048).decode()
            if not message:
                break  # Nếu client đóng kết nối

            print(f"Received from {client_address}: {message}")

            # Gửi tin nhắn đến tất cả các client khác
            for client in clients:
                if client != client_socket:
                    client.send(f"{client_address}: {message}".encode())

    except (ConnectionResetError, BrokenPipeError):
        print(f"[DISCONNECTED] {client_address} has disconnected.")
    finally:
        clients.remove(client_socket)
        client_socket.close()

def start_tcp_server():
    """Khởi động server TCP"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"TCP Server listening on {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        server_socket.close()
        print("Server socket closed.")

if __name__ == "__main__":
    start_tcp_server()
