import socket
import sys
import time
import os
import glob
from NetworkingHelpers import *

# FUNCTIONS FROM NETWORKINGHELPERS
# create_socket(host, port)
#   The purpose of this function is to set up a socket connection.
#
# read_csv(path)
#   The purpose of this function is to read in a CSV file.
#
# find_default_gateway(table)
#   The purpose of this function is to find the default port when no match
#   is found in the forwarding table for a packet's destination IP.
#
# ip_to_bin(ip : str)
#   The purpose of this function is to convert a string IP to its binary representation.
#
# find_ip_range(network_dst, netmask)
#   The purpose of this function is to find the range of IPs inside a given a destination IP address/subnet mask pair.
#
# bit_not(n, numbits=32)
#   The purpose of this function is to perform a bitwise NOT on an unsigned integer.
#
# generate_forwarding_table_with_range(table)
#   The purpose of this function is to generate a forwarding table that includes the IP range for a given interface.
#   In other words, this table will help the router answer the question:
#   Given this packet's destination IP, which interface (i.e., port) should I send it out on?
#   Destination, Netmask, Gateway, Interface
#
# write_to_file(path, packet_to_write, send_to_router=None)
#   The purpose of this function is to write packets/payload to file.

# Main Program

# 0. Remove any output files in the output directory
# (this just prevents you from having to manually delete the output files before each run).
files = glob.glob('./output/*')
for f in files:
    os.remove(f)

# 1. Connect to the appropriate sending ports (based on the network topology diagram).
print("Router 1 creating sockets")
socketTo2 = create_socket("127.0.0.1", 8002, True)
# socketTo2.connect(("127.0.0.1", 8002))

socketTo4 = create_socket("127.0.0.1", 8004, True)
# socketTo4.connect(("127.0.0.1", 8004))

# 2. Read in and store the forwarding table.
print("Router 1 reading in forwarding table")
forwarding_table = read_csv("input/router_1_table.csv")

# 3. Store the default gateway port.
print("Router 1 storing gateway port")
default_gateway_port = find_default_gateway(forwarding_table)

# 4. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
print("Router 1 generating new forwarding table")
forwarding_table_with_range = generate_forwarding_table_with_range(forwarding_table)

# 5. Read in and store the packets.
print("Router 1 reading and storing packets")
packets_table = read_csv("input/packets.csv")

# time.sleep(2)

# 6. For each packet,
for packet in packets_table:
    # 7. Store the source IP, destination IP, payload, and TTL.
    sourceIP = packet[0]
    destinationIP = packet[1]
    payload = packet[2]
    ttl = packet[3]

    # 8. Decrement the TTL by 1 and construct a new packet with the new TTL.
    new_ttl = str(int(ttl) - 1)
    new_packet = sourceIP + "," + destinationIP + "," + payload + "," + new_ttl

    # 9. Convert the destination IP into an integer for comparison purposes.
    destinationIP_bin = ip_to_bin(destinationIP)
    destinationIP_int = int(destinationIP_bin, 2)

    # 9. Find the appropriate sending port to forward this new packet to.
    sendTo = -1
    for item in forwarding_table_with_range:
        if destinationIP_int >= item[4] and destinationIP_int <= item[5]:
            print("Send to:")
            sendTo = item[3].strip()
            print(sendTo)
            break

    # 10. If no port is found, then set the sending port to the default port.
    if sendTo == -1:
        sendTo = default_gateway_port

    # 11. Either
    # (a) send the new packet to the appropriate port (and append it to sent_by_router_1.txt),
    # (b) append the payload to out_router_1.txt without forwarding because this router is the last hop, or
    # (c) append the new packet to discarded_by_router_1.txt and do not forward the new packet

    if sendTo == "8002" and new_ttl != 0:
        print("sending packet", new_packet, "to Router 2")
        socketTo2.send(new_packet.encode())
        f = open("output/sent_by_router_1.txt", "a")
        f.write(new_packet + "\n")
        f.close()

    elif sendTo == "8004" and new_ttl != 0:
        print("sending packet", new_packet, "to Router 4")
        socketTo4.send(new_packet.encode())
        f = open("output/sent_by_router_1.txt", "a")
        f.write(new_packet + "\n")
        f.close()

    elif sendTo == default_gateway_port and new_ttl != 0:
        f = open("output/out_router_1.txt", "a")
        f.write(payload + "\n")
        f.close()
        print("OUT:", payload)

    else:
        print("DISCARD:", new_packet)
        f = open("output/discarded_by_router_1.txt", "a")
        f.write(new_packet + "\n")
        f.close()

    # Sleep for some time before sending the next packet (for debugging purposes)
    time.sleep(1)