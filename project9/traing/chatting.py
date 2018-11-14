from socket import *

portNumber = 6667
servername = 'chat.freenode.net'

sock = socket(AF_INET,SOCK_STREAM)
sock.connect((servername,portNumber))

sock.send("NICK U201402329\r\n".encode())
sock.send("USER U201402329 U201402329 U201402329 : cnu bot\r\n".encode())
sock.send("JOIN #CNU\r\n".encode())
while 1:
    text = sock.recv(4096)
    text = text.decode()
    print(text)

    if text.find("JOIN")!=-1:
        sock.send(('PRIVMSG #CNU :HELLOS [['+text[1:11]+']]\r\n').encode())
sock.close()
