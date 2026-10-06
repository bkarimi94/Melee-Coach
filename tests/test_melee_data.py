from src.melee_data import (
    get_character_name,
    get_stage_name
)


def test_falco_character_name():
    assert (
        get_character_name(20)
        == "Falco"
    )


def test_fox_character_name():
    assert (
        get_character_name(2)
        == "Fox"
    )


def test_dream_land_stage_name():
    assert (
        get_stage_name(28)
        == "Dream Land"
    )