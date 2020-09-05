from main import cardPickerWithAdb as cp

print('Select the mode')
print('0\t normal mode\n1\t combat mode\n2\t card picking mode\n-1 debugg mode')
option = input()




if __name__ == '__main__':
    client=cp.botClient(hostName="40edac8d")

    if option == 0:
        client.timesToRestoreEnergy=0
        # test.npOnDangerOrServant=True
        client.selectSupport=True
        client.repeatQuest=True
        #test=botClient(debugg=True)

        # Test

        # Running Main
        client.main(mode=0)

    elif option == 1:
        client.main(mode=1)
    elif option == 2:
        client.main(mode=2)
    elif option == -1: # Under construction
        client.screenshot(True)
        client.debuggMode()
        # test.clickSpeedTest()
        # test.swipe([500,100],[200,200])
        # test.screenshot()
        # print(test.restoreApples(2))
