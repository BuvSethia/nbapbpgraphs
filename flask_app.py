# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import jsonify
from flask import render_template
from nba_info.teams import All_TEAMS
from nba_info.nba_requests import  make_request
import requests

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/games/<string:date>')
def games_for_date(date):
    #Get the result from nba.com
    url = 'http://stats.nba.com/stats/scoreboard?DayOffset=0&LeagueID=00&GameDate=' + date
    try:
        r = make_request(url)
        result = r.json()
        #Get the relevant rows
        row_set = result['resultSets'][0]['rowSet']
        games = list()
        for row in row_set:
            game_id = row[2]
            name = str(row[5]).split('/')[1]
            name_formatted = name[:3] + '@' + name[3:]
            games.append({'name': name_formatted, 'id': game_id})

        return jsonify(result='Success', gameList=games)
    except:
        return jsonify(result='Error')

# TODO: implement get_roster function
@app.route('/roster/<string:team>')
def get_roster(team):
    #Get the result from nba.com
    url = 'http://stats.nba.com/stats/commonteamroster?Season=2015-16&TeamID=' + (All_TEAMS[team])['id']
    try:
        r = make_request(url)
        result = r.json()
        #Get the relevant rows
        row_set = result['resultSets'][0]['rowSet']
        players = dict()
        for row in row_set:
            '''
            team_id = row[0]
            name = row[3]
            number = row[4]
            position = row[5]
            player_id = row[12]
            '''
            players[row[3]] = {'teamID': row[0], 'playerID': row[12], 'number': row[4], 'position': row[5]}

        return jsonify(result='Success', roster=players)
    except:
        return jsonify(result='Error')

if __name__ == '__main__':
    app.run(debug=True)

