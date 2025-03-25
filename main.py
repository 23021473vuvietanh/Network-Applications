# chat_app/main.py

import sys
from client import run_gui
from server import start_udp_server

if __name__ == '__main__':
    # Run the server if the first argument is 'server'
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        start_udp_server()
    else:
        # Otherwise, run the client GUI
        run_gui()
