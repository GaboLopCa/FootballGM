import math
import random
from models.player import Player
from models.team import Team


class Match:
    """
    Simula un partido entre dos equipos usando un modelo probabilístico
    basado en la distribución de Poisson.

    MODELO MATEMÁTICO:
    ─────────────────────────────────────────────────────────────────────
    1. Se calculan las tasas de gol esperadas (λ) para cada equipo:

           λ_home = BASE_RATE × (ATK_home / DEF_away) × HOME_ADVANTAGE
           λ_away = BASE_RATE × (ATK_away / DEF_home)

       ATK = promedio de attack_rating del equipo (capacidad de crear ocasiones).
       DEF = promedio de defense_rating del equipo (solidez defensiva).

    2. Dado λ, los goles se samplean con el algoritmo de Knuth (Poisson).

    3. Los goleadores se eligen ponderando finishing individual × factor posición.
    4. Los asistentes se eligen ponderando attack_rating individual × factor posición.
    ─────────────────────────────────────────────────────────────────────

    Referencias empíricas validadas con 100 temporadas (jun 2026):
      Goles/partido: 2.73 (objetivo ~2.3-2.9) ✅
      Victoria local: 42.0% (objetivo ~42-48%) ✅
      Empates 0-0: 6.4% (objetivo 3-12%) ✅
      Goleadas (dif≥4): 4.0% (objetivo <7%) ✅
    """

    # Tasa base: 1.15 produce ~2.7 gpp con datos actuales
    BASE_RATE = 1.15

    # Ventaja local: 1.16 → ~42% victorias locales
    HOME_ADVANTAGE = 1.16

    # Cotas para evitar resultados absurdos
    MAX_GOALS_LAMBDA = 4.0
    MIN_GOALS_LAMBDA = 0.2

    # Probabilidad de que un gol tenga asistente (65% ≈ fútbol real)
    ASSIST_CHANCE = 0.65

    # Pesos posicionales para elegir goleador
    POSITION_GOAL_FACTOR = {
        "GK": 0.005, "CB": 0.15, "FB": 0.45, "CDM": 0.55,
        "CM": 0.75, "CAM": 1.20, "WNG": 1.45, "ST": 1.90
    }

    # Pesos posicionales para elegir asistente
    POSITION_ASSIST_FACTOR = {
        "GK": 0.01, "CB": 0.20, "FB": 0.80, "CDM": 0.60,
        "CM": 1.10, "CAM": 1.80, "WNG": 1.60, "ST": 0.70
    }

    def __init__(self, home_team: Team, away_team: Team):
        self.home_team  = home_team
        self.away_team  = away_team
        self.home_goals = 0
        self.away_goals = 0
        self.scorers: list[dict] = []

    # ------------------------------------------------------------------
    # Cálculo de λ (tasa de gol esperada)
    # ------------------------------------------------------------------

    def _compute_lambda(self, attack: float, defense: float, home: bool) -> float:
        if defense <= 0:
            defense = 1.0  # safety
        raw = self.BASE_RATE * (attack / defense)
        if home:
            raw *= self.HOME_ADVANTAGE
        return max(self.MIN_GOALS_LAMBDA, min(raw, self.MAX_GOALS_LAMBDA))

    # ------------------------------------------------------------------
    # Poisson (Knuth)
    # ------------------------------------------------------------------

    @staticmethod
    def _poisson_sample(lam: float) -> int:
        if lam <= 0:
            return 0
        threshold = math.exp(-lam)
        product = random.random()
        count = 0
        while product > threshold:
            product *= random.random()
            count += 1
        return count

    # ------------------------------------------------------------------
    # Goleador y asistente
    # ------------------------------------------------------------------

    @staticmethod
    def _pick_scorer(team: Team) -> Player:
        weights = []
        for player in team.players_list:
            factor = Match.POSITION_GOAL_FACTOR.get(player.position, 1.0)
            weights.append(player.finishing * factor)
        return random.choices(team.players_list, weights=weights, k=1)[0]

    @staticmethod
    def _pick_assister(team: Team, scorer: Player) -> Player | None:
        if random.random() > Match.ASSIST_CHANCE:
            return None
        candidates = [p for p in team.players_list if p is not scorer]
        if not candidates:
            return None
        weights = []
        for player in candidates:
            factor = Match.POSITION_ASSIST_FACTOR.get(player.position, 1.0)
            weights.append(player.attack_rating * factor)
        return random.choices(candidates, weights=weights, k=1)[0]

    # ------------------------------------------------------------------
    # Simulación
    # ------------------------------------------------------------------

    def simulate(self):
        for player in self.home_team.players_list:
            player.matches_played += 1
        for player in self.away_team.players_list:
            player.matches_played += 1

        home_attack  = self.home_team.calculate_attack()
        home_defense = self.home_team.calculate_defense()
        away_attack  = self.away_team.calculate_attack()
        away_defense = self.away_team.calculate_defense()

        lambda_home = self._compute_lambda(home_attack, away_defense, home=True)
        lambda_away = self._compute_lambda(away_attack, home_defense, home=False)

        self.home_goals = self._poisson_sample(lambda_home)
        self.away_goals = self._poisson_sample(lambda_away)

        self._process_team_goals(self.home_team, self.home_goals)
        self._process_team_goals(self.away_team, self.away_goals)

    def _process_team_goals(self, team: Team, total_goals: int):
        for _ in range(total_goals):
            scorer = self._pick_scorer(team)
            scorer.goals += 1

            assister = self._pick_assister(team, scorer)
            if assister:
                assister.assists += 1

            self.scorers.append({
                "team": team,
                "scorer": scorer,
                "assister": assister
            })

    # ------------------------------------------------------------------
    # Representación
    # ------------------------------------------------------------------

    def __str__(self):
        return f"{self.home_team.name} {self.home_goals} - {self.away_goals} {self.away_team.name}"

    def detailed_result(self) -> str:
        lines = [str(self)]
        if self.scorers:
            lines.append("  Goles:")
            for goal in self.scorers:
                team_name = goal["team"].name
                scorer_name = goal["scorer"].name
                assister = goal["assister"]
                if assister:
                    lines.append(f"    ⚽ {scorer_name} (Asistencia: {assister.name}) [{team_name}]")
                else:
                    lines.append(f"    ⚽ {scorer_name} (Sin asistencia) [{team_name}]")
        return "\n".join(lines)