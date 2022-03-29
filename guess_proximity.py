from soccer_player import SoccerPlayer
from epl_table import EPLTable

CORRECT = "✓"
LOWER = "↓"
HIGHER = "↑"
WRONG = "X"


## Exact Matches
def get_exact_match_code(player_v, guess_v):
    if player_v == guess_v:
        return CORRECT
    else:
        return WRONG

def get_position_code(player: SoccerPlayer, guess: SoccerPlayer):
    player_v = player.position
    guess_v = guess.position
    return get_exact_match_code(player_v, guess_v)


# Comparison Matches with "Closeness"
def get_comparison_code(player_v, guess_v, offset):
    comp = player_v - guess_v
    if player_v == guess_v:
        return CORRECT
    elif comp > 0 and comp <= offset:
        return HIGHER
    elif comp < 0 and comp >= -offset:
        return LOWER
    else:
        return WRONG

def get_goals_code(player: SoccerPlayer, guess: SoccerPlayer, hint_range: int):
    player_v = player.goals
    guess_v = guess.goals
    return get_comparison_code(player_v, guess_v, hint_range)

def get_assists_code(player: SoccerPlayer, guess: SoccerPlayer, hint_range: int):
    player_v = player.assists
    guess_v = guess.assists
    return get_comparison_code(player_v, guess_v, hint_range)


# def get_mins_code(player: SoccerPlayer, guess: SoccerPlayer, hint_range: int):
#     player_v = player.mins_played
#     guess_v = guess.mins_played
#     return get_comparison_code(player_v, guess_v, hint_range)

def get_age_code(player: SoccerPlayer, guess: SoccerPlayer, hint_range: int):
    player_v = player.get_age()
    guess_v = guess.get_age()
    return get_comparison_code(player_v, guess_v, hint_range)


def get_appearances_code(player: SoccerPlayer, guess: SoccerPlayer, hint_range: int):
    player_v = player.appearances
    guess_v = guess.appearances
    return get_comparison_code(player_v, guess_v, hint_range)


def get_jersey_code(player: SoccerPlayer, guess: SoccerPlayer, hint_range: int):
    player_v = player.jersey
    guess_v = guess.jersey
    return get_comparison_code(player_v, guess_v, hint_range)

def get_team_code(player: SoccerPlayer, guess: SoccerPlayer, epl_table: EPLTable, hint_range: int):
    player_v = player.team
    guess_v = guess.team
    if player_v == guess_v:
        return CORRECT
    else:
        return get_comparison_code(0, epl_table.get_epl_table_diff(player_v, guess_v), hint_range)
    
def get_country_code(player: SoccerPlayer, guess: SoccerPlayer, confederation_mapping: dict):
    player_v = player.get_country()
    guess_v = guess.get_country()
    if player_v == guess_v:
        return CORRECT
    elif get_confederation(player, confederation_mapping) == get_confederation(guess, confederation_mapping):
        return get_confederation(player, confederation_mapping)
    else:
        return WRONG
    
def get_confederation(player: SoccerPlayer, conderation_mapping: dict):
    return conderation_mapping.get(player.get_country(), "N.A")