# Spotify Listening Analytics Report

An end-to-end Power BI portfolio project analyzing personal Spotify listening behavior from 2017 through 2026.

The report is built as a Power BI Project (`.pbip`) with a semantic model, Power Query transformations, DAX measures, custom HTML/DAX cards, Spotify-themed visual design, and a polished multi-page dashboard experience.

## Quick Look

For a non-Power BI preview, open the storytelling PDF:

[Spotify Listening Analytics - Storytelling Quick Look](./reports/spotify-listening-analytics-storytelling-quick-look.pdf)

The PDF includes the final report pages with short narrative notes explaining the core message and how each page supports the listening-behavior story.

## Project Summary

- **Domain:** Personal data analytics, music listening behavior, digital habits
- **Tooling:** Power BI Desktop, PBIP/TMDL, Power Query, DAX, HTML/DAX custom visuals, Git
- **Period covered:** 2017 through 2026
- **Data source:** Spotify Extended Streaming History export
- **Core lens:** Listening volume, routine, engagement quality, artist preference, and platform context
- **Report pages:** Cover plus 5 analytical pages, including separate Artist and Album views
- **Key techniques:** Star schema modeling, DAX measures, time intelligence, conditional formatting, heatmap analysis, scatter analysis, rank/top-N views, custom SVG backgrounds, storytelling PDF

## Data Note

This project uses a personal Spotify Extended Streaming History export. The raw files live under `docs/my_spotify_data/` and include audio/video streaming history JSON files plus Spotify's export readme.

The dataset was not generated synthetically. It comes from real account-level Spotify usage data and was transformed inside Power BI for analysis. The Spotify export arrives as event-level JSON history, so the model starts from a single streaming-history fact table and then derives supporting dimension tables for dates, time, platforms, artists/tracks, episodes, and stream start/end reasons.

Codex was used to assist with report documentation, PDF generation, TMDL inspection, and selected model/visual formatting work.

Because this is personal behavioral data, the report is intended as a portfolio artifact and analytical case study rather than a reusable public benchmark dataset.

## Report Pages

### 1. Cover

Landing page that frames the full story:

- 9 years of listening
- Total hours played
- Unique artists
- Active listening days
- 2017-2026 scope

The goal is to make the scale of the dataset clear before moving into analysis.

### 2. Sound Overview

High-level listening summary for the selected year:

- Total hours played
- Unique artists
- Active listening days
- Unique tracks
- Top artist, track, album, and platform
- Monthly listening hours
- Average daily listening hours by month

This page answers: how much did I listen, and how concentrated was that listening?

### 3. My Daily Rhythm

Routine and time-pattern analysis:

- Hours by weekday and hour heatmap
- Total hours, average hours per active day, streams per active day, active days
- Listening mix by week type
- Listening hours by weekday

The heatmap was chosen because hourly listening patterns are easiest to read as intensity, not as a long list of bars. It turns timestamp data into a behavioral routine map.

### 4. My Listening DNA

Engagement and listening-quality analysis:

- Completion rate
- Skip rate
- Shuffle rate
- Manual starts
- Artist completion vs streams scatter plot
- Skip rate by time of day
- Streams by start reason

The scatter plot separates high-volume artists from high-completion favorites. The matrix and start-reason visual add behavioral context beyond raw hours.

### 5. My Artists

Two-view artist and album page.

**Artist View**

- Top artist listening trends
- Top artists by listening hours
- Song-level detail table

This view shows how artist preference changes over time and which artists dominate the current listening profile.

**Album View**

- Artists with most albums played
- Top albums by listening hours
- Album-level detail table

This view adds depth to the artist story by showing whether listening is concentrated in a few songs or spread across broader catalogs.

### 6. Platforms & Context

Listening environment and device analysis:

- Offline rate
- Countries
- Platform groups
- Platform usage by year
- Listening hours by device type
- Listening hours by platform treemap

This page explains where listening happens. It connects the music story to device behavior, platform switching, and listening context.

## Data Model

The semantic model follows a star-schema structure centered on `fact_streaming_history`.

Spotify's raw export does not ship as an analytics-ready dimensional model. The project first consolidates the JSON files into one stream-level fact table, then creates dimension tables from the repeated descriptive attributes inside that fact table. This keeps the report model cleaner, reduces repeated text fields in visuals, and makes slicers and relationships easier to manage.

### Dimension Tables

| Table | Purpose |
|---|---|
| `dim_calendar` | Date, year, month, weekday, week type, and time-intelligence attributes |
| `dim_time` | Hour, time labels, and day-part buckets |
| `dim_song_artist` | Track, album, and artist metadata |
| `dim_episode` | Podcast/video episode metadata |
| `dim_platform` | Platform and device group normalization |
| `dim_reason_start` | Reason a stream started |
| `dim_reason_end` | Reason a stream ended |

### Fact and Measure Tables

| Table | Purpose |
|---|---|
| `fact_streaming_history` | Stream-level Spotify listening events |
| `formulas` | DAX measures, references, helper labels, and custom HTML visual measures |

## DAX and Visual Logic

The model includes measures grouped across overview, listening time, behavior, trends, rankings, text cards, and custom visuals.

All DAX measures are kept in a dedicated `formulas` table to avoid scattering business logic across fact and dimension tables. Measures are organized primarily by report page or analytical theme, then by metric type where useful.

Naming prefixes are used intentionally:

- `REF` for reference measures, labels, and text-card outputs
- `#` for counts, quantities, and numeric volume measures
- `%` for percentages and rates
- `VIS HTML` for DAX-generated HTML visual outputs

Common DAX patterns include `CALCULATE` for filter-context changes, `RANKX` for top-N and ranking visuals, `VAR`/`RETURN` for readable multi-step measures, and time-intelligence patterns such as previous month, previous year, and YoY growth calculations.

Notable examples:

- `# Streams`
- `# Total Hours Played`
- `# Active Listening Days`
- `# Unique Artists`
- `# Unique Tracks`
- `# Avg Hours per Active Day`
- `# Streams per Active Day`
- `% Completion Rate`
- `% Skip Rate`
- `% Shuffle Rate`
- `% Manual Start Rate`
- `% Offline Rate`
- `% Hours YoY Growth`
- `# Artist Rank by Hours`
- `REF Top Artist`
- `REF Top Track`
- `REF Top Album`
- `VIS HTML TOP Highlights`
- `VIS HTML Behavior Snapshot`
- `VIS HTML Rhythm Snapshot`
- `VIS HTML Platform Context Snapshot`

The calendar table uses explicit English month and weekday labels so visual axes remain consistent regardless of local Windows or Power BI culture settings.

## Visual Design Rationale

- **Area/line charts** show listening volume over time and make peaks/dips easy to scan.
- **Heatmap** shows time-of-day rhythm more clearly than stacked bars or tables.
- **Scatter plot** compares artist engagement quality against volume, separating habit from preference.
- **Ranked bar charts** keep top artists, albums, platforms, and reasons readable.
- **Treemap** works for platform share because the category count is small and the dominant platforms are immediately visible.
- **HTML/DAX cards** provide compact KPI storytelling with current value, movement, and context.
- **Custom SVG backgrounds** give the report a Spotify-native visual identity without relying on generic dashboard styling.

## Portfolio Highlights

- Built in PBIP/TMDL format for source control and semantic-model transparency
- Uses a real Spotify Extended Streaming History export
- Star-schema model around stream-level listening events
- Custom Spotify-themed layout and SVG report backgrounds
- DAX measures for volume, behavior, trends, rankings, and text-driven cards
- Heatmap and scatter analysis for behavioral storytelling
- Static storytelling PDF for viewers who do not have Power BI Desktop

## Repository Structure

```text
02-spotify-listening-analytics/
|-- README.md
|-- docs/
|   |-- my_spotify_data/
|   |   |-- ReadMeFirst_ExtendedStreamingHistory.pdf
|   |   `-- Spotify Extended Streaming History/
|   `-- Visuals/
|       |-- html-visuals-dax.md
|       |-- Spotify Visuals.pptx
|       `-- Spotify Visuals/
|-- pbip/
|   |-- Spotify Listening Analytics.pbip
|   |-- Spotify Listening Analytics.Report/
|   `-- Spotify Listening Analytics.SemanticModel/
|-- reports/
|   `-- spotify-listening-analytics-storytelling-quick-look.pdf
```

## How to Open

1. Open `pbip/Spotify Listening Analytics.pbip` in Power BI Desktop.
2. Refresh the semantic model if prompted.
3. Use the report tabs or in-report navigation to move through the analysis.

For a static preview, open:

[reports/spotify-listening-analytics-storytelling-quick-look.pdf](./reports/spotify-listening-analytics-storytelling-quick-look.pdf)

## Status

Completed portfolio report. Final dashboard pages, semantic model, DAX measures, visual assets, storytelling PDF, and README documentation are included.

---

Built by Cristian Perez Lagos as a BI and analytics portfolio project.
