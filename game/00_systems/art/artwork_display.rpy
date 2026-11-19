# Aspect-ratio-safe presentation for full-frame scene and CG artwork.

init python:
    def fit_scene_art(source, matte="#101522"):
        width = config.screen_width
        height = config.screen_height
        return Fixed(
            Solid(matte, xysize=(width, height)),
            Transform(
                source,
                xysize=(width, height),
                fit="contain",
                xalign=0.5,
                yalign=0.5,
            ),
            xsize=width,
            ysize=height,
        )
