import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((SERVER_IP, SERVER_PORT))
while True:
    pass
