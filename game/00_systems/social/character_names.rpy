# LOLA - Provisional character name pools and unique-name selection.

init python:
    first_names_female = [
        "Maya", "Elena", "Zara", "Lily", "Aria",
        "Nora", "Chloe", "Emma", "Sophia", "Olivia",
        "Ava", "Isabella", "Mia", "Charlotte", "Amelia",
    ]
    first_names_male = [
        "Alex", "Jordan", "Noah", "Liam", "Ethan",
        "Mason", "Logan", "Lucas", "Oliver", "Elijah",
        "James", "William", "Benjamin", "Lucas", "Henry",
    ]
    surnames = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    ]

    def generate_name(gender="any"):
        if gender == "female":
            pool = first_names_female
        elif gender == "male":
            pool = first_names_male
        else:
            pool = first_names_female + first_names_male
        available = [name for name in pool if name not in used_names]
        if not available:
            first = pool[renpy.random.randint(0, len(pool) - 1)]
            last = surnames[renpy.random.randint(0, len(surnames) - 1)]
            return "{} {}".format(first, last)
        name = available[renpy.random.randint(0, len(available) - 1)]
        used_names.add(name)
        return name
