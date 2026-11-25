"""Classify detected offensive openings in two-player Melee matches."""

from src.analysis.openings import detect_openings, get_countable_openings


def calculate_neutral_win_ratio(neutral_wins, opponent_neutral_wins):
    """Return the fraction of all neutral wins earned by this player."""
    total = neutral_wins + opponent_neutral_wins
    return None if total == 0 else neutral_wins / total


def get_openings_by_player(game):
    """Return damage-producing openings for both singles players."""
    if len(game.start.players) != 2:
        raise ValueError("Neutral analysis supports two-player singles matches only.")
    return {
        index: get_countable_openings(detect_openings(game, index))
        for index in (0, 1)
    }


def classify_openings_by_player(openings_by_player):
    """Group openings into neutral wins, counter-attacks, and trades.

    A simultaneous opening is a trade. Otherwise, an opening that begins
    while the attacking player is already being punished is a counter-attack.
    Remaining openings are neutral wins. This is an approximation of the
    Slippi conversion-classification rules, not an exact SDK port.
    """
    results = {
        index: {"neutral_wins": 0, "counter_attacks": 0, "trades": 0}
        for index in (0, 1)
    }

    for player_index in (0, 1):
        for opening in openings_by_player.get(player_index, []):
            opponent_openings = openings_by_player.get(1 - player_index, [])
            start = opening.start_frame

            is_trade = any(
                other.start_frame == start for other in opponent_openings
            )
            was_being_punished = any(
                other.start_frame < start
                and (other.end_frame is None or start < other.end_frame)
                for other in opponent_openings
            )

            if is_trade:
                results[player_index]["trades"] += 1
            elif was_being_punished:
                results[player_index]["counter_attacks"] += 1
            else:
                results[player_index]["neutral_wins"] += 1

    return results


def analyze_neutral(game, player_index):
    """Calculate neutral statistics for player index 0 or 1."""
    if player_index not in (0, 1):
        raise ValueError("player_index must be 0 or 1.")

    classified = classify_openings_by_player(get_openings_by_player(game))
    own = classified[player_index]
    opponent = classified[1 - player_index]
    wins = own["neutral_wins"]
    losses = opponent["neutral_wins"]

    return {
        "neutral_wins": wins,
        "neutral_losses": losses,
        "neutral_opportunities": wins + losses,
        "neutral_win_ratio": calculate_neutral_win_ratio(wins, losses),
        "counter_attacks": own["counter_attacks"],
        "trades": own["trades"],
    }