__author__ = 'Nerya Yekutiel'

import numpy as np
from matplotlib import pyplot as plt
import re


# Not used method, was used for personal research
def showImgAndHistogram(img, key, title):
    myImg = img[:, :, ::-1]
    Rlayer = myImg[:, :, 0] & key
    myImg[:, :, 0] = Rlayer

    plt.figure()
    plt.title(title)
    plt.subplot(111)
    plt.imshow(myImg)
    plt.show()

    myHist = calcHistogram(myImg)
    plt.figure()
    plt.title(title)
    plt.subplot(111)
    plt.bar(range(256), myHist)
    plt.show()


# Not used method, was used for personal research
def textToBinaryList(text):
    noSpacesText = re.sub("\s+"," ", text)
    binaryList = list()
    key = 3
    # go over all characters
    for i in range(noSpacesText.__len__()):
        tempChar = ord(noSpacesText[i])
        for j in range(4):
            binaryList.append(tempChar & key)
            tempChar >>= 2
    binaryList.append(32)
    return binaryList


def calcHistogram(img):
    myHist = np.zeros(256)
    for i in range(256):
        myHist[i] = len(img[img == i])
    return myHist


def calcNextCoordinates(i, j, k, dims):
    """
    Generic method to find the next coordinates for encryption
    this way, in the future this method could be filled with
    sophisticated mathematical function so the encryption will be spread
    across the image
    """
    if k + 1 < dims[2]:
        k += 1
    else:
        k = 0
        if j + 1 < dims[1]:
            j += 1
        else:
            j = 0
            if i + 1 < dims[0]:
                i += 1
            else:
                i, j, k = 0, 0, 0
    return i, j, k


def encryption(img, startingCoordinates, data):
    """
    encrypts the image with 2 types of data
    #1
        actual string
    #2
        string size
    :param img:
    :param startingCoordinates:
    :param data:
    :return: encrypted image:
    """
    dims = img.shape
    i, j, k = startingCoordinates[0], \
              startingCoordinates[1], \
              startingCoordinates[2]
    if isinstance(data, str):
        for r in range(len(data)):
            currentChar = ord(data[r])
            for h in range(4):
                # temp = currentChar & 3
                i, j, k = calcNextCoordinates(i, j, k, dims)
                img[i, j, k] = (img[i, j, k] & 252) | (currentChar & 3)
                currentChar = currentChar >> 2
    if isinstance(data, long):
        value = data
        for r in range(32):
            i, j, k = calcNextCoordinates(i, j, k, dims)
            # temp = value & 3
            # imgb = img[i, j, k]
            img[i, j, k] = (img[i, j, k] & 252) | (value & 3)
            # imga = img[i, j, k]
            value = value >> 2

    return img


def encrypteImageSize(img, size):
    """
    calls the encryption method with the text size
    and encrypts from the first pixel
    :param img:
    :param size:
    :return:
    """
    startingCoordinates = (0, 0, 0)
    img = encryption(img, startingCoordinates, size)
    return img


def encrypteImage(img, data):
    """
    calls the encryption method
    and encrypts the data from the 22th pixel
    (because the text size is encrypted to the 22th pixel)
    :param img:
    :param data:
    :return:
    """
    startingCoordinates = (0, 22, 0)
    img = encryption(img, startingCoordinates, data)
    return img


def getDecrtyptedTextSize(img, startingCoordinates):
    dims = img.shape
    i, j, k = startingCoordinates[0], \
              startingCoordinates[1], \
              startingCoordinates[2]
    decryptedTextSize = long(0)
    for r in range(31):
        i, j, k = calcNextCoordinates(i, j, k, dims)
        # temp = img[i, j, k] & 3
        value = long(img[i, j, k] & 3) << 62
        decryptedTextSize = (decryptedTextSize | value) >> 2
    return decryptedTextSize


def getDecryptedText(img, startingCoordinates, size):
    currentBits = 0
    tempChar = 0
    dims = img.shape
    i, j, k = startingCoordinates[0], \
              startingCoordinates[1], \
              startingCoordinates[2]
    decryptedString = ""
    for r in range(size):
        i, j, k = calcNextCoordinates(i, j, k, dims)
        value = img[i, j, k] & 3
        if currentBits < 8:
            twoBits = value << currentBits
            tempChar = tempChar | twoBits
            currentBits += 2
        else:
            decryptedString += chr(tempChar)
            tempChar = 0
            twoBits = value << 0
            tempChar = tempChar | twoBits
            currentBits = 2
    decryptedString += chr(tempChar)
    return decryptedString


def decrypteImage(img):
    decryptionSize = getDecrtyptedTextSize(img, (0, 0, 0))
    decryptedText = getDecryptedText(img, (0, 22, 0), decryptionSize)
    return decryptedText


