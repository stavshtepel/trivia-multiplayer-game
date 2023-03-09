import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "0.0.0.0"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
    conn.send((chatlib.build_message(code, data)).encode())

def build_send_recv_parse(conn, cmd, data):
    build_and_send_message(conn, cmd, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data

def get_score(conn):
    cmd, data = build_send_recv_parse(conn, "MY_SCORE", "")
    if cmd == "YOUR_SCORE":
        print(data)
    else:
        print("ERROR")

def get_highscore(conn):
    cmd, data = build_send_recv_parse(conn, "HIGHSCORE", "") 
    if cmd == "ALL_SCORE":
        print(data)
    else:
        print("ERROR")

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
    return cmd, data
	
	

def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    return client_socket


def error_and_exit(error_msg):
    print(error_msg)
    exit()


def play_question(conn):
    question_cmd, question_data = build_send_recv_parse(conn, "GET_QUESTION", "")
    if question_cmd == "YOUR_QUESTION":
        print("\n".join(question_data.split("#")[1:6]))
    else:
        print("ERROR")
    user_answer = int(input("Enter here the number of the answer for the question: "))
    question_id = question_data.split("#")[0]
    answer_cmd, answer_data = build_send_recv_parse(conn, "SEND_ANSWER", f"{question_id}#{user_answer}")
    if answer_cmd == "CORRECT_ANSWER":
        print("Your answer is correct")
    elif answer_cmd == "WRONG_ANSWER":
        print("Your answer is false")
    else:
        print("ERROR")

def get_logged_users(conn):
    cmd, data = build_send_recv_parse(conn, "LOGGED", "")
    if cmd == "LOGGED_ANSWER":
        print(data)
    else:
        print("ERROR")

def login(conn):
    login_server_message = chatlib.PROTOCOL_SERVER["login_failed_msg"]
    while login_server_message != chatlib.PROTOCOL_SERVER["login_ok_msg"]:
        login_server_message = chatlib.PROTOCOL_SERVER["login_failed_msg"]
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["login_msg"], f"{username}{chatlib.DATA_DELIMITER}{password}")
        login_server_message = cmd
        if login_server_message == chatlib.PROTOCOL_SERVER["login_failed_msg"]:
                print(data)
    return 

def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "logout")

def main():
    some_socket = connect()
    login(some_socket)
    user_action = ""
    while user_action != "q":
        user_action = input("What action would you like to do: [QUIT] - q / [SEE YOUR SCORES] - s / [SEE HIGHSCORE TABLE] - h / [GET_LOGGED_USERS] - g / s[PLAY_QUESTION] - p \n")
        if user_action == "s":
            get_score(some_socket)
        elif user_action == "h":
            get_highscore(some_socket)
        elif user_action == "g":
            get_logged_users(some_socket)
        elif user_action == "p":
            play_question(some_socket)
    logout(some_socket)
    some_socket.close()

if __name__ == '__main__':
    main()
