# LOLA Ren'Py 8.6.0 Initial Lint Report

**Date:** 2026-11-13
**SDK:** Ren'Py 8.6.0 pre-release
**Project:** C:\amd\aa\ASD\daa\GAME\LALALAND\LOLA\LOLA
**Exit Code:** 1 (errors found)

## Lint Output (stdout)

`

File "game/00_systems/college_manager.rpy", line 10: invalid syntax
    default college_course = "General Studies"
                ^^^^^^^^^^^^^^

File "game/30_screens/navigation.rpy", line 30: The text statement is not a valid child of the imagebutton statement.
    text get_location_name(loc_id) style "map_button_text"
        ^
ï»¿
`

## Lint Output (stderr)

`
Traceback (most recent call last):
  File "C:/RenPy/renpy-8.6.0/renpy-8.6.0-sdk/renpy/script.py", line 887, in load_file
    with open(rpycfn, "wb") as f:
         ^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied: 'C:/amd/aa/ASD/daa/GAME/LALALAND/LOLA/LOLA/game/tl/None/common.rpymc'
ï»¿
`

## Findings Summary

### Blocking Errors (2)

1. **college_manager.rpy line 10** - Invalid syntax on default statement
2. **navigation.rpy line 30** - Invalid screen child element

### Non-Blocking Issues (1)

1. **Permission denied** - tl/None/common.rpymc cache write error (likely benign)

## Next Steps

Fix the two blocking errors before re-running lint.

