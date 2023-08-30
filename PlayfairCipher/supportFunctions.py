import string
import re
import numpy as np


def alphabet(lang="CZ"):
    return list(string.ascii_lowercase.replace("w", "")) if lang == "CZ" \
            else list(string.ascii_lowercase.replace("q", ""))


def translateText(text, key):
    loweredText = text.lower()
    if key is True:
        toChange = {'ě': 'e', 'š': 's', 'č': 'c', 'ř': 'r', 'ž': 'z', 'ý': 'y', 'á': 'a', 'í': 'i', 'é': 'e', 'ú': 'u',
                    'ů': 'u', 'ň': 'n', 'ť': 't', "ó": "o"}
    else:
        toChange = {'ě': 'e', 'š': 's', 'č': 'c', 'ř': 'r', 'ž': 'z', 'ý': 'y', 'á': 'a', 'í': 'i', 'é': 'e', 'ú': 'u',
                    'ů': 'u', 'ň': 'n', 'ť': 't', "ó": "o", "0": "nula", "1": "jedna", "2": "dva", "3": "tri",
                    "4": "ctyri", "5": "pet", "6": "sest", "7": "sedm", "8": "osm", "9": "devet"}

    toTranslate = loweredText.maketrans(toChange)
    return loweredText.translate(toTranslate)


def splitText(text, pieces):
    text = text.upper()
    sT = ""
    for i in range(0, len(text), pieces):
        if i < len(text) - pieces:
            sT = sT + (text[i:i + pieces]) + " "
        else:
            sT = sT + (text[i:i + pieces])

    return sT


def filterText(text, lang, key=False):
    if key:
        reg = string.punctuation + string.digits + "°´¨ˇ§\t\n"
    else:
        reg = string.punctuation + "°´¨ˇ§\t\n"

    text = text.lower()
    text = translateText(text, key)

    text = text.replace("w", "v") if lang == "CZ" else text.replace("q", "o")

    text = re.sub(f"[{reg}]", "", text)
    return text


def repairText(text, lang, decrypt=False):
    text = text.replace("\\", "")
    text = text.lower()
    text = filterText(text, lang)
    if decrypt is False:
        text = text.replace(" ", "XMEZERAX")
        text = insertBetweenSameChars(text, lang)

        text = text.lower()
        textLen = len(text)
        if textLen % 2 != 0:
            if text[textLen-1] is "z":
                text += "w" if lang != "CZ" else "v"
            else:
                text += "z"
    else:
        text = text.replace(" ", "")

    return text


def insertBetweenSameChars(text, lang):
    text = text.lower()
    l = len(text)
    i = 0
    while i < l:
        textPart = text[i:i + 2]
        if len(textPart) > 1:
            if textPart[0] == textPart[1]:
                text = text[:i+1] + ("z" if textPart[0] != "z" else "w" if lang != "CZ" else "v") + text[i+1:]
                l = len(text)

        i += 2

    return text


def createTable(key, lang, size=5):
    key = list(dict.fromkeys(filterText(key.replace(" ", "").replace("\\", ""), lang, True)))

    al = alphabet(lang)
    fill = np.concatenate((key, al))    # arrays join
    filled = list(dict.fromkeys(fill))  # delete same keys

    arr = [[]*size]*size
    for i in range(0, size*size, size):
        arr[int(i/size)] = filled[i:i+size]

    return arr


def findIn2dArray(keyArray, find):
    for i, e in enumerate(keyArray):
        try:
            return i, e.index(find)
        except ValueError:
            pass
    return None


def getShape(key, chars, decrypt=False):
    a = findIn2dArray(key, chars[0])
    b = findIn2dArray(key, chars[1])

    if a[0] == b[0]:
        # Same row
        if decrypt is False:
            a = (a[0], a[1] + 1 if a[1] < len(key[1]) - 1 else 0)
            b = (b[0], b[1] + 1 if b[1] < len(key[1]) - 1 else 0)
        else:
            a = (a[0], a[1] - 1 if a[1] > 0 else len(key[1]) - 1)
            b = (b[0], b[1] - 1 if b[1] > 0 else len(key[1]) - 1)

    elif a[1] == b[1]:
        # Same column
        if decrypt is False:
            a = (a[0] + 1 if a[0] < len(key[0]) - 1 else 0, a[1])
            b = (b[0] + 1 if b[0] < len(key[0]) - 1 else 0, b[1])
        else:
            a = (a[0] - 1 if a[0] > 0 else len(key[0]) - 1, a[1])
            b = (b[0] - 1 if b[0] > 0 else len(key[0]) - 1, b[1])
            pass
    else:
        # Square
        aTemp = a
        a = (a[0], b[1])
        b = (b[0], aTemp[1])

    return a, b


def encrypt(text, key, lang):
    keyArr = createTable(key, lang)
    text = repairText(text, lang)

    pairs = splitText(text, 2)
    cT = ""
    for i in range(0, len(text)-1, 2):
        coords = getShape(keyArr, text[i:i+2])
        cT += keyArr[coords[0][0]][coords[0][1]]
        cT += keyArr[coords[1][0]][coords[1][1]]

    return pairs, splitText(cT, 5)


def recoverChanges(text):
    loweredText = text.lower()

    changedText = loweredText.replace("nula", "0").replace("jedna", "1").replace("dva", "2").replace("tri", "3")\
        .replace("ctyri", "4").replace("pet", "5").replace("sest", "6").replace("sedm", "7").replace("osm", "8")\
        .replace("devet", "9").replace("xmezerax", " ")
    return changedText


def decrypt(text, key, lang):
    keyArr = createTable(key, lang)
    text = repairText(text, lang, True)

    pairs = splitText(text, 2)
    oT = ""
    for i in range(0, len(text) - 1, 2):
        coords = getShape(keyArr, text[i:i + 2], True)
        oT += keyArr[coords[0][0]][coords[0][1]]
        oT += keyArr[coords[1][0]][coords[1][1]]

    oT = recoverChanges(oT)
    return pairs, oT
