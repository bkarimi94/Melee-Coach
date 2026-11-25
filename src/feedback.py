"""Generate simple, evidence-based observations about one match."""


def build_player_feedback(
    player_name,
    opk_results,
    neutral_results,
    damage_results=None,
    character=None,
    opponent_opk_results=None,
):
    """Return descriptive notes and a few clearly limited practice ideas."""
    feedback = []

    opk = opk_results["opk"]
    if opk is None:
        feedback.append(
            f"{player_name} did not record a kill, so OPK cannot be calculated."
        )
    else:
        feedback.append(
            f"{player_name} needed an average of {opk:.2f} openings per kill."
        )

    wins = neutral_results["neutral_wins"]
    total = neutral_results["neutral_opportunities"]
    ratio = neutral_results["neutral_win_ratio"]
    if ratio is None:
        feedback.append("Neutral Win Rate cannot be calculated for this match.")
    else:
        feedback.append(
            f"{player_name} won {wins} of {total} classified neutral wins "
            f"({100 * ratio:.1f}%)."
        )

    if damage_results is not None:
        average = damage_results["average_damage"]
        if average is None:
            feedback.append("No average opening damage is available for this match.")
        else:
            feedback.append(
                f"Estimated damage per opening was {average:.1f} percentage points."
            )

    if ratio is not None and total > 0 and ratio < 0.5:
        feedback.append(
            "Review the moments immediately before you lost neutral; look for "
            "repeated approaches or defensive habits."
        )

    if opponent_opk_results is not None:
        their_opk = opponent_opk_results["opk"]
        if opk is not None and their_opk is not None and opk > their_opk:
            feedback.append(
                "You needed more openings per kill than your opponent in this "
                "match. Review missed follow-ups and edgeguard situations."
            )

    if character and character.lower() == "falco" and ratio is not None and ratio < 0.5:
        feedback.append(
            "Falco review idea: check whether laser spacing and your next "
            "decision helped you safely start interactions."
        )

    return feedback