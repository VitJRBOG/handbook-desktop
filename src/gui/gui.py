import tkinter as tk
from typing import List


VERSION_ = '0.1.0-alpha'


class MainWindow(tk.Tk):
    width = 500
    height = 300

    def __init__(self):
        super().__init__()

        global VERSION_
        self.title(f'Handbook (v{VERSION_})')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        pos_x = (screen_width // 2) - (self.width // 2)
        pos_y = (screen_height // 2) - (self.height // 2)

        self.geometry(f'{self.width}x{self.height}+{pos_x}+{pos_y}')

        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)


class MainFrame(tk.Canvas):
    width: int
    height: int

    def __init__(self, master: MainWindow):
        self.width = master.width
        self.height = master.height

        super().__init__(master, width=self.width, height=self.height)

        self.place(x=0, y=0)


class NotesListFrame(tk.Canvas):
    width: int
    height: int
    notes_list: List[str]

    def __init__(self, master: MainFrame):
        self.width = int(master.width * 0.30)
        self.height = master.height

        super().__init__(master, width=self.width, height=self.height)

        self.place(x=0, y=0)


class NoteTitleLabel(tk.Label):
    text_var: tk.StringVar
    bg_color_default = '#A4A4A4'
    bg_color_focused = '#808080'

    def __init__(self, master: NotesListFrame, title: str, position: List[int]):
        self.text_var = tk.StringVar()
        self.text_var.set(title)

        super().__init__(master, textvariable=self.text_var)

        self.config(bg=self.bg_color_default)

        self.bind('<Enter>', self.__set_red_color)
        self.bind('<Leave>', self.__set_default_color)

        self.place(x=position[0], y=position[1])

    def __set_red_color(self, event):
        self.config(bg=self.bg_color_focused)

    def __set_default_color(self, event):
        self.config(bg=self.bg_color_default)
