from tkinter import * #Imports all tkinter code.
import time, os, json
from tkinter import messagebox
from tkinter import filedialog


#Import local classes
from Python_projects.NotepadTK.src.cryptography import Cryptography
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
        #TODO Check that settings.txt and currentFiles.json exist

        # Use readlines method to get each line
        file = open("settings.txt").readlines()
        self.settingsObject = {}
        for line in file:
            line=line.split()
            #May needed to edit if multiple options are added later
            self.settingsObject[line[0]] = line[1]

    def initUI(self):
        #FORAMT WINDOW
        self.root.configure(bg="#98fb98")
        self.root.title("Emera src")
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
                self.frameInfo[frameName] = {"path": "", "creationDate": currentDate}
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
            #TODO show the farme before the current frame before destroying it (rather than the first frame)
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
            #If no frames are left create a new frame, otherwise load the first frame, TODO swap frame loaded to the one next to the current
            if len(self.frames) == 0:
                self.createWindow("main", "", "")
            else:
                firstFrameName = list(self.frames)[0]
                #Set current frame now since the currentFrame no longer exists (causing key errors down the line)
                self.currentFrame = firstFrameName
                self.show_frame(firstFrameName)

            #If currentFiles.json is not overwritten at the end of the program, then frames need to be removed from it here

    #MANAGE TABS------------
    def createTab(self, frameName):
        #TODO Decide whether tabFrame and children should use self. or not, get frame name to fit inside the tab regardless of length
        #TODO Change colour of the active tab
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

        # TODO Figure out a way to change quit button to red
        # quitImage = PhotoImage(file="quitImage.png")
        # QuitTabButton.config(image=quitImage, activebackground="black")

    def changeActiveTab(self, frameName):
        self.tabs[self.currentFrame].winfo_children()[0].configure(bg=self.settingsObject["tabColour"])
        self.tabs[frameName].winfo_children()[0].configure(bg=self.settingsObject["activeTabColour"])

    # MANAGE FILE OPERATIONS-------------
    def openFile(self):
        #TODO fix error msg when an oponed a file is closed
        #TODO Determine if the file being opened has frameInfo in currentFiles, if it does pass it, otherwise pass ""
        filePath = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

        #fileName = print(os.path.basename(filePath))
        #Extract fileName from path
        pathHead, pathTail = os.path.split(filePath)
        #Create a fileInfo object to pass to self.createWindoe
        frameInfoItem = {"path": filePath, "creationTime": ""}

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
        filePath = filedialog.asksaveasfilename(initialdir="/", title=self.currentFrame,
                                                filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        #If the filePath does not include a file extension then add one
        #TODO Make this work for all file extensions
        if filePath.lower().endswith((".txt", ".log")):
            pass
        else:
            filePath = filePath + ".txt"

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
        #Change frame name
        self.tabs[frameName].winfo_children()[0]["text"] = frameName
        self.currentFrame = frameName

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

    def closePreperations(self):
        #Check if any frames have not been saved
        closeFile = True

        for frameName in self.frames:
            if self.frameInfo[frameName]["path"] == "":
                #If the file is a new file that was created inside the text editor and has no text then assume that file is not important
                if messagebox.askokcancel("Quit", "Are you sure you want to quit, file:{} is not saved".format(frameName)):
                    pass
                else:
                    closeFile = False
        if closeFile:
            file = open("currentFiles.json", "w")
            json.dump(self.frameInfo, file)
            root.destroy()

    def loadLastSession(self):
        #Open file containg fileInfo's of files closed last session
        oldFrameInfo = json.loads(open("currentFiles.json").read())
        for frameName in oldFrameInfo.keys():
            #Check if a loaded file exists, if it doesnt exist warn the user
            if os.path.isfile(oldFrameInfo[frameName]["path"]):
                self.openFileNoDialog(frameName, oldFrameInfo)
                #self.createWindow("main", frameName, oldFrameInfo[frameName])
            else:
                #TODO Load text for files that have been removed
                if messagebox.askyesno("Load last session", "The file {} does not exist anymore, keep it open?".format(frameName)):
                    self.createWindow("main", frameName, oldFrameInfo[frameName])


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
