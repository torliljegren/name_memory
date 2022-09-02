import tkinter as tk
import tkinter.ttk as ttk
from glob import glob
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from PIL import Image
from PIL import ImageTk
from PIL import ImageOps

class MainWin(object):
    def __init__(self):
        self.names: list[str] = []
        self.name_fails: list[str] = []
        self.name_wins: list[str] = []
        self.image_paths: list[str] = []
        self.current_image_index: int = 0
        self.image_directory_path: str = str()

        self.win: tk.Tk = tk.Tk()

        self.mainframe: ttk.Frame = ttk.Frame(self.win)
        self.mainframe.pack()

        # init the frame containing the buttons
        self.buttonframe: ttk.Frame = ttk.Frame(self.mainframe)
        self.buttonframe.pack()
        self.openbutton: ttk.Button = ttk.Button(master=self.buttonframe, text='Öppna', command=self.open_image_dir)
        self.openbutton.pack(side=tk.LEFT)
        self.submitbutton: ttk.Button = ttk.Button(master=self.buttonframe, text='Klar')
        self.submitbutton.pack(side=tk.RIGHT)

        # init the frame containing the image
        self.imageframe: ttk.Frame = ttk.Frame(self.mainframe)
        self.imageframe.pack()
        self.img = Image.open(fp='empty.jpg')
        self.photoimage = ImageTk.PhotoImage(image=ImageOps.contain(self.img, (500,500)))
        self.imagelabel: ttk.Label = ttk.Label(master=self.imageframe, image=self.photoimage)
        self.imagelabel.pack()

        self.nameframe: ttk.Frame = ttk.Frame(self.mainframe)
        self.nameframe.pack()
        self.namevar: tk.StringVar = tk.StringVar(master=self.nameframe, value='Inget namn')
        self.nameentry: ttk.Entry = ttk.Entry(master=self.nameframe)
        self.nameentry.pack(side=tk.BOTTOM)

        self.win.mainloop()

    def diplay_next_image(self):
        pass

    def open_image_dir(self):
        imgdirpath = askdirectory()
        if imgdirpath is not None and imgdirpath != "":
            self.image_directory_path = imgdirpath

    def prepare_image_paths(self):
        if self.image_directory_path != "":
            pass
        else:
            showerror(title='Fel', message='Ingen mapp är vald.')

        imgpaths = glob(self.image_directory_path + '/.jpg') + glob(self.image_directory_path + '/.jpeg')

        if len(imgpaths) == 0:
            showerror(title='Fel', message='Hittade inte några bilder i mappen.')
        else:
            for imgpath in imgpaths:
                self.image_paths.append(imgpath)

    def extract_name_from_path(self, imgpath: str):
        if '/' in imgpath:
            return imgpath.split('/')[-1]
        else:
            return str()

    def ok_action(self):
        pass

    def verify_name(self):
        pass

    def name_fail(self):
        pass

    def name_win(self):
        pass

    def game_over(self):
        pass

    def restart_game(self):
        pass

if __name__ == '__main__':
    mw = MainWin()
