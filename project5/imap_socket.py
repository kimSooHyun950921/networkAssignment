import socket
import ssl
import sys
class IMAP_server():
    def __init__(self):
        self.context = ssl.create_default_context()
        self.hostname = 'imap.naver.com'
        self.port = 993
        self.email = sys.argv[1]
        self.password = sys.argv[2]

    def create_socket(self):
        context= ssl.create_default_context()
        client_sock = socket.create_connection((self.hostname,self.port))
        ssl_client_sock = context.wrap_socket(client_sock,server_hostname=self.hostname)
        return ssl_client_sock

    def print_message(self,socket):
#        msg = socket.recv()
#        print(msg.decode())
#        while msg is not None:

            msg = socket.recv(20000)
            print(msg.decode())
            

    def send_msg(self,socket,message):

        return socket.send(message)

    def send_imap(self):
        socket = self.create_socket()
        stop_flag = 0
        self.print_message(socket)
        socket.send(('a login '+self.email+' '+self.password+'\r\n').encode())
        while socket is not 0:
            try:
                msg = socket.recv(100000)
                socket.settimeout(1.5)
                print(msg.decode())
                send_msg = input()
                if send_msg == '':
                    continue
                else:
                    print(send_msg)
                    socket.send((send_msg+"\r\n").encode())
            except Exception as e:
                send_msg = input()
                socket.send((send_msg+"\r\n").encode())
                
    def main(self):
        self.send_imap()

if __name__ =='__main__':
    if len(sys.argv) < 3:
        print('python3 imap_server.py [EMAIL] [PASSWORD]')
    else:
        server = IMAP_server()
        server.main()

