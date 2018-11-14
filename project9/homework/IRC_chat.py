import socket import *
from  hue import hue


class IRC_chat:
    def __init__(self):
        self.portNumber = 6667
        self.servername = "chat.freenode.net"
        self.server_connect(servername,portNumber)

    def server_connect(self,servername,portNumber):
        sock = socket(AF_INET,SOCK_STREAM)
        sock.connect((servername,portNubmer))
        sock.send("NICK U201402329\r\n".encode())
        sock.send("USER 201402329 U201402329 U201402329: cnu bot\r\n".encode())
        sock.send("JOIN #CNU\r\n".encode())

    def recv_data(self):
        while 1:
            text = sock.recv(4096)
            text = text.decode()
            print(text)
            if text[0:2] =="hue":
                self.controll_hue(text)


    def controll_hue(self,text):
        split_text = hue.split(" ")
        hue_num = split_text[1]
        hue_controll_args = split_text[2]
        self.check_which_hue_controll(hue_num,split_text[3])

    def check_which_hue_control(self,hue_num,args):
        if hue_controll_args is 'set':
            hue.power_controll(hue_num,args)
        if hue_controll_args is 'brightness':
            hue.brightness_controll(hue_num,args)
        if hue_controll_args is 'color' :
            hue.color_controll(hue_num,args)
