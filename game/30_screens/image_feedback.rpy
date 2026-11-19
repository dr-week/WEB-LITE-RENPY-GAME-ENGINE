# Bottom-right Thumbs Up / Thumbs Down / Relocate image rating overlay and modal.

transform feedback_overlay_enter:
    subpixel True
    alpha 0.0 yoffset 8
    ease 0.25 alpha 1.0 yoffset 0

transform feedback_modal_enter:
    subpixel True
    alpha 0.0 zoom 0.94
    ease 0.22 alpha 1.0 zoom 1.0

screen image_feedback_overlay():
    zorder 105
    if not main_menu and not renpy.context()._menu:
        $ _active_asset = current_scene_image_path()
        if _active_asset:
            $ _rating = current_image_rating()
            hbox:
                at feedback_overlay_enter
                xalign 0.992
                yalign 0.992
                spacing 6
                button:
                    alt ("Liked" if _rating == "up" else "Good")
                    style ("feedback_up_active" if _rating == "up" else "feedback_btn")
                    at ui_hover_pop
                    action Function(record_image_feedback, _active_asset, "up", "", "keep")
                    hbox:
                        spacing 6
                        add Transform("images/ui/icons/thumb_up.png", xysize=(18, 18)) yalign 0.5
                        text ("Liked" if _rating == "up" else "Good") style ("feedback_up_active_text" if _rating == "up" else "feedback_btn_text")
                button:
                    alt ("Flagged" if _rating in ("down", "relocate", "remove") else "Review")
                    style ("feedback_down_active" if _rating in ("down", "relocate", "remove") else "feedback_btn")
                    at ui_hover_pop
                    action Show("image_feedback_modal", asset_path=_active_asset)
                    hbox:
                        spacing 6
                        add Transform("images/ui/icons/thumb_down.png", xysize=(18, 18)) yalign 0.5
                        text ("Flagged" if _rating in ("down", "relocate", "remove") else "Review") style ("feedback_down_active_text" if _rating in ("down", "relocate", "remove") else "feedback_btn_text")

screen image_feedback_modal(asset_path):
    modal True
    zorder 200
    add Solid("#050814c8")
    frame:
        at feedback_modal_enter
        xalign 0.5
        yalign 0.5
        xsize 620
        background Solid("#12172df5")
        padding (32, 26)
        vbox:
            spacing 14
            xfill True
            text _("Image Disposition & Problem") style "choice_hint_text"
            text "[asset_path]" style "feedback_path_text"
            null height 4
            text _("ACTION: WHAT SHOULD HAPPEN TO THIS IMAGE?") size 14 bold True color "#ffe8a3"
            hbox:
                spacing 12
                xfill True
                textbutton _("Replace Here\n(Regenerate)"):
                    style "feedback_action_choice_btn"
                    action [Function(record_image_feedback, asset_path, "down", "Needs Replacement Here", "replace"), Hide("image_feedback_modal")]
                textbutton _("Relocate / Move\n(Good, but wrong place)"):
                    style "feedback_action_choice_btn"
                    action [Function(record_image_feedback, asset_path, "down", "Good Art - Move To Different Scene", "relocate"), Hide("image_feedback_modal")]
                textbutton _("Completely Remove\n(Discard Asset)"):
                    style "feedback_action_choice_btn"
                    action [Function(record_image_feedback, asset_path, "down", "Remove Completely", "remove"), Hide("image_feedback_modal")]
            null height 6
            text _("OR SELECT SPECIFIC DEFECT:") size 14 bold True color "#d0c8e8"
            for reason in FEEDBACK_REASONS:
                textbutton reason:
                    style "feedback_reason_btn"
                    action [Function(record_image_feedback, asset_path, "down", reason, "replace"), Hide("image_feedback_modal")]
            textbutton _("Cancel"):
                style "feedback_cancel_btn"
                action Hide("image_feedback_modal")
