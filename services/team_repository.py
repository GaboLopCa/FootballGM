import json
from pathlib import Path
from models.team import Team

_BASE_DIR = Path(__file__).resolve().parent.parent
_DATA_PATH = _BASE_DIR / "data" / "teams.json"

def save_team(team):
    
    try:
        with open(_DATA_PATH, "r") as file:
            data = json.load(file)

    except:
        data = {}

    data[team.name] = team.to_dict()

    with open(_DATA_PATH, "w") as file:
        json.dump(data, file, indent=4)

def load_team(name):
    
    with open(_DATA_PATH, "r") as file:
        data = json.load(file)

    if name not in data:
        return None

    team_data = data[name]

    return Team.from_dict(team_data)

def load_all_teams():
    
    with open(_DATA_PATH, "r") as file:
        data = json.load(file)
    
    return [Team.from_dict(team_data) for team_data in data.values()]
