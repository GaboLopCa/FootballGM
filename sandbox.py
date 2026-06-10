from models.player import Player
from models.team import Team
from models.league import League
import services.team_repository as team_repo

# PORTUGAL
portugal = Team("Portugal")

portugal.add_player(Player("Diogo Costa", 26, 87))
portugal.add_player(Player("Joao Cancelo", 31, 86))
portugal.add_player(Player("Ruben Dias", 29, 89))
portugal.add_player(Player("Antonio Silva", 22, 83))
portugal.add_player(Player("Nuno Mendes", 24, 86))
portugal.add_player(Player("Vitinha", 26, 87))
portugal.add_player(Player("Joao Neves", 21, 85))
portugal.add_player(Player("Bruno Fernandes", 31, 89))
portugal.add_player(Player("Rafael Leao", 27, 87))
portugal.add_player(Player("Bernardo Silva", 32, 89))
portugal.add_player(Player("Cristiano Ronaldo", 41, 85))

team_repo.save_team(portugal)

# COLOMBIA
colombia = Team("Colombia")

colombia.add_player(Player("Camilo Vargas", 37, 82))
colombia.add_player(Player("Daniel Munoz", 30, 84))
colombia.add_player(Player("Davinson Sanchez", 30, 81))
colombia.add_player(Player("Carlos Cuesta", 27, 79))
colombia.add_player(Player("Deiver Machado", 32, 78))
colombia.add_player(Player("Jefferson Lerma", 32, 82))
colombia.add_player(Player("Richard Rios", 26, 81))
colombia.add_player(Player("James Rodriguez", 35, 84))
colombia.add_player(Player("Luis Diaz", 29, 88))
colombia.add_player(Player("Jhon Arias", 29, 82))
colombia.add_player(Player("Jhon Duran", 23, 84))

team_repo.save_team(colombia)

# UZBEKISTÁN
uzbekistan = Team("Uzbekistan")

uzbekistan.add_player(Player("Utkir Yusupov", 34, 74))
uzbekistan.add_player(Player("Khojiakbar Alijonov", 29, 74))
uzbekistan.add_player(Player("Rustam Ashurmatov", 29, 73))
uzbekistan.add_player(Player("Abdukodir Khusanov", 22, 80))
uzbekistan.add_player(Player("Zafarmurod Abdirakhmatov", 25, 72))
uzbekistan.add_player(Player("Otabek Shukurov", 30, 74))
uzbekistan.add_player(Player("Odiljon Hamrobekov", 29, 73))
uzbekistan.add_player(Player("Jaloliddin Masharipov", 33, 76))
uzbekistan.add_player(Player("Abbosbek Fayzullaev", 23, 79))
uzbekistan.add_player(Player("Oston Urunov", 25, 73))
uzbekistan.add_player(Player("Eldor Shomurodov", 31, 77))

team_repo.save_team(uzbekistan)

# RD CONGO
rd_congo = Team("RD Congo")

rd_congo.add_player(Player("Dimitry Bertaud", 27, 72))
rd_congo.add_player(Player("Gedeon Kalulu", 29, 73))
rd_congo.add_player(Player("Chancel Mbemba", 32, 79))
rd_congo.add_player(Player("Dylan Batubinsika", 29, 72))
rd_congo.add_player(Player("Arthur Masuaku", 33, 74))
rd_congo.add_player(Player("Samuel Moutoussamy", 29, 73))
rd_congo.add_player(Player("Edo Kayembe", 28, 74))
rd_congo.add_player(Player("Gael Kakuta", 35, 75))
rd_congo.add_player(Player("Yoane Wissa", 30, 82))
rd_congo.add_player(Player("Meschack Elia", 29, 76))
rd_congo.add_player(Player("Cedric Bakambu", 35, 77))

team_repo.save_team(rd_congo)