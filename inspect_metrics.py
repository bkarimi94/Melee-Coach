import sys
from pathlib import Path

from src.analysis.neutral import (
    analyze_neutral,
)

from src.analysis.openings import (
    analyze_opk,
)

from src.match_summary import (
    create_match_summary,
)

from src.replay_parser import (
    load_replay,
)


def print_player_metrics(
    game,
    summary,
    player_index
):
    """
    Print the currently implemented
    gameplay statistics for one player.
    """

    opk_results = analyze_opk(
        game,
        player_index
    )

    neutral_results = (
        analyze_neutral(
            game,
            player_index
        )
    )

    if player_index == 0:
        player_name = (
            summary[
                "player_1_name"
            ]
        )

        character = (
            summary[
                "player_1_character"
            ]
        )

    else:
        player_name = (
            summary[
                "player_2_name"
            ]
        )

        character = (
            summary[
                "player_2_character"
            ]
        )

    print(
        "=============================="
    )

    print(
        f"{player_name} "
        f"({character})"
    )

    print(
        "=============================="
    )

    print(
        "Openings:",
        opk_results["openings"]
    )

    print(
        "Kills:",
        opk_results["kills"]
    )

    if opk_results["opk"] is None:
        print(
            "Openings Per Kill: N/A"
        )

    else:
        print(
            "Openings Per Kill:",
            round(
                opk_results["opk"],
                2
            )
        )

    print()

    print(
        "Neutral Wins:",
        neutral_results[
            "neutral_wins"
        ]
    )

    print(
        "Neutral Losses:",
        neutral_results[
            "neutral_losses"
        ]
    )

    print(
        "Total Neutral Interactions:",
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
        print(
            "Neutral Win Rate: N/A"
        )

    else:
        print(
            "Neutral Win Rate:",
            f"{neutral_win_ratio * 100:.2f}%"
        )

    print(
        "Counter-attacks:",
        neutral_results[
            "counter_attacks"
        ]
    )

    print(
        "Trades:",
        neutral_results[
            "trades"
        ]
    )

    print()


def main():
    """
    Load one replay from the command
    line and display its gameplay stats.
    """

    if len(sys.argv) != 2:
        print(
            "Usage:"
        )

        print(
            "python inspect_metrics.py "
            "path/to/replay.slp"
        )

        sys.exit(1)

    replay_path = Path(
        sys.argv[1]
    )

    game = load_replay(
        replay_path,
        skip_frames=False
    )

    summary = (
        create_match_summary(
            game
        )
    )

    for player_index in (0, 1):
        print_player_metrics(
            game,
            summary,
            player_index
        )


if __name__ == "__main__":
    main()