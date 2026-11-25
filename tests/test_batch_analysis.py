"""Tests for multi-replay summary logic."""

from types import SimpleNamespace

from src.batch_analysis import analyze_one_replay, flatten_match_results
from src.analysis.openings import Opening


def test_analyze_one_replay(monkeypatch):
    """Use fake parser results so this test does not require a .slp file."""
    import src.batch_analysis as batch

    game = SimpleNamespace(start=SimpleNamespace(players=[object(), object()]))
    monkeypatch.setattr(batch, "load_replay", lambda path, skip_frames: game)
    monkeypatch.setattr(batch, "create_match_summary", lambda game: {
        "player_1_name": "Buu",
        "player_1_character": "Falco",
        "player_2_name": "FoxUser",
        "player_2_character": "Fox",
        "stage": "Dream Land",
        "starting_stocks": 4,
        "timer_seconds": 480,
    })

    def fake_opk(game, index):
        opening = Opening(
            attacker_index=index,
            defender_index=1 - index,
            start_frame=100,
            start_percent=10.0,
            end_frame=180,
            end_percent=35.0,
            had_damage=True,
        )
        return {"openings": 1, "kills": 1, "opk": 1.0, "opening_details": [opening]}

    def fake_neutral(game, index):
        return {
            "neutral_wins": 1,
            "neutral_losses": 1,
            "neutral_opportunities": 2,
            "neutral_win_ratio": 0.5,
            "counter_attacks": 0,
            "trades": 0,
        }

    monkeypatch.setattr(batch, "analyze_opk", fake_opk)
    monkeypatch.setattr(batch, "analyze_neutral", fake_neutral)

    result = analyze_one_replay("sample_data/test_game.slp")
    assert result["players"][0]["name"] == "Buu"
    assert result["players"][0]["damage"]["average_damage"] == 25.0
    assert len(result["players"][0]["feedback"]) >= 3

    rows = flatten_match_results([result])
    assert len(rows) == 2
    assert rows[0]["OPK"] == 1.0
    assert rows[1]["Neutral Win Rate (%)"] == 50.0
