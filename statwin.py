from tkinter import Toplevel
from tkinter.ttk import Label, Button
from PIL import Image, ImageTk, ImageOps
from ttk_scroll import ScrollFrame


class StatWin(object):

    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.win = Toplevel(master=self.mainwin.win)
        self.win.title('Översikt')

        self.THUMB_SIZE = (100, 100)
        self.COLUMN_PADX = (0, 40)

        self.statframe = ScrollFrame(self.win)

        Label(master=self.statframe.viewPort, text=f'Avklarade ({len(self.mainwin.name_wins)} st)').grid(row=0,
                                                                                                         column=0)
        Label(master=self.statframe.viewPort, text=f'Missade ({len(self.mainwin.name_fails)} st)').grid(row=0,
                                                                                                        column=2)

        # a column with names entered correct
        for i in range(len(self.mainwin.name_wins)):
            img = Image.open(self.mainwin.name_wins[i])
            photoimg = ImageTk.PhotoImage(ImageOps.contain(img, self.THUMB_SIZE))
            lbl = Label(master=self.statframe.viewPort, image=photoimg)
            lbl.photoimage = photoimg
            lbl.grid(row=i+1, column=0)
            nlbl = Label(master=self.statframe.viewPort,
                         text=self.mainwin.extract_name_from_path(self.mainwin.name_wins[i]))
            nlbl.grid(row=i+1, column=1, padx=self.COLUMN_PADX)

        # a column with names entered incorrect
        for i in range(len(self.mainwin.name_fails)):
            img = Image.open(self.mainwin.name_fails[i])
            photoimg = ImageTk.PhotoImage(ImageOps.contain(img, self.THUMB_SIZE))
            lbl = Label(master=self.statframe.viewPort, image=photoimg)
            lbl.photoimage = photoimg
            lbl.grid(row=i+1, column=2)
            nlbl = Label(master=self.statframe.viewPort,
                         text=self.mainwin.extract_name_from_path(self.mainwin.name_fails[i]))
            nlbl.grid(row=i+1, column=3)

        # add a button to retry failed names
        if len(self.mainwin.name_fails) > 0:
            againbutton = Button(master=self.statframe.viewPort, text='Försök igen',
                                 command=lambda: self.mainwin.open_image_dir(self.mainwin.image_directory_path,
                                                                         [path for path in self.mainwin.name_fails]))
            againbutton.grid(row=len(self.mainwin.name_fails)+1, column=2)

        self.statframe.pack(side='top', fill='both', expand=True)

        self.win.update()
        mh = self.minheight()
        print(f'minheight={mh}')
        self.win.geometry(f'{self.win.winfo_width()}x{mh}')
        print(self.win.winfo_geometry())

    def minheight(self) -> int:
        # find the column with the most images
        wins = len(self.mainwin.name_wins)
        fails = len(self.mainwin.name_fails)

        # calculate approx height of the images
        imgheight = (wins if wins > fails else fails) * 110

        halfscreen = self.win.winfo_screenheight() / 2

        # return the smallest of them
        return int(imgheight if imgheight < halfscreen else halfscreen)


