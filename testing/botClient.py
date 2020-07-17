import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

import socket               # Import socket module
import time

import numpy
from past.builtins import raw_input
from PIL import Image
import io
import base64
import pickle

class client():
    def __init__(self):
        self.socket = socket.socket()         # Create a socket object

    # def sendScreenshot(self,s):
        # m='Screenshot!',1,2,3
        # m='{"code": 0, "type":"image"}'
        #DIC->JSON_string


        # s.sendall(m.encode())
        # pass
    def startServer(self): #StillNeedToTst
        #Start server
        self.serverip='0.0.0.0'
        self.serverport=12345
        self.socket.bind((self.serverip, self.serverport))        # Bind to the port
        self.socket.listen(5)                 # Now wait for client connection.
        print('Server started')
        # print('Waiting client connection')
        # self.client, self.clientaddr = self.s.accept()     # Establish connection with client.
        # print('Connection established')

    # def reciveResponse(self):
    #     print ('Server: ' + self.client.recv(1024))
    def main(self):
        # while True:
            self.screenshot()
            self.reciveJson()
            time.sleep(10)

    def connectToServer(self,ip,port=12345):
        try:
            self.socket.connect((ip, port))
            self.connected = True
        except:
            self.connected = False

    def sendMessage(self,code):
        #1=Imatge
        jsonMessageStr={'code':code}
        jsonMessage=json.dumps(jsonMessageStr)
        n=0
        # while True:
        self.socket.sendall(jsonMessage.encode())
        self.socket.sendall(jsonMessage.encode())
        print('sended msg')
        self.reciveResponse()
        # time.sleep(1)
        # n+=1

    def screenshot(self):
        self.makeScreenshot()
        self.sendScreenshot()

    def makeScreenshot(self):
        # self.img=None
        img=Image.open('tmp/cardsImage.jpg')
        # img=Image.open('tmp/androidCards.jpg')
        # print(img.size)
        self.imgVar=self.resizeScreenshot(img)
        # print(self.imgVar.size)

        # self.imgVar=bytearray(img)
        # self.imgVar=img
        # x = io.BinaryIO()
        # io.BinaryIO()
        # open_cv_image = numpy.array(img)
        # open_cv_image = open_cv_image[:, :, ::-1].copy()
        # self.imgVar=pickle.dumps(open_cv_image)
        # self.imgVar=open_cv_image

    def resizeScreenshot(self,img): #Ho fa bé
        # print('> ',img.shape)
        # cv2.imshow('ok',img)
        # cv2.waitKey()
        # imgSize=(img.size[1],)
        defaultSize=(1280,720) #Y,X
        # print('> ',defaultSize)
        self.imageProportion=defaultSize[1]/img.size[1]
        # print('> ',self.imageProportion)
        # img.show()
        # print(img.size)
        imgRes=(int(img.size[0]*self.imageProportion),int(img.size[1]*self.imageProportion))
        img=img.resize(imgRes)
        # print(img.size)
        # img.show()
        return img

    def sendScreenshot(self):
        # # Load de la imatge, ja que ara mateix no es guarda en variable
        #Convert IMG to string
        # self.img.show()
        # print(type(self.img))
        byteIO = io.BytesIO()
        self.imgVar.save(byteIO, format='PNG')
        bImg = byteIO.getvalue()

        self.socket.sendall(bImg)


    def reciveJson(self):
        print('Waiting for Json...')
        self.jsonRecivedStr = self.socket.recv(1024).decode()
        self.jsonRecived=json.loads(self.jsonRecivedStr)
        print(self.jsonRecived)
        # print(self.jsonRecived[cards])
        for element in self.jsonRecived:print('> {e}'.format(e=element))
        for element in self.jsonRecived:print('>> {e}: {j}'.format(e=element,j=self.jsonRecived[element]))
        for x in range(len(self.jsonRecived['cards'])):print('>>> Card {e}: {j}'.format(e=x,j=self.jsonRecived['cards'][x]))  # Print Cards

    def reciveResponse(self):
        # self.dataRecived = None
        self.jsonRecived = self.socket.recv(1024).decode()
        if not self.jsonRecived:
            print('F!')
        else:
            print('Server response: {}'.format(self.jsonRecived))
        time.sleep(0.4)

    def startConnectionClient(self):
        # try:
        #     run=True
        #
        #
        #     print('Start client')
        #     self.s = socket.socket()         # Create a socket object
        #     self.s.connect(('192.168.1.152', 12346))
        #     while run:
        #         self.sendScreenshot(s)
        #         raw_input()
        # except:
            print("Connection with server was lost")
        # finally:
        #     s.close()                     # Close the socket when done


#Send Example


bot=client()
# bot.startServer()
bot.connectToServer('localhost')
# bot.connectToServer('192.168.1.152')
print('Is the client connected to the server?\n{}'.format(bot.connected))
if bot.connected:
    bot.main()


