from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

'''
Fill in start.
'''
buffer = 1000000
tcpSerSock.bind((sys.argv[1], 8080))
tcpSerSock.listen(1)
'''
Fill in end.
'''

while 1:
    print("============STARTING============")
    print("============STARTING============")
    print("============STARTING============")
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print("First try")
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(buffer).decode()  # Fill in start. # Fill in end.

    print("============Message============")
    print(message)

    if len(message) < 1:
        print("Failed to receive message")
        continue

    # Extract the filename from the given message
    print("============Message.split()[1]============")
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print("============Filename============")
    print(filename)

    fileExist = "false"
    fileToUse = "/" + filename
    print("============FileToUse============")
    print(fileToUse)

    try:
        raise IOError
        # Check whether the file exist in the cache
        f = open(fileToUse[1:], "r")
        # print("HEREHEREHERE")
        outputData = f.readlines()
        print("============OutputData============")
        print(outputData)
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        '''
        Fill in start.
        '''

        '''
        Fill in end.
        '''
        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:

        if fileExist == "false":
            # Create a socket on the proxyserver

            newSocket = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print("============hostn============")
            print(hostn)

            try:
                # Connect to the socket to port 80
                '''
                Fill in start.
                '''
                ip = gethostbyname(hostn)
                newSocket.connect((ip, 80))
                # newSocket.listen(1)

                #newSocket.connect((sys.argv[1], 80))
                #newSocket.listen(1)

                # tcpCliSock, addr2 = newSocket.accept()
                # print('Received a connection from:', addr2)
                # message2 = newCliSock.recv(buffer).decode()  # Fill in start. # Fill in end.
                # print(message2)

                '''
                Fill in end.
                '''
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileObj = newSocket.makefile('rbw', 0)
                # writeString = "GET " + "http://" + filename + " HTTP/1.0\n\n"
                writeString = f"GET http://{filename} HTTP/1.0\n\n"
                fileObj.write(writeString.encode())
                print(fileObj)
                print(type(fileObj))

                # Read the response into buffer
                '''
                Fill in start.
                '''
                # print(fileObj.readline())
                print("============READING FROM MAKEFILE============")

                example = fileObj.readline()
                print(example)
                response = []
                while len(example) > 0:
                    response.append(example)
                    example = fileObj.readline()

                for x in response:
                    print(x)

                print("Made it through")
                '''
                Fill in end.
                '''

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename, "wb")

                '''
                Fill in start.
                '''

                for i in response:
                    tcpCliSock.send(i)

                '''
                Fill in end.
                '''

            except Exception as e:
                print("Illegal request")
                print(e)
                exit()

        else:
            # HTTP response message for file not found
            '''
            Fill in start.
            '''

            '''
            Fill in end.
            '''

            # Close the client and the server sockets
            tcpCliSock.close()
            '''
            Fill in start.
            '''

            '''
            Fill in end.
            '''










