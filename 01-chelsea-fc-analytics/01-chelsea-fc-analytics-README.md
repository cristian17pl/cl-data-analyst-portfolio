# Chelsea FC Analytics Dashboard

**An end-to-end Power BI portfolio project** — dimensional data modeling, 70+ DAX measures, and an 8-page interactive report tracking Chelsea FC performance, finances, and squad activity across six seasons.

Built to demonstrate BI/analytics engineering skills applicable to Microsoft Fabric, Power BI, and modern data architecture roles.

![Cover page screenshot](./screenshots/cover.png)
*(screenshot placeholder — replace with actual export)*

---

## ⚠️ A note on the data

This dataset is **synthetic** — built to closely mirror real-world figures in structure, scale, and realism, but it is **not** pulled live via API or scraping from any source. It's referenced/inspired by the following, for context and realism:

- **Transfermarkt** — transfer fees, market valuations
- **Capology** — wage and salary data
- **UEFA / Premier League official records** — match results, competition data
- **Deloitte Football Money League** — financial benchmarking context

The purpose of this project is to demonstrate data modeling, DAX, and dashboard design skills — not to serve as a source of factual club records.

---

## Scope

- **6 seasons**: 2020–21 through 2025–26
- **8 competitions**: Premier League, UEFA Champions League, UEFA Europa Conference League, FA Cup, EFL Cup, FIFA Club World Cup, UEFA Super Cup, plus friendlies (friendlies excluded from match data, included only as a financial revenue line)
- **~340+ matches**
- **40 players** tracked across the dataset

---

## Data model — star schema

**Dimension tables**
| Table | Description |
|---|---|
| `dim_season` | Season metadata, managers, ownership era, competition results, trophies |
| `dim_player` | Player master data (40 players), nationality, position, dates joined/left |
| `dim_competition` | 8 competitions with type and prestige level |
| `Calendar` | Calculated date table with custom football-season logic (July–June) |

**Fact tables**
| Table | Description |
|---|---|
| `fact_matches` | Match-level results, attendance, matchday revenue |
| `fact_financials` | Club P&L by revenue/cost category per season |
| `fact_transfers` | Transfer activity in/out, fees, loans |
| `fact_player_wages` | Per-player, per-season wages, bonuses, agent fees |
| `fact_player_valuations` | Transfermarkt-style market values per player per season |
| `fact_player_performance` | Appearances, goals, assists, ratings, cards |

---

## Report pages

1. **Cover**
2. **Season Overview**
3. **Match Performance**
4. **Financial Performance** — includes a Sankey money-flow diagram
5. **Transfer Activity**
6. **Squad & Wages**
7. **Player Market Values**
8. **Player Performance**

Interactive **bookmarks** allow toggling between views (All Competitions vs. PL only, Annual vs. Weekly wages, All players vs. 20+ appearances, etc.)

---

## DAX

**70+ custom measures**, organized by category:

| Category | # of Measures |
|---|---|
| Match Performance | 18 |
| Financial | 16 |
| Player Performance | 14 |
| Wages & Squad | 11 |
| Transfers | 9 |
| Player Valuations | 7 |

Full breakdown in [`docs/dax-measures.md`](./docs/dax-measures.md).

### Sample measures

```dax
Value vs Fee Ratio = 
DIVIDE(
    [Current Market Value],
    [Total Fee Paid],
    BLANK()
)
```
*Flags over/underpaid players by comparing what was paid against current market valuation.*

```dax
Goals per 90 = 
DIVIDE(
    [Total Goals],
    [Total Minutes Played],
    0
) * 90
```
*Normalizes goal output per 90 minutes played, enabling fair comparison across players with different playing time.*

*(more measures documented in `/docs`)*

---

## Notable features

- **Custom calendar table** with football-season logic (season runs July–June, not calendar year)
- **Value vs. fee paid ratio** — surfaces over/underpaid players relative to current market value
- **Per-90-minute normalization** — standardizes player performance stats for fair comparison
- **Sankey diagram** for financial money-flow visualization

---

## Tech stack

- Power BI Desktop
- DAX
- Star schema / dimensional modeling
- Power BI Project (PBIP) format, version-controlled via GitHub

---

## Project status

🚧 **In progress** — data model and DAX measures complete; report pages being built out incrementally.

---

## Repo structure

```
01-chelsea-fc-analytics/
├── README.md
├── /pbip              ← Power BI Project files
├── /docs              ← data dictionary, DAX measure docs, star schema diagram
└── /screenshots       ← report page exports
```

---

*Built by Cristian Perez as a portfolio project.*
