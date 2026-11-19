# Visual & Audio Transforms for Persona / Danganronpa-style Iconic UI
init -1:
    transform persona_choice_pop:
        on hover:
            easein 0.12 zoom 1.04 xoffset 12
        on idle:
            easeout 0.12 zoom 1.0 xoffset 0

    transform icon_pulse:
        zoom 1.0
        ease 1.2 zoom 1.15
        ease 1.2 zoom 1.0
        repeat

    transform wheel_icon_intro:
        alpha 0.0 zoom 0.7
        easein 0.18 alpha 1.0 zoom 1.0

    transform radial_slice_hover:
        on hover:
            easein 0.15 zoom 1.08
        on idle:
            easeout 0.15 zoom 1.0
