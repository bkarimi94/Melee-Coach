from dataclasses import dataclass


PUNISH_RESET_FRAMES = 45


# Damage states
DAMAGE_START = 75
DAMAGE_END = 91

DAMAGE_FALL = 38

JAB_RESET_UP = 185
JAB_RESET_DOWN = 193


# Grab / capture states
CAPTURE_START = 223
CAPTURE_END = 232


# Command-grab states
COMMAND_GRAB_RANGE_1_START = 266
COMMAND_GRAB_RANGE_1_END = 304

COMMAND_GRAB_RANGE_2_START = 327
COMMAND_GRAB_RANGE_2_END = 338

BARREL_WAIT = 293


# States considered "in control"
GROUNDED_CONTROL_START = 14
GROUNDED_CONTROL_END = 24

SQUAT_START = 39
SQUAT_END = 41

GROUND_ATTACK_START = 44
GROUND_ATTACK_END = 64

GRAB = 212


@dataclass
class Opening:
    attacker_index: int
    defender_index: int

    start_frame: int
    start_percent: float

    end_frame: int | None = None
    end_percent: float | None = None

    did_kill: bool = False
    had_damage: bool = False


def arrow_value(array, index):
    """
    Convert one PyArrow value into
    a normal Python value.
    """

    value = array[index]

    if hasattr(value, "as_py"):
        return value.as_py()

    return value


def get_final_frame_indices(frame_ids):
    """
    Return the array index for the final
    recorded version of every frame.

    Slippi rollback replays may contain
    multiple versions of the same frame.
    The last occurrence represents the
    corrected version in a completed replay.
    """

    last_index_by_frame = {}

    for index in range(
        len(frame_ids)
    ):
        frame_number = arrow_value(
            frame_ids,
            index
        )

        last_index_by_frame[
            frame_number
        ] = index

    final_indices = [
        last_index_by_frame[
            frame_number
        ]
        for frame_number in sorted(
            last_index_by_frame
        )
    ]

    return final_indices


def is_damaged(state):
    return (
        DAMAGE_START
        <= state
        <= DAMAGE_END
        or state == DAMAGE_FALL
        or state == JAB_RESET_UP
        or state == JAB_RESET_DOWN
    )


def is_grabbed(state):
    return (
        CAPTURE_START
        <= state
        <= CAPTURE_END
    )


def is_command_grabbed(state):
    in_first_range = (
        COMMAND_GRAB_RANGE_1_START
        <= state
        <= COMMAND_GRAB_RANGE_1_END
    )

    in_second_range = (
        COMMAND_GRAB_RANGE_2_START
        <= state
        <= COMMAND_GRAB_RANGE_2_END
    )

    return (
        (
            in_first_range
            or in_second_range
        )
        and state != BARREL_WAIT
    )


def is_in_control(state):
    grounded = (
        GROUNDED_CONTROL_START
        <= state
        <= GROUNDED_CONTROL_END
    )

    squatting = (
        SQUAT_START
        <= state
        <= SQUAT_END
    )

    ground_attack = (
        state > GROUND_ATTACK_START
        and state <= GROUND_ATTACK_END
    )

    grabbing = (
        state == GRAB
    )

    return (
        grounded
        or squatting
        or ground_attack
        or grabbing
    )


def calculate_damage_taken(
    previous_percent,
    current_percent
):
    """
    Calculate damage taken between
    consecutive finalized frames.
    """

    if (
        previous_percent is None
        or current_percent is None
    ):
        return 0.0

    damage_taken = (
        current_percent
        - previous_percent
    )

    if damage_taken < 0:
        return 0.0

    return damage_taken


def did_lose_stock(
    previous_stocks,
    current_stocks
):
    if (
        previous_stocks is None
        or current_stocks is None
    ):
        return False

    return (
        previous_stocks
        > current_stocks
    )


def detect_openings(
    game,
    player_index
):
    """
    Detect openings created by one player.

    Only the final version of each Slippi
    frame is analyzed so rollback revisions
    do not create false openings.

    This version currently supports
    two-player singles matches.
    """

    if len(game.start.players) != 2:
        raise ValueError(
            "OPK analysis currently supports "
            "two-player singles matches only."
        )

    if player_index not in (0, 1):
        raise ValueError(
            "player_index must be 0 or 1."
        )

    defender_index = (
        1 - player_index
    )

    defender = (
        game.start.players[
            defender_index
        ]
    )

    defender_port = (
        defender.port.value
    )

    defender_post = (
        game.frames
        .ports[defender_port]
        .leader
        .post
    )

    frame_ids = game.frames.id

    final_indices = (
        get_final_frame_indices(
            frame_ids
        )
    )

    openings = []

    current_opening = None

    reset_counter = 0

    if len(final_indices) < 2:
        return openings

    for position in range(
        1,
        len(final_indices)
    ):
        index = (
            final_indices[position]
        )

        previous_index = (
            final_indices[
                position - 1
            ]
        )

        frame_number = arrow_value(
            frame_ids,
            index
        )

        defender_state = arrow_value(
            defender_post.state,
            index
        )

        defender_percent = arrow_value(
            defender_post.percent,
            index
        )

        previous_percent = arrow_value(
            defender_post.percent,
            previous_index
        )

        defender_stocks = arrow_value(
            defender_post.stocks,
            index
        )

        previous_stocks = arrow_value(
            defender_post.stocks,
            previous_index
        )

        damage_taken = (
            calculate_damage_taken(
                previous_percent,
                defender_percent
            )
        )

        opponent_under_pressure = (
            is_damaged(defender_state)
            or is_grabbed(defender_state)
            or is_command_grabbed(
                defender_state
            )
        )

        if (
            current_opening is None
            and opponent_under_pressure
        ):
            current_opening = Opening(
                attacker_index=player_index,
                defender_index=defender_index,
                start_frame=frame_number,
                start_percent=(
                    previous_percent
                    if previous_percent
                    is not None
                    else 0.0
                )
            )

            openings.append(
                current_opening
            )

            reset_counter = 0

        if current_opening is None:
            continue

        if damage_taken > 0:
            current_opening.had_damage = (
                True
            )

        if opponent_under_pressure:
            reset_counter = 0

        opponent_in_control = (
            is_in_control(
                defender_state
            )
        )

        if (
            reset_counter == 0
            and opponent_in_control
        ):
            reset_counter = 1

        elif reset_counter > 0:
            reset_counter += 1

        stock_lost = did_lose_stock(
            previous_stocks,
            defender_stocks
        )

        if stock_lost:
            current_opening.did_kill = (
                True
            )

            current_opening.end_frame = (
                frame_number
            )

            current_opening.end_percent = (
                previous_percent
            )

            current_opening = None

            reset_counter = 0

            continue

        if (
            reset_counter
            > PUNISH_RESET_FRAMES
        ):
            current_opening.end_frame = (
                frame_number
            )

            current_opening.end_percent = (
                defender_percent
            )

            current_opening = None

            reset_counter = 0

    if current_opening is not None:
        final_index = (
            final_indices[-1]
        )

        current_opening.end_frame = (
            arrow_value(
                frame_ids,
                final_index
            )
        )

        current_opening.end_percent = (
            arrow_value(
                defender_post.percent,
                final_index
            )
        )

    return openings


def get_countable_openings(openings):
    """
    Keep only openings that eventually
    contain actual damage.
    """

    return [
        opening
        for opening in openings
        if opening.had_damage
    ]


def count_kills(openings):
    return sum(
        1
        for opening in openings
        if opening.did_kill
    )


def calculate_opk(
    opening_count,
    kill_count
):
    if kill_count == 0:
        return None

    return (
        opening_count
        / kill_count
    )


def analyze_opk(
    game,
    player_index
):
    detected_openings = (
        detect_openings(
            game,
            player_index
        )
    )

    openings = (
        get_countable_openings(
            detected_openings
        )
    )

    kills = count_kills(
        openings
    )

    opk = calculate_opk(
        len(openings),
        kills
    )

    return {
        "openings": len(openings),
        "kills": kills,
        "opk": opk,
        "opening_details": openings,
    }