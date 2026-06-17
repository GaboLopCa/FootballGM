class Player:
    """
    Representa a un jugador individual dentro del simulador.

    Atributos de identidad:
        name            Nombre del jugador.
        age             Edad del jugador.
        overall         Calidad general (OVR), usada para cálculos de equipo.
        position        Posición en la cancha del jugador.
            #Posiciones:
            GK: Arquero
            CB: Centrales
            FB: Laterales
            CDM: Volante de corte
            CM: Volante mixto
            CAM: Enganche/ Media punta
            WNG: Extremos
            ST: Delantero centro

    Atributos de rendimiento especializado:
        attack_rating   Capacidad de crear juego y asistir (0-99).
                        Se usa en el equipo para ponderar el ataque colectivo
                        y en Match._pick_assister para elegir asistentes.
        defense_rating  Capacidad defensiva (0-99). Usada en el futuro para
                        calcular intercepciones, duelos defensivos, etc.
        finishing       Capacidad de anotar goles (0-99).
                        Se usa en Match._pick_scorer para elegir goleadores.
                        Delanteros goleadores: finishing alto, attack_rating bajo.
                        Creadores de juego: attack_rating alto, finishing bajo.

    Estadísticas acumuladas (se persisten en JSON entre sesiones):
        goals           Goles marcados en la temporada/carrera.
        assists         Asistencias otorgadas.
        matches_played  Partidos jugados.
    """

    # Factores por defecto para calcular finishing a partir del OVR según posición
    _FINISHING_FACTORS = {
        "GK": 0.15,
        "CB": 0.35,
        "FB": 0.55,
        "CDM": 0.50,
        "CM": 0.65,
        "CAM": 0.80,
        "WNG": 1.00,
        "ST": 1.25
    }

    def __init__(self, name: str, age: int, overall: int, position: str,
                 attack_rating: int = None, defense_rating: int = None,
                 finishing: int = None):

        self.name    = name
        self.age     = age
        self.overall = overall
        self.position = position

        # Si no se especifican, se derivan del OVR como aproximación razonable.
        # Garantiza retrocompatibilidad con equipos guardados sin estos atributos.
        self.attack_rating  = attack_rating  if attack_rating  is not None else int(overall * 0.9)
        self.defense_rating = defense_rating if defense_rating is not None else int(overall * 0.9)

        # finishing: capacidad de anotar goles (0-99).
        # Los delanteros goleadores tienen finishing alto; los creadores de juego lo tienen bajo.
        # Se usa en Match._pick_scorer para ponderar quién convierte los goles.
        if finishing is not None:
            self.finishing = finishing
        else:
            # Fallback: derivación razonable según posición
            self.finishing = self._default_finishing()

        # Estadísticas de temporada (inician en 0, se recuperan desde JSON)
        self.goals          = 0
        self.assists        = 0
        self.matches_played = 0

    # ------------------------------------------------------------------
    # Representación
    # ------------------------------------------------------------------

    def __str__(self):
        return (
            f"Player: {self.name} | Position: {self.position} | Age: {self.age} | "
            f"OVR: {self.overall} | ATK: {self.attack_rating} | DEF: {self.defense_rating} | "
            f"FIN: {self.finishing}"
        )

    # ------------------------------------------------------------------
    # Métodos de modificación
    # ------------------------------------------------------------------

    def increase_overall(self, amount: int):
        """Incrementa el OVR del jugador (útil para desarrollo de jóvenes)."""
        self.overall += amount

    # ------------------------------------------------------------------
    # Método interno para derivar finishing por defecto
    # ------------------------------------------------------------------

    def _default_finishing(self) -> int:
        """
        Deriva un valor de finishing razonable a partir del OVR y la posición.
        Se usa como fallback cuando no se especifica finishing explícitamente.
        """
        factor = self._FINISHING_FACTORS.get(self.position, 0.7)
        raw = int(self.overall * factor)
        return min(99, max(1, raw))

    # ------------------------------------------------------------------
    # Serialización / deserialización  →  persistencia en JSON
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Convierte el jugador a un diccionario serializable para teams.json."""
        return {
            "name":           self.name,
            "age":            self.age,
            "overall":        self.overall,
            "attack_rating":  self.attack_rating,
            "defense_rating": self.defense_rating,
            "finishing":      self.finishing,
            "goals":          self.goals,
            "assists":        self.assists,
            "matches_played": self.matches_played,
            "position":       self.position
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """
        Reconstruye un Player desde un diccionario leído de teams.json.
        Usa .get() con fallback para que equipos guardados antes del sprint
        sigan funcionando sin lanzar KeyError.
        """
        position       = data.get("position")
        defense_rating = data.get("defense_rating")

        # Corrige JSON con position y defense_rating intercambiados.
        if isinstance(defense_rating, str) and isinstance(position, (int, float)):
            position, defense_rating = defense_rating, int(position)

        player = cls(
            name           = data["name"],
            age            = data["age"],
            overall        = data["overall"],
            position       = position,
            attack_rating  = data.get("attack_rating"),   # None activa el fallback en __init__
            defense_rating = defense_rating,
            finishing      = data.get("finishing")        # None activa _default_finishing()
        )

        player.goals          = data.get("goals", 0)
        player.assists        = data.get("assists", 0)
        player.matches_played = data.get("matches_played", 0)

        return player