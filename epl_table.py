import json

class EPLTable(object):
    
    def __init__(self, epl_table_file_location):
        with open(epl_table_file_location, "r") as f:
            self.table = json.loads(f.read())
            
        self.standings = [t["team"]["name"] for t in self.table]
        
    def get_standings(self):
        return [t["team"]["name"] for t in self.table]
    
    def get_epl_table_diff(self, team1, team2):
        position1 = self.standings.index(team1)
        position2 = self.standings.index(team2)
        return (position1 - position2)
    
    

    
