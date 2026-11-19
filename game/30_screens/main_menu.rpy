# Main menu presentation with right-focused card composition and clean glassmorphism.
screen main_menu():
    tag menu
    use menu_slideshow_bg()
    add "ui_vignette_ambient" at ui_vignette_overlay(0.55)

    frame:
        at ui_card_enter
        xalign 0.92
        yalign 0.50
        xsize 580
        ysize 840
        background Solid("#0b0f22dd")
        padding (44, 34)
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 12
            frame:
                style "title_banner"
                vbox:
                    xfill True
                    spacing 6
                    text _("LOLA") style "main_title"
                    text _("A New City, A New Beginning") style "main_subtitle"
            null height 4
            text _("Balance college, work, relationships, and urban hustle as Maya.") style "main_footer"
            null height 6
            textbutton _("New Game") action Start() style "main_menu_button" at ui_hover_pop
            textbutton _("Load Game") action ShowMenu("load") style "main_menu_button" at ui_hover_pop
            textbutton _("Music & DJ Lounge") action ShowMenu("music_jukebox") style "main_menu_button" at ui_hover_pop
            textbutton _("Status & Quests") action ShowMenu("status") style "main_menu_button" at ui_hover_pop
            textbutton _("Settings & Links") action ShowMenu("preferences") style "main_menu_button" at ui_hover_pop
            textbutton _("About") action ShowMenu("about") style "main_menu_button" at ui_hover_pop
            textbutton _("Quit") action Quit(confirm=True) style "main_menu_button" at ui_hover_pop

style main_title:
    font gui.interface_text_font
    size 64
    color "#f2d8ff"
    bold True
    xalign 0.5
    text_align 0.5

style main_subtitle:
    font gui.interface_text_font
    size 22
    color "#eee7f5"
    xalign 0.5
    text_align 0.5

style title_banner:
    xfill True
    background Solid("#192144")
    padding (22, 18)

style main_menu_button:
    xsize 460
    xalign 0.5
    background gui.glass_btn_idle
    hover_background gui.glass_btn_hover
    padding (18, 10)

style main_menu_button_text:
    font gui.interface_text_font
    size 23
    color "#ffffff"
    hover_color "#ffe8a3"
    xalign 0.5
    text_align 0.5

style main_footer:
    size 16
    color "#d5ccdf"
    xalign 0.5
    text_align 0.5
