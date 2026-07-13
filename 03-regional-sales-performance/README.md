# Regional Sales Performance Report

An end-to-end Power BI portfolio project analyzing regional revenue, profitability, target attainment, product concentration, seasonality, and channel economics.

The report is built as a Power BI Project (`.pbip`) with a dual-fact semantic model, PBIR/TMDL source files, DAX measures, field parameters, HTML/DAX custom visuals, report-page tooltips, drillthrough navigation, and a polished multi-page dashboard experience.

## Quick Look

For a non-Power BI preview, open the storytelling PDF:

[Regional Sales Performance - Storytelling Quick Look](./reports/regional-sales-performance-storytelling-quick-look.pdf)

The PDF includes the final report pages, visible filter contexts, tooltip and drillthrough behavior, semantic-model diagrams, measure architecture, and short narrative notes explaining how each page supports the commercial story.

## Project Summary

- **Domain:** Corporate sales analytics, regional performance, planning, product mix, and channel profitability
- **Tooling:** Power BI Desktop, PBIP/PBIR/TMDL, Power Query, DAX, HTML/DAX custom visuals, Python, Git
- **Period covered:** 2022 through 2025
- **Data source:** Microsoft AdventureWorks sales data transformed from normalized source tables into an analytical star schema
- **Core lens:** Revenue growth, geographic concentration, target accountability, product drivers, seasonality, and Online versus Reseller economics
- **Sales grain:** 121,317 sales-order lines
- **Report pages:** Cover plus 6 primary analytical pages, 1 drillthrough page, and 1 report-page tooltip
- **Measure layer:** 81 measures organized in a dedicated `formulas` table
- **Key techniques:** Dual-fact modeling, virtual relationships with `TREATAS`, time intelligence, field parameters, rank-based conditional formatting, decomposition tree, Azure Maps, report-page tooltips, drillthrough, custom SVG backgrounds, and HTML KPI cards

## Data Note

The transactional data comes from Microsoft's AdventureWorks sample database, a public relational dataset for a fictional bicycle manufacturer. The source tables were reshaped into dimensions and facts for analytical use.

Most of the data is real AdventureWorks sample data. One analytical table is intentionally synthetic:

- `fact_targets` contains monthly revenue targets by Year, Month, Territory, and Category.
- Targets are generated as prior-year same-month actual revenue multiplied by `1.08`.
- Target coverage begins in 2023 because the calculation requires a comparable prior year.
- The target construction is disclosed in the report cover and documentation.

AdventureWorks also contains a genuine margin story. Online sales remain strongly profitable, while Reseller pricing can fall below standard cost for some products. Negative reseller margin is therefore treated as an analytical finding, not removed as an error.

## Report Pages

### 1. Cover

Corporate landing page with project navigation, scope, data disclosure, and a sales-growth visual motif.

### 2. Executive Summary

Combines the report's primary commercial signals:

- Revenue, profitability, and target-performance HTML KPI cards
- Regional revenue-change waterfall
- Monthly revenue trend
- Revenue concentration by category
- Current top Region, Category, and Product

The page moves from headline performance to the specific regions and products responsible for the result.

### 3. Regional Performance

Answers where revenue sits and which regions are accountable for plan delivery:

- Revenue footprint by country using Azure Maps
- Actual versus target by Region
- Rank-based attainment chart with leader and laggard colors
- Exact regional scorecard with revenue, YoY, attainment, and margin
- Report-page tooltip with a rolling 12-month regional trend
- Region-driven drillthrough action

### 4. Product and Margin Drivers

Explains revenue below the category level:

- Interactive decomposition tree across Category, Subcategory, Product, Region, and Channel
- Top subcategories by revenue
- Product table with revenue, units, and margin context
- Conditional font formatting for negative-margin products

The decomposition tree supports self-service root-cause analysis, while the ranking and table provide a stable audit view.

### 5. Revenue Trend and Seasonality

Provides three complementary time perspectives:

- Metric-selector hero line for Revenue, Margin, Units, or Orders
- Month-by-Year seasonality comparison
- Year-to-date cumulative revenue race
- HTML cards for revenue pace, profit quality, and commercial activity

The metric selector uses a disconnected field parameter and a composite-key-safe bridge measure.

### 6. Channel Margin Story

Separates revenue scale from profit quality:

- Revenue columns with margin-rate line by month
- Gross margin by Category and Channel, including negative values
- Online versus Reseller revenue mix by year
- Exact channel economics with revenue, margin, margin rate, and average order value
- HTML cards summarizing Online, Reseller, and the channel trade-off

The key story is that Reseller produces greater revenue and basket size but materially weaker margin than Online.

### 7. Target Performance Scorecard

Turns target status into an action list:

- Region-by-Category attainment matrix with green, amber, and red status formatting
- Worst-first target variance table
- Revenue versus plan, plan attainment, and regional coverage cards

The matrix uses a DAX virtual relationship so Product Category can filter targets without creating an ambiguous physical relationship.

### 8. Territory Detail

Hidden drillthrough page scoped to a selected Region:

- Territory revenue, attainment, and profitability HTML cards
- Monthly territory revenue trajectory
- Top subcategories
- Top-15 products with units and margin
- Online versus Reseller mix by year
- Back-to-report navigation

### 9. Regional Trend Tooltip

Hidden tooltip page that provides revenue, YoY change, and a rolling 12-month trend without forcing the reader to leave the source visual.

## Data Model

The semantic model uses a dual-fact design: transactional sales and monthly targets share conformed Date and Territory dimensions.

### Dimension Tables

| Table | Purpose |
|---|---|
| `dim_date` | Daily calendar, sortable month attributes, English display labels, and `MonthStart` for continuous axes |
| `dim_product` | Category, subcategory, product line, product, color, list price, and standard cost |
| `dim_customer` | Customer and segment attributes |
| `dim_territory` | Region, country code, continent, and territory key |
| `dim_channel` | Online versus Reseller channel |

### Fact, Measure, and Selector Tables

| Table | Purpose |
|---|---|
| `fact_sales` | Order-line revenue, cost, margin, quantity, customer, product, territory, channel, and order date |
| `fact_targets` | Monthly Territory-by-Category revenue targets |
| `formulas` | Centralized measures, helper logic, conditional colors, text outputs, and HTML visuals |
| `Metric selector` | Disconnected field parameter used to switch the hero trend metric |

### Relationship Strategy

- `fact_sales` relates to Date, Product, Customer, Territory, and Channel.
- `fact_targets` relates physically to Date and Territory.
- Category target analysis uses `TREATAS(VALUES(dim_product[Category]), fact_targets[Category])` instead of a physical Product relationship.
- The Customer-to-Territory relationship remains inactive to avoid ambiguous filter paths.
- The metric-selector table is intentionally disconnected.

## DAX and Visual Logic

All measures are stored in the `formulas` table and organized as a reusable analytical layer.

### Display Folders

| Folder | Purpose |
|---|---|
| `0_Custom_Visuals` | DAX-generated HTML cards, tooltip cards, and leaders panel |
| `1_Sales` | Revenue, cost, margin, AOV, discount, and mix |
| `2_Volume` | Orders, order lines, units, active customers, and products sold |
| `3_Targets` | Target revenue, comparable-period variance, attainment, and coverage |
| `4_Time Intelligence` | Prior year, YTD, YoY, rolling windows, and percentage-point change |
| `5_Channel` | Online and Reseller revenue, margin, share, and AOV |
| `6_Rankings` | Context-aware ranks and Top-N measures |
| `7_Selectors` | Field-parameter resolution and selector logic |
| `7_Text Cards` | Labels, leaders, references, and conditional-formatting colors |

### Naming Prefixes

- `$` for currency measures
- `%` for rates and shares
- `#` for counts, quantities, and ranks
- `pp` for percentage-point change
- `REF` for helper labels, selected values, and color logic
- `VIS HTML` for DAX-generated HTML visual output

### Advanced DAX Patterns

The report uses more than basic aggregations. Important patterns include:

- `CALCULATE` for channel measures, prior periods, scoped KPIs, and context transitions
- `REMOVEFILTERS`, `KEEPFILTERS`, `ALL`, and `ALLSELECTED` for comparison denominators and visible-context control
- `TREATAS` for the virtual Product Category relationship to `fact_targets`
- `SAMEPERIODLASTYEAR`, `TOTALYTD`, and `EDATE` for prior-year, cumulative, and rolling-period analysis
- `RANKX`, `TOPN`, and `ISINSCOPE` for rankings, Top-N filters, and leader/laggard formatting
- `SELECTEDVALUE` and `SWITCH` for metric-selector and context-aware text logic
- `FORMAT`, variables, and string concatenation for compact labels and HTML visuals

Notable measures include:

- `$ Total Revenue`
- `$ Gross Margin`
- `% Margin Rate`
- `$ Target Revenue`
- `% Target Attainment`
- `$ Revenue YTD`
- `% Revenue YoY`
- `Selected Metric Value`
- `REF Region Attainment Bar Color`
- `REF Target Attainment Background Color`
- `VIS HTML Executive KPI Cards`
- `VIS HTML Trend KPI Cards`
- `VIS HTML Channel KPI Cards`
- `VIS HTML Target KPI Cards`
- `VIS HTML Territory KPI Cards`
- `VIS HTML Tooltip KPI Cards`

## Visual Design Rationale

- **Waterfall:** decomposes revenue change into accountable regional contributions.
- **Azure Map:** establishes country-level geographic footprint only where geography is the question.
- **Paired bars:** compare actual revenue and target at the same regional scale.
- **Rank-colored bars:** reserve gold for the leader, red for the laggard, and blue for middle ranks.
- **Decomposition tree:** lets the reader choose the root-cause path instead of forcing one static hierarchy.
- **Field parameter:** lets one hero trend support multiple metrics without bookmarks.
- **Combo chart:** uses separate revenue and margin-rate axes for one explicit volume-versus-quality decision.
- **RAG matrix:** compresses 40 target statuses into a readable operational scorecard.
- **HTML/DAX cards:** combine value, comparison, context, and status in compact report surfaces.
- **Report-page tooltip and drillthrough:** add detail on demand while preserving the report's visual grammar.

## Portfolio Highlights

- Built in PBIP/PBIR/TMDL format for source control and semantic-model transparency
- Dual-fact model combining real sales transactions with disclosed synthetic targets
- 81-measure DAX layer organized by analytical purpose and prefix convention
- Field-parameter-driven metric selector
- Virtual target relationship implemented with `TREATAS`
- Rank-based and RAG conditional formatting
- Custom HTML KPI cards with consistent visual semantics
- Report-page tooltip and Region drillthrough workflow
- Storytelling PDF covering pages, interactions, model architecture, and DAX patterns

## Repository Structure

```text
03-regional-sales-performance/
|-- README.md
|-- docs/
|   |-- dim_*.csv
|   |-- fact_*.csv
|   |-- raw/
|   |-- storytelling-designer-session-notes.md
|   `-- Visuals/
|       |-- Regional Sales Visuals.pptx
|       |-- Regional Sales Visuals/
|       |-- storytelling-screenshots/
|       `-- executive-summary-html-cards-dax.md
|-- pbip/
|   |-- Regional Sales.pbip
|   |-- Regional Sales.Report/
|   `-- Regional Sales.SemanticModel/
|-- reports/
|   `-- regional-sales-performance-storytelling-quick-look.pdf
`-- tools/
    `-- build_storytelling_pdf.py
```

## How to Open

1. Open `pbip/Regional Sales.pbip` in Power BI Desktop.
2. If you refresh after cloning, update the CSV source paths to the cloned project's `docs/` folder; the processed model inputs are included, while the larger public raw extracts remain git-ignored.
3. Use the cover navigation buttons or report tabs to move through the analysis.
4. On Regional Performance, select a Region before using **View Territory Detail**.

For a static preview, open:

[reports/regional-sales-performance-storytelling-quick-look.pdf](./reports/regional-sales-performance-storytelling-quick-look.pdf)

## Status

Completed portfolio report. Final dashboard pages, semantic model, DAX measures, visual assets, tooltip and drillthrough behavior, storytelling PDF, and documentation are included.

---

Built by Cristian Perez Lagos as a BI and analytics portfolio project.
