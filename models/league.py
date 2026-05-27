from models.player import Player
from models.team import Team
from models.match import Match
from random import shuffle

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
            self.standings[team] = 0
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

            if match.home_goals > match.away_goals:
                self.standings[match.home_team] += 3

            elif match.home_goals < match.away_goals:
                self.standings[match.away_team] += 3

            else:
                self.standings[match.home_team] += 1
                self.standings[match.away_team] += 1

        self.current_round += 1
        
    def show_standings(self):
      sorted_list = sorted(self.standings.items(), key=lambda item: item[1],reverse=True)
      i=1
      for team,points in sorted_list:
        print(f"{i}. {team.name} | Points: {points}")
        i+=1

    def generate_fixture(self, format):

        match format:

            case "1round_league":

                teams = self.teams_list.copy()

                if len(teams) % 2 != 0:
                    teams.append(None)

                total_rounds = len(teams) - 1
                matches_per_round = len(teams) // 2

                for round in range(total_rounds):

                    round_matches = []

                    for i in range(matches_per_round):

                        team1 = teams[i]
                        team2 = teams[-(i+1)]

                        if team1 is not None and team2 is not None:
                            round_matches.append((team1, team2))

                    self.fixtures.append(round_matches)

                    teams.insert(1, teams.pop())


            case "2round_league":

                teams = self.teams_list.copy()

                if len(teams) % 2 != 0:
                    teams.append(None)

                total_rounds = len(teams) - 1
                matches_per_round = len(teams) // 2

                first_leg = []
                second_leg = []

                for round in range(total_rounds):

                    round_matches = []
                    reverse_matches = []

                    for i in range(matches_per_round):

                        team1 = teams[i]
                        team2 = teams[-(i+1)]

                        if team1 is not None and team2 is not None:

                            round_matches.append((team1, team2))
                            reverse_matches.append((team2, team1))

                    first_leg.append(round_matches)
                    second_leg.append(reverse_matches)

                    teams.insert(1, teams.pop())

                self.fixtures = first_leg + second_leg