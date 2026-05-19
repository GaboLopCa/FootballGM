from models.player import Player

class Team:
  def __init__(self, name):
    self.name = name
    self.players_list = []
  
  def __str__(self):
    return f"{self.name} | {self.calculate_overall()} OVR | {len(self.players_list)} players"
    
  def add_player(self, player):
    if player not in self.players_list:
      self.players_list.append(player)
    else:
      return False
      
  def print_players(self):
    print(f"\n{self.name} players: \n")
    for player in self.players_list:
      print(player)
      
  def calculate_overall(self):
    aggregate = 0
    if not self.players_list:
      return 0.0
    else:
      for player in self.players_list:
        aggregate += player.overall
      return (aggregate/(len(self.players_list)))