# Chelsea FC Analytics Report

An end-to-end Power BI portfolio project analyzing Chelsea FC across performance, finances, transfer activity, squad cost, player market value, and player performance.

The report is built as a Power BI Project (`.pbip`) with a semantic model, CSV source data, DAX measures, custom visual storytelling, and a polished multi-page dashboard experience.

## Quick Look

For a non-Power BI preview, open the storytelling PDF:

[Chelsea FC Analytics - Storytelling Quick Look](./reports/chelsea-fc-analytics-storytelling-quick-look.pdf)

The PDF includes the final report pages with short narrative notes explaining the core message, how to read each page, and the portfolio signal behind the visual design.

## Project Summary

- **Domain:** Football analytics, club finance, transfers, squad efficiency
- **Tooling:** Power BI Desktop, PBIP/TMDL, DAX, CSV data model, Git
- **Period covered:** 2020-21 through 2025-26
- **Core lens:** Abramovich era vs BlueCo era
- **Player scope:** 51 player master records, 38 players with performance/value history, 17 players in the latest valuation snapshot
- **Report pages:** 7 analytical pages plus landing/navigation page
- **Key techniques:** Star schema modeling, DAX measures, conditional formatting, HTML/DAX custom visual, reference lines, rank movement, quadrant analysis

## Data Note

This dataset was **generated and curated with Claude and Codex**, based on publicly available football and business data patterns.

It is designed to be realistic enough for portfolio storytelling, dashboard development, DAX modeling, and analytical design practice. It should **not** be treated as an official Chelsea FC dataset or as a source of audited club records.

The dataset was inspired by publicly available references such as:

- Transfermarkt-style transfer fees and market value patterns
- Capology-style wage estimates
- Premier League and UEFA match/competition structures
- Deloitte Football Money League-style financial benchmarking

Some values were enriched, estimated, or normalized to create a complete six-season analytical story. The purpose is to demonstrate BI thinking, not to publish verified football accounting data.

## Report Pages

### 1. Report Home

Executive landing page with the project scope, key counts, data sources, and page navigation.

### 2. Season Overview

Compares season-level outcomes across ownership eras:

- PL finish, PL points, win rate, trophies, and net P/L
- PL points by season and ownership era
- Win/draw/loss by competition
- Season summary table with manager, points, trophies, and start year

### 3. Match Performance

Focuses on match outcomes and opponent difficulty:

- Goals for vs goals against by season
- Win rate against Top-6, Mid-table, and Bottom-half opposition
- W/D/L split by venue
- xG measures added for richer match context

### 4. Financial Performance

Two-view financial page:

- **Financial Sustainability:** revenue vs cost, revenue mix, wage-to-revenue ratio
- **Money Flow:** custom Sankey-style HTML/DAX visual showing revenue streams, direct costs, operating costs, and final net result

### 5. Transfer Activity

Analyzes Chelsea transfer activity as a portfolio:

- Transfer spend, income, net spend, transfers in/out, value-to-fee ratio
- Fee paid vs current market value scatter with quadrant analysis
- Median fee/value reference lines
- Transfer balance by season
- Largest transfer fees paid, colored by ROI signal

### 6. Squad & Wages

Looks at wage efficiency and squad cost:

- Annual wage bill, average weekly wage, wage/revenue, wage per appearance
- Wage bill trajectory vs revenue
- Wage efficiency trend with six-season average benchmark
- Highest cost per appearance by player

### 7. Player Market Value

Tracks squad value and individual asset movement:

- Squad market value trajectory
- Most valuable assets by current/latest market value
- Player value rank movement through a ribbon chart
- Focus story: Cole Palmer's rise to Chelsea's No. 1 asset

### 8. Player Performance

Connects player output with the performance story:

- Goals, assists, goal contributions, average rating, pass accuracy
- Top goal contributors: goals + assists
- Team rating trend across seasons
- Player detail table with appearances, goals, assists, rating, pass accuracy, and clean sheets

## Data Model

The semantic model follows a star-schema structure.

Because this report uses several fact tables, the model includes separate layout pages by analytical area/fact table. This makes the relationship paths easier to inspect than a single crowded all-model view. Layouts are organized around Financials, Wages, Transfers, Matches, and Performance & Valuation.

The model keeps fact tables at their analytical grain and uses shared dimensions such as season, player, competition, and calendar to support cross-page filtering.

### Dimension Tables

| Table | Purpose |
|---|---|
| `dim_season` | Season labels, start year, ownership era, manager, PL finish, trophies |
| `dim_player` | Player master data, position, position group, nationality |
| `dim_competition` | Competition metadata |
| `Calendar` | Date table for time intelligence |

### Fact Tables

| Table | Purpose |
|---|---|
| `fact_matches` | Match results, goals, attendance, matchday revenue, xG, opponent tiering |
| `fact_financials` | Revenue and cost categories by season |
| `fact_transfers` | Transfers in/out, fees, player movement |
| `fact_player_wages` | Player wage estimates by season |
| `fact_player_valuations` | Player market value snapshots |
| `fact_player_performance` | Player appearances, goals, assists, ratings, pass accuracy, clean sheets |
| `fact_trophies` | Trophy-level detail |

## DAX and Visual Logic

The model includes measures across match performance, financials, transfers, wages, squad value, player performance, trends, and HTML visuals.

All DAX measures are kept in a dedicated `DAX Measures` table rather than inside individual fact tables. Measures are organized primarily by report page or analytical theme, then by metric type.

Naming prefixes are used intentionally:

- `REF` for reference measures, text outputs, helper labels, color logic, and conditional-formatting helpers
- `#` for counts, quantities, and volume metrics
- `%` for rates, ratios, and growth metrics
- `$` for GBP/EUR money measures
- `VIS HTML` for DAX-generated HTML visuals

The model uses more advanced DAX patterns such as `CALCULATE`, `SWITCH(TRUE)`, `VAR`/`RETURN`, `RANKX`, `TOPN`, `MEDIANX`, `AVERAGEX`, `ALLSELECTED`, `DATEADD`, `DATESYTD`, `DIVIDE`, and string-based HTML generation for custom visuals.

Notable examples:

- `% Win Rate`
- `# PL Points`
- `$ Net Profit/Loss (GBP)`
- `% Wage to Revenue Ratio`
- `$ Net Transfer Spend (GBP)`
- `$ Player Latest Market Value (GBP)`
- `% Player Transfer ROI`
- `REF Transfer ROI Bar Color`
- `$ Wage per Appearance (GBP)`
- `REF Wage Efficiency Trend Color`
- `VIS HTML Financial Sankey`
- `VIS HTML Squad Value Snapshot`

The report also uses calculated columns for opponent strength tiering:

- `Top-6`
- `Mid-table`
- `Bottom half`
- `Cup / Unknown`

## Portfolio Highlights

- Built in PBIP/TMDL format for source control and semantic-model transparency
- Custom financial Sankey-style visual built with DAX-generated HTML
- Transfer ROI quadrant analysis using fee paid vs latest market value
- Wage efficiency analysis using cost per appearance and benchmark coloring
- Player market value tracking with intra-season snapshots
- Conditional formatting for performance, wage efficiency, ROI, and rating signals
- Storytelling PDF created for viewers who do not have Power BI Desktop

## Repository Structure

```text
01-chelsea-fc-analytics/
|-- README.md
|-- docs/
|   |-- *.csv
|   `-- Visuals/
|-- pbip/
|   |-- Chelsea FC - Results Dashboard.Report/
|   `-- Chelsea FC - Results Dashboard.SemanticModel/
|-- reports/
|   |-- chelsea-fc-analytics-storytelling-quick-look.pdf
|   `-- chelsea-fc-analytics-quick-look.pdf
`-- tools/
    |-- build_quicklook_pdf.py
    `-- build_storytelling_pdf.py
```

## How to Open

1. Open the Power BI Project from the `pbip` folder in Power BI Desktop.
2. Refresh the semantic model if prompted.
3. Use the landing page buttons or report tabs to navigate the analysis.

For a static preview, open:

[reports/chelsea-fc-analytics-storytelling-quick-look.pdf](./reports/chelsea-fc-analytics-storytelling-quick-look.pdf)

## Status

Completed portfolio report. Final dashboard pages, enriched dataset, DAX measures, storytelling PDF, and README documentation are included.

---

Built by Cristian Perez Lagos as a BI and analytics portfolio project.
