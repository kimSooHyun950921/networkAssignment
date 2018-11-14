import socket
import struct

def main():
    raw_socket = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(0x0003))
    while True:
        recv_packet = raw_socket.recvfrom(5000)

        ethernet_protocol = struct.unpack('!6s6sH',(recv_packet[0])[:14])[2]
        if ethernet_protocol == 0x800:
           ip_protocol = struct.unpack("!BBHHHBBH4s4s",recv_packet[0][14:34])[6]
           if ip_protocol ==17:
              udp_src_port = struct.unpack('!H',(recv_packet[0])[34:34+2])[0]
              if udp_src_port ==68:
                 print("Ethernet Header : ",recv_packet[0][0:14])
                 print("IPv4 Header : ",recv_packet[0][14:34])
                 print("UDP Header : " ,recv_packet[0][34:42])
                 print("DHCP DATA : ",recv_packet[0][42:])

if __name__ =="__main__":
   main()
              
