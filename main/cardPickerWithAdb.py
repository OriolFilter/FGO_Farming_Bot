# Project Irisviel

# Licence
# CreativeCommons (by-nc)
# print(mainDev.get_battery_level())


# Imports
import time
# from typing import Type
import os
import cv2
import numpy as np
from ppadb.client import Client as AdbClient
from PIL import Image, UnidentifiedImageError
import io

# Errors
class PhoneLockedOrVertical(OSError):
    """Raised when phone is locked or is playing with the aplication on vertical mode"""
    pass
# class PhoneHorizontal(OSError):
#     """Raised when android can't take a screenshot, like unlock screen or incognito mode google"""
class CantScreenshotDevice(OSError):
    """Raised when android can't take a screenshot, like unlock screen or incognito mode google"""
    pass
class FateUsaAppNotForeground(OSError):
    """Raised when FGO USA is not foreground or isn't in horizontal mode"""
    pass


def start_adb_server():
    if os.name == 'nt': # Windows
        os.system('adb kill-server')
        os.system('adb start-server')
        return True
    else: # Supposed to be Linux...
        os.system('sudo adb kill-server')
        os.system('sudo adb start-server')
        return True
    return False #??

class BotClient:
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
            except RuntimeError as e:
                print("Raised when Python can't connect with Adb Server or cannot find the specified dispositive, when this happens it will ask if you want to start the Adb server and try again")
                if start_adb_server():
                    print('Adb server started succefully')
                    self.__init__(emuName=emuName,ip=ip,hostName=hostName,port=port)
            # except ConnectionRefusedError:
            #     print('Connection refused or not aviable\nMake sure the server has started adb, and the client has debbug mode enabled, also check if wifi is inabled in case of using network, or the usb is plugged in correctly')

        # self
        self.debugg=False
        self.verbose=False

        # Default variables used on functions and default modes
        # Application
        self.emuName=emuName # If left empty it means None

        # Energy
        self.timesRestoredEnergy=0
        self.times_to_restore_energy=0 # -1 means infinite, does not use QZ
        self.useGoldApple=True
        self.useSilverApple=True
        self.useBronzeApple=True


        # Quests
        self.repeat_quest=False
        self.questsFinished=0 # Just conts the times that had to press 'Next', in certain events it might bugg since it might have multiple pages

        # Combat
        self.np_on_danger_or_servant=False
        self.danger_or_servant_foundVar=False
        self.colorOverEffectiveness=False
        self.cardsPrio=[0,1,2,3] # Default, 0 Buster, 1 Arts, 2 Quick, 3 Stunned, IMPORTANT, use 3, since in case you don't and you have +3 stunned cards you will have a loop

        # Support
        self.select_support_bool=False
        self.support_class_int=None
        self.support_color_palette=0 #0 means you finished the main history part 1
        self.ce_list=[]
        # Misc
        self.run=True # Mayb should move it to self.main()
        self.mask=None
        self.timeV=time.time() #D
        self.addFriend=False # Add Master as a friend when aviable, fa falta configurar per en cas de que el jugador no tingui espai

    # ImageThings
    def screenshot(self,save=False,imgPath="Test.png"):

        """ """


        if self.debugg:
            self.time(">")
            bimg = self.mainDev.screencap()
            print("f")
            # print("recived bimg")
            img = self.bimage_to_image(bimg)
            img = self.pil_to_opencv(img)
            img = self.resize_open_cv_screenshot(img)
            self.screenshotImg = img
            self.screenshotImg = self.resize_open_cv_screenshot(self.pil_to_opencv(self.bimage_to_image(bimg)))
            self.screenshotImgGray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
            if save:
                cv2.imwrite(imgPath, self.screenshotImg)
                print('Image Saved!')
            self.time(">>")
        else:
            try:
                if not self.emuName and self.check_active_app():
                    # print("reciving bimg")
                    if self.verbose:self.time(">")
                    bimg = self.mainDev.screencap()
                    # print("recived bimg")
                    try:
                        img = self.bimage_to_image(bimg)
                    except UnidentifiedImageError:raise CantScreenshotDevice("Can't screenshot the device, it could be due being restricted by android itself")

                    img = self.pil_to_opencv(img)
                    img = self.resize_open_cv_screenshot(img)
                    self.screenshotImg = img
                    self.screenshotImg = self.resize_open_cv_screenshot(self.pil_to_opencv(self.bimage_to_image(bimg)))
                    if save:
                        cv2.imwrite(imgPath,self.screenshotImg)
                        print('Image Saved!')
                    self.check_phone_bloqued()

                    self.screenshotImgGray = cv2.cvtColor(self.screenshotImg, cv2.COLOR_BGR2GRAY)
                    if self.verbose: self.time(">>")
                    return True

                elif self.emuName:
                    """ Does not work..."""
                    print('Taking screenshot from Windows Emulator')
                else:raise FateUsaAppNotForeground('FGO application isn\'t foreground')
            except (PhoneLockedOrVertical, FateUsaAppNotForeground, CantScreenshotDevice) as e:
                print(e)
                time.sleep(2)
                return False

    def bimage_to_image(self,bimg): # also RGBA to RGB
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

    def pil_to_opencv(self,img):
        # print(type(img))
        # Load image
        # img.show()
        # Image to opencv
        open_cv_image = np.array(img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        # imgReady = self.resize_open_cv_screenshot(open_cv_image) #No pot ser

        # cv2.imwrite("Test.png",open_cv_image)
        return open_cv_image

    def resize_open_cv_screenshot(self,img): #Ho fa bé
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

    def dragg_support(self, down=True,speed=400):
        if down:self.dragg([self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] - 50], [self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] / 2], time=speed)
        else:   self.dragg([self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] / 2], [self.screenshotImg.shape[1] / 2, self.screenshotImg.shape[0] - 50], time=speed)


    def check_phone_bloqued(self):
        if self.screenshotImg.shape[0] > self.screenshotImg.shape[1]: raise PhoneLockedOrVertical("Phone device is locked or on vertical position")
        # mask = np.copy(self.screenshotImg) # Not needed
        # mask[0:mask.shape[0],0:mask.shape[1]] = 255
        # # self.show_image(self.screenshotImg)
        # if np.equal(self.screenshotImg, mask).any(1).all():
        #     print("White...")
        #     self.screenshot(save=True)
        #     return False

        # return True

    def check_active_app(self):
            appname= "com.aniplex.fategrandorder.en"
            appList = self.mainDev.get_top_activities()
            # for eleemeint in app1List:    # D
            #     print(eleemeint)          # D
            # print(appList[len(appList)-1])# D
            if appname in str(appList[len(appList)-1]):
                return True
            return False

    # Menu related



    def clickRepeatButton(self):
        template = cv2.imread('../templates/repeat_button.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
        else: return False



    def click_check_tap_screen(self):
        template = cv2.imread('../templates/tap.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.7:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])

    def click_check_next_button(self):
        # screenshot()
        template = cv2.imread('../templates/next_button.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
            return True
        else:
            return
    def check_bond_intensified_message(self):
        # screenshot()
        template = cv2.imread('../templates/bond_up.png', 0)
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

    def check_select_support_screen(self):
        templateA = cv2.imread('../templates/select_support_a.png', 0)
        templateB = cv2.imread('../templates/select_support_b.png', 0)
        # self.show_image(self.screenshotImg)
        # input()
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

    # def selectRandomSupp(self):pass

    def select_support_class(self, classN=None):
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
        else: return None # If None
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

    def check_suport_barr_top_or_bottom(self,checkTop=True):

        # Check if barr is on max top or bottom

        # True = Check if barr is on top
        # False = Check if barr is on bottom

        template=None
        treshold=None
        if self.support_color_palette == 0:
            treshhold = 0.97 # Fucking annoying treshhold
            if checkTop:template = cv2.imread('../templates/supportList/color0/supportBarrTop.png', 0)
            else:template = cv2.imread('../templates/supportList/color0/supportBarrBottom.png', 0)
        elif self.support_color_palette == 1:
            treshhold = 0.98 # Fucking annoying treshhold
            if checkTop:
                template = cv2.imread('../templates/supportList/color1/supportBarrTop.png', 0)
                # print("checktop")
            else:
                template = cv2.imread('../templates/supportList/color1/supportBarrBottom.png', 0)
                # print("checkbot")
        # print(treshhold)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        # print(max_val)
        # print(max_val)
        if max_val > treshhold:return True
        return False



    def select_support(self):
        selected_support=False
        while self.check_select_support_screen():
            self.select_support_class(classN=self.support_class_int)
            if self.ce_list == []:
                self.find_ce(None)
            else:
                for ceName in self.ce_list:
                    dragg_down=True
                    x=0
                    while not selected_support and x < 3 and dragg_down:
                        self.screenshot()
                        selected_support=self.find_ce(ceName=ceName)

                        if not selected_support and self.check_suport_barr_top_or_bottom(False): # Dragg barr to the top
                            xy=self.return_barr_pos(0)
                            self.dragg(xy, [xy[0], 0], 200)
                            dragg_down=False
                            # DraggToTop

                        # elif not selected_support and self.check_suport_barr_top_or_bottom():dragg_down=True

                        if not selected_support:
                            self.dragg_support(dragg_down)
                            time.sleep(0.5)
                            lastBarrPos=self.return_barr_pos(0)
                        x+=1

                    if selected_support:return True
                    elif x == 3 and not self.check_select_support_screen(): return False
            while not self.update_friend_list():pass

    def select_support2(self): # In progress to improve the previous one
        selected_support = False
        while self.check_select_support_screen():
            self.select_support_class(classN=self.support_class_int)
            if self.ce_list == []:
                self.find_ce(None)
            else:
                for ceName in self.ce_list:
                    self.check_no_friends_aviable()



            while not self.update_friend_list():pass


    def find_ce(self,ceName=None):
        # print(ceName)
        if ceName is None:
            # Maybe quite forced, still one way to select a support when you don't really care about the CE
            self.click(xy=[660,250])
            return True
        else:
            template = cv2.imread('../templates/CE/{}.png'.format(ceName), 0)
            res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            treshHold = 0.96
            print("{} : {}".format(ceName,max_val))
            if max_val > treshHold:
                bestY, bestX = np.where(res >= max_val)
                if not self.debugg: self.click([bestX, bestY])
                return True
        return False



    # Friend related

    def send_friend_request(self,bool=False):
        if bool:
            template = cv2.imread('../templates/send_friend_request.png', 0)
        else:
            template = cv2.imread('../templates/dont_send_friend_request.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX,bestY])
        else: return False

    def send_friend_request_screen(self):
        template = cv2.imread('../templates/send_friend_request_screen.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            return True
        return False

    def check_compat_open_menu(self):
        template = cv2.imread('../templates/cross_window.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX, bestY])
            return True
        return False

    def update_friend_list(self):
        # Click update_friend_list
        template = cv2.imread('../templates/update_friends_button.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.click([bestX, bestY])
            # Find Yes, else find Close, either return False and do nothing
            time.sleep(0.5)
            self.screenshot()
            template = cv2.imread('../templates/yes.png', 0)
            res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.85
            if max_val>treshHold:
                bestY, bestX = np.where(res >= max_val)
                self.click([bestX, bestY])
                return True
            template = cv2.imread('../templates/close_pop_up.png', 0)
            res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.85
            # print(treshHold)
            # print(max_val)
            if max_val>treshHold:
                bestY, bestX = np.where(res >= max_val)
                self.click([bestX, bestY])
                return True
        return False

    def check_no_friends_aviable(self):
        template = cv2.imread('../templates/unable_to_find_the_corresponding_criteria.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            return True
        else: return False

    # Combat related

    def check_repeat_quest_button(self):
        template = cv2.imread('../templates/repeat_message.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        # print(max_val)
        if max_val > treshHold: return True
        else: return False

    def check_attack_button(self):
        template = cv2.imread('../templates/Combat/attackButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            self.attackButtonLoc=[bestX,bestY]
            return True
        else: return False

    def check_in_combat(self):
        template = cv2.imread('../templates/Combat/combatBackButton.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            return True
        else:
            return False

    def find_ok_menu(self,mode=0):
        # 0 don't click
        # 1 click
        template = cv2.imread('../templates/ok_button.png', 0)
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

    def danger_or_servant_found(self):
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



    def return_barr_pos(self,type=0):
        # 0 Top, generic barr, works with energy too, energy has priority
        # 1 Bottom, Support
        # 2 Center, Support
        # 3 Top, Support

        # Else, print no barr found

        if type == 0:template = cv2.imread('../templates/barr_top.png', 0)
        # elif type == 1:template = cv2.imread('../templates/support_bottom_scrollbar.png', 0)
        # elif type == 2:template = cv2.imread('../templates/barr.png', 0) # Sha de revistar
        # elif type == 3:template = cv2.imread('../templates/top_scroll_bar.png', 0)
        else:return False
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            return([int(bestX),int(bestY)])

    def find_spin_button(self,number=1,returnPos=True):
        # number 1=10 spins (default)
        # number 0=1/else
        if number==1: template = cv2.imread('../templates/lottery/spins_button.png', 0)
        else: template = cv2.imread('../templates/lottery/spin_button.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.95
        if max_val > treshHold:
            if returnPos:
                bestY, bestX = np.where(res >= max_val)
                return [bestX[0],bestY[0]]
            else: return True
        return False

    def find_prize_reset_button(self):
        # number 1=10 spins (default)
        # number 0=1/else
        template = cv2.imread('../templates/lottery/prize_reset.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.75
        print(max_val)
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            return [bestX[0]+10,bestY[0]+10]
        return False

    def lottery_items_replenished(self):
        # number 1=10 spins (default)
        # number 0=1/else
        template = cv2.imread('../templates/lottery/items_replenished.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            return True
        return False

    def find_reset_button(self):
        # number 1=10 spins (default)
        # number 0=1/else
        template = cv2.imread('../templates/lottery/reset_button.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            return [bestX[0],bestY[0]]
        return False

    def check_no_lottery_prizes_left(self):
        # number 1=10 spins (default)
        # number 0=1/else
        template = cv2.imread('../templates/lottery/no_lottery_prizes_left.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            return True
        return False



    def find_close_pop_up_button(self): # Might not be used at all, delete?
        template = cv2.imread('../templates/close_pop_up.png', 0)
        res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = np.where(res >= max_val)
            return [bestX[0],bestY[0]]
        return False
    # Combat
    def attack(self):
        self.cardsSelected=0
        self.cardsFound=0 # D
        self.cardsJsonStr={"NORMAL":[],
                           "NP":[]
                           }
        self.get_normal_card_info()

        if not self.np_on_danger_or_servant:pass
        elif self.danger_or_servant_found():
            self.danger_or_servant_foundVar=True

        if self.danger_or_servant_foundVar:self.get_np_card_info()




        # print(' --: {}'.format(self.cardsFound))
        if self.check_active_app():
            # print(self.cardsJsonStr)
            self.select_attack_cards()
        else:print("NOT ACTIVE")
        time.sleep(3)

    def get_np_card_info(self):
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
    #     # self.get_cards_info()
    #     # self.cardsFound=0
    #     # self.cardsJson={}
    #     for n in range(0,4):
    #         # print('T')
    #         receivedJson=None
    #         receivedJson=self.get_cards_info(n,mode=1) #Not real json tho
    #         if receivedJson:
    #             for line in receivedJson:
    #                 # print(recivedJson[line])
    #                 self.cardsJsonStr["NP"].append(receivedJson[line])
    #     print(self.cardsJsonStr["NP"]) # D
    #     # self.show_image(self.screenshotImg)
    #     # self.show_image(self.mask)
    #     self.mask=None
    #     # print('found {} cards'.format(self.cardsFound))
    #     # for element in self.cardsJsonStr["NORMAL"]:print(element)


    def get_normal_card_info(self):
        # self.detectBusterCards()
        # self.detectArtsCards()
        # self.detectQuickCards()
        # self.get_cards_info()
        # self.cardsFound=0
        # self.cardsJson={}
        for n in range(0,4):
            receivedJson=None
            receivedJson=self.get_cards_info(n,mode=0) #Not real json tho
            if receivedJson:
                for line in receivedJson:
                    # print(line)
                    # print(recivedJson[line])
                    self.cardsJsonStr["NORMAL"].append(receivedJson[line])
        # self.show_image(self.mask12312111)
        self.mask=None
        # print('found {} cards'.format(self.cardsFound))
        # for element in self.cardsJsonStr["NORMAL"]:print(element)

    def get_cards_info(self,color,mode=0): #Problemes amb els returns de Json
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
        if self.mask is None:self.generate_mask_from_image(mode=mode)

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
                    effectiveness=self.return_card_eff(cardCoordStart,cardCoordEnd)
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

    def generate_mask_from_image(self,mode):
        self.mask = np.zeros(self.screenshotImg.shape[:2], np.uint8) #Crear Mascara

        if mode == 0:self.mask[0:int(self.mask.shape[0]/2.5),0:self.mask.shape[1]]=255 #Normal
        else:self.mask[int(self.mask.shape[0]/1.75):,0:self.mask.shape[1]]=255 #NP

    def return_card_eff(self,coordS,coordE):
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

    def select_cards_order(self):
        pass #Maybe?

    def select_attack_cards(self):
        # print('>' ,self.cardsJson)
        # for card in self.cardsJsonStr["NORMAL"]:
        # print(self.cardsJsonStr["NORMAL"][0])
            # print(card["type"])
            # for e in range(0,4):
            #     if card[type] is
                # print(e)

        # NP
        if self.np_on_danger_or_servant:
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

    def restore_apples(self,id=None): #Wont use quartz
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
                xy = self.return_barr_pos(0)
                # self.click(xy)
                # self.swipe(xy,xy)
                self.dragg([xy[0]+10,xy[1]+10],[xy[0]+10,xy[1]+200])
                time.sleep(1)
                self.screenshot()

            template = cv2.imread(picker[id], 0)
            res = cv2.matchTemplate(self.screenshotImgGray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.85
            # print(max_val)
            if max_val > treshHold:
                bestY, bestX = np.where(res >= max_val)
                self.click([bestX,bestY])
                time.sleep(1)
                self.screenshot()
                if self.find_ok_menu(1):
                    self.timesRestoredEnergy+=appleValues[id]
                    print('{} time restoring energy'.format(self.timesRestoredEnergy))
                    time.sleep(4)
                    return True
                #else: #Find Close due lack of apples
        return False

    # Main
    def main(self,mode=0):
        # Main let you pick some predefined modes
        if self.debugg:self.debugg_mode()
        else:
                if mode == 0:self.basic_mode()
                elif mode == 1:self.combat_only()
                elif mode == 2:self.card_picker_only()
                elif mode == 3:self.spin_mode()

                else:
                    print('Wrong mode...')
                    input()
        print('Closing...')

    def card_picker_only(self):
        print('Card picker only mode selected')
        while self.run:
            if self.screenshot():
                if self.check_in_combat():self.attack()
                else:pass

    def combat_only(self):
        print('Combat mode selected')
        while self.run:
            if self.screenshot():
                if False:pass
                elif self.check_in_combat():self.attack()
                elif self.check_attack_button():
                    self.click(xy=[self.attackButtonLoc[0]+50,self.attackButtonLoc[1]])
                    time.sleep(1)
                else:pass

    def spin_mode(self):
        print('Spin mode selected.')
        while self.run:
            if self.screenshot():
                spin_pos=self.find_spin_button(returnPos=True)
                if not spin_pos: no_prizes_left=self.check_no_lottery_prizes_left()
                if spin_pos:
                    self.click(spin_pos)
                    time.sleep(1)
                    self.click([self.screenshotImgGray.shape[0]/2,self.screenshotImgGray.shape[1]/2])
                    self.click([self.screenshotImgGray.shape[0]/2,self.screenshotImgGray.shape[1]/2])
                    self.click([self.screenshotImgGray.shape[0]/2,self.screenshotImgGray.shape[1]/2])
                    time.sleep(1)
                    # self.click(self.imageProportion)
                    # self.click(self.imageProportion)
                # elif self.check_attack_button():
                #     self.click(xy=[self.attackButtonLoc[0] + 50, self.attackButtonLoc[1]])
                #     time.sleep(1)
                else:
                    prize_reset_button_pos = None
                    if no_prizes_left:prize_reset_button_pos = self.find_prize_reset_button()
                    if prize_reset_button_pos:
                        self.click(prize_reset_button_pos)
                        time.sleep(0.2)
                        self.screenshot()
                    reset_button_pos = self.find_reset_button()
                    if reset_button_pos:
                        self.click(reset_button_pos)
                        time.sleep(0.2)
                        self.screenshot()
                    lottery_items_replenished = self.lottery_items_replenished()
                    if lottery_items_replenished:
                        self.click(self.find_close_pop_up_button())
                        time.sleep(0.2)

    def basic_mode(self):
        print('Basic mode selected')
        while self.run:
            # self.time(">>")
            if self.screenshot():
            # self.time(">>")
                # print('?')
                # cv2.imwrite('Test.png',self.screenshotImg)
                if False:pass
                elif self.check_in_combat():self.attack()
                elif self.check_attack_button():
                    self.click(xy=[self.attackButtonLoc[0]+50,self.attackButtonLoc[1]])
                    time.sleep(1)
                elif self.select_support_bool and self.check_select_support_screen():
                    self.select_support()
                    # self.select_support2()
                    time.sleep(0.5)
                elif self.click_check_tap_screen():pass
                elif self.repeat_quest and self.check_repeat_quest_button(): #Repeat Questsss
                    self.clickRepeatButton()
                    time.sleep(0.5)
                    """Misc"""
                elif self.click_check_next_button():
                    self.questsFinished+=1
                    print('Finished quest nº {}'.format(self.questsFinished))
                elif self.send_friend_request_screen():self.send_friend_request(self.addFriend)
                elif self.restore_apples():
                    if self.timesRestoredEnergy < self.times_to_restore_energy or self.times_to_restore_energy == -1:
                        if self.useBronzeApple and self.restore_apples(2): print('Restored energy using{}'.format(' a Bronze Apple'))
                        elif self.useSilverApple and self.restore_apples(1): print('Restored energy using{}'.format(' a Silver Apple'))
                        elif self.useGoldApple and self.restore_apples(0): print('Restored energy using{}'.format(' a Golden Apple'))
                    elif self.timesRestoredEnergy >= self.times_to_restore_energy and self.times_to_restore_energy > 0 :
                        print('Stopping after restoring energy {} times'.format(self.timesRestoredEnergy))
                        self.run=False
                    elif self.times_to_restore_energy == 0:
                        print('Stopping after running out of energy')
                        self.run=False
                elif self.check_bond_intensified_message(): print('A servant leveled up his bond')
                # elif self.check_compat_open_menu():pass
                # else:pass



                #else:print('N')
                #RestoreEnergy/Stop
                #self.time(">>>")

    #Debugg, thats provably usenless... might need to delete
    def debugg_mode(self):#Test From images
        self.screenshotImg=cv2.imread('Test.png')
        # print(self.screenshotImg)
        # self.showScreenshot()
        self.basic_mode()
        # print(self.cardsJsonStr)
        # input()

    def show_image(self,img):
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

# Demo, there is no demo...
if __name__ == '__main__':
    print("you are running this from main, cya")

# Fer una especie de menu per sellecionar coses, podria estar guai, i que fos per terminal, per a que sigui fancy control
# https://www.youtube.com/watch?v=zwMsmBsC1GM

