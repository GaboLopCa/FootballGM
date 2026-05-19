from models.player import Player
from models.team import Team
from random import randint

class Match:
  def __init__(self, home_team, away_team):
    self.home_team = home_team
    self.away_team = away_team
    self.home_goals = 0
    selff.away_goals = 0
    
  def simulate(self):
    #Getting both teams aerage ovr
    home_ovr = self.home_team.calculate_overall()
    away_ovr = self.away_team.calculate_overall()
    
    home_attacks = (home_ovr/10) += randint(-3,5)
    for attack in home_attacks:
      chance = home_ovr/5
      roll = randint()
    away_attacks = (away_ovr/10) += randint(-3,5)