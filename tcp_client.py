import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

SERVER_IP = "192.168.114.1"  # Thay đổi theo IP của server
SERVER_PORT = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("TCP Chat Client")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Arial", 12))
chat_display.pack(pady=10)
chat_display.config(state=tk.DISABLED, bg="#ffffff", fg="#000000")

message_frame = tk.Frame(root, bg="#f0f0f0")
message_frame.pack(pady=5)

message_entry = tk.Entry(message_frame, width=40, font=("Arial", 12))
message_entry.pack(side=tk.LEFT, padx=5)

def send_message(event=None):
    """Gửi tin nhắn đến server"""
    message = message_entry.get()
    if message:
        try:
            client_socket.send(message.encode())
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"You: {message}\n")
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
            message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

def receive_messages():
    """Nhận tin nhắn từ server"""
    while True:
        try:
            message = client_socket.recv(2048).decode()
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, message + "\n")
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error receiving message: {e}")
            break

send_button = tk.Button(message_frame, text="Send", command=send_message, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
send_button.pack(side=tk.RIGHT)

# Nhấn Enter để gửi tin nhắn
root.bind("<Return>", send_message)

# Khởi động luồng nhận tin nhắn
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

root.mainloop()
client_socket.close()
