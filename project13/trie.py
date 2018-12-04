import pickle
class Trie:
    def __init__(self):
        self.data = self.read_file()
        self.left = Trie()
        self.right = Trie()

    def read_file(self):
        data_list = list()
        with open('mid_result.pickle', 'rb') as file:
            while True:
                try:
                    data = pickle.load(file)
                except EOFError:
                    break
                data_list.append(data)
        return data_list
    def ip_to_bit(self, networks):
        networks = networks.split('/')
        raw_ip = networks[0]
        bin_ip = []
        mask = networks[1]
        for x in raw_ip.split("."):
            bin_ip.append(format(x, "b"))
        all_bin = ''.join(bin_ip)
        return all_bin[0:mask-1]
