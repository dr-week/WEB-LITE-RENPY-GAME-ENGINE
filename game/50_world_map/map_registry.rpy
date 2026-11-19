# Symmetrical 3x3 sector map registry for Solis Bay (3840x2160, 1280x720 per sector).

init python:
    CITY_NAME = "Solis Bay"
    CITY_TAGLINE = "All-Terrain Coastal College City"
    MAP_CANVAS_SIZE = (3840, 2160)

    MAP_TERRAIN_ZONES = {
        "sector_1_1_nw": "Pinecrest Ridge & Viewpoint",
        "sector_1_2_nc": "Observation Tower Plaza",
        "sector_1_3_ne": "University & School Campus",
        "sector_2_1_w": "Brickwood Apartments & Transit Hub",
        "sector_2_2_c": "Midtown Market & Cafe Plaza",
        "sector_2_3_e": "College Library & Study Commons",
        "sector_3_1_sw": "Old Dockside Tenements (Slum Quarter)",
        "sector_3_2_sc": "Solis Harbor & Waterfront Piers",
        "sector_3_3_se": "Botanical Gardens & Emerald Park",
    }

    MAP_PINS = {
        "viewpoint": {"x": 640, "y": 360, "zone": "sector_1_1_nw", "terrain": "Mountain Viewpoint", "links": ["tower", "home"], "route": "location_public"},
        "tower": {"x": 1920, "y": 360, "zone": "sector_1_2_nc", "terrain": "Observation Tower", "links": ["viewpoint", "college", "cafe"], "route": "location_public"},
        "college": {"x": 3200, "y": 360, "zone": "sector_1_3_ne", "terrain": "School & Campus", "links": ["tower", "library"], "route": "location_college"},
        "home": {"x": 460, "y": 1080, "zone": "sector_2_1_w", "terrain": "Apartments", "links": ["bus_stop", "viewpoint", "slum_quarter"], "route": "location_home"},
        "bus_stop": {"x": 880, "y": 1080, "zone": "sector_2_1_w", "terrain": "Bus & Rail Hub", "links": ["home", "street"], "route": "location_transit"},
        "street": {"x": 1720, "y": 1140, "zone": "sector_2_2_c", "terrain": "Market Street", "links": ["bus_stop", "cafe", "harbor_pier"], "route": "location_public"},
        "cafe": {"x": 2120, "y": 980, "zone": "sector_2_2_c", "terrain": "Cafe Plaza", "links": ["street", "tower", "library"], "route": "location_work"},
        "library": {"x": 3200, "y": 1080, "zone": "sector_2_3_e", "terrain": "College Library", "links": ["college", "cafe", "park"], "route": "location_college"},
        "slum_quarter": {"x": 640, "y": 1800, "zone": "sector_3_1_sw", "terrain": "Old Tenements", "links": ["home", "harbor_pier"], "route": "location_public"},
        "harbor_pier": {"x": 1920, "y": 1800, "zone": "sector_3_2_sc", "terrain": "Harbor Waterfront", "links": ["slum_quarter", "street", "park"], "route": "location_public"},
        "park": {"x": 3200, "y": 1800, "zone": "sector_3_3_se", "terrain": "Botanical Gardens", "links": ["library", "harbor_pier"], "route": "location_public"},
    }

    def register_map_location(loc_id, x, y, zone, terrain, links, route="location_public"):
        """Register or update a map pin inside any 3x3 sector."""
        MAP_PINS[loc_id] = {"x": int(x), "y": int(y), "zone": zone, "terrain": terrain, "links": list(links), "route": route}

    def get_map_pin(loc_id):
        return MAP_PINS.get(loc_id)

    def get_connected_links(loc_id):
        pin = MAP_PINS.get(loc_id)
        return pin.get("links", []) if pin else []

    def get_map_lighting_tint(slot="afternoon", season="spring"):
        tints = {"morning": "#fff0d8", "afternoon": "#ffffff", "evening": "#e89b8e", "night": "#5c6ba8"}
        return tints.get(str(slot).lower(), "#ffffff")
