from models.player import Player
from models.team import Team
from random import randint

class Match:
  def __init__(self, home_team, away_team):
    self.home_team = home_team
    self.away_team = away_team
    self.home_goals = 0
    self.away_goals = 0

  def simulate(self):

    #Getting both teams average ovr
    home_ovr = self.home_team.calculate_overall()
    away_ovr = self.away_team.calculate_overall()


    #Simulating attacks and goals
    home_attacks = int((home_ovr/15) + randint(-1,2))

    if home_attacks < 1:
      home_attacks = 1

    for attack in range(home_attacks):
      chance = 20 + ((home_ovr-away_ovr)*2)
      
      if chance < 5:
        chance = 5
      if chance > 85:
        chance = 85

      roll = randint(1,100)

      if roll <=chance:
        self.home_goals +=1

    away_attacks = int((away_ovr/15) + randint(-1,2))

    if away_attacks < 1:
      away_attacks = 1

    for attack in range(away_attacks):
      chance = 20 + ((away_ovr-home_ovr)*2)
      
      if chance < 5:
        chance = 5
      if chance > 85:
        chance = 85

      roll = randint(1,100)

      if roll <=chance:
        self.away_goals +=1
        
  def __str__(self):
    return f"{self.home_team.name} {self.home_goals} - {self.away_goals} {self.away_team.name}"