import socket
import select
import time
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT =1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

client_list = []

def store_username(client_socket):
    client_list.append(user['data'].decode('utf-8'))

def del_username(client_socket):
    client_list.remove(user['data'].decode('utf-8'))

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)   
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user
            store_username(client_socket)
            
            #print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
            print(f"{client_address[0]}:{client_address[1]} {user['data'].decode('utf-8')} has joined the chat!")
            start = time.time()

        else:
            message = receive_message(notified_socket)
            if message is not False:
                if message['data'].decode('utf-8') == "user":
                    print("Users online:")
                    for username in client_list:
                        print(username)
                    continue
                

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            start = time.time()


            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        end = time.time()
        if ((end - start) > 900000):
            del_username(client_socket)


    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]