import datetime
import socket
import os


def send_response_to_client(data, communication_socket):
    communication_socket.send(data.encode('utf-8'))


def listing_files_in_folder():
    directory_path = "."
    existing_files = [file for file in os.listdir(directory_path) if os.path.isfile(file) or os.path.isdir(file)]
    file_list = ""
    for file in existing_files:
        file_list += file + "\n"
    return file_list


def creating_file(wanted_filename, communication_socket, client_address):
    # content = write(filename, communication_socket, server, current_dir)

    if wanted_filename not in (listing_files_in_folder()):
        with open(wanted_filename, "w") as f:
            print("Created the file in Server 3 /n")
            data = "Created the file in Server 3"
            send_response_to_client(data, communication_socket)
    else:
        data = "File already exist"
        send_response_to_client(data, communication_socket)
    communication_socket.close()
    print(f'Communication with {client_address} ended!')


def deleting_file(wanted_filename, communication_socket, client_address):
    if wanted_filename in (listing_files_in_folder()):
        os.remove(wanted_filename)
        data = "successfully deleted"
    else:
        data = "File doesn't exist"
    send_response_to_client(data, communication_socket)


def writing_into_file(wanted_filename, text, s_socket, communication_socket, client_address):
    # content = write(filename, communication_socket, server, current_dir)

    if wanted_filename in (listing_files_in_folder()):
        with open(wanted_filename, "w") as f:
            # data = "enter the text you want to insert: "
            # send_response_to_client(data, communication_socket)

            print("waiting for command (IN WRITE)...")
            # communication_socket, client_address = s_socket.accept()
            # client_write_data = communication_socket.recv(1024).decode('utf-8')
            print("Received the content of the file as: (IN WRITE)", text)
            f.write(text)
            communication_socket.send('Got your message for Server3. Thank you!'.encode('utf-8'))
            communication_socket.close()
            print(f'Communication with ended in S3!')
    else:
        data = "File doesn't exist"
        send_response_to_client(data, communication_socket)


def reading_file(wanted_filename, s_socket, communication_socket, client_address):
    if wanted_filename in (listing_files_in_folder()):
        with open(wanted_filename, "r") as f:
            data = f.read()
    else:
        data = "File doesn't exist"
    send_response_to_client(data, communication_socket)


def renaming_file(wanted_filename, new_filename, s_socket, communication_socket, client_address):
    if wanted_filename in (listing_files_in_folder()):
        with open(wanted_filename, "w") as f:
            # input_filename = "Enter the new name of the file: "
            # send_response_to_client(input_filename, communication_socket)
            print("waiting for command (IN WRITE)...")
            # communication_socket, client_address = s_socket.accept()
            # new_filename = communication_socket.recv(1024).decode('utf-8')
            print("Received the new name of the file as: (IN WRITE)", new_filename)
            os.rename(wanted_filename, new_filename)
            send_response_to_client("name changed successfully", communication_socket)
            communication_socket.close()
            print(f'Communication with {client_address} ended!')


def change_directory(main_dir, wanted_filename, s_socket, communication_socket, client_address):
    if wanted_filename == ".":
        os.chdir(main_dir)
        send_response_to_client("Directory changes to main successfully", communication_socket)
    elif wanted_filename in (listing_files_in_folder()):
        os.chdir(wanted_filename)
        send_response_to_client("S3: Directory changes successfully", communication_socket)
    else:
        send_response_to_client("S3: Directory doesn't exist", communication_socket)
    communication_socket.close()
    print(f'Communication with {client_address} ended!')


def creating_new_directory(wanted_filename, s_socket, communication_socket, client_address):
    if wanted_filename not in (listing_files_in_folder()):
        os.mkdir(wanted_filename)
        send_response_to_client("Directory created successfully", communication_socket)
    else:
        send_response_to_client("Directory already exits", communication_socket)
    communication_socket.close()
    print(f'Communication with {client_address} ended!')


def logging_activity(command_name, message, user_name, current_dir):
    ct = str(datetime.datetime.now())
    with open(current_dir + "/server_logs", "a") as f:
        f.write(ct + " | " + "Command : " + command_name + " | " + message + "| Username: " + user_name + "\n")


def main():
    host = socket.gethostbyname('localhost')
    # host = '130.85.243.2'
    port = 9092
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((host, port))
    s_socket.listen(5)
    main_dir = os.getcwd()
    print('Server 3 is listening!......')

    while True:
        communication_socket, client_address = s_socket.accept()
        print(f'Connected to {client_address}')
        # getting username
        # getting password
        # authorizing the client or users
        # users exist? or else create new directory

        print("Processing the message received from client...")
        input_client_message = communication_socket.recv(1024).decode('utf-8')
        print(f'Message from client is: {input_client_message}')

        client_message, user, text = input_client_message.split("|")

        client_message_0 = client_message.split()[0]
        if len(client_message.split()) > 1:
            wanted_filename = client_message.split()[1]

        if client_message_0 == "ls":
            existing_files = listing_files_in_folder()
            if existing_files is None:
                send_response_to_client("No files exist", communication_socket)
            else:
                send_response_to_client(existing_files, communication_socket)
            communication_socket.close()
            print(f'Communication with {client_address} ended!')
        if client_message_0 == "create":
            creating_file(wanted_filename, communication_socket, client_address)
            logging_activity(client_message_0, wanted_filename, user, main_dir)
        if client_message_0 == "delete":
            deleting_file(wanted_filename, communication_socket, client_address)
            logging_activity(client_message_0, wanted_filename, user, main_dir)
        if client_message_0 == "write":
            writing_into_file(wanted_filename, text, s_socket, communication_socket, client_address)
            logging_activity(client_message_0, wanted_filename, user, main_dir)
        if client_message_0 == "rename":
            renaming_file(wanted_filename, text.replace(" ", ""), s_socket, communication_socket, client_address)
            logging_activity(client_message_0, wanted_filename, user, main_dir)
        if client_message_0 == "read":
            reading_file(wanted_filename, s_socket, communication_socket, client_address)
            logging_activity(client_message_0, wanted_filename, user, main_dir)
        if client_message_0 == "cd":
            change_directory(main_dir, wanted_filename, s_socket, communication_socket, client_address)
            logging_activity(client_message_0, wanted_filename, user, main_dir)
        if client_message_0 == "mkdir":
            creating_new_directory(wanted_filename, s_socket, communication_socket, client_address)
            logging_activity(client_message_0, wanted_filename, user, main_dir)


if __name__ == "__main__":
    main()
