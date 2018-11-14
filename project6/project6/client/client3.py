import socket
import sys
from bs4 import BeautifulSoup
import time
import threading 
import concurrent.futures
class client():

    def __init__(self):
        self.server_IP = '192.168.1.66'
        self.server_port = 2345
        self.request_url = sys.argv[1]
        self.http_method = sys.argv[2]
        self.start_time = float()
        self.end_time = float()

    def recv_msg(self,socket):
        try:
            while True:
                recv_data = socket.recv(1024)
                print('getFirstData',recv_data.decode())
                if recv_data in b'HTTP/1.1 404 Not Found\r\n':
                    print("404 Not Found  ERROR : Not Found File:",self.request_url)
                else:
                    length = self.parsing_data(recv_data)
                    file_name = self.download_file(client_socket,recv_data,length)
                    if file_name is not None:
                        img_list = self.parseHTML(file_name)
                        self.send_data(img_list,socket)
        except Exception as e:
            print(e)

    def send_data(self,lists):
        while len(lists) is not 0:
            url = lists.pop()
            url = url['src']
            print('url',url[0:2])       
            if url[0:2] =='./':
                url = url[2:]
            print('url change',url)
            header = self.http_method+' '+url+' '+'HTTP/1.1'
            socket = self.make_connect_with_server()
            socket.send(header.encode())


            receive_data = socket.recv(1024)
            print(receive_data)
            self.download_file(socket,receive_data)
        self.end_time = time.time()


    def make_connect_with_server(self):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((self.server_IP,self.server_port))
        print('img server connect ok')
        return client_socket
        





    def parseHTML(self,url):
        img_list = []
        with open(url,'r') as fp:
            soup = BeautifulSoup(fp,features='lxml')
            img_list = soup.find_all('img')

        return img_list
    def tcp_connect(self,execute_num):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((self.server_IP,self.server_port))
       
        print("Connet to Sever...")
        self.start_time = time.time()
        http_header = self.make_http_header(self.request_url,self.http_method)
        client_socket.send(http_header.encode())
        
        print("Send Message to Server : ",http_header)
        recv_data = client_socket.recv(1024)

        if recv_data in b'HTTP/1.1 404 Not Found\r\n':
            print("404 Not Found  ERROR : Not Found File:",self.request_url)
        else:
            file_name = self.download_file(client_socket,recv_data)

            if file_name is not None:
                img_list = self.parseHTML(file_name)
                self.send_data(img_list)

        self.end_time = time.time()
        
        result = self.end_time - self.start_time
        self.write_performance(execute_num,result)


    def write_performance(self,execute_num,result):
        if execute_num is 10:
            f = open('execute_10process/process_result.csv','a')
        elif execute_num is 20:
            f = open('execute_20process/process_result.csv','a')
        elif execute_num is 30:
            f = open('execute_30process/process_result.csv','a')
        f.write(str(result)+'\n')
        print(result)

    def parsing_data(self,data):
        split_data = data.split(b'\r\n')
        get_header = split_data[1].decode('utf-8')
        split_data = get_header.split("\t")

        return int(length)


    def download_file(self,socket,data):
        data_piece =data
        file_name_split = self.request_url.split('.')
        file_name = file_name_split[0]+'_download.'+file_name_split[1]
        count = 0;
        with open(file_name,'wb') as f:
            try: 
                while len(data)>0:
                    data = socket.recv(1024)
                    data_piece += data
                
                receive_data = data_piece
                data_split = receive_data.split(b'\r\n')
                f.write(data_split[1])
                f.close()
                return file_name

            except Exception as e:
                print("error while download the ",self.request_url,"error - ",e)
                return None


    def make_http_header(self,url,method):

        http_template = method+' '+url+''' HTTP/1.1\r\nAccept:*/*\r\nAccept-Encoding: gzip,deflate\r\nAccept-Language: utf-8\r\n'''
        return http_template

    
    def main(self):
        with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
            for i in range(0,10):
                executor.submit(self.tcp_connect(10))
            for i in range(0,20):
                executor.submit(self.tcp_connect(20))
            for i in range(0,30):
                executor.submit(self.tcp_connect(30))


    
if __name__=="__main__":
   client = client()
   client.main()
