"""Tests for neutral-win and counter-attack classification."""

from src.analysis.neutral import calculate_neutral_win_ratio, classify_openings_by_player
from src.analysis.openings import Opening


def make_opening(attacker, start, end):
    """Create a short dummy opening without loading an actual Slippi file."""
    return Opening(
        attacker_index=attacker,
        defender_index=1 - attacker,
        start_frame=start,
        start_percent=0.0,
        end_frame=end,
        end_percent=20.0,
        had_damage=True,
    )


def test_neutral_win_ratio():
    assert calculate_neutral_win_ratio(6, 2) == 0.75
    assert calculate_neutral_win_ratio(0, 0) is None


def test_separate_openings_count_as_neutral_wins():
    results = classify_openings_by_player({
        0: [make_opening(0, 100, 120)],
        1: [make_opening(1, 200, 230)],
    })
    assert results[0]["neutral_wins"] == 1
    assert results[1]["neutral_wins"] == 1


def test_opening_during_opponents_punish_is_counter_attack():
    results = classify_openings_by_player({
        0: [make_opening(0, 150, 220)],
        1: [make_opening(1, 100, 200)],
    })
    assert results[0]["counter_attacks"] == 1
    assert results[0]["neutral_wins"] == 0
    assert results[1]["neutral_wins"] == 1


def test_simultaneous_openings_are_trades():
    results = classify_openings_by_player({
        0: [make_opening(0, 100, 150)],
        1: [make_opening(1, 100, 160)],
    })
    assert results[0]["trades"] == 1
    assert results[1]["trades"] == 1
    assert results[0]["neutral_wins"] == 0
    assert results[1]["neutral_wins"] == 0
