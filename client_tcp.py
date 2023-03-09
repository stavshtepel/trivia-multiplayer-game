import socket

# my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# my_socket.connect(("0.0.0.0", 8820))
# data = ""
# while data != "Bye":
#     msg = input("What do you want to send to the server: ").encode()
#     my_socket.send(msg)
#     data = my_socket.recv(1024).decode()
#     print("Server sent: " + data)
# my_socket.close()

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("0.0.0.0", 5555))
data = ""
while data != "Bye":
    msg = input("Please Write here a command to send to the server: [NAME/TIME/RAND]").encode()
    my_socket.send(msg)
    data = my_socket.recv(1024).decode()
    print("Server sent: " + data)
my_socket.close()
