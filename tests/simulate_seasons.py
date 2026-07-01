"""
Benchmark Monte Carlo del motor de simulación.

Ejecutar desde la raíz del proyecto:
    python tests/simulate_seasons.py
    python tests/simulate_seasons.py --runs 200
    python tests/simulate_seasons.py --format 2round_league
"""

from __future__ import annotations

import argparse
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from models.league import League  # noqa: E402
from models.match import Match  # noqa: E402
import services.team_repository as team_repo  # noqa: E402


@dataclass
class SeasonSnapshot:
    champion: str
    champion_pts: int
    champion_gf: int
    champion_gc: int
    last_place: str
    last_pts: int
    last_gf: int
    last_gc: int
    top_scorer: str
    top_scorer_team: str
    top_scorer_goals: int
    top_assister: str
    top_assister_team: str
    top_assister_count: int
    total_goals: int
    total_matches: int
    home_wins: int
    away_wins: int
    draws: int
    scoreless_draws: int
    high_scoring_matches: int  # 5+ goles totales
    blowouts: int              # diferencia >= 4
    top_5_scorers: list[tuple[str, str, int]] = field(default_factory=list)
    top_5_assisters: list[tuple[str, str, int]] = field(default_factory=list)


def _apply_match_result(league: League, match: Match) -> None:
    """Actualiza standings sin imprimir (misma lógica que League.simulate_round)."""
    home = league.standings[match.home_team]
    away = league.standings[match.away_team]

    home["pj"] += 1
    away["pj"] += 1

    home["gf"] += match.home_goals
    home["gc"] += match.away_goals
    away["gf"] += match.away_goals
    away["gc"] += match.home_goals

    if match.home_goals > match.away_goals:
        home["pts"] += 3
        home["g"] += 1
        away["p"] += 1
    elif match.home_goals < match.away_goals:
        away["pts"] += 3
        away["g"] += 1
        home["p"] += 1
    else:
        home["pts"] += 1
        away["pts"] += 1
        home["e"] += 1
        away["e"] += 1

    home["dg"] = home["gf"] - home["gc"]
    away["dg"] = away["gf"] - away["gc"]


def _sorted_standings(league: League) -> list[tuple]:
    return sorted(
        league.standings.items(),
        key=lambda item: (item[1]["pts"], item[1]["dg"], item[1]["gf"]),
        reverse=True,
    )


def run_season(fixture_format: str = "2round_league") -> SeasonSnapshot:
    """Simula una temporada completa sin salida a consola."""
    league = League("Benchmark")
    for team in team_repo.load_all_teams():
        league.add_team(team)

    league.generate_fixture(fixture_format)

    home_wins = away_wins = draws = 0
    scoreless_draws = high_scoring = blowouts = 0
    total_goals = 0
    total_matches = 0

    for round_matches in league.fixtures:
        for team1, team2 in round_matches:
            match = Match(team1, team2)
            match.simulate()
            _apply_match_result(league, match)

            hg, ag = match.home_goals, match.away_goals
            total_goals += hg + ag
            total_matches += 1

            if hg > ag:
                home_wins += 1
            elif ag > hg:
                away_wins += 1
            else:
                draws += 1
                if hg == 0:
                    scoreless_draws += 1

            if hg + ag >= 5:
                high_scoring += 1
            if abs(hg - ag) >= 4:
                blowouts += 1

    standings = _sorted_standings(league)
    champion, champ_stats = standings[0]
    last, last_place_team = standings[-1]

    # Procesar Goleadores
    all_players = league.get_all_players()
    scorers = sorted(all_players, key=lambda p: p.goals, reverse=True)
    top_goal = scorers[0]
    top_5_goal = [(p.name, _player_team_name(p, league), p.goals) for p in scorers[:5]]

    # Procesar Asistentes
    assisters = sorted(all_players, key=lambda p: p.assists, reverse=True)
    top_assist = assisters[0]
    top_5_assist = [(p.name, _player_team_name(p, league), p.assists) for p in assisters[:5]]

    return SeasonSnapshot(
        champion=champion.name,
        champion_pts=champ_stats["pts"],
        champion_gf=champ_stats["gf"],
        champion_gc=champ_stats["gc"],
        last_place=last.name,
        last_pts=last_place_team["pts"],
        last_gf=last_place_team["gf"],
        last_gc=last_place_team["gc"],
        top_scorer=top_goal.name,
        top_scorer_team=_player_team_name(top_goal, league),
        top_scorer_goals=top_goal.goals,
        top_assister=top_assist.name,
        top_assister_team=_player_team_name(top_assist, league),
        top_assister_count=top_assist.assists,
        total_goals=total_goals,
        total_matches=total_matches,
        home_wins=home_wins,
        away_wins=away_wins,
        draws=draws,
        scoreless_draws=scoreless_draws,
        high_scoring_matches=high_scoring,
        blowouts=blowouts,
        top_5_scorers=top_5_goal,
        top_5_assisters=top_5_assist,
    )


def _player_team_name(player, league: League) -> str:
    for team in league.teams_list:
        if player in team.players_list:
            return team.name
    return "?"


def _stats(values: list[float | int]) -> dict:
    if not values:
        return {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def _pct(part: int, total: int) -> float:
    return (100.0 * part / total) if total else 0.0


def _bar(label: str, count: int, total: int, width: int = 30) -> str:
    fill = int(width * count / total) if total else 0
    return f"  {label:<28} {count:>4} ({_pct(count, total):5.1f}%) {'#' * fill}"


def _format_stats_block(title: str, values: list[int]) -> list[str]:
    s = _stats(values)
    return [
        title,
        f"  Promedio : {s['mean']:.2f}",
        f"  Mediana  : {s['median']:.1f}",
        f"  Desv. est: {s['stdev']:.2f}",
        f"  Mín / Máx: {s['min']} / {s['max']}",
    ]


def run_benchmark(runs: int, fixture_format: str) -> None:
    snapshots: list[SeasonSnapshot] = []
    champion_counter: Counter = Counter()
    last_counter: Counter = Counter()
    
    pichichi_counter: Counter = Counter()
    pichichi_goals: defaultdict[str, list[int]] = defaultdict(list)
    player_goals_total: Counter = Counter()

    assist_king_counter: Counter = Counter()
    assist_king_counts: defaultdict[str, list[int]] = defaultdict(list)
    player_assists_total: Counter = Counter()

    team_champion_pts: defaultdict[str, list[int]] = defaultdict(list)

    for _ in range(runs):
        snap = run_season(fixture_format)
        snapshots.append(snap)

        champion_counter[snap.champion] += 1
        last_counter[snap.last_place] += 1
        
        pichichi_counter[snap.top_scorer] += 1
        pichichi_goals[snap.top_scorer].append(snap.top_scorer_goals)
        
        assist_king_counter[snap.top_assister] += 1
        assist_king_counts[snap.top_assister].append(snap.top_assister_count)

        team_champion_pts[snap.champion].append(snap.champion_pts)

        for name, _team, goals in snap.top_5_scorers:
            player_goals_total[name] += goals

        for name, _team, assists in snap.top_5_assisters:
            player_assists_total[name] += assists

    n = len(snapshots)
    teams_count = len(team_repo.load_all_teams())
    rounds = snapshots[0].total_matches * 2 // teams_count if snapshots else 0

    champ_pts = [s.champion_pts for s in snapshots]
    last_pts = [s.last_pts for s in snapshots]
    pichichi = [s.top_scorer_goals for s in snapshots]
    assists_leader = [s.top_assister_count for s in snapshots]
    gpg = [s.total_goals / s.total_matches for s in snapshots]
    season_goals = [s.total_goals for s in snapshots]

    total_match_count = sum(s.total_matches for s in snapshots)
    home_wins = sum(s.home_wins for s in snapshots)
    away_wins = sum(s.away_wins for s in snapshots)
    draws = sum(s.draws for s in snapshots)
    scoreless = sum(s.scoreless_draws for s in snapshots)
    high_scoring = sum(s.high_scoring_matches for s in snapshots)
    blowouts = sum(s.blowouts for s in snapshots)

    lines: list[str] = []
    sep = "=" * 72

    lines.append(sep)
    lines.append("  INFORME DE SIMULACION - FootballGM")
    lines.append(sep)
    lines.append("")
    lines.append("CONFIGURACION")
    lines.append(f"  Temporadas simuladas : {n}")
    lines.append(f"  Formato de fixture   : {fixture_format}")
    lines.append(f"  Equipos en liga      : {teams_count}")
    lines.append(f"  Fechas por temporada : {rounds}")
    lines.append(f"  Partidos / temporada : {snapshots[0].total_matches}")
    lines.append(f"  Motor                : Poisson (BASE={Match.BASE_RATE}, "
                 f"HOME_ADV={Match.HOME_ADVANTAGE})")
    lines.append("")

    lines.append(sep)
    lines.append("  1. PUNTOS — CAMPEÓN Y COLISTA")
    lines.append(sep)
    lines.extend(_format_stats_block("Campeón (PTS):", champ_pts))
    lines.append("")
    lines.extend(_format_stats_block("Colista (PTS):", last_pts))
    lines.append("")
    spread = [c - l for c, l in zip(champ_pts, last_pts)]
    lines.extend(_format_stats_block("Brecha campeon - colista:", spread))
    lines.append("")

    lines.append(sep)
    lines.append("  2. GOLES Y RENDIMIENTO GENERAL")
    lines.append(sep)
    lines.extend(_format_stats_block("Goles por partido (liga):", gpg))
    lines.append("")
    lines.extend(_format_stats_block("Goles totales / temporada:", season_goals))
    lines.append("")
    lines.extend(_format_stats_block("Pichichi — goles del líder:", pichichi))
    lines.append("")
    lines.extend(_format_stats_block("Líder de Asistencias — pases gol:", assists_leader))
    lines.append("")
    lines.append("Resultados de partido (todas las simulaciones):")
    lines.append(_bar("Victoria local", home_wins, total_match_count))
    lines.append(_bar("Victoria visita", away_wins, total_match_count))
    lines.append(_bar("Empates", draws, total_match_count))
    lines.append(_bar("Empates 0-0", scoreless, total_match_count))
    lines.append(_bar("Partidos 5+ goles", high_scoring, total_match_count))
    lines.append(_bar("Goleadas (dif >= 4)", blowouts, total_match_count))
    lines.append("")

    lines.append(sep)
    lines.append("  3. ¿QUIÉN GANA EL CAMPEONATO?")
    lines.append(sep)
    for team, count in champion_counter.most_common(10):
        avg_pts = statistics.mean(team_champion_pts[team])
        lines.append(
            f"  {team:<26} {count:>3} títulos ({_pct(count, n):5.1f}%)  "
            f"PTS al ganar: {avg_pts:.1f} prom."
        )
    lines.append("")

    lines.append(sep)
    lines.append("  4. ¿QUIÉN TERMINA ÚLTIMO?")
    lines.append(sep)
    for team, count in last_counter.most_common(10):
        lines.append(f"  {team:<26} {count:>3} veces ({_pct(count, n):5.1f}%)")
    lines.append("")

    lines.append(sep)
    lines.append("  5. LÍDERES INDIVIDUALES (PICHICHIS Y ASISTENCIAS)")
    lines.append(sep)
    lines.append("  Jugadores que más veces lideraron la tabla de goles:")
    for player, count in pichichi_counter.most_common(10):
        avg = statistics.mean(pichichi_goals[player])
        lines.append(
            f"  {player:<26} {count:>3} veces ({_pct(count, n):5.1f}%)  "
            f"{avg:.1f} goles prom. al liderar"
        )
    lines.append("")
    lines.append("  Jugadores que más veces lideraron en asistencias:")
    for player, count in assist_king_counter.most_common(10):
        avg = statistics.mean(assist_king_counts[player])
        lines.append(
            f"  {player:<26} {count:>3} veces ({_pct(count, n):5.1f}%)  "
            f"{avg:.1f} asist. prom. al liderar"
        )
    lines.append("")
    lines.append("  Acumulado de goles (top 5 por temporada sumados):")
    for player, total in player_goals_total.most_common(10):
        lines.append(f"  {player:<26} {total:>4} goles acumulados")
    lines.append("")
    lines.append("  Acumulado de asistencias (top 5 por temporada sumadas):")
    for player, total in player_assists_total.most_common(10):
        lines.append(f"  {player:<26} {total:>4} asistencias acumuladas")
    lines.append("")

    lines.append(sep)
    lines.append("  6. DIAGNOSTICO — SE COMPORTA CON NORMALIDAD?")
    lines.append(sep)

    alerts: list[str] = []
    ok: list[str] = []

    gpg_mean = statistics.mean(gpg)
    if 2.1 <= gpg_mean <= 3.1:
        ok.append(f"Goles/partido ({gpg_mean:.2f}) dentro de rango típico (~2.3–2.9).")
    else:
        alerts.append(f"Goles/partido ({gpg_mean:.2f}) fuera de rango esperado.")

    champ_mean = statistics.mean(champ_pts)
    max_possible = rounds * 3
    if champ_mean > max_possible * 0.85:
        alerts.append(f"Campeón promedia {champ_mean:.1f} pts. Dominancia excesiva.")
    elif champ_mean < rounds * 1.5:
        alerts.append(f"Campeón promedia solo {champ_mean:.1f} pts. Muy baja puntuación.")
    else:
        ok.append(f"Puntos del campeón ({champ_mean:.1f}) en rango razonable para {rounds} fechas.")

    home_pct = _pct(home_wins, total_match_count)
    if home_pct < 40 or home_pct > 53:
        alerts.append(f"Victorias locales ({home_pct:.1f}%) fuera de rango ideal (~42–48%).")
    else:
        ok.append(f"Ventaja local ({home_pct:.1f}% victorias) plausible.")

    scoreless_pct = _pct(scoreless, total_match_count)
    if scoreless_pct > 12:
        alerts.append(f"Demasiados 0-0 ({scoreless_pct:.1f}%).")
    elif scoreless_pct < 3:
        alerts.append(f"Muy pocos 0-0 ({scoreless_pct:.1f}%).")
    else:
        ok.append(f"Empates sin goles ({scoreless_pct:.1f}%) dentro de lo normal.")

    blowout_pct = _pct(blowouts, total_match_count)
    if blowout_pct > 7:
        alerts.append(f"Goleadas frecuentes ({blowout_pct:.1f}%).")
    else:
        ok.append(f"Goleadas ({blowout_pct:.1f}%) poco frecuentes — razonable.")

    if alerts:
        lines.append("  [!] ALERTAS:")
        for a in alerts:
            lines.append(f"    - {a}")
        lines.append("")
    if ok:
        lines.append("  [OK]:")
        for o in ok:
            lines.append(f"    - {o}")
    lines.append("")
    lines.append(sep)
    lines.append(f"  Fin del informe — {n} temporadas simuladas.")
    lines.append(sep)

    print("\n".join(lines))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Simula temporadas en silencio y genera un informe estadístico largo."
    )
    parser.add_argument(
        "--runs", type=int, default=200,
        help="Cantidad de temporadas a simular (default: 200)",
    )
    parser.add_argument(
        "--format", default="2round_league",
        choices=["1round_league", "2round_league"],
        help="Formato de fixture (default: 2round_league, torneo largo)",
    )
    args = parser.parse_args()
    run_benchmark(args.runs, args.format)


if __name__ == "__main__":
    main()