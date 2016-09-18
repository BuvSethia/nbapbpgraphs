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
        and bunch of other reasons I understand but don't know how to word. Maybe revisit this function later
        to see if it's possible to make it more efficient. But honestly, one pass per player is probably the best way.
'''


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
                    if whole_team:
                        print desc
                        home_score = int(row[_SCORE].split(" - ")[1])
                        print str(home_score)
                        # PTS BEING EXTRACTED NOW ADD THEM TO DATASET
                    elif pbp_name in desc and not ("(" + pbp_name) in desc:
                        print desc
                        try:
                            pts = int(re.search("\((.+?) PTS", desc).group(1))
                            print str(pts)
                            # PTS BEING EXTRACTED NOW ADD THEM TO DATASET
                        except AttributeError:
                            print "Could not find a value. Ignoring this pbp statement."
                    else:
                        pass

    return graph_data


# TODO HIGH PRIORITY - Detail options
def _init_config_json():
    graph_data = dict()
    graph_data["type"] = "line"
    graph_data["data"] = {"datasets": []}
    graph_data["options"] = dict()
    return graph_data


# TODO HIGH PRIORITY - Generate and insert color settings as well
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
        #print player.split(" ")[0].replace("sharedlast", "")[0] + ". " + player.split(" ")[-1]
        return player.split(" ")[0].replace("sharedlast", "")[0] + ". " + player.split(" ")[-1]
    else:
        return player.split(" ")[-1]
