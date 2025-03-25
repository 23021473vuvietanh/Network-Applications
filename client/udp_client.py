# chat_app/client/udp_client.py

import socket
import threading

def create_udp_client(server_ip="127.0.0.1", server_port=12000):
    """Creates and returns a UDP client socket."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return client_socket

def start_receive_thread(client_socket, display_callback):
    """
    Starts a thread that receives messages on the client_socket.
    Each message is passed to display_callback (a function that updates the GUI).
    """
    def receive_messages():
        while True:
            try:
                data, _ = client_socket.recvfrom(2048)
                message = data.decode()
                display_callback(f"Friend: {message}\n")
            except Exception as e:
                print("Error receiving message:", e)
                break
    thread = threading.Thread(target=receive_messages, daemon=True)
    thread.start()
    return thread
