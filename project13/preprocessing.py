"""
Preprocess : iptable의 정보를 전처리 해주는 함수
"""
import pickle
DEBUG = True
class Preprocess:

    @staticmethod
    def print_debug_msg(line):
        if DEBUG:
            print("[DEBUG] ", line, "\n")

    def __init__(self):
        self.__store_ip_address = list()
        self.__store_ip_set = list()
    #getter setter
    def store_ip_address(self):
        return self.__store_ip_address
    def set_store_ip_address(self, new_ip_address):
        self.__store_ip_address = new_ip_address
    def store_ip_set(self):
        return self.__store_ip_set
    def add_store_ip_set(self, ip_route_info):
        self.store_ip_set().append(ip_route_info)



    def file_read(self):
        file_name = 'oix-full-snapshot-2018-11-01-2200'
        #file_name = 'sample.txt'
        with open(file_name, 'r') as route_file:
            line = route_file.readline()
            is_first_line = True
            while True:
                if line == "":
                    break
                if '*' in line and not is_first_line:
                    ip_info = self.make_dict(line)
                    Preprocess.print_debug_msg("store ip adress : "+ str(self.store_ip_address()))

                    if not self.store_ip_address():
                        self.set_store_ip_address(ip_info)
                        continue
                    self.preprocess_route_info(ip_info)
                is_first_line = False
                line = route_file.readline()

            self.add_store_ip_set(self.store_ip_address())



    def file_write(self):
        print("he")
        Preprocess.print_debug_msg(self.store_ip_set())
        for row in self.store_ip_set():
            Preprocess.print_debug_msg(row)
            Preprocess.print_debug_msg("\n")


        file_name = 'mid_result.pickle'
        with open(file_name, 'wb') as write_file:
            pickle.dump(self.store_ip_set(), write_file)




    def make_dict(self, line):
        line = line.split()


        route_info = dict()
        route_info['Network'] = line[1]
        route_info['Next Hop'] = line[2]
        route_info['Metric'] = line[3]
        route_info['LocPrf'] = line[4]
        route_info['Weight'] = line[5]
        path_len = 0
        path_list = list()
        path_index = 6

        while True:
            end_of_row = ['i', '?', 'e']
            if  line[path_index] in end_of_row:
                break
            path_len += 1
            path_list.append(line[path_index])
            path_index += 1
        route_info['Path_Len'] = path_len
        route_info['Path'] = path_list
        return route_info

    def preprocess_route_info(self, cur_route_info):
        Preprocess.print_debug_msg("<!!!!1>")

        compare_route_info = self.store_ip_address()
        Preprocess.print_debug_msg(cur_route_info)

        if cur_route_info['Network'] == compare_route_info['Network']:
            self.choose_which_route_info(cur_route_info, compare_route_info)
        else:
            self.add_store_ip_set(self.store_ip_address())
            Preprocess.print_debug_msg("chosing data : "+str(self.store_ip_address()))
            self.set_store_ip_address(cur_route_info)

    def choose_which_route_info(self, cur, compare):
        if cur['Weight'] > compare['Weight']:
            self.set_store_ip_address(cur)
        elif cur['Weight'] < compare['Weight']:
            self.set_store_ip_address(compare)
        else:
            self.compare_LocPrf(cur, compare)
    def compare_LocPrf(self, cur, compare):
        if cur['LocPrf'] > compare['LocPrf']:
            self.set_store_ip_address(cur)
        elif cur['LocPrf'] < compare['LocPrf']:
            self.set_store_ip_address(compare)
        else:
            self.compare_path(cur, compare)
    def compare_path(self, cur, compare):
        if cur['Path_Len'] > compare['Path_Len']:
            self.set_store_ip_address(compare)
        elif cur['Path_Len'] < compare['Path_Len']:
            self.set_store_ip_address(cur)

    def main(self):
        Preprocess.print_debug_msg("start debug\nstart file_read and write")
        self.file_read()
        Preprocess.print_debug_msg("end preprocessing\nstart file write")
        self.file_write()
if __name__ == "__main__":
    preprocess = Preprocess()
    print("start")
    preprocess.main()
