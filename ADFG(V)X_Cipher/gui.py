# Autor: Jiří Daberger

import math
import PySimpleGUI as sg
import numpy as np

import supportFunctions as sf
import clipboard


matKeys = []
lang = "EN"
tableSize = 5
def callWindow():
    global matKeys, lang, tableSize

    encrypt = True
    toChange = False
    editTable = False

    layoutBtn = [
        [sg.Column([[sg.Text("TABLE SETTINGS", font=("Arial 15 bold underline"), text_color="White")]], justification="center")],
        [sg.Button("Generate", font=("Arial", 13), key="generateMatBtn"),
         sg.Button("A-Z", font=("Arial", 13), key="alMatBtn"),
         sg.Button("Empty", font=("Arial", 13), key="emptyMatBtn")
         ],
        [sg.Checkbox("Edit table", font=("Arial", 15), enable_events=True, key="editTable")],
        [sg.Radio("5x5", "RADIO1", font=("Arial", 15), default=True, change_submits=True, key="5x5"),
         sg.Image(filename="usa.png", enable_events=True, key="lang")],
        [sg.Radio("6x6", "RADIO1", font=("Arial", 15), change_submits=True, key="6x6")]
    ]
    layoutBox = [
         [sg.Column(layout=layoutBtn),
          sg.Graph((300, 300), (0, 301), (301, 0), change_submits=True, key='table'),
          sg.Column(layout=[[sg.Text("Select character\nor press ESC\nto cancel.", font=("Arial", 15), visible=True,
                                     key="hint", size=(16, 8))]])
          ]
    ]

    layout = [
        [sg.Text("Welcome in ADFG(V)X Cipher application.", text_color="black", font=('Arial', 30))],

        [sg.Text("Enter key:", font=("Arial", 15), key="key"),
         sg.Input(font=("Arial", 15), disabled=False, enable_events=True, key="keyInput")],

        [sg.Frame("", layout=layoutBox, border_width=0)],

        [sg.Image(filename="encryptBtn.png", enable_events=True, key="encryptBtn"),
         sg.Text("Enter text to encrypt:", font=("Arial", 15), key="text"),
         sg.Input(font=("Arial", 15), disabled=False, key="textInput")],

        [sg.Button("Encrypt", font=("Arial", 15), bind_return_key=True, key="ENTER")],

        [sg.pin(sg.Text("", size=(90, 1), justification="center", text_color="pink", font=('Arial 11 bold'),
                 visible=False, key="infoMsg"))],
        [sg.pin(sg.Text("Encrypted text:", justification="center", text_color="black", font=('Arial 15 bold'),
                        visible=False, key="resultText"))],
        [sg.Column(
            layout=[
                [sg.Text("", size=(48, 10), enable_events=True, font=("Arial", 20), justification="center",
                         tooltip="Click to copy text.", key="result")]
            ],
            visible=False, scrollable=True, vertical_scroll_only=True, size=(800, 100), pad=(0, 0), key="result2")],

        [sg.Button("EXIT", font=("Arial", 15))]
    ]

    window = sg.Window('ADFG(V)X Cipher', layout, return_keyboard_events=True, element_justification="center",
                       finalize=True)

    matKeys = sf.generateMatrix(tableSize, lang)
    handleMatrix(window, tableSize, matKeys)
    window["hint"].update(visible=False)
    while True:
        event, values = window.read(0)

        if values is not None and event is not None:
            if event == "5x5" and tableSize == 6:
                window["alMatBtn"].update("A-Z")
                tableSize = 5
                matKeys = sf.generateMatrix(tableSize, lang)
                handleMatrix(window, tableSize, matKeys)
                toChange = False
            if event == "6x6" and tableSize == 5:
                window["alMatBtn"].update("A-9")
                tableSize = 6
                matKeys = sf.generateMatrix(tableSize, lang)
                handleMatrix(window, tableSize, matKeys)
                toChange = False

            if event == "editTable":
                editTable = values["editTable"]

                if editTable is False:
                    window["keyInput"].update(disabled=False)
                    window["textInput"].update(disabled=False)
                    window["hint"].update(visible=False)
                    window["ENTER"].update(disabled=False)
                    handleMatrix(window, tableSize, matKeys)
                    toChange = False

            if editTable:
                window["keyInput"].update(disabled=True)
                window["textInput"].update(disabled=True)
                window["ENTER"].update(disabled=True)

                matrixCheck = sf.checkMatrix(matKeys, lang, tableSize)
                if matrixCheck is not True:
                    window["hint"].set_size((16, 8))
                    window["hint"].update("Characters to add: " + str(matrixCheck[1]), visible=True)
                else:
                    window["hint"].update(visible=False)

                if event == "table":
                    mouse = values["table"]
                    # boxSize = 60 if tableSize == 5 else 50
                    boxSize = 50 if tableSize == 5 else 42.9
                    row, col = math.floor((mouse[1]/boxSize)), math.floor((mouse[0]/boxSize))
                    if row == 0 or col == 0:
                        toChange = False
                        continue
                    editingMatrix(window, tableSize, matKeys, (row, col))
                    toChange = True

                if toChange is True:
                    window["hint"].set_size((16, 0))
                    window["hint"].update("Select character\nor press ESC\nto cancel.", visible=True)
                    if event == 'Escape:27':
                        handleMatrix(window, tableSize, matKeys)
                        window["hint"].update(visible=False)
                        toChange = False

                    if len(event) == 1:
                        char = sf.translateText(event[0].lower(), True)
                        if tableSize == 5:
                            if lang == "CZ" and char == "w":
                                char = "v"
                            if lang != "CZ" and char == "q":
                                char = "o"

                        if char not in sf.alphabet(lang, tableSize):
                            continue

                        matKeys[row-1][col-1] = char
                        handleMatrix(window, tableSize, matKeys)
                        toChange = False

            if event == "result":
                clipboard.copy(window["result"].get())

            if event == "encryptBtn":
                if encrypt:
                    window["encryptBtn"].update(filename="decryptBtn.png")
                    window["text"].update("Enter text to decrypt:")
                    window["ENTER"].update("Decrypt")
                    encrypt = False
                else:
                    window["encryptBtn"].update(filename="encryptBtn.png")
                    window["text"].update("Enter text to encrypt:")
                    window["ENTER"].update("Encrypt")
                    encrypt = True

            if event == "lang":
                toChange = False
                if tableSize == 5:
                    if lang == "EN":
                        window["lang"].update(filename="cze.png")
                        lang = "CZ"
                        c = np.where(np.char.find(matKeys, 'w') >= 0)
                        try:
                            for e in range(0, len(c[0])):
                                matKeys[int(c[0][e])][int(c[1][e])] = "q"
                            handleMatrix(window, tableSize, matKeys)
                        except:
                            pass
                    else:
                        window["lang"].update(filename="usa.png")
                        lang = "EN"
                        c = np.where(np.char.find(matKeys, 'q') >= 0)
                        try:
                            for e in range(0, len(c[0])):
                                matKeys[int(c[0][e])][int(c[1][e])] = "w"
                            handleMatrix(window, tableSize, matKeys)
                        except:
                            pass

            if event == "generateMatBtn":
                matKeys = sf.generateMatrix(tableSize, lang)
                handleMatrix(window, tableSize, matKeys)
                toChange = False
                window["hint"].update(visible=False)
            if event == "emptyMatBtn":
                matKeys = sf.generateMatrix(tableSize, lang, True)
                handleMatrix(window, tableSize, matKeys)
                toChange = False
            if event == "alMatBtn":
                matKeys = sf.generateMatrix(tableSize, lang, False, False)
                handleMatrix(window, tableSize, matKeys)
                toChange = False

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break

        if event == "ENTER":
            correctMatrix = True if sf.checkMatrix(matKeys, lang, tableSize) is True else False
            if correctMatrix is True:
                key = values["keyInput"]
                text = values["textInput"]

                window["resultText"].update("", visible=False)
                window["infoMsg"].update("", visible=False)
                window["result2"].update(visible=False)
                window["result"].update("")

                if encrypt:
                    txt = sf.encrypt(text, matKeys, lang, tableSize, key)
                    if txt[1] != "":
                        window["infoMsg"].update(txt[1], visible=True)
                    if txt[0] is not False:
                        window["resultText"].update("Encrypted text:", visible=True)
                        window["result2"].update(visible=True)
                        window["result"].update(txt[0])
                else:
                    dec = sf.decrypt(text, matKeys, lang, tableSize, key)
                    if dec[1] != "":
                        window["infoMsg"].update(dec[1], visible=True)
                    if dec[0] is not False:
                        window["resultText"].update("Decrypted text:", visible=True)
                        window["result2"].update(visible=True)
                        window["result"].update(dec[0])
            else:
                window["resultText"].update("", visible=False)
                window["infoMsg"].update("", visible=False)
                window["result2"].update(visible=False)
                window["result"].update("")

    window.close()


def handleMatrix(window, size, arr):
    global matKeys, lang, tableSize
    matKeys = arr

    matrixCheck = sf.checkMatrix(matKeys, lang, tableSize)

    table = window["table"]
    table.erase()
    # boxSize = 60 if size == 5 else 50
    boxSize = 50 if size == 5 else 42.9

    drawHeader(table, size, boxSize)

    i = 0
    for row in range(1, size+1):
        for col in range(1, size+1):
            if matrixCheck is True:
                color = "lightgreen" if i % 2 == 1 else "lightblue"
            else:
                color = "red" if [row-1, col-1] in matrixCheck[0] else "lightblue"

            table.draw_rectangle((col * boxSize, row * boxSize),
                                 (col * boxSize + boxSize, row * boxSize + boxSize), line_color='black',
                                 fill_color=color)
            table.draw_text(arr[row-1][col-1], (col * boxSize + boxSize / 2, row * boxSize + boxSize / 2),
                            font=("Arial", 15))
            i += 1

        if size == 6:
            i += 1


def editingMatrix(window, size, arr, coords):
    global matKeys
    matKeys = arr

    table = window["table"]
    table.erase()
    # boxSize = 60 if size == 5 else 50
    boxSize = 50 if size == 5 else 42.9

    drawHeader(table, size, boxSize)

    for row in range(1, size+1):
        for col in range(1, size+1):
            table.draw_rectangle((col * boxSize, row * boxSize),
                                 (col * boxSize + boxSize, row * boxSize + boxSize), line_color='black',
                                 fill_color=("green" if coords == (row, col) else "lightblue"))
            table.draw_text(arr[row-1][col-1], (col * boxSize + boxSize / 2, row * boxSize + boxSize / 2),
                            font=("Arial", 15))

            # table.draw_rectangle((col * boxSize, row * boxSize),
            #                      (col * boxSize + boxSize, row * boxSize + boxSize), line_color='black',
            #                      fill_color=("green" if coords == (row, col) else "lightblue"))
            # table.draw_text(arr[row-1][col-1], (col * boxSize + boxSize / 2, row * boxSize + boxSize / 2),
            #                 font=("Arial", 15), color="#8e9b9e")


def drawHeader(table, size, boxSize):
    keys = "ADFGX" if size == 5 else "ADFGVX"

    i = 0
    for row in range(0, size+1):
        for col in range(0, size+1):
            if row == 0 and col == 0:
                continue
            w = (col * boxSize + boxSize)/2 if row > 0 else col * boxSize + boxSize
            h = (row * boxSize + boxSize)/2 if col > 0 else row * boxSize + boxSize

            table.draw_rectangle((col * boxSize + boxSize if row > 0 else boxSize, row * boxSize + boxSize if col > 0 else boxSize),
                                 (w, h))

            table.draw_text(keys[i], (col * boxSize + boxSize/2 + (boxSize/4 if row > 0 else 0),
                                row * boxSize + boxSize/2 + (boxSize/4 if col > 0 else 0)),
                            font=("Arial", 15))
            i += 1
            if i >= size:
                i = 0
            if row > 0:
                break
