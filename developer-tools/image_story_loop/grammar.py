"""Small English helpers for filename-derived story narration."""

PAST = {
    "adjusting": "adjusted", "admiring": "admired", "arranging": "arranged",
    "arriving": "arrived", "asking": "asked", "attending": "attended",
    "balancing": "balanced", "bargaining": "bargained", "browsing": "browsed",
    "buying": "bought", "catching": "caught", "chasing": "chased",
    "checking": "checked", "choosing": "chose", "cleaning": "cleaned",
    "dancing": "danced", "delivering": "delivered", "drinking": "drank",
    "doing": "did", "eating": "ate", "entering": "entered", "fixing": "fixed",
    "holding": "held", "hiding": "hid", "interacting": "talked", "leaning": "leaned",
    "lacing": "laced", "kneading": "kneaded", "looking": "looked", "posing": "paused",
    "playing": "played", "pointing": "pointed", "pulling": "pulled", "reading": "read",
    "repairing": "repaired", "roasting": "roasted", "running": "ran", "shaping": "shaped",
    "skating": "skated", "sketching": "sketched", "sipping": "sipped", "smelling": "smelled",
    "smoking": "smoked", "sorting": "sorted", "standing": "stood", "stealing": "stole",
    "taking": "took", "talking": "talked", "testing": "tested", "throwing": "threw",
    "trimming": "trimmed", "using": "used", "waiting": "waited", "washing": "washed",
    "watching": "watched", "waving": "waved", "working": "worked",
}
MASS = {"coffee", "dough", "money", "music", "food", "work", "homework", "chili"}
ARTICLELESS = {"campus", "college", "home", "school", "work", "downtown"}
PLACE_NAMES = {"sushi": "the sushi bar", "tea": "the tea shop", "coffee": "the coffee shop",
               "juice": "the juice bar", "caf": "the cafe", "underground": "an underground kitchen",
               "lab": "the lab"}


def noun_phrase(words):
    phrase = " ".join(words)
    if phrase == "ramen":
        return "a bowl of ramen"
    plural = phrase.endswith("s") and not phrase.endswith(("us", "ss"))
    if not phrase or phrase in MASS or plural or phrase.startswith(("her ", "his ", "their ")):
        return phrase
    if phrase in {"phone", "bank balance", "textbook", "backpack", "watch", "resume"}:
        return "her " + phrase
    return ("an " if phrase[0] in "aeiou" else "a ") + phrase


def place_phrase(words):
    phrase = " ".join(words)
    if not phrase:
        return ""
    if phrase in PLACE_NAMES:
        return PLACE_NAMES[phrase]
    if phrase in ARTICLELESS or phrase.startswith(("the ", "a ", "an ")):
        return phrase
    return "the " + phrase


def past_verb(word):
    if word in PAST:
        return PAST[word]
    root = word[:-3] if word.endswith("ing") else word
    if root.endswith("e"):
        return root + "d"
    if root.endswith("y"):
        return root[:-1] + "ied"
    if len(root) > 2 and root[-1] not in "wxy" and root[-1] not in "aeiou" and root[-2] in "aeiou" and root[-3] not in "aeiou":
        root += root[-1]
    return root + "ed"
