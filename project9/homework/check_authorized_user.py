from sniffing import sniffing
from IRC_chat import IRC_chat
from hue import hue

class check_auth_user:
    def __init__(self):
        self.__sniff = sniffing()
        self.__hue_ctrl = hue()
        self.__registered_user_list = ["30:35:AD:76:58:02"]
    def __registered_user_list(self):
        return self.__registered_user_list
    def __sniffing(self):
        return self.__sniff
    def __hue(self):
        return self.__hue_ctrl

    def __get_sniffing(self,debug=True):
        while True:
            header_info = self.__sniffing().start_sniff()
            if header_info[0] in self.__registered_user_list():
                self.power_control_hue(1)
            else:
                self.power_control_hue(0)
                
    def power_control_hue(self.power):
        for i in rage([0:2]):
            self.__hue().power_controll(i,power)










if __name__ == '__main__':

    main()
