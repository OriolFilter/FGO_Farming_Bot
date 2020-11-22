from main import cardPickerWithAdb as cp
# import cardPickerWithAdb as cp
from time import sleep

print('Select the mode')
print('0\t normal mode\n1\t combat mode\n2\t card picking mode\n3\t qp mode\n-1\tTake screenshot\n-2\tSpin 10\n-3\tTest image recogntion\n')
# option = int(-3)
option = int(input())

if __name__ == '__main__':

    # hostname="b6997f9a"
    hostname="40edac8d"
    ceList=["ChaldeaLunchtimeU",""]
    if option == 0:
        client=cp.botClient(hostName=hostname)
        client.supportColorPalette=1
        # client.timesToRestoreEnergy=-1        # client.timesToRestoreEnergy=-1
        client.timesToRestoreEnergy=0
        client.npOnDangerOrServant=True
        client.selectSupportBool=True
        client.repeatQuest=True
        # client.cardsPrio=[1,2,0,3]
        client.cardsPrio=[0,1,2,3]
        #test=botClient(debugg=True)

        # Test

        # Running Main
        print('start')
        client.main(mode=0)
        print('END')

    elif option == 1:
        client=cp.botClient(hostName=hostname)
        client.main(mode=1)
    elif option == 2:
        client=cp.botClient(hostName=hostname)
        client.main(mode=2)
    elif option == 3:
        client=cp.botClient(hostName=hostname)
        client.selectSupportBool=False
        client.repeatQuest=True
        client.timesToRestoreEnergy=0
        client.main(mode=0)
    elif option == -1: # Under construction
        client=cp.botClient(hostName=hostname,debugg=True)
        print('START')
        client.screenshot(save=True,imgPath="Test.png")
        print('END')
    elif option == -2:
        client=cp.botClient(hostName=hostname)
        client.screenshot()
        spinnPos=None

        prizeResetButtonPos=None
        resetButtonPos=None
        closeButtonPos=None
        while True:

            if not prizeResetButtonPos:
                prizeResetButtonPos=client.findPrizeResetButton(returnPos=True)
                client.screenshot()
            if prizeResetButtonPos:
                client.click(prizeResetButtonPos)
                sleep(0.2)
            if not resetButtonPos:
                resetButtonPos=client.findResetButton(returnPos=True)
                client.screenshot()
            if resetButtonPos:
                client.click(resetButtonPos)
                sleep(1)
            if not closeButtonPos:
                closeButtonPos=client.findClosePopUpButton(returnPos=True)
                client.screenshot()
            if closeButtonPos:
                client.click(closeButtonPos)
                sleep(0.2)
    elif option == -3:
        # client = cp.botClient(hostName=hostname,debugg=True)
        # print('START')
        # client.screenshot(save=True,imgPath="Test.png")
        # print('END')
        # client = cp.botClient(hostName="40edac8d",debugg=True)
        # print('START')
        # client.screenshot(save=True,imgPath="Test2.png")
        # print('END')
        # client = cp.botClient(hostName=hostname)
        # client.screenshot()
        # client.screenshot()
        # while True:
        #     if client.checkAttackButton():
        #         print(True)
        #         client.click(xy=[client.attackButtonLoc[0] + 50, client.attackButtonLoc[1]])
        #         sleep(1)
        #         input()
        client = cp.botClient(hostName=hostname)
        client.supportColorPalette=1
        client.screenshot()
        client.selectSupport(ceName="ChaldeaLunchtimeU")
        # print(client.checkSuportBarrTopOrBottom())
        # print(client.checkSuportBarrTopOrBottom(False))
        # client.click([50,50])
        # client.draggSupport(True)
        # sleep(2)
        # client.draggSupport(False)
        # xy = client.returnBarrPos(1)
        # self.click(xy)
        # self.swipe(xy,xy)
        # input()
        # client.click(xy=xy)
        # input()
        # client.dragg([xy[0] + 15, xy[1]], [xy[0] + 15, xy[1] + 10],time=250)
        # client.dragg([xy[0] + 15, xy[1]], [xy[0] + 15, xy[1] + 10],time=250)

        # client.click([client.screenshotImg.shape[0]/2,client.screenshotImg.shape[1]/3])
        # client.click([client.screenshotImg.shape[0]/2,client.screenshotImg.shape[1]/2])
        # client.click([client.screenshotImg.shape[0]/2,client.screenshotImg.shape[1]/2])
        # client.click([client.screenshotImg.shape[0]/2,client.screenshotImg.shape[1]/4])
        # client.click([client.screenshotImg.shape[1]/2,client.screenshotImg.shape[0]/2])
        # print(client.screenshotImg.shape[0])
        # print(client.screenshotImg.shape[1])
        # client.click([client.screenshotImg.shape[0]/2,50])
        # print(client.screenshotImg.shape)
        # print(client.screenshotImg.shape)
        # print(client.screenshotImg.shape)
        # print(client.screenshotImg.shape[1])

# https: // www.python.org / dev / peps / pep - 0572 /