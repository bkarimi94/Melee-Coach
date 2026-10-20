def build_player_feedback(
    player_name,
    opk_results,
    neutral_results
):
    """
    Build simple descriptive feedback
    from the gameplay statistics
    currently supported by Melee Coach.

    More advanced coaching rules can
    be added later after enough data
    has been collected to justify
    meaningful thresholds.
    """

    feedback = []

    opk = (
        opk_results[
            "opk"
        ]
    )

    if opk is None:
        feedback.append(
            f"{player_name} did not "
            f"record a kill, so "
            f"Openings Per Kill cannot "
            f"be calculated."
        )

    else:
        feedback.append(
            f"{player_name} required "
            f"an average of "
            f"{opk:.2f} openings "
            f"for each kill."
        )

    neutral_wins = (
        neutral_results[
            "neutral_wins"
        ]
    )

    neutral_opportunities = (
        neutral_results[
            "neutral_opportunities"
        ]
    )

    neutral_win_ratio = (
        neutral_results[
            "neutral_win_ratio"
        ]
    )

    if neutral_win_ratio is None:
        feedback.append(
            f"No neutral wins were "
            f"recorded for either player, "
            f"so a neutral win rate "
            f"cannot be calculated."
        )

    else:
        neutral_percentage = (
            neutral_win_ratio
            * 100
        )

        feedback.append(
            f"{player_name} won "
            f"{neutral_wins} of "
            f"{neutral_opportunities} "
            f"neutral interactions "
            f"({neutral_percentage:.2f}%)."
        )

    return feedback