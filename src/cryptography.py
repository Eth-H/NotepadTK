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
        elif operation == "encryption":
            self.initUI_encryptionFrame()

    def initUI_hashFrame(self):

        #Hash algorithm selection
        #Inform the user of the currently selected algorithm
        self.currentHashAlgorithm = StringVar()
        self.currentHashAlgorithm.set("md5")
        self.currentHashAlgorithmLabel = Label(self,
                                               textvariable=self.currentHashAlgorithm)
        self.currentHashAlgorithmLabel.grid(row=0, column=0)
        #Allow the user to select a hash

        self.hashAlgorithms = StringVar()
        self.hashAlgorithms.set(['md5', 'sha1', 'sha2', 'sha256'])
        self.choseAlgorihmLB = Listbox(self, listvariable=self.hashAlgorithms)
        #for i in hashAlgorithms:
        #    self.choseAlgorihmLB.insert(END, i)
        self.choseAlgorihmLB.bind("<<ListboxSelect>>", lambda: self.onSelect)
        self.choseAlgorihmLB.grid(row=1, column=3)

        self.calculateHashButton = Button(self, text="Calculate hash", command=lambda: self.calculateHashes())
        self.calculateHashButton.grid(row=0, column=4)

        self.hashInput = Entry(self, text="")
        self.hashInput.grid(row=4, column=0)
        self.hashOutput = Entry(self, text="")
        self.hashOutput.grid(row=4, column=1)

        self.hashInput1 = Entry(self, text="")
        self.hashInput1.grid(row=5, column=0)
        self.hashOutput1 = Entry(self, text="")
        self.hashOutput1.grid(row=5, column=1)

        self.hashInput2 = Entry(self, text="")
        self.hashInput2.grid(row=6, column=0)
        self.hashOutput2 = Entry(self, text="")
        self.hashOutput2.grid(row=6, column=1)

        self.hashJSON = {"hash": [self.hashInput, self.hashOutput], "hash1": [self.hashInput1, self.hashOutput1], "hash2": [self.hashInput2, self.hashOutput2]}


    #Update currentHashAlgorithm after a listbox selection
    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.currentHashAlgorithm.set(value)

    #Calculate hashes for each input widget and insert into output widget
    def calculateHashes(self):
        for hashGroup in self.hashJSON.keys():
            print(hashGroup)
            print("{}".format(self.hashJSON[hashGroup][0].get()))
            self.hashJSON[hashGroup][1].delete(0,END)
            self.hashJSON[hashGroup][1].insert(0, self.calculateHash(self.currentHashAlgorithm.get(), self.hashJSON[hashGroup][0].get()))

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

