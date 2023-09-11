# Autor: Jiří Daberger

import random
import math
import base64
from sympy import nextprime


def splitText(text, pieces):
    sT = []
    for i in range(0, len(text), pieces):
        sT.append(text[i:i + pieces])

    return sT


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


def generateKeyPair(bits):
    ran1 = random.randint(10 ** (bits-1), 10 ** bits)
    ran2 = random.randint(10 ** (bits-1), 10 ** bits)

    p = nextprime(ran1)
    q = nextprime(ran2)
    while p == q:
        ran2 = random.randint(10 ** (bits - 1), 10 ** bits)
        q = nextprime(ran2)

    n = p*q
    eN = (p-1)*(q-1)

    e = random.randint(2, eN-1)
    while gcd(eN, e) != 1:
        e = random.randint(2, eN-1)

    d = inverse(e, eN)

    return [[n, e], [n, d]]


def convertText(text, toBin):
    x = 9
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


def encrypt(text, n, e):
    textSplit = splitText(text, 10)
    decBin = []
    for part in textSplit:
        binT = convertText(part, True)
        binT = "0" * (90 - len(str(binT))) + binT
        decBin.append(int(binT, 2))
    cT = []
    for dec in decBin:
        if dec < n:
            C = pow(dec, e, n)
            binC = format(C, "b")
            cT.append(base64.b64encode(binC.encode("ascii")).decode('ascii'))
        else:
            return [False, "Unable to encrypt, key is too small (use at least 15 decimals long number)."]

    return [" ".join(cT), ""]


def decrypt(text, n, d):
    text = text.split()

    decBin = []
    for part in text:
        try:
            binT = base64.b64decode(part.encode("ascii")).decode('ascii')
            decBin.append(int(binT, 2))
        except:
            return [False, "Wrong format (base64) of the message!"]

    oT = []
    for dec in decBin:
        if dec < n:
            M = pow(dec, d, n)
            oT.append(convertText(format(M, "b"), False))
    return ["".join(oT), ""]
