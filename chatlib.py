# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
    if len(cmd) < 16:
        new_command = cmd + " " * (16 - len(cmd))
        full_msg = new_command + DELIMITER + str(len(data)).zfill(4) + DELIMITER + data
    if len(new_command) == 16:
        return full_msg

def parse_message(data):
	# """
	# Parses protocol message and returns command name and data field
	# Returns: cmd (str), data (str). If some error occured, returns None, None
	# """
    if data.count("|") == 2:
        try:
            if len(data.split(DELIMITER)[0]) == 16 and int(data.split(DELIMITER)[1]) >= 0000 and int(data.split(DELIMITER)[1]) <= 9999 and len(data.split(DELIMITER)[1]) <= 4:
                cmd = list(data.split(DELIMITER)[0])
                for i in data.split(DELIMITER)[0]:
                    if i == " ":
                        cmd.remove(i)
                msg = data.split(DELIMITER)[2]
                return "".join(cmd), msg
            else:
                return None, None
        except:
            return None, None
    else:
            return None, None


	
def split_data(msg, expected_fields):
	# """
	# Helper method. gets a string and number of expected fields in it. Splits the string 
	# using protocol's data field delimiter (DELIMITERDATA_DELIMETER) and validates that there are correct number of fields.
	# Returns: list of fields if all ok. If some error occured, returns None
	# """
    fields_count = msg.count(DATA_DELIMITER)
    if expected_fields == fields_count:
        return msg.split(DATA_DELIMITER)[0]

def join_data(msg_fields):
	# """
	# Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	# Returns: string that looks like cell1#cell2#cell3
	# """
    return DATA_DELIMITER.join(msg_fields)
