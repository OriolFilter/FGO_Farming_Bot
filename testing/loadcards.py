import json
import time
import matplotlib.pyplot as plt
import cv2
import numpy as np


class getCardsInfo():
    def __init__(self,imgVar):
        self.imgVar=self.resizeScreenshot(imgVar)

        self.color=0

    def resizeScreenshot(self,img): #Ho fa bé
        # print('> ',img.shape)
        # cv2.imshow('ok',img)
        # cv2.waitKey()
        defaultSize=(720,1280) #X,Y
        # print('> ',defaultSize)
        self.imageProportion=defaultSize[0]/img.shape[0]
        # print('> ',self.imageProportion)
        outputImage=(int(img.shape[0]*self.imageProportion),int(img.shape[1]*self.imageProportion))
        # print(outputImage)
        img = cv2.resize(img,(outputImage[1],outputImage[0]))
        # print('> ',img.shape)
        # print()
        # print(img.shape)
        # cv2.imwrite('found.jpg',self.imgVar)
        # cv2.imshow('ok',img)
        # cv2.waitKey()
        #
        # time.sleep(20)
        return img
        # self.sizeProp=
    def getNormalCardInfo(self):
        # self.detectBusterCards()
        # self.detectArtsCards()
        # self.detectQuickCards()
        # self.getCardsInfo()
        self.cardsFound=0
        jsonData={"cards" :[]
                      }
        for n in range(0,4):
            recivedJson=None
            recivedJson=self.getCardsInfo(n) #Not real json tho
            if recivedJson:
                print('>', recivedJson)
                # jsonData["cards"].append(recivedJson)
        # self.getCardsInfo(3)
        # print(jsonData)
        # jsonStr=json.dumps("{'id': 4, 'type': {'Quick'}, 'effectiveness': {0}, 'pos': [{'x': {269}, 'y': {488}}]}")
        # jsonLoad=json.loads(jsonStr)
        # for element in jsonData["cards"]:print(element)
        # for element in jsonData["cards"]:print(element[0])
        # for element in jsonData:print(element.carss)

        # https://stackoverflow.com/questions/26745519/converting-dictionary-to-json

    def getCardsInfo(self,mode=0): #Problemes amb els returns de Json
        jsonCardList=[]
        modeSrc={0: '../templates/Combat/buster.png',
               1: '../templates/Combat/arts.png',
               2: '../templates/Combat/quick.png',
               3: '../templates/Combat/stunned.png'
               }
        textMode={0: 'Buster',
               1: 'Arts',
               2: 'Quick',
               3: 'Stunned'
               }
        # 0 Buster
        # 1 Arts
        # 2 Quick
        # 3 Stunned

        templateSrc=modeSrc[mode]

        # jsonCardList=json.dumps('{"a":2}')


        img = cv2.cvtColor(self.imgVar, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(templateSrc, 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        template = cv2.imread(templateSrc,0)
        # xw, yh = template.shape[::-1] #Unused
        mask = np.zeros(self.imgVar.shape[:2], np.uint8) #Crear Mascara
        # mask[int(mask.shape[0]/2.5):mask.shape[0],0:mask.shape[1]]=255 #passar a blanc, fer servir en NP
        mask[0:int(mask.shape[0]/2.5),0:mask.shape[1]]=255
        # print(mask.shape)
        treshHold = 0.85

        aviable = np.where( res >= treshHold)
        count=0
        for pt in zip(*aviable[::-1]): #No se com funciona, haig de mirar si tira b, sino tiro del for loc i ja
            #pt = found point
            cardCoordStart=((pt[0] - 45,pt[1] - 215)) #X,Y
            cardCoordEnd=(cardCoordStart[0]+213,cardCoordStart[1]+279) #X,Y (esta aixins per opencv)
            cardCoordCenter=(int((cardCoordStart[0]+cardCoordEnd[0])/2),int((cardCoordStart[1]+cardCoordEnd[1])/2))
            # print(cardCoordStart) #D
            # print(cardCoordCenter) #D
            #np.mask[Y,X]

            if int(mask[pt[1],pt[0]]) is 0:
                # cardCoord=(pt[0] + xw,pt[1] + yh)
                # self.imgVar[cardCoordStart[1]:cardCoordEnd[1],cardCoordStart[0]:cardCoordEnd[0]]=(0,0,255) #FILL
                # cv2.rectangle(mask, cardCoordStart, cardCoordEnd, (255,255,255), -1) #DrawMask
                cv2.rectangle(mask,cardCoordStart,cardCoordEnd,(255,255,255),-1) #Thik
                # mask[cardCoordStart[1]:cardCoordEnd[1],cardCoordStart[0]:cardCoordEnd[0]]=255 #OLD
                effectiveness=self.reurnCardEff(cardCoordStart,cardCoordEnd)
                print('Card found!\nType: {cType}\nEffectiveness: {eff}\n\n'.format(cType=textMode[mode],eff=effectiveness))
                cv2.rectangle(self.imgVar,cardCoordCenter,(cardCoordCenter[0]+10,cardCoordCenter[1]+10),(255,0,0),-1) #Thik
                # cv2.rectangle(self.imgVar,cardCoordStart,cardCoordEnd,(0,0,255),2) #MarkCenter #D
                # jsonCardList["cards"][self.cardsFound]='{"type": 0}'
                # jsonCardList["cards"][self.cardsFound]='{"type": {cType}}, "effectiveness": {eff}}'.format(cType=textMode[mode],eff=effectiveness,)
                # jsonCardList["cards"][self.cardsFound]={"type": {textMode[mode]}}, "effectiveness": {effectiveness}, "pos" :[{"x":{cardCoordCenter[0]},"y": {cardCoordCenter[1]}]}

                jsonCardList.append({"id": self.cardsFound,
                                            "type": {textMode[mode]},
                                            "effectiveness": {effectiveness},
                                            "pos" :[
                                                {"x":{cardCoordCenter[0]},
                                                 "y": {cardCoordCenter[1]}
                                                 }]
                                            })
                self.cardsFound+=1
                # print(jsonCardList['cards'])
                # print(jsonCardList)
                # print('FF\n\n')
        # print('found {}'.format(count))
        # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html


        # cv2.imshow('ok',self.imgVar)
        # # # cv2.imwrite('found.jpg',self.imgVar)
        # cv2.waitKey()
        #
        # cv2.imshow('ok',mask)
        # cv2.waitKey()

        return jsonCardList

    def getNPInfo(self):pass   ;'stunned/unusable=5, or 4 and if NPcard 4==not use' #Not prio, primer utlitzar cartes normals, i despres implementar


    def reurnCardEff(self,coordS,coordE):
        cardImg=self.imgVar[coordS[1]:coordE[1],coordS[0]:coordE[0]]

        effectivenes=1

        img_gray = cv2.cvtColor(cardImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/effective.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            effectivenes = 0
        else:
            img_gray = cv2.cvtColor(cardImg, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('../templates/Combat/resist.png', 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.9
            if max_val > treshHold:
                effectivenes = 2

        # cv2.imshow('ok',cardImg)
        # cv2.waitKey()
        return effectivenes






    def getNPInfo(self):pass   ;'stunned/unusable=5, or 4 and if NPcard 4==not use'



def loadImage():
    img = cv2.imread('tmp/androidCards.jpg',cv2.COLOR_BGR2GRAY)
    # img = cv2.imread('tmp/cardsImage.jpg',cv2.COLOR_BGR2GRAY)
    # cv2.imshow('ok',img)
    # cv2.waitKey()
    return img

img=loadImage()
# plt.imshow (img)
# plt.show ()
cl=getCardsInfo(img)
cl.getNormalCardInfo()


x=[]
for element in x:print(element) #Al ser 0 no fa res



#Falta

# Cards to Json

# Retrive Json Info

# Pick Cards (not click)

# Click cards selected

# Send screenshot from client

# Recive info from server  (just doing atack, later going to add more functions)



