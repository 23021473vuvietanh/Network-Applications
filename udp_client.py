import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

SERVER_IP = '192.168.56.1'  # Thay bằng IP của máy chủ
SERVER_PORT = 12000

# Tạo socket UDP cho client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(("", 0))  # Lắng nghe trên cổng bất kỳ
client_ip, client_port = client_socket.getsockname()

# Gửi thông báo kết nối tới server
client_socket.sendto(f"Client {client_ip}:{client_port} connected".encode(), (SERVER_IP, SERVER_PORT))

# Khởi tạo giao diện GUI
root = tk.Tk()
root.title("UDP Chat Client")
root.geometry("500x400")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
chat_display.pack(padx=10, pady=10)
chat_display.config(state=tk.DISABLED)

message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill=tk.X)

# Cập nhật giao diện với tin nhắn mới
def update_chat(message):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, message + "\n")
    chat_display.config(state=tk.DISABLED)

# Gửi tin nhắn tới server
def send_message():
    message = message_entry.get()
    if message:
        try:
            full_message = f"Client: {message}"  # Thay 'Server' thành 'Client'
            client_socket.sendto(full_message.encode(), (SERVER_IP, SERVER_PORT))
            update_chat(f"You: {message}")
            message_entry.delete(0, tk.END)
        except Exception as e:
            print("Error sending message:", e)

# Nhận tin nhắn từ server
def receive_messages():
    while True:
        try:
            data, _ = client_socket.recvfrom(2048)
            message = data.decode()
            root.after(0, update_chat, message)  # Cập nhật giao diện
        except Exception as e:
            print("Error receiving message:", e)
            break

# Bind phím Enter để gửi tin nhắn
message_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Tạo thread nhận tin nhắn
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

root.mainloop()
client_socket.close()
