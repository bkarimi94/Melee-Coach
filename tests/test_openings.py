from src.analysis.openings import (
    Opening,
    calculate_damage_taken,
    calculate_opk,
    count_kills,
    did_lose_stock,
    get_countable_openings,
    get_final_frame_indices,
    is_damaged,
    is_grabbed,
    is_in_control,
)


def test_calculate_opk():
    result = calculate_opk(
        opening_count=12,
        kill_count=4
    )

    assert result == 3.0


def test_one_opening_per_kill():
    result = calculate_opk(
        opening_count=4,
        kill_count=4
    )

    assert result == 1.0


def test_opk_with_no_kills():
    result = calculate_opk(
        opening_count=8,
        kill_count=0
    )

    assert result is None


def test_damage_state():
    assert is_damaged(75)
    assert is_damaged(80)
    assert is_damaged(91)


def test_non_damage_state():
    assert not is_damaged(14)


def test_grabbed_state():
    assert is_grabbed(223)
    assert is_grabbed(232)


def test_in_control_state():
    assert is_in_control(14)
    assert is_in_control(20)


def test_damage_taken():
    result = calculate_damage_taken(
        previous_percent=27.0,
        current_percent=39.0
    )

    assert result == 12.0


def test_no_damage_taken():
    result = calculate_damage_taken(
        previous_percent=27.0,
        current_percent=27.0
    )

    assert result == 0.0


def test_stock_loss_detection():
    assert did_lose_stock(
        previous_stocks=4,
        current_stocks=3
    )


def test_no_stock_loss():
    assert not did_lose_stock(
        previous_stocks=4,
        current_stocks=4
    )


def test_count_kills():
    openings = [
        Opening(
            attacker_index=0,
            defender_index=1,
            start_frame=100,
            start_percent=0,
            did_kill=True,
            had_damage=True
        ),
        Opening(
            attacker_index=0,
            defender_index=1,
            start_frame=500,
            start_percent=30,
            did_kill=False,
            had_damage=True
        ),
        Opening(
            attacker_index=0,
            defender_index=1,
            start_frame=900,
            start_percent=80,
            did_kill=True,
            had_damage=True
        ),
    ]

    assert count_kills(openings) == 2


def test_countable_openings():
    openings = [
        Opening(
            attacker_index=0,
            defender_index=1,
            start_frame=100,
            start_percent=0,
            had_damage=True
        ),
        Opening(
            attacker_index=0,
            defender_index=1,
            start_frame=500,
            start_percent=27,
            had_damage=False
        ),
    ]

    result = get_countable_openings(
        openings
    )

    assert len(result) == 1


def test_final_frame_indices_keep_latest_version():
    frame_ids = [
        100,
        101,
        102,
        101,
        102,
        103,
    ]

    result = get_final_frame_indices(
        frame_ids
    )

    assert result == [
        0,
        3,
        4,
        5,
    ]