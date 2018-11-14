import io
import socket
import sys
import select

def main():
    if len(sys.argv) !=3:
        print('python groupchatclient.py [IPADDRESS] [PORTNUMBER]')
        sys.exit(0)

    ip_address = sys.argv[1]
    port_number = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_number))

    

    read_list = [sys.stdin,client_socket]
    end_flag =0 
    while True:
    
        read_socket, write_socket, error_socket = select.select(read_list,[],[])
        for read_message in read_socket:
            if read_message is client_socket:
                data = read_message.recv(1024).decode()
                if not data:
                    print( '\n Disconnected from chat server')
                    sys.exit()
                else:
                    print(data)
                    sys.stdout.flush()

            else:
                message = input('[client]')
                client_socket.send(('[client] '+message).encode())
                if message == 'quit':
                    end_flag = 1
                    break
        if end_flag ==1:
            break
    print('Host Disconnected')
    client_socket.close()

if __name__ =="__main__":
    main()
