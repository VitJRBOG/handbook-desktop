from gui import gui
from handbookapi import handbookapi


def make_gui():
    main_window = gui.MainWindow()
    main_frame = gui.MainFrame(main_window)
    list_frame = gui.NotesListFrame(main_frame)

    notes = handbookapi.get_notes()

    for i, note in enumerate(notes):
        position = [15, i * 25 + 15]

        gui.NoteTitleLabel(list_frame, note.title, position)

    main_window.mainloop()
