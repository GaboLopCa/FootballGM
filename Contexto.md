# FootballGM — Contexto del Proyecto

## Visión del producto

Construir un **Football Manager jugable desde el navegador**, inspirado en la filosofía de [Basketball GM](https://basketball-gm.com/): simulación profunda, decisiones de dirección deportiva y partidas que se resuelven en segundos, sin gráficos 3D ni microgestión en tiempo real.

**North Star:** el jugador elige un club, arma plantel y táctica, avanza fecha a fecha y compite por el campeonato — todo desde una interfaz web, con partidas simuladas por un motor estadístico creíble.

**Alcance inicial:** Campeonato Nacional de Chile (16 equipos, planteles reales aproximados en `data/teams.json`).

> **Convención:** las ideas de diseño y desarrollo que surjan en conversaciones se documentan en este archivo. Es la hoja de ruta y carta de presentación del proyecto.

---

## Estado actual (resumen ejecutivo)

| Área | Estado |
|------|--------|
| Modelo de dominio (POO) | ✅ Implementado |
| Persistencia de planteles (JSON) | ✅ Implementado |
| Motor de partido (Poisson) | ✅ Implementado |
| Liga: fixture ida/vuelta + tabla + goleadores | ✅ Implementado |
| Interfaz de juego | ⚠️ Solo consola (`main.py`) |
| Rol de manager (decisiones del usuario) | ❌ No existe |
| Guardado de temporada en curso | ❌ No existe |
| Web / API | ❌ No iniciado |

El núcleo de simulación **ya funciona**. El gap principal hacia el producto final es la **capa de juego** (manager + persistencia de partida) y la **capa web** (API + frontend).

---

## Arquitectura del código

Separación estricta de responsabilidades. La lógica de negocio vive en `models/` y no debe depender de consola, JSON ni HTTP.

```
models/
  player.py    → Jugador: OVR, posición, attack_rating, defense_rating, finishing, stats de temporada
  team.py      → Plantel y métricas agregadas (OVR, ATK, DEF)
  match.py     → Motor probabilístico de un partido
  league.py    → Fixture, jornadas, tabla, goleadores

services/
  team_repository.py → Carga/guarda planteles en data/teams.json

main.py        → Demo en consola: simula una temporada completa
sandbox.py     → Script de seed: crea/actualiza equipos en JSON
data/
  teams.json   → 16 equipos chilenos con ~11 jugadores c/u
```

**Principio rector:** todo lo que se simule hoy en consola debe poder exponerse mañana vía API sin reescribir el dominio.

---

## Motor de simulación

Modelo inspirado en **Dixon-Coles / Poisson** (versión simplificada):

1. **Tasas de gol esperadas (λ):**
   - `λ_home = BASE_RATE (1.35) × (ATK_home / DEF_away) × HOME_ADVANTAGE (1.12)`
   - `λ_away = BASE_RATE (1.35) × (ATK_away / DEF_home)`
   - λ se clampea entre 0.2 y 4.0 para evitar resultados absurdos.

2. **Goles:** muestreo Poisson con algoritmo de Knuth.

3. **Goleadores y asistentes:** `random.choices()` con pesos distintos por rol (ver sección *Attack vs Finishing*).

4. **Stats persistidas por jugador:** `goals`, `assists`, `matches_played` (asistencias pendientes de implementar).

---

## Diseño de jugadores — Attack vs Finishing

**Idea de diseño (jun 2026):** separar la capacidad ofensiva en dos atributos independientes. Hoy `attack_rating` mezcla creación de juego y definición; eso produce perfiles poco realistas (un enganche y un 9 pueden tener el mismo peso goleador).

| Atributo | Nombre en código | Qué representa | Uso en simulación |
|----------|------------------|----------------|-------------------|
| **Creación / peligro** | `attack_rating` | Cuánto daño genera al rival: pases filtrados, llegada al área, volumen ofensivo | Promedio del equipo → λ (goles esperados). Peso al elegir **asistente**. |
| **Definición** | `finishing` *(nuevo)* | Capacidad de concretar: remate, cabeceo, definición en el área | Peso al elegir **goleador**. No altera cuántos goles hay, solo **quién** marca. |

**Ejemplos de perfil:**

- **Mediapunta (CAM)** — alto `attack_rating`, bajo `finishing`: filtra pases, asiste mucho, golea poco.
- **Delantero centro (ST)** — alto `finishing`, `attack_rating` moderado: convierte las ocasiones, asiste poco.
- **Extremo (WNG)** — puede tener ambos altos (cortador + definidor) o perfil asistidor según jugador real.

**Flujo por gol (Sprint 3):**

```
1. λ define cuántos goles marca el equipo (Poisson).
2. Goleador  → random.choices(pesos = finishing × factor_posición_gol)
3. Asistente → random.choices(pesos = attack_rating × factor_posición_asistencia)
               (excluir al goleador; ~20–30% de goles sin asistencia)
```

**Defaults por posición** (multiplicadores sobre OVR al crear/migrar jugadores):

| Posición | Attack (crear) | Finishing |
|----------|----------------|-----------|
| GK | bajo (0.90 × OVR) | muy bajo (0.15 × OVR) |
| CB | medio-alto (0.90 × OVR) | muy bajo (0.35 × OVR) |
| FB | medio (0.90 × OVR) | bajo (0.55 × OVR) |
| CDM | alto (0.90 × OVR) | bajo (0.50 × OVR) |
| CM | alto (0.90 × OVR) | medio (0.65 × OVR) |
| CAM | alto (0.90 × OVR) | medio-alto (0.80 × OVR) |
| WNG | alto (0.90 × OVR) | alto (1.00 × OVR) |
| ST | bajo (0.90 × OVR)* | muy alto (1.20–1.25 × OVR) |

*\*El `attack_rating` heredado de teams.json ya estaba bajo para ST (~33 avg) y alto para CAM/CM (~68 avg), coherente con la nueva semántica.*

**Migración desde `teams.json`:** se ejecutó script `migrate_add_finishing.py` que agregó `finishing` a los 176 jugadores usando los factores de posición sobre OVR. Backup automático creado como `teams.json.bak`.

**Impacto en UI futura:** en la ficha del jugador se verán arquetipos claros (creador vs goleador), útil para fichajes y alineación en el Football Manager web.

---

## Roadmap por sprints

Organizado de menor a mayor valor de producto. Cada sprint tiene **entregable demo-able** y criterio de cierre claro.

---

### ✅ Sprint 0 — Fundamentos *(completado)*

**Objetivo:** dominio sólido y datos persistentes.

- [x] Clases `Player`, `Team`, `Match`, `League`
- [x] Serialización JSON (`to_dict` / `from_dict`)
- [x] Repositorio de equipos
- [x] Plantel del Campeonato Nacional en `teams.json`

---

### ✅ Sprint 1 — Simulación de partido *(completado)*

**Objetivo:** resultados creíbles y atribución de goles.

- [x] Modelo Poisson con ventaja de local
- [x] Selección de goleador por posición y ATK
- [x] Registro de `matches_played` y `goals`

---

### ✅ Sprint 2 — Temporada en liga *(completado)*

**Objetivo:** loop competitivo completo en consola.

- [x] Fixture ida y vuelta (Round Robin)
- [x] Tabla de posiciones con desempate (pts → DG → GF)
- [x] Ranking de goleadores
- [x] Tabla formateada en consola

---

### 🔄 Sprint 3 — Calidad del motor *(en curso, ~70%)*

**Objetivo:** confiar en los números antes de construir encima.

| Tarea | Prioridad | Estado |
|-------|-----------|--------|
| Separar `attack_rating` (creación/λ) y `finishing` (goles) en `Player` | Alta | ✅ |
| Migrar `teams.json` con `finishing` por posición (176 jugadores) | Alta | ✅ |
| Goleadores por `finishing`, asistentes por `attack_rating` en `Match` | Alta | ✅ |
| Balancear λ (goleadas, empates 0-0, promedios de goles/liga) | Alta | ⚠️ Parcial (BASE=1.15, HOME_ADV=1.16, ~2.73 gpp) |
| Tests de regresión del motor (`tests/simulate_seasons.py`) | Media | ✅ (100 temporadas OK) |
| Reporte de partido enriquecido (marcador + goleadores + asistentes + λ) | Baja | ❌ Pendiente |

**Verificación:** 100 temporadas simuladas — todos los diagnósticos OK. Distribución coherente:
- Goleadores: ST dominan (Eduardo Vargas 21% pichichis, Lionel Altamirano 16%)
- Asistentes: CAM/CM dominan (Matías Palavecino 12%, Arturo Vidal 5%)
- Goles/partido: 2.73 (rango óptimo) | Victorias local: 42.0% | Empates 0-0: 6.4% | Goleadas: 4.0%

**Criterio de cierre:** ✅ simular 100 temporadas con distribución de goles/asistencias coherente por posición (CAM asiste más que ST; ST golea más que CAM).

---

### 📋 Sprint 4 — Capa de juego (Manager Mode v0)

**Objetivo:** dejar de ser un simulador automático y convertirse en un juego.

| Tarea | Prioridad |
|-------|-----------|
| Clase `Game` / `SaveGame`: estado de temporada (fecha, tabla, stats) | Alta |
| Elegir equipo a dirigir al iniciar partida | Alta |
| Simular solo la fecha del usuario (no toda la liga de golpe) | Alta |
| Persistir partida en `data/saves/` (JSON) | Alta |
| Alineación titular (11 jugadores) que afecte ATK/DEF del partido | Media |

**Criterio de cierre:** iniciar partida → jugar 5 fechas → cerrar → reabrir → continuar desde la misma fecha con tabla y stats intactas.

---

### 📋 Sprint 5 — API REST

**Objetivo:** desacoplar la lógica del frontend.

| Tarea | Prioridad |
|-------|-----------|
| FastAPI (recomendado) o Flask como capa delgada sobre `models/` | Alta |
| Endpoints: equipos, plantel, fixture, simular jornada, tabla, goleadores | Alta |
| Endpoints de save/load de partida | Alta |
| CORS habilitado para desarrollo local | Media |

**Criterio de cierre:** el flujo completo de Sprint 4 ejecutable solo con llamadas HTTP (Postman o frontend mínimo).

---

### 📋 Sprint 6 — Frontend web (MVP jugable)

**Objetivo:** primera versión usable en el navegador.

| Pantalla | Contenido |
|----------|-----------|
| Inicio | Nueva partida / continuar / elegir equipo |
| Dashboard | Próximo rival, posición en tabla, últimos resultados |
| Plantel | Lista de jugadores con OVR, posición, stats |
| Fecha | Resultados de la jornada + botón "Simular" |
| Clasificación | Tabla ordenada |
| Goleadores | Top 10 |

**Stack sugerido:** React + Vite (o SvelteKit). Estilos simples; priorizar datos y flujo sobre diseño.

**Criterio de cierre:** jugar una mini-temporada (3–5 fechas) 100% desde el navegador.

---

### 📋 Sprint 7 — Profundidad de manager

**Objetivo:** decisiones que cambien el resultado.

- Fichajes y ventas (mercado simplificado)
- Presupuesto / salarios
- Desarrollo y envejecimiento de jugadores
- Táctica básica (formación, estilo) que modifique λ o pesos de goleador
- Lesiones / rotación (opcional)

**Criterio de cierre:** una decisión de fichaje o táctica produce efecto medible en la simulación.

---

### 📋 Sprint 8 — Producto publicable

**Objetivo:** deploy y experiencia de usuario pulida.

- Autenticación opcional (cuentas + saves en nube)
- Deploy backend (Railway, Render, Fly.io) + frontend (Vercel, Netlify)
- Tutorial in-game / onboarding
- Balance final y datos actualizados por temporada

**Criterio de cierre:** URL pública donde cualquier persona puede crear una partida y jugar.

---

## Próximos pasos inmediatos (esta semana)

1. ✅ **Sprint 3:** añadir `finishing` a `Player` y migrar planteles en JSON. *(Completado)*
2. ✅ **Sprint 3:** goleadores por `finishing`, asistentes por `attack_rating`. *(Completado)*
3. ✅ **Sprint 3:** verificar con 100 temporadas Monte Carlo. *(Completado, todos OK)*
4. **Sprint 3 (restante):** balancear λ con simulaciones masivas.
5. **Sprint 4 (prep):** diseñar esquema JSON de `SaveGame`.
6. **Deuda técnica:** alinear `sandbox.py` con la firma actual de `Player(...)`.

---

## Decisiones de arquitectura (fijadas)

| Decisión | Elección | Motivo |
|----------|----------|--------|
| Lenguaje del motor | Python 3 | Rápido de iterar, suficiente para simulación |
| Persistencia inicial | JSON | Simple, legible, sin DB en MVP |
| Motor de partido | Poisson + ratings | Escalable; no requiere simular 90 minutos |
| Frontend objetivo | SPA en navegador | Alineado con Basketball GM |
| Separación dominio / I/O | Estricta | Permite consola hoy, web mañana |

---

## Referencia rápida — archivos clave

| Archivo | Para qué sirve |
|---------|----------------|
| `main.py` | Demo: temporada completa en consola |
| `models/match.py` | Motor de simulación (λ, Poisson, goleadores) |
| `models/league.py` | Fixture, jornadas, tabla, goleadores |
| `data/teams.json` | Base de datos de planteles (16 equipos) |
| `services/team_repository.py` | CRUD de equipos en disco |
| `tests/simulate_seasons.py` | Benchmark Monte Carlo: N temporadas silenciosas + informe estadístico |

---

*Última actualización: 17 jun 2026 — Sprint 3 ~70%. Attack/finishing separados en Player, goleadores por finishing, asistentes por attack_rating. 100 temporadas verificadas OK. Próximo: balancear λ, luego Sprint 4 (Manager Mode).*
