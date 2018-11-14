import socket
import sys
class client():

    def __init__(self):
        self.server_IP = '127.0.0.1'
        self.server_port = 2345
        self.request_url = sys.argv[1]
        self.http_method = sys.argv[2]


    def tcp_connect(self):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((self.server_IP,self.server_port))
        
        print("Connet to Sever...")
        
        http_header = self.make_http_header(self.request_url,self.http_method)
        client_socket.send(http_header.encode())
        print("Send Message to Server : ",http_header)
        recv_data = client_socket.recv(1024)

        if recv_data in b'HTTP/1.1 404 Not Found\r\n':
            print("404 Not Found  ERROR : Not Found File:",self.request_url)
            client_socket.close()
        else:
            length = self.parsing_data(recv_data)
            self.download_file(client_socket,recv_data,length)    
            client_socket.close()


    def parsing_data(self,data):
        split_data = data.split(b'\n')
        get_header = split_data[1].decode('utf-8')
        print(get_header)
        split_data = get_header.split(":")
        data = split_data[2]
        split_data = data.split(',')
        length = split_data[0].replace(' ','')
        return int(length)


    def download_file(self,socket,data,length):
        data_piece =data
        file_name_split = self.request_url.split('.')
        file_name = file_name_split[0]+'_download.'+file_name_split[1]
        count = 0;
        with open(file_name,'wb') as f:
            print(length)
            try: 
                while True:
                    if len(data_piece) >= length:
                        break
                    print(data)
                    data = socket.recv(1024)
                    data_piece += data
                
                print(8)
                receive_data = data_piece
                data_split = receive_data.split(b' \r\n')
                f.write(data_split[1])
                f.close()
            except:
                print("error while download the ",self.request_url)

    def make_http_header(self,url,method):

        http_template = method+' '+url+''' HTTP/1.1\r\nAccept:*/*\r\nAccept-Encoding: gzip,deflate\r\nAccept-Language: utf-8\r\n'''
        return http_template

        
    def main(self):
        self.tcp_connect()


if __name__=="__main__":
    client = client()
    client.main()

