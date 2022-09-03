from PIL import Image, ImageTk, ImageOps
from tkinter import Tk
from tkinter.ttk import Frame, Label

class TestImage(object):
    def __init__(self):
        self.win = Tk()
        self.mainframe = Frame(master=self.win)
        self.mainframe.pack()
        self.img = Image.open('empty.jpg')
        self.img = ImageOps.contain(self.img, (500,500))
        self.photoimage = ImageTk.PhotoImage(image=self.img)
        self.imagelabel = Label(master=self.mainframe, image=self.photoimage)
        self.imagelabel.pack()
        self.win.mainloop()

if __name__ == '__main__':
    prg = TestImage()