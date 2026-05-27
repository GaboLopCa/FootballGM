from models.player import Player
from models.team import Team
from models.league import League


# REAL MADRID
real_madrid = Team("Real Madrid")

real_madrid.add_player(Player("Courtois", 33, 90))
real_madrid.add_player(Player("Carvajal", 33, 84))
real_madrid.add_player(Player("Rüdiger", 32, 88))
real_madrid.add_player(Player("Militao", 27, 86))
real_madrid.add_player(Player("Mendy", 29, 83))
real_madrid.add_player(Player("Valverde", 26, 89))
real_madrid.add_player(Player("Tchouameni", 25, 86))
real_madrid.add_player(Player("Bellingham", 21, 91))
real_madrid.add_player(Player("Vinicius Jr", 24, 92))
real_madrid.add_player(Player("Rodrygo", 24, 87))
real_madrid.add_player(Player("Mbappe", 26, 94))


# DORTMUND
dortmund = Team("Borussia Dortmund")

dortmund.add_player(Player("Kobel", 27, 86))
dortmund.add_player(Player("Ryerson", 27, 79))
dortmund.add_player(Player("Schlotterbeck", 25, 84))
dortmund.add_player(Player("Sule", 29, 81))
dortmund.add_player(Player("Bensebaini", 30, 79))
dortmund.add_player(Player("Can", 31, 80))
dortmund.add_player(Player("Sabitzer", 31, 83))
dortmund.add_player(Player("Brandt", 29, 85))
dortmund.add_player(Player("Adeyemi", 23, 82))
dortmund.add_player(Player("Malen", 26, 83))
dortmund.add_player(Player("Guirassy", 29, 86))


# CELTIC
celtic = Team("Celtic")

celtic.add_player(Player("Joe Hart", 38, 77))
celtic.add_player(Player("Johnston", 26, 75))
celtic.add_player(Player("Carter-Vickers", 27, 78))
celtic.add_player(Player("Scales", 26, 73))
celtic.add_player(Player("Taylor", 27, 74))
celtic.add_player(Player("McGregor", 32, 80))
celtic.add_player(Player("Hatate", 27, 77))
celtic.add_player(Player("O'Riley", 24, 81))
celtic.add_player(Player("Maeda", 27, 78))
celtic.add_player(Player("Kyogo", 30, 80))
celtic.add_player(Player("Palma", 25, 76))


# SHERIFF
sheriff = Team("Sheriff Tiraspol")

sheriff.add_player(Player("Koval", 32, 68))
sheriff.add_player(Player("Zohouri", 24, 66))
sheriff.add_player(Player("Garananga", 24, 67))
sheriff.add_player(Player("Tovar", 23, 65))
sheriff.add_player(Player("Artunduaga", 30, 66))
sheriff.add_player(Player("Badolo", 25, 69))
sheriff.add_player(Player("Talal", 27, 68))
sheriff.add_player(Player("Joao Paulo", 27, 67))
sheriff.add_player(Player("Luvannor", 35, 70))
sheriff.add_player(Player("Ankeye", 22, 71))
sheriff.add_player(Player("Ngom Mbekeli", 26, 68))


# LEAGUE
champions = League("UEFA Champions League")

champions.add_team(real_madrid)
champions.add_team(dortmund)
champions.add_team(celtic)
champions.add_team(sheriff)


# TEAM PREVIEW
print(real_madrid)
print(dortmund)
print(celtic)
print(sheriff)

print("\n")


# GENERATE FIXTURE
champions.generate_fixture("2round_league")


# SIMULATE ALL MATCHDAYS
for i in range(len(champions.fixtures)):

    champions.simulate_round()

    print("\nTABLA:\n")

    champions.show_standings()

    print("\n============================\n")