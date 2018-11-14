import socket
import ssl
import base64
import sys
class SMTP_server():
    def __init__(self):
        self.context = ssl.create_default_context()
        self.hostname = 'smtp.naver.com'
        self.port = 465
        self.ID=sys.argv[1]
        self.password =sys.argv[2]
        self.send_addrss = ''
        self.receive_address = ''
        self.data =[]
    def create_socket(self):
        context = ssl.create_default_context()
        client_sock = socket.create_connection((self.hostname,self.port))
        ssl_client_sock = context.wrap_socket(client_sock,server_hostname=self.hostname)
        return ssl_client_sock

    def input_data(self):
        print("메일 내용을 알려주세요:")
        all_data = []
        input_data = input()
        while input_data != ".":
            all_data.append(input_data+'\r\n')
            input_data = input()
        all_data.append('.\r\n')
        return all_data

    def input_info(self):
        info = dict()
        print("=======smtp 메일 보내는 작업을 시작합니다=======\n\n")

        self.send_address = input("송신 메일주소를 입력하세요:")
        self.receive_address = input("발신 메일주소를 입력하세요:")
        inputs = self.input_data()
        self.data = inputs


    def send_smtp(self):
        socket = self.create_socket()
        stop_flag = 0
        while True:
            
                recv_message = socket.recv(5120)
                print("server:",recv_message.decode())
                msg_code = recv_message[0:3].decode() 
                if stop_flag == 1:
                    break

               # msg_code = int(msg_code)                   
             
                if  msg_code == '334':
                    send_ID = base64.b64encode((self.ID).encode())
                    send_password = base64.b64encode((self.password).encode())
                    Enters = '\r\n'.encode()
                    socket.send(send_ID+Enters)
                    print("client : ",send_ID.decode())
                    print("server:",socket.recv(1024).decode())
                    socket.send(send_password+Enters)
                    print("client:",send_password.decode())

                elif msg_code == '235':
                    send_from ='MAIL FROM: <'+self.send_address+'>\r\n'
                    send_to = "RCPT TO:<"+self.receive_address+">\r\n"

                    socket.send((send_from).encode())
                    print("client : "+send_from+"\n")

                    print("server :",socket.recv(1024))
                    socket.send((send_to).encode())
                    print("client :",send_to)

                elif msg_code=='354':
                    for i in range(len(self.data)):
                        socket.send(self.data[i].encode())
                        print("client : "+self.data[i])

                else:
                    send_message = input('client : ')
                    send_message+='\r\n'
                    socket.send(send_message.encode())
                    if send_message == 'quit\r\n' or send_message=='QUIT\r\n':
                     stop_flag = 1   
            
                
    def main(self):
        self.send_smtp()
if __name__=='__main__':
    if len(sys.argv) < 3:
        print('python3 smtp_servr.py [NAVER_ID] [PASSWORD]')
    else:
        smtp = SMTP_server()
        smtp.input_info()
        smtp.send_smtp()
