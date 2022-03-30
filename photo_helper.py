from IPython.display import Image, display
from soccer_player import SoccerPlayer
import requests

# def display_player_photo(player: SoccerPlayer):
#     base_path = "data/photos/"
#     path = base_path + "/photos/40x40/%s.png" % player.opta_id
#     display(Image(filename=path))

def get_player_photo(player: SoccerPlayer):
    pixels = "40x40" ## "250x250"
    url = "https://resources.premierleague.com/premierleague/photos/players/%s/%s.png" % (pixels, player.opta_id)
    response = requests.get(url)
    return response

def display_player_photo(player: SoccerPlayer):
    response = get_player_photo(player)
    if response.status_code == 200:
        display(Image(response.content))