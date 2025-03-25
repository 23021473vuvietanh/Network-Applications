# chat_app/server/udp_server.py

import socket

def start_udp_server(server_ip = "0.0.0.0", server_port = 12000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))
    print(f"UDP Server listening on {server_ip}:{server_port}")

    clients = set()

    try:
        while True:
            data, client_address = server_socket.recvfrom(2048)
            message = data.decode()
            print(f"Received from {client_address}: {message}")

            # Register the client if not seen before
            clients.add(client_address)

            # Forward message to all other clients
            for client in clients:
                if client != client_address:
                    server_socket.sendto(data, client)
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        server_socket.close()
        print("Socket closed.")

if __name__ == "__main__":
    start_udp_server()
