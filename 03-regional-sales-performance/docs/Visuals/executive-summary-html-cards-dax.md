# Executive Summary HTML KPI Cards

Use the measure `VIS HTML Executive KPI Cards` from the `formulas` table in one HTML Content visual spanning the KPI row.

The visual contains three cards:

- Revenue: total revenue, YoY movement, and prior-year revenue.
- Profitability: margin rate, gross margin dollars, and YoY percentage-point movement.
- Target Performance: coverage-aligned attainment, target value, variance, and a capped progress bar.

All HTML card surfaces use `#0E2841` as the project standard.

## Target coverage correction

Targets start in May 2023, while sales start in May 2022. Therefore, all-period attainment must compare the target only with revenue in months that have targets.

```DAX
$ Revenue in Target Period =
VAR _TargetMonths = VALUES(fact_targets[YearMonth])
RETURN
    CALCULATE(
        [$ Total Revenue],
        KEEPFILTERS(TREATAS(_TargetMonths, dim_date[YearMonth]))
    )

$ Variance to Target =
[$ Revenue in Target Period] - [$ Target Revenue]

% Target Attainment =
DIVIDE([$ Revenue in Target Period], [$ Target Revenue])
```

Across the complete dataset, this changes attainment from approximately 172.7% to 137.0%, because the corrected calculation excludes sales months without a corresponding target.

The complete HTML DAX is stored directly in `Regional Sales.SemanticModel/definition/tables/formulas.tmdl` under `8_HTML Visuals`.
