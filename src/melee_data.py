CHARACTER_NAMES = {
    0: "Captain Falcon",
    1: "Donkey Kong",
    2: "Fox",
    3: "Mr. Game & Watch",
    4: "Kirby",
    5: "Bowser",
    6: "Link",
    7: "Luigi",
    8: "Mario",
    9: "Marth",
    10: "Mewtwo",
    11: "Ness",
    12: "Peach",
    13: "Pikachu",
    14: "Ice Climbers",
    15: "Jigglypuff",
    16: "Samus",
    17: "Yoshi",
    18: "Zelda",
    19: "Sheik",
    20: "Falco",
    21: "Young Link",
    22: "Dr. Mario",
    23: "Roy",
    24: "Pichu",
    25: "Ganondorf",
}


STAGE_NAMES = {
    2: "Fountain of Dreams",
    3: "Pokémon Stadium",
    8: "Yoshi's Story",
    28: "Dream Land",
    31: "Battlefield",
    32: "Final Destination",
}


def get_character_name(character_id):
    return CHARACTER_NAMES.get(
        character_id,
        f"Unknown Character ({character_id})"
    )


def get_stage_name(stage_id):
    return STAGE_NAMES.get(
        stage_id,
        f"Unknown Stage ({stage_id})"
    )