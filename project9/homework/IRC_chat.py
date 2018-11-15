from socket import *
from  hue import hue


class IRC_chat:
    def __init__(self):
        self.__hue = hue()
        self.__portNumber = 6667
        self.__servername = "chat.freenode.net"
        self.__socket = self.__server_connect()
        self.__error_count = 0

    def __server_connect(self):
        sock = socket(AF_INET,SOCK_STREAM)
        sock.connect((self.__servername,self.__portNumber))
        sock.send("NICK U201402329\r\n".encode())
        sock.send("USER U201402329 U201402329 U201402329: cnu bot\r\n".encode())
        sock.send("JOIN #CNU\r\n".encode())
        return sock

    def DEBUG_MODE(self,msg,debug=True,):
        if debug:
            print(msg)

    def __recv_data(self):
        while 1:
            try:
                text = self.__socket.recv(4096)

                text = text.decode()

                check = self.check_infinite_loop(text)
                if check:
                    self.__controll_hue(text)
                else:
                    continue
            except Exception as e:
                self.DEBUG_MODE(str('error occur cause'+str(e)))

    def preprocess_text(self,text):
        text = text.replace('\r\n','')
        text = text.split(" ")
        new_text = text[3:]
        return new_text


    def check_infinite_loop(self,text):
        if self.__error_count >=10:
            self.__socket.close()
            self.__socket = self.__server_connect()
            self.__error_count = 0
            return False
        if len(text) == 0:
            self.__error_count +=1
            return False

        else:
            return True


    def __controll_hue(self,text):
        new_text = self.preprocess_text(text)
        if new_text[0] == ":hue":
            self.get_hue_command(new_text)

    def get_hue_command(self,text):
        hue_num = text[1]
        args = text[2]

        if args == 'set':
            self.__hue.power_controll(hue_num,text[3])
        if args == 'brightness':
            self.__hue.brightness_controll(hue_num,text[3])
        if args == 'color' :
            self.__hue.color_controll(hue_num,text[3],text[4])

    def main(self):
        self.__recv_data()
        self.__socket.close()


if __name__ == '__main__':
    chat = IRC_chat()
    chat.main()
