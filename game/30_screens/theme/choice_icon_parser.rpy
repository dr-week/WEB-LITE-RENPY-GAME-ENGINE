# LOLA - Iconic Choice Screen Renderer
# Automatically parses [charm], [logic], [cash], [stealth], [danger] tags into icons
init -3 python:
    def parse_choice_icon(caption):
        """Returns tuple of (icon_path, cleaned_caption)."""
        tags = {
            "[charm]": ("images/ui/icons/appeal.png", "#ff4081"),
            "[logic]": ("images/ui/icons/intelligence.png", "#00e5ff"),
            "[cash]": ("images/ui/icons/cash.png", "#00e676"),
            "[energy]": ("images/ui/icons/energy.png", "#ffd600"),
            "[danger]": ("images/ui/icons/warning.png", "#ff1744"),
            "[target]": ("images/ui/icons/target.png", "#d500f9"),
            "[social]": ("images/ui/icons/people.png", "#2979ff"),
            "[quest]": ("images/ui/extracted/diary_button_icon_quest.webp", "#ffab00"),
        }
        for tag, (icon, color) in tags.items():
            if caption.lower().startswith(tag):
                clean_text = caption[len(tag):].strip()
                return (icon, clean_text, color)
        # Default fallback icon
        return ("images/ui/icons/target.png", caption, "#b388ff")
