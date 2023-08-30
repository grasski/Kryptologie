import math
import string
import numpy as np
import re


def alphabet(lang, numbers):
    return list(string.ascii_lowercase + string.digits) if numbers == 6 \
        else list(dict.fromkeys(string.ascii_lowercase.replace("w", "v"))) if lang == "CZ" \
        else list(dict.fromkeys(string.ascii_lowercase.replace("q", "o")))


def checkMatrix(arr, lang, size):
    vals, idx_start, count = np.unique(arr, return_counts=True, return_index=True)
    vals = vals[count > 1]
    sameChars = []
    toDelete = []
    for c in vals:
        toDelete.append(c)
        coords = np.where(np.char.find(arr, c) >= 0)
        for i in range(0, len(coords[0])):
            sameChars.append([coords[0][i], coords[1][i]])

    al = alphabet(lang, size)
    for i, a in enumerate(arr):
        for c in range(0, len(a)):
            if a[c] in toDelete or a[c] == " ":
                continue
            else:
                al.remove(a[c])
    for c in toDelete:
        if c in string.punctuation + " °´¨§":
            continue
        al.remove(c)
    return True if len(sameChars) == 0 else (sameChars, al)


def generateMatrix(size, lang, empty=False, random=True):
    if random is False:
        prepareData = np.array_split(alphabet(lang, size), size)
        return np.array(np.matrix(prepareData))

    if empty:
        al = [" "] * size * size
    else:
        if size == 5:
            al = alphabet(lang, False)
        else:
            al = alphabet(lang, 6)

    return np.random.choice(al, replace=False, size=(size, size))


def translateText(text, key):
    loweredText = text.lower()

    if key is True:
        toChange = {'ě': 'e', 'š': 's', 'č': 'c', 'ř': 'r', 'ž': 'z', 'ý': 'y', 'á': 'a', 'í': 'i', 'é': 'e', 'ú': 'u',
                    'ů': 'u', 'ň': 'n', 'ť': 't', "ó": "o", "ľ": "l", "ď": "d"}
    else:
        toChange = {'ě': 'e', 'š': 's', 'č': 'c', 'ř': 'r', 'ž': 'z', 'ý': 'y', 'á': 'a', 'í': 'i', 'é': 'e', 'ú': 'u',
                    'ů': 'u', 'ň': 'n', 'ť': 't', "ó": "o", "ľ": "l", "ď": "d",
                    "0": "nula", "1": "jedna", "2": "dva", "3": "tri", "4": "ctyri", "5": "pet", "6": "sest",
                    "7": "sedm", "8": "osm", "9": "devet"}

    toTranslate = loweredText.maketrans(toChange)
    return loweredText.translate(toTranslate)


def filterText(text, lang, size, key=False):
    text = text.lower()
    if size == 5:
        text = text.replace("w", "v") if lang == "CZ" else text.replace("q", "o")

    text = translateText(text, key)

    if key:
        text = "".join(list(dict.fromkeys(text)))
        text = str(text).replace(" ", "")
    else:
        text = text.replace(" ", "xspacex")

    al = "".join(alphabet(lang, size))
    text = re.findall(f"[{al}]", text)
    return "".join(text)


def splitText(text, pieces):
    text = text.upper()
    sT = ""
    for i in range(0, len(text), pieces):
        if i < len(text) - pieces:
            sT = sT + (text[i:i + pieces]) + " "
        else:
            sT = sT + (text[i:i + pieces])

    return sT


def createMatrix(size, data):
    arr = [[] * size[0]] * size[1]
    for i in range(0, size[0] * size[1], size[0]):
        arr[math.floor(int(i / size[0]))] = data[i:i + size[0]]
    return arr


def encrypt(text, arr, lang, size, key):
    text = filterText(text, lang, size)
    key = filterText(key, lang, size, True)

    if len(text) < 1:
        return False, ""

    if len(key) < 2:
        return False, "Wrong key."

    if len(text) < 1:
        return False, ""

    indexKeys = "ADFGX" if size == 5 else "ADFGVX"
    translate = ""
    for c in text:
        if c == " ":
            continue
        coords = np.where(np.char.find(arr, c) >= 0)
        translate += indexKeys[int(coords[0])] + indexKeys[int(coords[1])]

    size = (len(key), math.ceil(len(translate) / len(key)))
    keyMatrix = createMatrix(size, translate)

    cT = [""] * size[0]
    sortedKey = sorted(key)
    for pos, i in enumerate(sortedKey):
        newIndex = key.index(i)
        key = key[:newIndex] + "-" + key[newIndex + 1:]  # indicate and replace same chars for correct index
        toAppend = ""
        for c in range(len(keyMatrix)):
            try:
                toAppend += keyMatrix[c][newIndex]
            except:
                pass
        cT[pos] = toAppend

    cT = "".join(cT)
    return cT, ""


def roundN(num):
    # DOWN = the missing keys are having column size of remainder and the rest is remainder + 1
    # UP = the missing keys are having column size of remainder - 1 and the rest is remainder

    index = str(num).find(".")
    remainder = int(str(num)[index+1])

    return (math.floor(num), "down") if remainder < 5 else (math.ceil(num), "up")


def recoverChanges(text):
    loweredText = text.lower()

    changedText = loweredText.replace("nula", "0").replace("jedna", "1").replace("dva", "2").replace("tri", "3")\
        .replace("ctyri", "4").replace("pet", "5").replace("sest", "6").replace("sedm", "7").replace("osm", "8")\
        .replace("devet", "9").replace("xspacex", " ")
    return changedText


def decrypt(text, arr, lang, size, key):
    indexKeys = "adfgx" if size == 5 else "adfgvx"

    text = text.replace("xspacex", "").replace(" ", "")
    text = filterText(text, lang, size, False)
    if len(text) < 1:
        return False, ""
    key = filterText(key, lang, size, True)

    correctChars = True if len(re.subn(f"[{indexKeys}]", "", text)[0]) == 0 else False
    text = "".join(re.findall(f"[{indexKeys}]", text))

    infoMsg = ""
    if correctChars is False:
        infoMsg = f"Characters other than '{indexKeys}' were removed! "
    if len(text) % 2 != 0:
        infoMsg += "Last character has been removed because of odd length."
        text = text[:len(text)-1]

    if len(key) < 2:
        infoMsg = "Wrong key."
        return False, infoMsg
    if len(text) < 1:
        return False, infoMsg

    diff = len(text) / len(key)
    columnLength = roundN(diff)
    columns = columnLength[0]+1 if columnLength[1] == "down" else columnLength[0]
    missing = columns * len(key) - len(text)
    missingKeys = list(key[len(key)-missing:])

    sortedKey = sorted(key)
    mat = [[] for _ in range(columns)]
    down = True if columnLength[1] == "down" else False
    column = columnLength[0]

    i = 0
    l = 0
    while l < len(text):
        if missing <= 0:
            toAppend = text[l:l+column]
            l += column
        else:
            if sortedKey[i] in missingKeys:
                if down:
                    toAppend = text[l:l+column]
                    l += column
                else:
                    toAppend = text[l:l+column-1]
                    l += column - 1
            else:
                if down:
                    toAppend = text[l:l+column+1]
                    l += column + 1
                else:
                    toAppend = text[l:l + column]
                    l += column

        fill = columns-len(toAppend)
        toAppend += " "*fill
        m = 0
        if toAppend == "":
            mat[m] += " "
        for c in toAppend:
            mat[m] += c
            m += 1

        i += 1

    keyMat = [""] * len(key)
    i = 0
    for l in range(len(mat[0])):
        toAppend = ""
        newIndex = key.index(sortedKey[i])
        for e in range(len(mat)):
            try:
                toAppend += mat[e][l]
            except:
                continue
        i += 1
        keyMat[newIndex] = toAppend

    i = 0
    txt = ""
    for p in range(columns):
        for l in range(len(keyMat)):
            try:
                txt += keyMat[l][i]
            except:
                pass
        i += 1

    txt = txt.replace(" ", "")
    oT = ""
    for c in range(0, len(txt), 2):
        coords = (indexKeys.index(txt[c]), indexKeys.index(txt[c+1]))
        oT += arr[coords[0]][coords[1]]

    oT = recoverChanges(oT)
    return oT, infoMsg
