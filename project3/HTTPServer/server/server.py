import socket
import threading 
import os
import time
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
               # client_num = client_thread(client_socket)
               # client_num.run()
            
           # self.data_send_recv(client_socket,address)
        
    def data_send_recv(self,socket,address):
           # try:
                data = socket.recv(5000)
                request_url = self.parsing_request_header(data)
                response_header = self.make_response_header(request_url)
                socket.send(response_header.encode())
                time.sleep(5)
           # except:
           #     print("error while sending and receiving files")

    def get_file(self,url):
        f = open(url,'rb')
        try:
            data = f.read()
            return data.decode('utf-8')
        except:
            print("error while read file")
            return None

    def parsing_request_header(self,data):
        '''
            요청한 URL 을 파악한다.
            @return:URL
            @param: http header
        '''
    
        data_str = str(data.decode('utf-8'))
        split_data = data_str.split('\r\n')
        get_url = split_data[0].split()
        print(get_url)
        url = get_url[1]
        url = url.replace('/','') 
        if url[0] == '/':
            url = url.replace('/','')
        return url
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
                print(request_msg)
            return request_msg
        else:
            return self.FILE_NO

    def main(self):
        self.createSocket()

if __name__ == "__main__":
    server = Server()
    server.main()
