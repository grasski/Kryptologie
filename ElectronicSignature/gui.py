import PySimpleGUI as sg
import os
import time
from hurry.filesize import size, alternative
import supportFunctions as sf


fileLoad = False
filePath = ""
pubKeyFilePath = ""
zipFilePath = ""
def callWindow():
    global fileLoad, filePath, pubKeyFilePath, zipFilePath
    saveFolder = ""
    doSign = True

    layoutMultiline = lambda k, s, c="black": [
        [sg.Multiline("", border_width=0, size=s, disabled=True, background_color=sg.theme_background_color(),
                      no_scrollbar=True, font="Arial 15", justification="c", text_color=c, key=k)]
    ]

    fileInfoLayout = [
        [sg.Text("File name: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="fileName")],
        [sg.Text("File size: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="fileSize")],
        [sg.Text("File type: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="fileType")],
        [sg.Text("Creation date: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="fileDate")],
        [sg.Text("Path to file: ", font="Arial 15")],
        [sg.Multiline("", border_width=0, size=(100, 2), disabled=True, background_color=sg.theme_background_color(),
                      no_scrollbar=True, font="Arial 15", text_color="black", key="filePath")
         ]
    ]

    zipLayout = [
        [sg.Column(layout=layoutMultiline("verifyZipSignName", (100, 1)))],
        [sg.Sizer(30, 0), sg.HorizontalSeparator(), sg.Sizer(30, 0)],
        [sg.Column(layout=layoutMultiline("verifyZipFileName", (100, 1)))],
    ]

    folderInfoLayout = [
        [sg.Text("Folder name: ", font="Arial 15")],
        [sg.Text("", font="Arial 15", text_color="black", key="folderName")],

        [sg.Text("Public key file: ", font="Arial 15"), sg.FileBrowse("...", target="publicKeyFile",
                                                                      file_types=[("pub (*.pub)", "*.pub")])],
        [sg.Text(visible=False, key="publicKeyFile")],
        [sg.Column(layout=layoutMultiline("publicKeyFileMulti", (100, 1)))],

        [sg.Text("ZIP files: ", font="Arial 15"), sg.FileBrowse("...", target="zipFile",
                                                                file_types=[("zip (*.zip)", "*.zip")])],
        [sg.Text(visible=False, key="zipFile")],
        [sg.pin(sg.Column(layout=zipLayout, visible=True, key="zipLayout"))],
        [sg.pin(sg.Text("", font="Arial 15 bold", text_color="pink", visible=False, key="verifyInfoMessage"))],

        [sg.Text("Path to folder: ", font="Arial 15", key="verifyTextPath")],
        [sg.Multiline("", border_width=0, size=(100, 2), disabled=True, background_color=sg.theme_background_color(),
                      no_scrollbar=True, font="Arial 15", text_color="black", key="folderPath")
         ]
    ]

    setupLayout = [
        [sg.Image(filename="signBtn.png", enable_events=True, key="toggleBtn"),
         sg.Input(visible=False, enable_events=True, key="pathInput"),
         sg.pin(sg.FileBrowse(button_text="Browse file", visible=True, font="Arial 15", target="pathInput",
                              key="fileBtn")),
         sg.pin(sg.FolderBrowse(button_text="Browse folder", visible=False, font="Arial 15", target="pathInput",
                                key="folderBtn")),
         sg.Button("Reset", enable_events=True, font="Arial 15", key="resetBtn")
         ],
        [sg.pin(sg.Frame("", size=(310, 360), visible=True, layout=fileInfoLayout, font="Arial 15",
                         element_justification="c", key="fileInfoLayout"))],
        [sg.pin(sg.Frame("", size=(310, 360), visible=False, layout=folderInfoLayout, font="Arial 15",
                         element_justification="c", key="folderInfoLayout"))]
    ]

    signLayout = [
        [sg.Sizer(20, 0), sg.FolderBrowse("Select folder", target="folderInput", enable_events=True, font="Arial 20",
                                          key="folderBtn")
         ],

        [sg.Input(enable_events=True, visible=False, key="folderInput")],
        [sg.pin(sg.Multiline(size=(38, 2), disabled=True, font="Arial 15", enable_events=True,
                             visible=False, background_color=sg.theme_background_color(),
                             border_width=1, no_scrollbar=True, key="savingFolderPath"))
         ],
        [sg.Sizer(20, 0), sg.Button("Sign and Save", font="Arial 20", disabled=True, key="signBtn")],
        [sg.Sizer(20, 0), sg.pin(sg.Text("", font="Arial 15 bold", visible=False, key="signResultText"))]
    ]

    verifyLayout = [
        [sg.Button("Verify", font="Arial 20", key="verifyBtn")],
        [sg.pin(sg.Column(layout=layoutMultiline("verifyResultText", (20, 2), "white"), justification="c"))]
    ]

    resultLayout = [
        [sg.pin(sg.Column(layout=signLayout, justification="c", element_justification="c", visible=True,
                          key="signLayout"))],
        [sg.pin(sg.Column(layout=verifyLayout, justification="c", element_justification="c", visible=False,
                          key="verifyLayout"))]
    ]

    layout = [
        [sg.Text("Welcome in Electronic Signature application.", text_color="black", font=('Arial', 30))],
        [sg.HorizontalSeparator()],

        [sg.Column(layout=setupLayout, justification="c", element_justification="c"),
         sg.pin(sg.Column(layout=resultLayout, justification="c", element_justification="c", visible=False,
                          key="resultLayout"))],

        [sg.Button("EXIT", font=("Arial", 15))]
    ]

    window = sg.Window('ElectronicSignature', layout, element_justification="center", finalize=True)
    while True:
        event, values = window.read(0)

        if values is not None and event is not None:
            if window["publicKeyFile"].get() != "":
                window["folderName"].update("")
                window["folderPath"].update(zipFilePath)
                window["zipLayout"].update(visible=True)
                window["verifyInfoMessage"].update("", visible=False)
                window["verifyResultText"].update("", visible=False)
                window["verifyTextPath"].update("Path to zip:")

                pubKeyFilePath = window["publicKeyFile"].get()
                window["publicKeyFileMulti"].update(pubKeyFilePath)
                window["publicKeyFile"].update("")

            if window["zipFile"].get() != "":
                window["folderName"].update("")
                window["verifyInfoMessage"].update("", visible=False)
                window["verifyResultText"].update("", visible=False)
                window["verifyTextPath"].update("Path to zip:")

                zipFilePath = window["zipFile"].get()
                window["folderPath"].update(zipFilePath)
                zipFiles = sf.getZipFiles(zipFilePath)
                zipInfo(window, zipFiles)
                window["zipFile"].update("")

            if event == "toggleBtn":
                window["folderInfoLayout"].update(visible=not window["folderInfoLayout"].visible)
                window["fileInfoLayout"].update(visible=not window["fileInfoLayout"].visible)
                window["fileBtn"].update(visible=not window["fileBtn"].visible)
                window["folderBtn"].update(visible=not window["folderBtn"].visible)
                window["verifyTextPath"].update("Path to folder:")

                doSign = not doSign
                window["signLayout"].update(visible=doSign)
                window["verifyLayout"].update(visible=not doSign)
                if doSign is False:
                    window["toggleBtn"].update(filename="verifyBtn.png")
                else:
                    window["toggleBtn"].update(filename="signBtn.png")

            if event == "pathInput":
                window["signResultText"].update("", visible=False)
                window["verifyResultText"].update("", visible=False)
                window["verifyTextPath"].update("Path to folder:")

                filePath = window["pathInput"].get()
                window["pathInput"].update("")
                if filePath != "":
                    if doSign:
                        fileName = os.path.basename(filePath)
                        window["fileName"].update(os.path.splitext(fileName)[0])
                        window["fileSize"].update(size(os.stat(filePath).st_size, system=alternative))
                        window["fileType"].update(os.path.splitext(filePath)[1])
                        window["fileDate"].update(time.ctime(os.path.getctime(filePath)))
                        window["filePath"].update(filePath)
                        fileLoad = True
                    else:
                        folderFiles = sf.getFolderFiles(filePath)
                        if folderFiles[0] is not False:
                            pubKeyFilePath = folderFiles[1][0]
                            zipFilePath = folderFiles[1][1]

                            folderName = os.path.basename(filePath)
                            window["folderName"].update(folderName)
                            window["folderPath"].update(filePath)
                            window["publicKeyFileMulti"].update(pubKeyFilePath)
                            zipInfo(window, sf.getZipFiles(zipFilePath))

                            pubKeyFilePath = filePath + "/" + pubKeyFilePath
                        else:
                            reset(window)
                            window["verifyInfoMessage"].update(folderFiles[1], visible=True)

            if event == "resetBtn" or event == "toggleBtn":
                reset(window)

            if fileLoad:
                window["resultLayout"].update(visible=True)
            elif pubKeyFilePath != "" and zipFilePath != "":
                window["resultLayout"].update(visible=True)
            else:
                window["resultLayout"].update(visible=False)
                saveFolder = ""

            if event == "folderInput":
                window["signResultText"].update("", visible=False)
                window["verifyResultText"].update("", visible=False)

                saveFolder = window["folderInput"].get()
                if saveFolder != "":
                    window["savingFolderPath"].update(saveFolder, visible=True)

            if saveFolder != "":
                window["signBtn"].update(disabled=False)
            else:
                window["signBtn"].update(disabled=True)

            if filePath != "" and saveFolder != "":
                if event == "signBtn":
                    window["signResultText"].update("Signing ...", text_color="white", visible=True)
                    window.read(0)
                    signed = sf.sign(filePath, saveFolder)
                    clr = "lightgreen" if "successfully" in signed[1] else "pink"
                    window["signResultText"].update(signed[1], text_color=clr, visible=True)

            if event == "verifyBtn":
                window["verifyResultText"].update("Verifying ...", text_color="white", visible=True)
                window.refresh()
                verify = sf.verify(pubKeyFilePath, zipFilePath)
                clr = "lightgreen" if "original" in verify[1] else "pink"
                window["verifyResultText"].update(verify[1], text_color=clr, visible=True)

        if event == "EXIT" or event == sg.WIN_CLOSED:
            break

    window.close()


def reset(window):
    global fileLoad, filePath, pubKeyFilePath, zipFilePath
    fileLoad = False
    filePath = ""
    pubKeyFilePath = ""
    zipFilePath = ""

    window["signResultText"].update("", visible=False)
    window["verifyResultText"].update("", visible=False)
    # File/Sign layout
    window["fileName"].update("")
    window["fileSize"].update("")
    window["fileType"].update("")
    window["fileDate"].update("")
    window["filePath"].update("")
    window["savingFolderPath"].update("", visible=False)
    # Folder/Verify layout
    window["folderName"].update("")
    window["folderPath"].update("")
    window["zipFile"].update("")
    window["zipLayout"].update(visible=True)
    window["verifyInfoMessage"].update("", visible=False)
    window["verifyZipSignName"].update("")
    window["verifyZipFileName"].update("")
    window["publicKeyFileMulti"].update("")
    window["publicKeyFile"].update("")
    window["verifyTextPath"].update("Path to folder:")


def zipInfo(window, files):
    global pubKeyFilePath, zipFilePath
    if files[0] is not False:
        window["zipLayout"].update(visible=True)
        window["verifyInfoMessage"].update("", visible=False)
        window["verifyZipSignName"].update(files[1][0])
        window["verifyZipFileName"].update(files[1][1])
    else:
        pubKeyFilePath = ""
        zipFilePath = ""
        window["zipLayout"].update(visible=False)
        window["verifyInfoMessage"].update(files[1], visible=True)
