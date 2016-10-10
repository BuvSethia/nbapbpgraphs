from flask import Flask, render_template, request
from pbpgraphsapi.nba_requests import *

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/games/<string:date>')
def games_for_date(date):
    return fetch_games_for_date(date)


@app.route('/roster/<string:team>')
def get_roster(team):
    return fetch_roster(team)


@app.route('/team/fullname/<string:abbr>')
def get_full_name(abbr):
    return fetch_team_name(abbr)


@app.route('/graphdata', methods=['POST'])
def create_graph_data():
    return generate_graph_data(request.json['gameid'], request.json['stat'], request.json['type'], request.json['home'], request.json['away'])


if __name__ == '__main__':
    app.run(debug=True)
