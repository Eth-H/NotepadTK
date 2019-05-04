from tkinter import *
#Inherits from tk.Frame

class Cryptography(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.hashLabel = Label(parent, text="Nice lookin hash label")
        self.hashLabel.grid(row=0, column=0)


        #button1 = Button(self, text="Visit page 1",command=lambda: controller.show_frame(PageOne))
        #button1.pack()

    def hashDialog(self):
        self.hashDialog = Toplevel()
        self.hashDialog.title = "Hash"
    def encryptionDialog(self):
        self.encryptionDialog = Toplevel()
        self.encryptionDialog.title = "Hash"
