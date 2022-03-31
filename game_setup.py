import json
import csv

from epl_table import EPLTable
from player_type_ahead import PlayerTypeAhead
from hint_config import HintConfig
from soccer_player import SoccerPlayer


## Returns players, player_map, and filtered_players
def init_players():
    with open("data/augmented_players.json", "r") as f:
        players = [SoccerPlayer(p) for p in json.loads(f.read())]
    
    player_map = {}
    for p in players:
        player_map[p.get_display_name()] = p
        
        
    min_mins_requirement = 900
    min_games = 10

    ## When choosing a random player, restrict the subset to players people would actually know
    filtered_players = [p for p in players if p.appearances >= min_games and p.mins_played > min_mins_requirement and p.position != "G"]
    
    return (players, player_map, filtered_players)
   
def init_type_ahead(players):
     ## Initialize Type Ahead Search
    return PlayerTypeAhead(players)
    
def init_hint_config():
    ## Initialize the Hint Configuration File!!
    team_d = 3 
    goal_d = 3
    assist_d = 3 
    app_d = 3
    age_d = 3 
    jersey_d = 3

    return HintConfig(team_d, goal_d, assist_d, app_d, age_d, jersey_d)
    
def init_epl_table():
     ## Initialize EPL Table
    return EPLTable("data/epl_table.json")

def init_confederation_mapping():
    ## Initialize the Country -> Continent Mapping
    confederation_mapping = {}
    with open("data/fifa.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            confederation_mapping[row[0]] = row[1]
    return confederation_mapping