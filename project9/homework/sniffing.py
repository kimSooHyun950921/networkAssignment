import socket
import struct
class sniffing:
    def __init__(self):
        self.__raw_socket = socket.socket(
                                        socket.AF_PACKET,
                                        socket.SOCK_RAW,
                                        socket.ntohs(0x0003)
                                        )

    def __packet_sniffing(self,protocol):
        recv_packet = self.__raw_socket.recvfrom(5000)
        ethernet_protocol = struct.unpack("!6s6sH",(recv_packet[0])[:14])[2]
        ethernet_header = struct.unpack("!6s6sH",(recv_packet[0])[:14])
        #print(ethernet_header[1].hex())
        if ethernet_protocol == 0x800:
            ip_protocol = struct.unpack("!BBHHHBBH4s4s",recv_packet[0][14:34])[6]

            if ip_protocol == 17:
                udp_src_port = struct.unpack("!H",(recv_packet[0])[34:34+2])[0]
                if udp_src_port == 68 and protocol == "dhcp":
                    ip =self.parsing_dhcp_data((recv_packet[0])[42:])
                    return (ethernet_header,ip)
        return None,None


    def parsing_dhcp_data(self,packet):
        dhcp = struct.unpack("!4s",packet[267:267+4])
        dhcp = dhcp[0]
        dhcp =dhcp.hex()
        string_dhcp = str(int(dhcp[0:2],16)) +"."+str(int(dhcp[2:4],16))+"."+str(int(dhcp[4:6],16))+"."+str(int(dhcp[6:8],16))



        return string_dhcp

    def start_sniff(self,protocol):
         headers,ip = self.__packet_sniffing(protocol)
         return headers,ip
