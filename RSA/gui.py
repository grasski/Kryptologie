import PySimpleGUI as sg
import supportFunctions as sf
import clipboard


def callWindow():
    encrypt = True

    layoutKey = lambda a: [
        [sg.Text(f"{a} key:", font="Ariel 18 bold")],
        [sg.Multiline(size=(30, 8), default_text="", enable_events=True, auto_refresh=True, font="Ariel 12",
                      key=f"key{a}")]
    ]

    layoutKeys = [
        [sg.Column(layout=layoutKey("N"), element_justification="c"),
         sg.Column(layout=layoutKey("E"), element_justification="c"),
         sg.Column(layout=layoutKey("D"), element_justification="c")
         ]
    ]

    layoutKeyOptions = [
        [sg.Button("Hide keys", font=("Arial", 12), key="hideKey")],
        [sg.Button("Clear keys", font=("Arial", 12), key="clearKey")],
    ]

    layoutKeySettings = [
        [sg.Radio("515b", "size", default=True, font=("Arial", 12), enable_events=True, key="5b"),
         sg.Radio("1024b", "size", font=("Arial", 12), enable_events=True, key="1b")
         ],
        [sg.Radio("2048b", "size", font=("Arial", 12), enable_events=True, key="2b"),
         sg.Radio("3072b", "size", font=("Arial", 12), enable_events=True, key="3b")
         ],
        [sg.HorizontalSeparator()],
        [sg.Text("Length of generated prime numbers.", font=("Arial", 12))],
        [sg.Radio("", "size", font=("Arial", 12), enable_events=True, key="userb"),
         sg.Input(size=(10, 1), font=("Arial", 12), enable_events=True, key="userBitInput")
         ]
    ]

    menu = ["", ["Copy"]]
    menu2 = ["", ["Paste"]]

    layout = [
        [sg.Text("Welcome in RSA Cipher application.", text_color="black", font=('Arial', 30))],

        [sg.Frame("", layout=layoutKeySettings, element_justification="center", key="keySettings"),
         sg.Button("Generate keys", font=("Arial", 15), key="keyGenerate"),
         sg.Frame("", layout=layoutKeyOptions, element_justification="center")
         ],

        [sg.pin(sg.Column(layoutKeys, key="keys"))],

        [sg.Image(filename="encryptBtn.png", enable_events=True, key="encryptBtn"),
         sg.Text("Enter text to encrypt:", font=("Arial", 15), key="text"),
         sg.Multiline(font=("Arial", 15), tooltip="Right click to paste.", right_click_menu=menu2, key="textInput")
         ],

        [sg.Button("Encrypt", font=("Arial", 15), bind_return_key=True, key="ENTER")],

        [sg.pin(sg.Text("", size=(90, 1), justification="center", text_color="pink", font=('Arial 11 bold'),
                        visible=False, key="infoMsg"))],
        [sg.pin(sg.Text("Encrypted text:", justification="center", text_color="black", font=('Arial 15 bold'),
                        visible=False, key="resultTextInfo"))],
        [sg.pin(sg.Column([[sg.Multiline("", size=(80, 5), font=("Arial", 15), disabled=True, right_click_menu=menu,
                                         background_color=sg.theme_background_color(),
                                         tooltip="Right click to copy.", key="resultText")]],
                          visible=False, key="resultBox"))],

        [sg.Button("EXIT", font=("Arial", 15))]
    ]

    window = sg.Window('RSA', layout, return_keyboard_events=True, element_justification="center",
                       finalize=True)

    window.set_min_size((972, 400))
    keys = [[0]*2, [0]*2]
    while True:
        event, values = window.read(0)

        if values is not None and event is not None:
            handleInput(window, "userBitInput")

            if event == "keyN":
                n = window["keyN"].get().replace("\t", "").replace("\n", "")
                if n.isnumeric():
                    keys[0][0] = int(n)
                    keys[1][0] = int(n)
            if event == "keyE":
                e = window["keyE"].get().replace("\t", "").replace("\n", "")
                if e.isnumeric():
                    keys[0][1] = int(e)
            if event == "keyD":
                d = window["keyD"].get().replace("\t", "").replace("\n", "")
                if d.isnumeric():
                    keys[1][1] = int(d)

            if event == "Copy":
                clipboard.copy(window["resultText"].get())
            if event == "Paste":
                window["textInput"].update(clipboard.paste())

            if event == "clearKey":
                window["keyN"].update("")
                window["keyE"].update("")
                window["keyD"].update("")
                keys = [[0]*2, [0]*2]

            if event == "hideKey":
                vis = window["keys"]
                txt = "Hide keys" if not vis.visible else "Show keys"
                window["hideKey"].update(txt)
                vis.update(visible=not vis.visible)

            if event == "keyGenerate":
                if window["userb"].get():
                    if handleInput(window, "userBitInput"):
                        bit = window["userBitInput"].get()
                    else:
                        bit = None
                else:
                    bit = 155 if window["5b"].get() else 309 if window["1b"].get() else \
                        617 if window["2b"].get() else 925

                if str(bit).isnumeric():
                    window["userBitInput"].ParentRowFrame.config(background=sg.theme_background_color())
                    keys = sf.generateKeyPair(int(bit))
                    window["keyN"].update(keys[0][0])
                    window["keyE"].update(keys[0][1])
                    window["keyD"].update(keys[1][1])
                else:
                    window["userBitInput"].ParentRowFrame.config(background='red')

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

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break

        if event == "ENTER":
            results(window, False)

            text = window["textInput"].get()
            if text not in ["\n", ""] and keys != [[0]*2, [0]*2]:
                if encrypt:
                    enc = sf.encrypt(text, keys[0][0], keys[0][1])
                    if enc[0] is not False:
                        window["resultTextInfo"].update("Encrypted text:", visible=True)
                        window["resultText"].update(enc[0], visible=True)
                        window["resultBox"].update(visible=True)
                    else:
                        results(window, False)
                        window["infoMsg"].update(enc[1], visible=True)
                else:
                    dec = sf.decrypt(window["textInput"].get(), keys[0][0], keys[1][1])
                    if dec[0] is not False and dec[0] != "":
                        window["resultTextInfo"].update("Decrypted text:", visible=True)
                        window["resultText"].update(dec[0], visible=True)
                        window["resultBox"].update(visible=True)
                    elif dec[0] is False:
                        results(window, False)
                        window["infoMsg"].update(dec[1], visible=True)
            else:
                results(window, False)

    window.close()


def results(window, vis):
    window["resultTextInfo"].update("", visible=vis)
    window["infoMsg"].update("", visible=vis)
    window["resultText"].update("", visible=vis)
    window["resultBox"].update(visible=vis)


def handleInput(window, key):
    userInput = window[key]
    inp = userInput.get()

    if inp.isnumeric():
        if int(inp) <= 0:
            userInput.update(background_color="red")
            return False
        window["userBitInput"].ParentRowFrame.config(background=sg.theme_background_color())
        userInput.update(background_color="lightgreen")
        return True
    else:
        if len(inp) > 1:
            userInput.update(str(inp).rstrip(inp[-1]))
            return True
        else:
            if inp.isnumeric():
                window["userBitInput"].ParentRowFrame.config(background=sg.theme_background_color())
                userInput.update(background_color="lightgreen")
                return True
            else:
                userInput.update("", background_color="white")
                return False
