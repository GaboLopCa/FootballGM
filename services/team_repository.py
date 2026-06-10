import json
from models.team import Team

def save_team(team):
    
    try:
        with open("data/teams.json", "r") as file:
            data = json.load(file)

    except:
        data = {}

    data[team.name] = team.to_dict()

    with open("data/teams.json", "w") as file:
        json.dump(data, file, indent=4)

def load_team(name):
    
    with open("data/teams.json", "r") as file:
        data = json.load(file)

    if name not in data:
        return None

    team_data = data[name]

    return Team.from_dict(team_data)

def load_all_teams():
    
    with open("data/teams.json", "r") as file:
        data = json.load(file)
    
    return [Team.from_dict(team_data) for team_data in data.values()]