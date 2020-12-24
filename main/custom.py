from main import cardPickerWithAdb as cp
# import cardPickerWithAdb as cp
from time import sleep

print('Select the mode')
print('0\t normal mode\n1\t combat mode\n2\t card picking mode\n3\t qp mode\n4\t Spin mode\n-1\tTake screenshot\n-2\tSpin 10\n-3\tTesting things\n')
# option = int(-3)
option = int(input())

if __name__ == '__main__':

    hostname="b6997f9a"
    # hostname="40edac8d"
    if option == 0:
        # ce_list = ["ChaldeaTeatimeU"]
        # ce_list = ["SprinterU", "TreefoldBarrierU", "TreefoldBarrier"] # D
        # ce_list = ["ChaldeaTeatimeU", "ChaldeaLunchtimeU"]
        # ce_list = ["SchwipsigInTheSnowU", "SchwipsigInTheSnow", "HolyMaidensTeachings"]
        # ce_list = ["SchwipsigInTheSnowU"]
        ce_list = ["HolyMaidensTeachingsU"]
        # ce_list = ["SchwipsigInTheSnowU"]
        # ce_list = ["BurningBroadcastSeatU"]
        # ce_list = ["RingTheBellU"]
        client=cp.BotClient(hostName=hostname)
        client.ce_list=ce_list
        client.support_color_palette=1
        # client.times_to_restore_energy=-1        # client.times_to_restore_energy=-1
        client.times_to_restore_energy=40
        client.np_on_danger_or_servant=True
        client.select_support_bool=True
        client.repeat_quest=True
        # client.support_class_int=6 # Castera
        client.support_class_int=4 # Lancer
        # client.support_class_int=0 # Mix
        # client.cardsPrio=[1,2,0,3]
        client.cardsPrio=[0,1,2,3]
        # test=BotClient(debugg=True)


        # Test

        # Running Main
        print('start')
        client.main(mode=0)
        print('END')
        # from os import system
        # system("shutdawn /s /t 5")

    elif option == 1:
        client=cp.BotClient(hostName=hostname)
        client.main(mode=1)
    elif option == 2:
        client=cp.BotClient(hostName=hostname)
        client.main(mode=2)
    elif option == 3:
        client=cp.BotClient(hostName=hostname)
        ce_list = ["MonaLisaU","MonaLisa"]
        client.ce_list=ce_list
        client.support_color_palette=0
        # client.times_to_restore_energy=-1        # client.times_to_restore_energy=-1
        client.times_to_restore_energy=0
        client.np_on_danger_or_servant=True
        client.select_support_bool=True
        client.repeat_quest=True
        client.support_class_int=5 # Rider
        client.cardsPrio=[0,1,2,3]
        print('start')
        client.main(mode=0)
        print('END')
    elif option == 4:
        client = cp.BotClient(hostName=hostname)
        client.main(mode=3)
    elif option == -1: # Under construction
        client=cp.BotClient(hostName=hostname)
        client.debugg=True
        wh=True
        # wh=input()
        print('START')
        while wh:
            client.screenshot(save=True,imgPath="Test.png")
            wh=input()
        print('END')

    elif option == -2:
        client=cp.BotClient(hostName=hostname)
        client.screenshot()
        spinnPos=None

        prizeResetButtonPos=None
        resetButtonPos=None
        closeButtonPos=None
        while True:

            if not prizeResetButtonPos:
                prizeResetButtonPos=client.find_prize_reset_button(returnPos=True)
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
        # client = cp.BotClient(hostName=hostname,debugg=True)
        # print('START')
        # client.screenshot(save=True,imgPath="Test.png")
        # print('END')
        # client = cp.BotClient(hostName="40edac8d",debugg=True)
        # print('START')
        # client.screenshot(save=True,imgPath="Test2.png")
        # print('END')
        # client = cp.BotClient(hostName=hostname)
        # client.screenshot()
        # client.screenshot()
        # while True:
        #     if client.checkAttackButton():
        #         print(True)
        #         client.click(xy=[client.attackButtonLoc[0] + 50, client.attackButtonLoc[1]])
        #         sleep(1)
        #         input()
        client = cp.BotClient(hostName=hostname)
        ce_list = ["MonaLisaU", "MonaLisa"]
        client.ce_list = ce_list
        client.support_color_palette=1
        client.screenshot()
        client.selectSupport()
        # client.updateFriendList()
        # client.screenshot()
        # ce_list = ["ChaldeaTeatimeU", "ChaldeaTeatime"]
        # ce_list = ["ChaldeaLunchtimeU", "ChaldeaLunchtime"]
        # client.ce_list = ce_list
        # client.debugg=True
        # for CE in ce_list:
        #     client.findCE(CE)
        # client.support_class_int = 6
        # client.ce_list=["ChaldeaTeatimeU","ChaldeaLunchtimeU"]
        # client.selectSupport()
        # xy=client.returnBarrPos(0)
        # client.click()


        # print("inline for:")
        # client.time(None)
        # var = [print("Found!") for ce in ce_list if client.findCE(ce)]
        # client.time("time:\n")
        # # input()
        # print("For:")
        # client.time(None)
        # for ce in ce_list:
        #     if client.findCE(ce):print("Found!") #Aqui aniria un return
        # client.time("time:\n")
        # # input()
        # print("While:")
        # client.time(None)
        # x=0
        # finish=False
        # while not finish and x<len(ce_list):
        #     finish=client.findCE(ce_list[x])
        #     if finish:print("Found!")
        #     x+=1
        # client.time("time:\n")


        # client.selectSupport(ceName="ChaldeaLunchtimeU")
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