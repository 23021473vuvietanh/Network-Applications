# chat_app/client/gui.py

import tkinter as tk
from tkinter import scrolledtext
from client import udp_client

def run_gui():
    # Configuration for server IP and port
    server_ip = "127.0.0.1"  # Change this if your server is on a different machine
    server_port = 12000

    # Create UDP client socket
    client_socket = udp_client.create_udp_client(server_ip, server_port)

    # Build the GUI
    root = tk.Tk()
    root.title("UDP Chat Client")
    root.geometry("500x500")

    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    chat_display.pack(padx=10, pady=10)
    chat_display.config(state=tk.DISABLED)

    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill=tk.X)

    # Bind the Enter key to send_message
    message_entry.bind("<Return>", lambda event: send_message())

    def display_message(msg):
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, msg)
        chat_display.config(state=tk.DISABLED)
        # Auto-scroll to the end
        chat_display.yview(tk.END)

    def send_message():
        message = message_entry.get()
        if message:
            client_socket.sendto(message.encode(), (server_ip, server_port))
            display_message(f"You: {message}\n")
            message_entry.delete(0, tk.END)

    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack(padx=10, pady=5, side=tk.RIGHT)

    # Start background thread to receive messages and update the chat display
    udp_client.start_receive_thread(client_socket, display_message)

    root.mainloop()
    client_socket.close()

if __name__ == "__main__":
    run_gui()
