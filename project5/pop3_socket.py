import socket
import ssl
import sys
class POP3_server():
    def __init__(self):
        self.context=ssl.create_default_context()
        self.hostname = 'pop.naver.com'
        self.port = 995
        self.id = sys.argv[1]
        self.password = sys.argv[2]

    def create_socket(self):
        context= ssl.create_default_context()
        client_sock = socket.create_connection((self.hostname,self.port))
        ssl_client_sock = context.wrap_socket(client_sock,server_hostname=self.hostname)
        return ssl_client_sock

    def print_message(self,socket):
        msg = socket.recv(200000)
        split_msg = msg.split('\r\n'.encode())
        #msg = socket.recv(1024)
        for msg in split_msg:
            try:
                if msg.decode() == '-ERR':
                    pass
                print(msg.decode())
                
                
            except:
                print(msg)
                

    def send_msg(self,socket,message):

        return socket.send(message)

    def send_pop3(self):
        socket = self.create_socket()
        stop_flag = 0
        self.print_message(socket)
        socket.send(('user '+self.id+'\r\n').encode())
        self.print_message(socket)
        socket.send(('pass '+self.password+'\r\n').encode())
        while socket is not 0:
            try:
                self.print_message(socket)
                socket.settimeout(1.5)
            
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
        self.send_pop3()
            
if __name__ =='__main__':
    if len(sys.argv) < 3:
        print('python3 pop3_server.py [NAVER_ID] [PASSWORD]')
    else:    
        server = POP3_server()
        server.main()

