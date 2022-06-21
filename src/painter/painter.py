from gui import gui
from handbookapi import handbookapi


def make_gui():
    main_window = gui.MainWindow()
    main_frame = gui.MainFrame(main_window)
    list_frame = gui.NotesListFrame(main_frame)
    note_text_frame = gui.NoteTextFrame(main_frame, list_frame.width+15)
    note_text_area = gui.NoteTextArea(note_text_frame, 0, '')

    notes = handbookapi.get_notes()

    for i, note in enumerate(notes):
        position = [15, i * 25 + 15]

        gui.NoteTitleLabel(list_frame, note.id, note.title,
                           position, note_text_area)

    main_window.mainloop()
