
import time
import adb

# pip install pycryptodome, llavors ha funcionat

# https://github.com/google/python-adb/issues/148

# https://programtalk.com/python-examples/pyadb.ADB/
# import pyadb

# import os
# import subprocess
# from os import popen3

# from pyadb import ADB


# def main():
#     # creates the ADB object
#     adb = ADB()
#     # IMPORTANT: You should supply the absolute path to ADB binary
#     if adb.set_adb_path('/home/chema/.android-sdks/platform-tools/adb') is True:
#         print ("Version: %s" % adb.get_version())
#     else:
#         print ("Check ADB binary path")


# import os.path as op
#
# from adb import adb_commands
# from adb import sign_cryptography
#
#
# # KitKat+ devices require authentication
# signer = sign_cryptography.CryptographySigner(
#     op.expanduser('~/.android/adbkey'))
# # Connect to the device
# device = adb_commands.AdbCommands()
# device.ConnectDevice(
#     rsa_keys=[signer])
# # Now we can use Shell, Pull, Push, etc!
# for i in xrange(10):
#   print device.Shell('echo %d' % i)

# import openslidpipe
# import os.path as op
# import adb
# from adb import adb_commands
# from adb import sign_m2crypto
# from usb1.libusb1 import

# import libusb1
# from adb import common

# KitKat+ devices require authentication
# signer = sign_m2crypto.M2CryptoSigner(op.expanduser('~/.android/adbkey'))
# Connect to the device
# device = adb_commands.AdbCommands.ConnectDevicersa_keys=[signer])
# Now we can use Shell, Pull, Push, etc!
for i in range(10):
    print (i)
    # print (device.Shell('echo %d' % i))


#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# from ppadb.client import Client as AdbClient
# from PIL import Image
# # Default is "127.0.0.1" and 5037
# client = AdbClient(host="127.0.0.1", port=5037)
# clientId="40edac8d"
# # devices = client.devices()
# mainDev = client.device(clientId)
#
# try:
#     # for device in devices:
#     #     print(device.get_battery_level())
#     #     img=device.screencap()
#         # print(device.input_text("adb test"))
#         # device.install(apk_path)
#
#     # print(mainDev.get_battery_level())
#     # img=mainDev.screencap()
#     # # img2=Image.open(img)
#     # print(mainDev.get_top_activity())
#     # print('ABC2')
#     # img.show()
#     # print(device1.input_text("Nigga thats alot of damage!\n"))
#     # result = device1.screencap()
#     # Image.open(result)
#             # print(img.size)
#             # img.show()
#     # https://pypi.org/project/pure-python-adb/
#     pass
# except (RuntimeError):
#     print('ABC')
#
# print(mainDev.get_battery_level())
# img =mainDev.screencap()
# with open("screen.png", "wb") as fp:
#     fp.write(img)
# client.remote_disconnect()
# # img.show()

# from ppadb.client import Client as AdbClient
# client = AdbClient(host="127.0.0.1", port=5037)
# device = client.device("40edac8d")
# result = device.screencap()
# with open("screen.png", "wb") as fp:
#     time.sleep(2)
#     # time.sleep(6)
#     fp.write(result)
# client.remote_disconnect()


# https://stackoverflow.com/questions/2807070/screenshot-of-the-nexus-one-from-adb

# from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
#
# # Connects to the current device, returning a MonkeyDevice object
# device = MonkeyRunner.waitForConnection()
#
# # Takes a screenshot
# result = device.takeSnapshot()
#
# # Writes the screenshot to a file
# result.writeToFile('1.png','png')


# https://stackoverflow.com/questions/48304210/how-to-show-adb-screenshot-directly-in-python

# import subprocess
# import numpy as np
# import cv2
#
#
# pipe = subprocess.Popen("adb shell screencap -p",
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE, shell=True)
# time.sleep(10)
# image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
# image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
# # cv2.imshow("", image)
# cv2.waitKey(0)
# cv2.destroyWindow("")


# import os




from ppadb.client import Client as AdbClient
from PIL import Image
# Default is "127.0.0.1" and 5037
port=5037
ip="192.168.1.78"
# client = AdbClient()
# client = AdbClient(host=port, port=port)
client = AdbClient(host="127.0.0.1", port=port)
# client2=client.remote_connect("127.0.0.1",port)
# client2.
# device=client.device("")
# for device in client.devices():
#     try:
#         print(device.framebuffer())
#         # print(device.get_battery_level())

import io
#     except:print("f")

# clientId="40edac8d"
clientId="192.168.1.78:5037"
# devices = client.devices()
mainDev = client.device(clientId)
print(mainDev.get_battery_level())
screenshot = mainDev.screencap()

image = Image.open(io.BytesIO(screenshot))
image.show()

# import os
# import PIL.Image as Image

# from array import array

# def readimage(path):
#     count = os.stat(path).st_size / 2
#     with open(path, "rb") as f:
#         return bytearray(f.read())

# bytes = readimage()
# image = Image.open(io.BytesIO(bytes))
# image.save("screencapTest.png")
from PIL import Image
import PIL

# creating a image object (main image)
# im1 = Image.open(screenshot)

# save a image using extension
# im1 = im1.save("screencapTest.png")
#
# try:
#     # for device in devices:
#     #     print(device.get_battery_level())
#     #     img=device.screencap()
#         # print(device.input_text("adb test"))
#         # device.install(apk_path)
#
#     # print(mainDev.get_battery_level())
#     # img=mainDev.screencap()
#     # # img2=Image.open(img)
#     # print(mainDev.get_top_activity())
#     # print('ABC2')
#     # img.show()
#     # print(device1.input_text("Nigga thats alot of damage!\n"))
#     # result = device1.screencap()
#     # Image.open(result)
#             # print(img.size)
#             # img.show()
#     # https://pypi.org/project/pure-python-adb/
#     pass
# except (RuntimeError):
#     print('ABC')
#
# print(mainDev.get_battery_level())
# img =mainDev.screencap()
# with open("screen.png", "wb") as fp:
#     fp.write(img)
# client.remote_disconnect()
# # img.show()
# client.remote_connect(ip,port)
# client.remote_disconnect()

