import tkinter as tk
import tkinter.ttk as ttk
from glob import glob
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror

class MainWin(object):
    def __init__(self):
        self.names: list[str] = []
        self.name_fails: list[str] = []
        self.name_wins: list[str] = []
        self.image_paths: list[str] = []
        current_image: int = 0

        self.win: tk.Tk = tk.Tk()
        self.mainframe: ttk.Frame = ttk.Frame(self.win)
        self.image_directory_path: str = str()

        # init game

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
                self.images.append(imgpath)

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

