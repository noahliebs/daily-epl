class HintConfig(object):
    
    ## Max distance from the answer to receive a hint
    def __init__(self, team_d: int, goal_d: int, assist_d: int, app_d: int, age_d: int, jersey_d: int):
        self.team_d = team_d
        self.goal_d = goal_d
        self.assist_d = assist_d
        self.app_d = app_d
        self.age_d = age_d
        self.jersey_d = jersey_d