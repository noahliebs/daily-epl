import requests

def get_live_player_stats(cleansed_player):
    url = 'https://footballapi.pulselive.com/football/stats/player/%s?comps=1&compSeasons=418' % str(int(cleansed_player["id"]))
    payload = requests.get(url, headers = { "origin": "https://www.premierleague.com"}).json()

    stats = payload["stats"]
    relevant_stats = {}
    
    stat_name_mapping = {
        "goals": "goals",
        "goal_assist": "assists",
        "appearances": "appearances",
        "mins_played": "mins_played"
    }
    
    for s in stats:
        if s["name"] in stat_name_mapping.keys():
            relevant_stats[stat_name_mapping[s["name"]]] = int(s["value"])
        
    for k in stat_name_mapping.values():
        if k not in relevant_stats:
            relevant_stats[k] = 0
            
    return relevant_stats



def get_live_epl_table():
    url = 'https://footballapi.pulselive.com/football/standings?compSeasons=418&altIds=true&detail=2&FOOTBALL_COMPETITION=1'
    payload = requests.get(url, headers = { "origin": "https://www.premierleague.com"}).json()
    table = payload["tables"][0]
    return table["entries"]