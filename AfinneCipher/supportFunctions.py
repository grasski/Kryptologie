# Autor: Jiří Daberger

import string
import re
import math


def alphabet(numbers, asText=False):
    """
    26 characters without numbers, 36 characters with numbers.

    :param numbers: Represent text with numbers [1] or without numbers [0].
    :param asText: Represent return as a string [True] or as a list [False].
    :return: [list/string] Selected alphabet used for encryption/decryption.
    """

    if not numbers:
        return list(string.ascii_lowercase) if asText is False \
            else str(string.ascii_lowercase)
    else:
        return list(string.ascii_lowercase + string.digits) if asText is False \
            else str(string.ascii_lowercase + string.digits)


def repairText(text, numbers, decrypt=False):
    """
    :param text: [string] Input text from user.
    :param numbers: Represent text with numbers [1] or without numbers [0].
    :param decrypt: Called from decrypt function [True], or not [False].
    :return: [string]
    """

    if not numbers:
        reg = string.punctuation + string.digits + "°´¨§\t\n"
    else:
        reg = string.punctuation + "°´¨§\t\n"

    if decrypt is False:
        text = text.replace(" ", "XMEZERAX")

    text = text.lower()
    clearedText = re.sub(f"[{reg}]", "", text)
    removed = re.findall(f"[{reg}]", text)
    loweredText = clearedText.lower()
    toChange = {'ě': 'e', 'š': 's', 'č': 'c', 'ř': 'r', 'ž': 'z', 'ý': 'y', 'á': 'a', 'í': 'i', 'é': 'e', 'ú': 'u',
                'ů': 'u', 'ň': 'n', 'ť': 't'}
    toTranslate = loweredText.maketrans(toChange)
    newText = loweredText.translate(toTranslate)

    correctText = re.findall(f"[{alphabet(numbers, True)}]", newText)
    return correctText, removed


# https://cs.wikipedia.org/wiki/Eukleid%C5%AFv_algoritmus
def gcd(a, m):
    try:
        if a < 0 or m < 0:
            return False
        while m > 0:
            r = a % m
            a = m
            m = r

        return a
    except:
        return False


def splitText(text, pieces):
    text = text.upper()
    sT = ""
    for i in range(0, len(text), pieces):
        if i < len(text) - pieces:
            sT = sT + (text[i:i + pieces]) + " "
        else:
            sT = sT + (text[i:i + pieces])

    return sT


def encrypt(text, numbers, a, b, m):
    try:
        t = repairText(text, numbers)
        rText = t[0]
        removed = t[1]
        al = alphabet(numbers, False)

        ct = ""
        for i in range(len(rText)):
            y = (a*al.index(str(rText[i])) + b) % m
            ct = ct + al[y]

        ct = ct.upper()
        ct = splitText(ct, 5)
        return ct, removed
    except:
        return False


# https://www.dcode.fr/bezout-identity
def inverse(a, m):
    if gcd(a, m) == 1:
        r0 = a
        r1 = m
        u0 = 1
        u1 = 0
        v0 = 0
        v1 = 1
        while r1 != 0:
            q = math.floor(r0/r1)
            rs = r0
            us = u0
            vs = v0
            r0 = r1
            u0 = u1
            v0 = v1
            r1 = rs - q*r1
            u1 = us - q*u1
            v1 = vs - q*v1
        if u0 < 0:
            u0 = u0 + m

        return u0
    return False


def decrypt(text, numbers, a, b, m):
    try:
        t = repairText(text, numbers, True)
        rText = t[0]
        removed = t[1]
        al = alphabet(numbers, False)
        aInverse = inverse(a, m)

        oT = ""
        for i in range(len(rText)):
            y = (aInverse * (al.index(str(rText[i])) - b)) % m
            oT = oT + al[y]

        oT = oT.replace("xmezerax", " ")
        return oT, removed
    except:
        return False
