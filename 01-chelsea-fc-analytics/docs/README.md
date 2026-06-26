# Chelsea FC Analytics Dataset (2020/21 – 2025/26)
## Power BI Portfolio Project

---

## Overview
This dataset covers 6 seasons of Chelsea FC data across all major competitions.
It follows a **star schema** (medallion-style) designed for Power BI semantic modeling.

All financial figures are in **GBP (£)**. EUR equivalents are provided as secondary columns.
Data is inspired by real-world sources (Transfermarkt, Capology, UEFA, Deloitte Football Money League).

---

## File Structure

| File | Type | Description |
|---|---|---|
| `dim_season.csv` | Dimension | Season metadata, managers, ownership era, competition results |
| `dim_player.csv` | Dimension | Player master data across all seasons |
| `dim_competition.csv` | Dimension | Competition reference table |
| `fact_matches.csv` | Fact | Match-level results, attendance, matchday revenue |
| `fact_financials.csv` | Fact | Club P&L broken down by revenue/cost category per season |
| `fact_transfers.csv` | Fact | Transfer activity in and out per season |
| `fact_player_wages.csv` | Fact | Per-player, per-season wage breakdown including bonuses |
| `fact_player_valuations.csv` | Fact | Market valuations per player per season (Transfermarkt-style) |
| `fact_player_performance.csv` | Fact | Per-player, per-season performance statistics |

---

## Data Model Relationships

```
dim_season (season_id) ──< fact_matches
dim_season (season_id) ──< fact_financials
dim_season (season_id) ──< fact_transfers
dim_season (season_id) ──< fact_player_wages
dim_season (season_id) ──< fact_player_valuations
dim_season (season_id) ──< fact_player_performance

dim_player (player_id) ──< fact_transfers
dim_player (player_id) ──< fact_player_wages
dim_player (player_id) ──< fact_player_valuations
dim_player (player_id) ──< fact_player_performance

dim_competition (competition_id) ──< fact_matches
```

---

## Suggested Dashboard Pages

### 1. Season Overview
- KPI cards: PL position, matches played, W/D/L, goals scored/conceded
- Season timeline with trophies
- Manager tenure bar

### 2. Financial Performance
- Revenue vs Cost waterfall by season
- Revenue breakdown by stream (Broadcast, Commercial, Matchday, Player Sales)
- Cost breakdown (Wages, Amortisation, Operations, Agent Fees)
- Net profit/loss trend

### 3. Transfer Activity
- Net spend by season (in vs out)
- Top 10 most expensive signings
- Nationality breakdown of signings
- Age at time of signing distribution

### 4. Squad & Wages
- Wage bill by season (trend)
- Top earners by season (bar chart)
- Wage vs market value scatter (efficiency)
- Position group wage distribution

### 5. Player Market Values
- Squad total value trend
- Top valued players per season
- Value change YoY per player
- Age vs value bubble chart

### 6. Match Performance
- Win/Draw/Loss % by competition
- Goals scored vs conceded by season
- Attendance trends (home)
- Home vs Away record

### 7. Player Performance
- Top scorers and assisters per season
- Minutes per goal/assist ratios
- Rating trends by player
- Position group contribution

---

## Notes
- Season S1 = 2020/21 (COVID, no matchday revenue)
- Ownership changed from Abramovich to BlueCo in May 2022 (S2)
- Financial figures for S6 are partial estimates (season in progress)
- Match results for S6 are through approximately April 2026
- Wage figures inspired by Capology and public reporting; treated as estimates
- Market valuations follow Transfermarkt-style peak/decline logic by age and performance
