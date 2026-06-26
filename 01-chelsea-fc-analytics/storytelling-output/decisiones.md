# Tabla de decisiones — Chelsea FC Results Dashboard

Cada fila mapea una metrica a su visual recomendado, con justificacion de marco, costo/advertencia de uso.

| Pagina | Metrica | Visual recomendado | Tipo de Power BI | Justificacion | Marco citado | Costo / Advertencia |
|---|---|---|---|---|---|---|
| Season Overview | REF PL Position | Tarjeta (card) | Card (nativo) | Un numero que importa arriba-izquierda — ancla el BLUF de la pagina. | BLUF + Knaflic — preatentivo | No usar velocimetro: sin contexto de tendencia, baja densidad. |
| Season Overview | # PL Points | Tarjeta | Card | Complemento cuantitativo: la posicion dice donde, los puntos dicen por cuanto. | Knaflic — contexto | — |
| Season Overview | % Win Rate | Tarjeta | Card | Compacta W/D/L en un KPI ejecutivo accionable. | Knaflic — eliminar desorden | Complementar con desglose W/D/L si hay espacio. |
| Season Overview | # Trophies Won | Tarjeta | Card | Contexto de exito que conecta con la audiencia mas amplia. | Knaflic — contexto | Verificar que COUNT sobre trophies_won no infle si hay varias filas por temporada. |
| Season Overview | $ Net Profit/Loss (£) | Tarjeta con variacion | Card (nativo, con KPI indicator) | Introduce la tension financiera del reporte sin necesitar pagina separada. | IBCS — notacion de varianza; BLUF | Verde/rojo SOLO segun convencion IBCS, nunca decorativo. |
| Season Overview | # PL Points por temporada | Columnas agrupadas | Column chart (nativo) | 6 periodos discretos — columnas comunican magnitud mejor que linea; color por era de propiedad. | Knaflic — grafico correcto; Gestalt — similitud | No torta; no linea con 6 puntos discretos sin continuidad logica entre valores. |
| Season Overview | Resumen por temporada | Tabla | Table (nativa) | 6 filas × 5 columnas — valores exactos, formato condicional en pl_finish. | Knaflic — valores exactos; Tufte — data-ink | Limitar a columnas clave; tabla gigante (15+ cols) es antipatron. |
| Match Performance | % Win Rate | Tarjeta | Card | KPI heroe de la pagina, posicion arriba-izquierda (patron Z). | BLUF + patron Z | — |
| Match Performance | % Home Win Rate / % Away Win Rate | Tarjetas par | Card x2 | La comparacion local vs visitante es la tension central; deben estar proximas (Gestalt). | Gestalt — proximidad; Knaflic — tension narrativa | — |
| Match Performance | % Clean Sheet Rate | Tarjeta | Card | Complemento defensivo al analisis ofensivo. | Knaflic — contexto completo | — |
| Match Performance | # Goal Difference | Tarjeta con color condicional | Card | Sintesis ofensiva + defensiva en un numero; positivo/negativo con color convencional. | IBCS — notacion de varianza | — |
| Match Performance | W/D/L por temporada | Barra apilada al 100% | Stacked bar chart (nativo) | 3 categorias que suman el total de partidos por temporada — permite comparacion entre temporadas. | Knaflic — parte-de-un-todo con 3 partes; IBCS — codificacion W=verde, L=rojo, D=gris | No torta: con 6 temporadas la barra apilada habilita la comparacion directa que la torta no puede. |
| Match Performance | Goals Scored vs Goals Conceded | Linea (2 series) | Line chart (nativo) | Tendencia temporal de 6 puntos con 2 series en la misma unidad (goles) — un solo eje Y. | Knaflic — tendencia; Tufte — integridad (sin doble eje si misma unidad) | Evitar doble eje aunque las escalas sean similares — no añade informacion y confunde. |
| Financial Performance | $ Net Profit/Loss | Tarjeta | Card con KPI indicator | El veredicto financiero de la temporada; formato IBCS positivo/negativo. | BLUF; IBCS | Verde/rojo solo por convencion, no decorativo. |
| Financial Performance | $ Total Revenue / $ Total Cost | Tarjetas par | Card x2 | El triangulo financiero (Net / Revenue / Cost) completo en el vistazo inicial. | Gestalt — proximidad; Knaflic — contexto | — |
| Financial Performance | % Wage to Revenue Ratio | Tarjeta | Card | Metrica de sostenibilidad clave en futbol; un wage-to-revenue >70% señala desequilibrio. | Knaflic — metrica accionable para la decision | Considerar linea de referencia del umbral si el visual lo soporta. |
| Financial Performance | Revenue vs Cost por temporada | Columnas agrupadas | Clustered column chart (nativo) | Dos series (revenue/cost) por temporada para comparar la brecha a lo largo del tiempo. | Knaflic — comparar dos series; Tufte — data-ink | No waterfall aqui: el waterfall es mejor para desglosar UNA temporada, no comparar 6. |
| Financial Performance | Revenue breakdown | Barra apilada al 100% | Stacked bar chart (nativo) | 4 subcategorias de ingreso que suman el total por temporada. | Knaflic — parte-de-un-todo; Gestalt — similitud por color | Limitar a 4 subcategorias; agrupar "Otros" si aparecen mas. |
| Transfer Activity | $ Net Transfer Spend | Tarjeta con variacion | Card | BLUF del mercado: gasto menos ingresos por ventas. IBCS positivo=gasto neto. | BLUF; IBCS | — |
| Transfer Activity | # Avg Age of Signings | Tarjeta | Card | Revela la estrategia de fichajes: sub-23 = potencial; 27+ = rendimiento inmediato. | Knaflic — decision accionable | — |
| Transfer Activity | $ Value vs Fee Ratio | Tarjeta | Card | La metrica de eficiencia central: >1 el jugador vale mas de lo que costo. | IBCS — unidad explicita; BLUF | Verificar cruce fact_transfers (IN, no loan) con fact_player_valuations en la misma season. |
| Transfer Activity | Spend IN vs Income OUT por temporada | Columnas agrupadas | Clustered column chart | La asimetria de gasto bajo BlueCo queda evidente con columnas agrupadas por temporada. | Knaflic — comparar categorias; IBCS — codificacion (rojo gasto / verde ingreso) | No usar linea: los valores son discretos por temporada y de diferente naturaleza (gasto vs ingreso). |
| Transfer Activity | Top 10 fichajes mas caros | Barras horizontales ordenadas | Bar chart (nativo) | Ranking de 10 elementos con etiquetas largas (nombres): barras horizontales obligan. | Knaflic — ranking con barras ordenadas; Tufte — data-ink | Un color unico + acento en el fichaje mas caro. No arcoiris de colores. |
| Squad & Wages | $ Total Annual Wage Bill | Tarjeta | Card | BLUF de la pagina: numero de sostenibilidad mas importante. | BLUF | — |
| Squad & Wages | % Wage Bill YoY Change | Tarjeta con variacion | Card con indicador | Convierte el absoluto en señal de tendencia: ¿la masa salarial se acelera o frena? | IBCS — notacion de varianza | — |
| Squad & Wages | $ Wage per Appearance | Tarjeta | Card | Metrica de eficiencia: coste salarial por aparicion real en cancha. | Knaflic — decision accionable | Cruce fact_player_wages + fact_player_performance debe usar el mismo season_id. |
| Squad & Wages | $ Highest Paid Player + nombre | Tarjeta | Card | Personaliza el dato y genera interes narrativo. | Knaflic — hacer el dato memorable | — |
| Squad & Wages | Wage Bill por temporada | Linea | Line chart (nativo) | Tendencia sostenida de 6 puntos: la linea enfatiza el crecimiento continuo. | Knaflic — tendencia temporal; Gestalt — continuidad | Anotar el cambio de propiedad directamente en el grafico (banda/linea vertical), no solo en leyenda. |
| Squad & Wages | Top 10 salarios por jugador | Barras horizontales ordenadas | Bar chart | Ranking salarial: barras ordenadas de mayor a menor por salario semanal. | Knaflic — ranking | Un color + acento en el mas alto. No un color por jugador (arcoiris sin significado). |
| Players Market Value | $ Squad Market Value | Tarjeta | Card | BLUF: el balance de activos del club en un numero. | BLUF | — |
| Players Market Value | % Squad Value YoY Change | Tarjeta con variacion | Card | Tendencia: ¿el plantel se revaloriza o deprecia vs la temporada anterior? | IBCS — varianza; Knaflic — atencion al cambio | — |
| Players Market Value | $ Value vs Fee Ratio | Tarjeta | Card | El veredicto de eficiencia: ¿el plantel vale lo que se pago? KPI de resolucion del hilo conductor. | IBCS — unidad; BLUF — resolucion narrativa | Verificar que el calculo use el valor mas reciente disponible en fact_player_valuations. |
| Players Market Value | Valor del plantel por temporada | Linea | Line chart | Serie temporal de 6 puntos. Anotar el pico para enfatizar la narrativa. | Knaflic — tendencia; Gestalt — continuidad | — |
| Players Market Value | Top 10 jugadores por valor de mercado | Barras horizontales ordenadas | Bar chart | Ranking de activos mas valiosos. Considerar añadir precio de compra como segunda barra para comparar. | Knaflic — ranking | Sin doble eje si se añade segunda barra. Alternativa: scatter (fee vs valor) en drillthrough. |
| Player Performance | Top Scorer Name + Goals | Tarjeta doble (KPI Card) | Card | BLUF nominal: el dato que la audiencia quiere ver primero. | BLUF; Knaflic — dato memorable | — |
| Player Performance | # Goals per 90 / # Goal Contributions per 90 | Tarjetas | Card x2 | Normalizacion por minutos elimina el sesgo de jugadores con mas partidos. | Knaflic — metrica justa para la decision | — |
| Player Performance | # Avg Player Rating | Tarjeta | Card | Evaluacion global de consistencia; complementa los KPIs de goles/asistencias. | Knaflic — contexto | Rating es media de medias — comunicar la fuente al usuario. |
| Player Performance | Top 10 por Goal Contributions | Barras apiladas horizontales | Stacked bar chart horizontal | Ranking con desglose goles/asistencias (2 categorias): barra apilada de 2 partes es legible. | Knaflic — ranking + parte-de-un-todo | No separar en dos barras independientes por jugador: menos compacto y mas dificil de comparar. |
| Player Performance | Estadisticas completas por jugador | Tabla (7 columnas max) | Table (nativa) | Detalle filtrable para responder preguntas exactas. Formato condicional en goals_per_90 y rating. | Knaflic — valores exactos; Tufte — data-ink | Maximo 7 columnas. El detalle adicional va en drillthrough. Tabla de 15+ cols es antipatron. |

---

## Historias que el modelo NO soporta todavia

| Historia | Razon | Que habria que añadir |
|---|---|---|
| Rendimiento por partido del jugador | fact_player_performance tiene grano de temporada, no de partido | fact_player_match_performance a grano partido |
| Expected Goals (xG) | No existe columna xG en el modelo | Fuente externa de xG (Opta, StatsBomb) |
| Analisis por dificultad del rival | opponent existe pero sin datos de fuerza rival | Dimension de ranking de rival o resultado de liga del oponente |
| Valuaciones mensuales de mercado | fact_player_valuations tiene valuation_date pero el modelo muestra una por temporada | Datos de valuacion mensual si disponibles en Transfermarkt |
