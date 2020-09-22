from main import cardPickerWithAdb as cp
# import cardPickerWithAdb as cp
from time import sleep

print('Welcome to SpinBot!')


if __name__ == '__main__':

    hostname="40edac8d"
    client=cp.botClient(hostName=hostname)
    spinnPos=None
    # while not spinnPos:
    #     client.screenshot()
    #     spinnPos=client.findSpinButton(returnPos=True)
    prizeResetButtonPos=None
    resetButtonPos=None
    closeButtonPos=None
    while True:
        client.screenshot()
        if not spinnPos:*-
            spinnPos = client.findSpinButton()
            # print(spinnPos)
        if client.findSpinButton(returnPos=False):
        # if client.findPrizeResetButton(False) and´ñççç client.findSpinButton(returnPos=False):
            for x in range(33 * 4, 0, -1): client.click(spinnPos)
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

