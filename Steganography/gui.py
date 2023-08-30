import PySimpleGUI as sg
from PIL import Image
import io
import os
from hurry.filesize import size, alternative
import supportFunctions as sf
from supportFunctions import charBits


encode = True
def callWindow():
    global encode
    previewData = None
    freeSpace = 0
    imgLoad = False
    activeImageFile = ""
    defaultEndPoint = "&##&"
    endPoint = defaultEndPoint

    fileTypes = [
        ("PNG (*.png)", "*.png"),
        ("BMP (*.bmp)", "*.bmp")
    ]

    imgL = [[sg.Image(enable_events=True, key="imageBtn")]]
    imgLayout = [[sg.Sizer(0, 700), sg.Column([[sg.Sizer(700, 0)]] + imgL, element_justification='c', pad=(0, 0))]]

    imgInfoLayout = [
        [sg.Text("Image size: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="imgSize")],
        [sg.Text("Image resolution: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="imgRes")],
        [sg.Text("File type: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="imgType")],
        [sg.Text("Path to image: ", font="Arial 15")],
        [sg.Multiline("", border_width=0, size=(100, 2), disabled=True, background_color=sg.theme_background_color(),
                      no_scrollbar=True, font="Arial 15", text_color="black", key="imgPath")
         ]
    ]

    spaceLayout = sg.Column(
        [
            [sg.Text("Can save:", text_color="white", font="Arial 15", key="freeSpaceText"),
             sg.Multiline("XXX chars.", border_width=0, disabled=True, text_color="white",
                          no_scrollbar=True, background_color=sg.theme_background_color(),
                          font="Arial 15", key="freeSpace")]
         ], key="spaceInfo")

    endPointLayout = sg.Column(
        [
            [sg.Text(f"Endpoint: ", text_color="white", font="Arial 15",
                     tooltip=f"Used to mark end of your message while decoding.\nDefault is {defaultEndPoint}."),
             sg.Input(defaultEndPoint, size=(10, 1), font="Arial 15", enable_events=True, key="endpoint")
             ]
        ], key="endPointInfo")

    codeLayout = [
        [sg.Image(filename="encodeBtn.png", enable_events=True, key="encodeBtn"),
         sg.Button("Do magic", font="Arial 18", key="magicBtn")
         ],
        [sg.HorizontalSeparator()],

        [sg.pin(endPointLayout),
         sg.Sizer(700, 0)
         ],
        [sg.pin(spaceLayout),
         sg.Sizer(700, 0)
         ],

        [sg.pin(sg.Column(layout=[
            [sg.Button("Show image", font="Arial 15", key="showNewImageBtn"),
             sg.Button("Change text", font="Arial 15", key="changeTextBtn"),
             sg.FileSaveAs("Save image", target="savePath", file_types=fileTypes, font="Arial 15", key="saveFolder"),
             sg.Input(size=(40, 1), visible=False, enable_events=True, font="Arial 15", key="savePath")
             ]
        ], visible=False, element_justification="c", key="encodeConfigButtons")
        )],

        [sg.pin(sg.Text("Fail", font="Arial 15 bold", text_color="pink", visible=False, key="infoText"))],
        [sg.Text("Message to hide into the image:", font="Arial 15", text_color="black", key="doInfoMessage")],
        [sg.Multiline(size=(700, 200), enable_events=True, font="Arial 15", key="messageInput")]
    ]

    layout = [
        [sg.Text("Welcome in Steganography application.", text_color="black", font=('Arial', 30))],
        [sg.HorizontalSeparator()],

        [
            sg.Text("Image File", font="Arial 15"),
            sg.Input(size=(40, 1), font="Arial 15", enable_events=True, key="dirPathInput"),
            sg.FileBrowse(file_types=fileTypes, font="Arial 15")
        ],
        [sg.Button("Load Image", font="Arial 15", key="loadImageBtn")],

        [sg.Frame("", size=(310, 310), layout=imgLayout, font="Arial 15"),
         sg.Frame("", size=(310, 310), layout=imgInfoLayout, font="Arial 15", element_justification="c")
         ],

        [sg.Frame("", size=(630, 250), layout=codeLayout, font="Arial 15", element_justification="c")],

        [sg.Button("EXIT", font=("Arial", 15))]
    ]

    window = sg.Window('Steganography', layout, element_justification="center", finalize=True)
    while True:
        event, values = window.read(0)

        if values is not None and event is not None:
            if event == "encodeBtn":
                window["encodeConfigButtons"].update(visible=False)
                if encode:
                    encode = False
                    magicInfoUpdate(window)

                    window["encodeBtn"].update(filename="decodeBtn.png")
                    window["doInfoMessage"].update("Message hidden in the image:")
                else:
                    encode = True
                    magicInfoUpdate(window)
                    window["messageInput"].update("")
                    window["encodeBtn"].update(filename="encodeBtn.png")
                    window["doInfoMessage"].update("Message to hide into the image:")

            if imgLoad and (event == "messageInput" or event == "endpoint" or event == "encodeBtn"):
                endPoint = window["endpoint"].get().replace("\n", "").replace(" ", "")
                magicInfoUpdate(window)
                window["encodeConfigButtons"].update(visible=False)
                updateSpace(window, freeSpace, endPoint)

            if event == "messageInput" or event == "endpoint" or event == "encodeBtn" or event == "dirPathInput":
                window["infoText"].update("", visible=False)

            if event == "magicBtn" and imgLoad is False:
                window["infoText"].update("Load the image first!", visible=True)

            if imgLoad and encode is False:
                if event == "magicBtn":
                    endPoint = fixEndpoint(window, endPoint, defaultEndPoint)
                    updateSpace(window, freeSpace, endPoint)

                    msg = sf.decode(activeImageFile, endPoint)
                    if msg[0] is not False:
                        window["messageInput"].update(msg[1])
                    else:
                        window["infoText"].update("Failed to find any message in the image!", visible=True)

            if imgLoad and encode:
                if (event == "magicBtn" or event == "changeTextBtn") and window["messageInput"].get() != "":
                    endPoint = fixEndpoint(window, endPoint, defaultEndPoint)
                    updateSpace(window, freeSpace, endPoint)

                    previewData = sf.encode(activeImageFile, window["messageInput"].get(), endPoint)
                    if previewData[0] is False:
                        window["infoText"].update("Failed to hide message into image!", visible=True)
                        continue

                    if event == "changeTextBtn":
                        window["infoText"].update("", visible=False)
                        window["magicBtn"].update(disabled=False)
                    else:
                        window["magicBtn"].update(disabled=True)

                    window["encodeConfigButtons"].update(visible=not window["encodeConfigButtons"].visible)
                    window["spaceInfo"].update(visible=not window["spaceInfo"].visible)
                    window["endPointInfo"].update(visible=not window["endPointInfo"].visible)
                if (event == "magicBtn" or event == "changeTextBtn") and window["messageInput"].get() == "":
                    window["infoText"].update("Enter any message first.", visible=True)

            if event == "showNewImageBtn" and previewData[0] is not False:
                popup(previewData[1], window, True)

            if event == "savePath":
                window["infoText"].update("", visible=False)
                if previewData[0] is not False and window["savePath"].get() != "":
                    if sf.saveImage(previewData[1], window["savePath"].get()) is False:
                        window["infoText"].update("Failed to save image!", visible=True)
                    else:
                        window["infoText"].update("Image has been saved.", visible=True)

            if event == "loadImageBtn":
                fileName = values["dirPathInput"]
                if os.path.exists(fileName):
                    window["infoText"].update("", visible=False)

                    activeImageFile = fileName
                    imgLoad = True

                    endPoint = fixEndpoint(window, endPoint, defaultEndPoint)
                    window["encodeConfigButtons"].update(visible=False)
                    magicInfoUpdate(window)

                    image = sf.openImage(fileName)
                    if image is False:
                        window["infoText"].update("Failed to open image!", visible=True)
                        continue

                    freeSpace = sf.freeSpace(fileName) // charBits

                    window["imgSize"].update(size(os.stat(fileName).st_size, system=alternative))
                    window["imgRes"].update(str(image.size[0]) + " x " + str(image.size[1]))
                    window["imgType"].update(fileName.split(".")[1])
                    window["imgPath"].update(fileName)
                    updateSpace(window, freeSpace, endPoint)

                    image.thumbnail((300, 300))
                    previewData = io.BytesIO()
                    image.save(previewData, format="PNG")
                    window["imageBtn"].update(data=previewData.getvalue())
                else:
                    window["infoText"].update("Wrong image file!", visible=True)

            if event == "imageBtn":
                popup(activeImageFile, window)

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break

    window.close()


def popup(fileName, window, preview=False):
    if preview is False:
        image = sf.openImage(fileName)
        if image is False:
            return False
    else:
        fileName.seek(0)
        image = Image.open(io.BytesIO(fileName.read()))

    image.thumbnail((window.get_screen_size()[0], window.get_screen_size()[1] - 150))
    bio = io.BytesIO()
    image.save(bio, format="PNG")

    winSize = window.get_screen_size()
    x = (winSize[0] // 2) - (image.size[0] // 2)
    y = (winSize[1] // 2) - (image.size[1] // 2) - 75 // 2

    layout = [
        [sg.Image(data=bio.getvalue())],
    ]
    window = sg.Window("Image viewer", layout, grab_anywhere=True, element_justification="center", location=(x, y),
                       modal=True)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()


def updateSpace(window, freeSpace, endPoint):
    msgSize = len(window["messageInput"].get() + endPoint)
    i = freeSpace - msgSize
    clr = "lightgreen" if i > 0 else "red"
    window["freeSpace"].update(f"{i} chars.", text_color=clr)


def magicInfoUpdate(window):
    window["magicBtn"].update(disabled=False)
    window["endPointInfo"].update(visible=True)
    window["infoText"].update("", visible=False)
    if encode:
        window["messageInput"].update(disabled=False)
        window["spaceInfo"].update(visible=True)
    else:
        window["messageInput"].update("", disabled=True)
        window["spaceInfo"].update(visible=False)
        window["encodeConfigButtons"].update(visible=False)


def fixEndpoint(window, endPoint, defaultEndPoint):
    if endPoint == "":
        endPoint = defaultEndPoint
        window["infoText"].update(f"Endpoint has been set to {defaultEndPoint}!", visible=True)
        window["endpoint"].update(endPoint)

    return endPoint
