# Project Irisviel

# Licence
# CreativeCommons (by-nc)
# print(mainDev.get_battery_level())


# Imports
import time
# from typing import Type

import cv2
import numpy as np
from ppadb.client import Client as AdbClient
from PIL import Image
import io


class BotClient():
    def __init__(self,emuName=None,ip=None,hostName=None,port=5037): # 5037 Might be the default port for adbServer
        # You can check the device host 'name' in case you are using a usb
        # appName not enabled
        if hostName or port: # Server connection to adb
            self.client = AdbClient(host="127.0.0.1", port=port)
            try:
                if not port: # Server connection to client
                    self.mainDev = self.client.device(":".join([ip,str(port)])) # Wifi/Network
                elif hostName:
                    self.mainDev = self.client.device(hostName) # "USB"
                elif emuName: print('Thats not enabled!') # Change to pass, or just remove
            except ConnectionRefusedError:
                print('Connection refused or not aviable\nMake sure the server has started adb, and the client has debbug mode enabled, also check if wifi is inabled in case of using network, or the usb is plugged in correctly')

        # self
        self.debugg=False
        self.verbose=False

        # Default variables used on functions and default modes
        # Application
        self.emuName=emuName # If left empty it means None

        # Energy
        self.timesRestoredEnergy=0
        self.timesToRestoreEnergy=0 # -1 means infinite, does not use QZ
        self.useGoldApple=True
        self.useSilverApple=True
        self.useBronzeApple=True


        # Quests
        self.repeatQuest=False
        self.questsFinished=0 # Just conts the times that had to press 'Next', in certain events it might bugg since it might have multiple pages

        # Combat
        self.npOnDangerOrServant=False
        self.dangerOrServantFoundVar=False
        self.colorOverEffectiveness=False
        self.cardsPrio=[0,1,2,3] # Default, 0 Buster, 1 Arts, 2 Quick, 3 Stunned, IMPORTANT, use 3, since in case you don't and you have +3 stunned cards you will have a loop

        # Support
        self.selectSupportBool=False
        self.supportClassInt=0
        self.supportColorPalette=0 #0 means you finished the main history part 1
        self.ceList=[]
        # Misc
        self.run=True # Mayb should move it to self.main()
        self.mask=None
        self.timeV=time.time() #D
        self.addFriend=False # Add Master as a friend when aviable, fa falta configurar per en cas de que el jugador no tingui espai

    # ImageThings
    def screenshot(self,save=False,imgPath="Test.png"):

        # print("screenshot Start")
        # if self.debugg:
        #     self.time(">")
        #     bimg = self.mainDev.screencap()
        #     self.time(">>")
        #     img = self.bimageToImage(bimg)
        #     img = self.pilToOpencv(img)
        #     img = self.resizeOpenCvScreenshot(img)
        #     self.screenshotImg = img
        #     self.screenshotImg = self.resizeOpenCvScreenshot(self.pilToOpencv(self.bimageToImage(bimg)))
        #     if save:
        #         cv2.imwrite(imgPath,self.screenshotImg)
        #         print('Image Saved!')
        try:
            if self.checkActiveApp():
                # print("reciving bimg")
                if self.verbose:self.time(">")
                bimg = self.mainDev.screencap()

                # print("recived bimg")
                img = self.bimageToImage(bimg)
                img = self.pilToOpencv(img)
                img = self.resizeOpenCvScreenshot(img)
                self.screenshotImg = img
                self.screenshotImg = self.resizeOpenCvScreenshot(self.pilToOpencv(self.bimageToImage(bimg)))
                self.screenshotImgGray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
                if save:
                    cv2.imwrite(imgPath,self.screenshotImg)
                    print('Image Saved!')
                if self.verbose: self.time(">>")
                if self.checkPhoneNotBloqued():return True
                else:
                    print('Phone device is not unlocked or not horizontal position')
                    time.sleep(5)  # Wait 5 seconds
                    return False

            elif self.emuName:
                print('Taking screenshot from Windows Emulator')
            else:
                print('FGO application isn\' foreground')
                time.sleep(2) # Wait 5 seconds
                return False
        except:
            print("Failed to take the screenshot, the device might be locked or with an app that doesn't let you take screenshots")
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
        if self.debugg: print("default:{} img:{}".format(defaultSize[0],img.shape[0]))
        outputImage=(int(img.shape[0]*self.imageProportion),int(img.shape[1]*self.imageProportion))
        img = cv2.resize(img,(outputImage[1],outputImage[0]))
        # cv2.imwrite("Test2.png",img)
        return img

    # ADB related
    def click(self,xy=[0,0]):
        # print(xy)
        # Te en compte la rotació del dispositiu
        # print("Clicking at: {} {}".format(x*self.clickResolution,y*self.clickResolution))
        # print("Clicking at: {} {}".format(x,y))
        if xy == []:pass
        # print('Click x:{} y:{}'.format(xy[0],xy[1]))
        if self.verbose:print('Click x:{} y:{}'.format(xy[0],xy[1]))
        if self.debugg:print("skipping click!")
        else:self.mainDev.input_tap(int(xy[0]*self.clickResolution),int(xy[1]*self.clickResolution))

    def dragg(self,xyStart=[0,0],xyEnd=[0,0],time=200):
        # print(xy)
        # Te en compte la rotació del dispositiu     ??!!
        # print("Clicking at: {} {}".format(x*self.clickResolution,y*self.clickResolution))
        # print("Clicking at: {} {}".format(x,y))
        if xyStart == [] or xyEnd == []:pass
        # print('Click x:{} y:{}'.format(xy[0],xy[1]))
        if self.verbose:print('Swipe xS:{} yS:{}\n\txE:{} yE:{}'.format(xyStart[0],xyStart[1],xyEnd[0],xyEnd[1]))
        if self.debugg:print("Debugg")
        else:self.mainDev.input_swipe(int(xyStart[0]*self.clickResolution),int(xyStart[1]*self.clickResolution),int(xyEnd[0]*self.clickResolution),int(xyEnd[1]*self.clickResolution),time)

    def draggSupport(self, down=True,speed=400):
        if down:self.dragg([self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] - 50], [self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] / 2], time=speed)
        else:   self.dragg([self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] / 2], [self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] - 50], time=speed)


    def checkPhoneNotBloqued(self):
        if self.screenshotImg.shape[0] > self.screenshotImg.shape[1]: return False
        mask = np.copy(self.screenshotImg)
        mask[0:mask.shape[0],0:mask.shape[1]] = 255
        # self.showImage(self.screenshotImg)
        if np.equal(self.screenshotImg, mask).any(1).all():return False

        return True

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



    def clickRepeatButton(self):
        template = cv2.imread('../templates/repeatButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
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

    # Support Related

    def checkSelectSuppScreen(self):
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

    def selectRandomSupp(self):
        pass

    # def selectRandomSupp(self):pass

    def selectSupportClass(self, classN=0):
        # print(classN)
        if classN == 0:
            template = cv2.imread('../templates/supportList/supportMix.png', 0)
        elif classN == 1:
            template = cv2.imread('../templates/supportList/supportAll.png', 0)
        elif classN == 2:
            template = cv2.imread('../templates/supportList/supportSaber.png', 0)
        elif classN == 3:
            template = cv2.imread('../templates/supportList/supportArcher.png', 0)
        elif classN == 4:
            template = cv2.imread('../templates/supportList/supportLancer.png', 0)
        elif classN == 5:
            template = cv2.imread('../templates/supportList/supportRider.png', 0)
        elif classN == 6:
            template = cv2.imread('../templates/supportList/supportCaster.png', 0)
        elif classN == 7:
            template = cv2.imread('../templates/supportList/supportAssassin.png', 0)
        elif classN == 8:
            template = cv2.imread('../templates/supportList/supportBerserker.png', 0)
        elif classN == 9:
            template = cv2.imread('../templates/supportList/supportSpecial.png', 0)
        else:
            template = cv2.imread('../templates/supportList/supportMix.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        # print(max_val)
        treshhold = 0.9
        if max_val > treshhold:
            # self.click(max_loc)
            self.click([max_loc[0]+2,max_loc[1]+2])
            # print(([max_loc[0]+2,max_loc[1]+2]))
            # return True
        else:pass
            # return False

    def checkSuportBarrTopOrBottom(self,checkTop=True):

        # Check if barr is on max top or bottom
        template=None
        treshold=None
        if self.supportColorPalette == 0:
            treshhold = 0.97 # Fucking annoying treshhold
            if checkTop:template = cv2.imread('../templates/supportList/color0/supportBarrTop.png', 0)
            else:template = cv2.imread('../templates/supportList/color0/supportBarrBottom.png', 0)
        elif self.supportColorPalette == 1:
            treshhold = 0.98 # Fucking annoying treshhold
            if checkTop:
                template = cv2.imread('../templates/supportList/color1/supportBarrTop.png', 0)
                print("checktop")
            else:
                template = cv2.imread('../templates/supportList/color1/supportBarrBottom.png', 0)
                print("checkbot")
        # print(treshhold)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        # print(max_val)
        print(max_val)
        if max_val > treshhold:return True
        return False



    def selectSupport(self):
        self.selectSupportClass(classN=self.supportClassInt)
        if self.ceList == []:
            self.findCE(None)
        else:
            for ceName in self.ceList:
                draggDown=True
                selectedSupport=False
                x=0
                while not selectedSupport and draggDown:
                    if x == 5 and not self.checkSelectSuppScreen():return False
                    self.screenshot()
                    selectedSupport=self.findCE(ceName=ceName)
                    if not selectedSupport and self.checkSuportBarrTopOrBottom(False):
                        xy=self.returnBarrPos(0)
                        self.dragg(xy, [xy[0], 0], 200)
                        draggDown=False
                        # DraggToTop

                    # elif not selectedSupport and self.checkSuportBarrTopOrBottom():draggDown=True

                    if not selectedSupport:
                        self.draggSupport(draggDown)
                        time.sleep(0.05)
                        lastBarrPos=self.returnBarrPos(0)
                    x+=1
                if selectedSupport:return True


    def findCE(self,ceName=None):
        print(ceName)
        if ceName is None:
            self.click(xy=[660,250])
            return True
        else:
            template = cv2.imread('../templates/CE/{}.png'.format(ceName), 0)
            res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            treshHold = 0.85
            if max_val > treshHold:
                bestY, bestX = np.where(res >= max_val)
                self.click([bestX, bestY])
                return True
        return False



    # Friend related

    def clickDoNotSend(self):
        template = cv2.imread('../templates/doNotSend.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
        else: return False

    def friendRequest(self):
        template = cv2.imread('../templates/friendRequest.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
            return True
        else: return False


    # Combat related

    def checkRepeatQuestButton(self):
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
        if max_val > treshHold:
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
        if max_val > treshHold:
            if mode == 1:
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
        if max_valD > treshHold or max_valS > treshHold:
            if max_valD > treshHold: self.click(max_locD)
            elif max_valS> treshHold: self.click(max_locS)
            return True
        else:
            return False



    def returnBarrPos(self,type=0):
        # 0 Top, generic barr, works with energy too, energy has priority
        # 1 Bottom, Support
        # 2 Center, Support
        # 3 Top, Support

        # Else, print no barr found

        if type == 0:template = cv2.imread('../templates/barrTop.png', 0)
        # elif type == 1:template = cv2.imread('../templates/supportBottomScrollbar.png', 0)
        # elif type == 2:template = cv2.imread('../templates/barr.png', 0) # Sha de revistar
        # elif type == 3:template = cv2.imread('../templates/topScrollBar.png', 0)
        else:return False
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            return([int(bestX),int(bestY)])

    def findSpinButton(self,number=1,returnPos=True):
        # number 1=10 spins (default)
        # number 0=1/else
        if number==1: template = cv2.imread('../templates/spin10.png', 0)
        else: template = cv2.imread('../templates/spin1.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.95
        if max_val > treshHold:
            if returnPos:
                bestY, bestX = np.where(res >= max_val)
                return [bestX[0],bestY[0]]
            else: return True
        return False

    def findPrizeResetButton(self,returnPos=False):
        # number 1=10 spins (default)
        # number 0=1/else
        template = cv2.imread('../templates/prizeReset.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            if returnPos:
                bestY, bestX = np.where(res >= max_val)
                return [bestX[0]+10,bestY[0]+10]
            else:return True
        return False

    def findResetButton(self,returnPos=False):
        # number 1=10 spins (default)
        # number 0=1/else
        template = cv2.imread('../templates/resetButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            if returnPos:
                bestY, bestX = np.where(res >= max_val)
                return [bestX[0],bestY[0]]
            else:return True
        return False

    def findClosePopUpButton(self,returnPos=False):
        # number 1=10 spins (default)
        # number 0=1/else
        template = cv2.imread('../templates/closePopUp.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            if returnPos:
                bestY, bestX = np.where(res >= max_val)
                return [bestX[0],bestY[0]]
            else:return True
        return False
    # Combat
    def attack(self):
        self.cardsSelected=0
        self.cardsFound=0 # D
        self.cardsJsonStr={"NORMAL":[],
                           "NP":[]
                           }
        self.getNormalCardInfo()

        if not self.npOnDangerOrServant:pass
        elif self.dangerOrServantFound():
            self.dangerOrServantFoundVar=True

        if self.dangerOrServantFoundVar:self.getNPCardInfo()




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
                                                     "y": 180
                                                     },
                                                "used": False
                                                })
        self.cardsJsonStr['NP'].append(
                                                {"pos" :
                                                    {"x":739,
                                                     "y": 180
                                                     },
                                                "used": False
                                                })
        self.cardsJsonStr['NP'].append(
                                                {"pos" :
                                                    {"x":987,
                                                     "y": 180
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
        # self.showImage(self.mask12312111)
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

        # template.view()
        img = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY) # Passa l'imatge a GRAY
        # img = self.screenshotImg
        # input()
        # img.show()

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
                    effectiveness=self.returnCardEff(cardCoordStart,cardCoordEnd)
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

    def returnCardEff(self,coordS,coordE):
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
        chain = False
        if chain: pass
        elif self.colorOverEffectiveness:
            while self.cardsSelected<3 and backup<5:
                t=0
                while t<4 and self.cardsSelected<3:
                    e=0
                    while e<4 and self.cardsSelected<3:
                        # print(len(self.car dsJsonStr["NORMAL"]))
                        c=0
                        while c<len(self.cardsJsonStr["NORMAL"]) and self.cardsSelected<3:
                            if self.cardsJsonStr["NORMAL"][c]["type"] == self.cardsPrio[t] and self.cardsJsonStr["NORMAL"][c]["effectiveness"] == e and not self.cardsJsonStr["NORMAL"][c]["used"]:
                                self.cardsJsonStr["NORMAL"][c]["used"]=True
                                self.cardsSelected+=1
                                # print(self.cardsJsonStr["NORMAL"][c]["pos"])
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
                                # print(self.cardsJsonStr["NORMAL"][c]["pos"])
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
                self.dragg([xy[0]+10,xy[1]+10],[xy[0]+10,xy[1]+200])
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
                    print('{} time restoring energy'.format(self.timesRestoredEnergy))
                    time.sleep(4)
                    return True
                #else: #Find Close due lack of apples
        return False


    def countColors(self):pass

    # Main
    def main(self,mode=0):
        # Main let you pick some predefined modes
        if self.debugg:self.debuggMode()
        else:
            # try:
                if mode == 0:self.basicMode()
                elif mode == 1:self.combatOnly()
                elif mode == 2:self.cardPickerOnly()

                else:
                    print('Wrong mode...')
                    input()

            # except cv2.error as e:
            #     print(e)
            #     print("Screen blocked")
            #     time.sleep(2)
        print('Closing...')


    def cardPickerOnly(self):
        print('Card picker only mode selected')
        while self.run:
            if self.screenshot():
                if self.checkInCombat():self.attack()
                else:pass


    def combatOnly(self):
        print('Combat mode selected')
        while self.run:
            if self.screenshot():
                if False:pass
                elif self.checkInCombat():self.attack()
                elif self.checkAttackButton():
                    self.click(xy=[self.attackButtonLoc[0]+50,self.attackButtonLoc[1]])
                    time.sleep(1)
                else:pass

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
                elif self.selectSupportBool and self.checkSelectSuppScreen():
                    self.selectSupport()
                    time.sleep(0.5)
                elif self.clickCheckTapScreen():pass
                elif self.repeatQuest and self.checkRepeatQuestButton():
                    self.clickRepeatButton()
                    time.sleep(0.5)
                elif self.clickCheckNextutton():
                    self.questsFinished+=1
                    print('Finished quest nº {}'.format(self.questsFinished))
                elif self.friendRequest():
                    if self.addFriend:self.clickDoNotSend()
                    else:print('Not enabled')
                elif self.restoreApples():
                    if self.timesRestoredEnergy < self.timesToRestoreEnergy or self.timesToRestoreEnergy == -1:
                        if self.useBronzeApple and self.restoreApples(2): print('Restored energy using{}'.format(' a Bronze Apple'))
                        elif self.useSilverApple and self.restoreApples(1): print('Restored energy using{}'.format(' a Silver Apple'))
                        elif self.useGoldApple and self.restoreApples(0): print('Restored energy using{}'.format(' a Golden Apple'))
                    elif self.timesRestoredEnergy >= self.timesToRestoreEnergy and self.timesToRestoreEnergy > 0 :
                        print('Stopping after restoring energy {} times'.format(self.timesRestoredEnergy))
                        self.run=False
                    elif self.timesToRestoreEnergy == 0:
                        print('Stopping after running out of energy')
                        self.run=False



                #else:print('N')
                #RestoreEnergy/Stop
                #self.time(">>>")

    #Debugg
    def debuggMode(self):#Test From images
        self.screenshotImg=cv2.imread('Test.png')
        # print(self.screenshotImg)
        # self.showScreenshot()
        self.basicMode()
        # print(self.cardsJsonStr)
        # input()

    def showImage(self,img):
        cv2.namedWindow('image')
        cv2.imshow('image',img)
        cv2.waitKey(0)
    # Misc /D
    def time(self,str=">"):
        if str is None:
            self.timeV=time.time()
        else:
            print('{} {}'.format(str,time.time()-self.timeV))
            self.timeV=time.time()

    def clickSpeedTest(self):
        self.screenshot()
        self.click([100,100])
        print('Click!')
        self.click([100,100])
        print('Click!')
        self.click([100,100])
        print('Click!')












# Demo
if __name__ == '__main__':
    # #test=BotClient(port=5037,ip="IP")
    # hostname=input("Specify the device name")
    # test=BotClient(hostName=hostname)
    # #Settind custom details
    # test.timesToRestoreEnergy=0
    # # test.npOnDangerOrServant=True
    # test.selectSupportBool=True
    # test.repeatQuest=True
    # #test=BotClient(debugg=True)
    # # test.screenshot(True)
    # # test.debuggMode()
    # # test.clickSpeedTest()
    # # test.swipe([500,100],[200,200])
    # # test.screenshot()
    # # print(test.restoreApples(2))
    #
    # # Test
    #
    # # Running Main
    # test.main(mode=0)
    #
    # input() # Input
    print("you are running this from main, cya")
#restoreApples -> refillEnergy

# Fer una especie de menu per sellecionar coses, podria estar guai, i que fos per terminal, per a que sigui fancy control
# https://www.youtube.com/watch?v=zwMsmBsC1GM
