import datetime
from dateutil.relativedelta import relativedelta
import json

class SoccerPlayer(object):
    
    def __init__(self, raw_value: dict):
        self.name = raw_value["name"]
        self.goals = raw_value.get("goals",0)
        self.assists = raw_value.get("assists", 0)
        self.appearances = raw_value["appearances"]
        self.mins_played = raw_value["mins_played"]
        self.team = raw_value["team"]
        self.nation = raw_value["nation"]
        self.dob = raw_value["dob"]
        self.position = raw_value["position"]
        self.jersey = raw_value["number"]
        self.id = raw_value["id"]
        self.raw = raw_value ## Retain all raw data
        
        
    def __str__(self):
        return json.dumps(self.raw)
    
    
    def get_age(self):
        date = datetime.datetime.fromtimestamp(self.dob / 1000)
        return relativedelta(datetime.datetime.now(), date).years
    
    def get_display_name(self):
        return self.name["display"]
    
    def get_first_name(self):
        return self.name["first"]
    
    def get_last_name(self):
        return self.name["last"]
        
    def get_country(self):
        return self.nation["country"]