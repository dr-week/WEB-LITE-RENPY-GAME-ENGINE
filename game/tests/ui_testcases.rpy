testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 30.0
        $ _test.overwrite_screenshots = True
        if not screen "main_menu":
            run MainMenu(confirm=False)
        assert screen "main_menu"

    teardown:
        exit


testcase main_menu_settings_round_trip:
    pause 0.1
    screenshot "01_main_menu.png"
    click "Settings"
    assert screen "preferences"
    click "Return"
    assert screen "main_menu"


testcase new_game_save_load_navigation:
    click "New Game"
    advance until "Day 1 - Morning"
    pause 0.1
    screenshot "02_day1_morning.png"
    click "Good"
    click "Continue ▸"
    click "Status"
    assert screen "status"
    pause 0.1
    screenshot "04_status_dashboard.png"
    click "People"
    assert screen "character_info"
    pause 0.1
    screenshot "05_people_screen.png"
    click "Map"
    assert screen "world_map"
    pause 0.1
    screenshot "08_city_map.png"
    click "Save"
    assert screen "save"
    click "Return"
    click "Load"
    assert screen "load"
    click "Main Menu"
    if screen "confirm":
        click "Yes"
    assert screen "main_menu"


testcase starting_job_tracks_experience:
    $ previous_experience = work_experience
    $ work_experience = 0
    $ start_job(starter_job)
    assert eval("employment_state == 'employed' and work_experience == 1")
    $ end_job()
    $ work_experience = previous_experience


testcase day_one_route_reaches_day_two:
    click "New Game"
    advance until screen "choice"
    pause 0.1
    screenshot "03_day1_choices.png"
    click "Get ready quickly and dress sharp"
    advance until screen "choice"
    click "Review class notes on her phone while waiting"
    advance until screen "choice"
    click "Ask a friendly student for directions"
    advance until screen "choice"
    click "Introduce yourself warmly"
    advance until screen "choice"
    click "Pay full attention and outline every concept"
    advance until screen "choice"
    click "Go home early to rest and review her budget"
    advance until screen "choice"
    click "Go to sleep"
    advance until screen "choice"
    click "Continue to Day 2"
    advance until "Day 2 - Morning"
    advance until screen "choice"
    click "Review yesterday's notes before class"
    advance until screen "choice"
    click "Open Maya's City Journal (+Appeal)"
    advance until screen "choice"
    assert eval("image_story_options[0][0].startswith('Explore Campus & Study Lounges')")
    pause 0.1
    screenshot "07_city_journal.png"
    click "Back to Afternoon/Evening Planner"
    advance until screen "choice"
    pause 0.1
    screenshot "06_day2_planner.png"
