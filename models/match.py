import math
import random
from models.player import Player
from models.team import Team


class Match:
    """
    Simula un partido entre dos equipos usando un modelo probabilístico
    basado en la distribución de Poisson, inspirado en el modelo Dixon-Coles (1997).

    MODELO MATEMÁTICO — RESUMEN:
    ─────────────────────────────────────────────────────────────────────
    1. Se calculan las tasas de gol esperadas (λ) para cada equipo:

           λ_home = BASE_RATE × (ATK_home / DEF_away) × HOME_ADVANTAGE
           λ_away = BASE_RATE × (ATK_away / DEF_home)

       Donde ATK = promedio de attack_rating del equipo (no finishing).
       attack_rating mide capacidad colectiva de generar ocasiones de gol.

    2. Dado λ, los goles se samplean usando el algoritmo de Knuth (Poisson).

    3. Los goleadores se eligen ponderando el atributo finishing individual
       (no attack_rating) y su posición.

    4. Los asistentes se eligen ponderando el atributo attack_rating individual
       y su posición (los creadores de juego asisten más que los rematadores).
    ─────────────────────────────────────────────────────────────────────
    """

    # Ajustado a 1.15 para mantener ~2.6 goles por partido en promedio
    BASE_RATE = 1.15

    # Incrementado a 1.16 para corregir la alerta y devolver las victorias locales al ~42-44%
    HOME_ADVANTAGE = 1.16

    MAX_GOALS = 9

    # Probabilidad base de que un gol sea asistido (65% es el estándar real)
    ASSIST_CHANCE = 0.65

    # Factores de peso para goles según posición
    POSITION_GOAL_FACTOR = {
        "GK": 0.005,
        "CB": 0.15,
        "FB": 0.45,
        "CDM": 0.55,
        "CM": 0.75,
        "CAM": 1.20,
        "WNG": 1.45,
        "ST": 1.90
    }

    # Factores de peso para asistencias según posición (los creadores dominan aquí)
    POSITION_ASSIST_FACTOR = {
        "GK": 0.01,
        "CB": 0.20,
        "FB": 0.80,
        "CDM": 0.60,
        "CM": 1.10,
        "CAM": 1.80,
        "WNG": 1.60,
        "ST": 0.70
    }

    def __init__(self, home_team: Team, away_team: Team):
        self.home_team  = home_team
        self.away_team  = away_team
        self.home_goals = 0
        self.away_goals = 0

        # Ahora estructuramos cada gol como un diccionario con más contexto
        self.scorers: list[dict] = []

    # ------------------------------------------------------------------
    # Cálculo de tasas de gol esperadas  →  λ (lambda)
    # ------------------------------------------------------------------

    def _compute_lambda(self, attack: float, defense: float, home: bool) -> float:
        raw_lambda = self.BASE_RATE * (attack / defense)
        if home:
            raw_lambda *= self.HOME_ADVANTAGE
        return max(0.2, min(raw_lambda, 4.0))

    # ------------------------------------------------------------------
    # Sampleo de Poisson
    # ------------------------------------------------------------------

    @staticmethod
    def _poisson_sample(lam: float) -> int:
        threshold = math.exp(-lam)
        product = random.random()
        count   = 0
        while product > threshold:
            product *= random.random()
            count   += 1
        return count

    # ------------------------------------------------------------------
    # Lógica de Eventos de Gol (Goleador y Asistente)
    # ------------------------------------------------------------------

    @staticmethod
    def _pick_scorer(team: Team) -> Player:
        """
        Elige al goleador ponderando finishing y su posición.
        Los jugadores con alto finishing (delanteros goleadores) tienen más
        probabilidad de convertir, mientras que los creadores de juego
        (alto attack_rating, bajo finishing) rara vez anotan.
        """
        weights = []
        for player in team.players_list:
            factor = Match.POSITION_GOAL_FACTOR.get(player.position, 1.0)
            weight = player.finishing * factor
            weights.append(weight)
        
        return random.choices(team.players_list, weights=weights, k=1)[0]

    @staticmethod
    def _pick_assister(team: Team, scorer: Player) -> Player | None:
        """
        Elige probabilísticamente al asistente del gol.
        Debe ser un compañero de equipo diferente al goleador.
        """
        if random.random() > Match.ASSIST_CHANCE:
            return None  # Gol sin asistencia (jugada individual, penal, rebote)

        # Filtrar para que el goleador no se asista a sí mismo
        potential_assisters = [p for p in team.players_list if p.name != scorer.name]
        if not potential_assisters:
            return None

        weights = []
        for player in potential_assisters:
            factor = Match.POSITION_ASSIST_FACTOR.get(player.position, 1.0)
            # Usamos attack_rating como proxy de visión ofensiva, ponderado por su posición
            weight = player.attack_rating * factor
            weights.append(weight)

        return random.choices(potential_assisters, weights=weights, k=1)[0]

    # ------------------------------------------------------------------
    # Simulación principal
    # ------------------------------------------------------------------

    def simulate(self):
        # --- 1. Registrar partido jugado ---
        for player in self.home_team.players_list:
            player.matches_played += 1
        for player in self.away_team.players_list:
            player.matches_played += 1

        # --- 2. Obtener métricas de cada equipo ---
        home_attack  = self.home_team.calculate_attack()
        home_defense = self.home_team.calculate_defense()
        away_attack  = self.away_team.calculate_attack()
        away_defense = self.away_team.calculate_defense()

        # --- 3. Calcular tasas de gol esperadas λ ---
        lambda_home = self._compute_lambda(home_attack, away_defense, home=True)
        lambda_away = self._compute_lambda(away_attack, home_defense, home=False)

        # --- 4. Samplear goles ---
        self.home_goals = self._poisson_sample(lambda_home)
        self.away_goals = self._poisson_sample(lambda_away)

        # --- 5. Procesar e integrar eventos de gol ---
        self._process_team_goals(self.home_team, self.home_goals)
        self._process_team_goals(self.away_team, self.away_goals)

    def _process_team_goals(self, team: Team, total_goals: int):
        """Asigna internamente los goles y las asistencias a los jugadores."""
        for _ in range(total_goals):
            scorer = self._pick_scorer(team)
            scorer.goals += 1

            assister = self._pick_assister(team, scorer)
            if assister:
                assister.assists += 1

            # Guardamos el evento con estructura expandible
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
        """Resultado detallado con goleadores, asistentes y contexto para diagnóstico."""
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