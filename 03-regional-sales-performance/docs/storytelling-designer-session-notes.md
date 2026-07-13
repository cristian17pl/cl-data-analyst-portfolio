# Storytelling Designer Upgrade Notes — Regional Sales

## Purpose

This document preserves the visual-design decisions, implementation patterns, failures, and fixes from the Regional Sales Performance PBIP refinement session. It is intended as source material for a future upgrade of the `storytelling-designer` skill.

The central lesson is that a visual is not finished when it renders. It is finished when its metric, comparison, emphasis, interaction, and exact implementation all support the intended decision.

## Report design system

| Role | Color |
|---|---|
| Report/page background | `#0A1628` |
| Standard HTML visual background | `#0E2841` |
| Standard native visual surface | `#0E2841` |
| Native visual border | `#29445F` |
| Primary gold emphasis | `#C8A84B` |
| Standard blue | `#1E6FBF` or `#1E90FF` |
| Positive green | `#3DBA7E` |
| Negative red | `#F04444` |
| Strong negative font | `#FF3131` |
| Secondary text | `#B3C7D9` |

Rules established during the session:

- Use gold for the single leading or strategically emphasized item.
- Use red for the single weakest item or a genuinely negative exception.
- Keep middle-ranked values blue.
- Do not use rank colors decoratively; they must encode a comparison.
- Apply `#29445F` borders to native visuals, but not to slicers or custom HTML visuals.
- Use the HTML background `#0E2841` consistently throughout this project.
- Avoid accent bars when the visual already has enough internal hierarchy.
- Keep subtitles explanatory: state what comparison or interaction the viewer should read.

## Page 1 — Executive Summary

### Before

- Four tall, isolated KPI cards displayed Revenue, Revenue YoY, Margin Rate, and Attainment.
- Revenue and YoY were separated even though they describe the same executive question.
- The multi-row leaders card had weak hierarchy and too much unused space.
- The category chart used an explicitly hard-coded gold Bikes bar.
- The waterfall initially showed a crowded multi-year bridge that was difficult to interpret.

### After

- Consolidated related values into three HTML KPI cards:
  - Revenue plus YoY context.
  - Profitability with margin value and rate.
  - Target performance with attainment and plan variance.
- Reduced card height and added a restrained gold accent bar on the KPI cards.
- Rebuilt current leaders as a wider HTML visual with Region, Category, and Product hierarchy.
- Removed the accent bar from the leaders visual and allowed the layout to provide hierarchy.
- Reframed the waterfall as a regional variance bridge for the current period versus the comparable prior-year period.
- Simplified the monthly line chart by reducing label noise and presenting a clean pulse/trend.
- Reworked category bar colors to use rank logic:
  - Highest visible value: gold.
  - Lowest visible nonblank value: red.
  - All others: blue.

### Reusable lesson

Related KPIs should live in the same card when one is the context for the other. A primary value plus its variance communicates more than two independent cards and uses less space.

## Page 2 — Regional Performance

### Before

- The Azure map worked geographically but had weak narrative support.
- Actual and target bars were visually similar and hard to distinguish.
- Attainment bars showed values but did not identify leaders and laggards.
- The regional table had default styling and inconsistent contrast.

### After

- Kept the Azure map because geography is the page's actual question.
- Clarified the map subtitle as selected-revenue concentration.
- Styled Actual versus Target with a stronger actual series and neutral target series.
- Converted attainment into a sorted accountability ranking:
  - Highest visible region: gold.
  - Lowest visible region: red.
  - Middle regions: blue.
- Restyled the regional scorecard for exact-number reading and drillthrough use.

### Reusable lesson

Use paired bars to show absolute actual-versus-plan gaps, then a normalized attainment ranking to show accountability. These visuals answer different questions and should coexist.

## Page 3 — Product and Margin Drivers

### Before

- The decomposition tree rendered mostly blank because its Analyze/Explain configuration was incomplete or visually unusable.
- The subcategory chart showed too many categories with default formatting.
- The product table initially rendered no useful data, then rendered with harsh default alternating rows and poor contrast.
- Negative margins were not visible enough.

### After

- Repaired the decomposition tree and gave it an explicit exploration instruction.
- Confirmed a useful path such as Category → Subcategory → Region while retaining self-service splitting.
- Used Top-N measures for subcategories and products instead of relying only on visual filters.
- Applied rank colors to the subcategory chart.
- Rebuilt the product table with readable dark styling, revenue sorting, compact spacing, and margin context.
- Applied strong red font to negative margin values rather than changing entire cell backgrounds.

### Reusable lesson

AI/exploration visuals need onboarding text and a useful initial state. A blank interactive visual is not self-explanatory. Tables need deliberate contrast, alignment, sorting, and exception formatting; default table styling is rarely portfolio-ready.

## Page 4 — Revenue Trend and Seasonality

### Before

- The hero line always displayed Revenue even though a Metric field parameter existed.
- The selector and chart were not connected correctly.
- Every monthly value was labeled, producing unnecessary noise.
- The seasonality chart was overcrowded.
- The YTD area chart used a continuous sawtooth series, which made cross-year pace comparisons difficult.

### After

- The hero uses a slicer-driven bridge measure and a continuous `MonthStart` axis.
- Labels were removed from the hero; the axis and line shape carry the trend.
- The seasonality view compares the same month across years.
- The YTD visual became a month-by-year cumulative race.
- Titles and subtitles now explain the analytical purpose and partial-year caveat.

### Remaining design check

The Metric selector slicer is positioned at approximately `x=17.8`, `y=35.6`, with `z=0`. In the latest screenshot it appears to be covered by the header or another visual. Before finalizing the page, ensure the selector is visible, intentionally placed, and above the background layer.

### Trend-page HTML KPI construction

The original top row used three native cards for `$ Revenue YTD`, `% Revenue YoY YTD`, and `$ Revenue PY`. This separated one comparison across three containers and compared YTD revenue with a non-YTD prior-year value.

The replacement is one HTML visual backed by `VIS HTML Trend KPI Cards`, containing three related cards:

- Revenue Pace: `$ Revenue YTD`, `% Revenue YoY YTD`, and `$ Revenue PY YTD`.
- Profit Quality: `% Margin Rate YTD`, `$ Gross Margin YTD`, and margin-rate percentage-point change versus PY YTD.
- Commercial Activity: `# Orders YTD`, `% Orders YoY YTD`, `# Units YTD`, and `$ Avg Order Value YTD`.

Supporting measures were added to their semantic folders:

| Measures | Folder |
|---|---|
| `$ Gross Margin YTD`, `$ Gross Margin PY YTD`, `$ Avg Order Value YTD` | `4_Time Intelligence\$` |
| `% Margin Rate YTD`, `% Margin Rate PY YTD`, `pp Margin Rate vs PY YTD`, `% Orders YoY YTD` | `4_Time Intelligence\%` |
| `# Orders YTD`, `# Orders PY YTD`, `# Units YTD` | `4_Time Intelligence\#` |
| `VIS HTML Trend KPI Cards` | `0_Custom_Visuals` |

Construction lesson: helper measures belong in analytical folders according to unit and purpose; only the final HTML-rendering measure belongs in the custom-visual folder. Keep the HTML measure responsible for presentation and the helper measures responsible for reusable business calculations.

## Page 5 — Channel Margin Story

### Analytical visual rebuild

The page intentionally combines revenue scale, margin quality, channel mix, and exact channel economics. The four top cards were deferred for a later HTML consolidation.

Changes applied:

- Combo chart `0ab005e663544fe49bb8`:
  - Replaced categorical `dim_date[YearMonthName]` with `dim_date[MonthStart]`.
  - Updated ascending sort to the same `MonthStart` field.
  - Set the category axis to scalar/continuous to remove the monthly scrollbar.
  - Fixed primary revenue color to blue and margin-rate line to gold.
  - Set the revenue axis to start at zero and the margin axis to 0%-50% so the line is not compressed against a default 100% scale.
  - Initially added a subtitle explaining the dual encoding, then removed it after rendered review because it duplicated the visible legend. This is a useful render-stage lesson: explanatory copy should not repeat an already-clear encoding key.
- Channel margin leakage chart `60e2b4e3d05b42e7b8ff`:
  - Sorted categories by gross margin descending.
  - Applied consistent channel colors: Online blue, Reseller gold.
  - Exposed the numeric axis so negative bars have a visible zero reference.
  - Preserved negative reseller margin rather than masking or taking absolute values.
  - Reduced category `innerPadding` to `10L` for thicker bars and placed data labels at `OutsideEnd` with white 10pt text so the negative reseller label remains readable left of zero.
- Channel mix chart `5fb173991675418394c6`:
  - Preserved the 100% normalized chart type.
  - Applied the same channel colors used in the margin chart.
  - Removed raw-dollar labels, which are misleading and crowded in a normalized view.
  - Exposed the percentage axis and clarified the normalization in the subtitle.
- Channel economics table `5f4c63d90eb84dd28902`:
  - Repaired the empty visual by changing Revenue, Gross Margin, Margin Rate, and AOV projections from `active: false` to `active: true`.
  - Sorted channels by revenue descending.
  - Added alternating dark rows, deliberate column widths, and compact spacing.
  - Added `REF Margin Rate Font Color` and bound it to Margin and Margin Rate so negative channel economics render in strong red.

Technical lesson: a table can contain correct fields and still render only one column when the remaining projections are serialized as inactive. A construction skill must inspect projection activation flags in addition to field names and relationships.

### Channel-page HTML KPI construction

The original top row separated Online Revenue, Online Margin, Reseller Revenue, and Reseller Margin into four native cards. This repeated labels and forced the viewer to mentally reconstruct the channel comparison.

The replacement `VIS HTML Channel KPI Cards` uses three connected cards:

- Online Engine: revenue, revenue share, gross margin, margin rate, and AOV.
- Reseller Scale: the same measures, with negative margin presented as an exception.
- Channel Trade-off: reseller-to-online revenue multiple, margin-rate gap in percentage points, and gross-margin gap.

AOV means Average Order Value and is calculated as:

```DAX
$ Avg Order Value = DIVIDE([$ Total Revenue], [# Orders])
```

It represents average revenue per distinct sales order. On this page it explains why Reseller can produce much higher revenue with fewer, larger baskets while still generating poor margin quality.

Supporting measures:

| Measures | Folder |
|---|---|
| `$ Gross Margin Online`, `$ Gross Margin Reseller`, `$ Avg Order Value Online`, `$ Avg Order Value Reseller` | `5_Channel\$` |
| `% Online Revenue Share`, `% Reseller Revenue Share` | `5_Channel\%` |
| `VIS HTML Channel KPI Cards` | `0_Custom_Visuals` |

The share denominator explicitly removes `dim_channel[Channel]`:

```DAX
CALCULATE(
    [$ Total Revenue],
    REMOVEFILTERS(dim_channel[Channel])
)
```

This is necessary because fixed Online/Reseller comparison cards should not produce 100% or otherwise distorted shares when the page's Channel slicer filters one channel. Other page filters remain active.

Construction lesson: do not create separate cards for a value and its rate when both describe the same business entity. Build entity-level cards and reserve the third card for the decision-relevant contrast between entities.

## Page 6 — Target Performance Scorecard

### Before

- Three native cards consumed 150 pixels of height and separated Revenue, Attainment, and Regions On Target without useful comparison context.
- The revenue KPI rendered blank.
- The region-by-category matrix occupied the full width but rendered as a small default table in the upper-left corner.
- The matrix had no RAG status colors despite that being its intended purpose.
- The action table rendered only Region because Revenue, Target, and Variance projections were serialized with `active: false`.
- The action table used `$ Total Revenue`, while target and variance used only months covered by `fact_targets`.
- The SVG page title incorrectly read `Channel Margin Target Scorecard`.

### After

- Corrected both the editable and registered SVG resources to `Target Performance Scorecard`.
- Added `VIS HTML Target KPI Cards` at `x=20`, `y=82`, `width=1240`, `height=87`.
- Hid the three superseded native cards with root-level `isHidden: true`.
- Rebuilt the page body as a side-by-side scorecard:
  - RAG matrix: `x=20`, `y=184`, `width=760`, `height=516`.
  - Action table: `x=800`, `y=184`, `width=460`, `height=516`.
- Rebound the action-list Revenue column to `$ Revenue in Target Period` so Revenue, Target, and Variance share the same comparison window.
- Activated all table projections and sorted `$ Variance to Target` ascending.
- Added alternating dark table rows, explicit column widths, and conditional red/green variance font.

### Target KPI construction

The compact HTML row contains:

- Revenue vs Plan: target-period revenue, target, and dollar variance.
- Plan Attainment: attainment percentage and percentage-point distance from 100%.
- Regional Coverage: regions on target, regions with targets, coverage percentage, and number below target.

Supporting measures:

| Measures | Folder |
|---|---|
| `# Regions With Target`, `# Regions Below Target` | `3_Targets\#` |
| `% Regions On Target` | `3_Targets\%` |
| `REF Target Attainment Background Color`, `REF Target Variance Font Color` | `7_Text Cards` |
| `VIS HTML Target KPI Cards` | `0_Custom_Visuals` |

### RAG matrix construction

`REF Target Attainment Background Color` implements the required thresholds:

```DAX
SWITCH(
    TRUE(),
    ISBLANK([% Target Attainment]), "#0E2841",
    [% Target Attainment] >= 1, "#3DBA7E",
    [% Target Attainment] >= 0.9, "#E8A33D",
    "#E63535"
)
```

The matrix `values.backColor` expression references this measure directly, so it evaluates in each Region × Category cell context. White text remains constant over the RAG background.

Rendered validation showed that the first implementation did not apply. The matrix retained white alternating rows because a measure placed only on the default `values.backColor` property was overridden by the matrix's primary/secondary row styling.

The corrected PBIR construction uses two value-style entries:

1. A default fallback that sets `fontColor`, `fontColorPrimary`, and `fontColorSecondary` to white and all three background properties to `#0E2841`.
2. A field-specific conditional entry with:

```json
"selector": {
  "data": [
    {
      "dataViewWildcard": {
        "matchingOption": 1
      }
    }
  ],
  "metadata": "formulas.% Target Attainment"
}
```

The RAG measure is bound to `backColor`, `backColorPrimary`, and `backColorSecondary` in that selected entry. Explicit column widths were also added for `dim_territory.Region` and `formulas.% Target Attainment`.

Construction lesson: matrix conditional formatting must target the value-field metadata and every active row-background variant. A schema-valid default color expression can still be visually ignored by primary/secondary style layers.

### Comparable-period correction

`$ Variance to Target` is defined as:

```DAX
[$ Revenue in Target Period] - [$ Target Revenue]
```

Therefore, a table containing `$ Total Revenue`, `$ Target Revenue`, and `$ Variance to Target` mixes incompatible time windows whenever sales history extends beyond target coverage. The action list must use `$ Revenue in Target Period`.

### Interpretation of extreme category attainment

The four-digit category attainment values were investigated before formatting. The virtual category relationship is working: `$ Target Revenue` uses `TREATAS(VALUES(dim_product[Category]), fact_targets[Category])`, and physical Territory and YearMonth relationships provide the remaining context.

The extreme percentages result from very small category targets relative to actual category revenue. They are a target-calibration/data-quality finding, not a join failure. The scorecard preserves the values rather than capping them, allowing the matrix to expose poorly calibrated targets.

Construction lesson: validate surprising numbers before styling them. Determine whether the issue comes from relationship context, incompatible time coverage, or genuinely extreme source data; each requires a different response.

## Page 8 — Territory Drillthrough

### Drillthrough wiring

The page was already correctly connected before the visual rebuild. Its `page.json` contains:

```json
{
  "filterConfig": {
    "filters": [
      {
        "name": "DrillthroughRegion",
        "field": {
          "Column": {
            "Expression": {
              "SourceRef": {
                "Entity": "dim_territory"
              }
            },
            "Property": "Region"
          }
        },
        "type": "Categorical",
        "howCreated": "Drillthrough"
      }
    ]
  },
  "visibility": "HiddenInViewMode",
  "type": "Drillthrough"
}
```

The Region filter also declares `requireSingleSelect: true`. This ensures the page represents one territory rather than an ambiguous aggregate.

To invoke it, the source visual's selected data point must contain `dim_territory[Region]`. The user right-clicks the data point or table row and chooses `Drill through > Territory Drillthrough`.

### Before

- Five native cards occupied the page header and overlapped the intended navigation/header area.
- The Territory card used disproportionate width while Revenue, YoY, Attainment, and Margin were isolated.
- The monthly line used categorical `YearMonthName`, vertical labels, all-point data labels, and a scrollbar.
- The subcategory chart displayed the full list rather than the required territory-scoped Top 10.
- The product table rendered only Product because Revenue, Units, and Margin projections were `active: false`.
- The channel-mix chart displayed raw dollar labels inside a 100% normalized visual.
- The SVG had no header or page title.

### After

- Added a report header and `Territory Detail` title to both Drillthrough SVG resources.
- Added `VIS HTML Territory KPI Cards` at `x=20`, `y=82`, `width=1240`, `height=87`.
- Hid the five superseded native cards with root-level `isHidden: true`.
- Repositioned the analytical visuals into a balanced 2×2 layout:
  - Revenue trajectory: `x=20`, `y=184`, `width=760`, `height=250`.
  - Subcategory mix: `x=800`, `y=184`, `width=460`, `height=250`.
  - Product table: `x=20`, `y=450`, `width=760`, `height=250`.
  - Channel mix: `x=800`, `y=450`, `width=460`, `height=250`.

### Territory HTML cards

The three cards are:

- Territory Revenue: selected Region, total revenue, prior-year revenue, and YoY change.
- Target Performance: attainment, target, and dollar variance for the comparable target period.
- Profitability: margin rate, gross margin, and AOV.

The final rendering measure is stored in `0_Custom_Visuals`. It uses `REF Selected Region`, which resolves the drillthrough Region context and falls back to `All Regions` only when the page is opened directly.

### Analytical visual construction

- Revenue line `2ee73ff7c3c74f38b414`:
  - Replaced `YearMonthName` with `MonthStart`.
  - Sorted by `MonthStart` ascending.
  - Set the category axis to `Scalar`.
  - Removed point labels and the categorical scrollbar.
- Subcategory bars `e08366c784ab4ae3937f`:
  - Rebound Y to `$ Revenue Top 10 Subcategory`.
  - Preserved drillthrough Region context inside the Top-N calculation.
  - Applied `REF Subcategory Revenue Bar Color` for gold leader, red laggard, and blue middle ranks.
- Product table `5f733bb6b0424a2fbfe3`:
  - Added `$ Revenue Top 15 Product`, `# Units Top 15 Product`, and `% Margin Rate Top 15 Product`.
  - Activated all four projections and sorted revenue descending.
  - Added alternating dark rows, explicit widths, hidden totals, and negative-margin font formatting.
- Channel mix `4365800b16004642a7c2`:
  - Preserved the 100% normalized chart type.
  - Applied Online blue and Reseller gold for cross-page consistency.
  - Removed raw-value labels and exposed the percentage axis.

### Navigation requirement

The PBIR page is connected, but it does not contain a Back button visual. Add one in Desktop:

1. Open the Territory Drillthrough page.
2. Select `Insert > Buttons > Back`.
3. Place it in the header, preferably near the upper-right edge.
4. Confirm Action is enabled and Type is `Back`.

Construction lesson: a drillthrough page requires three distinct things—destination filter metadata, source data points containing the drillthrough field, and a clear return path. Visual design alone does not create the interaction.

### Drillthrough registration failure discovered in Desktop

Rendered testing showed that the page-level PBIR definition was schema-valid and contained `howCreated: Drillthrough`, `type: Drillthrough`, a single-select Region filter, hidden-page visibility, and a working Back button, but Desktop still did not expose the destination in the source visual's drillthrough menu.

This confirms an important construction boundary: manually authoring a page filter that resembles a drillthrough filter is not always sufficient for Desktop to register the page as an operational drillthrough destination. Power BI can maintain additional interaction state when a field is added through the Drill-through field well.

Reliable repair procedure:

1. Open the destination page in Desktop.
2. Select blank canvas space so no visual is selected.
3. In the Build/Visualizations pane, locate `Drill-through` and `Add drill-through fields here`.
4. If Region is already present, remove it.
5. Drag the exact model column `dim_territory[Region]` into the drillthrough field well.
6. Enable `Keep all filters` when source Year, Category, and Channel context should carry forward.
7. Save the PBIP so Desktop serializes the full operational metadata.
8. Test from a source visual that directly contains the same unaggregated `dim_territory[Region]` column.

TMDL cannot configure this behavior because TMDL defines the semantic model, while drillthrough is report-layer interaction metadata.

Construction lesson: distinguish schema validity from feature registration. For Desktop-owned interactions such as drillthrough, bookmarks, and some button actions, require a rendered functional test and use the Desktop UI once when handcrafted PBIR metadata is not recognized.

### Root cause found after Desktop serialized the drillthrough field

After `dim_territory[Region]` was added through Desktop and the PBIP was saved, the filter and binding parameter were present, but the destination still appeared as `None` on a source drillthrough button. The resulting `page.json` exposed the mismatch:

- Page usage was correctly `"type": "Drillthrough"`.
- The Region filter was correctly marked `"howCreated": "Drillthrough"`.
- The `pageBinding` parameter correctly referenced that filter and `dim_territory[Region]`.
- However, `pageBinding.type` remained `"Default"` instead of `"Drillthrough"`.

Microsoft's PBIR page schema describes `pageBinding.type` as the binding's specific usage and supports `Default`, `Drillthrough`, or `Tooltip`. A page can therefore display a populated Drill-through field well while still not be advertised as a drillthrough destination when the binding itself remains `Default`.

Repair applied:

```json
"pageBinding": {
  "name": "c174dee66ba0c00b911d",
  "type": "Drillthrough",
  "parameters": [
    {
      "boundFilter": "e7b0d138c06f9cf1c5c1",
      "fieldExpr": {
        "Column": {
          "Expression": { "SourceRef": { "Entity": "dim_territory" } },
          "Property": "Region"
        }
      }
    }
  ]
}
```

Verification must check all four layers together: page `type`, filter `howCreated`, `pageBinding.type`, and the binding parameter's `boundFilter`/`fieldExpr`. Checking only the visible Desktop field well or only the page filter is insufficient.

## Regional Trend Tooltip

### Before

- The 320×240 tooltip canvas used two oversized native cards.
- Revenue and YoY text dominated the canvas at tooltip scale.
- The line used categorical `YearMonthName`, all-point labels, and a horizontal scrollbar.
- The title said 12 months, but the query still returned the full available history.

### After

- Added `VIS HTML Tooltip KPI Cards` at `x=10`, `y=10`, `width=300`, `height=60`.
- Hid the two native card visuals with root-level `isHidden: true`.
- Repositioned the line panel to `x=10`, `y=78`, `width=300`, `height=154`.
- Replaced `YearMonthName` with continuous `MonthStart`.
- Rebound the Y field to `$ Revenue Last 12M Tooltip`.
- Removed legend, value axis, data labels, subtitle, and scrollbar.
- Retained a minimal title and blue trend line.

The tooltip-specific measure calculates the final visible month outside the line's current axis point while preserving external hover/filter context:

```DAX
$ Revenue Last 12M Tooltip =
VAR _LastVisibleDate =
    CALCULATE(
        MAX(fact_sales[OrderDate]),
        ALLSELECTED(dim_date)
    )
VAR _LastVisibleMonth =
    DATE(YEAR(_LastVisibleDate), MONTH(_LastVisibleDate), 1)
VAR _FirstVisibleMonth = EDATE(_LastVisibleMonth, -11)
VAR _CurrentMonth = MAX(dim_date[MonthStart])
RETURN
    IF(
        NOT ISBLANK(_LastVisibleDate)
            && _CurrentMonth >= _FirstVisibleMonth
            && _CurrentMonth <= _LastVisibleMonth,
        [$ Total Revenue]
    )
```

### Tooltip assignment requirement

A page with `type: Tooltip` is only an eligible tooltip destination. Each source visual must still be assigned to that report page through its Tooltip formatting setting.

In Desktop:

1. Select the source Region visual.
2. Open `Format visual > General > Tooltips`.
3. Set Type to `Report page`.
4. Select `Regional Trend Tooltip` as Page.
5. Repeat for each regional visual that should show the hover trend.

The corresponding PBIR source-visual metadata uses `visualContainerObjects.visualTooltip` with `show: true` and a `section` reference to the tooltip page. As with drillthrough registration, Desktop assignment is preferred when interaction metadata has not already been generated by Desktop.

Construction lesson: tooltip canvas design and tooltip assignment are separate tasks. A polished hidden Tooltip page does nothing until compatible source visuals explicitly reference it.

## Metric selector architecture

### What Power BI creates

A field parameter is a calculated table. Each row stores:

1. A user-facing label.
2. A `NAMEOF()` reference to the actual measure or column.
3. A sort order.

Current parameter:

```DAX
Metric selector =
{
    ("$ Total Revenue", NAMEOF('formulas'[$ Total Revenue]), 0),
    ("$ Gross Margin", NAMEOF('formulas'[$ Gross Margin]), 1),
    ("# Units Sold", NAMEOF('formulas'[# Units Sold]), 2),
    ("# Orders", NAMEOF('formulas'[# Orders]), 3)
}
```

This produces three columns:

- `Metric selector[Metric selector]`: visible label used by the slicer.
- `Metric selector[Metric selector Fields]`: hidden technical field reference.
- `Metric selector[Metric selector Order]`: hidden sort order.

The visible label and hidden field-reference column form a composite key. That implementation detail caused one of the session's errors.

### How selection flows

```text
User selects a label in the slicer
        ↓
The disconnected parameter table is filtered to one row
        ↓
Selected Metric Value reads that row safely
        ↓
SWITCH returns the corresponding base measure
        ↓
Every data point in the hero line recalculates for that measure
```

The parameter table does not need a relationship to the star schema. The bridge measure reads its filter context and then evaluates a normal model measure.

### Stable bridge measure used in this report

```DAX
Selected Metric Value =
VAR _SelectedParameter =
    SELECTCOLUMNS(
        SUMMARIZE(
            'Metric selector',
            'Metric selector'[Metric selector],
            'Metric selector'[Metric selector Fields]
        ),
        "MetricName", 'Metric selector'[Metric selector]
    )
VAR _Metric =
    IF(
        COUNTROWS(_SelectedParameter) = 1,
        MAXX(_SelectedParameter, [MetricName]),
        "$ Total Revenue"
    )
RETURN
    SWITCH(
        _Metric,
        "$ Total Revenue", [$ Total Revenue],
        "$ Gross Margin", [$ Gross Margin],
        "# Units Sold", [# Units Sold],
        "# Orders", [# Orders],
        [$ Total Revenue]
    )
```

### Why the first implementation failed

#### Failure 1: direct hidden-column binding in PBIR

The hero Y projection was manually bound to:

```text
Metric selector[Metric selector Fields]
```

as though it were a regular column. Power BI attempted to combine the disconnected parameter table with the date axis and returned:

```text
InvalidUnconstrainedJoin
Can't determine relationships between the fields
```

Rule for the future skill: do not serialize a field parameter's hidden field-reference column as an ordinary categorical/value column. Native field-parameter projections contain special metadata that is safer to create through Desktop.

#### Failure 2: `SELECTEDVALUE` on the visible label

The first bridge measure used:

```DAX
SELECTEDVALUE('Metric selector'[Metric selector])
```

Power BI returned:

```text
Column [Metric selector] is part of composite key,
but not all columns of the composite key are included...
```

Rule for the future skill: when reading a field parameter label in DAX, include both the visible label and hidden Fields column in `SUMMARIZE`, then project the label with `SELECTCOLUMNS`.

## Native parameter versus bridge measure

### Native field-parameter binding

Best when building interactively in Power BI Desktop:

- Put the visible parameter column in a slicer.
- Drag the same parameter into the visual's Values/Y well.
- Power BI generates the special projection metadata.
- Each source measure retains its own formatting more naturally.

Risk: direct PBIR JSON authoring is brittle because the hidden Fields column is not a normal data column.

### Slicer plus bridge measure

Best when editing PBIR/TMDL programmatically:

- Keep the parameter table and slicer.
- Put `Selected Metric Value` in the chart.
- Use `SWITCH` to return the selected base measure.
- No model relationship is required.

Tradeoff: mixed units need deliberate formatting. Revenue and margin dollars use currency, while units and orders use counts. A future enhancement should add a dynamic format string or separate selectors by compatible unit family.

## When metric selectors are valuable

Use them when:

- The chart's analytical structure remains the same and only the measure changes.
- The measures share a meaningful axis and comparison grain.
- The selector removes redundant charts without hiding essential simultaneous comparisons.
- The title, subtitle, or dynamic title clearly communicates the active metric.

Good candidates:

- Revenue / Gross Margin / Units / Orders over time.
- Actual / Target / Variance by region.
- Revenue / Margin / Units by product.
- Current period / YoY change / attainment in a reusable ranking view.

Avoid or split selectors when:

- The measures require fundamentally different chart types.
- Currency, percentages, and counts create confusing shared axes.
- Users must compare the measures simultaneously.
- Changing the measure also changes the business question or required reference line.

## Recommended reusable implementation sequence

1. Define the business question shared by all candidate metrics.
2. Keep only measures that make sense with the same category axis and chart type.
3. Create the parameter table with clear labels and deterministic order.
4. Add a single-select slicer using the visible label.
5. Prefer native parameter binding when working in Desktop.
6. Prefer the composite-key-safe bridge measure when editing PBIR/TMDL.
7. Set an explicit default metric and fallback in DAX.
8. Add a dynamic title or subtitle that reflects the selected metric.
9. Verify format strings for currency, percentage, and whole-number metrics.
10. Test single selection, cleared selection, and unexpected multi-selection.

## PBIR/TMDL workflow rules learned

- Close Power BI Desktop before external PBIR/TMDL edits, or close without saving before reopening. An open Desktop session can overwrite external changes.
- Validate every edited `visual.json` after patching.
- Remove stale filter definitions when replacing a projected field.
- When changing a visual field, update projections, query references, sort definitions, and filters together.
- Prefer semantic measures for Top-N and conditional formatting when visual-level filters are difficult to serialize reliably.
- Conditional-format measures should return explicit colors for every intended state; an omitted fallback can leave values unchanged.
- Font-color formatting and background-color formatting are separate visual properties; a correct color measure will do nothing if bound to the wrong property.
- Verify actual rendering in Desktop after PBIR changes. Schema-valid JSON can still express an analytically invalid query.

## Technical construction appendix

This section is intentionally implementation-specific. A future report-construction skill should use these details to diagnose and prevent invalid PBIR/TMDL output, not merely reproduce the visual styling.

### Relevant project topology

```text
03-regional-sales-performance/
└── pbip/
    ├── Regional Sales.pbip
    ├── Regional Sales.Report/
    │   └── definition/
    │       └── pages/
    │           └── dd44ee55ff66aa77bb88/
    │               └── visuals/
    └── Regional Sales.SemanticModel/
        └── definition/
            └── tables/
                ├── formulas.tmdl
                ├── Metric selector.tmdl
                └── dim_date.tmdl
```

Revenue Trend and Seasonality page ID:

```text
dd44ee55ff66aa77bb88
```

Important visual IDs:

| Visual | ID | Type |
|---|---|---|
| Metric selector | `722bd32e71074c418468` | `slicer` |
| Hero trajectory | `c95e69de5a014fee9557` | `lineChart` |
| Seasonality | `d1fc1c065ee54a0e93a1` | `clusteredColumnChart` |
| YTD pace | `3e68d6a721e04a1290d8` | `areaChart` |

### Semantic-model construction

The selector table is stored in:

```text
Regional Sales.SemanticModel/definition/tables/Metric selector.tmdl
```

Its TMDL contains a calculated-table partition:

```tmdl
partition 'Metric selector' = calculated
    mode: import
    source = {
        ("$ Total Revenue", NAMEOF('formulas'[$ Total Revenue]), 0),
        ("$ Gross Margin", NAMEOF('formulas'[$ Gross Margin]), 1),
        ("# Units Sold", NAMEOF('formulas'[# Units Sold]), 2),
        ("# Orders", NAMEOF('formulas'[# Orders]), 3)
    }
```

The visible parameter column includes:

```tmdl
relatedColumnDetails
    groupByColumn: 'Metric selector Fields'
```

That `groupByColumn` declaration is the source of the composite-key behavior. Any DAX expression that tries to reduce the visible column to one scalar must account for the grouped hidden column.

The bridge measure is stored in:

```text
Regional Sales.SemanticModel/definition/tables/formulas.tmdl
```

Technical requirements for the bridge measure:

- It must return a numeric scalar, not `FORMAT()` text, because the result is plotted on a numeric Y axis.
- Its fallback must be a real measure so cleared or invalid slicer states do not blank the chart.
- It must include both composite-key columns when resolving the selected label.
- All returned measures should be compatible with the intended visual grain.
- Its lineage tag must be unique when added directly through TMDL.

### Failed hero projection

The invalid PBIR construction treated the hidden Fields column as a regular Y-axis column:

```json
{
  "field": {
    "Column": {
      "Expression": {
        "SourceRef": {
          "Entity": "Metric selector"
        }
      },
      "Property": "Metric selector Fields"
    }
  },
  "queryRef": "Metric selector.Metric selector Fields",
  "active": true
}
```

The visual also had a filter entry for the same hidden field. With `dim_date[MonthStart]` on Category, the generated query contained fields from two disconnected tables without the special native field-parameter expansion. The result was `InvalidUnconstrainedJoin`.

Construction rule:

```text
Hidden field-parameter reference column ≠ ordinary report column
```

Do not bind it as a normal `Column` projection in handcrafted PBIR.

### Corrected hero projection

The corrected PBIR Y projection points to a semantic measure:

```json
{
  "field": {
    "Measure": {
      "Expression": {
        "SourceRef": {
          "Entity": "formulas"
        }
      },
      "Property": "Selected Metric Value"
    }
  },
  "queryRef": "formulas.Selected Metric Value",
  "nativeQueryRef": "Selected Metric",
  "displayName": "Selected Metric"
}
```

The Category projection remains:

```json
{
  "field": {
    "Column": {
      "Expression": {
        "SourceRef": {
          "Entity": "dim_date"
        }
      },
      "Property": "MonthStart"
    }
  },
  "queryRef": "dim_date.MonthStart",
  "active": true
}
```

The visual's sort definition also uses `dim_date[MonthStart]` ascending. Category, sorting, and filtering must use the same chronological field to avoid lexical month sorting.

### Report-locale correction for continuous date axes

`dim_date[MonthStart]` is intentionally a `dateTime` column so line and combo charts can use a scalar/continuous axis. Its model format is `MMM yyyy`, but the semantic model culture is `es-ES`, which caused English report pages to render labels such as `ene 2024` and `abr 2024`.

Do not replace the date with `FORMAT()` text merely to translate month names; that would sacrifice continuous-axis behavior and chronological scaling. The supported report-layer repair is to set the PBIR report locale:

```json
"settings": {
  "locale": "en-US"
}
```

Microsoft's PBIR report schema defines this property as a report-specific locale that takes precedence over browser and operating-system locale. This keeps `MonthStart` typed as a date while rendering `Jan`, `Apr`, and other English labels consistently across every visual using locale-aware date formatting.

### Stale filter removal

Replacing a projection is insufficient if `filterConfig.filters` still contains the previous field. The hero initially retained a filter object referencing `Metric selector Fields` after the Y projection changed.

Required cleanup:

- Remove the stale hidden-field filter entirely.
- Retain only the valid `dim_date[MonthStart]` filter entry.
- Search the full visual JSON for the old property after patching.

Example verification:

```powershell
rg -n "Metric selector Fields|Selected Metric Value" `
  "Regional Sales.Report/definition/pages/dd44ee55ff66aa77bb88/visuals/c95e69de5a014fee9557/visual.json"
```

Expected result: `Selected Metric Value` appears in the Y projection and `Metric selector Fields` does not appear in the hero visual.

### Composite-key-safe DAX mechanics

The failed expression was:

```DAX
SELECTEDVALUE('Metric selector'[Metric selector], "$ Total Revenue")
```

`SELECTEDVALUE` internally needs to group the selected column. Because the column declares `Metric selector Fields` as a group-by column, the engine rejects an expression that groups only the visible label.

The safe expression first creates a table containing the complete composite identity:

```DAX
VAR _SelectedParameter =
    SELECTCOLUMNS(
        SUMMARIZE(
            'Metric selector',
            'Metric selector'[Metric selector],
            'Metric selector'[Metric selector Fields]
        ),
        "MetricName", 'Metric selector'[Metric selector]
    )
```

Then it explicitly handles cardinality:

```DAX
VAR _Metric =
    IF(
        COUNTROWS(_SelectedParameter) = 1,
        MAXX(_SelectedParameter, [MetricName]),
        "$ Total Revenue"
    )
```

This does three things a future skill should always implement:

- Respects the composite key.
- Protects against no selection.
- Protects against accidental multi-selection.

### Slicer construction details

The slicer itself correctly projects the visible label:

```text
Metric selector[Metric selector]
```

The slicer's internal filter identity can legitimately contain the hidden Fields column because Power BI generated the field-parameter filter metadata. This is different from binding that hidden column to an unrelated visual's Y well.

The slicer currently has approximately:

```json
{
  "x": 17.78,
  "y": 35.56,
  "z": 0,
  "height": 37.22,
  "width": 314.44
}
```

Its low z-order explains why the control can be hidden by header elements. Construction validation must include layer order and rendered visibility, not only query validity.

### Error-signature diagnostic matrix

| Error | Likely cause | Inspection | Corrective action |
|---|---|---|---|
| `InvalidUnconstrainedJoin` | Disconnected parameter field treated as an ordinary column alongside model fields | Inspect projections and filters for `Metric selector Fields` | Bind a real measure or recreate native parameter binding in Desktop |
| Composite-key `QueryUserError` | `SELECTEDVALUE`, `VALUES`, or grouping reads only the visible parameter label | Inspect `relatedColumnDetails/groupByColumn` in parameter TMDL | `SUMMARIZE` visible and Fields columns together, then project the label |
| Visual remains unchanged | Conditional-format measure is not bound to the intended property | Inspect visual objects for data color versus font color | Bind the measure to the correct formatting property using Field value |
| Valid JSON but blank/broken visual | Semantic query is invalid despite schema-valid serialization | Open in Desktop and inspect technical details | Validate field relationships, roles, filters, and aggregation semantics |
| External changes disappear | Desktop saved an older in-memory definition over PBIR/TMDL files | Compare timestamps/diffs after save | Close Desktop before edits; reopen after external patching |

### Conditional-formatting construction pattern

Leader/laggard bar coloring should be based on the current visible context:

```DAX
VAR _CurrentValue = [Metric]
VAR _VisibleItems = ALLSELECTED(Dimension[Category])
VAR _HighestValue =
    MAXX(_VisibleItems, CALCULATE([Metric]))
VAR _LowestValue =
    MINX(
        FILTER(_VisibleItems, NOT ISBLANK(CALCULATE([Metric]))),
        CALCULATE([Metric])
    )
RETURN
    SWITCH(
        TRUE(),
        ISBLANK(_CurrentValue), BLANK(),
        _CurrentValue = _HighestValue, "#C8A84B",
        _CurrentValue = _LowestValue, "#F04444",
        "#1E6FBF"
    )
```

Technical cautions:

- Use `ALLSELECTED`, not `ALL`, when the rank should respond to report slicers.
- Exclude blanks from the minimum calculation or blank categories can become the false laggard.
- Return the middle color explicitly. Returning `BLANK()` does not guarantee preservation of the manually configured blue.
- For Top-N visuals, calculate highest and lowest over the same Top-N table used to display values.
- Bind the color measure through conditional formatting as a field value.
- A font-color measure must be attached to font color; attaching it to background color changes a different property.

### Technical mutation sequence for a future skill

When changing a PBIR visual's field programmatically:

1. Identify the page ID and visual ID.
2. Read the entire `visual.json`, not only the projection fragment.
3. Inventory every occurrence of the old field:
   - Query projections.
   - Sort definitions.
   - `filterConfig` entries.
   - Conditional-formatting expressions.
   - Titles or subtitles that name the old metric.
4. Confirm the replacement semantic object exists in TMDL.
5. If adding a measure, use a unique lineage tag and a valid display folder.
6. Replace the projection with the correct `Column` or `Measure` object type.
7. Update `queryRef`, `nativeQueryRef`, and `displayName` consistently.
8. Remove or update stale filters and sorts.
9. Parse all edited JSON files.
10. Search for residual references to the old field.
11. Reopen the PBIP in Desktop and test actual query execution.
12. Test every slicer state and verify titles, formatting, sorting, and layer visibility.

### Validation boundary

JSON parsing verifies serialization only:

```powershell
Get-Content -Raw visual.json | ConvertFrom-Json | Out-Null
```

It does not verify:

- Model relationships.
- DAX compilation.
- Composite-key constraints.
- Whether a field is valid for a visual role.
- Whether conditional formatting is attached to the correct property.
- Whether a visual is obscured by another layer.

The future skill should therefore distinguish three validation levels:

1. **Serialization validation** — JSON/TMDL structure can be loaded.
2. **Semantic validation** — DAX and generated queries execute against the model.
3. **Rendered validation** — Desktop displays the intended hierarchy, colors, labels, and interactions.

## Proposed additions to `storytelling-designer`

- A before/after visual critique checklist covering message, comparison, clutter, emphasis, and interaction.
- A Power BI field-parameter recipe with native and bridge-measure variants.
- A composite-key warning and the safe `SUMMARIZE`/`SELECTCOLUMNS` pattern.
- An `InvalidUnconstrainedJoin` troubleshooting decision tree.
- Rank-color templates using `ALLSELECTED` for visible-context leader/laggard emphasis.
- Table-formatting guidance: contrast, row density, alignment, negative-value font colors, and exact-number roles.
- A rule to expose and label every interaction control; hidden selectors undermine discoverability.
- A requirement to test cleared and multi-select slicer states.
- A PBIR hygiene checklist covering projections, filters, sorts, field references, JSON validation, and Desktop reload behavior.
