# Chelsea FC Analytics Data Documentation

This folder contains the CSV source data and dataset documentation used by the Chelsea FC Analytics Power BI report.

## Data Provenance

The dataset was **generated and curated with Claude and Codex**, using publicly available football and business data patterns as reference material.

It is intended for portfolio storytelling, semantic modeling, dashboard design, and DAX practice. It is **not** an official Chelsea FC dataset and should not be used as an audited source of club records.

Reference inspiration includes:

- Transfermarkt-style transfer fees and player market values
- Capology-style wage estimates
- Premier League and UEFA competition structures
- Deloitte Football Money League-style financial benchmarking

Some values were estimated, normalized, or enriched to create a complete analytical story across six seasons.

## Player Counts

- `dim_player.csv`: 51 player master records
- `fact_player_valuations.csv`: 38 distinct players with valuation history
- `fact_player_performance.csv`: 38 distinct players with performance history
- Latest valuation snapshot (`2026-05-01`): 17 players

The Power BI report separates these concepts because "total players in the dataset" and "players in the latest market-value snapshot" answer different questions.

## Files

| File | Type | Description |
|---|---|---|
| `dim_season.csv` | Dimension | Season metadata, manager, ownership era, PL finish, trophies |
| `dim_player.csv` | Dimension | Player master data, position, position group, nationality |
| `dim_competition.csv` | Dimension | Competition reference table |
| `fact_matches.csv` | Fact | Match-level results, goals, attendance, matchday revenue, xG, opponent tiering inputs |
| `fact_financials.csv` | Fact | Revenue and cost categories by season |
| `fact_transfers.csv` | Fact | Transfer activity in/out and transfer fees |
| `fact_player_wages.csv` | Fact | Player wage estimates by season |
| `fact_player_valuations.csv` | Fact | Player market value snapshots |
| `fact_player_performance.csv` | Fact | Player appearances, goals, assists, ratings, pass accuracy, clean sheets |
| `fact_trophies.csv` | Fact | Trophy-level detail |

## Notes

- Financial values are modeled in GBP.
- 2025-26 data is treated as an analytical portfolio scenario, not a verified live season feed.
- Player valuations include multiple snapshots to support within-season value movement.
- The Power BI report is stored in PBIP/TMDL format under `../pbip`.
- Final PDF previews are stored under `../reports`.
