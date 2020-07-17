# Project Excalibur


# print(":".join(["a","b"]))

# print(mainDev.get_battery_level())


#Imports
import time

import cv2
import numpy as np
from ppadb.client import Client as AdbClient
from PIL import Image
import io


print('This is a test WITHOUT server/client')

# def click():
    # mainDev.input_tap()


class botClient():
    def __init__(self,port,ip):
        self.timeV=time.time() #D
        self.client = AdbClient(host="127.0.0.1", port=port)
        # clientId="192.168.1.78:5037"
        # print(":".join([ip,str(port)]))
        self.mainDev = self.client.device(":".join([ip,str(port)]))
        self.cardsPrio=[0,1,2,3]

    # ImageThings
    def screenshot(self):
        # print("screenshot Start")
        if self.checkActiveApp():
            # print("reciving bimg")
            self.time(">")
            bimg = self.mainDev.screencap()
            self.time(">>")
            # print("recived bimg")
            img = self.bimageToImage(bimg)
            img = self.pilToOpencv(img)
            img = self.resizeOpenCvScreenshot(img)
            self.screenshotImg = img
            self.screenshotImg = self.resizeOpenCvScreenshot(self.pilToOpencv(self.bimageToImage(bimg)))
        else:
            print('TIME STOPPE')
            time.sleep(5)
        # print("screenshot Ends")
        # Image is alredy in byte aray, don't need to do nothing

    def bimageToImage(self,bimg): # also RGBA to RGB
        # D
        png = Image.open(io.BytesIO(bimg))
        png.load() # required for png.split()

        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
        # img.show()
        # background.show()
        # background.save(img, 'JPEG', quality=80)
        return background
        # self.image.show()

    def pilToOpencv(self,img):
        # print(type(img))
        # Load image
        # img.show()
        # Image to opencv
        open_cv_image = np.array(img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        # imgReady = self.resizeOpenCvScreenshot(open_cv_image) #No pot ser

        # cv2.imwrite("Test.png",open_cv_image)
        return open_cv_image

    def resizeOpenCvScreenshot(self,img): #Ho fa bé
        defaultSize=(720,1280) #X,Y
        self.imageProportion=defaultSize[0]/img.shape[0]
        self.clickResolution=img.shape[0]/defaultSize[0]
        outputImage=(int(img.shape[0]*self.imageProportion),int(img.shape[1]*self.imageProportion))
        img = cv2.resize(img,(outputImage[1],outputImage[0]))
        # cv2.imwrite("Test2.png",img)
        return img

    # ADB related
    def click(self,xy=[]):
        # print(xy)
        # Te en compte la rotació del dispositiu
        # print("Clicking at: {} {}".format(x*self.clickResolution,y*self.clickResolution))
        # print("Clicking at: {} {}".format(x,y))
        if xy == []:pass
        else:self.mainDev.input_tap(int(xy[0]*self.clickResolution),int(xy[1]*self.clickResolution))

    def checkActiveApp(self):
        appname= "com.aniplex.fategrandorder.en"
        appList = self.mainDev.get_top_activities()
        if appname in str(appList[len(appList)-1]):
            return True
        return False

    # Menu related
    def selectRandomSupp(self):pass

    def clickRepeatButton(self):
        img_gray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/repeatButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:  # 0 means press attack button
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
        else: return False

    def clickCheckTapScreen(self):
        img_gray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/tap.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.7:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
            return True
        else: return False

    def clickCheckNextutton(self):
        # screenshot()
        img_gray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/nextButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
            return True
        else:
            return
    # checkState

    def checkSelectSupp(self):
        img_gray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/selectSupport.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        # print(max_val)
        if max_val > 0.9:
            return True
        else:
            return False

    def checkRepeatButton(self):
        img_gray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/repeatMessage.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold: return True
        else: return False

    def checkAttackButton(self):
        img_gray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/attackButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.attackButtonLoc=[bestX,bestY]
            return True
        else: return False

    def checkInCombat(self):
        img_gray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/combatBackButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:  # 0 means press attack button
            return True
        else:
            return False

    # Combat
    def attack(self):
        self.cardsSelected=0
        self.cardsJsonStr={"NORMAL":[],"NP":[]}
        self.getNormalCardInfo()
        if self.checkActiveApp():
            # print(self.cardsJsonStr)
            self.selectAttackCards()
        else:print("NOT ACTIVE")

    def getNormalCardInfo(self):
        # self.detectBusterCards()
        # self.detectArtsCards()
        # self.detectQuickCards()
        # self.getCardsInfo()
        self.cardsFound=0
        # self.cardsJson={}
        for n in range(0,4):
            receivedJson=None
            receivedJson=self.getCardsInfo(n) #Not real json tho
            if receivedJson:
                for line in receivedJson:
                    # print(line)
                    # print(recivedJson[line])
                    self.cardsJsonStr["NORMAL"].append(receivedJson[line])

        # print('found {} cards'.format(self.cardsFound))
        # for element in self.cardsJsonStr["NORMAL"]:print(element)

    def getCardsInfo(self,mode=0): #Problemes amb els returns de Json
        jsonCardList={}
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
        img = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(templateSrc, 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        # template = cv2.imread(templateSrc,0)
        # xw, yh = template.shape[::-1] #Unused
        mask = np.zeros(self.screenshotImg.shape[:2], np.uint8) #Crear Mascara
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
            if int(mask[pt[1],pt[0]]) == 0:
                cv2.rectangle(mask,cardCoordStart,cardCoordEnd,(255,255,255),-1) #Thik
                effectiveness=self.reurnCardEff(cardCoordStart,cardCoordEnd)
                # print('Card found!\nType: {cType}\nEffectiveness: {eff}\n\n'.format(cType=textMode[mode],eff=effectiveness))
                cv2.rectangle(self.screenshotImg,cardCoordCenter,(cardCoordCenter[0]+10,cardCoordCenter[1]+10),(255,0,0),-1) #Thik

                jsonCardList[self.cardsFound]=(
                                            # {"type": {textMode[mode]},
                                            {"type": mode,
                                            "effectiveness": effectiveness,
                                            "pos" :
                                                {"x":cardCoordCenter[0],
                                                 "y": cardCoordCenter[1]
                                                 },
                                            "used": False
                                            })
                self.cardsFound+=1
        return jsonCardList

    def reurnCardEff(self,coordS,coordE):
            cardImg=self.screenshotImg[coordS[1]:coordE[1],coordS[0]:coordE[0]]

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

    def selectCardsOrder(self):
        pass #Maybe?

    def selectAttackCards(self):
        # print('>' ,self.cardsJson)
        # for card in self.cardsJsonStr["NORMAL"]:
        # print(self.cardsJsonStr["NORMAL"][0])
            # print(card["type"])
            # for e in range(0,4):
            #     if card[type] is
                # print(e)
        backup=0
        while self.cardsSelected<3 and backup<5:
            t=0
            while t<4 and self.cardsSelected<3:
                e=0
                while e<4 and self.cardsSelected<3:
                    # print(len(self.cardsJsonStr["NORMAL"]))
                    c=0
                    while c<len(self.cardsJsonStr["NORMAL"]) and self.cardsSelected<3:
                        if self.cardsJsonStr["NORMAL"][c]["type"] == self.cardsPrio[t] and self.cardsJsonStr["NORMAL"][c]["effectiveness"] == e and not self.cardsJsonStr["NORMAL"][c]["used"]:
                            self.cardsJsonStr["NORMAL"][c]["used"]=True
                            self.cardsSelected+=1
                            print(self.cardsJsonStr["NORMAL"][c]["pos"])
                            # print(self.cardsJsonStr["NORMAL"][c]["pos"][0])
                            # print(self.cardsJsonStr["NORMAL"][c]["pos"]["x"])
                            self.click(xy=[self.cardsJsonStr["NORMAL"][c]["pos"]["x"],self.cardsJsonStr["NORMAL"][c]["pos"]["y"]])
                        c+=1
                    e+=1
                t+=1
            backup+=1
            # print(self.cardsSelected)
            # print()
            # print('END')
        # if self.cardsSelected > 2: time.sleep(4)

    def countColors(self):pass

    # Main
    def main(self):
        while True:
            # self.time(">>")
            self.screenshot()
            # self.time(">>")
            if False:pass
            elif self.checkInCombat():self.attack()
            elif self.checkAttackButton():
                self.click(xy=[self.attackButtonLoc[0],self.attackButtonLoc[1]])
                time.sleep(1)
            elif self.checkSelectSupp():self.click([675,250])
            elif self.checkRepeatButton():self.clickRepeatButton()
            elif self.clickCheckTapScreen():pass
            elif self.clickCheckNextutton():pass
            self.time(">>>")
    # Misc /D
    def time(self,str=">"):
        print('{} {}'.format(str,time.time()-self.timeV))
        self.timeV=time.time()

test=botClient(port=5037,ip="192.168.1.78")
test.main()
