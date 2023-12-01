import socket
import sys
import traceback
from NetworkingHelpers import *
from threading import Thread

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
#
# receive_packet(connection, max_buffer_size)
#   The purpose of this function is to receive and process an incoming packet.


# The purpose of this function is to
# (a) create a server socket,
# (b) listen on a specific port,
# (c) receive and process incoming packets,
# (d) forward them on, if needed.
def start_server():
    # 1. Create a socket.
    host = "127.0.0.1"
    port = 8005
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Sockets created")

    # 2. Try binding the socket to the appropriate host and receiving port (based on the network topology diagram).
    try:
        soc.bind((host, port))

    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    # 3. Set the socket to listen.
    print("Router 5 now listening")
    soc.listen(1)

    # 4. Read in and store the forwarding table.
    forwarding_table = read_csv("input/router_5_table.csv")

    # 5. Store the default gateway port.
    default_gateway_port = find_default_gateway(forwarding_table)

    # 6. Generate a new forwarding table that includes the IP ranges for matching against destination IPS.
    forwarding_table_with_range = generate_forwarding_table_with_range(forwarding_table)

    # 7. Continuously process incoming packets.
    while True:
        # 8. Accept the connection.
        connection, address = soc.accept()
        ip, port = soc.getpeername()
        print("Connected with " + ip + ":" + port)

        # 9. Start a new thread for receiving and processing the incoming packets.
        try:
            processing_thread(connection, ip, port, forwarding_table_with_range, default_gateway_port)

        except:
            print("Thread did not start.")
            traceback.print_exc()


# The purpose of this function is to receive and process incoming packets.
def processing_thread(connection, ip, port, forwarding_table_with_range, default_gateway_port, max_buffer_size=5120):
    # 1. Connect to the appropriate sending ports (based on the network topology diagram).
    con = connection.connect((ip, port))

    # 2. Continuously process incoming packets
    while True:
        # 3. Receive the incoming packet, process it, and store its list representation
        packet = receive_packet(con, max_buffer_size)
        sendTo = -1

        # 4. If the packet is empty (Router 1 has finished sending all packets), break out of the processing loop
        if len(packet[0]) < 1:
            break

        # 5. Store the source IP, destination IP, payload, and TTL.
        sourceIP = packet[0]
        destinationIP = packet[1]
        payload = packet[3]
        ttl = packet[4]

        # 6. Decrement the TTL by 1 and construct a new packet with the new TTL.
        new_ttl = str(int(ttl) - 1)
        new_packet = sourceIP + "," + destinationIP + "," + payload + "," + new_ttl

        # 7. Convert the destination IP into an integer for comparison purposes.
        destinationIP_bin = ip_to_bin(destinationIP)
        destinationIP_int = int(destinationIP_bin, 2)

        # 8. Find the appropriate sending port to forward this new packet to.
        for item in forwarding_table_with_range:
            if destinationIP_int >= item[4] and destinationIP_int <= item[5]:
                sendTo = item[3]

        # 9. If no port is found, then set the sending port to the default port.
        if sendTo == -1:
            sendTo = default_gateway_port

        # 11. Either
        # (a) send the new packet to the appropriate port (and append it to sent_by_router_2.txt),
        # (b) append the payload to out_router_2.txt without forwarding because this router is the last hop, or
        # (c) append the new packet to discarded_by_router_2.txt and do not forward the new packet
        if sendTo == default_gateway_port and new_ttl != 0:
            f = open("output/out_router_5.txt", "a")
            f.write(payload + "\n")
            f.close()
            print("OUT:", payload)

        else:
            print("DISCARD:", new_packet)
            f = open("output/discarded_by_router_5.txt", "a")
            f.write(new_packet)
            f.close()


# Main Program

# 1. Start the server.
start_server()