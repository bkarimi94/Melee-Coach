"""Estimate damage gained during each detected offensive opening."""

from src.analysis.openings import analyze_opk


def opening_damage(opening):
    """Return the increase in defender percent during one opening.

    This is an approximation, because the ending hit of a kill or other
    special replay situations may not be fully represented by end_percent.
    """
    if opening.start_percent is None or opening.end_percent is None:
        return 0.0
    return max(0.0, float(opening.end_percent) - float(opening.start_percent))


def summarize_opening_damage(openings):
    """Calculate total and average damage across countable openings."""
    amounts = [opening_damage(opening) for opening in openings]
    count = len(amounts)
    total = sum(amounts)
    return {
        "openings": count,
        "total_damage": round(total, 2),
        "average_damage": round(total / count, 2) if count else None,
    }


def analyze_opening_damage(game, player_index):
    """Calculate estimated opening damage for a player in one replay."""
    opk = analyze_opk(game, player_index)
    return summarize_opening_damage(opk["opening_details"])