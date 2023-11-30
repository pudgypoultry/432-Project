from socket import *
import sys

'''
README:

In order to run: 
    Choose a port directly below this comment, use the input:
    "python ProxyServer.py [Desired IP Address]"
    Then go to a browser and type "[Desired IP Address]:port#/[website].com
    
This should work for HTTP requests, I was not able to get HTTPS to work nor was I able to get json
to work so that it had POST support. I also was very much not able to get 301 working.

While I feel I learned a lot with this, I think with more time I could have finished this. Unfortunately
I didn't have that :(

Either way, hope this works smoothly enough.

'''

port = 8001

def GetFileName(message):
    return message.split()[1].partition("/")[2]

def GetHostName(message):
    fileName = GetFileName(message)
    return fileName.replace("www.", "", 1)

def IPGetByHostName(message):
    hostName = GetHostName(message)
    return gethostbyname(hostName)

def NewSocket():
    return socket(AF_INET, SOCK_STREAM)


class Proxy:

    def __init__(self, ip, port):
        self.proxyServerSocket = NewSocket()
        self.proxyServerSocket.bind((ip, port))
        self.proxyServerSocket.listen(1)
        self.cache = []

    def AddToCache(self, fileName, message):
        self.cache.append(CachedSite(fileName, message))

    def ClearCache(self):
        self.cache.clear()

    def IsInCache(self, fileName):
        retBool = False
        for file in self.cache:
            if file.fileName == fileName:
                retBool = True
        return retBool

    def FileFromCache(self, fileName):
        for file in self.cache:
            if file.fileName == fileName:
                return file.message

    def Accept(self):
        return Client(self.proxyServerSocket)


class Client:

    def __init__(self, proxyServerSocket):
        clientSocket, self.address = proxyServerSocket.accept()
        self.clientSocket = Socket(clientSocket)


class Socket:

    def __init__(self, socketObj = None):
        if socketObj is None:
            self.socketObj = NewSocket()
        else:
            self.socketObj = socketObj

    def Connect(self, ip, port):
        self.socketObj.connect((ip, port))

    def ReceiveAsBytes(self, buffer : int):
        return self.socketObj.recv(buffer)

    def ReceiveAsStr(self, buffer : int):
        return self.ReceiveAsBytes(buffer).decode()

    def SendAsBytes(self, message : str):
        self.socketObj.send(message.encode())

class CachedSite:

    def __init__(self, fileName, message):
        self.fileName = fileName
        self.message = message


if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)


# Establish proxy server
'''
This creates a new socket in self.proxyServerSocket
It binds that socket to (ip, port), which are the two inputs to the class
It listens with an input of (1)
It then sets up an empty client socket that hasn't been called yet
    as well as an empty address and cache (list of CachedFile class objects)
'''
buffer = 4096
proxyServer = Proxy(sys.argv[1], port)

# Begin server loop
while 1:
    print("============Creating Client============")

    '''
    The Client class initializes by taking in a Proxy object, performing 
        accept() on the the proxyServer's socket
    '''
    theClient = proxyServer.Accept()
    print("Received a connection from: ", theClient.address)

    '''
    Now that we've received a connection, we need to read a message from
        the connection, Client.ReceiveAsStr() is set up to do this
    '''
    print("============Attempting to Receive Message============")
    message = theClient.clientSocket.ReceiveAsStr(buffer)

    if len(message) < 1:
        print("Failed to receive message")
        continue

    print("============Getting File Info============")
    fileName = GetFileName(message)
    print("File Name: ", fileName)

    fileExists = "false"
    fileToUse = "/" + fileName
    print("File To Use: ", fileToUse)

    hostName = GetHostName(message)
    print("Host Name: ", hostName)

    # Hey what the hell is this thing make it stop
    if hostName == "favicon.ico":
        print("!!!Found a dumb favicon make it stop!!!")
        continue
    else:
        hostIP = IPGetByHostName(message)
        print("Host IP: ", hostIP)

    try:
        print("------------Opening File------------")
        f = open(fileToUse[1:], "r")
        print("------------Reading Lines------------")
        outputDataToClean = f.readlines()
        stringVariable = "HTTP/1.0 200 OK\r\n"
        stringVariable += "Content-Type:text/html\r\n"
        print("------------Stripping Text------------")

        # I swapped outputData and outputDataToClean by accident but whatever
        outputData = []
        [outputData.append(outputDataToClean.pop(i)) for i, v in enumerate(outputDataToClean) if v in ['\n']]

        print("------------Output Data------------")
        print("------------Output Data To Clean------------")

        for i in outputDataToClean:
            stringVariable += i

        print("------------String Variable------------")
        print(stringVariable)
        fileExists = "true"
        print("=======####=====Attempting To Find Cache Hit=====####=======")

        # theClient.clientSocket.SendAsBytes("HTTP/1.0 200 OK\r\n")
        # theClient.clientSocket.SendAsBytes("Content-Type:text/html\r\n")
        theClient.clientSocket.SendAsBytes(stringVariable)

        print("THIS IS READING FROM THE CACHE SUCCESSFULLY!")
        print("THIS IS READING FROM THE CACHE SUCCESSFULLY!")
        print("THIS IS READING FROM THE CACHE SUCCESSFULLY!")
        f.close()

    except IOError:

        if fileExists == "false":
            # Create a socket on the proxyServer
            '''
            Establish a new socket
            Get the host name, then try to load the page
            '''
            print("============Creating Site's Socket============")
            socketToSite = Socket()

            try:
                # Connect to socket to port 80
                print("============Connecting Site to Port 80============")
                socketToSite.socketObj.connect((hostName, 80))

                # Store this connection in a CachedSite object
                print("============Preparing to Cache Site============")
                currentSite = CachedSite(fileName, message)

                # Prepare request string
                print("============Writing Get Request============")
                writeStr = f"GET http://{currentSite.fileName} HTTP/1.0\n\n"

                # Send the request
                print("============Sending Get Request============")
                socketToSite.SendAsBytes(writeStr)

                # Set the CachedSite message as the result of socketToSite.recv(buffer)
                print("============Storing Response into Cached Site============")
                currentSite.message = socketToSite.ReceiveAsStr(buffer)

                # Position of error should be [1] when split
                # Error Handling Zone
                # ========================================================
                if "404" in currentSite.message.split()[1]:
                    print("NOPE NOPE NOPE NOPE NOPE")
                    print("404: PAGE NOT FOUND!")
                    raise Exception
                elif "403" in currentSite.message.split()[1]:
                    print("Nuh uh uh!")
                    print("Remember that one dude from Jurassic Park?")
                    print("Read this in his voice")
                    print("403 FORBIDDEN, YOU DIDN'T SAY THE MAGIC WORD")
                    raise Exception
                elif "409" in currentSite.message.split()[1]:
                    print("Giddyup")
                    print("This site ain't big enough for the two of us")
                    print("Looks like there's a 403 CONFLICT, pardner")
                    raise Exception
                elif "402" in currentSite.message.split()[1]:
                    print("You are not rich enough to access this site")
                    print("402: Payment is required")
                    raise Exception
                elif "301" in currentSite.message.split()[1]:
                    print("I have not implemented functionality for this:")
                    print("    301 error, that would require I had 5 more hours in the day")
                # ========================================================

                print("============Creating File To Save Message============")
                creatingFile = open(f"{fileName}", "w")


                print(type(currentSite.message))
                print(type(currentSite.message))
                print(type(currentSite.message))
                print(type(currentSite.message))

                currentSite.message = currentSite.message.replace('\n\n', '\n')
                print(currentSite.message)
                creatingFile.write(currentSite.message)
                print(currentSite.message)
                creatingFile.close()

                print("============Send Response to Client============")
                theClient.clientSocket.SendAsBytes(currentSite.message)




            except Exception as e:
                print("Illegal request")
                print(e)

        else:
            theClient.clientSocket.socketObj.close()









