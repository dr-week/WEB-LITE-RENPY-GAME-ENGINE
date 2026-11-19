# Confirmation modal for quit and destructive actions.

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    style_prefix "confirm"
    add Solid("#080b14d8")
    frame at ui_modal_pop:
        xalign 0.5
        yalign 0.5
        xsize 820
        background gui.glass_elevated
        padding (48, 42)
        vbox:
            spacing 30
            label _(message) xalign 0.5
            hbox:
                xalign 0.5
                spacing 30
                textbutton _("Yes") activate_sound ui_sfx_confirm action yes_action
                textbutton _("No") activate_sound ui_sfx_back action no_action
    key "game_menu" action no_action


style confirm_frame:
    background gui.glass_elevated


style confirm_prompt:
    xalign 0.5


style confirm_prompt_text:
    size 28
    color gui.text_color
    text_align 0.5


style confirm_button:
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover
    padding (28, 14)


style confirm_button_text:
    size 24
    color gui.text_color
