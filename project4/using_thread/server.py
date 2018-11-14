import socket
import threading
import sys

nth_client = 0
client_list = list()


def recv_msg(nth_socket):
    global client_list
    global nth_client

    while True:
        try:
            message = client_list[nth_socket-1].recv(1024).decode()
            message_format = '[{}_{}] {}'.format(message[1:7],nth_socket,message[8:])
            print(message_format)
            if message[9:13].lower() == 'quit':
                break
        except:
            pass
    client_list[nth_socket-1].close()
    client_list.pop(nth_socket-1)
    nth_client -=1
    print('Client Disconnected')
    
def send_msg(socket):
    global client_list
    try:
        while True:
            message = input('[Server]')
            if message[0:4].lower() == 'quit':
                send_clients('server DisConnected')
                break
            send_clients(message)
    except:
        pass
    socket.close()
    print('server terminated')
    return
        
        
def send_clients(message):
    global client_list
    for client in range(len(client_list)):
        client_list[client].send(('[server]'+message).encode())


def main():
    if len(sys.argv) !=2:
        print("python chat_server.py [PORTNUMBER]")
        sys.exit()
    port_number = int(sys.argv[1])

    global nth_client
    global client_list

    chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_server_socket.bind(('',port_number))
    chat_server_socket.listen(5)

    while nth_client <=5:
        (client_socket,addr) = chat_server_socket.accept()
        client_list.append(client_socket)
        nth_client+=1
        print('Client '+str(nth_client)+' connect')
        print('start chat :')
        threading.Thread(target=recv_msg, args=(nth_client,)).start()
        threading.Thread(target=send_msg, args=(chat_server_socket,)).start()

    print('Clinet Disconnected')
    chat_server_socket.close()

if __name__=="__main__":
    main()

