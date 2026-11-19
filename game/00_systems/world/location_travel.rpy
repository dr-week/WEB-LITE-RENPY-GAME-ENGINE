# LOLA - Location availability, travel, and unlock actions.

init python:
    def is_location_available(loc_id):
        loc = get_location(loc_id)
        if not loc:
            return False
        if not loc.get("available_from_start", False):
            return traveled_to.get(loc_id, False)
        return True

    def is_location_unlocked(loc_id):
        return traveled_to.get(loc_id, False)

    def travel_to(location_id):
        global current_location
        if not is_location_available(location_id):
            return False
        current_location = location_id
        traveled_to[location_id] = True
        return True

    def unlock_location(location_id):
        if location_id in locations:
            traveled_to[location_id] = True
            return True
        return False

    def get_available_locations():
        return [loc_id for loc_id, data in locations.items()
                if data.get("available_from_start", False) or
                traveled_to.get(loc_id, False)]

    def can_afford_location(loc_id):
        loc = get_location(loc_id)
        if not loc:
            return False
        cost = loc.get("requires_money")
        return cost is None or money >= cost
