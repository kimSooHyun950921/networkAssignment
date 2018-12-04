import pickle
import os
from node import node
from trie_node import trie_node
class Trie:
    DEBUG = True
    @staticmethod
    def DEBUG_MSG(msg):
        if Trie.DEBUG ==True:
            print("[DEBUG]",msg,"\n")

    def __init__(self):
        self.routing_table = self.read_file('mid_result.pickle')
        self.root = None

    def read_file(self,file_name):
        data = None
        with open(file_name, 'rb') as file:
            data = pickle.load(file)
        return data
    def write_file(self,file_name):
        with open(file_name, 'wb') as wfile:
            pickle.dump(self.root,wfile)

    def masking_ip(self,networks):
        networks = networks.split('/')
        raw_ip = networks[0]
        mask = int(networks[1])
        ip = self.ip_to_bit(raw_ip)
        if ip == None:
            return None
        return ip[0:mask-1]

    def ip_to_bit(self, raw_ip):
        bin_ip = []
        for x in raw_ip.split("."):
            bin_ip.append(str(bin(int(x)))[2:])
        all_bin = ''.join(bin_ip)

        Trie.DEBUG_MSG("final_result : "+all_bin+"\n\t raw_ip : "+raw_ip)
        return all_bin

    def traverse_trie(self):
        random_ips = self.read_file('random_ip_list.pickle')
        make_validation_data = list()
        for cur_ip in random_ips:
            traversal_root = self.root
            ip = self.ip_to_bit(cur_ip)
            if ip == None:
                continue
            Trie.DEBUG_MSG('random ip -'+ip)
            for bit in ip:
                Trie.DEBUG_MSG('traversal_root  info : '+ str(traversal_root))
                if self.is_leaf(traversal_root):
                    Trie.DEBUG_MSG(self.is_leaf(traversal_root))
                    break
                if bit == '0':
                    traversal_root = traversal_root.left
                    Trie.DEBUG_MSG('traversal_root left info : '+ str(traversal_root))
                elif bit == '1':
                    traversal_root = traversal_root.right
                    Trie.DEBUG_MSG('traversal_root right info : '+ str(traversal_root))
            if traversal_root.data != None:
                Trie.DEBUG_MSG('random ip\'s next hop - '+traversal_root.data.next_hop()+'\n\n')
                make_validation_data.append((cur_ip,traversal_root.data.next_hop()))
            else:
                Trie.DEBUG_MSG("ERROR")
        return make_validation_data

    def is_leaf(self, troot):
        if troot.left==None and troot.right==None:
            return True
        return False


    def make_trie(self):
        self.root = trie_node()
        for route_info in self.routing_table:
            temp_root = self.root
            networks = route_info['Network']
            ip = self.masking_ip(networks)
            if ip == None:
                continue
            for bit in ip:
                if bit == '0':
                    if temp_root.left== None:
                        new_left = trie_node()
                        temp_root.left = new_left
                        Trie.DEBUG_MSG('temp_root left info : '+ str(temp_root))
                    temp_root = temp_root.left
                    continue
                elif bit == '1':
                    if temp_root.right == None:
                        new_right = trie_node()
                        temp_root.right = new_right
                        Trie.DEBUG_MSG('temp_root right info : '+ str(temp_root))
                    temp_root = temp_root.right
                    continue
            temp_root.data = node(route_info['Next Hop'])
            Trie.DEBUG_MSG('temp_root FinalInfo info : '+ str(temp_root))
    def validate_data(self):
        checking_data = self.traverse_trie()
        validatioNone= self.read_file('trietree_resultset.pickle')
        differ_count = 0
        for cdata in checking_data:
            i = 0
            while i < len(validation_data):
                vdata = validation_data[i]
                if cmp(cdata,vdata) < 0:
                    differ_count += 1
                    Trie.DEBUG_MSG("check:"+cdata+"valid:"+vdata)
                    i+=1
            return differ_count
    
    def main(self):
        if not os.path.isfile('tree.pickle'):
            self.make_trie()
            self.write_file('tree.pickle')
        self.root = self.read_file('tree.pickle')
        result = self.validate_data()
        if result > 0:
            print("[RESULT] NOT Validate ", result)
        else:
            print("[RESULT] Validate")


if __name__ == "__main__":
  trie_ex = Trie()
  trie_ex.main()


