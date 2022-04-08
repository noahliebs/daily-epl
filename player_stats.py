import json
from datetime import date, datetime
import pytz

from game_functions import get_today

class PlayerStats(object):

    MAX_GUESSES = 8
    default_performance_map = { n : 0 for n in range(MAX_GUESSES + 1)}

    def __init__(self, first_date_played: date, win_streak: int = 0, max_streak: int = 0, performance_map: dict = default_performance_map, last_date_played: date = None):
        self.win_streak = win_streak
        self.max_streak = max_streak
        self.performance_map = performance_map
        self.first_date_played = first_date_played
        
       	if last_date_played == None:
       	    self.last_date_played = get_today()
        else:
            self.last_date_played = last_date_played


    def finish_game(self, won_game:bool, guess_count: int):
        ## Make sure we don't "finish" a game twice
        today = get_today()
        if (today - self.last_date_played).days >= 0:
            if won_game:
                if self.win_streak == 0 or (today - self.last_date_played).days != 1:
                    self.win_streak = 1
                else:
                    self.win_streak += 1
            else:
                self.win_streak = 0
                self.performance[0] += 1

            self.performance_map[guess_count] += 1
            self.last_date_played = today
            self.max_streak = max(self.max_streak, self.win_streak)

        
 
    def to_json(self):
        return {
            "win_streak": self.win_streak,
            "max_streak": self.max_streak,
            "performance": self.performance_map,
            "first_date": self.first_date_played.isoformat(),
            "last_date": self.last_date_played.isoformat(),
            "played": sum(self.performance_map.values())
        }
    
    @classmethod
    def from_json(cls, json_data):
        first_date_played = date.fromisoformat(json_data["first_date"])
        win_streak = json_data["win_streak"]
        max_streak = json_data["max_streak"]
        performance = json_data["performance"]
        last_date_played = date.fromisoformat(json_data["last_date"])
        return cls(first_date_played, win_streak, max_streak, performance, last_date_played)
