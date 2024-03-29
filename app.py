import datetime
import json
import redis
import base64
import os
import pytz

from flask import Flask, request, session, redirect, url_for, render_template, send_from_directory
from flask_session import Session
from game_functions import *
from photo_helper import *
from guess_history import GuessHistory
from player_stats import PlayerStats

from data_collection import get_live_epl_table, get_live_player_stats



from game_setup import *
players = init_players()



Randy_Gartside = SoccerPlayer({
    "appearances": 0,
    "mins_played": 0,
    "goals": 0,
    "assists": 0,
    "id": 0,
    "optaId": "na",
    "position": "D",
    "number": 13,
    "nation": {
        "isoCode": "US",
        "country": "United States",
        "demonym": "American"
    },
    "dob": 713775600000,
    "name": {
        "display": "That's a zero",
        "first": "Randy",
        "last": "Gartside"
    },
    "team": "Norwich City"
})


player_map = {}
for p in players:
    player_map[p.get_display_name()] = p

player_map[Randy_Gartside.get_display_name()] = Randy_Gartside

## Limit who's availability to be an answer
available_players = get_players_for_selection()


type_ahead_helper = init_type_ahead(players)
hint_config = init_hint_config()
epl_table = init_epl_table()
confederation_mapping = init_confederation_mapping()



headers = ["Name", "Team", "Country", "Position", "Age", "Jersey", "Goals", "Assists"]
GUESS_HISTORY = "guess_history"
PLAYER_STATS = "player_stats"


## TODO: Make this random. Right now it's deterministic because heroku isn't stateful
def get_todays_answer():
    today = get_today()
    launch_date = datetime.date(2022, 4, 1)
    days_since_launch = (today - launch_date).days
    date_hash = days_since_launch % len(available_players)
    return available_players[date_hash]


def get_todays_answer_as_player():
    name = get_todays_answer()
    return get_player_as_updated(name)


# Create the Flask application
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY' # TODO



app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_TYPE'] = 'mongodb'
##app.config['SESSION_TYPE'] = 'memcached'

# # Configure Redis for storing the session data on the server-side
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def input_guess():
    today = get_today().isoformat()
    answer = get_todays_answer_as_player()



    guess_history = get_guess_history(session)
    player_stats = get_player_stats(session)


    guess_history.hint_config = hint_config
    if answer in guess_history.guesses:
        guess_history.mark_as_winner()


    game_wasnt_finished = not is_game_over(guess_history)
        
    if request.method == 'POST' and game_wasnt_finished:              
        input_name = request.form['player_name']
        valid_names = type_ahead_helper.search_ahead(input_name)
        if len(valid_names) == 1:
            name = valid_names.pop()
            if already_guessed_player(name, guess_history):
                messsage = """{} was already guessed""".format(name)
                return return_response(guess_history, player_stats, messsage)
            else:
                guess = get_player_as_updated(name)
                process_guess(answer, guess, guess_history, epl_table, confederation_mapping)
                session[GUESS_HISTORY][today] = guess_history.to_json()
        else:
            message =  """Relevant options: {}""".format(", ".join(valid_names))
            return return_response(guess_history, player_stats, message)

    if is_game_over(guess_history):
        if game_wasnt_finished:
            player_stats.finish_game(guess_history.is_winner, len(guess_history.guesses))
            session[PLAYER_STATS] = player_stats.to_json()
        
        return return_finished(guess_history, player_stats)
        
 
    return return_response(guess_history, player_stats, "")
    


def return_response(guess_history: GuessHistory, player_stats: PlayerStats, message: str):
    guess_table_data = generate_guess_table_data(guess_history)

    images = [get_img_data(p) for p in guess_history.guesses]
    return render_template("game.html", headers = headers, stats = player_stats.to_json(), guess_table_data = guess_table_data, message = message, images = images, guess_count = len(images), size = list(range(len(images))))


def return_finished(guess_history: GuessHistory, player_stats: PlayerStats):
    answer_name = get_todays_answer()
    if guess_history.is_winner:
        message = "{} is correct!".format(answer_name)
    else:
        message = "Correct answer was: {}".format(answer_name)
        
    return return_response(guess_history, player_stats, message)




def get_guess_history(session) -> GuessHistory:
    today = get_today().strftime('%Y-%m-%d')

    if GUESS_HISTORY not in session:
        session[GUESS_HISTORY] = {}
    if today not in session[GUESS_HISTORY]:
        session[GUESS_HISTORY][today] = GuessHistory(hint_config).to_json()

    return GuessHistory.from_json(session[GUESS_HISTORY][today])


def get_player_stats(session) -> PlayerStats:
    if PLAYER_STATS not in session:
        today = get_today()
        session[PLAYER_STATS] = PlayerStats(today).to_json()

    return PlayerStats.from_json(session[PLAYER_STATS])


def generate_guess_table_data(guess_history: GuessHistory):
    todays_winner = get_todays_answer_as_player()
    guess_data = guess_history.get_guess_data()
    hint_data = guess_history.get_hint_data(todays_winner, epl_table, confederation_mapping)

    guess_table_data = []
    for i in range(len(guess_data)):
        row = []
        for j in range(len(headers)):
            value = [guess_data[i][j]]
            hint = hint_data[i][j]
            if hint == "✓":
                value.extend(["", "correct"])
            elif hint in ["↑", "↓"]:
                value.extend([hint, "close"])
            elif hint in list(confederation_mapping.values()):
                ## Dont display confederation
                value.extend(["", "close"])
            elif hint in ["↑↑", "↓↓"]:
                value.extend([hint, "wrong"])
            else:
                value.extend(["", "wrong"])
            row.append(value)
        guess_table_data.append(row)
    return guess_table_data


def get_img_data(player: SoccerPlayer):
    if player.get_display_name() == Randy_Gartside.get_display_name():
        with open("data/gartside.jpeg", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    else:
        return base64.b64encode(get_player_photo(player).content).decode("utf-8")
    

def update_epl_table():
    global epl_table

    try:
        print("Updating EPL Table Stats")

        table = get_live_epl_table()
        with open("data/epl_table.json", "w") as f:
            f.write(json.dumps(table))


        epl_table = init_epl_table()
        print("Done updating epl table")
    except: 
        print("Failed to update EPL Table")
    return "DONE"


def get_player_as_updated(player_display_name):
    if player_display_name == Randy_Gartside.get_display_name():
        return Randy_Gartside
    raw = player_map[player_display_name].raw
    raw.update(get_live_player_stats(raw))
    return SoccerPlayer(raw)


def update_player_stats():
    global players
    print("Updating Player Stats")

    updated_players = []
    for p in players:
        p.raw.update(get_live_player_stats(p.raw))
        updated_players.append(p.raw)
    with open("data/augmented_players.json", "w") as f:
        f.write(json.dumps(updated_players))


    players = init_players()
    print("Done updating player stats")
    return "DONE"




import atexit
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_epl_table, trigger="interval", minutes=5)
scheduler.start()

## Run them right away
for job in scheduler.get_jobs():
    job.modify(next_run_time=datetime.datetime.now())

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


## Admin API
@app.route('/update_players_zz', methods=['GET', 'POST'])
def update_players():
    update_player_stats()

## Admin API
@app.route('/update_table_zz', methods=['GET', 'POST'])
def update_table():
    update_epl_table()


if __name__ == '__main__':
    ##app.run(host='0.0.0.0')
    app.run()
    #app.run(debug=True)