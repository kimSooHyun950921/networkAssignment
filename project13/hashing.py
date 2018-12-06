import pickle
class hashing:
    DEBUG = True
    MAX_HASH_SIZE = 90000

    @staticmethod
    def DEBUG_MSG(msg):
        if hashing.DEBUG == True:
            print("[DEBUG] ", msg, "\n")

    def __init__(self):
        self.hash_table = dict()
        self.route_data = self.read_file('mid_result.pickle')
        self.valid_data = self.read_file('trietree_resultset.pickle')
    def read_file(self, file_name):
        with open(file_name,'rb') as f:
            data = pickle.load(f)
            return data
    def write_file(self,file_name,data):
        with open(file_name,'wb') as f:
            pickle.dump(data,f)

    def init_table(self):
        init_index = 0
        hash_list = list()
        #while init_index < hashing.MAX_HASH_SIZE:
        #    hash_list.append(dict())
        #    init_index += 1
        return dict()

    def ip_to_bin(self,ip):
        bin_ip = list()
        hashing.DEBUG_MSG("IP-"+str(ip))
        for part_ip in ip.split('.'):
            x_part_bin = format(int(part_ip),'08b')
            bin_ip.append(str(x_part_bin))
        all_bin = ''.join(bin_ip)
        hashing.DEBUG_MSG("IP:"+str(ip)+"bin:"+all_bin)
        return all_bin

    def split_ip_mask(self,networks):
        networks = networks.split('/')
        ip = networks[0]
        mask = int(networks[1])
        hashing.DEBUG_MSG("mask : "+str(mask))
        return self.masking_ip(ip,mask)

    def masking_ip(self,networks,mask):
        ip = self.ip_to_bin(networks)
        if mask == 0:
            return None
        return ip[0:mask]

    def make_hashtable(self):
        for data in self.route_data:
            hashing.DEBUG_MSG(str(data))

            ip = data['Network']
            bin_ip = self.split_ip_mask(ip)
            if bin_ip == None:
                continue

            hash_ip = hash(bin_ip)
            hashing.DEBUG_MSG("hashing ip :"+str(hash_ip)+" "+str(bin_ip))

            #insert hash
            #{hash_ip:[{bin_ip:(ip,data)......}]
            insert_data = {bin_ip:(ip,data['Next Hop'])}
            if self.hash_table.get(hash_ip) == None:
                self.hash_table[hash_ip] = list()
                self.hash_table[hash_ip].append(insert_data)
            else:
                get_list = hash_table[hash_ip]
                get_list.append(insert_data)
                hash_table[hash_ip] = get_list
            hashing.DEBUG_MSG('hash_table['+str(hash_ip)+']='+str(self.hash_table[hash_ip]))
            

    def traverse_hash(self):
        random_ips = self.read_file('random_ip_list.pickle')
        make_validation_data = list()
        prefix_leng = 8

        ongoing_index = 0
        #traverse start
        for ip in random_ips:
            hashing.DEBUG_MSG("we go here :"+str(ongoing_index)+"random ip :"+str(ip))
            #맞는 IP들을 모두 골라온다.
            find_matching_ip = list()
            prefix_leng = 8

            while prefix_leng <= 32:
                hashing.DEBUG_MSG("prefix_leng : "+str(prefix_leng))
                # Ip를 bin화
                mask_bin_ip = self.masking_ip(ip,prefix_leng)
                hashing.DEBUG_MSG("random ip_mask: "+str(mask_bin_ip))
                #해시화
                hash_ip = hash(mask_bin_ip)
                #해시테이블로부터 리스트를을 가져온다
                get_list = None
                if self.hash_table.get(hash_ip) !=None:
                    get_list = self.hash_table[hash_ip]
                else:
                    hashing.DEBUG_MSG("NO in the hash table"+str(hash_ip))
                    prefix_leng +=1
                    continue
                # 해시 리스트로부터 ip를 찾는다. 
                slot = None 
                list_index = 0
                for table_ip in get_list:
                    if table_ip.get(mask_bin_ip) != None:
                        break
                    list_index += 1

                slot = self.hash_table[hash_ip][list_index]
                hashing.DEBUG_MSG("slot: "+str(slot))
                if slot == None:
                    hashing.DEBUG_MSG("there is no slot about :"+str(ip))
                    continue
                    #find_matching_ip 저장
                next_hop = slot[mask_bin_ip][1]
                slot_ip  = slot[mask_bin_ip][0]
                ip_split =slot_ip.split('/')
                prefix = ip_split[1]
                raw_ip = ip_split[0]
                reconstruct_ip = (raw_ip,prefix_leng,next_hop)
                hashing.DEBUG_MSG("re ip: "+str(reconstruct_ip))
                find_matching_ip.append(reconstruct_ip)
                prefix_leng = prefix_leng + 1



            if len(find_matching_ip) == 0:
                next_hop = None
            else:
                find_matching_ip = sorted(find_matching_ip, key = lambda ip_info : ip_info[1],reverse=True)
                next_hop = find_matching_ip[0][2]
                hashing.DEBUG_MSG("next_hop: "+str(next_hop)+"which ip : "+str(find_matching_ip[0]))
            print("ip",ip,"next_hop",next_hop)
            ongoing_index += 1
            make_validation_data.append((ip,next_hop))
        return make_validation_data

    def validate_data(self, check_data):
        differ_count = 0
        i = 0
        while i < len(self.valid_data):
            cdata = check_data[i]
            vdata = self.valid_data[i]
            hashing.DEBUG_MSG("check : "+str(cdata)+"valid : "+str(vdata))
            if self.cmp(cdata,vdata) == False:
                differ_cont+=1
                hashing.DEBUG_MSG("diff")
            i+=1
        return differ_count

    def cmp(self, cdata, vdata):
        if cdata[0]== vdata[0] :
            if cdata[1] == vdata[1]:
                return True
        return False








        




    
    def main(self):
        import time
        import os
        start_timestamp = time.time()
        if not os.path.isfile('hash_result.pickle'):
            self.make_hashtable()
            find_dest_ips = self.traverse_hash()
            self.write_file("hash_result.pickle",find_dest_ips)
        checking_data = self.read_file('hash_result.pickle')
        result = self.validate_data(checking_data)




        if result > 0:
            print("[RESULT] NOT Validate ", result)
        else:
            print("[RESULT] Validate")
        end_timestamp = time.time()
        take_time = end_timestamp - start_timestamp
        print("TAKE TIME : ",take_time)

if __name__ == "__main__":
    hashings = hashing()

    hashings.main()










        
