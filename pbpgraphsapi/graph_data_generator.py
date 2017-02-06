__author__ = 'Sumbhav'

import re

_HOME_DESCRIPTION = 7
_AWAY_DESCRIPTION = 9
_PERIOD = 4
_PLAY_CLOCK = 6
_SCORE = 10
_NOPLAYERS = 'NOPLAYERS'

# TODO LOW PRIORITY - Consider adding an option to look at data quarter by quarter (As in select one quarter and make the start of the quarter 0,0)
# TODO LOW PRIORITY - Add datapoints for sub-ins and sub-outs
# TODO LOW PRIORITY - Add option to remove missed shots
# TODO HIGHEST PRIORITY - Implement the rest of the stats
# TODO HIGHEST PRIORITY - Handle overtime games
# TODO LOWEST PRIORITY - Y-axis should always start at 0

# TODO HIGHEST PRIORITY - Add support for graph refresh
def generate_data(home, away, row_set, stat):
	graph_data = _init_config_json()
	home_data = _generate_data_for_roster('HOME', home, row_set, stat)
	away_data = _generate_data_for_roster('AWAY', away, row_set, stat)
	graph_data["data"]["datasets"].extend(home_data)
	graph_data["data"]["datasets"].extend(away_data)
	return graph_data

def _generate_data_for_roster(roster_type, roster, data, stat):
	datasets = []
	desc_loc = _index_for_roster_type(roster_type)
    # If players to evaluate
	if not _NOPLAYERS in roster:
		for item in roster:
			print item
            # Is the current item the whole team
			whole_team = ("(team" in item)
            # Name as it appears in a play by play
			pbp_name = _prepare_player_name(item)
			dataset = _init_dataset_json(item)
			value = 0
			for row in data:
                # Play by play description
				desc = row[desc_loc]
				if desc and _row_contains_stat_data(desc, stat):
					if whole_team or _stat_pertains_to_player(stat, pbp_name, desc):
						if whole_team:
							value = _extract_stat_for_whole_team(stat, row, desc, value)
						else:
							value = _extract_stat_for_player(stat, desc, value)
						time = _convert_pctime_to_timestamp(row[_PERIOD], row[_PLAY_CLOCK])
						label = ["Q" + str(row[_PERIOD]) + ", " + str(row[_PLAY_CLOCK]) + "  --  " + str(value) + " " + stat, desc]
						dataset["data"].append({"x": time, "y": value, "label": label})
            # Add endgame value to dataset if game is over
			if data[-1][_PLAY_CLOCK] == "0:00":
				final_label = "Final total: " + str(value) + " " + stat
				dataset["data"].append({"x": _get_game_length_as_string(data[-1][_PERIOD]), "y": value, "label": final_label})
				datasets.append(dataset)
	return datasets


def _init_config_json():
    graph_data = dict()
    graph_data["type"] = "line"
    graph_data["data"] = {"datasets": []}
    graph_data["options"] = {
        "responsive": True,
        "title":{
            "display": True,
            "text": "NBA Play By Play Graphs"
        },
        "scales": {
            "xAxes": [{
                "type": "time",
                "time": {
                    "format": "mm:ss",
                    "tooltipFormat": 'mm:ss',
                    "displayFormats":{
                        'second': 'mm:ss',
                        'minute': 'mm:ss'
                    }
                },
                "scaleLabel": {
                    "display": True,
                    "labelString": 'Minutes into the Game'
                }
            }],
            "yAxes": [{
                "scaleLabel": {
                    "display": True,
                    # TODO LOW PRIORITY - Make this the acutal stat being displayed
                    "labelString": 'Value'
                },
                "ticks": {
                    "suggestedMax": 20,
                    "suggestedMin": 0
                }
            }]
        }
    }

    '''
    "zoom": {
        "enabled": True,
        "mode": 'x'
    },
    '''

    return graph_data


def _init_dataset_json(item):
    # Prepare name for label - gets rid of sharedlast for players who share last name with teammate and remove (team) for full team
    name = item.replace("sharedlast", "").replace("(team)", "").strip()
    return {"label": name, "data": [{"x": "00:00", "y": 0, "label": "Start of game"}], "fill": False}


# Return item name as it will appear in a play by play
def _prepare_player_name(player):
    # If it's the whole team, leave it untouched
    if "(team)" in player:
        return player
    # If it was determined that they player shared a last name with a teammate
    elif "sharedlast" in player:
        return player.split(" ")[0].replace("sharedlast", "")[0] + ". " + player.split(" ")[-1]
    else:
        return player.split(" ")[-1]


def _convert_pctime_to_timestamp(quarter, play_clock_time):
    total_minutes = (quarter * 12) if quarter <= 4 else 48 + (quarter - 4) * 5
    total_seconds = 60
    time_split = play_clock_time.split(":")
    minutes = total_minutes - int(time_split[0])
    seconds = int(time_split[1])
    if seconds > 0:
        minutes -= 1
        seconds = total_seconds - seconds
    return str(minutes) + ":" + str(seconds)


def _get_game_length_as_string(quarter):
    return "48:00" if quarter == 4 else str(48 + ((quarter - 4) * 5)) + ":00"

def _get_keywords_for_stat(stat):
    if stat == 'PTS':
        return ["Shot", "shot", "Layup", "layup", "Free", "free", "Dunk", "dunk", "Jumper", "jumper"]
    else:
        return []

def _row_contains_stat_data(row, stat):
    if stat == 'PTS':
        return any(substring in row for substring in _get_keywords_for_stat(stat)) and (not "Shot Clock" in row)
    else:
        return False

def _period_as_string(period):
    return 'Q' + str(period) if period <= 4 else 'OT' + str(period - 4)

def _index_for_roster_type(roster):
    return _HOME_DESCRIPTION if roster == 'HOME' else _AWAY_DESCRIPTION

def _extract_stat_for_whole_team(stat, row, description, current_value):
	if stat == 'PTS':
		if not 'MISS' in description:
			return int(row[_SCORE].split(" - ")[1])
		else:
			return current_value
	else:
		return None

def _extract_stat_for_player(stat, description, current_value):
	if stat == 'PTS':
		if not 'MISS' in description:
			return int(re.search("\((.+?) PTS", description).group(1))
		else:
			return current_value
	else:
		return None

def _stat_pertains_to_player(stat, pbp_name, desc):
	if stat == 'PTS':
		return pbp_name in desc and not ("(" + pbp_name) in desc
	else:
		return False
