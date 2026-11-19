# Memory pre-caching configuration and predictive preloading helpers.

define config.image_cache_size_mb = 512

init 2 python:
    def precache_images(paths, limit=8):
        """Queue upcoming image paths into Ren'Py's predictive RAM cache."""
        queued = [p for p in paths[:limit] if isinstance(p, str) and p]
        if queued:
            renpy.start_predict(*queued)

    def clear_precached_images(paths):
        for p in paths:
            if isinstance(p, str) and p:
                renpy.stop_predict(p)

    if "MENU_SLIDES" in globals() and MENU_SLIDES:
        precache_images(MENU_SLIDES, limit=6)
