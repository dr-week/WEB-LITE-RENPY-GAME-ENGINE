# Persistent non-repeating database for story images and random prologue starts.

init python:
    import random

    if persistent.seen_story_images is None:
        persistent.seen_story_images = []
    if persistent.seen_prologue_starts is None:
        persistent.seen_prologue_starts = []

    def mark_story_image_seen(asset_id):
        if not asset_id:
            return
        if not isinstance(persistent.seen_story_images, list):
            persistent.seen_story_images = []
        if asset_id not in persistent.seen_story_images:
            persistent.seen_story_images.append(asset_id)

    def pick_unseen_entry(entries, seen_list, key="id"):
        if not entries:
            return None
        seen = set(seen_list or [])
        unseen = [e for e in entries if e.get(key) not in seen]
        if not unseen:
            if isinstance(seen_list, list):
                seen_list[:] = []
            unseen = list(entries)
        chosen = random.choice(unseen)
        if isinstance(seen_list, list) and chosen.get(key):
            seen_list.append(chosen[key])
        return chosen
