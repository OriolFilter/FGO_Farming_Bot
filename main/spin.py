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
    # prizeResetButtonPos=None
    # resetButtonPos=None
    # closeButtonPos=None
    while True:
        client.screenshot()
        if not spinnPos:
            spinnPos = client.findSpinButton()
            # print(spinnPos)
        if client.findSpinButton(returnPos=False) and spinnPos:
        # if client.findPrizeResetButton(False) and´ñççç client.findSpinButton(returnPos=False):
            for x in range(33 * 4, 0, -1): client.click(spinnPos)
        if client.findPrizeResetButton(returnPos=False):
            client.click(client.findPrizeResetButton(returnPos=True))
            sleep(0.2)
        if client.findResetButton(returnPos=False):
            client.click(client.findResetButton(returnPos=True))
            sleep(1)
        if client.findClosePopUpButton(returnPos=False):
            client.click(client.findClosePopUpButton(returnPos=True))
            sleep(0.2)

