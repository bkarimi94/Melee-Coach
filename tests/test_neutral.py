from src.analysis.neutral import (
    calculate_neutral_win_ratio,
    classify_openings_by_player,
)

from src.analysis.openings import (
    Opening,
)


def test_neutral_win_ratio():
    result = (
        calculate_neutral_win_ratio(
            neutral_wins=6,
            opponent_neutral_wins=2
        )
    )

    assert result == 0.75


def test_even_neutral_win_ratio():
    result = (
        calculate_neutral_win_ratio(
            neutral_wins=4,
            opponent_neutral_wins=4
        )
    )

    assert result == 0.5


def test_no_neutral_wins():
    result = (
        calculate_neutral_win_ratio(
            neutral_wins=0,
            opponent_neutral_wins=0
        )
    )

    assert result is None


def test_separate_openings_are_neutral_wins():
    player_0_opening = Opening(
        attacker_index=0,
        defender_index=1,
        start_frame=100,
        start_percent=0,
        end_frame=150,
        end_percent=20,
        had_damage=True
    )

    player_1_opening = Opening(
        attacker_index=1,
        defender_index=0,
        start_frame=300,
        start_percent=0,
        end_frame=350,
        end_percent=15,
        had_damage=True
    )

    openings_by_player = {
        0: [
            player_0_opening
        ],

        1: [
            player_1_opening
        ],
    }

    results = (
        classify_openings_by_player(
            openings_by_player
        )
    )

    assert (
        results[0]["neutral_wins"]
        == 1
    )

    assert (
        results[1]["neutral_wins"]
        == 1
    )


def test_overlapping_response_is_counter_attack():
    player_1_opening = Opening(
        attacker_index=1,
        defender_index=0,
        start_frame=100,
        start_percent=0,
        end_frame=200,
        end_percent=30,
        had_damage=True
    )

    player_0_opening = Opening(
        attacker_index=0,
        defender_index=1,
        start_frame=150,
        start_percent=0,
        end_frame=250,
        end_percent=25,
        had_damage=True
    )

    openings_by_player = {
        0: [
            player_0_opening
        ],

        1: [
            player_1_opening
        ],
    }

    results = (
        classify_openings_by_player(
            openings_by_player
        )
    )

    assert (
        results[1]["neutral_wins"]
        == 1
    )

    assert (
        results[0]["counter_attacks"]
        == 1
    )


def test_same_start_frame_is_trade():
    player_0_opening = Opening(
        attacker_index=0,
        defender_index=1,
        start_frame=100,
        start_percent=0,
        end_frame=150,
        end_percent=20,
        had_damage=True
    )

    player_1_opening = Opening(
        attacker_index=1,
        defender_index=0,
        start_frame=100,
        start_percent=0,
        end_frame=160,
        end_percent=15,
        had_damage=True
    )

    openings_by_player = {
        0: [
            player_0_opening
        ],

        1: [
            player_1_opening
        ],
    }

    results = (
        classify_openings_by_player(
            openings_by_player
        )
    )

    assert (
        results[0]["trades"]
        == 1
    )

    assert (
        results[1]["trades"]
        == 1
    )

    assert (
        results[0]["neutral_wins"]
        == 0
    )

    assert (
        results[1]["neutral_wins"]
        == 0
    )