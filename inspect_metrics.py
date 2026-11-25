"""Print a readable gameplay-statistics summary for one Slippi replay."""

import sys
from src.batch_analysis import analyze_one_replay


def main():
    if len(sys.argv) != 2:
        print("Usage: python inspect_metrics.py sample_data/test_game.slp")
        sys.exit(1)

    try:
        match = analyze_one_replay(sys.argv[1])
    except Exception as error:
        print(f"Could not analyze replay: {error}")
        sys.exit(1)

    print(f"Replay: {match['filename']}")
    print(f"Stage: {match['summary']['stage']}")
    for player in match["players"]:
        opk = player["opk"]
        neutral = player["neutral"]
        damage = player["damage"]
        ratio = neutral["neutral_win_ratio"]
        opk_text = "N/A" if opk["opk"] is None else f"{opk['opk']:.2f}"
        ratio_text = "N/A" if ratio is None else f"{100 * ratio:.2f}%"
        damage_value = damage["average_damage"]
        damage_text = "N/A" if damage_value is None else f"{damage_value:.2f}%"
        print(f"\n{player['name']} ({player['character']})")
        print(f"Openings: {opk['openings']}; Kills: {opk['kills']}; OPK: {opk_text}")
        print(
            f"Neutral Wins: {neutral['neutral_wins']}; "
            f"Neutral Losses: {neutral['neutral_losses']}; "
            f"Neutral Win Rate: {ratio_text}"
        )
        print(f"Counter-attacks: {neutral['counter_attacks']}; Trades: {neutral['trades']}")
        print(f"Avg. Damage per Opening (estimate): {damage_text}")
        for note in player["feedback"]:
            print(f"- {note}")


if __name__ == "__main__":
    main()