from tkinter import Toplevel
from tkinter.ttk import Frame, Label, Button
from PIL import Image, ImageTk, ImageOps
from scrolledframe import ScrolledWindow


class StatWin(object):

    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.win = Toplevel(master=self.mainwin.win)

        self.THUMB_SIZE = (100,100)
        self.COLUMN_PADX = (0, 40)

        self.statframe = ScrolledWindow(parent=self.win)

        Label(master=self.statframe.scrollwindow, text=f'Avklarade ({len(self.mainwin.name_wins)} st)').grid(row=0, column=0)
        Label(master=self.statframe.scrollwindow, text=f'Missade ({len(self.mainwin.name_fails)} st)').grid(row=0, column=2)

        for i in range(len(self.mainwin.name_wins)):
            img = Image.open(self.mainwin.name_wins[i])
            photoimg = ImageTk.PhotoImage(ImageOps.contain(img, self.THUMB_SIZE))
            lbl = Label(master=self.statframe.scrollwindow, image=photoimg)
            lbl.photoimage = photoimg
            lbl.grid(row=i+1, column=0)
            nlbl = Label(master=self.statframe.scrollwindow, text=self.mainwin.extract_name_from_path(self.mainwin.name_wins[i]))
            nlbl.grid(row=i+1, column=1, padx=self.COLUMN_PADX)

        for i in range(len(self.mainwin.name_fails)):
            img = Image.open(self.mainwin.name_fails[i])
            photoimg = ImageTk.PhotoImage(ImageOps.contain(img, self.THUMB_SIZE))
            lbl = Label(master=self.statframe.scrollwindow, image=photoimg)
            lbl.photoimage = photoimg
            lbl.grid(row=i+1, column=2)
            nlbl = Label(master=self.statframe.scrollwindow, text=self.mainwin.extract_name_from_path(self.mainwin.name_fails[i]))
            nlbl.grid(row=i+1, column=3)

        # will be laid out by itself
        # self.statframe.pack()
