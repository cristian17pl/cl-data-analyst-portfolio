# Storyboard — Chelsea FC Results Dashboard (2020/21 – 2025/26)

## Hilo conductor

> **La era BlueCo triplico el gasto en transferencias. ¿Los resultados en el campo y el valor del plantel justifican la inversion?**

Arco narrativo: **Contexto → Conflicto → Resolucion**

| Etapa | Pregunta | Paginas que la responden |
|---|---|---|
| **Contexto** | ¿Que paso en cada temporada? ¿Quien dirigia el equipo, en que posicion terminamos? | Season Overview |
| **Conflicto** | ¿Los resultados en cancha mejoraron? ¿A que costo financiero? ¿Vale el plantel lo que se pago? | Match Performance → Financial Performance → Transfer Activity |
| **Resolucion** | ¿Que jugadores representan el verdadero valor del plantel? ¿Quien justifica su sueldo con rendimiento? | Squad & Wages → Players Market Value → Player Performance |

---

## Audiencia y decision

- **Audiencia primaria:** Direccion deportiva, directores financieros del club, analitica de rendimiento.
- **Audiencia secundaria:** Stakeholders externos, aficionados con interes analitico.
- **Decision central:** Evaluar si la estrategia de inversion de BlueCo (mercado + salarios) se traduce en progreso sostenible en el campo y en el balance del club.

---

## Plan de paginas

### 0. Cover
- **Rol:** Portada decorativa. Sin visuales de datos.
- **Takeaway:** N/A

---

### 1. Season Overview
- **Rol:** BLUF ejecutivo. El vistazo de 3 segundos que responde "¿como fue esta temporada?"
- **Takeaway:** *Seis temporadas, dos eras: la era BlueCo mejoro la posicion en la Premier League pero a un costo financiero record.*
- **Metrica heroe:** REF PL Position
- **Decision habilitada:** ¿En que temporada estuvo Chelsea en su mejor y peor momento? ¿Bajo que gestor y era de propietario?
- **Flujo de lectura (patron Z):**
  - Arriba (tarjetas): PL Position → PL Points → Win Rate → Trophies → Net Profit/Loss → Current Season
  - Abajo izquierda: Evolucion de puntos PL por temporada (columnas coloreadas por era)
  - Abajo derecha: Tabla resumen temporal (gestor, posicion, trofeos, era)

---

### 2. Match Performance
- **Rol:** Analisis de resultados en cancha. La historia ofensiva y defensiva.
- **Takeaway:** *El rendimiento en casa es solido; la tasa de victorias fuera de casa es donde se pierden los puntos decisivos.*
- **Metrica heroe:** % Win Rate
- **Decision habilitada:** ¿Donde enfocar el trabajo tactico: rendimiento local o visitante? ¿En que competicion fallamos mas?
- **Flujo de lectura:**
  - Arriba: Win Rate global → Home Win Rate → Away Win Rate → Clean Sheet Rate → Goal Difference → Avg Attendance
  - Abajo izquierda: Distribucion W/D/L por temporada (barra apilada al 100%, colores por resultado)
  - Abajo derecha: Goles anotados vs encajados por temporada (linea, mismo eje)

---

### 3. Financial Performance
- **Rol:** Salud financiera del club. La tension entre ingresos crecientes y costes crecientes mas rapido.
- **Takeaway:** *Los ingresos se recuperan del COVID, pero los costes de amortizacion y salarios mantienen al club en perdidas bajo BlueCo.*
- **Metrica heroe:** $ Net Profit/Loss (£)
- **Decision habilitada:** ¿El modelo financiero es sostenible? ¿Donde crecen los costes mas rapidamente?
- **Flujo de lectura:**
  - Arriba: Net P&L → Total Revenue → Total Cost → Wage-to-Revenue Ratio
  - Abajo izquierda: Columnas agrupadas Revenue vs Cost por temporada (tendencia de brecha)
  - Abajo derecha: Barra apilada al 100% de Revenue breakdown (Broadcast / Commercial / Matchday / Player Sales)

---

### 4. Transfer Activity
- **Rol:** Eficiencia del mercado de fichajes. ¿Donde fue el dinero y que retorno genera?
- **Takeaway:** *Mas de £1B gastados bajo BlueCo en 3 temporadas; el ratio Valor/Precio muestra que la mayoria de las inversiones aun no han madurado.*
- **Metrica heroe:** $ Net Transfer Spend (£)
- **Decision habilitada:** ¿Fue eficiente la estrategia de mercado? ¿Que ventanas aportaron mas valor relativo?
- **Flujo de lectura:**
  - Arriba: Net Transfer Spend → Transfers IN → Avg Age of Signings → Value vs Fee Ratio → Total Loans
  - Abajo izquierda: Columnas agrupadas (Spend IN vs Income OUT) por temporada
  - Abajo derecha: Top 10 fichajes mas caros (barras horizontales ordenadas)

---

### 5. Squad & Wages
- **Rol:** Sostenibilidad salarial y eficiencia del gasto en salarios.
- **Takeaway:** *La masa salarial crecio mas del 40% bajo BlueCo; el coste por aparicion revela que varios jugadores de alta remuneracion aportan poco tiempo en cancha.*
- **Metrica heroe:** $ Total Annual Wage Bill (£)
- **Decision habilitada:** ¿Estamos obteniendo valor deportivo del gasto en salarios? ¿Que perfiles salariales son mas eficientes?
- **Flujo de lectura:**
  - Arriba: Wage Bill anual → YoY Change → Wage per Appearance → Highest Paid Player
  - Abajo izquierda: Linea de masa salarial por temporada (anotacion del cambio de era)
  - Abajo derecha: Top 10 salarios por jugador (barras horizontales, temporada seleccionada)

---

### 6. Players Market Value
- **Rol:** Balance de activos del plantel. La pregunta: ¿vale lo que se pago?
- **Takeaway:** *El valor total del plantel supero los £1B en su pico, pero el ratio Valor/Precio indica que la mayoria de las inversiones aun no han madurado.*
- **Metrica heroe:** $ Value vs Fee Ratio
- **Decision habilitada:** ¿Vale el plantel lo que se pago por el? ¿Que jugadores son los activos mas valiosos hoy?
- **Flujo de lectura:**
  - Arriba: Squad Market Value → YoY Change % → Value vs Fee Ratio → Most Valuable Player
  - Abajo izquierda: Linea de valor total del plantel por temporada
  - Abajo derecha: Top 10 jugadores por valor de mercado (barras horizontales)

---

### 7. Player Performance
- **Rol:** Evaluacion individual. Quien aporta mas valor real en cancha.
- **Takeaway:** *Las metricas por 90 minutos y el rating promedio identifican a los verdaderos creadores de juego mas alla del simple conteo de apariciones.*
- **Metrica heroe:** # Goal Contributions per 90
- **Decision habilitada:** ¿Quien aporta mas valor relativo? ¿Que jugadores justifican su ficha salarial con rendimiento real?
- **Flujo de lectura:**
  - Arriba: Top Scorer (nombre + goles) → Goals per 90 → Goal Contributions per 90 → Avg Rating
  - Abajo izquierda: Top 10 jugadores por Goal Contributions (barras apiladas goles/asistencias)
  - Abajo derecha: Tabla detallada por jugador (appearances, goals, assists, minutes, goals_per_90, rating)

---

## Lo que el modelo NO soporta todavia

| Historia pedida | Por que no funciona | Que habria que modelar |
|---|---|---|
| Rendimiento por partido del jugador (tendencia intra-temporada) | fact_player_performance tiene grano de temporada, no de partido | Añadir fact_player_match_performance a nivel partido |
| Expected Goals (xG) | No existe ninguna columna xG en el modelo | Incorporar datos de xG de una fuente externa |
| Analisis por rival / dificultad del calendario | fact_matches tiene `opponent` pero no hay datos de fuerza del rival | Añadir una dimension de fuerza rival o resultado final de liga del oponente |
| Evoluciones mensuales de valor de mercado | fact_player_valuations tiene valuation_date pero el modelo actual solo muestra una valuacion por temporada | Cargar datos de valuacion mensual si estan disponibles |

---

## Encadenamiento con /new-pbip

Para construir el reporte real a partir de este diseno:
1. Usar `proposal.json` de este storyboard como semilla para `/new-pbip`.
2. Las posiciones de `positionHint` se pueden traducir a coordenadas absolutas 1280×720 con la formula de la grilla 12×12.
3. Las medidas ya existen en la tabla `DAX Measures`; el modelo no requiere cambios para las historias soportadas.
