# Continuous Vinyl Rotation and Hover Transparency Transforms
init -1:
    transform cd_spin_continuous:
        subpixel True
        rotate 0
        linear 3.5 rotate 360
        repeat

    transform cd_hud_fader:
        on idle:
            easein 0.35 alpha 0.38 zoom 0.95
        on hover:
            easein 0.20 alpha 1.0 zoom 1.05

    transform cd_hover_tooltip:
        alpha 0.0 yoffset 6
        easein 0.15 alpha 1.0 yoffset 0
