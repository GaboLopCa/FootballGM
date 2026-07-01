from models.league import League
import services.team_repository as team_repo

# Crear liga
liga_chilena = League("Campeonato Nacional")

# Cargar todos los equipos guardados
equipos = team_repo.load_all_teams()

# Agregar equipos a la liga
for equipo in equipos:
    liga_chilena.add_team(equipo)

# Mostrar equipos participantes
print("=== EQUIPOS PARTICIPANTES ===\n")

for equipo in liga_chilena.teams_list:
    print(equipo)

print("\n=== SORTEO COMPLETADO ===\n")

# Generar calendario ida y vuelta
liga_chilena.generate_fixture("2round_league")

# Simular temporada
for fecha in range(len(liga_chilena.fixtures)):

    print(f"\n========== FECHA {fecha + 1} ==========\n")

    liga_chilena.simulate_round()

    print("\nTABLA DE POSICIONES\n")
    liga_chilena.show_standings()

    input("\nPresione Enter para continuar...")

print("\n========== CAMPEONATO FINALIZADO ==========\n")

liga_chilena.show_standings()

# Campeón
campeon = liga_chilena.get_champion()

print(f"\n🏆 CAMPEÓN: {campeon.name}")

liga_chilena.show_top_scorers()