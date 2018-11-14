import select
import socket
import sys

class Server:
    def __init__(self):
        self.input_list = []
        self.chat_sever_socket=''
        self.client_list = []

    def find_what_socket(self,finding_socket):
        i = 0
        while i<len(self.client_list):
            if self.client_list[i] is finding_socket:
                return i
            i+=1



    def recv_msg(self,client_socket):
        data = client_socket.recv(1024).decode()
        socket_num = self.find_what_socket(client_socket)

        if not data or data[9:] =='quit':
            print('client_'+str(socket_num)+' is Disconnected')
            self.client_list.remove(client_socket)
            self.input_list.remove(client_socket)
            return
        
        what_socket = '[client_'+str(socket_num)+']'
        print(what_socket,data[9:])
        
    def connect_client_socket(self,input_fd):
        client_socket, addrss = input_fd.accept()
        self.client_list.append(client_socket)
        
        what_socket = self.find_what_socket(client_socket)
        print('client_'+str(what_socket)+' connected')
        client_socket.setblocking(0)
        client_socket.send('Host Connected'.encode())
        self.input_list.append(client_socket)
        

    def send_messages(self,io,fds):
        message = input('[server]')
        message = '[server] '+message
        for sockets in fds:
            if sockets is not self.chat_server_socket and sockets is not sys.stdin:
                sockets.send(message.encode())
        return message
        

    def main(self):
        if len(sys.argv) !=2:
            print("python chat_server.py [PORTNUMBER]")
            sys.exit()

        port_number = int(sys.argv[1])

        self.chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_server_socket.setblocking(0)
        self.chat_server_socket.bind(('',port_number))
        self.chat_server_socket.listen(5)

        self.input_list = [sys.stdin,self.chat_server_socket]

        outputs = []    
        send_data = ''
        exit_flag = 0
        while self.input_list:
            input_fd,write_fd,except_fd = select.select(self.input_list,outputs,self.input_list)
            for fd in  input_fd:
                if fd is self.chat_server_socket:
                    
                    self.connect_client_socket(fd)
                    
                elif fd is sys.stdin:
                    flag =self.send_messages(fd,self.input_list)
                    
                    if flag[9:] == 'quit':
                        exit_flag = 1
                        break
                else:
                    self.recv_msg(fd)
            if exit_flag==1:
                break
            
        print('Clinet Disconnected')
        self.chat_server_socket.close()

if __name__=="__main__":
    server =  Server()
    server.main() 

     
