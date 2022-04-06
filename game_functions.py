import random

from guess_history import GuessHistory
from soccer_player import SoccerPlayer
from player_type_ahead import PlayerTypeAhead
from photo_helper import display_player_photo
from epl_table import EPLTable



MAX_GUESSES = 8

def pick_random_player(filtered_players: dict):
    return random.choice(list(filtered_players))


def is_game_over(guess_history: GuessHistory):
     return guess_history.is_winner or len(guess_history.guesses) >= MAX_GUESSES


def already_guessed_player(input_name: str, guess_history: GuessHistory):
    return input_name in [p.get_display_name() for p in guess_history.guesses]

## Process a player guess and return length of guesses
def process_guess(answer: SoccerPlayer, guess: SoccerPlayer, guess_history: GuessHistory, epl_table: EPLTable, confederation_mapping: dict):
    guess_history.add_guess(guess)
    if (guess.get_display_name() == answer.get_display_name()):
        guess_history.mark_as_winner()

    