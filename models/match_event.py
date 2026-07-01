class MatchEvent:
    """
    Representa un evento atómico ocurrido durante un partido.

    Responsabilidad única: almacenar información de un hecho puntual
    (gol, tarjeta, lesión, cambio, etc.).

    No sabe simular, no modifica estadísticas, no conoce el marcador.
    Todo eso pertenece a Match, que es quien orquesta la simulación
    y va agregando eventos a una lista.

    Atributos:
        minute           Minuto del evento.
        team_name        Nombre del equipo involucrado (string, no el objeto Team completo).
        player           Jugador protagonista principal (referencia al objeto Player).
        event_type       Tipo de evento ("GOAL", "YELLOW_CARD", "RED_CARD", etc.).
        secondary_player Jugador secundario (asistente, jugador que entra en cambio, etc.).
    """

    def __init__(self, minute: int, team_name: str, player, event_type: str,
                 secondary_player=None):
        """
        Construye un MatchEvent.

        Recibe team_name (string) en lugar del objeto Team completo para
        evitar cargar todo el plantel cuando solo se necesita el nombre
        del equipo para representar el evento.

        player y secondary_player son referencias a objetos Player vivos,
        necesarias para que Match pueda actualizar estadísticas después
        de crear el evento.
        """
        self.minute = minute
        self.team_name = team_name
        self.player = player
        self.event_type = event_type
        self.secondary_player = secondary_player

    def __str__(self):
        """
        Devuelve una representación legible del evento.

        El formato cambia según el tipo de evento:

            Gol con asistencia:         14' ⚽ Eduardo Vargas (Charles Aránguiz)
            Gol sin asistencia:         14' ⚽ Eduardo Vargas
            Autogol:                    55' ⚽ (autogol) Marcelo Díaz
            Penal convertido:           23' ⚽ (p) Juan Ferney
            Penal fallado:              67' ❌ (p) Pablo Parra
            Tarjeta amarilla:           41' 🟨 Erick Pulgar
            Tarjeta roja:               78' 🟥 Gabriel Suazo
            Cambio:                     62' 🔁 Nicolás Guerra ↔ Eduardo Vargas
            Lesión:                     33' 🩹 Matías Zaldivia
        """
        match self.event_type:
            case "GOAL":
                if self.secondary_player:
                    return (f"{self.minute}' ⚽ {self.player.name} "
                            f"({self.secondary_player.name})")
                else:
                    return f"{self.minute}' ⚽ {self.player.name}"

            case "OWN_GOAL":
                return f"{self.minute}' ⚽ (autogol) {self.player.name}"

            case "PENALTY_SCORED":
                return f"{self.minute}' ⚽ (p) {self.player.name}"

            case "PENALTY_MISSED":
                return f"{self.minute}' ❌ (p) {self.player.name}"

            case "YELLOW_CARD":
                return f"{self.minute}' 🟨 {self.player.name}"

            case "RED_CARD":
                return f"{self.minute}' 🟥 {self.player.name}"

            case "SUBSTITUTION":
                if self.secondary_player:
                    return (f"{self.minute}' 🔁 {self.player.name} "
                            f"↔ {self.secondary_player.name}")
                else:
                    return f"{self.minute}' 🔁 {self.player.name}"

            case "INJURY":
                return f"{self.minute}' 🩹 {self.player.name}"

            case _:
                # Fallback para tipos de evento no contemplados explícitamente
                return (f"{self.minute}' {self.event_type} "
                        f"{self.player.name}")

    def to_dict(self) -> dict:
        """Serializa el evento a un diccionario para persistencia."""
        return {
            "minute": self.minute,
            "team_name": self.team_name,
            "player_name": self.player.name,
            "event_type": self.event_type,
            "secondary_player_name": (self.secondary_player.name
                                      if self.secondary_player else None)
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MatchEvent":
        """
        Reconstruye un MatchEvent desde un diccionario.

        NOTA: al reconstruir desde JSON, se pierden las referencias
        a los objetos Player (solo tenemos los nombres). Quien cargue
        el evento debe resolver los objetos Player por su nombre si
        los necesita.
        """
        # Creamos un evento con valores mínimos; el caller debe
        # reasignar player y secondary_player si tiene los objetos.
        event = cls(
            minute=data["minute"],
            team_name=data["team_name"],
            player=None,  # El caller debe resolver el objeto Player
            event_type=data["event_type"],
            secondary_player=None
        )
        return event