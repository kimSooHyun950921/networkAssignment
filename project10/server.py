'''
서버 html파일을 읽는 클래스
'''
import socket
import threading
import os
import time
import sys
from bs4 import BeautifulSoup


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
    def __get_mp3_file():
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
    @staticmethod
    def __html_templates(srces, download_name, file_name):
        tr_templates = """
    <tr>
      <td>
        <audio controls>
          <source src='"""+srces+"""' type='audio/mpeg'>
        </audio>
      </td>
      <td>
        <a href='"""+srces+"""' download='"""+download_name+"""'>
          """+file_name+"""</a>
      </td>
    </tr>
    """
        return tr_templates

    @staticmethod
    def __find_template_loc(html_list):
        i = 0
        print(html_list)
        for element in html_list:
            print(element)
            print(element.find("</tr>"))
            if element.find("</tr>") > 0:
                print("I", i)
                return i
            i += 1
        return -1

    def add_mp3_to_html(self,url):

        mp3_list = Server.__get_mp3_file()
        html_list = Server.__read_files()
        loc = Server.__find_template_loc(html_list)
        print(loc)

        for mp3 in mp3_list:
            src = "./mp3_file/"+mp3
            print("INFO", src, mp3, mp3)
            html_list.insert(loc+1, Server.__html_templates(src, mp3, mp3))
            loc  += 1

        with open(url[2:], 'w') as html:
            html.writelines(html_list)

    @staticmethod
    def __read_files():
        with open('html_template.txt', 'r') as html:
            return html.readlines()

    def send_http(self, url, client_socket):
        if os.path.isfile(url):
            print('there is file', url)
            is_first = True
            self.add_mp3_to_html(url)

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


    def make_response_header(self, url, client_socket):
        url = Server.__make_relative_path(url)
        file_extension = url.split(".")[2]
        if file_extension == "html":

            self.send_http(url, client_socket)
        elif file_extension == "mp3":
            print(url)
            print(file_extension)
            with open(url,'rb') as mp3_file:
                byte_file = self.FILE_OK+'\n'
                byte_file = byte_file.encode()+mp3_file.read()
                client_socket.send(byte_file)
    def main(self):
        self.createSocket()

if __name__ == '__main__':
    server = Server()
    server.main()
