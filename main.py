from models.player import Player
from models.team import Team

messi = Player("Messi", 37, 90)

barcelona = Team("Barcelona")
barcelona.add_player(messi)
barcelona.print_players()

messi.increase_overall(-2)
barcelona.print_players()

print(barcelona)