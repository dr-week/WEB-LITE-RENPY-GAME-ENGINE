# Compact rotating vinyl disc: small when idle, pops out icon-based controls on hover.

screen cd_music_widget():
    zorder 105
    default _cd_hover = False
    if not main_menu and not renpy.context()._menu:
        if auto_dj_enabled:
            timer 2.5 repeat True action Function(dj_check_auto_advance)
        $ track_label = getattr(renpy.store, "current_dj_track_name", "Downtown Glow")
        hbox:
            at cd_hud_fader
            xpos 24
            ypos 66
            spacing 8
            button:
                at music_disc_hover
                xysize (42, 42)
                padding (0, 0)
                background None
                hovered SetScreenVariable("_cd_hover", True)
                unhovered SetScreenVariable("_cd_hover", False)
                action Function(dj_skip_and_remix)
                add Transform("images/ui/vinyl_disc.png", xysize=(36, 36), align=(0.5, 0.5)) at cd_spin_continuous
            if _cd_hover:
                frame:
                    at music_pill_pop
                    yalign 0.5
                    background Solid("#0e1326f0")
                    padding (10, 5)
                    hbox:
                        spacing 7
                        yalign 0.5
                        imagebutton idle Transform("images/ui/icons/arrowLeft.png", xysize=(14, 14)) action Function(dj_prev_track) yalign 0.5
                        add Transform("images/ui/icons/fastForward.png", xysize=(15, 15)) yalign 0.5
                        text _("SKIP") size 12 bold True color "#ffe8a3" yalign 0.5
                        text "|" size 12 color "#6d678a" yalign 0.5
                        textbutton _("CUE") text_size 12 text_bold True text_color "#9ee7ff" action Function(dj_cue_bridge_remix) padding (2, 0) yalign 0.5
                        text "|" size 12 color "#6d678a" yalign 0.5
                        textbutton ("AUTO" if auto_dj_enabled else "MAN") text_size 11 text_bold True text_color ("#8ef5b5" if auto_dj_enabled else "#a8a2bf") action Function(toggle_auto_dj) padding (2, 0) yalign 0.5
                        text "|" size 12 color "#6d678a" yalign 0.5
                        add Transform("images/ui/icons/audioOn.png", xysize=(14, 14)) yalign 0.5
                        text "[track_label]" italic True size 13 color "#e8d5ff" yalign 0.5 at music_title_shimmer
