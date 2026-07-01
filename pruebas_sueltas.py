import services.team_repository as team_repo
from models.team import Team

u_de_chile = team_repo.load_team("Universidad de Chile")

for player in u_de_chile.players_list:
    print(
        player.name,
        type(player.attack_rating),
        player.attack_rating,
        type(player.defense_rating),
        player.defense_rating
    )