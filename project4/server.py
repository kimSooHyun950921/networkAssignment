'''
리눅스는 소켓역시 하나의 파일로 인식한다.
select란?
    file descriptor의 변화를 인식해서 알려주는것
    보통 file descriptor들의 묶음으로 변화를 알려준다.
    여기서는 먼저 chat_server_socket 을 file descriptor변화를 알리기위한 집합으로써 만들어준다.

    그후, socket들이 연결되면 연결된 client_socket의 select 에 넣어서  변화를 확인한다.

    반환값은?

'''

import select
import socket
import sys
import queue
def recv_msg(client_socket):
    print(recv_msg)
    while True:
        data = client_socket.recv(1024).decode()
        print(data)
    

def main():
    if len(sys.argv) !=2:
        print("python chat_server.py [PORTNUMBER]")
        sys.exit()

    port_number = int(sys.argv[1])

    chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_server_socket.setblocking(0)
    chat_server_socket.bind(('',port_number))
    chat_server_socket.listen(5)

    input_list = [chat_server_socket]

    outputs = []    
    message_queues = {}# 데이터를 보내는데 버퍼로서 사용하기 위해 필요
#    print('Client connect')
#    print('start chat :')
    send_data = ''
    while input_list:
        input_fd,write_fd,except_fd = select.select(input_list,outputs,input_list)
        client_socket = ''
        i = 0
        print(input_fd)
        for s in input_fd:
            #연결 요청 발생
            if s is chat_server_socket:
                print('[연결 요쳥 발생]')   
                client_socket,address = s.accept()
                client_socket.setblocking(0)
                client_socket.send(('Host Connected').encode())
                input_list.append(client_socket)
                continue
                #수락
            #연결 요청이 아니라면
            print(s)
            if s is not sys.stdin:
                try:
                    print('[data 받음]')
                    data = s.recv(1024).decode()
                    #메세지 읽어들임 
                    if data:
                        print("data:",)
                        print(data,s.getpeername())
                        if data == 'quit':
                            print("print 해야함")
                except Exception as e:
                    print('데이터 에러',e)
                try:
                    message = sys.stdin.readline()
                    s.send(message.encode())
                    sys.stdout.write('[server]')
                    sys.stdout.flush()
                except Exception as e:
                    print('readError',e)

    print('Clinet Disconnected')
    chat_server_socket.close()

if __name__=="__main__":
    main()
 
