# Custom easing warpers (replacing Ren'Py's stiff default ease/easein_quad).

init -1 python:
    import math

    @renpy.atl_warper
    def ease_expo_out(t):
        """Snappy start with silky exponential deceleration for UI entrances."""
        return 1.0 if t >= 1.0 else 1.0 - pow(2.0, -10.0 * t)

    @renpy.atl_warper
    def ease_quint_out(t):
        """Smooth quintic deceleration for modals, overlays, and crossfades."""
        return 1.0 - pow(1.0 - t, 5)

    @renpy.atl_warper
    def ease_sine_inout(t):
        """Gentle, inertia-matched sine curve for camera pans and Ken Burns."""
        return -(math.cos(math.pi * t) - 1.0) / 2.0
