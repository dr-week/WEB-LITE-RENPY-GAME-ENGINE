# File-slot navigation and screens.

screen save():
    tag menu
    use file_slots(_("Save"))


screen load():
    tag menu
    use file_slots(_("Load"))


screen file_slots(title):
    default page_name_value = FilePageNameInputValue(
        pattern=_("Page {}"),
        auto=_("Automatic saves"),
        quick=_("Quick saves")
    )
    use game_menu(title):
        fixed:
            order_reverse True
            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                input:
                    style "page_label_text"
                    value page_name_value
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.48
                spacing gui.slot_spacing
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)
                        has vbox
                        add FileScreenshot(slot) xalign 0.5
                        text FileTime(
                            slot,
                            format=_("{#file_time}%A, %B %d, %Y, %H:%M"),
                            empty=_("Empty slot")
                        ) style "slot_time_text"
                        text FileSaveName(slot) style "slot_name_text"
                        key "save_delete" action FileDelete(slot)
            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.0
                spacing gui.page_spacing
                textbutton _("<") action FilePagePrevious()
                key "save_page_prev" action FilePagePrevious()
                if config.has_autosave:
                    textbutton _("A") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("Q") action FilePage("quick")
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)
                textbutton _(">") action FilePageNext()
                key "save_page_next" action FilePageNext()
