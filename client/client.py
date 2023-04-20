import socket
import time
import sys
import hashlib
import getpass
from configparser import ConfigParser
import rsa
import base64


def send_to_all_servers(client_message, content):
    message_recv_from_server1 = send_data_to_server1(content)
    message_recv_from_server2, message_recv_from_server3 = send_data_to_all_servers(client_message, content)
    return message_recv_from_server1, message_recv_from_server2, message_recv_from_server3


def send_data_to_all_servers(client_message, content):
    message_recv_from_server2 = send_data_to_server2(client_message, content)
    message_recv_from_server3 = send_data_to_server3(client_message, content)
    return message_recv_from_server2, message_recv_from_server3


def send_to_server_replicas(client_message, content):
    message_recv_from_server2 = send_to_server2(client_message, content)
    message_recv_from_server3 = send_to_server3(client_message, content)
    return message_recv_from_server2, message_recv_from_server3


def send_to_server1(message):
    ip_address_host = socket.gethostbyname('localhost')
    port = 9090
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.connect((ip_address_host, port))
    s_socket.send(message.encode('utf-8'))
    message_recv_from_server1 = None
    if (message.split('|')[0] in ["ls"]) or (
            message.split(' ')[0] in ["create", "cd", "delete", "mkdir", "write", "rename"]):
        # data received in bytes, converted to string and stored as string
        message_recv_from_server1 = s_socket.recv(1024).decode('utf-8')
    elif message.split(' ')[0] in ["read"]:
        # data received and stored in bytes 
        message_recv_from_server1 = s_socket.recv(1024)
    s_socket.close()
    return message_recv_from_server1


def send_data_to_server1(content):
    host = socket.gethostbyname('localhost')
    port = 9090
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.connect((host, port))
    encrypted_content = rsa.encrypt(content.encode(), publicKey)
    s_socket.send(encrypted_content)

    message_recv_from_server = None
    message_recv_from_server = s_socket.recv(1024)
    s_socket.close()
    return message_recv_from_server


def send_to_server2(client_message, content):
    try:
        host = socket.gethostbyname('localhost')
        port = 9091
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.connect((host, port))
        status2 = ('Client Connected to Server2', 'Server2')
        print(status2[0], status2[1])

        command = client_message + ' | ' + content
        s_socket.send(command.encode('utf-8'))
        response = s_socket.recv(1024).decode('utf-8')
        time.sleep(1)
        s_socket.close()
        return response
    except ConnectionRefusedError:
        status2 = ('Could not connect to Server2', 'Server2')
        print(status2[0], status2[1])


def send_data_to_server2(client_message, content):
    host = socket.gethostbyname('localhost')
    port = 9091
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.connect((host, port))
    status2 = ('Client Connected to Server2', 'Server2')
    print(status2[0], status2[1])

    encrypted_content = rsa.encrypt(content.encode(), publicKey)
    encrypted_content_string = str(base64.b64encode(encrypted_content), 'utf-8')
    command = client_message + ' | ' + encrypted_content_string
    s_socket.send(command.encode('utf-8'))
    message_recv_from_server = None
    message_recv_from_server2 = s_socket.recv(1024)
    s_socket.close()
    return message_recv_from_server2


def send_to_server3(client_message, content):
    try:
        host = socket.gethostbyname('localhost')
        port = 9092
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.connect((host, port))
        status3 = ('Client Connected to Server3', 'Server3')
        print(status3[0], status3[1])
        command = client_message + ' | ' + content
        s_socket.send(command.encode('utf-8'))
        response = s_socket.recv(1024).decode('utf-8')
        time.sleep(1)
        s_socket.close()
        return response
    except ConnectionRefusedError:
        status3 = ('Could not connect to Server3', 'Server3')
        print(status3[0], status3[1])


def send_data_to_server3(client_message, content):
    host = socket.gethostbyname('localhost')
    port = 9092
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.connect((host, port))
    status2 = ('Client Connected to Server3', 'Server3')
    print(status2[0], status2[1])

    encrypted_content = rsa.encrypt(content.encode(), publicKey)
    encrypted_content_string = str(base64.b64encode(encrypted_content), 'utf-8')
    command = client_message + ' | ' + encrypted_content_string
    s_socket.send(command.encode('utf-8'))
    message_recv_from_server = None
    message_recv_from_server3 = s_socket.recv(1024)
    s_socket.close()
    return message_recv_from_server3


def encrypting_pwd(word):
    result = hashlib.md5(word.encode())

    # printing the equivalent hexadecimal value.
    # print("The hexadecimal equivalent of hash is : ")
    return result.hexdigest()


def user_creation():
    config = ConfigParser()
    config.read('auth.ini')
    usernames = list(config['AUTHENTICATION'])
    username = input("please enter your new username: ")
    if username in usernames:
        print("Error creating new user. user already exists!")
        sys.exit()
    pwd = input("please enter your new password: ")
    enc_pwd = encrypting_pwd(pwd)
    config.set('AUTHENTICATION', username, enc_pwd)

    with open('auth.ini', 'w') as configfile:
        config.write(configfile)


# main
def main():
    global publicKey, privateKey
    publicKey, privateKey = rsa.newkeys(1024)

    config = ConfigParser()
    config.read('auth.ini')
    usernames = list(config['AUTHENTICATION'])
    print("Current usernames : ", usernames)
    is_existing_user = input("Is your username on the list? Y/N: ")
    if is_existing_user.lower() != "y" :
        print('Let\'s create a new user for you : ')
        user_creation()
        print('The user has been successfully created.')
        sys.exit()
    access_permission = 'Unconfirmed'
    num_of_trial = 0
    while access_permission == 'Unconfirmed':
        username = input("Enter Username : ")
        user_entered_pwd = getpass.getpass("Enter Password : ")
        encpt_pwd = encrypting_pwd(user_entered_pwd)
        num_of_trial += 1
        if (username in usernames) and (encpt_pwd == config['AUTHENTICATION'][username]):
            access_permission = 'User confirmed'
        else:
            print("Your credentials do not match. You have " + str(3 - num_of_trial) + " trials.")
        if num_of_trial == 3:
            print("You have exhausted the number of trials. Please check your credentials and try again.")
            sys.exit()

    while True:
        print("Welcome " + username + " !")
        client_message = input("Which operation do you want to perform :  ")
        message_recv_from_server = send_to_server1(client_message + '|' + username)
        message_recv_from_server2, message_recv_from_server3 = send_to_server_replicas(
                client_message + '|' + username, "None")
        client_message_0 = client_message.split()[0]
        if len(client_message.split()) > 1:
            wanted_filename = client_message.split()[1]

        if client_message_0 == "ls":
            print("The list of existing files: ", message_recv_from_server)
            
        if client_message_0 == "create":
            print(message_recv_from_server2, message_recv_from_server3)

        if client_message_0 == "delete":
            print(message_recv_from_server2, message_recv_from_server3)

        if client_message_0 == "read":
            decrypted_message = (rsa.decrypt(message_recv_from_server, privateKey)).decode('utf-8')
            print(decrypted_message)

        if client_message_0 == "write":
            content = input("enter the text you want to insert: ")
            message_recv_from_server = send_to_all_servers(client_message + '|' + username, content)
            print(message_recv_from_server)

        if client_message_0 == "rename":
            new_filename = input("Enter the new name of the file: ")
            send_to_server1(new_filename)
            message_recv_from_server = send_to_server_replicas(client_message + '|' + username, new_filename)

        if client_message_0 == "cd":
            message_recv_from_server = send_to_server_replicas(client_message + '|' + username, "None")
            print(message_recv_from_server)

        if client_message_0 == "mkdir":
            message_recv_from_server = send_to_server_replicas(client_message + '|' + username, "None")


if __name__ == "__main__":
    main()
