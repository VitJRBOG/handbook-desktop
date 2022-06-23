import threading
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
from typing import List
from datetime import datetime

from handbookapi import handbookapi


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


class NoteTextFrame(tk.Canvas):
    width: int
    height: int

    def __init__(self, master: MainFrame, indent: int):
        self.width = int(master.width * 0.65)
        self.height = master.height - 40

        super().__init__(master, width=self.width, height=self.height)

        self.place(x=indent, y=0)


class NoteTextArea(tkst.ScrolledText):
    width: int
    height: int
    note_id: int
    text: str

    def __init__(self, master: NoteTextFrame, note_id: int, text: str):
        self.width = master.width
        self.height = master.height
        self.note_id = note_id
        self.text = text

        super().__init__(master, wrap=tk.WORD,
                         width=self.width, height=self.height,
                         font=('Times New Roman', 16))

        self.insert(tk.END, self.text)

        self.place(x=0, y=0)

    def update_text(self, note_id: int, text: str):
        self.note_id = note_id
        self.delete('0.0', tk.END)
        self.text = text
        self.insert(tk.END, self.text)


class NoteManageButtonsFrame(tk.Canvas):
    note_text_area: NoteTextArea

    def __init__(self, master: MainFrame,
                 note_text_area: NoteTextArea,
                 indent_x: int, indent_y: int):

        self.note_text_area = note_text_area

        super().__init__(master)

        self.place(x=indent_x, y=indent_y)

    def add_version(self):
        if self.note_text_area.note_id != 0:
            note_id = self.note_text_area.note_id
            text = self.note_text_area.get('1.0', tk.END)
            handbookapi.add_version(note_id, text)


class SaveButton(tk.Button):
    def __init__(self, master: NoteManageButtonsFrame):
        super().__init__(master, text='Save',
                         command=lambda: threading.Thread(
                             target=master.add_version,
                             daemon=True).start())

        self.place(x=0, y=0)


class NoteVersionsList(ttk.Combobox):
    note_id: int
    text_var: tk.StringVar

    def __init__(self, master: NoteManageButtonsFrame, versions: List[str]):
        self.text_var = tk.StringVar()
        super().__init__(master, textvariable=self.text_var,
                         values=versions, state='readonly')
        self.text_var.set(versions[len(versions)-1])

        self.place(x=70, y=0)


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
    note_id: int
    text_var: tk.StringVar
    bg_color_default = '#A4A4A4'
    bg_color_focused = '#808080'
    note_text_area: NoteTextArea
    version_list: NoteVersionsList

    def __init__(self, master: NotesListFrame, note_id: int, title: str,
                 position: List[int], note_text_area: NoteTextArea,
                 version_list: NoteVersionsList):
        self.note_id = note_id
        self.text_var = tk.StringVar()
        self.text_var.set(title)
        self.note_text_area = note_text_area
        self.version_list = version_list

        super().__init__(master, textvariable=self.text_var)

        self.config(bg=self.bg_color_default)

        self.bind('<Enter>', self.__set_red_color)
        self.bind('<Leave>', self.__set_default_color)
        self.bind('<Button-1>', self.__display_note)

        self.place(x=position[0], y=position[1])

    def __set_red_color(self, event):
        self.config(bg=self.bg_color_focused)

    def __set_default_color(self, event):
        self.config(bg=self.bg_color_default)

    def __display_note(self, event):
        notes = handbookapi.get_versions(self.note_id)
        self.note_text_area.update_text(notes[0].id, notes[0].text)

        versions: List[str] = []

        for version in notes:
            date = datetime.utcfromtimestamp(
                version.date).strftime('%d.%m.%Y %H:%M:%S')
            versions.append(date)

        self.version_list.config(values=versions)
        self.version_list.text_var.set(versions[0])


class ButtonsFrame(tk.Canvas):
    note_text_area: NoteTextArea

    def __init__(self, master: NotesListFrame,
                 note_text_area: NoteTextArea, indent: int):
        self.note_text_area = note_text_area

        super().__init__(master)

        self.place(x=0, y=indent)

    def add_note(self):
        if self.note_text_area.note_id == 0:
            text = self.note_text_area.get('1.0', tk.END)
            handbookapi.add_note(text)

    def delete_note(self):
        note_id = self.note_text_area.note_id
        # TODO: API method for deleting of note is missing


class AddButton(tk.Button):

    def __init__(self, master: ButtonsFrame):
        super().__init__(master, text='+',
                         command=lambda: threading.Thread(
                             target=master.add_note,
                             daemon=True).start())

        self.place(x=0, y=0)


class DeleteButton(tk.Button):

    def __init__(self, master: ButtonsFrame):
        super().__init__(master, text='-',
                         command=lambda: threading.Thread(
                             target=master.delete_note,
                             daemon=True).start())

        self.place(x=40, y=0)
