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
from random import sample




from game_setup import *
(players, player_map, filtered_players) = init_players()
type_ahead_helper = init_type_ahead(players)
hint_config = init_hint_config()
epl_table = init_epl_table()
confederation_mapping = init_confederation_mapping()



headers = ["Name", "Team", "Country", "Position", "Age", "Jersey", "Goals", "Assists", "Appearances"]
GUESS_HISTORY = "guess_history" 



## Track list of answers
answers = {}
## TODO: Make this random. Right now it's deterministic because heroku isn't stateful
def get_today():
    now = datetime.datetime.now(tz=pytz.utc)
    return now.astimezone(pytz.timezone('US/Pacific'))

def get_todays_answer():
    today = get_today()
    date_hash = (int(today.strftime('%Y%m%d')) * 33) % len(filtered_players)
    if today in answers:
        return answers[today]
    else:
        answer = filtered_players[date_hash]
        answers[today] = answer
        return answer



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
    today = get_today().strftime('%Y-%m-%d')
    answer = get_todays_answer()
    if GUESS_HISTORY not in session:
        session[GUESS_HISTORY] = {}
        if today not in session[GUESS_HISTORY]:
            session[GUESS_HISTORY][today] = GuessHistory(hint_config).to_json()

    guess_history = GuessHistory.from_json(session[GUESS_HISTORY][today])
    guess_history.hint_config = hint_config
    if answer in guess_history.guesses:
        guess_history.mark_as_winner()
        
    if request.method == 'POST' and not is_game_over(guess_history):              
        input_name = request.form['player_name']
        valid_names = type_ahead_helper.search_ahead(input_name)
        if len(valid_names) == 1:
            name = valid_names.pop()
            if already_guessed_player(name, guess_history):
                messsage = """{} was already guessed""".format(name)
                return return_response(guess_history, messsage)
            else:
                guess = player_map[name]
                process_guess(answer, guess, guess_history, epl_table, confederation_mapping)
                session[GUESS_HISTORY][today] = guess_history.to_json()
        else:
            message =  """Valid relevant options: {}""".format(", ".join(valid_names))
            return return_response(guess_history, message)

    if is_game_over(guess_history):
        return return_finished(guess_history)
        
 
    return return_response(guess_history, "Partial names accepted")
    


def return_response(guess_history: GuessHistory, message: str):
    guess_table_data = generate_guess_table_data(guess_history)

    images = [get_img_data(p) for p in guess_history.guesses]
    return render_template("game.html", headers = headers, guess_table_data = guess_table_data, message = message, images = images, size = list(range(len(images))))


def return_finished(guess_history):
    answer_name = get_todays_answer().get_display_name()
    if guess_history.is_winner:
        message = "{} is correct! YOU WIN!".format(answer_name)
    else:
        message = "Correct answer was: {}. You Lose!".format(answer_name)
        
    return return_response(guess_history, message)



def generate_guess_table_data(guess_history: GuessHistory):
    todays_winner = get_todays_answer()
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
            elif hint in (["↑", "↓"] + list(confederation_mapping.values())):
                value.extend([hint, "close"])
            elif hint in ["↑↑", "↓↓"]:
                value.extend([hint, "wrong"])
            else:
                value.extend(["", "wrong"])
            row.append(value)
        guess_table_data.append(row)
    return guess_table_data


def get_img_data(player: SoccerPlayer):
    return base64.b64encode(get_player_photo(player).content).decode("utf-8")
    


if __name__ == '__main__':
    ##app.run(host='0.0.0.0')
    app.run()
