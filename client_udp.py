import socket
import random

SERVER_IP = "127.0.0.1"
PORT = 8821
MAX_MSG_SIZE = 1024
SERIAL_NUMBER_FIELD_SIZE = 4
MAX_SERIAL_NUM = 10000
TIMEOUT_IN_SECONDS = 5

# data = ""
# while data != "QUIT":
#     some_text = input("What do you want to get: ")
#     my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     my_socket.sendto(some_text.encode(), (SERVER_IP, PORT))
#     (response, remode_address) = my_socket.recvfrom(MAX_MSG_SIZE)
#     data = response.decode()
#     print(data)
# my_socket.close()

def special_sendto(socket_object, response, client_address):
    fail = random.randint(1, 3)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops")
# special_sendto(my_socket, packet, (SERVER_IP, PORT))

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

request_serial_number = 0
serial_number_field = str(request_serial_number).zfill(SERIAL_NUMBER_FIELD_SIZE)
some_text = serial_number_field + input("What would you like to send: ")
special_sendto(my_socket, some_text, (SERVER_IP, PORT))
request_sent = False
while request_sent == False:
    try:
        my_socket.settimeout(TIMEOUT_IN_SECONDS)
    except:
        special_sendto(my_socket, some_text, (SERVER_IP, PORT))
    else:
        request_sent = True
    finally:
        request_serial_number += 1
        if request_serial_number == MAX_SERIAL_NUM:
            request_serial_number = 0
        my_socket.close()
