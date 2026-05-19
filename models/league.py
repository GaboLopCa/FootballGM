from models.player import Player
from models.team import Team
from models.match import Match
from random import shuffle

class League:
    
    def __init__(self,name):
        self.name = name
        self.teams_list = []
        self.standings = []

    def add_team(self, team):
        if team not in self.teams_list:
            self.teams_list.append(team)
        else:
            return False
    
    def show_teams(self):
        if not self.teams_list:
            return False
        else:
            for team in self.teams_list:
                print(team)

    def simulate_round(self):
        shuffle(self.teams_list)
        match = Match(self.teams_list[0],self.teams_list[1])
        match.simulate()
        print(match)

        match2 = Match(self.teams_list[2],self.teams_list[3])
        match2.simulate()
        print(match2)