##############################################################################
# server.py
##############################################################################

import socket
import select
import chatlib
import random

# GLOBALS
users = {"test": ["test", 0, 0], "abc": ["123", 0, 0]}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "0.0.0.0"
MAX_MSG_LENGTH = 1024

client_sockets = []
messages_to_send = []

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    """
    Builds a new message using chatlib, wanted code and message. 
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    global messages_to_send
    # conn.send((chatlib.build_message(code, msg)).encode())
    full_msg = chatlib.build_message(code, msg)
    messages_to_send += [(conn, full_msg)]
    print("[SERVER] ",full_msg)   # Debug print

def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message. 
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    print("[CLIENT] ",full_msg)   # Debug print
    return cmd, data
    

# Data Loaders #

def load_questions():
    """
    Loads questions bank from file  ## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
                2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
                4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
                }
    
    return questions

def load_user_database():
    """
    Loads users list from file  ## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
            "test"      :   {"password":"test","score":0,"questions_asked":[]},
            "yossi"     :   {"password":"123","score":50,"questions_asked":[]},
            "master"    :   {"password":"master","score":200,"questions_asked":[]}
            }
    return users

    
# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    return server_socket
    


        
def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, error_msg, "")
    


    
##### MESSAGE HANDLING


def print_client_sockets(sockets_list):
    for i in sockets_list:
        print(i.getpeername())

def handle_getscore_message(conn, username):
    global users
    scores = users[username][1]
    build_and_send_message(conn, "YOUR_SCORE", str(scores))

def handle_highscore_message(conn):
    high_scores = []
    for value in users.values():
        for i in value:
            if value.index(i) == 1:
                high_scores += [i]
    sorted_user_scores = (sorted(users.items(), key=lambda item: item[1][1]))[-3:]
    users_with_scores = {}
    for i in sorted_user_scores:
        for item in i[1]:
            if i[1].index(item) == 1:
                users_with_scores[i[0]] = item
    users_high_score = "\n".join("{!r}: {!r}".format(k, v) for k, v in users_with_scores.items())
    build_and_send_message(conn, "ALL_SCORE", users_high_score)
    
def handle_logged_message(conn):
    build_and_send_message(conn, "LOGGED_ANSWER", ", ".join(list(logged_users.values())))

def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    client_sockets.remove(conn)
    del logged_users[conn.getpeername()]
    conn.close()


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later
    
    username, password = data.split(chatlib.DATA_DELIMITER)
    if username in users.keys() and password == users[username][0]:
        build_and_send_message(conn, "LOGIN_OK", data)
        logged_users[conn.getpeername()] = username
    elif username in users.keys() and password != users[username]:
        build_and_send_message(conn, "ERROR", "Password does not match")
    else:
        # users[username] = [password, 0, []]
        build_and_send_message(conn, "ERROR", "Username does not exist")

def handle_question_message(conn):
    build_and_send_message(conn, "YOUR_QUESTION" ,create_random_question())

def handle_answer_message(conn, username, data):
    global questions_with_id_and_answer
    question_id, user_answer = data.split(chatlib.DATA_DELIMITER)
    for question in questions_with_id_and_answer:
        if str(question.split(chatlib.DATA_DELIMITER)[0]) == str(question_id):
            if str(question.split(chatlib.DATA_DELIMITER)[-1]) == str(user_answer):
                build_and_send_message(conn, "CORRECT_ANSWER", "")
                users[username] = [users[username][0], users[username][1] + 5, users[username][2]]
                
            else:
                build_and_send_message(conn, "WRONG_ANSWER", "")

def create_random_question():
    question_id = 0
    global questions_with_id_and_answer
    questions_with_id = []
    questions_with_id_and_answer = []
    trivia_questions_list = [
            ("In which Italian city can you find the Colosseum?#Venice#Rome#Naples#Milan", 3),
            ("In the TV show New Girl, which actress plays Jessica Day? Zooey Deschanel#Kaley Cuoco# Jannifer Aniston #Alyson Hannigan", 2),
            ("What is the largest canyon in the world?#Verdon Gorge, France#King’s Canyon, Australia#Grand Canyon, USA#Fjaðrárgljúfur Canyon, Iceland", 3),
            ("How long is the border between the United States and Canada?#3,525 miles#4,525 miles#5,525 miles#6,525 miles", 3),
            ("What is the largest active volcano in the world?#Mount Etna#Mount Vesuvius#Mouna Loa#Mount Batur", 3)
            ]
    for i in trivia_questions_list:
        questions_with_id += [str(question_id) + "#" + i[0]]
        questions_with_id_and_answer += [str(question_id) + "#" + i[0] + "#" + str(i[1])]
        question_id += 1

    return random.choice(questions_with_id)
         

def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users  # To be used later
    if conn.getpeername() in logged_users.keys():
        if cmd == "LOGOUT":
            handle_logout_message(conn)
        elif cmd == "MY_SCORE":
            handle_getscore_message(conn, logged_users[conn.getpeername()])
        elif cmd == "HIGHSCORE":
            handle_highscore_message(conn)
        elif cmd == "LOGGED":
            handle_logged_message(conn)
        elif cmd == "GET_QUESTION":
            handle_question_message(conn)
        elif cmd == "SEND_ANSWER":
            handle_answer_message(conn, logged_users[conn.getpeername()], data)
        # else:
        #     build_and_send_message(conn, "ERROR", "")
    else:
        if cmd == "LOGIN":
            handle_login_message(conn, data)
        # else:
        #     build_and_send_message(conn, "ERROR", "")


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    global messages_to_send
    
    print("Welcome to Trivia Server!")
    server_socket = setup_socket()
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = server_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                cmd, data = recv_message_and_parse(client_socket)
                handle_client_message(client_socket, cmd, data)
            else:
                cmd, data = recv_message_and_parse(current_socket)
                if cmd == "" or cmd == None:
                    print("Connection closed")
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    # client_socket.send(data.encode())
                    handle_client_message(current_socket, cmd, data)
        for message in messages_to_send:
            message[0].send(message[1].encode())  
            messages_to_send.remove(message)
        



if __name__ == '__main__':
    main()
