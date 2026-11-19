# Runtime image rating store with Replace / Relocate / Remove support.

default image_story_path = ""

init 1 python:
    import datetime
    import json
    import os
    import re

    if persistent.image_feedback is None:
        persistent.image_feedback = {}

    def _build_scene_alias_map():
        alias_map = {}
        pattern = re.compile(r'^\s*image\s+((?:bg|cg|scene)_[\w]+)\s*=.*?["\'](images/[^"\']+)["\']')
        for path in renpy.list_files():
            if not path.startswith("10_characters/") or not path.endswith(".rpy"):
                continue
            try:
                with renpy.open_file(path, encoding="utf-8") as handle:
                    for raw_line in handle:
                        line = raw_line.decode("utf-8", errors="ignore") if isinstance(raw_line, bytes) else raw_line
                        match = pattern.match(line)
                        if match:
                            alias_map[match.group(1)] = match.group(2)
            except Exception:
                pass
        return alias_map

    SCENE_ALIAS_MAP = _build_scene_alias_map()
    FEEDBACK_REASONS = (
        "Wrong character / outfit",
        "Bad anatomy / artifacts",
        "Wrong setting / location",
        "Low quality / blurry",
        "Style mismatch",
    )

    def current_scene_image_path():
        if image_story_path:
            return image_story_path if image_story_path.startswith("images/") else "images/" + image_story_path
        for tag in renpy.get_showing_tags(layer="master"):
            if tag in SCENE_ALIAS_MAP:
                return SCENE_ALIAS_MAP[tag]
        return ""

    def current_image_rating():
        asset = current_scene_image_path()
        if not asset or not isinstance(persistent.image_feedback, dict):
            return ""
        return persistent.image_feedback.get(asset, "")

    def record_image_feedback(asset_path, rating, reason="", disposition="replace"):
        """Records feedback with explicit disposition: 'keep', 'replace', 'relocate', or 'remove'."""
        if not asset_path or rating not in ("up", "down"):
            return
        if not isinstance(persistent.image_feedback, dict):
            persistent.image_feedback = {}
        persistent.image_feedback[asset_path] = disposition if rating == "down" else "up"
        _append_feedback_json(asset_path, rating, reason, disposition)
        if rating == "up":
            msg = "Image rated: Approved & Kept"
        elif disposition == "relocate":
            msg = "Marked for Relocation: Kept for other scenes"
        elif disposition == "remove":
            msg = "Marked for Removal: Discard from game"
        else:
            msg = "Marked for Replacement: New prompt queued"
        renpy.notify(msg)
        renpy.restart_interaction()

    def _append_feedback_json(asset_path, rating, reason, disposition):
        data_dir = os.path.join(config.gamedir, "data")
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)
        out_path = os.path.join(data_dir, "image_feedback.json")
        payload = {"schema_version": 2, "ratings": []}
        if os.path.isfile(out_path):
            try:
                with open(out_path, "r", encoding="utf-8") as handle:
                    loaded = json.load(handle)
                if isinstance(loaded, dict) and isinstance(loaded.get("ratings"), list):
                    payload = loaded
            except Exception:
                pass
        payload["ratings"].append({
            "asset_path": asset_path,
            "rating": rating,
            "reason": reason,
            "disposition": disposition,
            "scene_label": str(getattr(renpy.context(), "current", "") or ""),
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        })
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
