from pathlib import Path

from src.analysis.openings import (
    analyze_opk
)
from src.match_summary import (
    create_match_summary
)
from src.replay_parser import (
    load_replay
)


replay_path = Path(
    "sample_data/test_game.slp"
)


game = load_replay(
    replay_path,
    skip_frames=False
)


summary = create_match_summary(
    game
)


for player_index in (0, 1):
    results = analyze_opk(
        game,
        player_index
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
        f"{player_name} ({character})"
    )

    print(
        "=============================="
    )

    print(
        "Openings:",
        results["openings"]
    )

    print(
        "Kills:",
        results["kills"]
    )

    if results["opk"] is None:
        print(
            "Openings Per Kill: N/A"
        )

    else:
        print(
            "Openings Per Kill:",
            round(
                results["opk"],
                2
            )
        )

    print()

    print("Opening details:")

    for number, opening in enumerate(
        results["opening_details"],
        start=1
    ):
        print(
            f"{number}. "
            f"Frames "
            f"{opening.start_frame}"
            f"–"
            f"{opening.end_frame}, "
            f"Start percent: "
            f"{opening.start_percent}, "
            f"End percent: "
            f"{opening.end_percent}, "
            f"Kill: "
            f"{opening.did_kill}"
        )

    print()