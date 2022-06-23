from gui import gui
from handbookapi import handbookapi


def make_gui():
    main_window = gui.MainWindow()
    main_frame = gui.MainFrame(main_window)

    list_frame = gui.NotesListFrame(main_frame)

    note_text_frame = gui.NoteTextFrame(main_frame, list_frame.width+15)
    note_text_area = gui.NoteTextArea(note_text_frame, 0, '')

    buttons_frame = gui.ButtonsFrame(
        list_frame, note_text_area, list_frame.height-30)
    add_button = gui.AddButton(buttons_frame)
    delete_button = gui.DeleteButton(buttons_frame)

    note_manage_buttons_frame = gui.NoteManageButtonsFrame(
        main_frame,
        note_text_area,
        list_frame.width+15,
        note_text_area.height+10)
    save_button = gui.SaveButton(note_manage_buttons_frame)
    note_versions_list = gui.NoteVersionsList(note_manage_buttons_frame, [''])

    notes = handbookapi.get_notes()

    for i, note in enumerate(notes):
        position = [15, i * 25 + 15]

        gui.NoteTitleLabel(list_frame, note.id, note.title,
                           position, note_text_area,
                           note_versions_list)

    main_window.mainloop()
