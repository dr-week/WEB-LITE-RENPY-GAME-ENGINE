"""Stable identity shared by story requests and generated image sidecars."""

import hashlib


def story_request_id(source, label, dialogue):
    identity = f"{source}|{label}|{dialogue.casefold()}"
    return "story_" + hashlib.sha1(identity.encode("utf-8")).hexdigest()[:10]
