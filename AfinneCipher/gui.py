# Autor: Jiří Daberger

import PySimpleGUI as sg
import supportFunctions as sf
import clipboard


def callWindow():
    encrypt = True

    layoutKeysA = [
        [sg.Image(filename="up.png", enable_events=True, key="A_up")],
        [sg.Image(filename="down.png", enable_events=True, key="A_down")]
    ]

    layoutKeysB = [
        [sg.Image(filename="up.png", enable_events=True, key="B_up")],
        [sg.Image(filename="down.png", enable_events=True, key="B_down")]
    ]

    layout = [
        [sg.Text("Welcome in Affine cipher application.", text_color="black", font=('Arial', 30),
                 justification='center')],
        [sg.Text("Select alphabet:", font=("Arial", 15)),
         sg.Combo(["A-Z + 'space'", "A-Z + 'space' + 0-9"], default_value="A-Z + 'space'", font=("Arial", 15),
                  readonly=True, enable_events=True, key="alphabet"),

         sg.Text("Key A:", font=("Arial", 15)),
         sg.Input(default_text=3, background_color="lightgreen", size=(5, 2), font=("Arial", 15), enable_events=True,
                  key="A"), sg.Frame(layout=layoutKeysA, title=""),

         sg.Text("Key B:", font=("Arial", 15)),
         sg.Input(default_text=5,  background_color="lightgreen", size=(5, 2), font=("Arial", 15), enable_events=True,
                  key="B"), sg.Frame(layout=layoutKeysB, title="")],

        [sg.Image(filename="encryptBtn2.png", enable_events=True, key="encryptBtn"),
         sg.Text("Enter text to encrypt:", font=("Arial", 15), key="text"),
         sg.Input(font=("Arial", 15), key="input")],

        [sg.Button("Encrypt", font=("Arial", 15), bind_return_key=True, key="ENTER")],
        [sg.Text("", font=("Arial", 10), key="removed")],

        [sg.Column(layout=[[sg.Text("Encrypted text:", font=("Arial", 15), key="code")],
                           [sg.Text("", size=(48, 10), justification="center", enable_events=True, font=("Arial", 20),
                                    tooltip="Click to copy text.", key="result")]],
                   size=(800, 100), visible=False, scrollable=True, vertical_scroll_only=True, key="result2")],

        [sg.Button("EXIT", font=("Arial", 15))]
    ]

    window = sg.Window("Affine cipher.", layout, element_justification="center")

    while True:
        event, values = window.read(0)
        a, b, alIndex, alphabetSize = None, None, None, None

        if values is not None and event is not None:
            alIndex = window["alphabet"].TKCombo.current()
            alphabetSize = len(sf.alphabet(alIndex))

            if event == "A_up":
                handleKeys(window, "A", "+")
            if event == "B_up":
                handleKeys(window, "B", "+")
            if event == "A_down":
                handleKeys(window, "A", "-")
            if event == "B_down":
                handleKeys(window, "B", "-")

            if event == "result":
                clipboard.copy(window["result"].get())

            if handleInput(window, "A"):
                try:
                    a = int(values["A"])
                    gcd = sf.gcd(a, alphabetSize)
                    if gcd == 1:
                        pass
                    else:
                        a = None
                        window["A"].update(background_color="red")
                except:
                    pass

            if handleInput(window, "B"):
                try:
                    b = int(values["B"])
                except:
                    b = None
                    pass

            if event == "encryptBtn":
                if encrypt:
                    window["encryptBtn"].update(filename="decryptBtn2.png")
                    window["text"].update("Enter text to decrypt:")
                    window["ENTER"].update("Decrypt")
                    window["code"].update("Decrypted text:")
                    encrypt = False
                else:
                    window["encryptBtn"].update(filename="encryptBtn2.png")
                    window["text"].update("Enter text to encrypt:")
                    window["ENTER"].update("Encrypt")
                    window["code"].update("Encrypted text:")
                    encrypt = True

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break

        if event == "ENTER":
            if None not in [a, b, alIndex, alphabetSize]:
                if encrypt is True:
                    ec = sf.encrypt(values["input"], alIndex, a, b, alphabetSize)
                    if ec is not False:
                        cT = ec[0]
                        if cT != "":
                            window["result2"].update(visible=True)
                            window["removed"].update("Removed chars:" + str(ec[1]), visible=True)
                            window["result"].update(cT)
                        else:
                            window["result2"].update(visible=False)
                            window["removed"].update(visible=False)
                else:
                    dc = sf.decrypt(values["input"], alIndex, a, b, alphabetSize)
                    if dc is not False:
                        oT = dc[0]
                        if oT != "":
                            window["result2"].update(visible=True)
                            window["removed"].update("Removed chars:" + str(dc[1]), visible=True)
                            window["result"].update(oT)
                        else:
                            window["result2"].update(visible=False)
                            window["removed"].update(visible=False)
            else:
                window["result2"].update(visible=False)
                window["removed"].update(visible=False)
            pass

    window.close()


def handleInput(window, key):
    userInput = window[key]
    inp = userInput.get()

    if inp.isnumeric():
        userInput.update(background_color="lightgreen")
        return True
    else:
        if len(inp) > 1:
            userInput.update(str(inp).rstrip(inp[-1]))
            return True
        else:
            if inp.isnumeric():
                userInput.update(background_color="lightgreen")
                return True
            else:
                userInput.update("", background_color="red")
                return False


def handleKeys(window, key, mark):
    textInput = window[key]
    try:
        oldText = int(textInput.get())
    except:
        textInput.update(1)
        return True

    if mark == "+":
        textInput.update(int(oldText) + 1)
    else:
        if oldText > 1:
            textInput.update(int(oldText) - 1)
