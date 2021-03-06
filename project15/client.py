import socket
import sys
import threading
from threading import *
def recv_message(message_socket): 
    try:
        while True:
            message = message_socket.recv(1024)
            print(message.decode())
            if message[7:11].lower() == 'quit':
                break
    except:
        message_socket.close()
        #print(message_socket.close())

def main():
    if len(sys.argv) !=3:
        print('python groupchatclient.py [IPADDRESS] [PORTNUMBER]')
        sys.exit(0)

    ip_address = sys.argv[1]
    port_number = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_number))

    print('Host connected')

    recv_thread = threading.Thread(target = recv_message, args = (client_socket,))
    recv_thread.start()

    while True:
        message = input('[Client] ')
        send_msg = '[Client] '+message
        client_socket.send(send_msg.encode())

        if message[0:4].lower() == 'quit':
            client_socket.close()
            break
    client_socket.close()
    print('Host Disconnected')
    

if __name__ =="__main__":
    main()
