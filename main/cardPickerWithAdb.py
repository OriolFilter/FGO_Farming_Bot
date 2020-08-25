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
    def __init__(self,ip=None,port=None,debugg=False):
        if not debugg:
            if port != None:
                self.client = AdbClient(host="127.0.0.1", port=port)
            else:
                self.client = AdbClient(host="127.0.0.1", port=5037)
            if port != None:
                self.mainDev = self.client.device(":".join([ip,str(port)]))
            else:
                self.mainDev = self.client.device(ip)
            # clientId="192.168.1.78:5037"
            # print(":".join([ip,str(port)]))
            self.debugg=False

        # self
        else:self.debugg=True


        # Energy
        self.timesRestoredEnergy=0
        self.timesToRestoreEnergy=0 # -1 means infinite, does not use QZ

        # Quests
        self.repeatQuest=False
        self.selectSupport=False


        # Combat
        self.npOnDangerOrServant=False
        self.colorOverEffectiveness=False
        self.cardsPrio=[0,1,2,3] # Default, Buster, Arts, Quick, Stunned

        # Misc
        self.run=True # Mayb should move it to self.main()
        self.mask=None
        self.timeV=time.time() #D

    # ImageThings
    def screenshot(self,save=False):
        # print("screenshot Start")
        if self.debugg:return True
        elif self.checkActiveApp():
            # print("reciving bimg")
            # self.time(">")
            bimg = self.mainDev.screencap()
            self.time(">>")
            # print("recived bimg")
            img = self.bimageToImage(bimg)
            img = self.pilToOpencv(img)
            img = self.resizeOpenCvScreenshot(img)
            self.screenshotImg = img
            self.screenshotImg = self.resizeOpenCvScreenshot(self.pilToOpencv(self.bimageToImage(bimg)))
            self.screenshotImgGray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
            if save:
                cv2.imwrite("Test.png",self.screenshotImg)
            return True
        else:
            print('TIME STOPPE')
            time.sleep(5)
            return False
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
        # print('Click x:{} y:{}'.format(xy[0],xy[1]))
        if self.debugg:print('Click x:{} y:{}'.format(xy[0],xy[1]))
        else:self.mainDev.input_tap(int(xy[0]*self.clickResolution),int(xy[1]*self.clickResolution))

    def swipe(self,xyStart=[],xyEnd=[],time=200):
        # print(xy)
        # Te en compte la rotació del dispositiu
        # print("Clicking at: {} {}".format(x*self.clickResolution,y*self.clickResolution))
        # print("Clicking at: {} {}".format(x,y))
        if xyStart == [] or xyEnd == []:pass
        # print('Click x:{} y:{}'.format(xy[0],xy[1]))
        if self.debugg:print('Swipe xS:{} yS:{}\n\txE:{} yE:{}'.format(xyStart[0],xyStart[1],xyEnd[0],xyEnd[1]))
        else:self.mainDev.input_swipe(int(xyStart[0]*self.clickResolution),int(xyStart[1]*self.clickResolution),int(xyEnd[0]*self.clickResolution),int(xyEnd[1]*self.clickResolution),time)

    def checkActiveApp(self):
        try:
            appname= "com.aniplex.fategrandorder.en"
            appList = self.mainDev.get_top_activities()
            if appname in str(appList[len(appList)-1]):
                return True
            return False
        except AttributeError as e:
            return True

    # Menu related
    def selectRandomSupp(self):pass

    def clickRepeatButton(self):
        template = cv2.imread('../templates/repeatButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:  # 0 means press attack button
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
        else: return False

    def clickCheckTapScreen(self):
        template = cv2.imread('../templates/tap.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.7:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
            return True
        else: return False

    def clickCheckNextutton(self):
        # screenshot()
        template = cv2.imread('../templates/nextButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
            return True
        else:
            return
    # checkState

    def checkSelectSupp(self):
        templateA = cv2.imread('../templates/selectSupportA.png', 0)
        templateB = cv2.imread('../templates/selectSupportB.png', 0)
        resA = cv2.matchTemplate(self.screenshotImgGray, templateA, cv2.TM_CCOEFF_NORMED)
        resB = cv2.matchTemplate(self.screenshotImgGray, templateB, cv2.TM_CCOEFF_NORMED)
        _, max_valA, _, max_loc = cv2.minMaxLoc(resA)
        _, max_valB, _, max_loc = cv2.minMaxLoc(resB)
        # print(max_val)
        treshhold=0.9
        if max_valA > treshhold or max_valB > treshhold:
            return True
        else:
            return False

    def checkRepeatButton(self):
        template = cv2.imread('../templates/repeatMessage.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold: return True
        else: return False

    def checkAttackButton(self):
        template = cv2.imread('../templates/Combat/attackButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.attackButtonLoc=[bestX,bestY]
            return True
        else: return False

    def checkInCombat(self):
        template = cv2.imread('../templates/Combat/combatBackButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:  # 0 means press attack button
            return True
        else:
            return False

    def findOkMenu(self,mode=0):
        # 0 don't click
        # 1 click
        template = cv2.imread('../templates/okButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:  # 0 means press attack button
            if mode is 1:
                bestY, bestX = np.where(res >= max_val)
                self.click([bestX,bestY])
                return True
            return True
        else:
            return False

    def dangerOrServantFound(self):
        templateDanger = cv2.imread('../templates/Combat/danger.png', 0)
        templateServant = cv2.imread('../templates/Combat/servant.png', 0)
        resD = cv2.matchTemplate(self.screenshotImgGray, templateDanger, cv2.TM_CCOEFF_NORMED)
        resS = cv2.matchTemplate(self.screenshotImgGray, templateServant, cv2.TM_CCOEFF_NORMED)
        _, max_valD, _, max_locD = cv2.minMaxLoc(resD)
        _, max_valS, _, max_locS = cv2.minMaxLoc(resS)
        treshHold = 0.85
        if max_valD > treshHold or max_valS > treshHold:  # 0 means press attack button
            return True
        else:
            return False

    def returnBarrPos(self,type=0):
        # 0 Top, generic barr, works with energy too, energy has priority
        # 1 Bottom, Support
        # 2 Center, Support
        # 3 Top, Support

        # Else, print no barr found

        if type is 0:template = cv2.imread('../templates/barrTop.png', 0)
        elif type is 1:template = cv2.imread('../templates/supportBottomScrollbar.png', 0)
        elif type is 2:template = cv2.imread('../templates/barr.png', 0) # Sha de revistar
        elif type is 3:template = cv2.imread('../templates/topScrollBar.png', 0)
        else:return False
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            return([int(bestX),int(bestY)])


    # Combat
    def attack(self):
        self.cardsSelected=0
        self.cardsJsonStr={"NORMAL":[],
                           "NP":[]
                           }
        self.cardsFound=0 # D
        self.getNormalCardInfo()
        if self.dangerOrServantFound():
            self.getNPCardInfo()
        # print(' --: {}'.format(self.cardsFound))
        if self.checkActiveApp():
            # print(self.cardsJsonStr)
            self.selectAttackCards()
        else:print("NOT ACTIVE")
        time.sleep(3)

    def getNPCardInfo(self):
        self.cardsJsonStr['NP'].append(
                                                {"pos" :
                                                    {"x":514,
                                                     "y": 201
                                                     },
                                                "used": False
                                                })
        self.cardsJsonStr['NP'].append(
                                                {"pos" :
                                                    {"x":739,
                                                     "y": 210
                                                     },
                                                "used": False
                                                })
        self.cardsJsonStr['NP'].append(
                                                {"pos" :
                                                    {"x":987,
                                                     "y": 232
                                                     },
                                                "used": False
                                                })

    #     # self.detectBusterCards()
    #     # self.detectArtsCards()
    #     # self.detectQuickCards()
    #     # self.getCardsInfo()
    #     # self.cardsFound=0
    #     # self.cardsJson={}
    #     for n in range(0,4):
    #         # print('T')
    #         receivedJson=None
    #         receivedJson=self.getCardsInfo(n,mode=1) #Not real json tho
    #         if receivedJson:
    #             for line in receivedJson:
    #                 # print(recivedJson[line])
    #                 self.cardsJsonStr["NP"].append(receivedJson[line])
    #     print(self.cardsJsonStr["NP"]) # D
    #     # self.showImage(self.screenshotImg)
    #     # self.showImage(self.mask)
    #     self.mask=None
    #     # print('found {} cards'.format(self.cardsFound))
    #     # for element in self.cardsJsonStr["NORMAL"]:print(element)


    def getNormalCardInfo(self):
        # self.detectBusterCards()
        # self.detectArtsCards()
        # self.detectQuickCards()
        # self.getCardsInfo()
        # self.cardsFound=0
        # self.cardsJson={}
        for n in range(0,4):
            receivedJson=None
            receivedJson=self.getCardsInfo(n,mode=0) #Not real json tho
            if receivedJson:
                for line in receivedJson:
                    # print(line)
                    # print(recivedJson[line])
                    self.cardsJsonStr["NORMAL"].append(receivedJson[line])
        # self.showImage(self.mask)
        self.mask=None
        # print('found {} cards'.format(self.cardsFound))
        # for element in self.cardsJsonStr["NORMAL"]:print(element)

    def getCardsInfo(self,color,mode=0): #Problemes amb els returns de Json
        # 0 Normal
        # 1 N?P
        jsonCardList={}
        colorSrc={0: '../templates/Combat/buster.png',
               1: '../templates/Combat/arts.png',
               2: '../templates/Combat/quick.png',
               3: '../templates/Combat/stunned.png'
               }
        # textMode={0: 'Buster',
        #        1: 'Arts',
        #        2: 'Quick',
        #        3: 'Stunned'
        #        }
        # 0 Buster
        # 1 Arts
        # 2 Quick
        # 3 Stunned
        if mode == 1:print('searching')
        if self.mask is None:self.generateMaskFromImage(mode=mode)

        templateSrc=colorSrc[color]
        template = cv2.imread(templateSrc, 0)


        img = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY) # Passa l'imatge a GRAY

        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) # Match Template
        treshHold = 0.85

        aviable = np.where( res >= treshHold)
        for pt in zip(*aviable[::-1]): #No se com funciona, haig de mirar si tira b, sino tiro del for loc i ja
            #pt = found point
            cardCoordStart=((pt[0] - 45,pt[1] - 215)) #X,Y
            cardCoordEnd=(cardCoordStart[0]+213,cardCoordStart[1]+279) #X,Y (esta aixins per opencv)
            cardCoordCenter=(int((cardCoordStart[0]+cardCoordEnd[0])/2),int((cardCoordStart[1]+cardCoordEnd[1])/2))
            if int(self.mask[pt[1],pt[0]]) == 0:
                cv2.rectangle(self.mask,cardCoordStart,cardCoordEnd,(255,255,255),-1) #Thik
                # cv2.rectangle(self.screenshotImg,cardCoordCenter,(cardCoordCenter[0]+10,cardCoordCenter[1]+10),(255,0,0),-1) #Thik
                if mode==1:
                    jsonCardList[self.cardsFound]=(
                                                {"pos" :
                                                    {"x":cardCoordCenter[0],
                                                     "y": cardCoordCenter[1]
                                                     },
                                                "used": False
                                                })
                else:
                    effectiveness=self.reurnCardEff(cardCoordStart,cardCoordEnd)
                    jsonCardList[self.cardsFound]=(
                                                {"type": color,
                                                "effectiveness": effectiveness,
                                                "pos" :
                                                    {"x":cardCoordCenter[0],
                                                     "y": cardCoordCenter[1]
                                                     },
                                                "used": False
                                                })
                self.cardsFound+=1
        return jsonCardList

    def getCardColor(self):
        for x in range(0,4):pass

    def generateMaskFromImage(self,mode):
        self.mask = np.zeros(self.screenshotImg.shape[:2], np.uint8) #Crear Mascara

        if mode == 0:self.mask[0:int(self.mask.shape[0]/2.5),0:self.mask.shape[1]]=255 #Normal
        else:self.mask[int(self.mask.shape[0]/1.75):,0:self.mask.shape[1]]=255 #NP

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

        # NP
        if self.npOnDangerOrServant:
            c=0
            while c<len(self.cardsJsonStr["NP"]) and self.cardsSelected<3:
                if not self.cardsJsonStr["NP"][c]["used"]:
                    self.cardsJsonStr["NP"][c]["used"]=True
                    # self.cardsSelected+=1
                    print(self.cardsJsonStr["NP"][c]["pos"])
                    # print(self.cardsJsonStr["NP"][c]["pos"][0])
                    # print(self.cardsJsonStr["NP"][c]["pos"]["x"])
                    self.click(xy=[self.cardsJsonStr["NP"][c]["pos"]["x"],self.cardsJsonStr["NP"][c]["pos"]["y"]])
                c+=1

        backup=0

        if self.colorOverEffectiveness:
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
        else:
            while self.cardsSelected<3 and backup<5:
                e=0
                while e<4 and self.cardsSelected<3:
                    t=0
                    while t<4 and self.cardsSelected<3:
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
                        t+=1
                    e+=1
            backup+=1
            # print(self.cardsSelected)
            # print()
            # print('END')
        # if self.cardsSelected > 2: time.sleep(4)

    def restoreApples(self,id=None): #Wont use quartz
        #None/False Restore menu, returns true/false
        #0 Gold Apple
        #1 Silver Apple
        #2 Bronze Apple -> Not enabled, still have to do drag barr

        appleValues={ 0:1,  #100%
                      1:0.5,#50%
                      2:0.1 #10%
        }

        if id is None:
            template = cv2.imread('../templates/energy/restoreEnergyMenu.png', 0)
            res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.85
            if max_val > treshHold:return True

        elif int(id) in [0,1,2]:
            picker={0: '../templates/energy/goldApple.png',
                    1: '../templates/energy/silverApple.png',
                    2: '../templates/energy/bronzeApple.png'
                    }
            if id == 2: #Dragg
                xy = self.returnBarrPos(0)
                # self.click(xy)
                # self.swipe(xy,xy)
                self.swipe(xy,[xy[0]+2,xy[1]+200])
                time.sleep(1)
                self.screenshot()

            template = cv2.imread(picker[id], 0)
            res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.85
            print(max_val)
            if max_val > treshHold:
                bestY, bestX = np.where(res >= max_val)
                self.click([bestX,bestY])
                time.sleep(1)
                self.screenshot()
                if self.findOkMenu(1):
                    self.timesRestoredEnergy+=appleValues[id]
                    return True
                    time.sleep(4)
                #else: #Find Close due lack of apples
        return False


    def countColors(self):pass

    # Main
    def main(self,mode=0):
        # Main let you pick some predefined modes
        if self.debugg:self.debuggMode()
        else:
            try:
                if mode == 0:self.basicMode()
                elif mode == 1:self.combatOnly()
                elif mode == 2:self.cardPickerOnly()

                else:
                    print('Wrong mode...')
                    input()

            except cv2.error as e:
                print(e)
                print("Screen blocked")
                time.sleep(2)
        print('Closing...')


    def cardPickerOnly(self):
        print('Card picker only mode selected')
        while self.run:
            if self.screenshot():
                if self.checkInCombat():self.attack()
                else:print('N')


    def combatOnly(self):
        print('Combat mode selected')
        while self.run:
            if self.screenshot():
                if False:pass
                elif self.checkInCombat():self.attack()
                elif self.checkAttackButton():
                    self.click(xy=[self.attackButtonLoc[0]+50,self.attackButtonLoc[1]])
                    time.sleep(1)
                else:print('N')

    def basicMode(self):
        print('Basic mode selected')
        while self.run:
            # self.time(">>")
            if self.screenshot():
            # self.time(">>")
                # print('?')
                # cv2.imwrite('Test.png',self.screenshotImg)
                if False:pass
                elif self.checkInCombat():self.attack()
                elif self.checkAttackButton():
                    self.click(xy=[self.attackButtonLoc[0]+50,self.attackButtonLoc[1]])
                    time.sleep(1)
                elif self.selectSupport and self.checkSelectSupp():
                    self.click([675,250])
                    time.sleep(1)
                elif self.clickCheckTapScreen():pass
                elif self.repeatQuest and self.checkRepeatButton():
                    self.clickRepeatButton()
                    time.sleep(1)
                elif self.clickCheckNextutton():pass
                elif self.restoreApples() and self.timesRestoredEnergy < self.timesToRestoreEnergy or self.timesToRestoreEnergy == -1:
                    if self.restoreApples(0):pass
                    elif self.restoreApples(1):pass
                    elif self.restoreApples(2):pass
                elif self.timesRestoredEnergy >= self.timesToRestoreEnergy and self.timesToRestoreEnergy > 0 :
                    print('Stopping after restoring {}'.format(self.timesRestoredEnergy))
                    self.run=False


                else:print('N')
                #RestoreEnergy/Stop
                self.time(">>>")

    #Debugg
    def debuggMode(self):#Test From images
        self.screenshotImg=cv2.imread('Test.png')
        # print(self.screenshotImg)
        # self.showScreenshot()
        self.basicMode()
        print(self.cardsJsonStr)
        input()

    def showImage(self,img):
        cv2.namedWindow('image')
        cv2.imshow('image',img)
        cv2.waitKey(0)
    # Misc /D
    def time(self,str=">"):
        print('{} {}'.format(str,time.time()-self.timeV))
        self.timeV=time.time()

    def clickSpeedTest(self):
        test.screenshot()
        self.click([100,100])
        print('Click!')
        self.click([100,100])
        print('Click!')
        self.click([100,100])
        print('Click!')












# Demo
if __name__ == '__main__':
    #test=botClient(port=5037,ip="192.168.1.78")
    test=botClient(ip="40edac8d")
    #Settind custom details
    test.timesToRestoreEnergy=2
    # test.npOnDangerOrServant=True
    test.selectSupport=True
    test.repeatQuest=True
    #test=botClient(debugg=True)
    # test.screenshot(True)
    # test.debuggMode()
    # test.clickSpeedTest()
    # test.swipe([500,100],[200,200])
    # test.screenshot()
    # print(test.restoreApples(2))

    # Test

    # Running Main
    test.main(mode=0)


    #22:46-22:46, 3 mins per quest, 40 per missio, 140 total, 140/40=3.5, al 50% = 7, good math bro!, 3x7=21
