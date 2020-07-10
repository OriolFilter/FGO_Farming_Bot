# imports
import time
import webbrowser
import pyautogui
import pygetwindow as gw
import pyscreenshot as ImageGrab
import cv2
import numpy
import threading
from tkinter import *
from tkinter import ttk, IntVar

#NEW
import matplotlib.pyplot as plt
import base64
from PIL import Image


# Variables

class bot():
    def __init__(self,mode:int=2):
        self.version = "v1.06"
        self.appname: str = None
        self.appPos: int = [0, 0]  # x,y
        self.proportions: int = [0, 0]  # widh,height
        # self.screenshotImgPath = "tmp/Screenshot.jpg"
        self.mainMenuTemplates = ["templates/quests/chaldea", "templates/quests/S2"]
        self.menuClicks: int = [200, 200, 1253, 30, 757,
                                205]  # PreMainMenu/PrePre #close_news #LastQuest #remember doing appos+menuclicks

        self.cardPosition: int = [[140, 387],  # NP
                                  [140, 638],  # NP
                                  [140, 881],  # NP
                                  [135, 466],
                                  [387, 466],
                                  [638, 466],
                                  [904, 466],
                                  [1149, 466]]

        # npPosition: int = [140, 387, 638, 881]  # Might be temporal y,x0,x1,2

        self.revertCardOrder = None
        self.cardColorDictionary = {'B': 0, 'A': 1, 'Q': 2}
        self.close = False
        self.botIsRunning = False
        self.botFarmingMode = None
        self.questPicker = None
        self.chaldeaQuestType = None
        self.dailyQuest = [None, None]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)
        self.lastQuest = None
        self.SupportCE = None
        self.NPBehavior = None
        self.cardPrio = [None, None, None]  # 0Buster,1Arts,2Quick
        self.autoRestoreEnergy: bool = None
        self.chainCardsEnabled: bool = False
        self.timesRefilled = 0
        self.timesToRefill = None
        self.dangerOrServantFound = None
        self.NPBehavior: int = None  # 0 Don't, 1 DangerSpam, 2 Spam

        self.cardScreenshotPos: int = [[0, 0, 0, 0],  # NP
                                       [0, 0, 0, 0],  # NP
                                       [0, 0, 0, 0],  # NP
                                       [40, 350, 277, 635],
                                       [300, 350, 537, 635],
                                       [547, 350, 784, 635],
                                       [796, 350, 1033, 635],
                                       [1062, 350, 1299, 635]]  # X1,X2,Y1,Y2
        # tempvalues
        self.questPicker = 0  # questpicker = chaldea gate (0) #It's static..., looking for differents modes, in case there are some running events that can add
        self.chaldeaQuestType = 0  # 0 = DailyMissions  #It's static...
        # Now means, training mode, at almost max difficulty (lvl 40 if im not wrong)

        self.botMode=mode
        if self.botMode is 0: print('Satrint TCP')

        # Functions



    def screenshot(self):
        ("Screenshot")
        if self.botMode is 2:
            self.window_coordenades()
            # ImageGrab.grab()
            # img=ImageGrab.grab()#       #X      #Y               #x2                      #y2
            try:
                img = ImageGrab.grab(bbox=(self.appPos[0], self.appPos[1], self.appPos[0] + self.proportions[0],
                                           self.appPos[1] + self.proportions[1]))
                # Convert RGB to BGR
                # img.save('cardsImage.jpg')
                open_cv_image = numpy.array(img)
                open_cv_image = open_cv_image[:, :, ::-1].copy()
                self.screenshotImg = open_cv_image
                return True

            except:print('error doing the screenshot')
            finally:return False
        else:print('Waiting to recive a screenshot!!')

    def screenshotCard(self, cardNumber: int):
        self.window_coordenades()
        # ImageGrab.grab()
        # img=ImageGrab.grab()
        img = ImageGrab.grab(bbox=(
            self.appPos[0] + self.cardScreenshotPos[cardNumber][0],
            self.appPos[1] + self.cardScreenshotPos[cardNumber][1],
            self.appPos[0] + self.cardScreenshotPos[cardNumber][2],
            self.appPos[1] + self.cardScreenshotPos[cardNumber][3]))
        # img.save('tmp/Screenshot.jpg')
        open_cv_image = numpy.array(img)
        open_cv_image = open_cv_image[:, :, ::-1].copy() #Es pot mirar de passar a greyscale
        self.screenshotCImg = open_cv_image

    def clickScreen(self,x,y):
        pyautogui.click(x,y)

    ## Check
    def checkCombat(self, a: int = None):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/attackButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold and a == 1:  # 0 means press attack button
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        elif max_val > treshHold:
            return True
        else:
            return False

    def checkFriendRequest(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/friendRequest.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            # bestY, bestX = numpy.where(res >= max_val)
            # pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def declineFriendRequest(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/doNotSend.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.85
        if max_val > treshHold:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)

    def checkSupportCE(self, CEname, mode=None):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('templates/CE/' + CEname + 'U.png', 0)
        # template = cv2.imread('templates/CE/ChaldeaLunchtime.png',0)
        try:
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.95
            if max_val > treshHold:
                treshHold = 0.98
                if max_val > treshHold and mode == None:
                    bestY, bestX = numpy.where(res >= max_val)
                    pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
                    return True, True
                elif mode == 1:
                    bestY, bestX = numpy.where(res >= max_val)
                    pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
                else:
                    return True, False  # Found,Selected
                # if mode=1select95
                # if max_val > treshHold:
                # if mode == 1:
                #     bestY, bestX = numpy.where(res >= max_val)
                #     pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            else:
                return False, False
        except cv2.error:
            print(
                'Couldn\' find ' + CEname + ' inside our folders, download \'templates\' folder again and if the issue persists contact the owner')

    def checkScrollIsUp(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/supportTopScrollbar.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.99
        if max_val >= treshHold:
            return True
        else:
            return False

    def checkScrollIsDown(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/supportBottomScrollbar.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.99
        if max_val >= treshHold:
            return True
        else:
            return False

    def searchSupportCE(self):
        dragToBottom = True
        selectedCE = False
        foundCE = False
        time.sleep(1.5)
        self.screenshot()
        # searchforTheCE
        if self.checkActiveWindow() == True:
            foundCE, selectedCE = self.checkSupportCE(self.SupportCE)
        while dragToBottom and selectedCE == False and self.checkActiveWindow() == True:
            if self.checkActiveWindow() == True:
                self.dragBarr(70, 'selectSupport')
                self.screenshot()
                foundCE, selectedCE = self.checkSupportCE(self.SupportCE)
            if self.checkScrollIsDown() == True and selectedCE == False:
                dragToBottom = False
        while not dragToBottom and selectedCE != True and self.checkActiveWindow() == True:
            if self.checkActiveWindow():
                self.dragBarr(-70, 'selectSupport')
                self.screenshot()
                foundCE, selectedCE = self.checkSupportCE(self.SupportCE)
            if self.checkScrollIsUp() and selectedCE == False: dragToBottom = True
        # SelectCE
        # if foundCE == True and selectedCE == False and checkActiveWindow() == True:
        while dragToBottom and selectedCE != True and self.checkActiveWindow() == True and foundCE:
            if self.checkActiveWindow() == True:
                self.screenshot()
                foundCE, selectedCE = self.checkSupportCE(self.SupportCE)

            if self.checkScrollIsDown() and selectedCE == False:
                foundCE, selectedCE = self.checkSupportCE(self.SupportCE)
                dragToBottom = False
        while dragToBottom != True and selectedCE != True and self.checkActiveWindow() == True and foundCE:
            if self.checkActiveWindow() == True:
                self.screenshot()
                foundCE, selectedCE = self.checkSupportCE(self.SupportCE)
                if self.checkActiveWindow() == True and selectedCE == False:  self.dragBarr(-70, 'selectSupport')
        while foundCE == False:
            pyautogui.click(self.appPos[0] + 137, self.appPos[1] + 270)  # SelectFirstSupport
            foundCE = True
        time.sleep(0.3)

    def preCheckMainMenu(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/start.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            pyautogui.click(self.appPos[0] + self.menuClicks[0], self.appPos[1] + self.menuClicks[1])
            return True
        else:
            return False

    def checkLastQuest(self, file):
        if file != None:
            img_rgb = self.screenshotImg
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(file, 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val > 0.8:
                pyautogui.click(self.appPos[0] + self.menuClicks[0], self.appPos[1] + self.menuClicks[1])
                return True
            else:
                return False
        else:
            return False

    def tap(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/tap.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.7:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def checkNewsMenu(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/X_news.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            pyautogui.click(self.appPos[0] + self.menuClicks[2], self.appPos[1] + self.menuClicks[3])
            return True
        else:
            return False

    def checkMainMenu(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/newsButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            return True
        else:
            return False

    def checkChaldeaGate(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/quests/chaldea.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            bestY, bestX = numpy.where(res >= max_val)
            return [bestX, bestY, True]
        else:
            return [0, 0, False]

    def checkStartQuest(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/startQuest.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def checkDailyQuests(self):
        self.screenshot()
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/quests/chaldea/dailyQuests.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            time.sleep(0.4)
            return True
        else:
            return False

    def SelectDailyQuest(self, type: int, diff: int):  # Difficulty
        global lastQuest
        self.screenshot()
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        if type == 0:
            if diff == 0:
                quest = 'templates/quests/chaldea/free/ember_0.png'
            elif diff == 1:
                quest = 'templates/quests/chaldea/free/ember_1.png'
            elif diff == 2:
                quest = 'templates/quests/chaldea/free/ember_2.png'
            else:
                quest = 'templates/quests/chaldea/free/ember_3.png'
        elif type == 1:
            if diff == 0:
                quest = 'templates/quests/chaldea/free/training_0.png'
            elif diff == 1:
                quest = 'templates/quests/chaldea/free/training_1.png'
            elif diff == 2:
                quest = 'templates/quests/chaldea/free/training_2.png'
            else:
                quest = 'templates/quests/chaldea/free/training_3.png'
        else:
            if diff == 0:
                quest = 'templates/quests/chaldea/free/vault_0'
            elif diff == 1:
                quest = 'templates/quests/chaldea/free/vault_1'
            elif diff == 2:
                quest = 'templates/quests/chaldea/free/vault_2'
            else:
                quest = 'templates/quests/chaldea/free/vault_3'
        template = cv2.imread(quest, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.7
        if max_val > treshHold:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            lastQuest = quest
            return True
        else:
            return False

    def checkSelectSupp(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/selectSupport.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            return True
        else:
            return False

    def checkConfirmParty(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/confirmParty.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            return True
        else:
            return False

    def checkClosePopUp(self):  # Revisar
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/closePopUp.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def findOk(self):  # Revisar
        self.screenshot()
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/okButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    # Misc
    def checkLoading(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/loading.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            return True
        else:
            return False

    def checkConnecting(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/connecting.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            return True
        else:
            return False

    def checkBackCombat(self, mode = 1):
        # 0 == return true
        # 1 == click where back is
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/combatBackButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            if mode is not 1:
                bestY, bestX = numpy.where(res >= max_val)
                pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def checkClose(self):
        # screenshot()
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/close.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def checkSelectLastQuest(self):
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/close.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            pyautogui.click(self.appPos[0] + self.menuClicks[4], self.appPos[1] + self.menuClicks[5])
            time.sleep(0.5)
            return True
        else:
            return False

    def checkNextButton(self):
        # screenshot()
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/nextButton.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def checkResumeButton(self):
        # screenshot()
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/resume.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.9:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
            return True
        else:
            return False

    def checkDangerEnemiesAndServants(self):
        self.screenshot()
        img_rgb = self.screenshotImg
        # Danger
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/danger.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.75:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX + 15, self.appPos[1] + bestY)
            return True
        # Servants
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/servant.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.95:
            bestY, bestX = numpy.where(res >= max_val)
            pyautogui.click(self.appPos[0] + bestX + 15, self.appPos[1] + bestY)
            return True
        return False

    def checkServant(self):
        pass

    def checkActiveWindow(self):
        ('check screen')
        try:
            window = (gw.getWindowsWithTitle(self.appname)[0])
            if window.isActive == True:
                return True
            else:
                return False
        except IndexError:
            return 2

    def dragBarr(self, distance: int, barrType=None):
        # FindBar
        # DragDownClick
        if barrType == None:
            barPos = self.findTopBar(0)
        elif barrType == 'energyBar':
            barPos = self.findTopBar(1)
        elif barrType == 'selectSupport':
            barPos = self.findTopBar(2)
        if barPos[2]:
            pyautogui.moveTo(self.appPos[0] + self.barPos[0], self.appPos[1] + self.barPos[1] + 10)
            pyautogui.dragRel(0, distance, 0.5, button='left')
        time.sleep(0.1)

    def findTopBar(self, barrType):
        if barrType == 0:
            file = '../templates/topScrollBar.png'
            treshHold = 0.92
        elif barrType == 1:
            file = '../templates/energy/energyScrollBar.png'
            treshHold = 0.95
        elif barrType == 2:
            file = '../templates/topFriendScrollBarr.png'
            treshHold = 0.95
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(file, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > treshHold:
            bestX, bestY = numpy.where(res >= max_val)
            return [bestY, bestX, True]
        else:
            return [0, 0, False]

    def checkCardInfo(self):
        img_rgb = self.screenshotCImg
        effectivenes = 1

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/Stunned.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.8
        if max_val > treshHold:
            return (3, 3)

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/effective.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            effectivenes = 0
        else:
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('../templates/Combat/resist.png', 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            treshHold = 0.9
            if max_val > treshHold:
                effectivenes = 2

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/buster.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            return (0, effectivenes)
        else:
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('../templates/Combat/arts.png', 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val > treshHold:
                return (1, effectivenes)
            else:
                return (2, effectivenes)

    def checkNpInfo(self):
        # IF found, max prio
        # If not found, 4 (4=not found/StunnedNP)
        # Effectivenes does not matter
        img_rgb = self.screenshotImg

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/Stunned.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.8
        if max_val > treshHold:
            return (4)

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/buster.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            return (0)

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/arts.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > treshHold:
            return (0)

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/Combat/quick.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > treshHold:
            return (0)

        return (4)

    def restoreEnergy(self):
        global close
        global timesRefilled
        img_rgb = self.screenshotImg
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('../templates/energy/restoreEnergyMenu.png', 0)  # to check that im inside of that
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        # print(max_val)
        if max_val > 0.99:
            print(self.timesToRefill, timesRefilled)
            if (timesRefilled < self.timesToRefill) or self.timesToRefill == 0:
                self.dragBarr(200, 'energyBar')
                # search bronze>silver>gold and have attleast 1!
                self.screenshot()
                restoredAP = False
                if restoredAP == False and self.autoRestoreEnergy == True:  # Bronze
                    img_rgb = self.screenshotImg
                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                    template = cv2.imread('../templates/energy/bronzeApple.png', 0)
                    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(res)
                    if max_val > 0.98:
                        bestY, bestX = numpy.where(res >= max_val)
                        pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
                        time.sleep(0.1)
                        if self.findOk() == True:
                            restoredAP = True
                            timesRefilled += 1
                if restoredAP == False and self.autoRestoreEnergy == True:  # Silver
                    img_rgb = self.screenshotImg
                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                    template = cv2.imread('../templates/energy/silverApple.png', 0)
                    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(res)
                    if max_val > 0.98:
                        bestY, bestX = numpy.where(res >= max_val)
                        pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
                        time.sleep(0.1)
                        if self.findOk() == True:
                            timesRefilled += 1
                            restoredAP = True
                if restoredAP == False and self.autoRestoreEnergy == True:  # Silver
                    img_rgb = self.screenshotImg
                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                    template = cv2.imread('../templates/energy/goldApple.png', 0)
                    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(res)
                    if max_val > 0.98:
                        bestY, bestX = numpy.where(res >= max_val)
                        pyautogui.click(self.appPos[0] + bestX, self.appPos[1] + bestY)
                        time.sleep(0.1)
                        if self.findOk() == True:
                            timesRefilled += 1
                            restoredAP = True
                if restoredAP == False:
                    print("No apples left")
                    close = True
                    return True
            else:
                print("Stopping after restoring energy", timesRefilled, "times")
                close = True
                # botMenu.Terminal('No energy left, stopping')
                return True

    ## Actions
    def selectSupport(self):
        # select_first_supp_atm
        if self.checkActiveWindow() == True:
            if self.SupportCE != None:
                self.searchSupportCE()
            else:
                pyautogui.click(self.appPos[0] + 137, self.appPos[1] + 270)  # SelectFirstSupport

    def mainMenu(self):  # questPicker,chaldeaQuestType = None,dailyType = None
        # Selecting quest
        if self.questPicker == 0:  # ChaldeaQuests
            chaledaPos = self.checkChaldeaGate()
            pyautogui.click(self.appPos[0] + chaledaPos[0], self.appPos[1] + chaledaPos[1])
            if self.chaldeaQuestType == 0:  # Daily
                selectedDailyQuests = False
                contadorLost = 0
                questSelected = False
                while contadorLost < 3 and questSelected != True:
                    if self.checkDailyQuests == True or selectedDailyQuests == True:
                        # print('Selecting daily quests')
                        selectedDailyQuests = True
                        if self.SelectDailyQuest(self.dailyQuest[0], self.dailyQuest[1]) == True:
                            questSelected = True
                        elif self.SelectDailyQuest(self.dailyQuest[0], self.dailyQuest[1]) != True:
                            contadorLost = contadorLost + 1
                            draggedDown = False
                            draggedTop = False
                            timesDragged = 0
                            while draggedDown == False and timesDragged < 5 and questSelected == False:
                                self.dragBarr(80)
                                if self.SelectDailyQuest(self.dailyQuest[0], self.dailyQuest[1]) == True:
                                    contadorLost = 3
                                    draggedDown = True
                                    draggedTop = True
                                    questSelected = True
                                else:
                                    timesDragged = timesDragged + 1
                            timesDragged = 0
                            while draggedTop == False and timesDragged < 5 and questSelected == False:
                                self.dragBarr(-80)
                                if self.SelectDailyQuest(self.dailyQuest[0], self.dailyQuest[1]) == True:
                                    contadorLost = 3
                                    draggedTop = True
                                    questSelected = True
                                else:
                                    timesDragged = timesDragged + 1
                    else:  # elseChaldea
                        contadorLost = contadorLost + 1
                        draggedDown = False
                        draggedTop = False
                        timesDragged = 0
                        while draggedDown == False and timesDragged < 3:
                            self.dragBarr(80)
                            if self.checkDailyQuests() == True:
                                draggedDown = True
                                draggedTop = True
                                selectedDailyQuests = True
                            else:
                                timesDragged = timesDragged + 1
                        timesDragged = 0
                        while draggedTop == False and timesDragged < 3:
                            self.dragBarr(-80)
                            if self.checkDailyQuests() == True:
                                draggedTop = True
                                selectedDailyQuests = True
                            else:
                                timesDragged = timesDragged + 1
            else:
                print('not implemented yet!')
        else:
            print('not implemented yet!')

    def combat(self):
        # print('Im in combat!')
        # Use spells
        self.dangerOrServantFound = self.checkDangerEnemiesAndServants()
        self.attack()

    def window_coordenades(self):
        window = (gw.getWindowsWithTitle(self.appname)[0])
        if window.isMinimized == True:
            # print('Restore!')
            window.restore()
        else:
            try:
                if window.isActive != True:
                    window.activate()
            except:  # Buscar ExceptionQueToca
                print('Somthing didn\'t let me drag NoxPlayer in front of Screen!')

        self.appPos[0] = window.left  #
        self.appPos[1] = window.top + 32  #
        self.proportions[0] = window.width
        self.proportions[1] = window.height - 32
        # print(self.appPos)
        # print(proportions)

    def attack(self):
        # print('Attacking...')
        # primer reconeixement de tipus
        # SEARCHBUSTERCARDS
        artsCards = 0
        quickCards = 0
        busterCards = 0
        chainTurn = False
        npCards = 0
        cardInfo: int = [[0, 0, 0],  # NP1
                         [0, 0, 0],  # NP2
                         [0, 0, 0],  # NP3
                         [0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]  # 4   #0B,1A,2Q, 0Effective,#1NeutracheckC,2#Resist #Alredypicked? 0False,1True
        c = 0
        if (self.NPBehavior == 1 and self.dangerOrServantFound) or self.NPBehavior == 2:
            c = +3

        time.sleep(0.3)
        while c < 7:
            self.screenshotCard(c)
            if c < 3:
                cardInfo[c][0], cardInfo[c][1] = self.checkNpInfo()
                npCards = +1
            else:
                cardInfo[c][0], cardInfo[c][1] = self.checkCardInfo()
                if self.chainCardsEnabled:
                    if cardInfo[c][0] == 0:
                        busterCards += 1
                    elif cardInfo[c][0] == 1:
                        artsCards += 1
                    elif cardInfo[c][0] == 2:
                        quickCards += 1

            c = c + 1
        # Select Cards
        if self.botMode is 2:
            # Chains
            cardsPicked: int = 0
            cardsOrder: int = [0, 0, 0]
            if (artsCards > 2) | (quickCards > 2) | (busterCards > 2):
                chainTurn = True
                if busterCards >= 3:
                    cardE: int = 0
                    while cardE < 3 and cardsPicked < 3:
                        cardN: int = 0
                        if (self.NPBehavior == 1 and self.dangerOrServantFound) or self.NPBehavior == 2: cardN = +3
                        while cardN < 7 and cardsPicked < 3:
                            if cardInfo[cardN][0] == 0 and cardInfo[cardN][1] == cardE and cardInfo[cardN][2] == 0:
                                cardsOrder[cardsPicked] = cardN
                                cardsPicked = cardsPicked + 1
                                cardInfo[cardN][2] = 1
                            cardN = cardN + 1
                        cardE = cardE + 1
                elif artsCards >= 3:
                    cardE: int = 0
                    while cardE < 3 and cardsPicked < 3:
                        cardN: int = 0
                        if (self.NPBehavior == 1 and self.dangerOrServantFound) or self.NPBehavior == 2: cardN = +3
                        while cardN < 7 and cardsPicked < 3:
                            if cardInfo[cardN][0] == 1 and cardInfo[cardN][1] == cardE and cardInfo[cardN][2] == 0:
                                cardsOrder[cardsPicked] = cardN
                                cardsPicked = cardsPicked + 1
                                cardInfo[cardN][2] = 1
                            cardN = cardN + 1
                        cardE = cardE + 1
                else:
                    cardE: int = 0
                    while cardE < 3 and cardsPicked < 3:
                        cardN: int = 0
                        if (self.NPBehavior == 1 and self.dangerOrServantFound) or self.NPBehavior == 2: cardN = +3
                        while cardN < 7 and cardsPicked < 3:
                            if cardInfo[cardN][0] == 2 and cardInfo[cardN][1] == cardE and cardInfo[cardN][2] == 0:
                                cardsOrder[cardsPicked] = cardN
                                cardsPicked = cardsPicked + 1
                                cardInfo[cardN][2] = 1
                            cardN = cardN + 1
                        cardE = cardE + 1

            # CardOrder
            cardE: int = 0
            while cardE < 4 and cardsPicked < 3 and chainTurn == False:
                cardT: int = 0
                while cardT < 4 and cardsPicked < 3:
                    cardN: int = 0
                    if (self.NPBehavior == 1 and self.dangerOrServantFound) or self.NPBehavior == 2: cardN = +3
                    while cardN < 7 and cardsPicked < 3:
                        if cardInfo[cardN][0] == self.cardPrio[cardT] and cardInfo[cardN][1] == cardE and cardInfo[cardN][
                            2] == 0:
                            cardsOrder[cardsPicked] = cardN
                            cardsPicked = cardsPicked + 1
                            cardInfo[cardN][2] = 1
                        cardN = cardN + 1
                    cardT = cardT + 1
                cardE = cardE + 1

            # NP #Depractated
            # if NPBehavior == 1 & dangerOrServantFound:
            #     ('Attacking Danger Enemies')
            #     d: int = 1
            #     while d < 4:
            #         time.sleep(0.1)
            #         pyautogui.click(self.appPos[0] + npPosition[d], self.appPos[1] + npPosition[0])
            #         d += 1
            # elif NPBehavior == 2:
            #     ('Spamming NP')
            #     d: int = 1
            #     while d < 4:
            #         time.sleep(0.1)
            #         pyautogui.click(self.appPos[0] + npPosition[d], self.appPos[1] + npPosition[0])
            #         d += 1
            # elif 0:
            #     pass

            # UseCards
            if self.revertCardOrder == True:
                c: int = 2
                while c >= 0:
                    time.sleep(0.1)
                    pyautogui.click(self.appPos[0] + self.cardPosition[cardsOrder[c]][0],
                                    self.appPos[1] + self.cardPosition[cardsOrder[c]][1])
                    c -= 1
            else:
                c: int = 0
                while c < 3:
                    time.sleep(0.1)
                    pyautogui.click(self.appPos[0] + self.cardPosition[cardsOrder[c]][0],
                                    self.appPos[1] + self.cardPosition[cardsOrder[c]][1])
                    c += 1
            time.sleep(3)
        else:
            print('Sending card info to the client')

    # MainCode

    # CheckMenu
    def farm(self):
        if self.checkActiveWindow() != 2:
            while self.close == False:
                print('bot is running')
                if self.botFarmingMode == 0:  # {
                    ('Daily Mode')
                    if self.checkActiveWindow() is True and self.botMode is 2:
                        self.screenshot()
                        if False:
                            pass
                        elif self.checkCombat(1) == True:
                            self.combat()
                        elif self.checkSelectSupp() == True:
                            self.selectSupport()
                        elif self.checkLoading() == True:
                            time.sleep(2)
                        elif self.checkConnecting() == True:
                            time.sleep(4)
                        elif self.checkConfirmParty() == True:
                            checkStartQuest()
                        elif self.checkLastQuest(lastQuest) == True:
                            pass
                        elif self.checkMainMenu() == True:
                            mainMenu()
                        elif self.SelectDailyQuest(self.dailyQuest[0], self.dailyQuest[1]) == True:
                            pass
                        elif self.restoreEnergy() == True:
                            time.sleep(5)
                        elif self.checkClose() == True:
                            pass
                        elif self.checkClosePopUp() == True:
                            pass
                        elif self.checkNextButton() == True:
                            pass
                        elif self.checkBackCombat() == True:
                            pass
                        elif self.checkFriendRequest() == True:
                            self.declineFriendRequest()
                        elif self.tap() == True:
                            pass
                        elif self.checkResumeButton() == True:
                            pass
                        elif self.checkNewsMenu() == True:
                            pass
                        elif self.preCheckMainMenu() == True:
                            pass
                        else:
                            time.sleep(2)  # print('im fucking lost')
                    else:
                        time.sleep(2)

                # }
                elif self.botFarmingMode is 1:
                    ('Repeating Last Quest Mode!')  # This will need some explanation
                    if self.checkActiveWindow() is True and self.botMode is 2:
                        self.screenshot()
                        if False:
                            pass
                        elif self.checkCombat(1) is True:
                            self.combat()
                        elif self.checkSelectSupp() is True:
                            self.selectSupport()
                        elif self.checkLoading() is True:
                            time.sleep(2)
                        elif self.checkConnecting() == True:
                            time.sleep(4)
                        elif self.checkConfirmParty() == True:
                            checkStartQuest()
                        elif self.restoreEnergy() == True:
                            time.sleep(5)
                        elif self.checkClosePopUp() == True:
                            pass
                        elif self.checkNextButton() == True:
                            pass
                        elif self.checkBackCombat(1) == True:
                            pass
                        elif self.tap() == True:
                            pass
                        elif self.checkResumeButton() == True:
                            pass
                        elif self.checkSelectLastQuest() == True:
                            pass
                        else:
                            time.sleep(2)  # print('im fucking lost')
                    else:
                        time.sleep(2)
                elif self.botFarmingMode is 2:  # If windows not in front do nothing
                    ('Battle Mode!')
                    if self.checkActiveWindow() is True and self.botMode is 2:
                        self.screenshot()
                        if False:
                            pass
                        elif self.checkCombat(1) is True:
                            self.combat()
                        elif self.checkBackCombat() is True:
                            self.combat()
                        else:
                            time.sleep(2)  # print('im fucking lost')
                    else:
                        time.sleep(2)
                elif self.botFarmingMode is 3:  # If windows not in front do nothing
                    ('Asisted mode')
                    if self.checkActiveWindow() is True and self.botMode is 2:
                        self.screenshot()
                        if False:
                            pass
                        elif self.checkBackCombat(1) == True:
                            self.combat()
                        else:
                            time.sleep(2)  # print('im fucking lost')
                    else:
                        time.sleep(2)
        else:
            ('NoxPlayer was not found...')
        self.botIsRunning = False
        return ('Bot Stopped')

    def end(self):
        self.close=True


# Menu
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kw):

        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


class botMenu(Tk):  # StoleFrametructureFromSomone, im so sorry, will try to improve and, maybe don't change the structure since it works well, but atleast to understand it and being capable to o it myself

    def stopBot(self):
        self.botProc.close = True
        # try:
        self.TerminalVar.set('Stopping bot...')
        # except:
        #     print('Stopping bot...')

    def startBot(self):
        self.botProc.timesRefilled = 0
        self.botProc.botFarmingMode = self.botFarmingModeVar.get()
        self.botProc.questPicker = self.questPickerVar.get()
        self.botProc.NPBehavior = self.npModesDictionary[self.NPModeVar.get()]
        self.botProc.SupportCE = self.CEDictionary[self.SupportCEVar.get()]
        self.botProc.appname = self.emuWinNameVar.get()
        self.botProc.timesToRefill = self.timesToRefillVar.get()
        cardPrioText = self.cardPrioVar.get()
        self.botProc.autoRestoreEnergy = self.restoreEnergyVar.get()
        self.botProc.chainCardsEnabled = self.enableChainsVar.get()
        self.botProc.revertCardOrder = self.revertCardOrderVar.get()
        self.botProc.dailyQuest = [self.dailyQuestTypeVar.get(),
                                   self.dailyQuestDiffVar.get()]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)

        # for i in range(0, 3):  #Depracatted
        #     x = ord(cardPrioText[i])
        #     if x == 66:
        #         cardPrio[i] = 0
        #     elif x == 65:
        #         cardPrio[i] = 1
        #     else:
        #         cardPrio[i] = 2

        for i in range(0, 3):
            self.botProc.cardPrio[i] = self.botProc.cardColorDictionary[cardPrioText[i]]

        self.botProc.cardPrio.append(4)

        if self.botProc.botIsRunning == False:
            self.botProc.close = False
            self.botProc.botIsRunning = True
            self.TerminalVar.set('Started bot')
            try:
                self.TerminalVar.set(self.botProc.farm())
            except RuntimeError:
                print('Exiting...')
        else:
            self.TerminalVar.set('Bot is running, updated your configuration')

    def createRadioButton(self, option, variable=None):
        text, value = option
        return Radiobutton(self.frame.interior, anchor="n", text=text, value=value,
                           command=None, variable=variable, state='normal').pack()

    def checkCorrectInput(self):
        error = False
        message = ""
        try:
            x = self.timesToRefillVar.get()
            x += 1
        except TclError:
            message += 'There was an error with the \'Times to refill\' configuration'
            error = True
        if error == True:
            self.TerminalVar.set(message)
        else:
            self.TerminalVar.set('starting bot...')
            botThread = threading.Thread(target=self.startBot)
            botThread.start()

    def selectedApp(self):
        if self.emuType.get() == 'Nox':
            self.emuType.set('NoxPlayer')

    def __init__(self, *args, **kwargs):
        self.botFarmingModes = [("Daily Quests", 0), ("Last Quest", 1), ("Auto battle only", 2),
                               ("Asisted Mode (Only pick cards)", 3)]
        self.dailyQuests = [('Ember Gathering (XP)', 0), ('Training Grounds (Items)', 1),
                            ('Treasure Vault (QP)', 2)]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)
        self.dailyQuestsDifficulty = [('Novice', 0), ('Intermediate', 1), ('Advanced', 2),
                                      ('Expert', 3)]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)
        self.cardPrios = 'BAQ', 'BQA', 'ABQ', 'AQB', 'QBA', 'QAB'
        self.CEDictionary = {'None': None,
                             'ChaldeaLunchtime': 'ChaldeaLunchtime',
                             'MonaLisa': 'MonaLisa'

                             # Event/Temp #ShikiEvent
                             # 'MysticEyesOfDistortion': 'MysticEyesOfDistortion',
                             # 'Chorus': 'Chorus',
                             # 'DecapitatingBunny2018': 'DecapitatingBunny2018',
                             # 'Sprinter': 'Sprinter',
                             # 'RepeatMagic': 'RepeatMagic',
                             # 'MatureGentelman': 'MatureGentelman',
                             # 'VividDanceOfFists': 'VividDanceOfFists',
                             # 'SummersPrecognition': 'SummersPrecognition',
                             # 'TreefoldBarrier': 'TreefoldBarrier',
                             # 'GrandPuppeteer': 'GrandPuppeteer'
                             }
        self.npModesDictionary = {"None": 0, "Only Danger Enemies & Servants": 1, "Spam": 2}
        self.CEList: list = []
        self.npModesList: list = []
        self.botProc = bot()


        root = Tk.__init__(self, *args, **kwargs)
        self.frame = VerticalScrolledFrame(root)
        self.frame.pack(fill=BOTH, side=BOTTOM, expand=YES)
        self.geometry('550x750')

        self.botFarmingModeVar = IntVar()
        self.questPickerVar = IntVar()
        self.dailyQuestTypeVar = IntVar()  # Not using, only dailyquests on chaldea atm
        self.dailyQuestDiffVar = IntVar()
        self.cardPrioVar = StringVar(value='BAQ')
        self.NPModeVar = StringVar(value='Spam')
        self.SupportCEVar = StringVar(value='None')
        self.TerminalVar = StringVar()
        self.restoreEnergyVar = BooleanVar(value=1)
        self.emuType = StringVar()
        self.emuWinNameVar = StringVar(value='NoxPlayer')
        self.timesToRefillVar = IntVar(value=0)
        self.enableChainsVar = BooleanVar(value=1)
        self.revertCardOrderVar = BooleanVar(value=1)

        for x in self.CEDictionary:
            self.CEList.append(x)

        for x in self.npModesDictionary:
            self.npModesList.append(x)

        # scrollbar = Scrollbar(menu)
        # scrollbar.pack(side=RIGHT, fill=Y)

        self.title("FGOFarmingBot " + self.botProc.version)
        Label(self.frame.interior, text='Welcome to FGOFarmingBot', anchor='center').pack()
        Label(self.frame.interior, text="Start by selection one of this options, then proceed to press 'Start' button!",
              anchor='center').pack()
        Label(self.frame.interior, text="\nChoose which mode do you want the bot runs", anchor='center').pack()
        modeButtons = [self.createRadioButton(m, self.botFarmingModeVar) for m in self.botFarmingModes]
        self.botFarmingModeVar.set(1)

        Label(self.frame.interior,
              text="\nIn case you selected 'Daily Quests' select which type and difficulty must be",
              anchor='center').pack(fill='both')
        Label(self.frame.interior, text="\nType: ", anchor='center').pack(fill='both')
        dailyQuestsButtons = [self.createRadioButton(m, self.dailyQuestTypeVar) for m in self.dailyQuests]
        Label(self.frame.interior, text="\nDifficulty: ", anchor='center').pack(fill='both')
        dailyQuestsButtons = [self.createRadioButton(m, self.dailyQuestDiffVar) for m in self.dailyQuestsDifficulty]

        Label(self.frame.interior,
              text="\nIn case you selected 'Daily Quests' or 'Last Quest'\nselect which CE must search from your friendlist:",
              anchor='center').pack(fill='both')
        self.supportCEBox = ttk.Combobox(self.frame.interior, values=self.CEList, state="readonly",
                                         textvariable=self.SupportCEVar).pack()
        Label(self.frame.interior, text="").pack()
        Checkbutton(self.frame.interior, text="Restore Energy Automatically", variable=self.restoreEnergyVar).pack()

        Label(self.frame.interior,
              text="\nHow many times do you want to get the energy refilled?\n(0 means infinite)\n",
              anchor='center').pack()
        ttk.Entry(self.frame.interior, textvariable=self.timesToRefillVar).pack()
        var1 = IntVar()

        Label(self.frame.interior, text="\nCombat System:", anchor='center').pack(fill='both')
        Label(self.frame.interior, text="Select which card prioroty order:\n", anchor='center').pack(fill='both')
        self.cardPrioBox = ttk.Combobox(self.frame.interior, values=self.cardPrios, state="readonly",
                                        textvariable=self.cardPrioVar).pack()

        Label(self.frame.interior, text="").pack()
        Checkbutton(self.frame.interior, text="Color chains priority", variable=self.enableChainsVar).pack()
        Label(self.frame.interior, text="").pack()
        Checkbutton(self.frame.interior,
                    text="Revert card order?\n(higher priority card at the end, does not apply to NP)",
                    variable=self.revertCardOrderVar).pack()
        Label(self.frame.interior, text="\nChoose the NP behavior:\n", anchor='center').pack(fill='both')
        NPBBox = ttk.Combobox(self.frame.interior, values=self.npModesList, state="readonly",
                              textvariable=self.NPModeVar, width=50).pack()

        Label(self.frame.interior, text="\nEmulator config:\n", anchor='center').pack()
        Label(self.frame.interior,
              text="Please select your emulator from this list (it will be used to give a config):\n",
              anchor='center').pack()

        self.EmulatorConfigBox = ttk.Combobox(self.frame.interior, values='Nox', textvariable=self.emuType,
                                              state="readonly")
        self.EmulatorConfigBox.set('Nox')
        self.EmulatorConfigBox.pack()

        Label(self.frame.interior,
              text="\nIntroduce the window name from your emulator:\n(you can check that from 'tasklist')\n",
              anchor='center').pack()
        self.EmulatorWinNameEntry = ttk.Entry(self.frame.interior, textvariable=self.emuWinNameVar).pack()

        Label(self.frame.interior, text="\nStatus:", anchor='center').pack()
        self.terminal = Entry(self.frame.interior, textvariable=self.TerminalVar, state='disabled').pack(fill=X)

        Label(self.frame.interior, text="\n").pack()

        # Buttons
        self.github = Label(self.frame.interior, text="github.com/OriolFilter/FGO_farming_bot", fg="blue",
                            cursor="hand2", anchor='s')
        self.github.pack(side=BOTTOM)
        self.github.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/OriolFilter/FGO_farming_bot"))
        Button(self.frame.interior, text="Stop", anchor='s', command=self.stopBot).pack(side=BOTTOM, fill=X)
        Button(self.frame.interior, text="Start/Upadte", anchor='s', command=self.checkCorrectInput).pack(side=BOTTOM,
                                                                                                          fill=X)


    # def startWindow(self):


class functionManager():
    def __init__(self,mode):
        if mode is 2:
            print('Starting stand alone mode...')
            # print('Starting server mode...')
            window = botMenu()
            window.mainloop()
            window.stopBot()
        elif mode is 1:
            #startclient?
            pass
        elif mode is 0:
            print('Starting stand alone mode...')
            botStance=bot(0)

            botStance.revertCardOrder = True
            botStance.close = False
            botStance.botIsRunning = False
            botStance.botFarmingMode = 3
            botStance.questPicker = None
            botStance.chaldeaQuestType = None
            botStance.dailyQuest = [None, None]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)
            botStance.lastQuest = None
            botStance.SupportCE = None
            botStance.NPBehavior = None
            botStance.cardPrio = [None, None, None]  # 0Buster,1Arts,2Quick
            botStance.autoRestoreEnergy: bool = None
            botStance.chainCardsEnabled: bool = False
            botStance.timesToRefill = 0
            botStance.dangerOrServantFound = False
            botStance.NPBehavior: int = 0  # 0 Don't, 1 DangerSpam, 2 Spam
            # tempvalues
            botStance.questPicker = 0  # questpicker = chaldea gate (0) #It's static..., looking for differents modes, in case there are some running events that can add
            botStance.chaldeaQuestType = 0  # 0 = DailyMissions  #It's static...
            # Now means, training mode, at almost max difficulty (lvl 40 if im not wrong)

            botStance.botMode=3

# Main
mode={"server": 0,
      "client": 1,
      "stand alone" :2}

#PreguntarModeAIniciar

selectedMode=2
manager=functionManager(selectedMode)
# window = botMenu()
# window.mainloop()




## Notes

# 1280 * 720
# Don't allow resizing screen
