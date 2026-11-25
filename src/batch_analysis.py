"""Analyze one or several Slippi replay files and prepare summary rows."""

from pathlib import Path

from src.analysis.neutral import analyze_neutral
from src.analysis.opening_damage import summarize_opening_damage
from src.analysis.openings import analyze_opk
from src.feedback import build_player_feedback
from src.match_summary import create_match_summary
from src.replay_parser import load_replay


def analyze_one_replay(path):
    """Load a singles replay and build statistics for both players."""
    game = load_replay(Path(path), skip_frames=False)
    if len(game.start.players) != 2:
        raise ValueError("Only two-player singles replays are supported.")

    summary = create_match_summary(game)
    players = []

    for index in (0, 1):
        name = summary[f"player_{index + 1}_name"] or f"Player {index + 1}"
        character = summary[f"player_{index + 1}_character"]
        opk = analyze_opk(game, index)
        neutral = analyze_neutral(game, index)
        damage = summarize_opening_damage(opk["opening_details"])
        players.append({
            "name": name,
            "character": character,
            "opk": opk,
            "neutral": neutral,
            "damage": damage,
        })

    for index in (0, 1):
        player = players[index]
        opponent = players[1 - index]
        player["feedback"] = build_player_feedback(
            player["name"],
            player["opk"],
            player["neutral"],
            damage_results=player["damage"],
            character=player["character"],
            opponent_opk_results=opponent["opk"],
        )

    return {
        "filename": Path(path).name,
        "summary": summary,
        "players": players,
    }


def analyze_many_replays(paths):
    """Analyze files independently, collecting errors without aborting all."""
    matches = []
    errors = []
    for path in paths:
        try:
            matches.append(analyze_one_replay(path))
        except (OSError, ValueError, RuntimeError, AttributeError) as error:
            errors.append(f"{Path(path).name}: {error}")
    return matches, errors


def flatten_match_results(matches):
    """Convert structured results into one flat row per player and replay."""
    rows = []
    for match in matches:
        for player in match["players"]:
            neutral = player["neutral"]
            ratio = neutral["neutral_win_ratio"]
            rows.append({
                "Replay": match["filename"],
                "Player": player["name"],
                "Character": player["character"],
                "Stage": match["summary"]["stage"],
                "Openings": player["opk"]["openings"],
                "Kills": player["opk"]["kills"],
                "OPK": player["opk"]["opk"],
                "Neutral Wins": neutral["neutral_wins"],
                "Neutral Losses": neutral["neutral_losses"],
                "Neutral Win Rate (%)": round(100 * ratio, 2) if ratio is not None else None,
                "Counter-attacks": neutral["counter_attacks"],
                "Trades": neutral["trades"],
                "Avg. Damage per Opening": player["damage"]["average_damage"],
            })
    return rows