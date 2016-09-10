from flask import Flask
from flask import jsonify
from flask import render_template

from nba_info.teams import All_TEAMS
from nba_info.nba_requests import *
from nba_info.graph_data_generators.graph_data_generator_pts import generate_data_pts

app = Flask(__name__)

# TODO - For all methods, transfer the logic to nba_requests.py to abstract logic from REST API.

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

# TODO: Currently only works for 2015-16 season. Use date ranges to make work for all seasons
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

@app.route('/team/fullname/<string:abbr>')
def get_full_name(abbr):
    return All_TEAMS[abbr]['name']

@app.route('/graphdata/<string:gameid>/<string:stat>/<string:home>/<string:away>')
def create_graph_data_for_players_and_stat(gameid, stat, home, away):
    url = 'http://stats.nba.com/stats/playbyplay?GameID=' + gameid + '&StartPeriod=1&EndPeriod=4'
    r = make_request(url)
    result = r.json()
    #Get the relevant rows
    row_set = result['resultSets'][0]['rowSet']

    if stat == "PTS":
        return generate_data_pts(home, away, row_set)
    else:
        return 'Magical edge case that should never be reached ' + stat

if __name__ == '__main__':
    app.run(debug=True)

