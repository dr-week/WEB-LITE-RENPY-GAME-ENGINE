# Dialogue deck, say screen, and choice-card styles.

style choice_button:
    xsize gui.choice_btn_width
    xalign 0.5
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover
    padding gui.choice_btn_pad

style choice_button_text:
    font gui.text_font
    size gui.choice_button_text_size
    color gui.choice_button_text_idle_color
    hover_color gui.choice_button_text_hover_color
    xalign 0.5
    text_align 0.5

style choice_hint_text:
    font gui.interface_text_font
    size gui.hint_text_size
    bold True
    color gui.accent_highlight
    xalign 0.5
    text_align 0.5

style say_continue_button:
    background gui.glass_pill
    hover_background gui.glass_btn_hover
    padding gui.pill_pad

style say_continue_button_text:
    font gui.interface_text_font
    size gui.pill_text_size
    color gui.text_color
    hover_color gui.gold_hover

style window:
    xalign 0.5
    xsize gui.window_width
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background gui.glass_elevated
    padding gui.window_pad

style namebox:
    xalign 0.0
    background gui.glass_pill
    padding gui.namebox_pad

style say_label:
    font gui.name_text_font
    size gui.name_text_size
    color gui.text_color
    bold True

style say_dialogue:
    font gui.text_font
    size gui.text_size
    xsize gui.dialogue_width
    adjust_spacing False
    color gui.text_color
