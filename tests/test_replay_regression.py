"""Compare the original example replay to previously checked Slippi results."""

from pathlib import Path

import pytest

from src.batch_analysis import analyze_one_replay

REPLAY = Path("sample_data/test_game.slp")
pytestmark = pytest.mark.skipif(not REPLAY.exists(), reason="Original .slp file not installed")


def test_original_replay_opk():
    match = analyze_one_replay(REPLAY)
    falco, fox = match["players"]
    assert falco["opk"]["openings"] == 9
    assert falco["opk"]["kills"] == 2
    assert falco["opk"]["opk"] == 4.5
    assert fox["opk"]["openings"] == 11
    assert fox["opk"]["kills"] == 4
    assert fox["opk"]["opk"] == 2.75


def test_original_replay_neutral_wins():
    match = analyze_one_replay(REPLAY)
    falco, fox = match["players"]
    assert falco["neutral"]["neutral_wins"] == 2
    assert fox["neutral"]["neutral_wins"] == 6
