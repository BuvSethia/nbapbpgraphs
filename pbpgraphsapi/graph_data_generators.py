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
# TODO MEDIUM PRIORITY - Move color configuration and moment time conversion to front end
# TODO LOW PRIORITY - Custom tooltips
# TODO LOW PRIORITY - Add datapoints for sub-ins and sub-outs
# TODO HIGH PRIORITY - Free throws occur at the same timestamp for each pair of free throws. Figure out how to handle this in the data generation (if the graph ends up looking bad)
# TODO MEDIUM PRIORITY - Add final data point for end of 4th quarter for each player

# Generate graph data when selected stat is points
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
            for row in row_set:
                # Play by play description
                desc = row[_HOME_DESCRIPTION]
                # Is the description we're looking at talking about a made basket
                if desc and any(substring in desc for substring in keywords) and (not 'MISS' in desc):
                    # TODO LOWEST PRIORITY - Maybe condense the if-elif into one and then break them up in a nested if-elif because the stuff after extracting the points is exactly the same
                    if whole_team:
                        print desc
                        pts = int(row[_SCORE].split(" - ")[1])
                        print str(pts)
                        time = _convert_pctime_to_timestamp(row[_PERIOD], row[_PLAY_CLOCK])
                        dataset["data"].append({"x": time, "y": pts})
                    elif pbp_name in desc and not ("(" + pbp_name) in desc:
                        print desc
                        try:
                            pts = int(re.search("\((.+?) PTS", desc).group(1))
                            print str(pts)
                            time = _convert_pctime_to_timestamp(row[_PERIOD], row[_PLAY_CLOCK])
                            dataset["data"].append({"x": time, "y": pts})
                        except AttributeError:
                            print "Could not find a value. Ignoring this pbp statement."
                    else:
                        pass
            graph_data["data"]["datasets"].append(dataset)

    return graph_data


# TODO HIGH PRIORITY - Detail options (maybe on the front end?)
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
                    "labelString": 'Minutes'
                }
            }],
            "yAxes": [{
                "scaleLabel": {
                    "display": True,
                    # TODO LOW PRIORITY - Make this the acutal stat being displayed
                    "labelString": 'Value'
                }
            }]
        },
    }
    return graph_data


def _init_dataset_json(item):
    # Prepare name for label - gets rid of sharedlast for players who share last name with teammate and remove (team) for full team
    name = item.replace("sharedlast", "").replace("(team)", "").strip()
    return {"label": name, "data": [{"x": "00:00", "y": 0}], "fill": False}


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


# TODO HIGHEST PRIORITY - Finish this function
# TODO - Might have to format so minutes and seconds are ALWAYS mm:ss (right now could potentially return m:s)
def _convert_pctime_to_timestamp(quarter, pctime):
    total_minutes = quarter * 12
    total_seconds = 60
    time_split = pctime.split(":")
    minutes = int(time_split[0])
    seconds = int(time_split[1])
    minutes = total_minutes - minutes
    if seconds > 0:
        minutes = minutes - 1
        seconds = total_seconds - seconds
    return str(minutes) + ":" + str(seconds)
