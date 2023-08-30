import PySimpleGUI as sg
import supportFunctions as sf
import clipboard


def callWindow():
    encrypt = True
    lang = "EN"

    layoutBox = [
        [sg.Graph((320, 320), (0, 301), (301, 0), key='table')]
    ]

    layout = [
        [sg.Text("Welcome in Playfair Cipher application.", text_color="black", font=('Arial', 30))],

        [sg.Image(filename="usa.png", enable_events=True, key="lang"),
         sg.Text("Enter key:", font=("Arial", 15), key="key"),
         sg.Input(font=("Arial", 15), size=(20, 1), enable_events=True, key="keyInput")],
        [sg.Frame("", layout=layoutBox, border_width=0)],

        [sg.Image(filename="encryptBtn.png", enable_events=True, key="encryptBtn"),
         sg.Text("Enter text to encrypt:", font=("Arial", 15), key="text"),
         sg.Input(font=("Arial", 15), key="textInput")],

        [sg.Button("Encrypt", font=("Arial", 15), bind_return_key=True, key="ENTER")],

        [sg.Column(layout=[
            [sg.Text("Encrypted text:", font=("Arial", 15), key="code")],
            [sg.Text("", size=(48, 10), justification="center", enable_events=True, font=("Arial", 20),
                     tooltip="Click to copy text.", key="result")
             ]], size=(800, 100), scrollable=True, vertical_scroll_only=True, visible=False, key="result2")],

        [sg.Button("EXIT", font=("Arial", 15))]
    ]

    window = sg.Window('Playfair Cipher', layout, element_justification="center", finalize=True)

    handleKey(window, "keyInput", lang)
    while True:
        event, values = window.read(0)

        if values is not None and event is not None:
            if event == "keyInput":
                handleKey(window, "keyInput", lang)

            if event == "result":
                clipboard.copy(window["result"].get())

            if event == "encryptBtn":
                if encrypt:
                    window["encryptBtn"].update(filename="decryptBtn.png")
                    window["text"].update("Enter text to decrypt:")
                    window["ENTER"].update("Decrypt")
                    window["code"].update("Decrypted text:")
                    encrypt = False
                else:
                    window["encryptBtn"].update(filename="encryptBtn.png")
                    window["text"].update("Enter text to encrypt:")
                    window["ENTER"].update("Encrypt")
                    window["code"].update("Encrypted text:")
                    encrypt = True

            if event == "lang":
                if lang == "EN":
                    window["lang"].update(filename="cze.png")
                    lang = "CZ"
                else:
                    window["lang"].update(filename="usa.png")
                    lang = "EN"
                handleKey(window, "keyInput", lang)

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break

        if event == "ENTER":
            text = window["textInput"].get()
            key = window["keyInput"].get()
            if text != "":
                if encrypt:
                    cT = sf.encrypt(text, key, lang)
                    if cT[1] != "":
                        window["result2"].update(visible=True)
                        window["result"].update(cT[1])
                    else:
                        window["result2"].update(visible=False)
                else:
                    oT = sf.decrypt(text, key, lang)
                    if oT[1] != "":
                        window["result2"].update(visible=True)
                        window["result"].update(oT[1])
                    else:
                        window["result2"].update(visible=False)
            else:
                window["result2"].update(visible=False)

    window.close()


def handleKey(window, key, lang):
    keyInput = window[key].get()
    keys = sf.createTable(keyInput, lang)

    table = window["table"]
    table.erase()
    boxSize = 60
    i = 0
    for row in range(5):
        for col in range(5):
            table.draw_rectangle((col * boxSize, row * boxSize),
                                 (col * boxSize + boxSize, row * boxSize + boxSize), line_color='black',
                                 fill_color=("lightgreen" if i % 2 == 1 else "lightblue"))
            i += 1
            table.draw_text(keys[row][col], (col * boxSize + boxSize / 2, row * boxSize + boxSize / 2),
                            font=("Arial", 15))
