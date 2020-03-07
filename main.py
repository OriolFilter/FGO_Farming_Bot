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

# Variables

version = "v1.04"
appname: str = None
appPos: int = [0, 0]  # x,y
proportions: int = [0, 0]  # widh,height
screenshotImg = "tmp/Screenshot.jpg"
mainMenuTemplates = ["templates/quests/chaldea", "templates/quests/S2"]
menuClicks: int = [200, 200, 1253, 30, 757,205]  # PreMainMenu/PrePre #close_news #LastQuest #remember doing appos+menuclicks
cardClickPos: int = [135, 519, 391, 519, 649, 519, 905, 519.1162, 519]  # card?1Y,2Y,3Y,4Y,5Y   (why not Y,1,2,3,4,5?)
cardScreenshotPos: int = [[40, 350, 277, 635], [300, 350, 537, 635], [547, 350, 784, 635], [796, 350, 1033, 635],[1062, 350, 1299, 635]]  # Y
cardPosition: int = [[135, 466], [387, 466], [638, 466], [904, 466], [1149, 466]]
revertCardOrder = None
npPosition: int = [140, 387, 638, 881]  # Might be temporal y,x0,x1,2
cardColorDictionary = {'B':0,'A':1,'Q':2}
close = False
botIsRunning = False
botMode = None
questPicker = None
chaldeaQuestType = None
dailyQuest = [None, None]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)
lastQuest = None
SupportCE = None
NPBehavior = None
cardPrio = [None, None, None]  # 0Buster,1Arts,2Quick
autoRestoreEnergy: bool = None
chainCardsEnabled: bool = False
timesRefilled = None
timesToRefill = None
dangerOrServantFound = None
NPBehavior: int = None  # 0 Don't, 1 DangerSpam, 2 Spam


# tempvalues
questPicker = 0  # questpicker = chaldea gate (0) #It's static..., looking for differents modes, in case there are some running events that can add
chaldeaQuestType = 0  # 0 = DailyMissions  #It's static...
# Now means, training mode, at almost max difficulty (lvl 40 if im not wrong)

# Classes


# Functions
def screenshot():
    window_coordenades()
    # ImageGrab.grab()
    # img=ImageGrab.grab()#       #X      #Y               #x2                      #y2
    try:
        img = ImageGrab.grab(bbox=(appPos[0], appPos[1], appPos[0] + proportions[0], appPos[1] + proportions[1]))
        img.save('tmp/Screenshot.jpg')
    except:
        ('error doing the screenshot')
        return False


def screenshotCard(cardNumber: int):
    window_coordenades()
    # ImageGrab.grab()
    # img=ImageGrab.grab()
    img = ImageGrab.grab(bbox=(
    appPos[0] + cardScreenshotPos[cardNumber][0], appPos[1] + cardScreenshotPos[cardNumber][1],
    appPos[0] + cardScreenshotPos[cardNumber][2], appPos[1] + cardScreenshotPos[cardNumber][3]))
    img.save('tmp/Screenshot.jpg')


## Check
def checkCombat(a: int = None):
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/Combat/attackButton.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.85
    if max_val > treshHold and a == 1:  # 0 means press attack button
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    elif max_val > treshHold:
        return True
    else:
        return False


def checkSupportCE(CEname, mode=None):
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
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
                pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
                return True,True
            elif mode == 1:
                bestY, bestX = numpy.where(res >= max_val)
                pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
            else: return True,False # Found,Selected
            # if mode=1select95
            # if max_val > treshHold:
            # if mode == 1:
            #     bestY, bestX = numpy.where(res >= max_val)
            #     pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        else:
            return False,False
    except cv2.error:
        print('Couldn\' find ' + CEname + ' inside our folders, download \'templates\' folder again and if the issue persists contact the owner')


def checkScrollIsUp():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/supportTopScrollbar.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.99
    if max_val >= treshHold:
        return True
    else:
        return False


def checkScrollIsDown():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/supportBottomScrollbar.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.99
    if max_val >= treshHold:
        return True
    else:
        return False


def searchSupportCE():
    global SupportCE
    dragToBottom = True
    selectedCE = False
    foundCE = False
    time.sleep(1.5)
    screenshot()
    # searchforTheCE
    if checkActiveWindow() == True:
        foundCE,selectedCE= checkSupportCE(SupportCE)
    while dragToBottom and selectedCE == False and checkActiveWindow() == True:
        if checkActiveWindow() == True:
            dragBarr(70, 'selectSupport')
            screenshot()
            foundCE,selectedCE= checkSupportCE(SupportCE)
        if checkScrollIsDown() == True and selectedCE == False:
            dragToBottom = False

    while not dragToBottom and selectedCE != True and checkActiveWindow() == True:
        if checkActiveWindow():
            dragBarr(-70, 'selectSupport')
            screenshot()
            foundCE,selectedCE= checkSupportCE(SupportCE)
        if checkScrollIsUp() and selectedCE == False: dragToBottom = True
    # SelectCE
    # if foundCE == True and selectedCE == False and checkActiveWindow() == True:
    while dragToBottom and selectedCE != True and checkActiveWindow() == True and foundCE:
        if checkActiveWindow() == True:
            screenshot()
            foundCE,selectedCE= checkSupportCE(SupportCE)

        if checkScrollIsDown() and selectedCE == False:
            foundCE,selectedCE= checkSupportCE(SupportCE)
            dragToBottom = False

    while dragToBottom != True and selectedCE != True and checkActiveWindow() == True and foundCE:
        if checkActiveWindow() == True:
            screenshot()
            foundCE,selectedCE= checkSupportCE(SupportCE)
            if checkActiveWindow() == True and selectedCE == False:  dragBarr(-70, 'selectSupport')
    while foundCE == False:
        pyautogui.click(appPos[0] + 137, appPos[1] + 270)  # SelectFirstSupport
        foundCE = True



def preCheckMainMenu():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/start.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        pyautogui.click(appPos[0] + menuClicks[0], appPos[1] + menuClicks[1])
        return True
    else:
        return False


def checkLastQuest(file):
    if file != None:
        img_rgb = cv2.imread('tmp/Screenshot.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(file, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8:
            pyautogui.click(appPos[0] + menuClicks[0], appPos[1] + menuClicks[1])
            return True
        else:
            return False
    else:
        return False


def tap():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/tap.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.7:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    else:
        return False


def checkNewsMenu():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/X_news.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        pyautogui.click(appPos[0] + menuClicks[2], appPos[1] + menuClicks[3])
        return True
    else:
        return False


def checkMainMenu():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/newsButton.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        return True
    else:
        return False


def checkChaldeaGate():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/quests/chaldea.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.9
    if max_val > treshHold:
        bestY, bestX = numpy.where(res >= max_val)
        return [bestX, bestY, True]
    else:
        return [0, 0, False]


def checkStartQuest():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/startQuest.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.9
    if max_val > treshHold:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    else:
        return False


def checkDailyQuests():
    screenshot()
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/quests/chaldea/dailyQuests.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.9
    if max_val > treshHold:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        time.sleep(0.4)
        return True
    else:
        return False


def SelectDailyQuest(type: int, diff: int):  # Difficulty
    global lastQuest
    screenshot()
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
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
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        lastQuest = quest
        return True
    else:
        return False


def checkSelectSupp():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/selectSupport.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        return True
    else:
        return False


def checkConfirmParty():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/confirmParty.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        return True
    else:
        return False


def checkClosePopUp():  # Revisar
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/closePopUp.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    else:
        return False


def findOk():  # Revisar
    screenshot()
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/okButton.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    else:
        return False


# Misc
def checkLoading():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/loading.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        return True
    else:
        return False


def checkConnecting():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/connecting.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        return True
    else:
        return False


def checkBackCombat():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/Combat/combatBackButton.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        bestY,bestX = numpy.where( res >= max_val)
        pyautogui.click(appPos[0]+bestX, appPos[1]+bestY)
        return True
    else:
        return False


def checkClose():
    # screenshot()
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/close.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    else:
        return False


def checkSelectLastQuest():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/close.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        pyautogui.click(appPos[0] + menuClicks[4], appPos[1] + menuClicks[5])
        time.sleep(0.5)
        return True
    else:
        return False


def checkNextButton():
    # screenshot()
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/nextButton.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    else:
        return False


def checkResumeButton():
    # screenshot()
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/resume.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
        return True
    else:
        return False


def checkDangerEnemiesAndServants():
    screenshot()
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    #Danger
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/Combat/danger.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.75:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX+15, appPos[1] + bestY)
        return True
    #Servants
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/Combat/servant.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.95:
        bestY, bestX = numpy.where(res >= max_val)
        pyautogui.click(appPos[0] + bestX+15, appPos[1] + bestY)
        return True
    return False

def checkServant():
    pass

def checkActiveWindow():
    try:
        window = (gw.getWindowsWithTitle(appname)[0])
        if window.isActive == True:
            return True
        else:
            return False
    except IndexError:
        return 2


def dragBarr(distance: int, barrType=None):
    # FindBar
    # DragDownClick
    if barrType == None:
        barPos = findTopBar(0)
    elif barrType == 'energyBar':
        barPos = findTopBar(1)
    elif barrType == 'selectSupport':
        barPos = findTopBar(2)
    if barPos[2]:
        pyautogui.moveTo(appPos[0] + barPos[0], appPos[1] + barPos[1] + 10)
        pyautogui.dragRel(0, distance, 0.5, button='left')
    time.sleep(0.1)


def findTopBar(barrType):
    if barrType == 0:
        file = 'templates/topScrollBar.png'
        treshHold = 0.92
    elif barrType == 1:
        file = 'templates/energy/energyScrollBar.png'
        treshHold = 0.95
    elif barrType == 2:
        file = 'templates/topFriendScrollBarr.png'
        treshHold = 0.95
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(file, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > treshHold:
        bestX, bestY = numpy.where(res >= max_val)
        return [bestY, bestX, True]
    else:
        return [0, 0, False]


def checkCardInfo():
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    effectivenes = 1

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/Combat/Stunned.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.8
    if max_val > treshHold:
        return(3,3)


    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/Combat/effective.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.9
    if max_val > treshHold:
        effectivenes = 0
    else:
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('templates/Combat/resist.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        treshHold = 0.9
        if max_val > treshHold:
            effectivenes = 2

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/Combat/buster.png', 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    treshHold = 0.9
    if max_val > treshHold:
        return (0, effectivenes)
    else:
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('templates/Combat/arts.png', 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > treshHold:
            return (1, effectivenes)
        else:
            return (2, effectivenes)


def restoreEnergy():
    global close
    global timesRefilled
    img_rgb = cv2.imread('tmp/Screenshot.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/energy/goldApple.png', 0)  # to check that im inside of that
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if (timesRefilled < timesToRefill) | (timesToRefill == 0):
        if max_val > 0.9:
            dragBarr(200, 'energyBar')
            # search bronze>silver>gold and have attleast 1!
            screenshot()
            restoredAP = False
            if restoredAP == False and autoRestoreEnergy == True:  # Bronze
                img_rgb = cv2.imread('tmp/Screenshot.jpg')
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                template = cv2.imread('templates/energy/bronzeApple.png', 0)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val > 0.98:
                    bestY, bestX = numpy.where(res >= max_val)
                    pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
                    time.sleep(0.1)
                    if findOk() == True:
                        restoredAP = True
                        timesRefilled += 1
            if restoredAP == False and autoRestoreEnergy == True:  # Silver
                img_rgb = cv2.imread('tmp/Screenshot.jpg')
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                template = cv2.imread('templates/energy/silverApple.png', 0)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val > 0.98:
                    bestY, bestX = numpy.where(res >= max_val)
                    pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
                    time.sleep(0.1)
                    if findOk() == True:
                        timesRefilled += 1
                        restoredAP = True
            if restoredAP == False and autoRestoreEnergy == True:  # Silver
                img_rgb = cv2.imread('tmp/Screenshot.jpg')
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                template = cv2.imread('templates/energy/goldApple.png', 0)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val > 0.98:
                    bestY, bestX = numpy.where(res >= max_val)
                    pyautogui.click(appPos[0] + bestX, appPos[1] + bestY)
                    time.sleep(0.1)
                    if findOk() == True:
                        timesRefilled += 1
                        restoredAP = True

            if restoredAP == False:
                print("Stopping after restoring energy "+timesToRefill+" times")
                close = True
                # botMenu.Terminal('No energy left, stopping')
                return True
        return False
    else:
        print("No apples left")
        close = True
        return True


## Actions
def selectSupport():
    # select_first_supp_atm
    if checkActiveWindow() == True:
        if SupportCE != None:
            searchSupportCE()
        else:
             pyautogui.click(appPos[0] + 137, appPos[1] + 270)  # SelectFirstSupport


def mainMenu():  # questPicker,chaldeaQuestType = None,dailyType = None
    # Selecting quest
    if questPicker == 0:  # ChaldeaQuests
        chaledaPos = checkChaldeaGate()
        pyautogui.click(appPos[0] + chaledaPos[0], appPos[1] + chaledaPos[1])
        if chaldeaQuestType == 0:  # Daily
            selectedDailyQuests = False
            contadorLost = 0
            questSelected = False
            while contadorLost < 3 and questSelected != True:
                if checkDailyQuests == True or selectedDailyQuests == True:
                    # print('Selecting daily quests')
                    selectedDailyQuests = True
                    if SelectDailyQuest(dailyQuest[0], dailyQuest[1]) == True:
                        questSelected = True
                    elif SelectDailyQuest(dailyQuest[0], dailyQuest[1]) != True:
                        contadorLost = contadorLost + 1
                        draggedDown = False
                        draggedTop = False
                        timesDragged = 0
                        while draggedDown == False and timesDragged < 5 and questSelected == False:
                            dragBarr(80)
                            if SelectDailyQuest(dailyQuest[0], dailyQuest[1]) == True:
                                contadorLost = 3
                                draggedDown = True
                                draggedTop = True
                                questSelected = True
                            else:
                                timesDragged = timesDragged + 1
                        timesDragged = 0
                        while draggedTop == False and timesDragged < 5 and questSelected == False:
                            dragBarr(-80)
                            if SelectDailyQuest(dailyQuest[0], dailyQuest[1]) == True:
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
                        dragBarr(80)
                        if checkDailyQuests() == True:
                            draggedDown = True
                            draggedTop = True
                            selectedDailyQuests = True
                        else:
                            timesDragged = timesDragged + 1
                    timesDragged = 0
                    while draggedTop == False and timesDragged < 3:
                        dragBarr(-80)
                        if checkDailyQuests() == True:
                            draggedTop = True
                            selectedDailyQuests = True
                        else:
                            timesDragged = timesDragged + 1
        else:
            print('not implemented yet!')
    else:
        print('not implemented yet!')


def combat():
    global dangerOrServantFound
    # print('Im in combat!')
    # Use spells
    dangerOrServantFound = checkDangerEnemiesAndServants()
    attack()




def window_coordenades():
    window = (gw.getWindowsWithTitle(appname)[0])
    if window.isMinimized == True:
        # print('Restore!')
        window.restore()
    else:
        try:
            if window.isActive != True:
                window.activate()
        except:  # Buscar ExceptionQueToca
            print('Somthing didn\'t let me put NoxPlayer in front of Screen!')
    appPos[0] = window.left  #
    appPos[1] = window.top + 32  #
    proportions[0] = window.width
    proportions[1] = window.height - 32
    # print(appPos)
    # print(proportions)


def attack():
    # print('Attacking...')
    # primer reconeixement de tipus
    # SEARCHBUSTERCARDS
    artsCards=0
    quickCards=0
    busterCards=0
    chainTurn = False
    cardInfo: int = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]  # 4   #0B,1A,2Q, 0Effective,#1NeutracheckC,2#Resist #Alredypicked? 0False,1True
    c = 0
    time.sleep(0.3)
    while c < 5:
        screenshotCard(c)
        cardInfo[c][0], cardInfo[c][1] = checkCardInfo()
        if chainCardsEnabled:
            if cardInfo[c][0] == 0: busterCards+=1
            elif cardInfo[c][0] == 1: artsCards+=1
            elif cardInfo[c][0] == 2: quickCards+=1

        c = c + 1
    #Chains
    cardsPicked: int = 0
    cardsOrder: int = [0, 0, 0]
    if (artsCards > 2) | (quickCards > 2) | (busterCards > 2):
        chainTurn=True
        if busterCards >= 3:
            cardE: int = 0
            while cardE < 3 and cardsPicked < 3:
                cardN: int = 0
                while cardN < 5 and cardsPicked < 3:
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
                while cardN < 5 and cardsPicked < 3:
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
                while cardN < 5 and cardsPicked < 3:
                    if cardInfo[cardN][0] == 2 and cardInfo[cardN][1] == cardE and cardInfo[cardN][2] == 0:
                        cardsOrder[cardsPicked] = cardN
                        cardsPicked = cardsPicked + 1
                        cardInfo[cardN][2] = 1
                    cardN = cardN + 1
                cardE = cardE + 1

    #CardOrder
    cardE: int = 0
    while cardE < 3 and cardsPicked < 3 and chainTurn == False:
        cardT: int = 0
        while cardT < 4 and cardsPicked < 3:
            cardN: int = 0
            while cardN < 5 and cardsPicked < 3:
                if cardInfo[cardN][0] == cardPrio[cardT] and cardInfo[cardN][1] == cardE and cardInfo[cardN][2] == 0:
                    cardsOrder[cardsPicked] = cardN
                    cardsPicked = cardsPicked + 1
                    cardInfo[cardN][2] = 1
                cardN = cardN + 1
            cardT = cardT + 1
        cardE = cardE + 1

    #NP
    if NPBehavior == 1 & dangerOrServantFound:
        ('Attacking Danger Enemies')
        d: int = 1
        while d < 4:
            time.sleep(0.1)
            pyautogui.click(appPos[0] + npPosition[d], appPos[1] + npPosition[0])
            d += 1
    elif NPBehavior == 2:
        ('Spamming NP')
        d: int = 1
        while d < 4:
            time.sleep(0.1)
            pyautogui.click(appPos[0] + npPosition[d], appPos[1] + npPosition[0])
            d += 1
    elif 0:
        pass

    # UseCards
    if revertCardOrder == True:
        c: int = 2
        while c >= 0:
            time.sleep(0.1)
            pyautogui.click(appPos[0] + cardPosition[cardsOrder[c]][0], appPos[1] + cardPosition[cardsOrder[c]][1])
            c -=1
    else:
        c: int = 0
        while c < 3:
            time.sleep(0.1)
            pyautogui.click(appPos[0] + cardPosition[cardsOrder[c]][0], appPos[1] + cardPosition[cardsOrder[c]][1])
            c += 1
    time.sleep(3)


# MainCode

# CheckMenu
def farm():
    global botIsRunning
    if checkActiveWindow() != 2:
        while close == False:
            print('bot is running')
            if botMode == 0:  # {
                ('Normal Mode')
                if checkActiveWindow() == True:
                    screenshot()
                    if False: pass
                    elif checkCombat(1) == True: combat()
                    elif checkSelectSupp() == True: selectSupport()
                    elif checkLoading() == True: time.sleep(2)
                    elif checkConnecting() == True: time.sleep(4)
                    elif checkConfirmParty() == True: checkStartQuest()
                    elif checkLastQuest(lastQuest) == True: pass
                    elif checkMainMenu() == True: mainMenu()
                    elif SelectDailyQuest(dailyQuest[0], dailyQuest[1]) == True: pass
                    elif restoreEnergy() == True: pass
                    elif checkClose() == True:  pass
                    elif checkClosePopUp() == True: pass
                    elif checkNextButton() == True: pass
                    elif checkBackCombat() == True: pass
                    elif tap() == True: pass
                    elif checkResumeButton() == True: pass
                    elif checkNewsMenu() == True: pass
                    elif preCheckMainMenu() == True: pass
                    else: time.sleep(2)  # print('im fucking lost')
                else: time.sleep(2)

            # }
            elif botMode == 1:
                ('Repeating Last Quest Mode!')  # This will need some explanation
                if checkActiveWindow() == True:
                    screenshot()
                    if False: pass
                    elif checkCombat(1) == True: combat()
                    elif checkSelectSupp() == True: selectSupport()
                    elif checkLoading() == True: time.sleep(2)
                    elif checkConnecting() == True: time.sleep(4)
                    elif checkConfirmParty() == True: checkStartQuest()
                    elif restoreEnergy() == True: pass
                    elif checkClosePopUp() == True: pass
                    elif checkNextButton() == True: pass
                    elif checkBackCombat() == True: pass
                    elif tap() == True: pass
                    elif checkResumeButton() == True: pass
                    elif checkSelectLastQuest() == True: pass
                    else: time.sleep(2)  # print('im fucking lost')
                else: time.sleep(2)
            elif botMode == 2:  # If windows not in front do nothing
                ('Battle Mode!')
                if checkActiveWindow() == True:
                    screenshot()
                    if False: pass
                    elif checkCombat(1) == True: combat()
                    elif checkBackCombat() == True: combat()
                    else: time.sleep(2)  # print('im fucking lost')
                else: time.sleep(2)
    else:
        ('NoxPlayer was not found...')
    botIsRunning = False
    return('Bot Stopped')


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


class botMenu(
    Tk):  # StoleFrametructureFromSomone, im so sorry, will try to improve and, maybe don't change the structure since it works well, but atleast to understand it and being capable to o it myself
    botModes = [("Daily Quests", 0), ("Last Quest", 1), ("Auto battle only", 2)]
    dailyQuests = [('Ember Gathering (XP)', 0), ('Training Grounds (Items)', 1),
                   ('Treasure Vault (QP)', 2)]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)
    dailyQuestsDifficulty = [('Novice', 0), ('Intermediate', 1), ('Advanced', 2),
                             ('Expert', 3)]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)
    cardPrios = 'BAQ', 'BQA', 'ABQ', 'AQB', 'QBA', 'QAB'
    CEDictionary = {'None': None,
                    'ChaldeaLunchtime': 'ChaldeaLunchtime',
                    'MonaLisa': 'MonaLisa'


                    #Event/Temp #ShikiEvent
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
    npModesDictionary = {"None": 0, "Only Danger Enemies & Servants": 1, "Spam": 2}
    CEList: list = []
    npModesList: list = []

    def stopBot(self):
        global close
        close = True
        self.TerminalVar.set('Stopping bot...')

    def startBot(self):
        global botIsRunning
        global botMode
        global questPicker
        global dailyQuest
        global cardPrio
        global NPBehavior
        global SupportCE
        global appname
        global autoRestoreEnergy
        global timesToRefill
        global timesRefilled
        global chainCardsEnabled
        global revertCardOrder
        global close

        timesRefilled = 0
        botMode = self.botModeVar.get()
        questPicker = self.questPickerVar.get()
        NPBehavior = self.npModesDictionary[self.NPModeVar.get()]
        SupportCE = self.CEDictionary[self.SupportCEVar.get()]
        appname = self.emuWinNameVar.get()
        timesToRefill = self.timesToRefillVar.get()
        cardPrioText = self.cardPrioVar.get()
        autoRestoreEnergy = self.restoreEnergyVar.get()
        chainCardsEnabled = self.enableChainsVar.get()
        revertCardOrder = self.revertCardOrderVar.get()
        dailyQuest = [self.dailyQuestTypeVar.get(),
                      self.dailyQuestDiffVar.get()]  # 0 = xp, 1 = training ,2 = vault / 0123 (difficulty)

        # for i in range(0, 3):  #Depracatted
        #     x = ord(cardPrioText[i])
        #     if x == 66:
        #         cardPrio[i] = 0
        #     elif x == 65:
        #         cardPrio[i] = 1
        #     else:
        #         cardPrio[i] = 2

        for i in range(0, 3): cardPrio[i]=cardColorDictionary[cardPrioText[i]]
        cardPrio.append(4)

        if botIsRunning == False:
            close = False
            botIsRunning = True
            self.TerminalVar.set('Started bot')
            self.TerminalVar.set(farm())
        else: self.TerminalVar.set('Bot is running, updated your configuration')

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
            message+= 'There was an error with the \'Times to refill\' configuration'
            error = True
        if error == True: self.TerminalVar.set(message)
        else:
            self.TerminalVar.set('starting bot...')
            botThread = threading.Thread(target=self.startBot)
            botThread.start()


    def selectedApp(self):
        if self.emuType.get() == 'Nox':
            self.emuType.set('NoxPlayer')

    def __init__(self, *args, **kwargs):
        root = Tk.__init__(self, *args, **kwargs)
        self.frame = VerticalScrolledFrame(root)
        self.frame.pack(fill=BOTH, side=BOTTOM, expand=YES)
        self.geometry('550x750')

        self.botModeVar = IntVar()
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

        self.title("FGOFarmingBot "+version)
        Label(self.frame.interior, text='Welcome to FGOFarmingBot', anchor='center').pack()
        Label(self.frame.interior, text="Start by selection one of this options, then proceed to press 'Start' button!",
              anchor='center').pack()
        Label(self.frame.interior, text="\nChoose which mode do you want the bot runs", anchor='center').pack()
        modeButtons = [self.createRadioButton(m, self.botModeVar) for m in self.botModes]
        self.botModeVar.set(1)

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

        Label(self.frame.interior, text="\nHow many times do you want to get the energy refilled?\n(0 means infinite)\n", anchor='center').pack()
        ttk.Entry(self.frame.interior, textvariable=self.timesToRefillVar).pack()
        var1 = IntVar()


        Label(self.frame.interior, text="\nCombat System:", anchor='center').pack(fill='both')
        Label(self.frame.interior, text="Select which card prioroty order:\n", anchor='center').pack(fill='both')
        self.cardPrioBox = ttk.Combobox(self.frame.interior, values=self.cardPrios, state="readonly",textvariable=self.cardPrioVar).pack()

        Label(self.frame.interior, text="").pack()
        Checkbutton(self.frame.interior, text="Color chains priority", variable=self.enableChainsVar).pack()
        Label(self.frame.interior, text="").pack()
        Checkbutton(self.frame.interior, text="Revert card order?\n(higher priority card at the end, does not apply to NP)", variable=self.revertCardOrderVar).pack()
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
        Button(self.frame.interior, text="Start/Upadte", anchor='s', command=self.checkCorrectInput).pack(side=BOTTOM, fill=X)

        mainloop()


# Main
app = botMenu()
app.mainloop()
close = True

## Notes

# 1280 * 720
# Don't allow resizing screen
