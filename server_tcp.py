import socket
import time
import random

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ("localhost", 8820)
# server_socket.bind(server_address)
# server_socket.listen()
# (my_socket, address) = server_socket.accept()
# while True:
#     some_word = my_socket.recv(1024).decode()
#     print("Client sent: " + some_word)
#     my_socket.send((some_word.upper() + "!!!").encode())
#     if some_word == "Quit":
#         my_socket.send("Bye".encode())
#         break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 8820)
server_socket.bind(server_address)
server_socket.listen()
(my_socket, address) = server_socket.accept()
while True:
    some_word = my_socket.recv(1024).decode()
    # print("The command that the client send is: " + some_word)
    if some_word == "NAME":
        my_socket.send("some server".encode())
    elif some_word == "TIME":
        my_socket.send(time.asctime().split(" ")[3].encode())
    elif some_word == "RAND":
        my_socket.send(str(random.randint(1, 10)).encode())
    elif some_word == "Quit":
        my_socket.send("Bye".encode())
        break
    else:
        my_socket.send("You entered invalid input")
