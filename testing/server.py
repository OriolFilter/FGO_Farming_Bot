import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import socket               # Import socket module


def startServer(ip,port):
    s = socket.socket()         # Create a socket object
    s.bind((ip, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    print('Start server')
    c, addr = s.accept()     # Establish connection with client.
    try:
        while True:
            print ('Got connection from', addr)
            # recived = c.recv(1024)

            #Recive JSON
            recived = c.recv(10000*1024).decode()
            print('Client > '+recived)
            jsonR=json.loads(recived)
            print('Code ',jsonR['code'])

            #ReciveIMG

    except:
        c.close()                # Close the connection

while True:
    startServer('192.168.1.152',12346)

# while
