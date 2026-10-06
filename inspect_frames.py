from pathlib import Path

from src.replay_parser import load_replay


def python_value(arrow_array, index):
    """
    Convert one value from a PyArrow array
    into a regular Python value.
    """

    value = arrow_array[index]

    if hasattr(value, "as_py"):
        return value.as_py()

    return value


replay_path = Path(
    "sample_data/test_game.slp"
)

game = load_replay(
    replay_path,
    skip_frames=False
)

print("Replay successfully loaded with frame data.")
print()

print("Number of frames:")
print(len(game.frames.id))

print()


for player_number, player in enumerate(
    game.start.players
):
    port_index = player.port.value

    post = (
        game.frames
        .ports[port_index]
        .leader
        .post
    )

    print(
        f"=== PLAYER {player_number + 1} ==="
    )

    print(
        "Character ID:",
        python_value(post.character, 0)
    )

    print(
        "Action state:",
        python_value(post.state, 0)
    )

    print(
        "Percent:",
        python_value(post.percent, 0)
    )

    print(
        "Stocks:",
        python_value(post.stocks, 0)
    )

    print(
        "Last attack landed:",
        python_value(
            post.last_attack_landed,
            0
        )
    )

    print(
        "Last hit by:",
        python_value(
            post.last_hit_by,
            0
        )
    )

    print(
        "Combo count:",
        python_value(
            post.combo_count,
            0
        )
    )

    print()