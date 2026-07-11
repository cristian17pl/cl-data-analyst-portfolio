# Tabla de decisiones — Spotify: 9 Años de Escucha

> Cada visual se justifica en tres ejes: qué decisión habilita, qué marco lo respalda, y qué advierte.

---

## Visuals propuestos

| Visual ID | Página | Tipo | Métricas | Decisión habilitada | Marco | Advertencia / Costo |
|-----------|--------|------|---------|---------------------|-------|---------------------|
| **p1n05** | Resumen Sonoro | `areaChart` | # Total Hours Played × year_month_name | ¿Cómo evolucionó mi escucha en 9 años? | Knaflic — tendencia temporal; Tufte — data-ink; IBCS — título con mensaje | 108 puntos pueden quedar densos — añadir marcas de año con textbox |
| **p1n06** | Resumen Sonoro | `clusteredBarChart` | # Avg Hours per Active Day × year | ¿En qué año fui más intenso (no solo más voluminoso)? | Knaflic — métrica correcta; IBCS — comparación sin distorsión | La métrica puede ser 0 si un año tiene pocos datos — verificar |
| **p1n07** | Resumen Sonoro | `multiRowCard` | REF Top Artist + REF Top Track | ¿Quién y qué definen el periodo seleccionado? | Knaflic — lo concreto ancla la historia | Reacciona al slicer de año — validar que cambia correctamente |
| **p2n04** ⭐ | El Ritmo de Mi Día | `pivotTable` (heatmap) | # Total Hours Played × day_name × hour_label | ¿Cuándo escucho? — mapa de rituales 7×24 | Tufte — data-ink ratio; Gestalt — figura/fondo; glance test | **CRÍTICO**: conditional formatting por columna, no por tabla entera |
| **p2n05** | El Ritmo de Mi Día | `hundredPercentStackedBarChart` | # Total Hours × week_type × day_part | ¿El patrón del día cambia en semana vs. fin de semana? | IBCS — normalización; Knaflic — parte-de-un-todo | Solo 4 partes (day_part) — correcto para 100% stacked |
| **p2n06** | El Ritmo de Mi Día | `barChart` | # Total Hours × day_name | ¿Qué día escucho más en total? — ranking semanal | Knaflic — comparar categorías; Gestalt — proximidad con 100% stacked | Ordenar por día de semana (lunes-domingo), no por valor |
| **p3n05** ⭐ | Mi ADN de Escucha | `scatterChart` | artist × # Streams × % Completion Rate × # Total Hours (size) | ¿Cuáles son mis artistas de fondo vs. mis favoritos reales? | Knaflic — relación entre métricas; Tufte — 3 vars sin chartjunk | Filtrar top 40 artistas; excluir artistas con < 5 streams (ruido estadístico) |
| **p3n06** | Mi ADN de Escucha | `pivotTable` (heatmap) | % Skip Rate × day_name × day_part | ¿Cuándo soy más impaciente con las canciones? | Gestalt — figura/fondo; Knaflic — color preatentivo | Gradiente verde→rojo sobre tabla entera (no por columna) |
| **p3n07** | Mi ADN de Escucha | `barChart` | # Streams × reason_start | ¿Cómo inicio mis streams? — intención vs. flujo automático | Knaflic — comparar categorías; Tufte — honestidad | reason_start tiene valores técnicos de API — añadir etiquetas descriptivas en Power Query |
| **p4n01** ⭐ | Mis Artistas | `ribbonChart` | # Total Hours × year × artist | ¿Cómo evolucionó el ranking de artistas año a año? | Knaflic — ranking + tendencia; Tufte — densidad sin chartjunk | Filtrar top 8-10 artistas; más series = bandas ilegibles |
| **p4n02** | Mis Artistas | `barChart` | # Total Hours × artist (top 10) | ¿Quién es mi artista #1 de toda la historia? | Knaflic — comparar categorías; Tufte — eje desde cero | Limitar a top 10 + agrupar "Otros" si se quiere mostrar el % |
| **p4n03** | Mis Artistas | `tableEx` | track + artist + # Streams + % Completion Rate + Avg Min/Stream | ¿Qué canciones me marcaron más? ¿Las completo? | Knaflic — valores exactos en tabla; Tufte — conditional formatting como dato | Máx 5 columnas, top 20 filas; ordenar por # Streams |
| **p5n05** ⭐ | Plataformas y Contexto | `hundredPercentStackedBarChart` | # Total Hours × year × platform_group | ¿Cuándo migré de plataforma? — historia de dispositivos | IBCS — normalización; Tufte — honestidad; glance test | Agrupar "Not Applicable" + "Other" si < 5% individual |
| **p5n06** | Plataformas y Contexto | `barChart` | # Total Hours × device_brand | ¿Qué marcas de dispositivos usé más? | Knaflic — comparar categorías | "Unknown" puede dominar — verificar cobertura del parser de dim_platform |
| **p5n07** | Plataformas y Contexto | `hundredPercentStackedColumnChart` | # Total Hours × year × device_type | ¿Cómo evolucionó Mobile vs. Desktop vs. Console vs. TV? | IBCS — normalización; Gestalt — similitud con visual principal | Solo 5 device_types — paleta de 5 colores bien distinguibles |

⭐ = Visual flagship de la página (el más sofisticado, el que más insight entrega).

---

## Antipatrones descartados explícitamente

| Antipatrón descartado | Contexto | Por qué se descartó | Alternativa elegida |
|----------------------|----------|---------------------|---------------------|
| **Torta de plataformas** | Página 5 | > 5 sectores, comparar ángulos es ilegible (Knaflic, Tufte) | `hundredPercentStackedBarChart` |
| **Velocímetro para completion rate** | Página 3 | Ocupa mucho espacio para un número; la aguja sesga la percepción; sin tendencia (IBCS) | `cardVisual` con valor + formato |
| **Doble eje** para # Streams + % Completion Rate | Página 3 | Invita a correlaciones falsas; escalas arbitrarias (Tufte — honestidad gráfica) | `scatterChart` con ambas métricas en ejes independientes |
| **3D en cualquier visual** | Global | Distorsión de perspectiva pura (Tufte — chartjunk) | Ninguno — todos los visuals son 2D planos |
| **Línea spaghetti de 10+ artistas** | Página 4 | Ilegible con más de 4-5 series (Knaflic) | `ribbonChart` (diseñado específicamente para esto) |
| **Dashboard de números sin historia** | Página 1 | Colección de tarjetas sin mensaje ni flujo (Knaflic — antipatrón de tablón) | KPIs solo en fila BLUF + visual héroe como protagonista |
| **Tabla de 20+ columnas** | Página 4 | Nadie la lee; entierra el dato relevante (tipos-visual.md) | `tableEx` de 5 columnas focalizadas |

---

## Costo de cada visual principal (Direct Lake / query)

> Nota: este modelo usa modo Import, no Direct Lake — el costo de query es menor. Igualmente se documentan por buena práctica.

| Visual | Costo estimado | Razón |
|--------|---------------|-------|
| Matrix heatmap 7×24 | Medio-alto | 168 celdas = 168 puntos de agregación en la misma query |
| Scatter chart artistas | Medio | Una query por artista en el contexto — filtrar a top 40 reduce el costo |
| Ribbon chart | Medio | N series × M años — filtrar a top 10 artistas |
| 100% stacked por año | Bajo | Agrupación simple por año y platform_group |
| Area chart mensual | Bajo | Una serie, 108 puntos |
| tableEx canciones | Bajo-Medio | Top 20 filas con 5 columnas + 2 medidas calculadas |

---

## Medidas del modelo usadas / no usadas

### Usadas en el diseño

| Carpeta | Medidas usadas |
|---------|---------------|
| 1_Overview | `# Streams`, `# Track Streams`, `# Unique Tracks`, `# Unique Artists`, `# Active Listening Days`, `# Countries Streamed From`, `# Platform Groups Used` |
| 2_Listening Time | `# Total Hours Played`, `# Avg Hours per Active Day`, `# Avg Minutes per Stream`, `# Streams per Active Day` |
| 3_Behavior | `% Completion Rate`, `% Skip Rate`, `% Shuffle Rate`, `% Manual Start Rate`, `% Offline Rate`, `% Private Session Rate` |
| 4_Trends | `% Hours YoY Growth` (como referencia en el área chart) |
| 5_Rankings | `# Artist Rank by Hours` (para filtrar scatter y ribbon) |
| 6_Text Cards | `REF Top Artist`, `REF Top Track`, `REF Selected Date Range` |

### No usadas / descartadas con justificación

| Medida | Razón de no uso |
|--------|----------------|
| `# Total Ms Played`, `# Total Minutes Played`, `# Total Days Played` | Redundantes con `# Total Hours Played` para el storytelling (misma historia, diferente unidad) |
| `# Episode Streams`, `# Unique Episodes` | No forman parte del hilo conductor principal; podrían ser una página adicional de podcasts si el volumen de episodios es significativo |
| `# Hours Previous Month`, `# Hours Previous Year`, `# Streams Previous Year` | Son medidas auxiliares para calcular varianza — se usan indirectamente en los YoY/MoM pero no como visuales propios |
| `% Hours MoM Growth`, `% Streams YoY Growth` | Útiles en un contexto de monitoreo continuo, pero el foco de este reporte es retrospectivo, no de seguimiento |
| `# Forward Skip Ends`, `% Forward Skip End Rate`, `# Auto Continuation Starts`, `% Auto Continuation Rate`, `# Shuffle Streams`, `# Skipped Streams`, `# Completed Streams`, `# Manual Starts`, `# Offline Streams`, `# Private Session Streams` | Los conteos crudos se DEGRADAN a favor de sus tasas (%) que son más comparables entre periodos de diferente volumen |
| `# Track Rank by Streams`, `# Platform Rank by Hours` | Usados como filtros, no como visuales propios |
| `REF Top Platform Group` | Podría añadirse a la página 5 si hay espacio; no es crítico |
