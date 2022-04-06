import json
from datetime import datetime
import pytz

class PlayerStats(object):

    MAX_GUESSES = 8
    default_performance_map = { n : 0 for n in range(MAX_GUESSES + 1)}
    date_format = '%Y-%m-%d'

    def __init__(self, first_date_played: datetime, win_streak: int = 0, max_streak: int = 0, performance_map: dict = default_performance_map, last_date_played: datetime = None):
        self.win_streak = win_streak
        self.max_streak = max_streak
        self.performance_map = performance_map
        self.first_date_played = first_date_played
        
       	if last_date_played == None:
       	    self.last_date_played = PlayerStats.get_today()
        else:
            self.last_date_played = last_date_played


    def finish_game(self, won_game:bool, guess_count: int, today:datetime):
        ## Make sure we don't "finish" a game twice
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
            "first_date_played": PlayerStats.datetime_to_str(self.first_date_played),
            "last_date_played": PlayerStats.datetime_to_str(self.last_date_played),
            "played": sum(self.performance_map.values())
        }
    
    @classmethod
    def from_json(cls, json_data):
        first_date_played = PlayerStats.str_to_datetime(json_data["first_date_played"])
        win_streak = json_data["win_streak"]
        max_streak = json_data["max_streak"]
        performance = json_data["performance"]
        last_date_played = PlayerStats.str_to_datetime(json_data["last_date_played"])
        return cls(first_date_played, win_streak, max_streak, performance, last_date_played)

    @staticmethod
    def str_to_datetime(date_string: str) -> datetime:
        return datetime.strptime(date_string, PlayerStats.date_format).astimezone(pytz.timezone('US/Pacific'))

    @staticmethod
    def datetime_to_str(date: datetime) -> str:
        return date.strftime(PlayerStats.date_format)


    @staticmethod
    def get_today():
        now = datetime.now(tz=pytz.utc)
        return now.astimezone(pytz.timezone('US/Pacific'))
