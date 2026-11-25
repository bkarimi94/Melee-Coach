"""Tests for descriptive coaching feedback."""

from src.feedback import build_player_feedback


def example_opk(value=4.5):
    return {"openings": 9, "kills": 2, "opk": value}


def example_neutral(wins=2, losses=6):
    total = wins + losses
    return {
        "neutral_wins": wins,
        "neutral_losses": losses,
        "neutral_opportunities": total,
        "neutral_win_ratio": wins / total if total else None,
        "counter_attacks": 1,
        "trades": 0,
    }


def test_basic_feedback():
    messages = build_player_feedback("Buu", example_opk(), example_neutral())
    assert "4.50 openings" in messages[0]
    assert "2 of 8 classified neutral wins" in messages[1]
    assert any("Review the moments" in note for note in messages)


def test_no_kill_or_neutral_win():
    messages = build_player_feedback(
        "Player", example_opk(None), example_neutral(0, 0)
    )
    assert "cannot be calculated" in messages[0]
    assert "cannot be calculated" in messages[1]


def test_falco_feedback_uses_comparison():
    messages = build_player_feedback(
        "Buu", example_opk(4.5), example_neutral(2, 6),
        damage_results={"average_damage": 26.0},
        character="Falco",
        opponent_opk_results=example_opk(2.75),
    )
    assert any("laser spacing" in note for note in messages)
    assert any("more openings per kill" in note for note in messages)
    assert any("26.0 percentage points" in note for note in messages)
