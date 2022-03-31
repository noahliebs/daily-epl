from soccer_player import SoccerPlayer
from guess_proximity import *
from epl_table import EPLTable
from hint_config import HintConfig
from photo_helper import display_player_photo
import pandas as pd

import json

class GuessHistory(object):
    
    def __init__(self, hint_config: HintConfig):
        self.guesses = []
        self.hint_config = hint_config
        self.is_winner = False        
        
    def mark_as_winner(self):
        self.is_winner = True
        
        
    def add_guess(self, guess: SoccerPlayer):
        if guess.get_display_name() not in [g.get_display_name() for g in self.guesses]:
            self.guesses.append(guess)
            return True
        else:
            return False
        
    def guess_header(self):
        return ["Name", "Team", "Country", "Position", "Age", "Jersey", "Goals", "Assists", "Appearances"]
        
    def guess_to_data(self, guess: SoccerPlayer):
        return [guess.get_display_name(), guess.team, guess.get_country(), guess.position, guess.get_age(), guess.jersey, guess.goals, guess.assists, guess.appearances]
    
    
    def guess_to_hint(self, answer: SoccerPlayer, guess: SoccerPlayer, epl_table: EPLTable, conderation_mapping: dict):
        name_code = get_exact_match_code(answer.get_display_name(), guess.get_display_name())
        team_hint = get_team_code(answer, guess, epl_table, self.hint_config.team_d)
        position_hint = get_position_code(answer, guess)
        goal_hint = get_goals_code(answer, guess, self.hint_config.goal_d)
        assist_hint = get_assists_code(answer, guess, self.hint_config.assist_d)
        app_hint = get_appearances_code(answer, guess, self.hint_config.app_d)
        country_hint = get_country_code(answer, guess, conderation_mapping)
        age_hint = get_age_code(answer, guess, self.hint_config.age_d)
        jersey_hint = get_jersey_code(answer, guess, self.hint_config.jersey_d)
        
        return [name_code, team_hint, country_hint, position_hint, age_hint, jersey_hint, goal_hint, assist_hint, app_hint]
    
    
    def get_history_table(self, answer: SoccerPlayer, epl_table: EPLTable, confederation_mapping: dict):
        guess_table = self.get_guess_data()
        hint_table = self.get_hint_data(answer, epl_table, confederation_mapping)
        
        result = [None]*(2 * len(guess_table))
        result[::2] = guess_table
        result[1::2] = hint_table
        return result
    
    def get_guess_data(self):
        return [self.guess_to_data(g) for g in self.guesses]
    
    def get_hint_data(self, answer: SoccerPlayer, epl_table: EPLTable, confederation_mapping: dict):
        return [self.guess_to_hint(answer, g, epl_table, confederation_mapping) for g in self.guesses]
    
    def print_history(self, answer: SoccerPlayer, epl_table: EPLTable, confederation_mapping: dict):
        table = [self.guess_header()] + self.get_history_table(answer, epl_table, confederation_mapping)
        l1, l2 = len(table), len(table[0])
        pd.set_option('expand_frame_repr', False)
        print(pd.DataFrame(table, index=['']*l1, columns=['']*l2))

            
    def __str__(self):
        return json.dumps(self.to_json())
        
        
    def to_json(self):
        return {
            "hint_config": self.hint_config.to_json(),
            "guesses": [p.raw for p in self.guesses],
            "is_winner": self.is_winner
        }
        
        return [p.raw for p in self.guesses]
    
    @classmethod
    def from_json(cls, json_data):
        hint_config = HintConfig.from_json(json_data["hint_config"])
        guesses = [SoccerPlayer(g) for g in json_data["guesses"]]
        is_winner = json_data["is_winner"]
        obj = cls(hint_config)
        obj.guesses = guesses
        obj.is_winner = is_winner
        return obj