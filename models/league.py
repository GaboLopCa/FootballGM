from models.player import Player
from models.team import Team
from models.match import Match
from random import shuffle

class League:
    
    def __init__(self,name):
        self.name = name
        self.teams_list = []
        self.standings = {}
        
    def add_team(self, team):
        if team not in self.teams_list:
            self.teams_list.append(team)
            self.standings[team] = 0
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
        
        if match.home_goals > match.away_goals:
          self.standings[match.home_team] +=3
        elif match.home_goals < match.away_goals:
          self.standings[match.away_team] +=3
        else:
          self.standings[match.away_team] +=1
          self.standings[match.home_team] +=1
        
    def show_standings(self):
      sorted_list = sorted(self.standings.items(key=lambda item: item[1],reverse=True))
      i=1
      for team,points in sorted_list:
        print(f"{i}. {team} | {points}")
        i+=1