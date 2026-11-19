# LOLA - Location catalog and read-only location queries.

init python:
    locations = {
        "home": {
            "name": "Home",
            "description": "Your small apartment. Not much, but it's yours.",
            "type": "home",
            "requires_money": None,
            "available_from_start": True,
        },
        "bus_stop": {
            "name": "Bus Stop",
            "description": "The corner where you catch the bus to college.",
            "type": "transit",
            "requires_money": 0,
            "available_from_start": True,
        },
        "college": {
            "name": "Campus",
            "description": "The college campus. Classes, library, and new people.",
            "type": "education",
            "requires_money": 0,
            "available_from_start": True,
        },
        "cafe": {
            "name": "The Daily Grind Cafe",
            "description": "A local cafe where you might find work.",
            "type": "work",
            "requires_money": 0,
            "available_from_start": True,
        },
        "street": {
            "name": "City Streets",
            "description": "Busy sidewalks, corner shops, and street markets.",
            "type": "public",
            "requires_money": 0,
            "available_from_start": True,
        },
        "library": {
            "name": "College Library",
            "description": "Quiet study space with books and computers.",
            "type": "education",
            "requires_money": 0,
            "available_from_start": False,
        },
        "park": {
            "name": "City Park",
            "description": "A green space in the city. Good for thinking.",
            "type": "leisure",
            "requires_money": 0,
            "available_from_start": False,
        },
    }

    def get_location(loc_id):
        return locations.get(loc_id)

    def get_location_name(loc_id):
        loc = get_location(loc_id)
        return loc["name"] if loc else loc_id

    def get_location_description(loc_id):
        loc = get_location(loc_id)
        return loc["description"] if loc else "{} location".format(loc_id)
