from models.player import Player
from models.team import Team
from models.league import League

# ARSENAL
arsenal = Team("Arsenal")

arsenal.add_player(Player("David Raya", 29, 84))
arsenal.add_player(Player("Ben White", 27, 84))
arsenal.add_player(Player("William Saliba", 24, 89))
arsenal.add_player(Player("Gabriel Magalhães", 27, 87))
arsenal.add_player(Player("Oleksandr Zinchenko", 28, 82))
arsenal.add_player(Player("Declan Rice", 26, 90))
arsenal.add_player(Player("Martin Ødegaard", 26, 89))
arsenal.add_player(Player("Kai Havertz", 25, 84))
arsenal.add_player(Player("Bukayo Saka", 23, 91))
arsenal.add_player(Player("Gabriel Martinelli", 23, 85))
arsenal.add_player(Player("Leandro Trossard", 30, 83))



# MANCHESTER CITY
man_city = Team("Manchester City")

man_city.add_player(Player("Ederson", 31, 88))
man_city.add_player(Player("Kyle Walker", 34, 84))
man_city.add_player(Player("Ruben Dias", 27, 89))
man_city.add_player(Player("John Stones", 30, 87))
man_city.add_player(Player("Josko Gvardiol", 23, 88))
man_city.add_player(Player("Rodri", 28, 92))
man_city.add_player(Player("Kevin De Bruyne", 33, 91))
man_city.add_player(Player("Bernardo Silva", 30, 89))
man_city.add_player(Player("Phil Foden", 24, 91))
man_city.add_player(Player("Jeremy Doku", 22, 85))
man_city.add_player(Player("Erling Haaland", 24, 93))


# LIVERPOOL
liverpool = Team("Liverpool")

liverpool.add_player(Player("Alisson", 32, 89))
liverpool.add_player(Player("Trent Alexander-Arnold", 26, 87))
liverpool.add_player(Player("Virgil van Dijk", 33, 90))
liverpool.add_player(Player("Ibrahima Konaté", 25, 85))
liverpool.add_player(Player("Andrew Robertson", 31, 84))
liverpool.add_player(Player("Alexis Mac Allister", 26, 86))
liverpool.add_player(Player("Dominik Szoboszlai", 24, 85))
liverpool.add_player(Player("Curtis Jones", 24, 82))
liverpool.add_player(Player("Mohamed Salah", 32, 91))
liverpool.add_player(Player("Luis Díaz", 28, 86))
liverpool.add_player(Player("Darwin Núñez", 25, 84))


# REAL MADRID
real_madrid = Team("Real Madrid")

real_madrid.add_player(Player("Thibaut Courtois", 33, 90))
real_madrid.add_player(Player("Dani Carvajal", 33, 84))
real_madrid.add_player(Player("Antonio Rüdiger", 32, 88))
real_madrid.add_player(Player("Éder Militão", 27, 86))
real_madrid.add_player(Player("Ferland Mendy", 29, 83))
real_madrid.add_player(Player("Federico Valverde", 26, 89))
real_madrid.add_player(Player("Aurélien Tchouaméni", 25, 86))
real_madrid.add_player(Player("Jude Bellingham", 21, 91))
real_madrid.add_player(Player("Vinícius Jr.", 24, 92))
real_madrid.add_player(Player("Rodrygo", 24, 87))
real_madrid.add_player(Player("Kylian Mbappé", 26, 94))

champions = League("Champions League")
champions.add_team(real_madrid)
champions.add_team(man_city)
champions.add_team(liverpool)
champions.add_team(arsenal)

champions.simulate_round()
champions.show_standings()