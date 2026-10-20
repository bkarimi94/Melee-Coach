from src.analysis.openings import (
    detect_openings,
    get_countable_openings,
)


def calculate_neutral_win_ratio(
    neutral_wins,
    opponent_neutral_wins
):
    """
    Calculate the player's share of
    all neutral wins in the game.

    Example:

    Player:
        6 neutral wins

    Opponent:
        2 neutral wins

    Neutral Win Ratio:
        6 / (6 + 2)
        = 0.75
        = 75%
    """

    total_neutral_wins = (
        neutral_wins
        + opponent_neutral_wins
    )

    if total_neutral_wins == 0:
        return None

    return (
        neutral_wins
        / total_neutral_wins
    )


def get_openings_by_player(game):
    """
    Detect the countable openings
    belonging to both players.

    Neutral-win analysis currently
    supports two-player singles matches.
    """

    if len(game.start.players) != 2:
        raise ValueError(
            "Neutral-win analysis currently "
            "supports two-player singles "
            "matches only."
        )

    openings_by_player = {}

    for player_index in (0, 1):
        detected_openings = (
            detect_openings(
                game,
                player_index
            )
        )

        countable_openings = (
            get_countable_openings(
                detected_openings
            )
        )

        openings_by_player[
            player_index
        ] = countable_openings

    return openings_by_player


def classify_openings_by_player(
    openings_by_player
):
    """
    Classify openings as:

    - neutral wins
    - counter-attacks
    - trades

    This follows the general conversion
    classification used by Slippi.
    """

    results = {}

    for player_index in (
        openings_by_player
    ):
        results[player_index] = {
            "neutral_wins": 0,
            "counter_attacks": 0,
            "trades": 0,
        }

    all_openings = []

    for player_index, openings in (
        openings_by_player.items()
    ):
        for opening in openings:
            all_openings.append(
                opening
            )

    openings_by_start_frame = {}

    for opening in all_openings:
        start_frame = (
            opening.start_frame
        )

        if (
            start_frame
            not in openings_by_start_frame
        ):
            openings_by_start_frame[
                start_frame
            ] = []

        openings_by_start_frame[
            start_frame
        ].append(
            opening
        )

    last_end_frame_by_defender = {}

    for start_frame in sorted(
        openings_by_start_frame
    ):
        openings = (
            openings_by_start_frame[
                start_frame
            ]
        )

        is_trade = (
            len(openings) >= 2
        )

        for opening in openings:
            if opening.end_frame is not None:
                last_end_frame_by_defender[
                    opening.defender_index
                ] = opening.end_frame

            if is_trade:
                results[
                    opening.attacker_index
                ]["trades"] += 1

                continue

            previous_opponent_end_frame = (
                last_end_frame_by_defender.get(
                    opening.attacker_index
                )
            )

            is_counter_attack = (
                previous_opponent_end_frame
                is not None
                and
                previous_opponent_end_frame
                > opening.start_frame
            )

            if is_counter_attack:
                results[
                    opening.attacker_index
                ][
                    "counter_attacks"
                ] += 1

            else:
                results[
                    opening.attacker_index
                ][
                    "neutral_wins"
                ] += 1

    return results


def analyze_neutral(
    game,
    player_index
):
    """
    Analyze neutral interactions for
    one player in a two-player match.
    """

    if player_index not in (0, 1):
        raise ValueError(
            "player_index must be 0 or 1."
        )

    openings_by_player = (
        get_openings_by_player(
            game
        )
    )

    classifications = (
        classify_openings_by_player(
            openings_by_player
        )
    )

    opponent_index = (
        1 - player_index
    )

    neutral_wins = (
        classifications[
            player_index
        ]["neutral_wins"]
    )

    opponent_neutral_wins = (
        classifications[
            opponent_index
        ]["neutral_wins"]
    )

    total_neutral_wins = (
        neutral_wins
        + opponent_neutral_wins
    )

    neutral_win_ratio = (
        calculate_neutral_win_ratio(
            neutral_wins,
            opponent_neutral_wins
        )
    )

    return {
        "neutral_wins":
            neutral_wins,

        "neutral_losses":
            opponent_neutral_wins,

        "neutral_opportunities":
            total_neutral_wins,

        "neutral_win_ratio":
            neutral_win_ratio,

        "counter_attacks":
            classifications[
                player_index
            ][
                "counter_attacks"
            ],

        "trades":
            classifications[
                player_index
            ][
                "trades"
            ],
    }