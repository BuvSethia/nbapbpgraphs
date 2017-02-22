from flask import jsonify
from teams import All_TEAMS
from graph_data_generator import generate_data
import requests


def fetch_games_for_date(date):
    # Get the result from nba.com
	url = 'http://stats.nba.com/stats/scoreboard?DayOffset=0&LeagueID=00&GameDate=' + date
	response = _make_request(url)
	if response["result"] is not "Error":
		row_set = response["data"]
		games = list()
		for row in row_set:
			game_id = row[2]
			name = str(row[5]).split('/')[1]
			name_formatted = name[:3] + '@' + name[3:]
			games.append({'name': name_formatted, 'id': game_id})
		return jsonify(result='Success', gameList=games)
	return jsonify(result='Error')


# TODO HIGH PRIORITY - Currently only works for 2015-16 season. Use date ranges to make work for all seasons
# TODO LOW PRIORITY - Modify to make this endpoint work for the All-Star teams as well
# TODO MEDIUM PRIORITY - Modify this to account for mid-season trades somehow
def fetch_roster(team):
    # Get the result from nba.com
    url = 'http://stats.nba.com/stats/commonteamroster?Season=2015-16&TeamID=' + (All_TEAMS[team])['id']
    response = _make_request(url)
    if response["result"] is not "Error":
        row_set = response["data"]
        players = dict()
        for row in row_set:
            # team_id = row[0], name = row[3], number = row[4], position = row[5], player_id = row[12]
            players[row[3]] = {'teamID': row[0], 'playerID': row[12], 'number': row[4], 'position': row[5]}
        return jsonify(result='Success', roster=players)
	return jsonify(result='Error', message='Unable to get the current roster for ' + team + '. Please try again later.')


def fetch_team_name(team):
    if All_TEAMS[team]:
        return All_TEAMS[team]['name']
    else:
        return "TNF"


def generate_graph_data(gameid, stat, type, home, away):
	url = 'http://stats.nba.com/stats/playbyplay?GameID=' + gameid + '&StartPeriod=1&EndPeriod=14'
	response = _make_request(url)
	if response["result"] is "Error":
		return jsonify(result='Error', message='Unable to generate graph data right now. Please try again later.')

	row_set = response["data"]
	if stat == "PTS":
		return jsonify(generate_data(home, away, row_set, 'PTS'))
	elif stat == "AST":
		return jsonify(generate_data(home, away, row_set, 'AST'))
	elif stat == 'OREB':
		return jsonify(generate_data(home, away, row_set, 'OREB'))
	elif stat == 'DREB':
		return jsonify(generate_data(home, away, row_set, 'DREB'))
	elif stat == 'TREB':
		return jsonify(generate_data(home, away, row_set, 'TREB'))
	elif stat == 'STL':
		return jsonify(generate_data(home, away, row_set, 'STL'))
	elif stat == 'BLK':
		return jsonify(generate_data(home, away, row_set, 'BLK'))
	elif stat == 'PF':
		return jsonify(generate_data(home, away, row_set, 'PF'))
	return 'Magical edge case that should never be reached ' + stat


# TODO HIGH PRIORITY - Check for return status codes here
def _make_request(url):
    headers = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/45.0.2454.101 Safari/537.36'),
               'referer': 'http://stats.nba.com/scores/'
    }
    try:
        result = requests.get(url, headers=headers).json()
        # Return the relevant rows
        return {'result': 'Success', 'data': result['resultSets'][0]['rowSet']}
    except:
		return {'result': 'Error'}
