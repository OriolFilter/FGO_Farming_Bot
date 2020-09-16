# from main import cardPickerWithAdb as cp
import cardPickerWithAdb as cp

print('Select the mode')
print('0\t normal mode\n1\t combat mode\n2\t card picking mode\n3\t qp mode\n-1\tTake screenshot\n-2\tSpin 10\n')
option = int(input())

if __name__ == '__main__':

    hostname="40edac8d"
    if option == 0:
        client=cp.botClient(hostName="40edac8d")
        client.timesToRestoreEnergy=20
        client.npOnDangerOrServant=True
        client.selectSupport=True
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
        client.selectSupport=False
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
        pos=None
        while not pos:pos=client.findSpinButton()
        print(pos)
        while True:client.click(pos)
