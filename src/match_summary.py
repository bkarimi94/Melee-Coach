from src.melee_data import (
    get_character_name,
    get_stage_name
)


def create_match_summary(game):
    player_1 = game.start.players[0]
    player_2 = game.start.players[1]

    return {
        "player_1_name": player_1.netplay.name,
        "player_1_character": get_character_name(
            player_1.character
        ),
        "player_2_name": player_2.netplay.name,
        "player_2_character": get_character_name(
            player_2.character
        ),
        "stage": get_stage_name(
            game.start.stage
        ),
        "starting_stocks": player_1.stocks,
        "timer_seconds": game.start.timer,
    }