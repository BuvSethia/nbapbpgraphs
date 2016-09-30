__author__ = 'Sumbhav'

import re

_HOME_DESCRIPTION = 7
_AWAY_DESCRIPTION = 9
_PERIOD = 4
_PLAY_CLOCK = 6
_SCORE = 10

'''
NOTES - Right now, the easiest (but probably least efficient) way of generating data is to do one pass per player.
        This is because of the way that the names of players in a play by play differ from their actual names
        and bunch of other reasons I understand but don't know how to word. Maybe revisit this later
        to see if it's possible to make it more efficient. But honestly, one pass per player is probably the best way.
'''

# TODO LOW PRIORITY - Consider adding an option to look at data quarter by quarter (As in select one quarter and make the start of the quarter 0,0)
# TODO LOW PRIORITY - Custom tooltips
# TODO LOW PRIORITY - Add datapoints for sub-ins and sub-outs
# TODO LOW PRIORITY - Add option to remove missed shots
# TODO HIGHEST PRIORITY - Implement the rest of the stats
# TODO HIGHEST PRIORITY - Handle overtime games

# Generate graph data when selected stat is points
# TODO HIGH PRIORITY - Add away players generation
def generate_data_pts(home, away, row_set):
    graph_data = _init_config_json()
    keywords = ["Shot", "shot", "Layup", "layup", "Free", "free", "Dunk", "dunk", "Jumper", "jumper"]

    # Home roster first
    if not "NOPLAYERS" in home:
        for item in home:
            print item
            # Is the current item the whole team
            whole_team = ("(team" in item)
            # Name as it appears in a play by play
            pbp_name = _prepare_player_name(item)
            dataset = _init_dataset_json(item)
            pts = 0
            final_quarter = 0
            for row in row_set:
                # Play by play description
                desc = row[_HOME_DESCRIPTION]
                final_quarter = row[_PERIOD]
                # Is the description we're looking at talking about a made basket (and not talking about the shot clock)
                if desc and any(substring in desc for substring in keywords) and (not "Shot Clock" in desc):
                    # TODO LOWEST PRIORITY - Maybe condense the if-elif into one and then break them up in a nested if-elif because the stuff after extracting the points is exactly the same
                    if whole_team:
                        print desc
                        if not 'MISS' in desc:
                            pts = int(row[_SCORE].split(" - ")[1])
                        print str(pts)
                        time = _convert_pctime_to_timestamp(row[_PERIOD], row[_PLAY_CLOCK])
                        label = ["Q" + str(row[_PERIOD]) + ", " + str(row[_PLAY_CLOCK]), desc]
                        dataset["data"].append({"x": time, "y": pts, "label": label})
                    elif pbp_name in desc and not ("(" + pbp_name) in desc:
                        print desc
                        try:
                            if not 'MISS' in desc:
                                pts = int(re.search("\((.+?) PTS", desc).group(1))
                            print str(pts)
                            time = _convert_pctime_to_timestamp(row[_PERIOD], row[_PLAY_CLOCK])
                            # TODO LOW PRIORITY - Turn Q + period into function that accounts for overtimes
                            label = ["Q" + str(row[_PERIOD]) + ", " + str(row[_PLAY_CLOCK]), desc]
                            dataset["data"].append({"x": time, "y": pts, "label": label})
                        except AttributeError:
                            print "Could not find a value. Ignoring this pbp statement."
                    else:
                        pass
            # Add endgame value to dataset
            final_label = "Final total: " + str(pts) + " points"
            dataset["data"].append({"x": _get_game_length_as_string(final_quarter), "y": pts, "label": final_label})
            graph_data["data"]["datasets"].append(dataset)

    return graph_data


def _init_config_json():
    graph_data = dict()
    graph_data["type"] = "line"
    graph_data["data"] = {"datasets": []}
    graph_data["options"] = {
        "responsive": True,
        "title":{
            "display":True,
            "text":"NBA Play By Play Graphs"
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
                }
            }]
        }
    }
    return graph_data


def _init_dataset_json(item):
    # Prepare name for label - gets rid of sharedlast for players who share last name with teammate and remove (team) for full team
    name = item.replace("sharedlast", "").replace("(team)", "").strip()
    return {"label": name, "data": [{"x": "00:00", "y": 0, "label": "Start of game"}], "fill": False}


# Return item name as it will appear in a box score
def _prepare_player_name(player):
    # If it's the whole team, leave it untouched
    if "(team)" in player:
        return player
    # If it was determined that they player shared a last name with a teammate
    elif "sharedlast" in player:
        return player.split(" ")[0].replace("sharedlast", "")[0] + ". " + player.split(" ")[-1]
    else:
        return player.split(" ")[-1]


def _convert_pctime_to_timestamp(quarter, pctime):
    if quarter <= 4:
        total_minutes = quarter * 12
    else:
        total_minutes = 48 + (quarter - 4) * 5
    total_seconds = 60
    time_split = pctime.split(":")
    minutes = int(time_split[0])
    seconds = int(time_split[1])
    minutes = total_minutes - minutes
    if seconds > 0:
        minutes = minutes - 1
        seconds = total_seconds - seconds
    return str(minutes) + ":" + str(seconds)


def _get_game_length_as_string(quarter):
    if quarter == 4:
        return "48:00"
    else:
        return str(48 + ((quarter - 4) * 5)) + ":00"
