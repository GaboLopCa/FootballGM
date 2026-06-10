from models.player import Player
from models.team import Team
from models.league import League
import services.team_repository as team_repo

# Cargar selecciones desde JSON
portugal = team_repo.load_team("Portugal")
colombia = team_repo.load_team("Colombia")
uzbekistan = team_repo.load_team("Uzbekistan")
rd_congo = team_repo.load_team("RD Congo")

# Crear grupo
grupo_k = League("Grupo K - Mundial 2026")

grupo_k.add_team(portugal)
grupo_k.add_team(colombia)
grupo_k.add_team(uzbekistan)
grupo_k.add_team(rd_congo)

# Mostrar equipos cargados
print(portugal)
print(colombia)
print(uzbekistan)
print(rd_congo)

print("\n=== SORTEO COMPLETADO ===\n")

# Generar fase de grupos ida
grupo_k.generate_fixture("1round_league")

# Simular fecha a fecha
for fecha in range(3):

    print(f"\n========== FECHA {fecha + 1} ==========\n")

    grupo_k.simulate_round()

    print("\nTABLA DE POSICIONES\n")
    grupo_k.show_standings()

    input("\nPresione Enter para continuar...")

print("\n========== FASE DE GRUPOS FINALIZADA ==========\n")

grupo_k.show_standings()