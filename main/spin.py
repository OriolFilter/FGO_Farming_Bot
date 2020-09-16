# from main import cardPickerWithAdb as cp
import cardPickerWithAdb as cp
from time import sleep

print('Welcome to SpinBot!')


if __name__ == '__main__':

    hostname="40edac8d"
    client=cp.botClient(hostName=hostname)
    client.screenshot()
    spinnPos=None
    while not spinnPos:spinnPos=client.findSpinButton()
    # print(spinnPos)
    prizeResetButtonPos=None
    resetButtonPos=None
    while True:
        client.screenshot()
        # while not client.findPrizeResetButton():
        for x in range (33*5,0,-1):client.click(spinnPos)
        if not prizeResetButtonPos:prizeResetButtonPos=client.findPrizeResetButton(returnPos=True)
        if prizeResetButtonPos:client.click(prizeResetButtonPos)
        sleep(1)
        if not resetButtonPos:client.findResetButton=client.findResetButton(returnPos=True)
        if resetButtonPos:client.click(resetButtonPos)
