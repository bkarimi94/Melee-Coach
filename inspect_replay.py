from pathlib import Path

from src.replay_parser import load_replay
from src.match_summary import create_match_summary


replay_path = Path("sample_data/test_game.slp")

game = load_replay(replay_path)

summary = create_match_summary(game)

print("=== MELEE COACH REPLAY SUMMARY ===")
print()

print(
    f"Player 1: {summary['player_1_name']} "
    f"({summary['player_1_character']})"
)

print(
    f"Player 2: {summary['player_2_name']} "
    f"({summary['player_2_character']})"
)

print(f"Stage: {summary['stage']}")

print(
    f"Starting stocks: "
    f"{summary['starting_stocks']} each"
)

print(
    f"Timer: "
    f"{summary['timer_seconds']} seconds"
)