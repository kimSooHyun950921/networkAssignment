import socket
import threading 
import os
import time
import ssl
import base64
import sys
from urllib import parse
class Server():
    def __init__(self):
        self.ip_address = '192.168.1.66'
        self.port_number = int(sys.argv[1])
        self.FILE_OK = 'HTTP/1.1 200 OK\r\n'
        self.FILE_NO = 'HTTP/1.1 404 Not Found\r\n'

    def createSocket(self):
        
            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                server_socket.bind((self.ip_address,self.port_number))
            except Exception as e:
                print("bind error",e)
                server_socket.close()
                return

            print("server socekt open...")
            print("listening...")
            server_socket.listen(5)

            print("Connected with client")
            while True:
               client_socket,address = server_socket.accept()
               threading.Thread(target=self.data_send_recv, args=(client_socket,address)).start()
            
        
    def data_send_recv(self,socket,address):
           
        data = socket.recv(5000)
        request_url = self.parsing_request_header(data)
        if request_url is not None:
            
            self.make_response_header(request_url,socket)
        else:
            pass
        socket.close()
        time.sleep(5)

    def get_file(self,url,f):
        if f is  None:
            f =open(url,'rb')
        try:
            data = f.read(1024)
            return [data,f]
        except:
            print("error while read file")
            return None

    def get_mail_info(self,url):
        info = dict()
        split_url = url.split('&')
        #print(split_url)
        info['ID'] = split_url[0].split('=')[1]
        info['password'] = split_url[1].split('=')[1]
        info['send_mail_address']=parse.unquote(split_url[2].split('=')[1])
        
        info['mail_title'] = parse.unquote(split_url[3].split('=')[1])#.decode('utf-8')
        info['mail_area'] = parse.unquote(split_url[4].split('=')[1])#.decode('utf-8')
        return info

    def create_mail_socket(self):
        context = ssl.create_default_context()
        client_sock = socket.create_connection(('smtp.naver.com',465))
        ssl_client_sock = context.wrap_socket(client_sock,server_hostname='smtp.naver.com')
        return ssl_client_sock

    def encode_base64(self,info):
        return base64.b64encode(info.encode())

    def send_mail(self,info):
        try:
            Enters ='\r\n'.encode()
            socket = self.create_mail_socket()
            print(socket.recv().decode())
            socket.send('EHLO naver.com'.encode()+Enters)
            print(socket.recv().decode())
            socket.send('AUTH LOGIN'.encode()+Enters)
            print(socket.recv().decode())
            socket.send((self.encode_base64(info['ID'])+Enters))
            print(socket.recv().decode())
            socket.send((self.encode_base64(info['password'])+Enters))
            print(socket.recv().decode())
            socket.send(('MAIL FROM: <'+info['ID']+'@naver.com>\r\n').encode())
            print(socket.recv().decode())
            socket.send(('RCPT TO: <'+info['send_mail_address']+'>\r\n').encode())
            print(socket.recv().decode())
            socket.send('DATA\r\n'.encode())
            print(socket.recv().decode())
            msg = '''SUBJECT:'''+info['mail_title']+'''\r\nFROM:'''+info['ID']+'''@naver.com\r\nTO:'''+info['send_mail_address']+'''\r\n'''+info['mail_area']+'''\r\n.\r\n '''
            print(msg)
            socket.send(msg.encode())
            print(socket.recv().decode())
            socket.send('QUIT'.encode())
            print(socket.recv().decode())
            return True
        except Exception as e:
            print(e)

        return False



        
    def parsing_request_header(self,data):
         
        data_str = str(data.decode('utf-8'))
        split_data = data_str.split('\r\n')
        get_url = split_data[0].split()
        print("headerrequest",get_url)
        try:
            url = get_url[1] 
            """
            if len(url[22:]) > 0:
                info = self.get_mail_info(url)
                result = self.send_mail(info)
                return 'mail_send_ok.html'
            """
            url = url.replace('?','')    
           # print("url",url)
           # print(url)
            return url
        except Exception as e:
            print(e)    
    
    def response_header_templates(self,data):
         response_headers = {
                 #"Content-Type":"text/html",
                 #"Content-Length": len(data),
                 #"Connection": 'close'
                 }
         return response_headers

    def make_response_header(self,url,socket):
        
        if url[0] == '/':
            url = '.'+url
        else:
            url = './'+url
        print(url)
        if os.path.isfile(url):
            print("there is fileE",url)
            is_first = True
            f = open(url, "rb")

            while True:
                file_data = f.read(1024)

                if len(file_data) == 0:
                    break
                content_length = str(len(file_data))
                if is_first:
                    request_msg = self.FILE_OK+"\n"
                    request_msg = request_msg.encode()+file_data
                    is_first = False
                    socket.send(request_msg)
                else:
                    request_msg=file_data
                    socket.send(request_msg)
            
            f.close()
                
        else:
            print('nofile')
            socket.send(self.FILE_NO.encode())


    def main(self):
        self.createSocket()

if __name__ == "__main__":
    server = Server()
    server.main()
