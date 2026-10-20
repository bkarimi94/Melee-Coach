from src.feedback import (
    build_player_feedback,
)


def test_feedback_with_opk_and_neutral():
    opk_results = {
        "openings": 9,
        "kills": 2,
        "opk": 4.5,
    }

    neutral_results = {
        "neutral_wins": 2,
        "neutral_losses": 6,
        "neutral_opportunities": 8,
        "neutral_win_ratio": 0.25,
        "counter_attacks": 6,
        "trades": 1,
    }

    feedback = (
        build_player_feedback(
            "Buu",
            opk_results,
            neutral_results
        )
    )

    assert len(feedback) == 2

    assert (
        "4.50 openings"
        in feedback[0]
    )

    assert (
        "2 of 8 neutral interactions"
        in feedback[1]
    )

    assert (
        "25.00%"
        in feedback[1]
    )


def test_feedback_with_no_kills():
    opk_results = {
        "openings": 5,
        "kills": 0,
        "opk": None,
    }

    neutral_results = {
        "neutral_wins": 3,
        "neutral_losses": 2,
        "neutral_opportunities": 5,
        "neutral_win_ratio": 0.6,
        "counter_attacks": 0,
        "trades": 0,
    }

    feedback = (
        build_player_feedback(
            "Player",
            opk_results,
            neutral_results
        )
    )

    assert (
        "cannot be calculated"
        in feedback[0]
    )


def test_feedback_with_no_neutral_wins():
    opk_results = {
        "openings": 4,
        "kills": 2,
        "opk": 2.0,
    }

    neutral_results = {
        "neutral_wins": 0,
        "neutral_losses": 0,
        "neutral_opportunities": 0,
        "neutral_win_ratio": None,
        "counter_attacks": 0,
        "trades": 0,
    }

    feedback = (
        build_player_feedback(
            "Player",
            opk_results,
            neutral_results
        )
    )

    assert (
        "cannot be calculated"
        in feedback[1]
    )