from tkinter import *
import hashlib
#Inherits from tk.Frame

class Cryptography(Frame):
    def __init__(self, parent, operation):
        Frame.__init__(self, parent)
        self.parent = parent

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        if operation == "hash":
            self.initUI_hashFrame()
            self.hashLabel = Label(parent, text="Nice lookin hash label")
            self.hashLabel.grid(row=0, column=0)
        elif operation == "encryption":
            self.initUI_encryptionFrame()

    def initUI_hashFrame(self):
        print("Hash frame")

        #Hash algorithm selection
        #Inform the user of the currently selected algorithm
        self.currentHashAlgorithm = StringVar()
        self.currentHashAlgorithmLabel = Label(self, text=self.currentHashAlgorithm,
                                               textvariable=self.currentHashAlgorithm)
        self.currentHashAlgorithmLabel.grid(x=0, y=0)
        #Allow the user to select a hash
        hashAlgorithms = ['md5', 'sha1', 'sha2', 'sha256']
        self.choseAlgorihmLB = Listbox(self.parent, listvariable=hashAlgorithms)
        #for i in hashAlgorithms:
        #    self.choseAlgorihmLB.insert(END, i)
        self.choseAlgorihmLB.bind("<<ListboxSelect>>", self.onSelect)
        self.choseAlgorihmLB.grid(x=0, y=0)

        self.calculateHashButton = Button(self.parent, text="Calculate hash", command=lambda: self.calculateHashes())

        self.hashInput = Entry(self.parent, text="")
        self.hashInput.grid(x=0, y=3)
        self.hashOutput = Entry(self.parent, text="")
        self.hashOutput.grid(x=3, y=3)

        self.hashInput1 = Entry(self.parent, text="")
        self.hashInput1.grid(x=0, y=4)
        self.hashOutput1 = Entry(self.parent, text="")
        self.hashOutput1.grid(x=3, y=4)

        self.hashInput2 = Entry(self.parent, text="")
        self.hashInput2.grid(x=0, y=5)
        self.hashOutput2 = Entry(self.parent, text="")
        self.hashOutput2.grid(x=3, y=5)

        self.hashJSON = {"hash": [self.hashInput, self.hashOutput], "hash1": [self.hashInput1, self.hashOutput1], "hash2": [self.hashInput2, self.hashOutput]}
    #Update currentHashAlgorithm after a listbox selection
    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.currentHashAlgorithm.set(value)

    #Calculate hashes for each input widget and insert into output widget
    def calculateHashes(self):
        #TODO iterate self.hashJSON calculate hash for each hashInput and insert into hashOutput text
        for hashInp in self.hashInputList:
            hashInp["text"] = self.calculateHash(self.currentHashAlgorithm, hashInp.get())

    #Calculate hash using passed algorithm and data
    def calculateHash(self, hashAlgorithm, data):
        h = hashlib.new(hashAlgorithm)
        h.update(data.encode("utf-8"))
        return h.hexdigest()
        #print(hashlib.new(hashAlgorithm, data.encode('utf-8')).hexdigest())


    def initUI_encryptionFrame(self):
        print("Encryption frame")







    #TODO Add optional hash and encryption dialogs if user doesn't want to create a frame
    def hashDialog(self):
        self.hashDialog = Toplevel()
        self.hashDialog.title = "Hash"
    def encryptionDialog(self):
        self.encryptionDialog = Toplevel()
        self.encryptionDialog.title = "Hash"

