"""Grounded LOLA storyline locations, cameras, and innocent-vs-shameless beats."""

STORY_LOCATIONS = (
    ("college", "campus_stairwell", "photorealistic sunlit college stairwell between lectures with metal lockers and bulletin boards"),
    ("college", "library_study_nook", "photorealistic evening university library oak table lit by a warm brass desk lamp"),
    ("college", "campus_club_fair", "photorealistic bustling college courtyard lined with folding club tables and string banners"),
    ("college", "lecture_hall_backrow", "photorealistic tiered university lecture hall back row with warm overhead sconces"),
    ("food_drink", "daily_grind_counter", "photorealistic warm-lit Daily Grind Cafe counter with espresso machine steam and pastry case"),
    ("food_drink", "street_food_alley", "photorealistic narrow night-market alley glowing with steamy food-cart bulbs and wet asphalt"),
    ("food_drink", "bakery_backroom_prep", "photorealistic cozy artisan bakery prep counter dusted with flour and morning window light"),
    ("home_lodging", "maya_tiny_kitchen", "photorealistic small lived-in apartment kitchen at dusk with city glow outside the window"),
    ("home_lodging", "laundromat_midnight", "photorealistic glowing midnight laundromat with stainless washers and warm pastel tile"),
    ("transport", "rainy_bus_shelter", "photorealistic rain-streaked downtown bus shelter reflecting passing neon headlights"),
    ("transport", "subway_turnstile", "photorealistic tiled underground metro station platform with warm ceiling strips"),
    ("public_places", "twilight_city_park", "photorealistic city park stone bench beneath glowing streetlamps and autumn leaves"),
    ("public_places", "cinema_lobby_neon", "photorealistic retro movie theater lobby with velvet ropes and warm marquee bulbs"),
    ("relationships", "rooftop_hangout_ledge", "photorealistic brick apartment rooftop parapet overlooking glittering downtown towers"),
    ("home_lodging", "maya_bedroom_mirror", "photorealistic cozy apartment bedroom with a tall wooden full-length mirror and warm fairy lights"),
    ("hobbies_outdoors", "gym_studio_mirror", "photorealistic sunlit neighborhood fitness studio with wall-to-wall mirrors, dumbbells, and yoga mats"),
    ("shops_markets", "boutique_fitting_mirror", "photorealistic vintage clothing boutique fitting corner with tri-fold gilt mirror and velvet curtain"),
    ("shops_markets", "late_night_corner_mart", "photorealistic corner convenience store aisle window at midnight with street lights"),
    ("shops_markets", "indie_bookstore_aisle", "photorealistic wood-shelved indie bookstore aisle with warm hanging pendant lamps"),
    ("shops_markets", "vintage_thrift_rack", "photorealistic sunlit vintage thrift boutique between denim racks and ornate mirrors"),
    ("social_events", "gallery_opening_corner", "photorealistic modern loft art gallery with concrete walls and warm track spotlights"),
    ("social_events", "neon_arcade_corner", "photorealistic retro-neon downtown arcade aisle with glowing cabinet reflections on dark carpet"),
    ("college", "campus_cafeteria_line", "photorealistic lively college dining hall with warm pendant lights and stainless food counters"),
    ("food_drink", "midnight_pizzeria_window", "photorealistic neighborhood pizza shop takeout window glowing warmly onto a quiet night sidewalk"),
)

STORY_CAMERAS = (
    "intimate low three-quarter perspective with natural foreground depth",
    "22-degree Dutch-tilt editorial medium shot",
    "dynamic over-the-shoulder foreshortened close-mid shot",
    "ground-level upshot emphasizing confident posture and environment scale",
    "wide-angle doorway/reflection shot framing Maya cleanly on solid ground",
    "table-level close-mid perspective with shallow photorealistic background bokeh",
    "low tracking-shot angle catching natural walking momentum",
    "high three-quarter angle looking slightly down across the scene",
)

STORY_BEATS = (
    "standing firmly on both feet, glancing sideways down the hall with an innocent 'who, me?' smile while pocketing a spare keycard, never looking at the camera",
    "leaning one hip solidly against the counter, batting her lashes innocently at the off-frame barista while negotiating a bold favor, eyes off-camera",
    "seated squarely with knees tucked, gazing thoughtfully out the window with a sweet angel-face hiding a sly, confident plan, no eye contact with camera",
    "walking with grounded mid-stride weight, looking ahead toward the crowd as she tosses her hair back with effortless swagger, gaze away from camera",
    "resting her chin on one hand with elbows planted firmly, peeking sideways over her notebook with wide innocent eyes and a mischievous half-wink off-frame",
    "counting folded bills with one hand on her hip, looking down at the cash with a playfully charming grin, never looking at the camera",
    "tucking a small notebook under her arm, tilting her head innocently toward a distant conversation while overhearing a juicy secret, gaze off-camera",
    "holding a takeout coffee cup steadily, gazing out toward the city skyline with playful, fearless con-artist confidence, no eye contact with lens",
    "adjusting one shoulder strap with deceptive sweetness while scanning the far side of the room, eyes directed away from the camera",
    "leaning casually on one elbow, looking sideways at someone off-frame with a disarming doe-eyed stare and a faint knowing smirk",
    "pausing mid-turn with fingers grazing her collarbone, looking down the street with innocent charm and bold intent, never looking at camera",
    "perched calmly on a sturdy stool with ankles crossed, biting her lower lip lightly while watching the door, gaze directed off-camera",
    "glancing sideways over dark sunglasses lowered slightly on her nose toward a passing stranger, wide innocent eyes peeking out off-frame",
    "standing relaxed with hands tucked behind her back, looking over her shoulder toward the balcony exit while hiding a shiny VIP pass, no eye contact",
    "leaning forward slightly over the railing, watching the street below with effortless allure and zero hesitation, never looking at the camera",
)

BODY_CONFIDENCE_ARC = (
    ("home_lodging", "bedroom_mirror_fit_check", "photorealistic cozy apartment bedroom with a tall wooden full-length mirror and warm bedside lamp",
     "standing side-profile in front of the tall bedroom mirror, glancing back over her shoulder at her silhouette and lower-body fit with a cute worried pout, never looking at the camera"),
    ("shops_markets", "boutique_mirror_hem_worry", "photorealistic vintage clothing boutique fitting corner with tri-fold gilt mirror and warm amber bulbs",
     "turning sideways before the tri-fold mirror, gently tugging the back hem of her oversized navy-blue t-shirt dress while worrying over her curves and silhouette, gaze fixed on the mirror"),
    ("hobbies_outdoors", "gym_studio_squat_check", "photorealistic neighborhood fitness studio with wall-to-wall mirrors, kettlebells, and warm afternoon sun",
     "hands resting on her hips in front of the gym mirror, eyeing her lower-body posture and curve proportions with dramatic mock-despair after skipping leg day, eyes off-camera"),
    ("home_lodging", "apartment_scale_dilemma", "photorealistic tiled apartment bathroom doorway with soft morning light and a digital floor scale nearby",
     "peeking sideways into the doorway mirror while pinching the side of her waist with a comical worried expression, debating late-night snacks, no eye contact with camera"),
    ("food_drink", "pizzeria_window_reflection", "photorealistic neighborhood pizza shop glass storefront glowing warmly at night, reflecting Maya's silhouette",
     "pausing outside the glass window holding a pizza slice box, catching her own side-profile reflection in the glass and sighing playfully about her curves, never looking at the camera"),
)

TRAPPED_ARC = (
    ("public_places", "stuck_elevator_car", "photorealistic vintage brass-and-wood apartment elevator cab stopped between floors with warm flickering ceiling light",
     "leaning back against the elevator handrail with one knee bent, eyeing the jammed floor indicator with a playful 'welp' grimace, never looking at the camera"),
    ("college", "locked_library_stack", "photorealistic after-hours university library aisle locked behind heavy glass doors lit by amber security lamps",
     "peeking past tall mahogany bookshelves while testing a locked brass latch with a mischievous 'uh-oh' expression, eyes directed off-camera"),
    ("relationships", "rooftop_door_jam", "photorealistic twilight apartment rooftop beside a heavy steel access door that clicked shut against the city skyline",
     "jiggling the locked rooftop door handle with one hand while holding a bent hairpin in the other, glancing sideways in mock-exasperation, no eye contact"),
    ("home_lodging", "laundromat_backroom_lock", "photorealistic midnight laundromat supply alcove with frosted glass door, stacked detergent jugs, and neon street glow",
     "peeking sideways through the frosted glass panel of the locked alcove toward the empty street, plotting an escape with a sly pout, gaze off-camera"),
    ("transport", "subway_maintenance_gate", "photorealistic empty underground metro corridor beside a pulled-down steel accordion gate after the last train",
     "perched calmly on her heels beside the closed station gate, resting her chin on one hand while looking down the tunnel for a night guard, never looking at the camera"),
)

TRAPPED_NIGHTOUT_ARC = (
    ("relationships", "locked_rooftop_chill", "photorealistic twilight brick rooftop terrace beside a jammed heavy steel door with city lights glittering behind her",
     "sitting calmly on a concrete ledge after getting locked out, holding a hand-rolled smoke between two fingers and a cold drink bottle in the other, exhaling sideways into the breeze, never looking at the camera"),
    ("social_events", "vip_backroom_lockin", "photorealistic dim velvet-booths nightclub VIP storage lounge after closing time with neon sign spill",
     "lounging casually on a leather crate beside a locked service door, swirling a cocktail glass while puffing a hand-rolled smoke with an unbothered sly grin, eyes off-camera"),
    ("general_scenes", "fire_escape_rain_trap", "photorealistic rain-slicked brick apartment fire escape landing with a latched window and glowing alley below",
     "leaning back against the iron railing under the awning, sipping from a chilled bottle and holding a glowing hand-rolled smoke while waiting out the jammed window, gaze away from camera"),
    ("home_lodging", "balcony_sliding_lockout", "photorealistic high-rise apartment balcony at midnight behind a locked glass sliding door overlooking neon streets",
     "perched on a patio chair with ankles crossed, lifting a glass to her lips while resting a hand-rolled smoke over the rail after locking herself out, no eye contact"),
    ("public_places", "alley_courtyard_gate", "photorealistic quiet brick downtown courtyard behind a padlocked wrought-iron gate lit by a single warm streetlamp",
     "leaning one shoulder against the brick wall beside the locked gate, tilting her head back with a slow exhale of smoke and a cold canned drink in hand, never looking at the camera"),
)
