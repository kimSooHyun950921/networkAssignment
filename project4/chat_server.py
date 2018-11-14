import socket
import threading
import sys

def recv_msg(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

        if message[9:13].lower() == 'quit':
            break

    print('Client Disconnected')

def main():
    if len(sys.argv) !=2:
        print("python chat_server.py [PORTNUMBER]")
        sys.exit()

    port_number = int(sys.argv[1])

    chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_server_socket.bind(('',port_number))
    chat_server_socket.listen(1)

    (client_socket,addr) = chat_server_socket.accept()
    print('Client connect')
    print('start chat :')

    threading.Thread(target=recv_msg, args=(client_socket,)).start()

    while True:
        message = input('')
        client_socket.send(('[Server] ' +message).encode())

        if message[0:4].lower() == 'quit':
            break

    print('Clinet Disconnected')
    chat_server_socket.close()

if __name__=="__main__":
    main()

