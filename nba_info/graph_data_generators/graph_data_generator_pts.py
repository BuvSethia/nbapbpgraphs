__author__ = 'Sumbhav'

HOME_DESCRIPTION = 7
AWAY_DESCRIPTION = 9

# Generate graph data when selected stat is points
'''
NOTES - Right now, the easiest (but probably least efficient) way of doing this is to do one pass per player.
        This is because of the way that the names of players in a play by play differ from their actual names
        and bunch of other reasons I understand but don't know how to word. Maybe revisit this function later
        to see if it's possible to make it more efficient.
'''
def generate_data_pts(home, away, row_set):
    graph_data = init_pts_return_json(home, away)
    keywords = ["Shot", "shot", "Layup", "layup", "Free", "free", "Dunk", "dunk"]

    return "Funky fresh rhymes"

    ''' OLD WAY OF DOING IT THAT IS WAY TOO COMPLICATED AND PROBABLY WOULDN'T HAVE WORKED...
    home_roster = prepare_player_names(home.split('_'))
    print home_roster
    home_team_selected = False
    if any("(team" in substring for substring in home_roster):
        home_team_selected = True;
    for row in row_set:
        # If players from the home team were selected by user
        if not home == 'NOPLAYERS':
            # Play by play description
            home_desc = row[HOME_DESCRIPTION]
            if home_desc and any(substring in home_desc for substring in keywords) and (not 'MISS' in home_desc):
                if any(substring in home_desc for substring in home_roster):
                    print home_desc
                if home_team_selected:
                    print "WHOLE TEAM [" + home_desc + "]"
    return "Pass complete"
    '''

# TODO - Move this process to the front end so that you can check for players with the same last name
def prepare_player_names(team):
    cleaned_names = list()
    for player in team:
        if "(team)" in player:
            cleaned_names.append(player)
        else:
            cleaned_names.append((player.split(" "))[-1])
    return cleaned_names

def init_pts_return_json(home, away):
    graph_data = dict()
    graph_data["type"] = "line"
    graph_data["data"] = dict()
    graph_data["datasets"] = list()
    for item in (home + away):
        # TODO - Generate and insert color settings as well
        dataset = {"label":item, "data":[{"x": "00:00", "y": 0}]}
        graph_data["datasets"].append(dataset)
    graph_data["options"] = dict()
    return graph_data