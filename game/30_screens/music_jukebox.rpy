# In-game and Main Menu DJ Music Jukebox & Track Explorer
# Ren'Py 8.6.0

screen music_jukebox():
    tag menu
    modal True
    use game_menu(_("Lofi Music Lounge & DJ Deck"), scroll="viewport", spacing=14):
        vbox:
            spacing 18
            xfill True

            # Active Track Control Header Card
            frame:
                background Solid("#14182ed0")
                padding (20, 16)
                xfill True
                hbox:
                    spacing 20
                    yalign 0.5
                    add Transform("images/ui/vinyl_disc.png", xysize=(52, 52), align=(0.5, 0.5)) at cd_spin_continuous
                    vbox:
                        spacing 4
                        text _("NOW PLAYING & LIVE MIXING") size 12 bold True color "#ffe8a3"
                        $ now_title = getattr(renpy.store, "current_dj_track_name", "Downtown Glow")
                        text "[now_title]" size 22 bold True color "#ffffff"
                    null width 20
                    hbox:
                        yalign 0.5
                        spacing 12
                        textbutton _("⚡ Remix & Skip (DJ Cut)"):
                            action Function(dj_skip_and_remix)
                            style "music_deck_button"
                        textbutton _("🔊 Settings"):
                            action ShowMenu("preferences")
                            style "music_deck_button_secondary"

            # Tracklist Grid / Card Deck
            label _("Curated 16-Track Chill Lofi Library") style "music_section_label"

            grid 2 8:
                spacing 12
                xfill True
                for track in DJ_MUSIC_LIBRARY:
                    $ is_active = (track.get("id") == getattr(renpy.store, "current_dj_track_id", ""))
                    frame:
                        background (Solid("#3a2550e0") if is_active else Solid("#161a2be0"))
                        padding (14, 10)
                        xfill True
                        hbox:
                            spacing 12
                            yalign 0.5
                            add Transform("images/ui/icons/audioOn.png", xysize=(20, 20)) yalign 0.5
                            vbox:
                                spacing 2
                                text "[track['title']]" size 16 bold True color ("#ffe8a3" if is_active else "#f0ebf8")
                                text "[track['artist']] • [track['bpm']] BPM • [track.get('key', 'C')]" size 12 color "#a59eb7"
                            null width 10
                            textbutton (_("Playing") if is_active else _("Play Track")):
                                yalign 0.5
                                action Function(dj_play_specific_track, track["id"], "beat_drop")
                                style ("music_track_btn_active" if is_active else "music_track_btn")
