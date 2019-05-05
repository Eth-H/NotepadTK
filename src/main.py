from tkinter import * #Imports all tkinter code.
import time, os, json
from tkinter import messagebox
from tkinter import filedialog


#Import local classes
from src.cryptography import Cryptography
#TODO Add functionality for keeping deleted files stored temporarily
#TODO: create cryptogrpahy functions, add new menu items and functionality
#https://pythonspot.com/tk-file-dialogs/

class ContainerWindow:
    def __init__(self, parent):
        self.parent = parent
        self.root = root
        self.loadSettings()
        self.initUI()

    def loadSettings(self):
        #settings.txt -> settings for current installation, currentInstance.txt -> Contains info on the current session being run, currentFiles.json -> Contains a frameInfo instance from the last time the program was closed


        #Check if settings.txt file and currentFiles.json exist
        if not os.path.isfile("./settings.txt"):
            file = open("settings.txt", "w")
            defaultSettings = "mainThemeColor LightGreen\ntabColour white\nactiveTabColour Yellow\naskUnsavedTabsOnClose CheckEach\n"
            file.writelines(defaultSettings)
            file.close()

        if not os.path.isfile("./currentInstance.json"):
            defaultInstanceParameters = {"lastPathUsed": "/"}
            self.updateCurrentInstanceJSON(defaultInstanceParameters)


        if not os.path.isfile("./currentFiles.json"):
            file = open("currentFiles.json","w")
            file.close()

        # Use readlines method to get each line
        file = open("settings.txt").readlines()
        self.settingsObject = {}
        for line in file:
            line=line.split()
            #If line is empty pass
            if len(line) == 0:
                pass
            else:
                self.settingsObject[line[0]] = line[1]

        self.currentInstanceObject = json.loads(open("currentInstance.json").read())
        print(self.currentInstanceObject)

    def initUI(self):
        #FORAMT WINDOW
        self.root.configure(bg="#98fb98")
        self.root.title("NotepadTK")
        self.root.minsize(500, 500)

        #CREATE MENU
        self.menubar = Menu(root)  # Make a menu.
        self.root.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.openFile)
        self.filemenu.add_command(label="Save", command=self.saveFile)
        self.filemenu.add_command(label="Save As", command=self.saveAsFile)
        self.filemenu.add_command(label="New", command=lambda: self.createWindow("main", "", ""))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)  # Attached to a parent window instead of a toplevel window

        # create more pulldown menus
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Cut", command=self.hello)
        self.editmenu.add_command(label="Copy", command=self.hello)
        self.editmenu.add_command(label="Paste", command=self.hello)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.windowMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window", menu=self.windowMenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.hello)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.toolsMenu = Menu(self.menubar, tearoff=0)
        #Add sub menuas menu item
        self.cryptographyMenu = Menu(self.toolsMenu, tearoff=0)
        self.cryptographyMenu.add_command(label="Hash", command=lambda: Cryptography.hashDialog(self))
        self.cryptographyMenu.add_command(label="Encryption", command=lambda: Cryptography.encryptionDialog(self))
        self.toolsMenu.add_cascade(label="Cryptography", menu=self.cryptographyMenu)
        #Add normal menu item
        self.toolsMenu.add_command(label="About tools", command=self.hello)
        self.menubar.add_cascade(label="Tools", menu=self.toolsMenu)

        #CREATE TABBAR
        self.tabBar = Frame(root, borderwidth=1, relief='raised', bg=self.settingsObject["mainThemeColor"])
        self.tabBar.pack(side=TOP, fill= X)
        #Tab JSON, EG frameName: tabFrameObject
        self.tabs = {}

        #CREATE BASE FRAME
        self.baseFrame = Frame(root)
        self.baseFrame.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.baseFrame.grid_rowconfigure(0, weight=1)
        self.baseFrame.grid_columnconfigure(0, weight=1)

        #Create JSON of all frames, EG frameName: frameObject
        self.frames = {}
        #Contain meta data on frames, EG frameName: {path: "", date: ""}
        self.frameInfo = {}
        # Create current name to identity which frame is current open (to operate specific commands on)
        self.currentFrame = ""

        #Load files left open in the last session
        self.loadLastSession()

        #Create the first frame if no fames where loaded
        if len(self.frames) == 0:
            self.createWindow("main", "", "")



    #MANAGE FRAMES-------------------
    def show_frame(self, frameName):
        # Raise wanted frame to the top
        frame = self.frames[frameName]
        frame.tkraise()
        #If only one frame exists, then sets current frame before changing active tab to counteract reference errors
        if len(self.frames) == 1:
            self.currentFrame=frameName
        self.changeActiveTab(frameName)
        self.currentFrame = frameName

    #Create windows from their class templates, some windows are imported from other files
    def createWindow(self, windowTitle, frameName, frameInfoItem):
        if windowTitle == "main":
            #Create mainWindowFrame with parent baseFrame -> Set a class to derive from mainWindowFrame ->
            # grid all of mainWindowFrames widgets to it from its derived class -> then grid the mainWindowFrame to the baseFrame
            self.mainWindowFrame = Frame(self.baseFrame)
            self.mainWindow = MainWindow(self.mainWindowFrame, self)
            #mainWindow is grided to mainWindowFrame
            self.mainWindow.grid(row=0, column=0, sticky="nesw")
            #mainWindowFrame is grided to baseFrame, it can now be switched with the desireded Window Frame
            self.mainWindowFrame.grid(row=0, column=0, sticky="nesw")
            #Decide on the name of the window, if it has no name give a random name
            if frameName != "":
                self.frames[frameName] = self.mainWindowFrame
            else:
                #Make sure random name is not taken
                frameName = "new {}".format(len(self.frames)+1)
                self.frames[frameName] = self.mainWindowFrame

            # Create metadata for use (EG reopen files when the program next starts)
            currentDate = time.strftime('%d-%m-%Y')
            #If no frameInfo was passed give it default values, otherwise assume old fileInfo
            if frameInfoItem == "":
                self.frameInfo[frameName] = {"path": "", "creationDate": currentDate, "windowType": "text"}
            else:
                self.frameInfo[frameName] = frameInfoItem
            # Add frame to menu so that it can be switched too
            self.windowMenu.add_command(label=frameName, command=lambda: self.show_frame(frameName))
            #Create a tab for the frame:
            self.createTab(frameName)

            #Set current frame, this method also sets current tab
            self.show_frame(frameName)
        """
        elif windowTitle == "CryptographyWindow":
            self.cryptWindowFrame = Frame(self.baseFrame)
            self.cryptWindow = CryptWindow(self.cryptWindowFrame, self)
            # mainWindow is grided to mainWindowFrame
            self.cryptWindow.grid(row=0, column=0, sticky="nesw")
            # mainWindowFrame is grided to baseFrame, it can now be switched with the desireded Window Frame
            self.cryptWindowFrame.grid(row=0, column=0, sticky="nesw")
            self.frames[CryptWindow] = self.cryptWindowFrame
            # Add frame to menu so that it can be switched too
            self.windowMenu.add_command(label="HashWindow", command=lambda: self.show_frame(CryptWindow))
        """
        #print(self.baseFrame.winfo_children())

    def removeFrame(self, frameName):
        # currentFrameText = self.frames[self.currentFrame].winfo_children()[1].get(1.0, END)
        #Check if the frame is saved
        removeFrame = True
        if self.frameInfo[frameName]["path"] == "":
            if messagebox.askokcancel("Quit", "Are you sure you want to quit, file:{} is not saved".format(frameName)):
                pass
            else:
                removeFrame = False
        #Remove the frame completely from the application
        if removeFrame:
            #Remove from GUI
            self.frames[frameName].grid_forget()
            self.tabs[frameName].pack_forget()
            #Remove from menu
            self.windowMenu.delete(frameName)
            #Remove from JSON data
            del self.frames[frameName]
            del self.frameInfo[frameName]
            del self.tabs[frameName]

            #Set next frame
            #If no frames are left create a new frame, otherwise load the first frame
            if len(self.frames) == 0:
                self.createWindow("main", "", "")
            else:
                firstFrameName = list(self.frames)[-1]
                #Set current frame now since the currentFrame no longer exists (causing key errors down the line)
                self.currentFrame = firstFrameName
                self.show_frame(firstFrameName)

            #If currentFiles.json is not overwritten at the end of the program, then frames need to be removed from it here

    #MANAGE TABS------------
    def createTab(self, frameName):
        #Create a frame
        tabFrame = Frame(self.tabBar, bg=self.settingsObject["activeTabColour"])
        tabFrame.pack(side=LEFT)
        #ChangeWindowButton = Button(tabFrame, text=frameName, command=lambda: self.show_frame(frameName))
        #ChangeWindowButton.pack(side=LEFT)

        ChangeWindowLabel = Label(tabFrame, text=frameName)
        ChangeWindowLabel.pack(side=LEFT)
        ChangeWindowLabel.bind("<Button-1>", lambda e: self.show_frame(frameName))

        QuitTabButton = Button(tabFrame, bg="red", command=lambda: self.removeFrame(frameName))
        QuitTabButton.pack(side=RIGHT)
        self.tabs[frameName] = tabFrame

        # quitImage = PhotoImage(file="quitImage.png")
        # QuitTabButton.config(image=quitImage, activebackground="black")

    def changeActiveTab(self, frameName):
        self.tabs[self.currentFrame].winfo_children()[0].configure(bg=self.settingsObject["tabColour"])
        self.tabs[frameName].winfo_children()[0].configure(bg=self.settingsObject["activeTabColour"])

    # MANAGE FILE OPERATIONS-------------
    def openFile(self):
        filePath = filedialog.askopenfilename(initialdir=self.currentInstanceObject["lastPathUsed"], title="Select file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        #fileName = print(os.path.basename(filePath))
        #Extract fileName from path
        pathHead, pathTail = os.path.split(filePath)
        #Remember the last directory the program was in, so next time you interact with the file system you start there
        self.currentInstanceObject["lastPathUsed"] = pathHead
        #Create a fileInfo object to pass to self.createWindow
        frameInfoItem = {"path": filePath, "creationTime": "", "windowType": "text"}

        #Open the file and write its contents to a new frame
        try:
            #Open file and create a new window with relevant details
            file = open(filePath, "r")
            self.createWindow("main", pathTail, frameInfoItem)
            #Write text
            self.frames[self.currentFrame].winfo_children()[1].insert(END, file.read())
        except(IOError):
            messagebox.showerror("Open file", "Path error")

    #When opening files when loading last session
    def openFileNoDialog(self, frameName, oldFrameInfo):
        try:
            #Open file and create a new window with relevant details
            file = open(oldFrameInfo[frameName]["path"], "r")
            self.createWindow("main", frameName, oldFrameInfo[frameName])
            #Write text
            self.frames[self.currentFrame].winfo_children()[1].insert(END, file.read())
        except(IOError):
            messagebox.showerror("Open file", "Path error")


    def saveAsFile(self):
        #TODO Fix saveAs problems when clicking anouther tab and then clicking back
        #Get the user to chose a location (to generate a path)
        filePath = filedialog.asksaveasfilename(initialdir=self.currentInstanceObject["lastPathUsed"], title=self.currentFrame,
                                                filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        #If the user presses quit rather than exiting, exit the function
        if len(filePath) == 0:
            return None
        #If the filePath does not include a file extension then add one
        #TODO Make this work for all file extensions
        pathHead, pathTail = os.path.split(filePath)
        self.currentInstanceObject["lastPathUsed"] = pathHead

        currentFrameText = self.frames[self.currentFrame].winfo_children()[1].get(1.0, END)
        try:
            file = open(filePath, "w")
            file.write(currentFrameText)
            file.close()
            self.frameInfo[self.currentFrame]["path"] = filePath
            #Extract file name from path and change throughout frame
            pathHead, pathTail = os.path.split(filePath)
            self.changeFrameName(pathTail)
        except:
            messagebox.showerror("Save Error", "Incorrect path or file position")

    def changeFrameName(self, frameName):
        #Update frameName in each JSON using old currentFrame and then set currentFrame to new frameName
        self.frames[frameName] = self.frames.pop(self.currentFrame)
        self.frameInfo[frameName] = self.frameInfo.pop(self.currentFrame)
        self.tabs[frameName] = self.tabs.pop(self.currentFrame)

        #Update tabs, change tab binded method (so that when the tab is clicked it doesnt look for the old frameName )
        self.tabs[frameName].winfo_children()[0]["text"] = frameName
        self.tabs[frameName].winfo_children()[0].unbind("<Button-1>")
        self.tabs[frameName].winfo_children()[0].bind("<Button-1>", lambda e: self.show_frame(frameName))
        #Finally set old currentFrame to the new frame name
        self.currentFrame = frameName

        #ChangeWindowLabel.bind("<Button-1>", lambda e: self.show_frame(frameName))

    def saveFile(self):
        #If file does not exist
        if self.frameInfo[self.currentFrame]["path"] == "":
            self.saveAsFile()
        else:
            try:
                file = open(self.frameInfo[self.currentFrame]["path"], "w")
                file.write(self.frames[self.currentFrame].winfo_children()[1].get(1.0, END))
                file.close()
            except:
                messagebox.showerror("Save Error", "Incorrect path or file position")
    ### Methods related to closing the program ----------
    def closePreperations(self):
        #Check if any frames have not been saved
        closeFile = True
        #Check if the user wants to use check for unsaved tabs on exit
        unwantedUnsavedFrames = []
        if self.settingsObject["askUnsavedTabsOnClose"] == "CheckEach":
            for frameName in self.frames:
                self.currentFrame = frameName
                #If a file has no text then it wasnt saved
                if self.frameInfo[frameName]["path"] == "":
                    #If the file is a new file that was created inside the text editor and has no text then assume that file is not important
                    if len(self.frames[frameName].winfo_children()[1].get(1.0, END)) > 1:
                        #If yes save the file (self.currentFrame used to select it), otherwise remove from currentFrames.json so the editor doesnt try to open it on startup
                        if messagebox.askyesno("Save file {}?".format(frameName)):
                            self.saveAsFile()
                        else:
                            unwantedUnsavedFrames.append(frameName)
                    else:
                        unwantedUnsavedFrames.append(frameName)
            #Update frameInfo contained in currentFiles.json and close program
            self.closeProgram(unwantedUnsavedFrames)
            # End program
        #TODO add a dialog box that asks the user what files they want to close
        elif self.settingsObject["askUnsavedTabsOnClose"] == "List":
            unsavedFrames = []
            for frameName in self.frames:
                if self.frameInfo[frameName]["path"] == "":
                    unsavedFrames.append(frameName)
            self.checkUnsavedTabsDialog(unsavedFrames)
        #If setting is not a selected option, assume the user doesnt want them to be saved, discard and remove all unsaved frames
        else:
            for frameName in self.frames:
                if self.frameInfo[frameName]["path"] == "":
                    unwantedUnsavedFrames.append(frameName)
            self.closeProgram(unwantedUnsavedFrames)

    #When the askUnsavedTabsOnClose is set to List in settings.txt, a dialog is loaded with all the currently unsaved frames
    def checkUnsavedTabsDialog(self, unsavedFrames):
        saveFileDialog = Toplevel()
        saveFileDialog.grab_set()
        saveFileDialog.configure(bg=self.settingsObject["mainThemeColor"])
        self.SFDlistBoxLabel = Label(saveFileDialog, text="Chose files to save")
        self.SFDlistBoxLabel.grid(row=0, column=0)
        self.SFDoptions = StringVar()
        self.SFDoptions.set(unsavedFrames)
        self.SFDlistBox = Listbox(saveFileDialog, listvariable=self.SFDoptions, exportselection=0,
                                  selectmode=MULTIPLE, font=("Trebuchet MS", 10), width=50)
        self.SFDlistBox.grid(row=1, column=0)
        self.saveSelected = Button(saveFileDialog, text="Save selected files",
                               command=lambda: self.saveSelectedFrames(saveFileDialog, unsavedFrames))
        self.saveSelected.grid(row=4, column=0)
        self.saveNone = Button(saveFileDialog, text="Just delete all files", bg="red",
                               font=("Trebuchet MS", 10, 'bold'),
                               command=lambda: self.closeProgram(unsavedFrames))
        self.saveNone.grid(row=4, column=3)

    def saveSelectedFrames(self, saveFileDialog, unsavedFrames):
        self.SFDlistBoxSelectedList = []
        selection = self.SFDlistBox.curselection()
        if len(selection) == 0:
            pass
        else:
            for i in selection:
                entrada = self.SFDlistBox.get(i)
                self.SFDlistBoxSelectedList.append(entrada)
            #Save the files selected
            for frameName in self.SFDlistBoxSelectedList:
                self.currentFrame = frameName
                self.saveAsFile()
            saveFileDialog.grab_release()
            saveFileDialog.destroy()
        #Build a list of items not selected
        unwantedUnsavedFrames = []
        for frameName in unsavedFrames:
            if frameName not in self.SFDlistBoxSelectedList:
                unwantedUnsavedFrames.append(frameName)
        self.closeProgram(unwantedUnsavedFrames)

    #Writes any data needed for the next session to the file system then closes the program completely
    def closeProgram(self, unwantedUnsavedFrames):
        self.updateCurrentFramesJSON(self.frameInfo, unwantedUnsavedFrames)
        self.updateCurrentInstanceJSON(self.currentInstanceObject)
        root.destroy()
    ### ----------

    def loadLastSession(self):
        #Open file containg fileInfo's of files closed last session
        oldFrameInfo = json.loads(open("currentFiles.json").read())
        unwantedUnsavedFiles = []
        for frameName in oldFrameInfo.keys():
            #Check if a loaded file exists, if it doesnt exist warn the user
            if os.path.isfile(oldFrameInfo[frameName]["path"]):
                self.openFileNoDialog(frameName, oldFrameInfo)
                #self.createWindow("main", frameName, oldFrameInfo[frameName])
            else:
                #TODO Load text for files that have been removed
                if messagebox.askyesno("Load last session", "The file {} does not exist anymore or has been moved, keep it open?".format(frameName)):
                    self.createWindow("main", frameName, oldFrameInfo[frameName])
                else:
                    #Add to list of files to remove from currentFiles.json
                    unwantedUnsavedFiles.append(frameName)
        self.updateCurrentFramesJSON(oldFrameInfo, unwantedUnsavedFiles)

    #Get rid of frames from currentFiles.json when they don't exist in the current application instance, should be called during opening and closing of the program (frameInfo doesnt need to be edited since the program will be closed)
    def updateCurrentFramesJSON(self, frameInfo, framesToRemove):
        #Format frameInfo instance to reflect changes
        for frameName in framesToRemove:
            del frameInfo[frameName]
        #Write changes
        file = open("currentFiles.json", "w")
        json.dump(frameInfo, file)
        file.close()

    def updateCurrentInstanceJSON(self, currentInstanceObject):
        file = open("currentInstance.json", "w")
        json.dump(currentInstanceObject, file)
        file.close()

    #MENU OPERATIONS------
    def hello(self):
        print("Hello")

#Inherits from tk.Frame
class MainWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self ,parent)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        #Create text
        self.mainTextBox = Text(parent, borderwidth=3, relief="sunken")
        #self.mainTextBox.pack(side=TOP, fill=BOTH, expand=True)
        self.mainTextBox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        #Create vertical scrollbar and attach to text
        self.verticalScrollbar = Scrollbar(parent, orient=VERTICAL, command=self.mainTextBox.yview)
        self.verticalScrollbar.grid(row=0, column=1, sticky='nsew')
        self.mainTextBox['yscrollcommand'] = self.verticalScrollbar.set

        #Create horizontal scrollbar and attach to text
        self.horizontalScrollbar = Scrollbar(parent, orient=HORIZONTAL, command=self.mainTextBox.xview)
        self.horizontalScrollbar.grid(row=1, column=0, sticky='nsew')
        self.mainTextBox['xscrollcommand'] = self.horizontalScrollbar.set


        #button1 = Button(self, text="Visit page 1",command=lambda: controller.show_frame(PageOne))
        #button1.pack()




root = Tk()  # Creates the root window for the application.
window = ContainerWindow(root)  # Creates an object
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
#                                   root.winfo_screenheight()))
#When the user closes the app call this function
root.protocol("WM_DELETE_WINDOW", window.closePreperations)
root.mainloop()
