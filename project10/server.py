'''
서버 html파일을 읽는 클래스
'''
from bs4 import BeautifulSoup
import socket
import threading
import os
import time
import sys

class Server():
    '''
    서버 클래스
    '''
    def __init__(self):
        self.ip_address = 'localhost'
        self.port_number = int(sys.argv[1])
        self.FILE_OK = 'HTTP/1.1 200 OK\r\n'
        self.FILE_NO = 'HTTP/1.1 404 Not Found\r\n'

    def createSocket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self.ip_address, self.port_number))
        except Exception as e:
            print('bind error', e)
            server_socket.close()
            return

        print('server socekt open...')
        print('listening...')
        server_socket.listen(5)

        print('Connected with client')
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=self.data_send_recv, args=(client_socket, address)).start()


    def data_send_recv(self, client_socket,address):
        data = client_socket.recv(5000)
        request_url = self.parsing_request_header(data)

        if request_url is not None:
            split_url = request_url.split('?')
            if len(split_url) > 1:
                print('split', split_url)
                request_url = split_url[0]
            self.make_response_header(request_url, client_socket)

        client_socket.close()
        time.sleep(5)

    @staticmethod
    def get_mp3_file():
        path_dir = './mp3_file'
        file_list = os.listdir(path_dir)
        return file_list

    def parsing_request_header(self, data):

        data_str = str(data.decode('utf-8'))
        split_data = data_str.split('\r\n')
        get_url = split_data[0].split()
        print('header request msg', get_url)
        try:
            return get_url[1]
        except Exception as e:
            print(e)

    @staticmethod
    def __make_relative_path(url):
        if url[0] == '/':
            return '.'+url
        return './'+url

    def add_mp3_file(self,url):
        mp3_list = Server.get_mp3_file()
        with open(url, encoding='utf8') as file_name:
            html = file_name.read()
            print(html)
            soup = BeautifulSoup(html, 'html.parser')
            count = 1

            for mp3 in mp3_list:

        #        audio_path = soup.new_tag('audio', controls=True)
        #        audio_path.append(soup.new_tag('source', src=mp3, type='audio/mpeg'))
        #        soup.body.insert(count, audio_path)

                href = soup.new_tag('a', href=mp3)
                href.string = mp3+'_downloads'
                soup.body.insert(count,href)

                br = soup.new_tag('br')
                soup.body.a.insert_after(br)
                count += 1
            print(soup)
            return str(soup.prettify())

    def check_is_down_mp3(self, url):
        if url == './downloadRadioMP3.html':
            html = self.add_mp3_file(url)
            print(html)
            with open('downloadRadioMP3.html', 'w') as fp:
                fp.write(html)

    def make_response_header(self, url, client_socket):
        url = Server.__make_relative_path(url)
        if os.path.isfile(url):
            print('there is file', url)
            is_first = True
            self.check_is_down_mp3(url)
            with open('downloadRadioMP3.html', 'rb') as file_name:
                print("DONE", file_name)
                while True:
                    file_data = file_name.read(1024)
                    if len(file_data) == 0:
                        break
                    if is_first:
                        request_msg = self.FILE_OK+'\n'
                        request_msg = request_msg.encode()+file_data
                        is_first = False
                        client_socket.send(request_msg)
                    else:
                        request_msg = file_data
                        client_socket.send(request_msg)


        else:
            print('there isn\'t file - ', url)
            client_socket.send(self.FILE_NO.encode())



    def main(self):
        self.createSocket()

if __name__ == '__main__':
    server = Server()
    server.main()
