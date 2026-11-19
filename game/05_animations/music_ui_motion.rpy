# Sleek subpixel animations for the compact vinyl disc & hover music pill.

transform music_disc_hover:
    subpixel True
    on hover:
        warp ease_expo_out 0.18 zoom 1.14
    on idle:
        warp ease_quint_out 0.20 zoom 1.0

transform music_pill_pop:
    subpixel True
    alpha 0.0 xoffset -10
    warp ease_expo_out 0.22 alpha 1.0 xoffset 0

transform music_title_shimmer:
    subpixel True
    alpha 0.85
    warp ease_sine_inout 1.6 alpha 1.0 xoffset 2
    warp ease_sine_inout 1.6 alpha 0.80 xoffset 0
    repeat
