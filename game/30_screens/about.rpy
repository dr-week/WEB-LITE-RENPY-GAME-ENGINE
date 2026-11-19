# About screen content.

screen about():
    tag menu
    use game_menu(_("About"), scroll="viewport"):
        vbox:
            spacing 18
            label "[config.name!t]"
            text _("Version [config.version!t]")
            text _("A choice-driven life-story visual novel.")
            text _("Made with Ren'Py [renpy.version_only].")
            text _("This project uses Ren'Py's native screen and story systems.")
