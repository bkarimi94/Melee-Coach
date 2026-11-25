"""Tests for the estimated damage-per-opening metric."""

from src.analysis.openings import Opening
from src.analysis.opening_damage import opening_damage, summarize_opening_damage


def make_opening(start_percent, end_percent):
    return Opening(
        attacker_index=0,
        defender_index=1,
        start_frame=100,
        start_percent=start_percent,
        end_frame=150,
        end_percent=end_percent,
        had_damage=True,
    )


def test_damage_per_opening():
    assert opening_damage(make_opening(20, 55)) == 35.0


def test_negative_or_missing_damage_is_not_counted():
    assert opening_damage(make_opening(55, 20)) == 0.0
    assert opening_damage(make_opening(None, 20)) == 0.0


def test_average_damage_per_opening():
    summary = summarize_opening_damage([
        make_opening(0, 20),
        make_opening(10, 40),
    ])
    assert summary["openings"] == 2
    assert summary["total_damage"] == 50.0
    assert summary["average_damage"] == 25.0


def test_empty_opening_list():
    assert summarize_opening_damage([])["average_damage"] is None
