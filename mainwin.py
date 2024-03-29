import random
import platform
from glob import glob
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from PIL import Image, ImageTk, ImageOps
from tkinter import Tk, LEFT, RIGHT, BOTTOM, StringVar, END
from tkinter.ttk import Frame, Label, Button, Entry
from statwin import StatWin


class MainWin(object):
    def __init__(self):
        self.win = Tk()
        self.win.title('Gissa namn')

        # will be instanciated when calling game_over()
        self.statwin: StatWin = None

        self.IMAGE_SIZE = (500, 500)

        self.name_fails: list[str] = []
        self.name_wins: list[str] = []
        self.image_paths: list[str] = []
        self.current_image_index: int = 0
        self.image_directory_path: str = str()

        self.mainframe: Frame = Frame(self.win)
        self.mainframe.pack()

        # init the frame containing the buttons
        self.buttonframe: Frame = Frame(self.mainframe)
        self.buttonframe.pack()
        self.openbutton: Button = Button(master=self.buttonframe, text='Öppna', command=self.open_image_dir)
        self.openbutton.pack(side=LEFT, anchor='w', padx=(0, 10))
        self.submitbuttonvar = StringVar(master=self.win, value='Klar')
        self.submitbutton: Button = Button(master=self.buttonframe, textvariable=self.submitbuttonvar,
                                           command=self.ok_action)
        self.submitbutton.pack(side=LEFT)
        self.win.bind('<Return>', lambda e: self.ok_action())
        self.statvar = StringVar(master=self.win, value='0 av 0')
        self.statlabel = Label(master=self.buttonframe, textvariable=self.statvar)
        self.statlabel.pack(side=RIGHT, padx=(20,0), anchor='e')


        # init the frame containing the image
        self.imageframe: Frame = Frame(self.mainframe)
        self.imageframe.pack()
        # create a image and set it to the default image
        self.img = Image.open('empty.jpg')
        self.img = ImageOps.contain(self.img, self.IMAGE_SIZE)
        self.photoimage = ImageTk.PhotoImage(image=self.img)
        self.imagelabel = Label(master=self.imageframe, image=self.photoimage)
        self.imagelabel.pack()

        self.nameframe: Frame = Frame(self.mainframe)
        self.nameframe.pack()
        self.namevar: StringVar = StringVar(master=self.nameframe, value='Inget namn')
        self.nameentry: Entry = Entry(master=self.nameframe, style='NORMAL.TEntry', textvariable=self.namevar)
        self.nameentry.pack(side=BOTTOM)

        self.win.mainloop()

    def display_default_image(self):
        self.img = Image.open('empty.jpg')
        self.photoimage = ImageTk.PhotoImage(image=ImageOps.contain(self.img, self.IMAGE_SIZE))
        self.imagelabel.config(image=self.photoimage)

    def diplay_next_image(self):
        if self.current_image_index >= len(self.image_paths)-1:
            # showinfo('Klar', 'Nu har du gissat klart.')
            self.game_over()
            return

        try:
            self.img = Image.open(self.image_paths[self.current_image_index+1])
            if self.img.height > self.IMAGE_SIZE[0]:
                resizefactor = self.IMAGE_SIZE[0] / self.img.height
                h = round(resizefactor * self.img.height)
                w = round(resizefactor * self.img.width)
                self.img = self.img.resize((w, h))
        except FileNotFoundError:
            self.display_default_image()
            return

        self.current_image_index += 1
        self.photoimage = ImageTk.PhotoImage(image=self.img)
        self.imagelabel.config(image=self.photoimage)
        self.update_statlabel()


    def open_image_dir(self, imgdir: str=None, imgpaths: tuple[str]=None):
        if self.statwin is not None:
            self.statwin.win.destroy()
            self.statwin = None

        # ask to open a dir if none is given
        if imgdir is None and imgpaths is None:
            imgdir = askdirectory()

        if imgdir is not None and imgdir != "" and imgdir != ():
            print(f'Setting image directory to {imgdir}')
            self.name_wins.clear()
            self.name_fails.clear()
            self.image_directory_path = imgdir
            self.current_image_index = 0
            if imgpaths is None:
                self.prepare_image_paths()
            else:
                self.image_paths = list(imgpaths)
            self.update_statlabel()
            # display the first image
            self.img = Image.open(self.image_paths[0])
            if self.img.height > self.IMAGE_SIZE[0]:
                resizefactor = self.IMAGE_SIZE[0] / self.img.height
                h = round(resizefactor * self.img.height)
                w = round(resizefactor * self.img.width)
                self.img = self.img.resize((w, h))
            self.photoimage = ImageTk.PhotoImage(self.img)
            self.imagelabel.config(image=self.photoimage)
            self.namevar.set('')
            self.nameentry.config(state='normal')
            self.nameentry.focus_set()

    def prepare_image_paths(self):
        if self.image_directory_path == "":
            showerror(title='Fel', message='Ingen mapp är vald.')
            return

        # path_separator = '\\' if platform.system() == 'Windows' else '/'
        path_separator = '/'
        # print('Searching for ' + self.image_directory_path + '/*.jpg')
        imgpaths = glob(self.image_directory_path + path_separator + '*.jpg') + \
                   glob(self.image_directory_path + path_separator + '*.jpeg')
        print(f'Platform: {platform.system()}, separator: {path_separator}')
        print('Found images:')
        for imgp in imgpaths:
            print(f'{imgp}   with name: {self.extract_name_from_path(imgp)}')

        if len(imgpaths) == 0:
            showerror(title='Fel', message='Hittade inte några bilder i mappen.')
        else:
            random.shuffle(imgpaths)
            self.image_paths = imgpaths

    def extract_name_from_path(self, imgpath: str):
        if '\\' in imgpath:
            imgpath = imgpath.replace('\\', '/')


        if '/' in imgpath:
            return imgpath.split('/')[-1].split('.')[0].split(' ')[0]
        else:
            return imgpath.split('.')[0]

    def ok_action(self):
        if len(self.image_paths) == 0:
            print('No image dir set')
            return
        elif len(self.namevar.get()) == 0:
            print('Text entry is empty')
            return

        # print('Verifying name')
        # print(f'Correct name: {self.current_correct_name()}  Guess: {self.namevar.get()}')
        if self.verify_name():
            print('Correct guess')
            self.name_win()
        else:
            print('Wrong guess')
            self.name_fail()

    def current_correct_name(self) -> str:
        return self.extract_name_from_path(self.image_paths[self.current_image_index])

    def update_statlabel(self):
        self.statvar.set(f'{self.current_image_index + 1 } av {len(self.image_paths)}')

    def verify_name(self) -> bool:
        return self.namevar.get().lower() == \
               self.extract_name_from_path(self.image_paths[self.current_image_index]).lower()

    def name_fail(self):
        self.namevar.set(self.extract_name_from_path(self.image_paths[self.current_image_index]))
        self.nameentry.select_range(0, END)
        self.nameentry.icursor(END)
        self.nameentry.focus_set()
        # self.nameentry.config(style='WRONG.TEntry')
        self.name_fails.append(self.image_paths[self.current_image_index])

    def name_win(self):
        self.namevar.set('')
        self.nameentry.focus_set()
        # self.nameentry.config(style='NORMAL.TEntry')
        # only add to correct guesses if first guess was correct
        if self.image_paths[self.current_image_index] not in self.name_fails:
            self.name_wins.append(self.image_paths[self.current_image_index])
        self.diplay_next_image()

    def game_over(self):
        self.nameentry.config(state='disabled')
        self.statwin = StatWin(self)
        self.submitbuttonvar.set('Omstart')
        self.submitbutton.config(command=self.restart_game)

    def restart_game(self, imgpaths=None):
        if self.statwin is not None:
            self.statwin.win.destroy()
            self.statwin = None

        self.nameentry.config(state='normal')
        self.update_statlabel()
        self.submitbuttonvar.set('Klar')
        self.submitbutton.config(command=self.ok_action)
        self.name_wins.clear()
        self.name_fails.clear()
        self.current_image_index = 0
        self.open_image_dir(self.image_directory_path, imgpaths)


if __name__ == '__main__':
    mw = MainWin()
