import socket
import threading
import os
import time
import ssl
import base64
import sys
from urllib import parse
import hue
class Server():
    def __init__(self):
        self.ip_address = 'localhost'
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
            split_url = request_url.split("?")
            if len(split_url)>1:
                print("split",split_url)
                self.check_is_hue(split_url)
                request_url = split_url[0]
            self.make_response_header(request_url,socket)

        else:
            pass


        socket.close()
        time.sleep(5)

    def check_is_hue(self,url):
        print("url",url)
        if url[0]  == '/hueControl.html':
            hue_args = url[1].split("&")
            self.controll_hue(hue_args)

    def controll_hue(self,hue_args):
        hue_num = hue_args[0][4]
        print("hue,args",hue_args)
        power = hue_args[0].split("=")[1]
        print("power",power)
        brightness = hue_args[1].split("=")[1]
        X = hue_args[2].split("=")[1]
        Y = hue_args[3].split("=")[1]
        print("!!!!!",hue_num,power,brightness,X,Y)
        hues = hue.hue()
        hues.power_controll(hue_num,power)
        hues.brightness_controll(hue_num,brightness)
        hues.color_controll(hue_num,X,Y)






    def get_file(self,url,f):
        if f is  None:
            f =open(url,'rb')
        try:
            data = f.read(1024)
            return [data,f]
        except:
            print("error while read file")
            return None


    def parsing_request_header(self,data):

        data_str = str(data.decode('utf-8'))
        split_data = data_str.split('\r\n')
        get_url = split_data[0].split()
        print("header request msg",get_url)
        try:
            return get_url[1]
        except Exception as e:
            print(e)



    def make_response_header(self,url,socket):

        if url[0] == '/':
            url = '.'+url
        else:
            url = './'+url
        if os.path.isfile(url):
            print("there is file",url)
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
            print('there isn\'t file - ',url)
            socket.send(self.FILE_NO.encode())

    def get_mail_info(self,url):
        info = dict()
        split_url = url.split('&')
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


    def main(self):
        self.createSocket()

if __name__ == "__main__":
    server = Server()
    server.main()
