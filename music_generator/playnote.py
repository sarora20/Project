import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9001        # The port used by the server

def playnote():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            midi = str(input("midi"))
            duration = str(input("duration"))
            msg = midi + " " + duration + " ;"
            s.send(msg.encode('utf-8'))


playnote()