from models.player import Player
from models.team import Team
from models.match import Match

messi = Player("Messi", 37, 90)

barcelona = Team("Barcelona")
barcelona.add_player(messi)
barcelona.print_players()

madrid = Team("Madrid")
cristiano = Player("Cristiano", 40, 90)

madrid.add_player(cristiano)
madrid.print_players()

partido = Match(madrid, barcelona)
partido.simulate()