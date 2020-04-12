from tkinter import *
import hashlib

# Inherits from tk.Frame


class Cryptography(Frame):
    def __init__(self, parent, operation):
        Frame.__init__(self, parent)
        self.parent = parent
        for i in range(12):
            self.rowconfigure(i, pad=0, weight=1, minsize=1)
            self.columnconfigure(i, pad=0, weight=1)
        if operation == "hash":
            self.initUI_hashFrame()
        elif operation == "encryption":
            self.initUI_encryptionFrame()

    def initUI_hashFrame(self):
        # Hash algorithm selection
        # Inform the user of the currently selected algorithm
        self.hashCalculateLabel = Label(
            self, text="Calculate hash", font=("Trebuchet MS", 10)
        )
        self.hashCalculateLabel.grid(row=0, column=0, sticky="nesw")
        self.currentHashAlgorithm = StringVar()
        self.currentHashAlgorithm.set("md5")
        self.currentHashAlgorithmLabel = Label(
            self, textvariable=self.currentHashAlgorithm
        )
        self.currentHashAlgorithmLabel.grid(row=1, column=0)
        # Allow the user to select a hash

        self.hashAlgorithms = StringVar()
        self.hashAlgorithms.set(["md5", "sha1", "sha2", "sha256"])
        self.choseAlgorihmLB = Listbox(self, listvariable=self.hashAlgorithms)
        # for i in hashAlgorithms:
        #    self.choseAlgorihmLB.insert(END, i)
        self.choseAlgorihmLB.bind("<<ListboxSelect>>", self.onSelect)
        self.choseAlgorihmLB.grid(row=2, column=0, sticky="nesw")

        self.calculateHashButton = Button(
            self, text="Calculate hash", command=self.calculateHashes
        )
        self.calculateHashButton.grid(row=1, column=1)
        # self.calculateHashErrorLabel = Label(self, bg="red")
        # self.calculateHashErrorLabel.grid(row=2, column=4)

        self.hashCalculateEntryFrame = Frame(self)
        self.hashCalculateEntryFrame.grid(row=2, column=1)

        self.hashInput = Entry(self.hashCalculateEntryFrame, text="")
        self.hashInput.grid(row=0, column=0)
        self.hashOutput = Entry(self.hashCalculateEntryFrame, text="")
        self.hashOutput.grid(row=0, column=2)

        self.hashInput1 = Entry(self.hashCalculateEntryFrame, text="")
        self.hashInput1.grid(row=1, column=0)
        self.hashOutput1 = Entry(self.hashCalculateEntryFrame, text="")
        self.hashOutput1.grid(row=1, column=2)

        self.hashInput2 = Entry(self.hashCalculateEntryFrame, text="")
        self.hashInput2.grid(row=2, column=0)
        self.hashOutput2 = Entry(self.hashCalculateEntryFrame, text="")
        self.hashOutput2.grid(row=2, column=2)

        self.hashJSON = {
            "hash": [self.hashInput, self.hashOutput],
            "hash1": [self.hashInput1, self.hashOutput1],
            "hash2": [self.hashInput2, self.hashOutput2],
        }

        self.compareHashTitle = Label(
            self, text="Compare hashes", font=("Trebuchet MS", 10)
        )
        self.compareHashTitle.grid(row=8, column=0, sticky="nesw")
        self.compareHashEntry = Entry(self)
        self.compareHashEntry.bind("<Key>", self.compareHashes)
        self.compareHashEntry.grid(row=9, column=0)
        self.compareHashEntry1 = Entry(self)
        self.compareHashEntry1.bind("<Key>", self.compareHashes)
        self.compareHashEntry1.grid(row=10, column=0)
        self.compareHashResult = Label(self, text="no entry")
        self.compareHashResult.grid(row=9, column=1)

    # Update currentHashAlgorithm after a listbox selection
    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        try:
            value = sender.get(idx)
            self.currentHashAlgorithm.set(value)
        except TclError:
            pass

    # Calculate hashes for each input widget and insert into output widget
    def calculateHashes(self):
        for hashGroup in self.hashJSON.keys():
            # print("{}".format(self.hashJSON[hashGroup][0].get()))
            self.hashJSON[hashGroup][1].delete(0, END)
            self.hashJSON[hashGroup][1].insert(
                0,
                self.calculateHash(
                    self.currentHashAlgorithm.get(), self.hashJSON[hashGroup][0].get()
                ),
            )

    # Calculate hash using passed algorithm and data
    def calculateHash(self, hashAlgorithm, data):
        try:
            h = hashlib.new(hashAlgorithm)
            h.update(data.encode("utf-8"))
            return h.hexdigest()
        except ValueError:
            return "Hash algorithm not supported"
        # print(hashlib.new(hashAlgorithm, data.encode('utf-8')).hexdigest())

    def compareHashes(self, text):
        # Both need to be checked against checked, since the one that triggered the method wont have the updated character
        if self.compareHashEntry.get() == self.compareHashEntry1.get() + text.char:
            self.compareHashResult["text"] = "match"
        elif self.compareHashEntry.get() + text.char == self.compareHashEntry1.get():
            self.compareHashResult["text"] = "match"
        else:
            self.compareHashResult["text"] = "no match"

    def initUI_encryptionFrame(self):
        print("Encryption frame")

    # TODO Add optional hash and encryption dialogs if user doesn't want to create a frame
    def hashDialog(self):
        self.hashDialog = Toplevel()
        self.hashDialog.title = "Hash"

    def encryptionDialog(self):
        self.encryptionDialog = Toplevel()
        self.encryptionDialog.title = "Encrypt"
