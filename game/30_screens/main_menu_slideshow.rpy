# Dual-layer overlapping Ken Burns slideshow for Main Menu (Right-Aligned Focus).
init python:
    import random

    def _discover_menu_slides():
        exts = (".png", ".jpg", ".jpeg", ".webp")
        return sorted(p for p in renpy.list_files() if p.startswith("images/menu_assets/") and p.lower().endswith(exts))

    MENU_SLIDES = _discover_menu_slides()
    MENU_KB_TRANSFORMS = (
        "menu_kb_zoom_in", "menu_kb_zoom_out", "menu_kb_zoom_in_left",
        "menu_kb_zoom_out_right", "menu_kb_pan_up_zoom", "menu_kb_pan_down_zoom",
    )
    _menu_queue = []
    menu_current_slide = MENU_SLIDES[0] if MENU_SLIDES else "bg_menu"
    menu_prev_slide = None
    menu_kb_name = MENU_KB_TRANSFORMS[0]
    menu_prev_kb_name = MENU_KB_TRANSFORMS[0]
    menu_slide_tick = 0
    menu_prev_tick = -1

    def _next_from_queue():
        global _menu_queue
        if not MENU_SLIDES:
            return "bg_menu"
        if not _menu_queue:
            _menu_queue = list(MENU_SLIDES)
            random.shuffle(_menu_queue)
            if len(_menu_queue) > 1 and _menu_queue[0] == menu_current_slide:
                _menu_queue[0], _menu_queue[-1] = _menu_queue[-1], _menu_queue[0]
        return _menu_queue.pop(0)

    def advance_menu_slide():
        global menu_current_slide, menu_prev_slide, menu_kb_name, menu_prev_kb_name
        global menu_slide_tick, menu_prev_tick
        menu_prev_slide = menu_current_slide
        menu_prev_kb_name = menu_kb_name
        menu_prev_tick = menu_slide_tick
        menu_current_slide = _next_from_queue()
        choices = [t for t in MENU_KB_TRANSFORMS if t != menu_prev_kb_name] or list(MENU_KB_TRANSFORMS)
        menu_kb_name = random.choice(choices)
        menu_slide_tick += 1
        renpy.restart_interaction()

screen menu_slideshow_bg():
    timer 4.8 repeat True action Function(advance_menu_slide)
    fixed:
        xsize 1920
        ysize 1080
        # Crop left side, anchor to right side (xalign 1.0) so the main right card is always showcased
        if menu_prev_slide:
            add Transform(menu_prev_slide, xysize=(1920, 1080), xalign=1.0, yalign=0.5, fit="cover") at globals()[menu_prev_kb_name] id ("slide_" + str(menu_prev_tick))
        add Transform(menu_current_slide, xysize=(1920, 1080), xalign=1.0, yalign=0.5, fit="cover") at globals()[menu_kb_name], slide_fade_in id ("slide_" + str(menu_slide_tick))
