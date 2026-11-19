# Main/game menu and save-slot geometry.

init offset = -1

define gui.main_menu_background = Solid("#0a0a1a", xysize=(1920, 1080))
define gui.game_menu_background = Solid("#0a0a1a", xysize=(1920, 1080))
define gui.slot_button_width = 360
define gui.slot_button_height = 260
define gui.slot_button_borders = Borders(10, 10, 10, 10)
define gui.slot_button_text_size = 14
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color
define config.thumbnail_width = 256
define config.thumbnail_height = 144
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

define gui.navigation_xpos = 40
define gui.skip_ypos = 12
define gui.notify_ypos = 55
define gui.choice_spacing = 24
define gui.navigation_spacing = 4
define gui.pref_spacing = 10
define gui.pref_button_spacing = 10
define gui.page_spacing = 20
define gui.slot_spacing = 10
define gui.main_menu_text_xalign = 0.5

define gui.frame_borders = Borders(4, 4, 4, 4)
define gui.confirm_frame_borders = Borders(45, 45, 45, 45)
define gui.skip_frame_borders = Borders(18, 6, 55, 6)
define gui.notify_frame_borders = Borders(18, 5, 45, 5)
define gui.frame_tile = False
