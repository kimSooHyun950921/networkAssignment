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
        self.validToDo = None

    def read_file(self,file_name):
        data = None
        with open(file_name, 'rb') as file:
            data = pickle.load(file)
        return data
    def write_file(self,file_name,data):
        with open(file_name, 'wb') as wfile:
            pickle.dump(data,wfile)

    def masking_ip(self,networks):
        networks = networks.split('/')
        raw_ip = networks[0]
        mask = int(networks[1])
        Trie.DEBUG_MSG("mask : "+str(mask))
        ip = self.ip_to_bit(raw_ip)
        if mask == 0:
            return None
        return ip[0:mask]

    def ip_to_bit(self, raw_ip):
        bin_ip = []
        for x in raw_ip.split("."):
            x_part_bin = format(int(x),'08b')
            bin_ip.append(str(x_part_bin))
        all_bin = ''.join(bin_ip)

        Trie.DEBUG_MSG("final_result : "+all_bin+"\n\t raw_ip : "+raw_ip)
        return all_bin

    def traverse_trie(self):
        random_ips = self.read_file('random_ip_list.pickle')
        make_validation_data = list()
        for cur_ip in random_ips:
            traversal_root = self.root
            ip = self.ip_to_bit(cur_ip)
            temp_data = None
            if ip == None:
                continue
            Trie.DEBUG_MSG('random ip -'+ip)
            for bit in ip:
                Trie.DEBUG_MSG('traversal_root  info : '+ str(traversal_root))
                try:
                    if self.is_leaf(traversal_root):
                        Trie.DEBUG_MSG(self.is_leaf(traversal_root))
                        break
                    if traversal_root.data != None:
                        temp_data = traversal_root.data
                    if bit == '0':
                        traversal_root = traversal_root.left
                        Trie.DEBUG_MSG('traversal_root left info : '+ str(traversal_root))
                    elif bit == '1':
                        traversal_root = traversal_root.right
                        Trie.DEBUG_MSG('traversal_root right info : '+ str(traversal_root))
                except:
                    break
            if traversal_root == None and temp_data != None:
                Trie.DEBUG_MSG('random ip\'s nexts hop - '+temp_data.next_hop()+'\n\n')
                make_validation_data.append((cur_ip,temp_data.next_hop()))
                continue
            elif traversal_root !=None and traversal_root.data != None:
                Trie.DEBUG_MSG('random ip\'s next hop - '+traversal_root.data.next_hop()+'\n\n')
                make_validation_data.append((cur_ip,traversal_root.data.next_hop()))
            else:
                Trie.DEBUG_MSG("ERROR")
                make_validation_data.append((cur_ip,None))
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
            Trie.DEBUG_MSG('masking ip - '+str(ip))
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
    def validate_data(self,checking_data):
        Trie.DEBUG_MSG("validate")

        validation_data= self.read_file('trietree_resultset.pickle')
        differ_count = 0
        
        i = 0
        while i < len(checking_data):
            cdata = checking_data[i]
            vdata = validation_data[i]
            Trie.DEBUG_MSG("check : "+str(cdata) + "valid:"+str(vdata))
            if self.cmp(cdata,vdata) == False:
                differ_count += 1
                Trie.DEBUG_MSG("diff : "+str(differ_count))
            i+=1
        return differ_count

    def cmp(self, cdata, vdata):
        if cdata[0]== vdata[0] :
            if cdata[1] == vdata[1]:
                return True
        return False
    
    def main(self):
        import time
        start_time = time.time()
  #      if not os.path.isfile('tree.pickle'):
        self.make_trie()
        self.write_file('tree.pickle',self.root)
        self.root = self.read_file('tree.pickle')
        
        #if not os.path.isfile('ValidCheck.pickle'):
        result = self.traverse_trie()
        self.write_file('ValidCheck.pickle',result)
        checking_data = self.read_file('ValidCheck.pickle')

        result = self.validate_data(checking_data)

        if result > 0:
            print("[RESULT] NOT Validate ", result)
        else:
            print("[RESULT] Validate")
        end_time = time.time()
        print("TAKE_TIME : "+str(end_time-start_time))


if __name__ == "__main__":
  trie_ex = Trie()
  trie_ex.main()


