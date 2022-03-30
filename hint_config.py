class HintConfig(object):
    
    ## Max distance from the answer to receive a hint
    def __init__(self, team_d: int, goal_d: int, assist_d: int, app_d: int, age_d: int, jersey_d: int):
        self.team_d = team_d
        self.goal_d = goal_d
        self.assist_d = assist_d
        self.app_d = app_d
        self.age_d = age_d
        self.jersey_d = jersey_d
        
        
    def to_json(self):
        return {
         "team_d": self.team_d,
         "goal_d": self.goal_d,
         "assist_d": self.assist_d,
         "app_d": self.app_d,
         "age_d": self.age_d,
         "jersey_d": self.jersey_d
        }
    
    @classmethod
    def from_json(cls, json_data):
        team_d = json_data["team_d"]
        goal_d = json_data["goal_d"]
        assist_d = json_data["assist_d"]
        app_d = json_data["app_d"]
        age_d = json_data["age_d"]
        jersey_d = json_data["jersey_d"]
        return cls(team_d, goal_d, assist_d, app_d, age_d, jersey_d)