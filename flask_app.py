# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import jsonify
from flask import render_template
from nba_info.teams import All_TEAMS
import requests

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/games/<string:date>')
def games_for_date(date):
    #Get the result from nba.com
    url = 'http://stats.nba.com/stats/scoreboard?DayOffset=0&LeagueID=00&GameDate=' + date
    #BORROWED FROM seemsthere's nba_py
    headers = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/45.0.2454.101 Safari/537.36'),
               'referer': 'http://stats.nba.com/scores/'
            }
    r = requests.get(url, headers=headers)
    try:
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
    pass

if __name__ == '__main__':
    app.run(debug=True)

