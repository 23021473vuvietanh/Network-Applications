import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

serverName = '192.168.0.101'
serverPort = 12000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind((serverName, 0))
clientIP, clientPort = clientSocket.getsockname()
clientSocket.sendto(("Hello from client " + str(clientSocket.getsockname()[1])).encode(), (serverName, serverPort))
# clientSocket.sendto(("Hello client " + str(clientPort)).encode(), (serverName, serverPort))

root = tk.Tk()
root.title("Client " + str(clientPort))
root.geometry("500x400")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
chat_display.pack(pady=10)
chat_display.config(state=tk.DISABLED)


message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

def send_message():
    message = message_entry.get()
    if message:
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            data, _ = clientSocket.recvfrom(2048)
            received_text = data.decode()

            if received_text.islower(): 
                modified_text = received_text.upper()
                clientSocket.sendto(modified_text.encode(), (serverName, serverPort)) 
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Received & sent back: {modified_text}\n")
                chat_display.config(state=tk.DISABLED)
            else:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Server: {received_text}\n")
                chat_display.config(state=tk.DISABLED)
        except OSError:
            break


send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

root.mainloop()

clientSocket.close()
