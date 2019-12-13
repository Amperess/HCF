import socket
from hopCountFiltering import HCFStateManager
from struct import *
import sys

def PacketMonitoring():

    # set up the packet manager
    ipAddrs = ["10.0.2.100", "10.0.3.100"]
    packetManager = HCFStateManager(ipAddrs, 0.1, 0.2)

    # set up the socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    # catch set up errors
    except socket.error as e:
        err = e.args[0]
        print ("Error setting up socket: ", e)
        sys.exit()

    # Leave socket open to recieving packets
    while True:
        packet = sock.recvfrom(65535)
        packet = packet[0]
        ip_header = packet[0:20]
        iphead = unpack ("!BBHHHBBH4s4s", ip_header)
        version_ihl = iphead[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        ttl = iphead[5]
        source_addr = socket.inet_ntoa(iphead[8])
        source_addr = socket.inet_ntop(socket.AF_INET, source_addr)
        dest_addr = socket.inet_ntoa(iphead[9])
        dest_addr = socket.inet_ntop(socket.AF_INET, dest_addr)

        print("\nSource IP address: ", source_addr)
        print("TTL: ", ttl)

        packetTest = packetManager.accept_packet({'ttl':ttl, 'src':source_addr})
        if packetTest == 1 :
            print("Packet accepted")
        elif packetTest == -1:
            print("Packet flagged")
        else:
            print("Packet dropped")

if __name__ == "__main__":
    PacketMonitoring()
