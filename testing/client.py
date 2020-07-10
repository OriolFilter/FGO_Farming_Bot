import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

import socket               # Import socket module
import time

from past.builtins import raw_input

def sendScreenshot(s):
    # m='Screenshot!',1,2,3
    # m='{"code": 0, "type":"image"}'
    #DIC->JSON_string
    m=json.dumps({"code": 0, "type":"image"})

    s.sendall(m.encode())
    print('Client < ',m)
    time.sleep(3)
    img=mpimg.imread('../tmp/01.jpg')
    plt.imshow (img)
    plt.show ()

    # s.sendall(m.encode())

def reciveResponse(): #StillNeedToTst
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 3125
    s.bind(('0.0.0.0', port))
    # print ('Socket binded to port 3125')
    s.listen(3)
    # print ('socket is listening')
    c, addr = s.accept()
    # print ('Got connection from ', addr)
    print ('Server: ' + c.recv(1024))
    c.close()

def startConnectionClient():
    try:
        run=True


        print('Start client')
        s = socket.socket()         # Create a socket object
        s.connect(('192.168.1.152', 12346))
        while run:
            sendScreenshot(s)
            raw_input()
    except:
        print("Connection with server was lost")
    finally:
        s.close()                     # Close the socket when done

cardSize=None
setattr(cardSize.x,'x','218')
cardSize.y= lambda :None
setattr(cardSize.y,'y','218')

# while True:
startConnectionClient()
