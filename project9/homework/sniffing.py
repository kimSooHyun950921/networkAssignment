import socket
import struct

class sniffing:
    def __init__(self):
        self.__raw_socket = socket.socket(
                                        sock.AF_PACKET,
                                        socket.SOCK_RAW,socket.ntohs(0x0003)
                                        )
    def __packet_sniffing(self):
        recv_packet = self.__raw_socket.recvfrom(5000)
        ethernet_protocol = struct.unpack("!6s6sH",(recv_packet[0])[:14])[2]
        if ethernet_protocol == 0x800:
            ip_protocol = struct.unpack("!BBHHHBBH4s4s",recv_packet[0][14:34])[6]
            if ip_protocol == 17:
                udp_src_port = struct.unpack("!H",(recv_packet[0])[34:36])[0]
                if udp_src_port == 68:
                    return self.__print_header_info(recv_packet)

    def __print_header_info(self,packet,debug=True):
        ethernet,ipv4,udp,dhcp=self.__parsing_packet(packet)
        if debug:
            print("Ethernet Header : ",ethernet)
            print("IPv4 Header :",ipv4)
            print("UDP Header":,udp)
            print("DHCP Data:",dhcp)
        return (ether,ipv4,udp,dhcp)



    def __parsing_packet(self,packet):
        ethernet_header = packet[0][0:14]
        IPv4_headr = packet[0][14:34]
        udp_header = packet[0][34:42]
        dhcp_data = packet[0][42:]
        return ethernet_header,IPv4_headr,udp_header,dhcp_data

    def start_sniff():
        return self.__packet_sniffing()
