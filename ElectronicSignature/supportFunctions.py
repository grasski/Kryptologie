import hashlib
import os
import rsa
import zipfile


def doHash(fileDir):
    if os.path.isfile(fileDir):
        blockSize = 65536

        hash = hashlib.sha3_512()
        with open(fileDir, 'rb') as f:
            fb = f.read(blockSize)
            while len(fb) > 0:
                hash.update(fb)
                fb = f.read(blockSize)

        return hash.hexdigest()

    return False


def sign(filePath, saveToPath):
    key = rsa.generateKeyPair(15)

    hashedFile = doHash(filePath)
    if hashedFile is False:
        return [False, "Failed to do file hash."]

    sign = rsa.encrypt(hashedFile, key[1][0], key[1][1])
    if sign[0] is False:
        return [False, sign[1]]
    sign = f"RSA_SHA3-512 {sign[0]}"

    pub = f"RSA {rsa.baseEncode(str(key[0][0]))}\nRSA {rsa.baseEncode(str(key[0][1]))}"
    priv = f"RSA {rsa.baseEncode(str(key[1][0]))}\nRSA {rsa.baseEncode(str(key[1][1]))}"
    if save(saveToPath, ".pub", pub) is False or save(saveToPath, ".priv", priv) is False:
        return [False, "Failed to save keys!"]

    if save(saveToPath, ".sign", sign) is False:
        return [False, "Failed to save electronic signature!"]

    fileName = os.path.splitext(os.path.basename(filePath))[0]
    try:
        with zipfile.ZipFile(f"{saveToPath}/{fileName}.zip", "w") as zip:
            zip.write(f"{saveToPath}/.sign", ".sign")
            zip.write(filePath, os.path.basename(filePath))
        os.remove(f"{saveToPath}/.sign")
    except:
        return [False, "Failed to create zip file."]

    return [True, "File has been successfully signed!"]


def verify(publicKeyFilePath, zipFilePath):
    try:
        with open(publicKeyFilePath, "r") as f:
            n = f.readline()
            e = f.readline()

        if len(n) > 5 and len(e) > 5:
            n = int(rsa.baseDecode(n[4:].replace("\n", "")))
            e = int(rsa.baseDecode(e[4:].replace("\n", "")))
        else:
            return [False, "Failed to get public key."]
    except:
        return [False, "Failed to get public key."]

    files = getZipFiles(zipFilePath)
    if files[0] is False:
        return [False, files[1]]
    try:
        with zipfile.ZipFile(zipFilePath, 'r') as zip:
            sign = zip.read(files[1][0]).decode('ascii')
            path = os.path.dirname(os.path.abspath(zipFilePath))
            l = zip.infolist()
            for f in l:
                if f.filename == files[1][1]:
                    f.filename = "extractedZipFileHash__" + f.filename
                    file = zip.extract(f, path=path)

        zipFileHash = doHash(file)
        os.remove(file)
        if len(sign) > 14 and zipFileHash is not False:
            sign = sign[13:]
        else:
            return [False, "Failed to read zip file"]
    except:
        return [False, "Failed to read zip file"]

    originalHash = rsa.decrypt(sign, n, e)
    if originalHash[0] is False:
        return [False, "Failed to decrypt hash."]

    if originalHash[0] == zipFileHash:
        return [True, "File is original!"]
    else:
        return [False, "File has been changed!"]


def save(saveToPath, fileName, message):
    try:
        if not os.path.exists(saveToPath):
            os.makedirs(saveToPath)

        with open(os.path.join(saveToPath, fileName), 'w') as temp_file:
            temp_file.write(message)

        return True
    except:
        return False


def getZipFiles(zipPath):
    try:
        with zipfile.ZipFile(zipPath, "r") as zip:
            files = zip.namelist()
            if len(zip.namelist()) == 2:
                if ".sign" in files[0]:
                    return [True, [files[0], files[1]]]
                if ".sign" in files[1]:
                    return [True, [files[1], files[0]]]

            return [False, "Wrong zip content."]
    except:
        return [False, "Problem with getting zip information."]


def getFolderFiles(folderPath):
    files = os.listdir(folderPath)
    pub = ""
    zipF = ""
    for f in files:
        if pub != "" and zipF != "":
            break

        if ".pub" in f:
            pub = f
        if ".zip" in f:
            zipF = f

    if pub != "" and zipF != "":
        return [True, [pub, folderPath+"/"+zipF]]
    else:
        return [False, "Wrong folder content."]
