# Ren'Py device-specific layout variants.

init offset = -1

init python:
    @gui.variant
    def touch():
        gui.quick_button_borders = Borders(40, 14, 40, 0)

    @gui.variant
    def small():
        gui.text_size = 30
        gui.name_text_size = 36
        gui.notify_text_size = 25
        gui.interface_text_size = 30
        gui.button_text_size = 30
        gui.label_text_size = 34
        gui.textbox_height = 240
        gui.name_xpos = 80
        gui.dialogue_xpos = 90
        gui.dialogue_width = 1100
        gui.slider_size = 36
        gui.choice_button_width = 1240
        gui.choice_button_text_size = 30
        gui.navigation_spacing = 20
        gui.pref_button_spacing = 10
        gui.history_height = 190
        gui.history_text_width = 690
        gui.quick_button_text_size = 20
        gui.file_slot_cols = 2
        gui.file_slot_rows = 2
        gui.nvl_height = 170
        gui.nvl_name_width = 305
        gui.nvl_name_xpos = 325
        gui.nvl_text_width = 915
        gui.nvl_text_xpos = 345
        gui.nvl_text_ypos = 5
        gui.nvl_thought_width = 1240
        gui.nvl_thought_xpos = 20
        gui.nvl_button_width = 1240
        gui.nvl_button_xpos = 20
