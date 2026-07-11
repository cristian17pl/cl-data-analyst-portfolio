# Storyboard — Spotify: 9 Años de Escucha

## Audiencia y decisión central

**Audiencia principal:** Portfolio viewer / análisis personal  
**Decisión habilitada:** ¿Qué revelan 9 años de datos de Spotify sobre mis hábitos, gustos y evolución personal?  
**Audiencia secundaria:** Reclutadores o colegas del área de datos que ven el portfolio — aquí el reporte también debe demostrar capacidad analítica y criterio de storytelling.

---

## Hilo conductor

> **"Mis datos de Spotify revelan quién soy como oyente: cuándo escucho, a quién repito, y cómo cambié."**

Arco narrativo completo (Knaflic — contexto → conflicto → resolución):

| Fase | Páginas | Pregunta | Tensión |
|------|---------|----------|---------|
| **Contexto** | 1 — Resumen Sonoro | ¿Cuánto escucho? ¿Cómo creció? | La escala sorprende |
| **Conflicto** | 2 — El Ritmo de Mi Día | ¿Cuándo escucho realmente? | Los patrones ocultos de hora y día |
| **Conflicto** | 3 — Mi ADN de Escucha | ¿Cómo escucho? ¿Soy activo o pasivo? | Escucha intencional ≠ escucha de fondo |
| **Resolución** | 4 — Mis Artistas | ¿Quién define mi identidad musical? | La identidad no es estática |
| **Resolución** | 5 — Plataformas y Contexto | ¿Dónde y con qué escucho? | Los dispositivos reflejan cambios de vida |

---

## Plan de páginas

### Página 1: Resumen Sonoro
**Frase de takeaway:** "Más de X,000 horas en 9 años: el arco de una vida musical visible en una sola curva."  
**Decisión habilitada:** ¿Soy un oyente intenso o casual? ¿Cómo evolucionó mi escucha?  
**Estructura:** 4 KPI cards (horas totales, artistas únicos, días activos, canciones únicas) + área chart de 9 años (visual héroe) + barras de intensidad por año + card de top artist/track.

**Visual héroe:** `areaChart` — # Total Hours Played × year_month_name (108 meses).  
El área sobre el tiempo es el único visual que muestra simultáneamente la escala total y la irregularidad estacional. Cada pico y valle es visible y le da al portfolio viewer algo para relacionar con eventos de vida.

---

### Página 2: El Ritmo de Mi Día
**Frase de takeaway:** "La escucha se concentra en tarde-noche entre semana; los domingos extienden el patrón hacia la madrugada."  
**Decisión habilitada:** ¿Tengo rituales musicales según la hora y el día? ¿El patrón varía en fin de semana?  
**Estructura:** 2 KPI cards + REF texto | matrix heatmap 7×24 (visual héroe) | 100% stacked día_parte × tipo_semana | barras por día de la semana.

**Visual héroe:** `pivotTable` con formato condicional en gradiente — heatmap 7 días × 24 horas de # Total Hours Played.  
168 celdas con gradiente blanco→verde revelan los rituales de escucha en un solo vistazo. Es el visual más sofisticado del reporte y el que más insight per cm² entrega. Los bookmarks "Días hábiles" / "Fines de semana" permiten comparar si el patrón del commute desaparece el fin de semana.

---

### Página 3: Mi ADN de Escucha
**Frase de takeaway:** "Los artistas más escuchados no son los más completados — hay dos universos: escucha intencional y escucha de fondo."  
**Decisión habilitada:** ¿Cómo escucho? ¿Activo o pasivo? ¿Cuándo soy más impaciente?  
**Estructura:** 4 KPI cards de comportamiento | scatter artista-loyalty (visual héroe) | heatmap 7×4 de skip rate | barras de reason_start.

**Visual héroe:** `scatterChart` — artista × # Streams (X) × % Completion Rate (Y) × horas (tamaño).  
Este es el visual más analíticamente profundo del reporte. Muestra que "escuchar mucho a un artista" y "comprometerse con ese artista" son dimensiones independientes. Los outliers cuentan historias: el artista con 500 streams pero 30% de completion es "música de fondo"; el artista con 50 streams pero 95% de completion es "una joya que apenas descubro".  
El drillthrough a la página 4 permite profundizar en cualquier artista.

---

### Página 4: Mis Artistas
**Frase de takeaway:** "El artista #1 ha cambiado al menos 3 veces en 9 años — la identidad musical es más dinámica de lo que parece."  
**Decisión habilitada:** ¿Quiénes definen mi identidad musical y cómo cambió ese ranking?  
**Estructura:** ribbon chart (visual héroe, ocupa la mitad superior) | barras horizontales top 10 | tabla focalizada top 15-20 canciones.

**Visual héroe:** `ribbonChart` — # Total Hours Played × year × artist.  
El ribbon chart es el visual específicamente diseñado para mostrar cambios de ranking en el tiempo. Cada banda de color es un artista, el ancho proporcional a las horas ese año. En 9 años de datos, esto revela fases musicales claras que ningún bar chart acumulado podría mostrar. Es el visual más narrativamente poderoso del reporte.

---

### Página 5: Plataformas y Contexto
**Frase de takeaway:** "La migración de plataformas es visible año a año — cada cambio refleja un cambio en mi vida."  
**Decisión habilitada:** ¿Desde qué dispositivos escucho? ¿Cómo cambió eso con el tiempo?  
**Estructura:** 4 KPI cards de contexto | 100% stacked platform × year (visual héroe) | barras de device brand | 100% stacked device_type × year.

**Visual héroe:** `hundredPercentStackedBarChart` — # Total Hours Played × year × platform_group.  
Normalizado al 100%, cada año es comparable independientemente del volumen. La historia del cambio de dispositivo —Android → iOS → quizás Smart TV en la pandemia— se lee en segundos. Sin la normalización, los años con más data distorsionarían la composición.

---

## Interactividad global

| Elemento | Tipo | Alcance | Decisión que sirve |
|----------|------|---------|-------------------|
| Slicer: Año | `between` | Todas las páginas | "¿Cómo era yo en 2019 vs. 2024?" |
| Bookmarks P2: Días hábiles / Fines de semana | Filtro de contexto | Página 2 | "¿Cambia mi patrón en el fin de semana?" |
| Slicer P2: Tipo de semana | `dropdown` | Página 2 | Toggle preciso del bookmark |
| Drillthrough P3→P4: Artista | Filtro de navegación | P3 → P4 | "Dame el detalle de este artista del scatter" |
| Tooltip P3 scatter | Página de tooltip | Scatter de p3 | Nombre artista + streams + horas sin abandonar la vista |
| Slicer P5: Tipo dispositivo | `dropdown` | Página 5 | "¿Cómo se ve el patrón de plataformas solo en móvil?" |
| Navegación top-bar | Botones de página | Global | Flujo contexto→conflicto→resolución reflejado en el orden |

---

## Lo que el modelo NO soporta aún (requiere modelar primero)

> **Principio de honestidad (Knaflic §1):** no se diseñan visuales para datos que no existen. Estas historias se marcan como pendientes.

| Historia deseada | Por qué no es posible ahora | Qué habría que modelar |
|-----------------|---------------------------|----------------------|
| **Racha de escucha** (días consecutivos) | No existe medida de streak | Nueva medida DAX con lógica de ventana secuencial (DATEADD + tabla de fechas consecutivas) |
| **Fecha de descubrimiento** por artista/canción | dim_song_artist no tiene fecha de primer stream | Columna calculada en dim_song_artist: `MINX(RELATEDTABLE(fact_streaming_history), fact_streaming_history[ts])` |
| **Género musical** | El export de Spotify no incluye género | Join con Spotify Web API (audio features) vía Power Query o Python ETL |
| **Análisis de audio features** (energía, tempo, danceability) | No están en el export | Spotify Web API por `track_key` (spotify_track_uri) |
| **Comparativa con escucha promedio global** | Dato externo | API de Spotify Charts o Spotify Wrapped API (limitada) |

---

## Paleta y sistema de diseño

| Token | Valor | Uso |
|-------|-------|-----|
| `background` | `#121212` | Fondo de página (Spotify dark) |
| `accent` | `#1DB954` | Color principal, máximos en heatmaps, barras activas |
| `positive` | `#1DB954` | Varianza positiva, skip rate bajo (verde = comprometido) |
| `negative` | `#E22134` | Varianza negativa, skip rate alto (rojo = impaciente) |
| `neutral` | `#535353` | Barras secundarias, texto desactivado |
| `text` | `#FFFFFF` | Texto principal |
| `textSecondary` | `#B3B3B3` | Etiquetas, leyendas |
| Series 1-8 | Ver `proposal.json` | Artistas en ribbon chart, plataformas en 100% stacked |
