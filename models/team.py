from models.player import Player


class Team:
    """
    Representa un equipo de fútbol con su plantel completo.

    Responsabilidades de esta clase:
        - Almacenar la lista de jugadores.
        - Calcular métricas agregadas del plantel (OVR, ATK, DEF).
        - Serializar/deserializar desde JSON.

    Lo que NO hace esta clase (separación de responsabilidades):
        - No simula partidos  → responsabilidad de Match.
        - No gestiona la liga → responsabilidad de League.
        - No persiste en disco → responsabilidad de team_repository.
    """

    def __init__(self, name: str):
        self.name         = name
        self.players_list = []

    # ------------------------------------------------------------------
    # Representación
    # ------------------------------------------------------------------

    def __str__(self):
        return (
            f"{self.name} | "
            f"OVR: {self.calculate_overall():.1f} | "
            f"ATK: {self.calculate_attack():.1f} | "
            f"DEF: {self.calculate_defense():.1f} | "
            f"Jugadores: {len(self.players_list)}"
        )

    # ------------------------------------------------------------------
    # Gestión de plantel
    # ------------------------------------------------------------------

    def add_player(self, player: Player) -> bool:
        """
        Agrega un jugador al plantel.
        Retorna False si el jugador ya estaba en la lista.
        """
        if player not in self.players_list:
            self.players_list.append(player)
            return True
        return False

    def print_players(self):
        """Imprime todos los jugadores del plantel con sus atributos."""
        print(f"\n{self.name} — Plantel:\n")
        for player in self.players_list:
            print(player)

    # ------------------------------------------------------------------
    # Métricas del equipo
    # ------------------------------------------------------------------

    def _average_attribute(self, attribute: str) -> float:
        """
        Método privado: calcula el promedio de un atributo numérico
        sobre todos los jugadores del plantel.

        Usar un método interno evita repetir la misma lógica de promedio
        en calculate_overall, calculate_attack y calculate_defense.
        """
        if not self.players_list:
            return 0.0
        total = sum(getattr(player, attribute) for player in self.players_list)
        return total / len(self.players_list)

    def calculate_overall(self) -> float:
        """Retorna el OVR promedio del plantel."""
        return self._average_attribute("overall")

    def calculate_attack(self) -> float:
        """
        Retorna el promedio de attack_rating del plantel.
        Representa la capacidad ofensiva colectiva del equipo.
        """
        return self._average_attribute("attack_rating")

    def calculate_defense(self) -> float:
        """
        Retorna el promedio de defense_rating del plantel.
        Representa la solidez defensiva colectiva del equipo.
        """
        return self._average_attribute("defense_rating")

    # ------------------------------------------------------------------
    # Serialización / deserialización  →  persistencia en JSON
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Serializa el equipo completo (incluyendo plantel) a un diccionario."""
        return {
            "name":    self.name,
            "players": [player.to_dict() for player in self.players_list]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        """Reconstruye un Team (con su plantel) desde un diccionario de teams.json."""
        team = cls(data["name"])
        for player_data in data["players"]:
            team.add_player(Player.from_dict(player_data))
        return team
