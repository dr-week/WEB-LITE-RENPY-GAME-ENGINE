# Situational atmospheric overlays (rain, dust motes, neon bokeh, night tint).

image fx_rain = SnowBlossom(
    Solid("#b8d4ff78", xysize=(2, 22)),
    count=90, xspeed=(-35, -15), yspeed=(650, 950), start=30
)

image fx_dust_motes = SnowBlossom(
    Solid("#ffe8a355", xysize=(5, 5)),
    count=32, xspeed=(-14, 18), yspeed=(-12, 16), start=25
)

image fx_neon_bokeh = SnowBlossom(
    Solid("#d8b4f833", xysize=(14, 14)),
    count=20, xspeed=(-10, 10), yspeed=(-18, -6), start=20
)

default active_fx_override = None

init python:
    def current_situational_fx():
        if active_fx_override:
            return active_fx_override
        if time_slot in ("evening", "night") and current_location in ("street", "bus_stop", "park"):
            return "fx_neon_bokeh"
        if current_location in ("library", "cafe", "home"):
            return "fx_dust_motes"
        return None

screen situational_fx_overlay():
    zorder 50
    if not main_menu and not renpy.context()._menu:
        $ _fx = current_situational_fx()
        if _fx:
            add _fx
        if time_slot == "night":
            add Solid("#0a0e1f28", xysize=(1920, 1080))
