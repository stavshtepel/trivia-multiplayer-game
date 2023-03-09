import socket
import random

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_SIZE = 1024
SERIAL_NUMBER_FIELD_SIZE = 4
MAX_SERIAL_NUM = 10000
TIMEOUT_IN_SECONDS = 5

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((SERVER_IP, PORT))
# data = ""
# while data != "EXIT":
#     (client_message, address) = server_socket.recvfrom(MAX_MSG_SIZE)
#     data = client_message.decode()
#     print("Client sent " + data)
#     if data == "SEND_HELLO":
#         server_socket.sendto("Hello", (address, PORT))
#     elif data == "SEND_NAME":
#         server_socket.sendto("Some name", (address, PORT))
#     elif data == "SEND_SOMETHING":
#         server_socket.sendto("Something", (address, PORT))
#     else:
#         server_socket.sendto("Error", (address, PORT))
# server_socket.close()

def special_sendto(socket_object, response, client_address):
    fail = random.randint(1, 3)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))

request_recieved = False
while request_recieved == False:
    try:
        (data, remote_address) = server_socket.recvfrom(MAX_MSG_SIZE)
        server_socket.settimeout(TIMEOUT_IN_SECONDS)
    except:
        print("This code reached despite client not answering")
    else:
        print(data.decode())
        request_recieved = True
    finally:
        server_socket.close()
