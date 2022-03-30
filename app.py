import datetime
import json
import redis

from prettytable import PrettyTable
from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_session import Session
from game_functions import *
from guess_history import GuessHistory
from random import sample




from setup import *
(players, player_map, filtered_players) = init_players()
type_ahead_helper = init_type_ahead(players)
hint_config = init_hint_config()
epl_table = init_epl_table()
confederation_mapping = init_confederation_mapping()



GUESS_HISTORY = "guess_history" 



## Store guesses for each user by day
today = datetime.datetime.today()
date = today



## Pre populate list of answers
pre_populated_answers = 100
answers = {}
random_sample = sample(filtered_players, pre_populated_answers)
for i in range(pre_populated_answers):
    date += datetime.timedelta(days=i)
    answers[date.strftime('%Y-%m-%d')] = random_sample[i]
del random_sample



# Create the Flask application
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY' # TODO


# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)


@app.route('/game', methods=['GET', 'POST'])
def input_guess():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    answer = answers[today]
    if GUESS_HISTORY not in session:
        session[GUESS_HISTORY] = {}
        if today not in session[GUESS_HISTORY]:
            session[GUESS_HISTORY][today] = GuessHistory(hint_config).to_json()

    guess_history = GuessHistory.from_json(session[GUESS_HISTORY][today])
    guess_history.hint_config = hint_config
    if answer in guess_history.guesses:
        guess_history.mark_as_winner()
    
    history_table = create_history_table(guess_history)
    
    if request.method == 'POST':              
        input_name = request.form['player_name']
        valid_names = type_ahead_helper.search_ahead(input_name)
        if len(valid_names) == 1:
            name = valid_names.pop()
            if already_guessed_player(name, guess_history):
                already_guessed = """<h1>{} was already guessed</h1>""".format(name)
                return return_response(history_table + already_guessed)
            else:
                guess = player_map[name]
                process_guess(answer, guess, guess_history, epl_table, confederation_mapping)
                session[GUESS_HISTORY][today] = guess_history.to_json()
        else:
            valid_options = """<h1>Valid relevant options: {}</h1>""".format(", ".join(valid_names))
            return return_response(history_table + valid_options)
            

    # whether its get or post, we return the same response
    history_table = create_history_table(guess_history)


    if is_game_over(guess_history):
        if guess_history.is_winner:
            print(answer.get_display_name() + " is correct! YOU WIN!!")
            return return_response(history_table + winner_response())
        else:
            print("Correct answer was: " + answer.get_display_name())                
            return return_response(history_table + loser_response())
        
 
    
    return return_response(history_table)





BASE_FORM = """<label for="name">Enter player name:</label>
        <input type="name" id="name" name="player_name" required />
        <button type="submit">Submit</button>"""

                           
def loser_response():
    return """<h1>YOU LOSE! {} was the answer!</h1>""".format(get_todays_answer().get_display_name())
                           
def winner_response():
    return """<h1>YOU WIN! {} is correct!</h1>""".format(get_todays_answer().get_display_name())
                           

def get_todays_answer():
    return answers[datetime.datetime.today().strftime('%Y-%m-%d')]
                           
def return_response(extra_data: str):
    return """<form method="post">""" + BASE_FORM + extra_data + """</form>"""


def create_history_table(guess_history):
    history_table = guess_history.get_history_table(get_todays_answer(), epl_table, confederation_mapping)
    header = ["Name", "Team", "Country", "Position", "Age", "Jersey", "Goals", "Assists", "Appearances"]
    table = """<table>
      <tr>
        {}
      </tr>""".format("\n".join(["<th>{}</th>".format(h) for h in header]))
    for r in history_table:
        table += """<tr>
        {}
      </tr>""".format("\n".join(["<th>{}</th>".format(d) for d in r]))
    table += """</table>"""
    return table




if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run()