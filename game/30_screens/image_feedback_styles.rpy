# Styles for the image feedback overlay and modal.

style feedback_btn:
    background Solid("#101522e8")
    hover_background Solid("#3b2c52")
    padding (10, 6)

style feedback_btn_text:
    font gui.interface_text_font
    size 16
    color "#d8d0e5"
    hover_color "#ffffff"

style feedback_up_active is feedback_btn:
    background Solid("#1f5c3a")

style feedback_up_active_text is feedback_btn_text:
    color "#d7ffea"
    bold True

style feedback_down_active is feedback_btn:
    background Solid("#6e2432")

style feedback_down_active_text is feedback_btn_text:
    color "#ffd9df"
    bold True

style feedback_path_text:
    font gui.interface_text_font
    size 14
    color "#9ea6c4"
    xalign 0.5

style feedback_reason_btn:
    xfill True
    background Solid("#1f2642")
    hover_background Solid("#5b3d73")
    padding (14, 8)

style feedback_reason_btn_text:
    font gui.interface_text_font
    size 16
    color "#f0ecfa"
    xalign 0.5

style feedback_action_choice_btn:
    background Solid("#2a3560")
    hover_background Solid("#6e428c")
    padding (12, 10)
    xfill True

style feedback_action_choice_btn_text:
    font gui.interface_text_font
    size 14
    bold True
    color "#ffffff"
    text_align 0.5
    xalign 0.5

style feedback_cancel_btn is feedback_reason_btn:
    background Solid("#2b1e2e")
    hover_background Solid("#4f2f40")
