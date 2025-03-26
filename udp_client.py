import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

SERVER_IP = '127.0.0.1'  
SERVER_PORT = 12000

# Tạo socket UDP cho client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((SERVER_IP, 0))
client_ip, client_port = client_socket.getsockname()

client_socket.sendto(f"Client {client_ip}:{client_port} connected".encode(), (SERVER_IP, SERVER_PORT))

# Build the GUI
root = tk.Tk()
root.title("UDP Chat Client")
root.geometry("500x400")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
chat_display.pack(padx=10, pady=10)
chat_display.config(state=tk.DISABLED)

message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill=tk.X)

# Bind the Enter key to send_message
message_entry.bind("<Return>", lambda event: send_message())

def send_message():
    """Gửi tin nhắn đến server"""
    message = message_entry.get()
    if message:
        try:
            full_message = f"Server: {message}"
            client_socket.sendto(full_message.encode(), (SERVER_IP, SERVER_PORT))
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"You: {message}\n")
            chat_display.config(state=tk.DISABLED)
            message_entry.delete(0, tk.END)
        except Exception as e:
            print("Error sending message:", e)

def receive_messages():
    """Nhận tin nhắn từ server"""
    while True:
        try:
            data, _ = client_socket.recvfrom(2048)
            message = data.decode()
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, message + "\n")
            chat_display.config(state=tk.DISABLED)
        except Exception as e:
            print("Error receiving message:", e)
            break

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

root.mainloop()
client_socket.close()