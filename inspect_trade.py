from pathlib import Path

from src.analysis.openings import (
    arrow_value,
    is_damaged,
)
from src.replay_parser import (
    load_replay,
)


replay_path = Path(
    "sample_data/test_game.slp"
)


game = load_replay(
    replay_path,
    skip_frames=False
)


player_0 = game.start.players[0]
player_1 = game.start.players[1]


player_0_port = player_0.port.value
player_1_port = player_1.port.value


player_0_post = (
    game.frames
    .ports[player_0_port]
    .leader
    .post
)

player_1_post = (
    game.frames
    .ports[player_1_port]
    .leader
    .post
)


frame_ids = game.frames.id


print(
    "Inspecting frames 2640 through 2825"
)

print()


for index in range(
    1,
    len(frame_ids)
):
    frame = arrow_value(
        frame_ids,
        index
    )

    if frame < 2640:
        continue

    if frame > 2825:
        break


    p0_percent = arrow_value(
        player_0_post.percent,
        index
    )

    p0_previous_percent = arrow_value(
        player_0_post.percent,
        index - 1
    )

    p0_state = arrow_value(
        player_0_post.state,
        index
    )

    p0_last_hit_by = arrow_value(
        player_0_post.last_hit_by,
        index
    )


    p1_percent = arrow_value(
        player_1_post.percent,
        index
    )

    p1_previous_percent = arrow_value(
        player_1_post.percent,
        index - 1
    )

    p1_state = arrow_value(
        player_1_post.state,
        index
    )

    p1_last_hit_by = arrow_value(
        player_1_post.last_hit_by,
        index
    )


    p0_percent_changed = (
        p0_percent
        != p0_previous_percent
    )

    p1_percent_changed = (
        p1_percent
        != p1_previous_percent
    )


    p0_damaged = is_damaged(
        p0_state
    )

    p1_damaged = is_damaged(
        p1_state
    )


    if (
        p0_percent_changed
        or p1_percent_changed
        or p0_damaged
        or p1_damaged
    ):
        print(
            f"FRAME {frame}"
        )

        print(
            "  Player 0:"
        )

        print(
            f"    percent: "
            f"{p0_previous_percent} "
            f"-> {p0_percent}"
        )

        print(
            f"    state: "
            f"{p0_state}"
        )

        print(
            f"    damaged: "
            f"{p0_damaged}"
        )

        print(
            f"    last_hit_by: "
            f"{p0_last_hit_by}"
        )


        print(
            "  Player 1:"
        )

        print(
            f"    percent: "
            f"{p1_previous_percent} "
            f"-> {p1_percent}"
        )

        print(
            f"    state: "
            f"{p1_state}"
        )

        print(
            f"    damaged: "
            f"{p1_damaged}"
        )

        print(
            f"    last_hit_by: "
            f"{p1_last_hit_by}"
        )

        print()