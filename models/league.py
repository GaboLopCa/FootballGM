from models.player import Player
from models.team import Team
from models.match import Match
import random

class League:
    
    def __init__(self,name):
        self.name = name
        self.teams_list = []
        self.standings = {}
        self.fixtures = []
        self.current_round = 0
        
    def add_team(self, team):
        if team not in self.teams_list:
            self.teams_list.append(team)
           
            self.standings[team] = {
                "pts": 0,
                "pj": 0,
                "g": 0,
                "e": 0,
                "p": 0,
                "gf": 0,
                "gc": 0,
                "dg": 0
            }

        else:
            return False
    
    def show_teams(self):
        if not self.teams_list:
            return False
        else:
            for team in self.teams_list:
                print(team)

    def simulate_round(self):

        if self.current_round >= len(self.fixtures):
            print("No quedan jornadas")
            return

        print(f"\n--- JORNADA {self.current_round + 1} ---\n")

        current_matches = self.fixtures[self.current_round]

        for fixture in current_matches:

            team1, team2 = fixture

            match = Match(team1, team2)
            match.simulate()

            print(match)

            # Partidos jugados
            self.standings[match.home_team]["pj"] += 1
            self.standings[match.away_team]["pj"] += 1

            # Goles
            self.standings[match.home_team]["gf"] += match.home_goals
            self.standings[match.home_team]["gc"] += match.away_goals

            self.standings[match.away_team]["gf"] += match.away_goals
            self.standings[match.away_team]["gc"] += match.home_goals

            if match.home_goals > match.away_goals:

                self.standings[match.home_team]["pts"] += 3

                self.standings[match.home_team]["g"] += 1
                self.standings[match.away_team]["p"] += 1

            elif match.home_goals < match.away_goals:

                self.standings[match.away_team]["pts"] += 3

                self.standings[match.away_team]["g"] += 1
                self.standings[match.home_team]["p"] += 1

            else:

                self.standings[match.home_team]["pts"] += 1
                self.standings[match.away_team]["pts"] += 1

                self.standings[match.home_team]["e"] += 1
                self.standings[match.away_team]["e"] += 1

            # Diferencia de gol
            self.standings[match.home_team]["dg"] = (
                self.standings[match.home_team]["gf"]
                - self.standings[match.home_team]["gc"]
            )

            self.standings[match.away_team]["dg"] = (
                self.standings[match.away_team]["gf"]
                - self.standings[match.away_team]["gc"]
            )

        self.current_round += 1
        
    def show_standings(self):

        # item[0] = equipo
        # item[1] = estadísticas del equipo
        sorted_list = sorted(
            self.standings.items(),

            # Ordenar primero por puntos
            key=lambda item: (
                item[1]["pts"],
                item[1]["dg"],
                item[1]["gf"]              
            ),
            # De mayor a menor
            reverse=True
        )

        print("\nTABLA DE POSICIONES\n")

        pos_width  = max(3, len(str(len(sorted_list))))
        name_width = max(len(team.name) for team, _ in sorted_list)

        header = (
            f"{'Pos':>{pos_width}}  "
            f"{'Equipo':<{name_width}}  "
            f"{'PTS':>3}  "
            f"{'PJ':>3}  "
            f"{'G':>3}  "
            f"{'E':>3}  "
            f"{'P':>3}  "
            f"{'GF':>3}  "
            f"{'GC':>3}  "
            f"{'DG':>4}"
        )
        print(header)
        print("-" * len(header))

        for i, (team, stats) in enumerate(sorted_list, start=1):
            print(
                f"{i:>{pos_width}}  "
                f"{team.name:<{name_width}}  "
                f"{stats['pts']:>3}  "
                f"{stats['pj']:>3}  "
                f"{stats['g']:>3}  "
                f"{stats['e']:>3}  "
                f"{stats['p']:>3}  "
                f"{stats['gf']:>3}  "
                f"{stats['gc']:>3}  "
                f"{stats['dg']:>4}"
            )

    def generate_fixture(self, format):
        teams = self.teams_list.copy()
        random.shuffle(teams)
        if len(teams) % 2 != 0:
            teams.append(None)
        total_rounds = len(teams) - 1
        matches_per_round = len(teams) // 2
        self.fixtures = []
        if format == "1round_league":
            for _ in range(total_rounds):
                round_matches = []
                for i in range(matches_per_round):
                    team1 = teams[i]
                    team2 = teams[-(i+1)]
                    if team1 is not None and team2 is not None:
                        round_matches.append((team1, team2))
                self.fixtures.append(round_matches)
                teams.insert(1, teams.pop())
        elif format == "2round_league":
            first_leg = []
            for _ in range(total_rounds):
                round_matches = []
                for i in range(matches_per_round):
                    team1 = teams[i]
                    team2 = teams[-(i+1)]
                    if team1 is not None and team2 is not None:
                        round_matches.append((team1, team2))
                first_leg.append(round_matches)
                teams.insert(1, teams.pop())
            second_leg = [[(b, a) for (a, b) in round_matches] for round_matches in first_leg]
            self.fixtures = first_leg + second_leg


    def get_champion(self):

        sorted_list = sorted(
            self.standings.items(),
            key=lambda item: (
                item[1]["pts"],
                item[1]["dg"],
                item[1]["gf"]
            ),
            reverse=True
        )

        return sorted_list[0][0]
    
    def get_all_players(self):
        
        players = []

        for team in self.teams_list:
            players.extend(team.players_list)

        return players
    
    def show_top_scorers(self):

        players = sorted(
            self.get_all_players(),
            key=lambda player: player.goals,
            reverse=True
        )

        print("\nGOLEADORES\n")

        for i, player in enumerate(players[:10], start=1):
            print(f"{i}. {player.name} - {player.goals}")
            