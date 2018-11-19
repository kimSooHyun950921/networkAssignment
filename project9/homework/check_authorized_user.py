from sniffing import sniffing
from IRC_chat import IRC_chat
from hue import hue
import struct
import subprocess
import threading

class check_auth_user:
    def __init__(self):
        self.__sniff = sniffing()
        self.__hue_ctrl = hue()
        self.__registered_user_list = ["3035ad765802"]
        self.__ping_ip = None
        self.__is_connected = False



    def __get_sniffing(self,debug=True):
        while True:
            try:

                header_info ,ip= self.__sniff.start_sniff("dhcp")
                if ip is not None:
                    self.__ping_ip = ip

                if header_info is not None:
                    header = header_info[1]
                    header = header.hex()
                    if header in self.__registered_user_list:
                        self.power_control_hue("on")
                        self.__is_connected = True
                        threading.Thread(target=self.is_ping,args=(self.__ping_ip,)).start()
            except Exception as e:
                print(e)

    def power_control_hue(self,power):
        for i in range(3):
            self.__hue_ctrl.power_controll(i+1,power)

    def is_ping(self,ip):
        while True:
            if ip is None:
                return None
            p1 = subprocess.call(["ping","-c 1",ip],stdout=subprocess.PIPE)
            if p1 is None or p1 == 1:
                self.power_control_hue("off")
                self.__ping_ip = None


    def main(self):
        self.__get_sniffing()










if __name__ == '__main__':
    check = check_auth_user()
    check.main()
