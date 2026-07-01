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
| Tests unitarios por modelo | ❌ No iniciado |
| Economía (presupuesto, salarios, fichajes) | ❌ No iniciado |

El núcleo de simulación **ya funciona**. El gap principal hacia el producto final es la **capa de juego** (manager + persistencia de partida) y la **capa web** (API + frontend).

---

## Arquitectura del código

Separación estricta de responsabilidades. La lógica de negocio vive en `models/` y no debe depender de consola, JSON ni HTTP.

```
FootballGM/
├── models/
│   ├── player.py       → Jugador: OVR, posición, attack_rating, defense_rating, finishing, stats de temporada
│   ├── team.py         → Plantel y métricas agregadas (OVR, ATK, DEF)
│   ├── match.py        → Motor probabilístico de un partido (orquesta la simulación y acumula eventos)
│   ├── match_event.py  → Evento atómico del partido (gol, tarjeta, lesión, cambio, etc.)
│   └── league.py       → Fixture, jornadas, tabla, goleadores
│
├── services/
│   ├── team_repository.py → Carga/guarda planteles en data/teams.json
│   ├── team_ratings.py    → Cálculos de ataque, defensa, mediocampo, pressing, etc. (futuro)
│   ├── match_engine.py    → Orquestador de simulación de partido (futuro)
│   ├── league_scheduler.py → Generación de fixture (futuro)
│   ├── transfer_market.py  → Lógica de fichajes (futuro)
│   └── finance_engine.py   → Presupuestos, salarios, premios (futuro)
│
├── utils/            → Utilidades transversales (formateo, constantes, helpers) (futuro)
├── config/           → Configuración del juego (constantes de simulación, defaults) (futuro)
├── data/
│   ├── teams.json    → 16 equipos chilenos con ~11 jugadores c/u
│   └── saves/        → Partidas guardadas (futuro)
│
├── tests/
│   ├── test_player.py   → Tests unitarios de Player (futuro)
│   ├── test_team.py     → Tests unitarios de Team (futuro)
│   ├── test_match.py    → Tests unitarios de Match (futuro)
│   ├── test_league.py   → Tests unitarios de League (futuro)
│   └── simulate_seasons.py → Benchmark Monte Carlo (actual)
│
├── main.py           → Demo en consola: simula una temporada completa
└── sandbox.py        → Script de seed: crea/actualiza equipos en JSON
```

**Principio rector:** los modelos (`models/`) solo contienen datos y lógica de negocio pura. Los servicios (`services/`) contienen algoritmos y operaciones. Los modelos no deben depender de consola, JSON ni HTTP.

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

## Roadmap por etapas

El desarrollo se organiza en **5 etapas progresivas**. Cada etapa es un hito vertical: al terminarla, el proyecto es funcional y testeable en ese nivel. No se avanza a la siguiente hasta que la anterior está completa y testeada.

```
ETAPA 1 ─── Motor de simulación (actual)
  │
  ▼
ETAPA 2 ─── Economía (presupuesto, fichajes, contratos)
  │
  ▼
ETAPA 3 ─── Manager (formación, titulares, cambios, cantera)
  │
  ▼
ETAPA 4 ─── Interfaz web (React + TypeScript)
  │
  ▼
ETAPA 5 ─── Online (usuarios, cuentas, multiplayer, cloud)
```

---

### 🔷 ETAPA 1 — Motor de simulación *(actual, ~70%)*

**Objetivo:** una temporada completa puede simularse automáticamente desde consola con estadísticas individuales, tabla de posiciones, goleadores, asistentes, tarjetas, lesiones y campeón.

**Principio:** no importa si todo es por consola. Lo importante es que el motor funcione.

#### ✅ Sprint 0 — Fundamentos *(completado)*

- [x] Clases `Player`, `Team`, `Match`, `League`
- [x] Serialización JSON (`to_dict` / `from_dict`)
- [x] Repositorio de equipos
- [x] Plantel del Campeonato Nacional en `teams.json`

#### ✅ Sprint 1 — Simulación de partido *(completado)*

- [x] Modelo Poisson con ventaja de local
- [x] Selección de goleador por posición y ATK
- [x] Registro de `matches_played` y `goals`

#### ✅ Sprint 2 — Temporada en liga *(completado)*

- [x] Fixture ida y vuelta (Round Robin)
- [x] Tabla de posiciones con desempate (pts → DG → GF)
- [x] Ranking de goleadores
- [x] Tabla formateada en consola

#### 🔄 Sprint 3 — Calidad y profundidad del motor *(~50%)*

| Tarea | Prioridad | Estado |
|-------|-----------|--------|
| Separar `attack_rating` (creación/λ) y `finishing` (goles) en `Player` | Alta | ✅ |
| Migrar `teams.json` con `finishing` por posición (176 jugadores) | Alta | ✅ |
| Goleadores por `finishing`, asistentes por `attack_rating` en `Match` | Alta | ✅ |
| Balancear λ (goleadas, empates 0-0, promedios de goles/liga) | Alta | ⚠️ Parcial (BASE=1.15, HOME_ADV=1.16, ~2.73 gpp) |
| Tests de regresión del motor (`tests/simulate_seasons.py`) | Media | ✅ (100 temporadas OK) |
| Reporte de partido enriquecido (marcador + goleadores + asistentes + λ) | Baja | ❌ Pendiente |
| Alinear `sandbox.py` con la firma actual de `Player(...)` | Baja | ❌ Pendiente |

#### 📋 Sprint 4 — Estadísticas y eventos del partido

| Tarea | Prioridad | Estado |
|-------|-----------|--------|
| Clase `MatchEvent`: evento atómico (gol, tarjeta, lesión, cambio, etc.) | Alta | ✅ |
| Integrar `MatchEvent` en `Match.simulate()` reemplazando `self.scorers` | Alta | ✅ |
| `Match._random_minute()`: generar minuto con sesgo a segunda mitad | Alta | ✅ |
| `Match.detailed_result()`: reporte usando `MatchEvent.__str__()` | Alta | ✅ |
| Asistencias: registrar y persistir en stats de jugador | Alta | ✅ (desde Sprint 3) |
| Tarjetas amarillas y rojas (probabilidad por posición y atributos) | Alta | ❌ Pendiente |
| Lesiones durante el partido (probabilidad, duración, impacto en atributos) | Media | ❌ Pendiente |
| Suspensiones por acumulación de tarjetas | Media | ❌ Pendiente |
| Estadísticas individuales completas: minutos, goles, asistencias, tarjetas, lesiones | Alta | ❌ Pendiente |
| Reporte de partido completo (marcador, goles, asistentes, tarjetas, lesiones, λ) | Media | ❌ Pendiente |

#### 📋 Sprint 5 — Tests unitarios del motor

| Tarea | Prioridad |
|-------|-----------|
| `tests/test_player.py` — creación, serialización, actualización de stats | Alta |
| `tests/test_team.py` — cálculo de OVR, ATK, DEF, plantel | Alta |
| `tests/test_match.py` — simulación, distribución de goles, goleadores, asistentes | Alta |
| `tests/test_league.py` — fixture, tabla, desempates, goleadores | Alta |
| Tests de borde: equipos con 0 jugadores, λ extremos, fixture incompleto | Media |

**Criterio de cierre de ETAPA 1:** ✅ simular una temporada completa desde consola con goles, asistencias, tarjetas, lesiones, tabla de posiciones, goleadores y campeón. Todos los tests unitarios pasan. El motor es confiable y predecible.

---

### 🔷 ETAPA 2 — Economía *(siguiente)*

**Objetivo:** el juego tiene un sistema económico que gobierna fichajes, salarios, presupuestos y scouting. Todo esto depende completamente de que la simulación (ETAPA 1) ya exista.

#### 📋 Sprint 6 — Presupuesto y finanzas

| Tarea | Prioridad |
|-------|-----------|
| Presupuesto inicial por equipo (basado en rendimiento histórico) | Alta |
| Ingresos por rendimiento (premios por posición en tabla) | Alta |
| Gastos operativos (salarios del plantel) | Alta |
| Estado de resultados del club por temporada | Media |

#### 📋 Sprint 7 — Fichajes y contratos

| Tarea | Prioridad |
|-------|-----------|
| Valor de mercado de jugadores (basado en OVR, edad, rendimiento) | Alta |
| Sistema de fichajes: oferta, negociación, transferencia | Alta |
| Contratos: duración, salario, cláusula de salida | Alta |
| Agentes libres y fin de contrato | Media |
| Scouting básico: generar jugadores jóvenes con potencial aleatorio | Media |

**Criterio de cierre de ETAPA 2:** ✅ se puede comprar y vender jugadores. El presupuesto del club se actualiza. Los fichajes impactan en el rendimiento del equipo en la simulación.

---

### 🔷 ETAPA 3 — Manager *(posterior)*

**Objetivo:** FootballGM deja de ser una simulación automática y se convierte en un juego donde el usuario toma decisiones que afectan los resultados.

#### 📋 Sprint 8 — Formación y alineación

| Tarea | Prioridad |
|-------|-----------|
| Elegir formación (4-4-2, 4-3-3, 3-5-2, etc.) que afecte ATK/DEF | Alta |
| Seleccionar 11 titulares desde el plantel | Alta |
| Suplentes y cambios durante el partido | Alta |
| Rotación de plantel y fatiga | Media |

#### 📋 Sprint 9 — Decisiones de manager

| Tarea | Prioridad |
|-------|-----------|
| Instrucciones tácticas (presión alta, contraataque, posesión) que modifiquen λ | Alta |
| Objetivos del club por temporada (pelear campeonato, mantener categoría, etc.) | Alta |
| Cantera: juveniles que suben al primer equipo | Media |
| Moral y confianza del plantel (impacto en rendimiento) | Media |

**Criterio de cierre de ETAPA 3:** ✅ una decisión táctica del usuario (formación, titulares, instrucciones) produce un efecto medible en la simulación del partido.

---

### 🔷 ETAPA 4 — Interfaz web *(posterior)*

**Objetivo:** migrar la experiencia a web. No antes, porque cambiar de consola a React no cambia el motor. Simplemente cambia cómo se muestran los datos. Si se hace antes, se terminará corrigiendo bugs del simulador mientras se pelea con CSS, componentes, rutas y estados.

#### 📋 Sprint 10 — API REST con FastAPI

| Tarea | Prioridad |
|-------|-----------|
| FastAPI como capa delgada sobre `models/` y `services/` | Alta |
| `GET /api/teams` — lista de equipos | Alta |
| `GET /api/teams/{id}/players` — plantel de un equipo | Alta |
| `GET /api/league/standings` — tabla de posiciones | Alta |
| `GET /api/league/fixture` — fixture completo o jornada actual | Alta |
| `GET /api/league/top-scorers` — ranking de goleadores | Alta |
| `POST /api/save/new` — crear nueva partida (elige equipo) | Alta |
| `GET /api/save/{id}` — estado de la partida | Alta |
| `POST /api/save/{id}/simulate-round` — simular la siguiente jornada | Alta |
| `POST /api/save/{id}/lineup` — establecer alineación titular | Media |
| CORS habilitado para desarrollo local | Media |

**Criterio de cierre:** el flujo completo de ETAPA 3 ejecutable solo con llamadas HTTP (Postman o curl).

#### 📋 Sprint 11 — Frontend React + TypeScript (MVP jugable)

| Pantalla | Contenido |
|----------|-----------|
| Inicio | Nueva partida / continuar / elegir equipo |
| Dashboard | Próximo rival, posición en tabla, últimos resultados |
| Plantel | Lista de jugadores con OVR, posición, stats de temporada |
| Fecha | Resultados de la jornada + botón "Simular" |
| Clasificación | Tabla ordenada completa |
| Goleadores | Top 10 de la liga |

**Stack:** React + Vite + TypeScript. Estilos simples (CSS modules o Tailwind básico). Priorizar datos y flujo sobre diseño.

**Criterio de cierre:** jugar una mini-temporada (3–5 fechas) 100% desde el navegador.

#### 📋 Sprint 12 — Profundidad de interfaz

| Tarea | Prioridad |
|-------|-----------|
| Pantalla de formación y alineación (drag & drop o selección) | Alta |
| Pantalla de fichajes (mercado, ofertas, negociación) | Alta |
| Pantalla de finanzas del club | Media |
| Reporte de partido enriquecido en web | Media |
| Perfil de jugador con stats detalladas | Media |

**Criterio de cierre:** todas las decisiones de ETAPA 3 se pueden tomar desde la interfaz web.

---

### 🔷 ETAPA 5 — Online *(futuro)*

**Objetivo:** FootballGM como servicio con cuentas, persistencia en nube y funcionalidades sociales.

#### 📋 Sprint 13 — Usuarios y persistencia cloud

| Tarea | Prioridad |
|-------|-----------|
| Autenticación (registro, login, sesiones) | Alta |
| Guardar partidas en nube (asociadas a cuenta) | Alta |
| Cargar partida desde cualquier dispositivo | Alta |
| Rankings globales de managers | Media |

#### 📋 Sprint 14 — Multiplayer y comunidad

| Tarea | Prioridad |
|-------|-----------|
| Ligas multijugador (cada manager controla un equipo) | Alta |
| Mercado de fichajes compartido entre jugadores | Alta |
| Chat / notificaciones in-game | Media |
| Temporadas online con histórico | Media |

**Criterio de cierre de ETAPA 5:** URL pública donde cualquier persona puede crear una cuenta, iniciar una partida y jugar. Los datos persisten entre sesiones.

---

## MatchEvent — eventos atómicos del partido

**Archivo:** `models/match_event.py`

**Responsabilidad:** representar un evento atómico ocurrido durante un partido. No sabe simular, no modifica estadísticas, no conoce el marcador. Solo almacena información de un hecho puntual.

`Match` es el director de la orquesta: simula, crea eventos y los acumula en una lista. Al finalizar, el partido completo puede reconstruirse únicamente leyendo la secuencia de eventos (el marcador, los goleadores, las tarjetas, etc. se derivan de ahí).

### Atributos

```
minute: int                       → Minuto del evento.
team: Team                        → Equipo involucrado.
player: Player                    → Protagonista principal.
event_type: str                   → Tipo de evento ("GOAL", "YELLOW_CARD", "RED_CARD", "SUBSTITUTION", "INJURY", "PENALTY_SCORED", "PENALTY_MISSED", "OWN_GOAL", etc.).
secondary_player: Player | None   → Jugador secundario (asistente, jugador que entra en un cambio, etc.).
```

### Métodos

- `__init__(minute, team, player, event_type, secondary_player=None)` — construye el evento.
- `__str__()` — representación bonita para consola:
  ```
  14' ⚽ Eduardo Vargas
  14' ⚽ Eduardo Vargas (Charles Aránguiz)
  62' 🟨 Marcelo Díaz
  81' 🔁 Nicolás Guerra ↔ Eduardo Vargas
  ```
- `to_dict()` — serialización opcional para guardar partidos.
- `from_dict()` — deserialización opcional desde JSON.

### Lo que NO hace

❌ Aumentar goles, sumar asistencias, modificar estadísticas, decidir quién hizo el gol, calcular probabilidades ni conocer el marcador. Todo eso pertenece a `Match`.

### Flujo de uso

```
Match.simulate()
  │
  ▼
elige goleador
  │
  ▼
crea MatchEvent(event_type="GOAL", ...)
  │
  ▼
events.append(event)
  │
  ▼
actualiza estadísticas del jugador
  │
  ▼
continúa simulación
```

Al finalizar:

```
Match
├── home_team
├── away_team
├── score
└── events
      ├── GOAL
      ├── GOAL
      ├── YELLOW
      ├── GOAL
      └── RED
```

---

## Sobre la IA del partido (visión a futuro)

El motor actual usa Poisson puro, que es simple y funciona. Pero el objetivo a largo plazo es un enfoque más granular, similar a Football Manager:

```
Inicio
  │
  ▼
Comparar mediocampo (midfield_rating local vs visitante)
  │
  ▼
Comparar posesión (possession_rating)
  │
  ▼
Generar ocasiones de gol (creativity_rating vs defensive_rating)
  │
  ▼
Comparar ataque vs defensa (attack_rating vs defense_rating)
  │
  ▼
Determinar probabilidad de gol (finishing vs goalkeeper_rating)
  │
  ▼
Actualizar estadísticas del partido
  │
  ▼
Avanzar al siguiente minuto / evento
```

Este enfoque escala mucho mejor porque:
- Permite agregar nuevas fases (pressing, contraataques, balón parado) sin reescribir el motor.
- Genera estadísticas más ricas (posesión, tiros, ocasiones) que alimentan la UI.
- Es más fácil de balancear porque cada fase tiene su propia constante.

**No se implementa ahora.** Se implementará cuando el motor actual esté completo y testeado (ETAPA 1), y servirá como reemplazo del algoritmo Poisson manteniendo la misma interfaz.

---

## Módulo de predicción (GoalStrength / Dixon-Coles)

**Inspirado en:** [Oloraculo](https://github.com/jorgezapeda/Oloraculo) — proyecto open source de predicción de fútbol en C#.

### ¿Qué es?

Un sistema predictivo que, a partir de resultados históricos, calcula la **fuerza real de ataque** y **vulnerabilidad defensiva** de cada equipo, ajustada por el rival. No es un promedio simple; es un modelo iterativo que descubre cuánto mejor o peor es cada equipo respecto a la media de la liga.

### ¿Cuándo implementarlo?

**Después de ETAPA 1**, cuando el simulador haya generado datos históricos suficientes (múltiples temporadas con goles, asistencias, resultados). El orden recomendado es:

1. ✅ Completar ETAPA 1 (motor de simulación con estadísticas completas).
2. ✅ Asegurar persistencia de resultados históricos (cada temporada se guarda en `data/historical_results.csv` o similar).
3. ➡️ **Implementar el módulo de predicción** (puede correr en paralelo a ETAPA 2, no bloquea economía).
4. Luego ETAPA 3, 4, 5.

### Algoritmo: GoalStrength.Fit()

El núcleo del modelo es un algoritmo iterativo que calcula dos métricas por equipo:

- **Attack** (>1.0 = mejor que el promedio de la liga, <1.0 = peor)
- **DefenseVulnerability** (>1.0 = más vulnerable que el promedio, <1.0 = más sólido)

```
1. Tomar N años de resultados históricos con peso decreciente (0.75^años)
   (los partidos más recientes importan más).

2. Calcular goles promedio de la liga (avg ≈ 1.25-1.35).

3. Inicializar: attack = 1.0, vulnerability = 1.0 para todos los equipos.

4. Iterar 8 veces (o hasta converger):
   a) Para cada equipo:
      - attack = goles_anotados / (avg × vulnerability_del_rival)
      - vulnerability = goles_recibidos / (avg × attack_del_rival)
      - Aplicar "shrinkage": acercar el valor a 1.0 si el equipo
        tiene pocos partidos (evita sobreajuste).
   b) Normalizar: re-escalar para que el promedio de todos los equipos sea 1.0.

5. Resultado: cada equipo tiene un par (attack, defenseVulnerability).
```

### Predicción de partido

Dado el contexto de un partido:

```
λ_local  = avg × attack_local × vulnerability_visitante × GoalScale
λ_visita = avg × attack_visitante × vulnerability_local × GoalScale
(si no es cancha neutral: λ_local × HomeAdvantageMultiplier ≈ 1.08)

Limitar λ entre 0.1 y 5.5 para evitar absurdos.
```

Luego, con los dos λ se genera una **grilla completa de marcadores** (0-0 hasta 10-10) usando Dixon-Coles, que ajusta la correlación en partidos de pocos goles (el 0-0 y 1-0 son más probables que en Poisson puro).

### Componentes a implementar en Python

```
services/
  goal_strength.py       → GoalStrength.Fit() (ataque/defensa ajustados)
  prediction_service.py  → Orquestar predictores, elegir el mejor
  evaluation_service.py  → Evaluar precisión (Brier Score, Log Loss)

predictors/
  ipredictor.py          → Interfaz base (abstract class)
  goal_model.py          → Poisson + Dixon-Coles con GoalStrength
  recent_form_model.py   → Últimos 5 partidos del equipo

data/
  historical_results.csv → Resultados acumulados de todas las temporadas
```

### Evaluación de predicciones

Cuando el modelo empiece a predecir, se evalúa con:

| Métrica | Qué mide |
|---------|----------|
| **Brier Score** | Qué tan calibradas están las probabilidades (0 = perfecto) |
| **Ranked Probability Score** | Para distribución de marcadores completos |
| **Log Loss** | Penaliza predicciones muy seguras pero equivocadas |
| **Top Pick Correct** | % de veces que el resultado más probable fue el correcto |

### Integración con FootballGM

El módulo de predicción NO modifica el motor de simulación. Es una capa aparte que:

1. **Lee** los resultados históricos que genera el simulador.
2. **Calcula** GoalStrength (ataque/defensa ajustados) para cada equipo.
3. **Predice** partidos futuros con esos datos.
4. **Evalúa** qué tan buena es la predicción vs. el resultado real.

Esto permite que en el futuro se pueda:
- Mostrar predicciones antes de cada partido en la UI.
- Usar el modelo como base para IA de fichajes (comprar jugadores que mejoren attack/vulnerability).
- Alimentar un sistema de "scouting" que identifique equipos sobrevalorados o subvalorados.
- Incluso reemplazar el Poisson actual del motor si la predicción es mejor que la simulación.

El código de referencia (Oloraculo, C#) está disponible en `Oloraculo (inspo)/` para consultar la implementación original del algoritmo `Fit()` cuando se quiera portar a Python.

---

## Sobre los servicios (separación de responsabilidades)

Hoy `Team` tiene métodos como `calculate_attack()`, `calculate_defense()`, `calculate_overall()`. Mañana probablemente se quieran:

- `calculate_midfield()`
- `calculate_pressing()`
- `calculate_possession()`
- `calculate_speed()`
- `calculate_creativity()`
- `calculate_setpieces()`

Si eso ocurre, **no se hace dentro de `Team`**. Se crea `services/team_ratings.py` que recibe un equipo y devuelve las métricas. `Team` debe representar un equipo (sus datos), no convertirse en una calculadora gigante.

Los servicios planificados son:

| Servicio | Responsabilidad |
|----------|----------------|
| `services/team_ratings.py` | Cálculo de todas las métricas de equipo (ATK, DEF, MID, PRESS, etc.) |
| `services/match_engine.py` | Orquestador de simulación de partido (futuro reemplazo de Poisson) |
| `services/league_scheduler.py` | Generación de fixture y gestión de jornadas |
| `services/transfer_market.py` | Lógica de fichajes, valoraciones, negociaciones |
| `services/finance_engine.py` | Presupuestos, salarios, premios, ingresos |

---

## Sobre los tests

Los tests no son opcionales. Son lo que permite modificar el simulador sin romper cosas. Apenas ETAPA 1 esté completa, debe existir:

```
tests/
├── test_player.py   → creación, serialización, actualización de stats, casos borde
├── test_team.py     → cálculo de OVR/ATK/DEF, plantel vacío, jugadores duplicados
├── test_match.py    → simulación, distribución de goles, goleadores, asistentes, tarjetas
├── test_league.py   → fixture, tabla, desempates, goleadores, temporada completa
└── simulate_seasons.py → benchmark Monte Carlo (ya existe)
```

Cada test debe ser ejecutable individualmente con `python -m tests.test_match` y todos juntos con un runner.

---

## Decisiones de arquitectura (fijadas)

| Decisión | Elección | Motivo |
|----------|----------|--------|
| Lenguaje del motor | Python 3 | Rápido de iterar, suficiente para simulación |
| Persistencia inicial | JSON | Simple, legible, sin DB en MVP |
| Motor de partido | Poisson + ratings | Escalable; no requiere simular 90 minutos |
| Frontend objetivo | SPA en navegador | Alineado con Basketball GM |
| Separación dominio / I/O | Estricta | Permite consola hoy, web mañana |
| Tests por modelo | Unitarios + Monte Carlo | Modificar sin romper |
| Servicios separados de modelos | Sí | Team no es una calculadora |

---

## Referencia rápida — archivos clave

| Archivo | Para qué sirve |
|---------|----------------|
| `main.py` | Demo: temporada completa en consola |
| `models/match.py` | Motor de simulación (λ, Poisson, goleadores, orquesta eventos) |
| `models/match_event.py` | Evento atómico del partido (gol, tarjeta, lesión, cambio, etc.) |
| `models/league.py` | Fixture, jornadas, tabla, goleadores |
| `data/teams.json` | Base de datos de planteles (16 equipos) |
| `services/team_repository.py` | CRUD de equipos en disco |
| `tests/simulate_seasons.py` | Benchmark Monte Carlo: N temporadas silenciosas + informe estadístico |

---

## Próximos pasos inmediatos (priorizados)

1. ✅ **ETAPA 1 – Sprint 3:** separar attack/finishing, migrar JSON, verificar goleadores/asistentes. *(Completado)*
2. 🔄 **ETAPA 1 – Sprint 3 (restante):** balancear λ con simulaciones masivas.
3. 🔄 **ETAPA 1 – Sprint 3 (restante):** alinear `sandbox.py` con `Player(...)` actual.
4. ⬜ **ETAPA 1 – Sprint 4:** implementar asistencias, tarjetas, lesiones, suspensiones, estadísticas individuales.
5. ⬜ **ETAPA 1 – Sprint 5:** crear tests unitarios por modelo (`test_player.py`, `test_team.py`, `test_match.py`, `test_league.py`).
6. ⬜ **ETAPA 2 – Sprint 6:** diseñar sistema de presupuesto y finanzas.
7. ⬜ **ETAPA 2 – Sprint 7:** implementar fichajes, contratos y scouting básico.
8. ⬜ **ETAPA 3 – Sprint 8:** formación, alineación titular y cambios.
9. ⬜ **ETAPA 3 – Sprint 9:** instrucciones tácticas, objetivos del club, cantera.
10. ⬜ **ETAPA 4 – Sprint 10:** API REST con FastAPI.
11. ⬜ **ETAPA 4 – Sprint 11:** frontend React + TypeScript MVP.
12. ⬜ **ETAPA 5 – Sprints 13–14:** online, cuentas, multiplayer.

---

*Última actualización: 22 jun 2026 — Roadmap reestructurado en 5 etapas verticales (Motor → Economía → Manager → Interfaz → Online). Añadidas secciones de tests, servicios, visión de IA del partido, MatchEvent (eventos atómicos) y Módulo de predicción GoalStrength/Dixon-Coles (implementar después de ETAPA 1). ETAPA 1 ~70% (Sprint 3 en curso). Próximo: completar estadísticas del motor (Sprint 4) y tests unitarios (Sprint 5).*
