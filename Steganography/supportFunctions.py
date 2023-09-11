# Autor: Jiří Daberger

import io
from PIL import Image


charBits = 9

def editImage(image, text):
    i = 0
    try:
        pixdata = image.load()
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                r = format(pixdata[x, y][0], "08b")
                g = format(pixdata[x, y][1], "08b")
                b = format(pixdata[x, y][2], "08b")
                a = format(pixdata[x, y][3], "08b")

                if i < len(text):
                    r = r[0:7] + text[i]
                    i += 1
                if i < len(text):
                    g = g[0:7] + text[i]
                    i += 1
                if i < len(text):
                    b = b[0:7] + text[i]
                    i += 1
                # if i < len(text):
                #     a = a[0:7] + text[i]
                #     i += 1

                pixdata[x, y] = (int(r, 2), int(g, 2), int(b, 2), int(a, 2))

        return image
    except:
        return False


def readImage(image, endPoint):
    global charBits
    binText = ""
    text = ""
    try:
        pixdata = image.load()
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                r = format(pixdata[x, y][0], "08b")
                g = format(pixdata[x, y][1], "08b")
                b = format(pixdata[x, y][2], "08b")

                binText += r[7:8]+g[7:8]+b[7:8]

                if len(binText) == 3 * charBits:
                    text += convertText(binText, False)

                    if endPoint in text:
                        end = text.find(endPoint)
                        return text[:end]

                    binText = ""

        bitsLeft = len(binText)//charBits * charBits
        text += convertText(binText[0:bitsLeft], False)
        if endPoint in text:
            end = text.find(endPoint)
            return text[:end]

        return False
    except:
        return False


def convertText(text, toBin):
    global charBits
    x = charBits
    if toBin:
        bins = []
        for char in text:
            bins.append(format(ord(char), f"0{x}b"))
        return "".join(bins)
    else:
        if len(text) % x != 0:
            text = "0"*(x-len(text) % x) + text
        chars = []
        for i in range(0, len(text), x):
            part = text[i:i+x]
            dec = int(part, 2)
            chars.append(chr(dec))

        return "".join(chars)


def openImage(img):
    try:
        img = Image.open(img)
        img = img.convert("RGBA")

        return img
    except:
        return False


def saveImage(imgData, saveTo):
    try:
        imgData.seek(0)
        Image.open(io.BytesIO(imgData.read())).save(saveTo)

        return True
    except:
        return False


def freeSpace(img):
    img = openImage(img)
    if img is False:
        return False

    return img.size[0] * img.size[1] * 3


def encode(image, text, endPoint):
    img = openImage(image)
    if img is False:
        return [False, "Failed to open image!"]

    binText = convertText(text+endPoint, True)
    if freeSpace(image) < len(binText):
        return [False, "Message is too long."]

    newImage = editImage(img, binText)
    if newImage is False:
        return [False, "Failed to hide message."]

    previewData = io.BytesIO()
    img.save(previewData, format="PNG")

    return [True, previewData]


def decode(image, endPoint):
    img = openImage(image)
    if img is False:
        return [False, "Failed to open image!"]

    message = readImage(img, endPoint)
    if message is False:
        return [False, "Failed to get message from image."]

    return [True, message]
