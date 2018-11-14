import socket
import threading 
import os
import time
import ssl
import base64
from urllib import parse
class Server():
    def __init__(self):
        self.ip_address = '127.0.0.1'
        self.port_number = 2345
        self.FILE_OK = 'HTTP/1.1 200 OK\r\n'
        self.FILE_NO = 'HTTP/1.1 404 Not Found\r\n'

    def createSocket(self):
        
            server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                server_socket.bind((self.ip_address,self.port_number))
            except:
                print("bind error")
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
            response_header = self.make_response_header(request_url)
            socket.send(response_header.encode())
        else:
            pass
        time.sleep(5)

    def get_file(self,url):
        f = open(url,'rb')
        try:
            data = f.read()
            return data.decode('utf-8')
        except:
            print("error while read file")
            return None
    def get_mail_info(self,url):
        info = dict()
        split_url = url.split('&')
        print(split_url)
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
        '''
            요청한 URL 을 파악한다.
            @return:URL
            @param: http header
        '''
    
        data_str = str(data.decode('utf-8'))
        split_data = data_str.split('\r\n')
        get_url = split_data[0].split()
        print("headerrequest",get_url)
        try:
            url = get_url[1] 
            
            if len(url[22:]) > 0:
                info = self.get_mail_info(url)
                result = self.send_mail(info)
                return 'mail_send_ok.html'
            url = url.replace('?','')    
            url = url.replace('/','') 
            if url[0] == '/':
                url = url.replace('/','')
            return url
        except:
            pass
    def response_header_templates(self,data):
         response_headers = {
                 "Content-Type":"text/html",
                 "Content-Length": len(data),
                 "Connection": 'close'
                 }
         return response_headers

    def make_response_header(self,url):
        """
            @param:request url
            서버가 보유한 파일이라면
            @return:HTTP/1.1 200 OK
            서버가 보유하지 않는 파일이라면
            @return:HTTP/1.1 404 Not Found'
        """
        
        if os.path.isfile(url):
            file_data = self.get_file(url)
            content_length = str(len(file_data))
            if file_data is not None:
                request_msg = self.FILE_OK+" "+str(self.response_header_templates(file_data))+" \r\n"+file_data
                print("header",request_msg)
            return request_msg
        else:
            return self.FILE_NO

    def main(self):
        self.createSocket()

if __name__ == "__main__":
    server = Server()
    server.main()
