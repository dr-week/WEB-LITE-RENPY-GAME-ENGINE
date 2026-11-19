# LOLA - Custom Choice Screens
# Custom choice displays for the game
# Ren'Py 8.6.0

# Extended choice screen with optional image
screen extended_choice(items, background=None):
    """Choice screen with optional background image."""
    style_prefix "choice"
    
    if background:
        add background
    else:
        add Solid("#0a0a1a")
    
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20
        
        for i in items:
            textbutton i.caption action i.action style "choice_button_extended"


style choice_button_extended:
    properties gui.button_properties("choice_button")
    background Solid("#2a2a3e", xysize=(900, 55))
    padding (80, 12)
    xalign 0.5
    yalign 0.5


style choice_button_extended_text:
    properties gui.text_properties("choice_button")
    color gui.text_color
    font "DejaVuSans.ttf"
    size 26
    xalign 0.5


# Confirmation screen
screen confirmation_dialog(message, yes_action, no_action):
    """Simple confirmation dialog."""
    modal True
    zorder 200
    
    add Solid("#0a0a1a", xysize=(1920, 1080))
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 250
        
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 25
            
            text message style "confirm_text"
            
            hbox:
                xalign 0.5
                spacing 80
                
                textbutton "Yes" action yes_action style "confirm_yes"
                textbutton "No" action no_action style "confirm_no"


style confirm_text:
    font "DejaVuSans.ttf"
    size 24
    color gui.text_color
    xalign 0.5


style confirm_yes:
    properties gui.button_properties("navigation_button")
    background Solid("#2a3a2a", xysize=(120, 45))
    padding (12, 10)
    xalign 0.5


style confirm_yes_text:
    color gui.text_color
    font "DejaVuSans.ttf"
    size 20


style confirm_no:
    properties gui.button_properties("navigation_button")
    background Solid("#3a2a2a", xysize=(120, 45))
    padding (12, 10)
    xalign 0.5


style confirm_no_text:
    color gui.text_color
    font "DejaVuSans.ttf"
    size 20
