# Chelsea FC HTML Visuals - DAX Measure Library

Paste these measures into the `DAX Measures` table and use them with an HTML Content visual. The styling follows the Chelsea report palette: dark navy background, gold labels/accent borders, white values, muted blue context text, and green/red only for variance.

## Recommended Page Mapping

| Report page | HTML measure |
|---|---|
| Season Overview | `VIS HTML Season Overview Snapshot` |
| Match Performance | `VIS HTML Match Snapshot` |
| Financial Performance | `VIS HTML Financial Snapshot` |
| Transfer Activity | `VIS HTML Transfer Snapshot` |
| Squad & Wages | `VIS HTML Wage Snapshot` |
| Players Market Value | `VIS HTML Squad Value Snapshot` |
| Player Performance | `VIS HTML Player Performance Snapshot` |

## VIS HTML Season Overview Snapshot

Good for `Season Overview`. It combines the core board-level football and finance context for the selected season.

```DAX
VIS HTML Season Overview Snapshot =
VAR _CurrentStartYear = SELECTEDVALUE(dim_season[start_year])
VAR _PrevStartYear = _CurrentStartYear - 1
VAR _HasSingleSeason = NOT ISBLANK(_CurrentStartYear)

VAR _PL = [REF PL Position]
VAR _PLPY =
    IF(
        _HasSingleSeason,
        CALCULATE([REF PL Position], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear)
    )
VAR _PLNum = IFERROR(VALUE(_PL), BLANK())
VAR _PLPYNum = IFERROR(VALUE(_PLPY), BLANK())
VAR _PLMove = _PLPYNum - _PLNum
VAR _PLClass = IF(ISBLANK(_PLMove) || _PLMove >= 0, "pos", "neg")
VAR _PLArrow = IF(ISBLANK(_PLMove), "•", IF(_PLMove >= 0, "↑", "↓"))
VAR _PLMoveFmt = IF(ISBLANK(_PLMove), "—", FORMAT(ABS(_PLMove), "#,##0") & " places")
VAR _PLPYFmt = IF(ISBLANK(_PLPY), "—", _PLPY)

VAR _Points = [# PL Points]
VAR _PointsPY =
    IF(
        _HasSingleSeason,
        CALCULATE([# PL Points], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear)
    )
VAR _PointsG = DIVIDE(_Points - _PointsPY, _PointsPY)
VAR _PointsClass = IF(ISBLANK(_PointsG) || _PointsG >= 0, "pos", "neg")
VAR _PointsArrow = IF(ISBLANK(_PointsG), "•", IF(_PointsG >= 0, "↑", "↓"))
VAR _PointsFmt = FORMAT(_Points, "#,##0")
VAR _PointsPYFmt = IF(ISBLANK(_PointsPY), "—", FORMAT(_PointsPY, "#,##0"))
VAR _PointsGFmt = IF(ISBLANK(_PointsG), "—", FORMAT(ABS(_PointsG), "0.0%"))

VAR _Win = [% Win Rate]
VAR _WinPY =
    IF(
        _HasSingleSeason,
        CALCULATE([% Win Rate], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear)
    )
VAR _WinDelta = _Win - _WinPY
VAR _WinClass = IF(ISBLANK(_WinDelta) || _WinDelta >= 0, "pos", "neg")
VAR _WinArrow = IF(ISBLANK(_WinDelta), "•", IF(_WinDelta >= 0, "↑", "↓"))
VAR _WinFmt = FORMAT(_Win, "0.0%")
VAR _WinPYFmt = IF(ISBLANK(_WinPY), "—", FORMAT(_WinPY, "0.0%"))
VAR _WinGFmt = IF(ISBLANK(_WinDelta), "—", FORMAT(ABS(_WinDelta) * 100, "0.0") & " pp")

VAR _Trophies = [# Trophies Won]
VAR _TrophiesPY =
    IF(
        _HasSingleSeason,
        CALCULATE([# Trophies Won], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear)
    )
VAR _TrophiesDelta = _Trophies - _TrophiesPY
VAR _TrophiesClass = IF(ISBLANK(_TrophiesDelta) || _TrophiesDelta >= 0, "pos", "neg")
VAR _TrophiesArrow = IF(ISBLANK(_TrophiesDelta), "•", IF(_TrophiesDelta >= 0, "↑", "↓"))
VAR _TrophiesFmt = FORMAT(_Trophies, "#,##0")
VAR _TrophiesPYFmt = IF(ISBLANK(_TrophiesPY), "—", FORMAT(_TrophiesPY, "#,##0"))
VAR _TrophiesGFmt = IF(ISBLANK(_TrophiesDelta), "—", FORMAT(ABS(_TrophiesDelta), "#,##0"))

VAR _Net = [$ Net Profit/Loss (£)]
VAR _NetPY =
    IF(
        _HasSingleSeason,
        CALCULATE([$ Net Profit/Loss (£)], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear)
    )
VAR _NetG = DIVIDE(_Net - _NetPY, ABS(_NetPY))
VAR _NetClass = IF(ISBLANK(_NetG) || _NetG >= 0, "pos", "neg")
VAR _NetArrow = IF(ISBLANK(_NetG), "•", IF(_NetG >= 0, "↑", "↓"))
VAR _NetFmt = IF(ABS(_Net) >= 1000000000, "£" & FORMAT(DIVIDE(_Net, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Net, 1000000), "#,##0.0") & "m")
VAR _NetPYFmt = IF(ISBLANK(_NetPY), "—", IF(ABS(_NetPY) >= 1000000000, "£" & FORMAT(DIVIDE(_NetPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_NetPY, 1000000), "#,##0.0") & "m"))
VAR _NetGFmt = IF(ISBLANK(_NetG), "—", FORMAT(ABS(_NetG), "0.0%"))
RETURN
"<style>
.cv{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ci{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.cl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cn{color:#fff;font-size:18px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.cf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.cp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #00A651;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #D62D20;color:#f87171;}
.cy{font-size:10px;color:#7FA4CF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""cv"">
  <div class=""ci""><div class=""cl"">PL Finish</div><div class=""cn"">" & _PL & "</div><div class=""cf""><span class=""cp " & _PLClass & """>" & _PLArrow & " " & _PLMoveFmt & "</span><span class=""cy"">vs PY: " & _PLPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">PL Points</div><div class=""cn"">" & _PointsFmt & "</div><div class=""cf""><span class=""cp " & _PointsClass & """>" & _PointsArrow & " " & _PointsGFmt & "</span><span class=""cy"">vs PY: " & _PointsPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Win Rate</div><div class=""cn"">" & _WinFmt & "</div><div class=""cf""><span class=""cp " & _WinClass & """>" & _WinArrow & " " & _WinGFmt & "</span><span class=""cy"">vs PY: " & _WinPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Trophies</div><div class=""cn"">" & _TrophiesFmt & "</div><div class=""cf""><span class=""cp " & _TrophiesClass & """>" & _TrophiesArrow & " " & _TrophiesGFmt & "</span><span class=""cy"">vs PY: " & _TrophiesPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Net P/L</div><div class=""cn"">" & _NetFmt & "</div><div class=""cf""><span class=""cp " & _NetClass & """>" & _NetArrow & " " & _NetGFmt & "</span><span class=""cy"">vs PY: " & _NetPYFmt & "</span></div></div>
</div>"
```

## VIS HTML Match Snapshot

Good for `Match Performance`. It avoids `Calendar` and calculates previous season directly from `dim_season[start_year]`. Goals scored and conceded are combined into one relationship card, while win rate shows the home/away split.

```DAX
VIS HTML Match Snapshot =
VAR _CurrentStartYear = SELECTEDVALUE(dim_season[start_year])
VAR _PrevStartYear = _CurrentStartYear - 1
VAR _HasSingleSeason = NOT ISBLANK(_CurrentStartYear)

VAR _Points = [# PL Points]
VAR _PointsPY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [# PL Points],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _PointsG = DIVIDE(_Points - _PointsPY, _PointsPY)
VAR _PointsClass = IF(ISBLANK(_PointsG) || _PointsG >= 0, "pos", "neg")
VAR _PointsArrow = IF(ISBLANK(_PointsG), "•", IF(_PointsG >= 0, "↑", "↓"))
VAR _PointsFmt = FORMAT(_Points, "#,##0")
VAR _PointsPYFmt = IF(ISBLANK(_PointsPY), "—", FORMAT(_PointsPY, "#,##0"))
VAR _PointsGFmt = IF(ISBLANK(_PointsG), "—", FORMAT(ABS(_PointsG), "0.0%"))

VAR _Win = [% Win Rate]
VAR _WinPY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [% Win Rate],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _WinDelta = _Win - _WinPY
VAR _WinClass = IF(ISBLANK(_WinDelta) || _WinDelta >= 0, "pos", "neg")
VAR _WinArrow = IF(ISBLANK(_WinDelta), "•", IF(_WinDelta >= 0, "↑", "↓"))
VAR _WinFmt = FORMAT(_Win, "0.0%")
VAR _WinPYFmt = IF(ISBLANK(_WinPY), "—", FORMAT(_WinPY, "0.0%"))
VAR _WinGFmt = IF(ISBLANK(_WinDelta), "—", FORMAT(ABS(_WinDelta) * 100, "0.0") & " pp")
VAR _HomeWinFmt = FORMAT([% Home Win Rate], "0.0%")
VAR _AwayWinFmt = FORMAT([% Away Win Rate], "0.0%")

VAR _GF = [# Goals Scored]
VAR _GA = [# Goals Conceded]
VAR _GD = [# Goal Difference]
VAR _GDClass = IF(_GD >= 0, "pos", "neg")
VAR _GDFmt = IF(_GD > 0, "+" & FORMAT(_GD, "#,##0"), FORMAT(_GD, "#,##0"))
VAR _GoalsFmt = FORMAT(_GF, "#,##0") & " / " & FORMAT(_GA, "#,##0")
VAR _AvgGoalsFmt = FORMAT([# Avg Goals Scored], "0.0") & " for · " & FORMAT([# Avg Goals Conceded], "0.0") & " against"

VAR _Attendance = [# Avg Home Attendance]
VAR _AttendancePY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [# Avg Home Attendance],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _AttendanceG = DIVIDE(_Attendance - _AttendancePY, _AttendancePY)
VAR _AttendanceClass = IF(ISBLANK(_AttendanceG) || _AttendanceG >= 0, "pos", "neg")
VAR _AttendanceArrow = IF(ISBLANK(_AttendanceG), "•", IF(_AttendanceG >= 0, "↑", "↓"))
VAR _AttendanceFmt = FORMAT(_Attendance, "#,##0")
VAR _AttendancePYFmt = IF(ISBLANK(_AttendancePY), "—", FORMAT(_AttendancePY, "#,##0"))
VAR _AttendanceGFmt = IF(ISBLANK(_AttendanceG), "—", FORMAT(ABS(_AttendanceG), "0.0%"))
RETURN
"<style>
.cv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ci{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.cl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cn{color:#fff;font-size:20px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.cs{display:flex;align-items:center;gap:8px;color:#7FA4CF;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cs b{color:#fff;font-weight:700;}
.cf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.cp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #00A651;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #D62D20;color:#f87171;}
.cy{font-size:10px;color:#7FA4CF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""cv"">
  <div class=""ci""><div class=""cl"">PL Points</div><div class=""cn"">" & _PointsFmt & "</div><div class=""cf""><span class=""cp " & _PointsClass & """>" & _PointsArrow & " " & _PointsGFmt & "</span><span class=""cy"">vs PY: " & _PointsPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Win Rate</div><div class=""cn"">" & _WinFmt & "</div><div class=""cs""><span>H <b>" & _HomeWinFmt & "</b></span><span>A <b>" & _AwayWinFmt & "</b></span></div><div class=""cf""><span class=""cp " & _WinClass & """>" & _WinArrow & " " & _WinGFmt & "</span><span class=""cy"">vs PY: " & _WinPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Goals For / Against</div><div class=""cn"">" & _GoalsFmt & "</div><div class=""cs"">" & _AvgGoalsFmt & "</div><div class=""cf""><span class=""cp " & _GDClass & """>GD " & _GDFmt & "</span><span class=""cy"">scored / conceded</span></div></div>
  <div class=""ci""><div class=""cl"">Avg Home Attendance</div><div class=""cn"">" & _AttendanceFmt & "</div><div class=""cf""><span class=""cp " & _AttendanceClass & """>" & _AttendanceArrow & " " & _AttendanceGFmt & "</span><span class=""cy"">vs PY: " & _AttendancePYFmt & "</span></div></div>
</div>"
```

## VIS HTML Financial Snapshot

Good for `Financial Sustainability`. Cost increase and wage-ratio increase are treated as negative movement.

```DAX
VIS HTML Financial Snapshot =
VAR _PrevStartYear = CALCULATE(MIN(dim_season[start_year]), ALLSELECTED(dim_season)) - 1

VAR _Rev = [$ Total Revenue (£)]
VAR _RevPY = CALCULATE([$ Total Revenue (£)], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _RevG = DIVIDE(_Rev - _RevPY, _RevPY)
VAR _RevClass = IF(ISBLANK(_RevG) || _RevG >= 0, "pos", "neg")
VAR _RevArrow = IF(ISBLANK(_RevG), "•", IF(_RevG >= 0, "↑", "↓"))
VAR _RevFmt = IF(ABS(_Rev) >= 1000000000, "£" & FORMAT(DIVIDE(_Rev, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Rev, 1000000), "#,##0.0") & "m")
VAR _RevPYFmt = IF(ISBLANK(_RevPY), "—", IF(ABS(_RevPY) >= 1000000000, "£" & FORMAT(DIVIDE(_RevPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_RevPY, 1000000), "#,##0.0") & "m"))
VAR _RevGFmt = IF(ISBLANK(_RevG), "—", FORMAT(ABS(_RevG), "0.0%"))

VAR _Cost = [$ Total Cost (£)]
VAR _CostPY = CALCULATE([$ Total Cost (£)], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _CostG = DIVIDE(_Cost - _CostPY, _CostPY)
VAR _CostClass = IF(ISBLANK(_CostG) || _CostG <= 0, "pos", "neg")
VAR _CostArrow = IF(ISBLANK(_CostG), "•", IF(_CostG >= 0, "↑", "↓"))
VAR _CostFmt = IF(ABS(_Cost) >= 1000000000, "£" & FORMAT(DIVIDE(_Cost, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Cost, 1000000), "#,##0.0") & "m")
VAR _CostPYFmt = IF(ISBLANK(_CostPY), "—", IF(ABS(_CostPY) >= 1000000000, "£" & FORMAT(DIVIDE(_CostPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_CostPY, 1000000), "#,##0.0") & "m"))
VAR _CostGFmt = IF(ISBLANK(_CostG), "—", FORMAT(ABS(_CostG), "0.0%"))

VAR _Net = [$ Net Profit/Loss (£)]
VAR _NetPY = CALCULATE([$ Net Profit/Loss (£)], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _NetG = DIVIDE(_Net - _NetPY, ABS(_NetPY))
VAR _NetClass = IF(ISBLANK(_NetG) || _NetG >= 0, "pos", "neg")
VAR _NetArrow = IF(ISBLANK(_NetG), "•", IF(_NetG >= 0, "↑", "↓"))
VAR _NetFmt = IF(ABS(_Net) >= 1000000000, "£" & FORMAT(DIVIDE(_Net, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Net, 1000000), "#,##0.0") & "m")
VAR _NetPYFmt = IF(ISBLANK(_NetPY), "—", IF(ABS(_NetPY) >= 1000000000, "£" & FORMAT(DIVIDE(_NetPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_NetPY, 1000000), "#,##0.0") & "m"))
VAR _NetGFmt = IF(ISBLANK(_NetG), "—", FORMAT(ABS(_NetG), "0.0%"))

VAR _Wage = [% Wage to Revenue Ratio]
VAR _WagePY = CALCULATE([% Wage to Revenue Ratio], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _WageDelta = _Wage - _WagePY
VAR _WageClass = IF(ISBLANK(_WageDelta) || _WageDelta <= 0, "pos", "neg")
VAR _WageArrow = IF(ISBLANK(_WageDelta), "•", IF(_WageDelta >= 0, "↑", "↓"))
VAR _WageFmt = FORMAT(_Wage, "0.0%")
VAR _WagePYFmt = IF(ISBLANK(_WagePY), "—", FORMAT(_WagePY, "0.0%"))
VAR _WageGFmt = IF(ISBLANK(_WageDelta), "—", FORMAT(ABS(_WageDelta) * 100, "0.0") & " pp")
RETURN
"<style>
.cv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ci{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.cl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cn{color:#fff;font-size:20px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.cf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.cp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #00A651;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #D62D20;color:#f87171;}
.cy{font-size:10px;color:#7FA4CF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""cv"">
  <div class=""ci""><div class=""cl"">Revenue</div><div class=""cn"">" & _RevFmt & "</div><div class=""cf""><span class=""cp " & _RevClass & """>" & _RevArrow & " " & _RevGFmt & "</span><span class=""cy"">vs PY: " & _RevPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Total Cost</div><div class=""cn"">" & _CostFmt & "</div><div class=""cf""><span class=""cp " & _CostClass & """>" & _CostArrow & " " & _CostGFmt & "</span><span class=""cy"">vs PY: " & _CostPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Net P/L</div><div class=""cn"">" & _NetFmt & "</div><div class=""cf""><span class=""cp " & _NetClass & """>" & _NetArrow & " " & _NetGFmt & "</span><span class=""cy"">vs PY: " & _NetPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Wage / Revenue</div><div class=""cn"">" & _WageFmt & "</div><div class=""cf""><span class=""cp " & _WageClass & """>" & _WageArrow & " " & _WageGFmt & "</span><span class=""cy"">vs PY: " & _WagePYFmt & "</span></div></div>
</div>"
```

## VIS HTML Transfer Snapshot

Good for `Transfer Market ROI`. It uses `dim_season[start_year]` for previous-season comparisons. Spend and net spend increases are treated as negative movement; income and transfer activity increases are treated as positive context.

```DAX
VIS HTML Transfer Snapshot =
VAR _CurrentStartYear = SELECTEDVALUE(dim_season[start_year])
VAR _PrevStartYear = _CurrentStartYear - 1
VAR _HasSingleSeason = NOT ISBLANK(_CurrentStartYear)

VAR _Spend = [$ Total Transfer Spend (£)]
VAR _SpendPY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [$ Total Transfer Spend (£)],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _SpendG = DIVIDE(_Spend - _SpendPY, ABS(_SpendPY))
VAR _SpendClass = IF(ISBLANK(_SpendG) || _SpendG <= 0, "pos", "neg")
VAR _SpendArrow = IF(ISBLANK(_SpendG), "•", IF(_SpendG >= 0, "↑", "↓"))
VAR _SpendFmt = IF(ABS(_Spend) >= 1000000000, "£" & FORMAT(DIVIDE(_Spend, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Spend, 1000000), "#,##0.0") & "m")
VAR _SpendPYFmt = IF(ISBLANK(_SpendPY), "—", IF(ABS(_SpendPY) >= 1000000000, "£" & FORMAT(DIVIDE(_SpendPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_SpendPY, 1000000), "#,##0.0") & "m"))
VAR _SpendGFmt = IF(ISBLANK(_SpendG), "—", FORMAT(ABS(_SpendG), "0.0%"))

VAR _Income = [$ Total Transfer Income (£)]
VAR _IncomePY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [$ Total Transfer Income (£)],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _IncomeG = DIVIDE(_Income - _IncomePY, ABS(_IncomePY))
VAR _IncomeClass = IF(ISBLANK(_IncomeG) || _IncomeG >= 0, "pos", "neg")
VAR _IncomeArrow = IF(ISBLANK(_IncomeG), "•", IF(_IncomeG >= 0, "↑", "↓"))
VAR _IncomeFmt = IF(ABS(_Income) >= 1000000000, "£" & FORMAT(DIVIDE(_Income, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Income, 1000000), "#,##0.0") & "m")
VAR _IncomePYFmt = IF(ISBLANK(_IncomePY), "—", IF(ABS(_IncomePY) >= 1000000000, "£" & FORMAT(DIVIDE(_IncomePY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_IncomePY, 1000000), "#,##0.0") & "m"))
VAR _IncomeGFmt = IF(ISBLANK(_IncomeG), "—", FORMAT(ABS(_IncomeG), "0.0%"))

VAR _Net = [$ Net Transfer Spend (£)]
VAR _NetPY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [$ Net Transfer Spend (£)],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _NetG = DIVIDE(_Net - _NetPY, ABS(_NetPY))
VAR _NetClass = IF(ISBLANK(_NetG) || _NetG <= 0, "pos", "neg")
VAR _NetArrow = IF(ISBLANK(_NetG), "•", IF(_NetG >= 0, "↑", "↓"))
VAR _NetFmt = IF(ABS(_Net) >= 1000000000, "£" & FORMAT(DIVIDE(_Net, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Net, 1000000), "#,##0.0") & "m")
VAR _NetPYFmt = IF(ISBLANK(_NetPY), "—", IF(ABS(_NetPY) >= 1000000000, "£" & FORMAT(DIVIDE(_NetPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_NetPY, 1000000), "#,##0.0") & "m"))
VAR _NetGFmt = IF(ISBLANK(_NetG), "—", FORMAT(ABS(_NetG), "0.0%"))

VAR _In = [# Total Transfers IN]
VAR _InPY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [# Total Transfers IN],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _InG = DIVIDE(_In - _InPY, ABS(_InPY))
VAR _InClass = IF(ISBLANK(_InG) || _InG >= 0, "pos", "neg")
VAR _InArrow = IF(ISBLANK(_InG), "•", IF(_InG >= 0, "↑", "↓"))
VAR _InFmt = FORMAT(_In, "#,##0")
VAR _InPYFmt = IF(ISBLANK(_InPY), "—", FORMAT(_InPY, "#,##0"))
VAR _InGFmt = IF(ISBLANK(_InG), "—", FORMAT(ABS(_InG), "0.0%"))

VAR _Out = [# Total Transfers OUT]
VAR _OutPY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [# Total Transfers OUT],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _OutG = DIVIDE(_Out - _OutPY, ABS(_OutPY))
VAR _OutClass = IF(ISBLANK(_OutG) || _OutG >= 0, "pos", "neg")
VAR _OutArrow = IF(ISBLANK(_OutG), "•", IF(_OutG >= 0, "↑", "↓"))
VAR _OutFmt = FORMAT(_Out, "#,##0")
VAR _OutPYFmt = IF(ISBLANK(_OutPY), "—", FORMAT(_OutPY, "#,##0"))
VAR _OutGFmt = IF(ISBLANK(_OutG), "—", FORMAT(ABS(_OutG), "0.0%"))

VAR _Flow = _In - _Out
VAR _FlowFmt = IF(_Flow > 0, "+" & FORMAT(_Flow, "#,##0"), FORMAT(_Flow, "#,##0"))
VAR _ActivityFmt = _InFmt & " / " & _OutFmt

VAR _Ratio = [$ Value vs Fee Ratio]
VAR _RatioPY =
    IF(
        _HasSingleSeason,
        CALCULATE(
            [$ Value vs Fee Ratio],
            REMOVEFILTERS(dim_season),
            dim_season[start_year] = _PrevStartYear
        )
    )
VAR _RatioG = DIVIDE(_Ratio - _RatioPY, ABS(_RatioPY))
VAR _RatioClass = IF(ISBLANK(_RatioG) || _RatioG >= 0, "pos", "neg")
VAR _RatioArrow = IF(ISBLANK(_RatioG), "•", IF(_RatioG >= 0, "↑", "↓"))
VAR _RatioFmt = FORMAT(_Ratio, "0.00") & "x"
VAR _RatioPYFmt = IF(ISBLANK(_RatioPY), "—", FORMAT(_RatioPY, "0.00") & "x")
VAR _RatioGFmt = IF(ISBLANK(_RatioG), "—", FORMAT(ABS(_RatioG), "0.0%"))
RETURN
"<style>
.cv{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ci{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.cl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cn{color:#fff;font-size:18px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.cf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.cp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #00A651;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #D62D20;color:#f87171;}
.neu{background:#172a43;border:1px solid #416f9f;color:#9cc5ee;}
.cy{font-size:10px;color:#7FA4CF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""cv"">
  <div class=""ci""><div class=""cl"">Transfer Spend</div><div class=""cn"">" & _SpendFmt & "</div><div class=""cf""><span class=""cp " & _SpendClass & """>" & _SpendArrow & " " & _SpendGFmt & "</span><span class=""cy"">vs PY: " & _SpendPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Transfer Income</div><div class=""cn"">" & _IncomeFmt & "</div><div class=""cf""><span class=""cp " & _IncomeClass & """>" & _IncomeArrow & " " & _IncomeGFmt & "</span><span class=""cy"">vs PY: " & _IncomePYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Net Spend</div><div class=""cn"">" & _NetFmt & "</div><div class=""cf""><span class=""cp " & _NetClass & """>" & _NetArrow & " " & _NetGFmt & "</span><span class=""cy"">vs PY: " & _NetPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Transfers IN / OUT</div><div class=""cn"">" & _ActivityFmt & "</div><div class=""cf""><span class=""cp neu"">Net " & _FlowFmt & "</span><span class=""cy"">in / out</span></div></div>
  <div class=""ci""><div class=""cl"">Value / Fee</div><div class=""cn"">" & _RatioFmt & "</div><div class=""cf""><span class=""cp " & _RatioClass & """>" & _RatioArrow & " " & _RatioGFmt & "</span><span class=""cy"">vs PY: " & _RatioPYFmt & "</span></div></div>
</div>"
```

## VIS HTML Squad Value Snapshot

Good for `Squad Market Value`. All four measures treat upward movement as positive.

```DAX
VIS HTML Squad Value Snapshot =
VAR _PrevStartYear = CALCULATE(MIN(dim_season[start_year]), ALLSELECTED(dim_season)) - 1

VAR _Squad = [$ Squad Market Value (£)]
VAR _SquadPY = CALCULATE([$ Squad Market Value (£)], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _SquadG = DIVIDE(_Squad - _SquadPY, _SquadPY)
VAR _SquadClass = IF(ISBLANK(_SquadG) || _SquadG >= 0, "pos", "neg")
VAR _SquadArrow = IF(ISBLANK(_SquadG), "•", IF(_SquadG >= 0, "↑", "↓"))
VAR _SquadFmt = IF(ABS(_Squad) >= 1000000000, "£" & FORMAT(DIVIDE(_Squad, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Squad, 1000000), "#,##0.0") & "m")
VAR _SquadPYFmt = IF(ISBLANK(_SquadPY), "—", IF(ABS(_SquadPY) >= 1000000000, "£" & FORMAT(DIVIDE(_SquadPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_SquadPY, 1000000), "#,##0.0") & "m"))
VAR _SquadGFmt = IF(ISBLANK(_SquadG), "—", FORMAT(ABS(_SquadG), "0.0%"))

VAR _Avg = [$ Avg Player Market Value (£)]
VAR _AvgPY = CALCULATE([$ Avg Player Market Value (£)], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _AvgG = DIVIDE(_Avg - _AvgPY, _AvgPY)
VAR _AvgClass = IF(ISBLANK(_AvgG) || _AvgG >= 0, "pos", "neg")
VAR _AvgArrow = IF(ISBLANK(_AvgG), "•", IF(_AvgG >= 0, "↑", "↓"))
VAR _AvgFmt = "£" & FORMAT(DIVIDE(_Avg, 1000000), "#,##0.0") & "m"
VAR _AvgPYFmt = IF(ISBLANK(_AvgPY), "—", "£" & FORMAT(DIVIDE(_AvgPY, 1000000), "#,##0.0") & "m")
VAR _AvgGFmt = IF(ISBLANK(_AvgG), "—", FORMAT(ABS(_AvgG), "0.0%"))

VAR _High = [$ Highest Player Market Value (£)]
VAR _HighPY = CALCULATE([$ Highest Player Market Value (£)], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _HighG = DIVIDE(_High - _HighPY, _HighPY)
VAR _HighClass = IF(ISBLANK(_HighG) || _HighG >= 0, "pos", "neg")
VAR _HighArrow = IF(ISBLANK(_HighG), "•", IF(_HighG >= 0, "↑", "↓"))
VAR _HighFmt = "£" & FORMAT(DIVIDE(_High, 1000000), "#,##0.0") & "m"
VAR _HighPYFmt = IF(ISBLANK(_HighPY), "—", "£" & FORMAT(DIVIDE(_HighPY, 1000000), "#,##0.0") & "m")
VAR _HighGFmt = IF(ISBLANK(_HighG), "—", FORMAT(ABS(_HighG), "0.0%"))

VAR _Players = [# Players Tracked]
VAR _PlayersPY = CALCULATE([# Players Tracked], FILTER(ALL(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _PlayersG = DIVIDE(_Players - _PlayersPY, _PlayersPY)
VAR _PlayersClass = IF(ISBLANK(_PlayersG) || _PlayersG >= 0, "pos", "neg")
VAR _PlayersArrow = IF(ISBLANK(_PlayersG), "•", IF(_PlayersG >= 0, "↑", "↓"))
VAR _PlayersFmt = FORMAT(_Players, "#,##0")
VAR _PlayersPYFmt = IF(ISBLANK(_PlayersPY), "—", FORMAT(_PlayersPY, "#,##0"))
VAR _PlayersGFmt = IF(ISBLANK(_PlayersG), "—", FORMAT(ABS(_PlayersG), "0.0%"))
RETURN
"<style>
.cv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ci{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.cl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cn{color:#fff;font-size:20px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.cf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.cp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #00A651;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #D62D20;color:#f87171;}
.cy{font-size:10px;color:#7FA4CF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""cv"">
  <div class=""ci""><div class=""cl"">Squad Value</div><div class=""cn"">" & _SquadFmt & "</div><div class=""cf""><span class=""cp " & _SquadClass & """>" & _SquadArrow & " " & _SquadGFmt & "</span><span class=""cy"">vs PY: " & _SquadPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Avg Player Value</div><div class=""cn"">" & _AvgFmt & "</div><div class=""cf""><span class=""cp " & _AvgClass & """>" & _AvgArrow & " " & _AvgGFmt & "</span><span class=""cy"">vs PY: " & _AvgPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Highest Value</div><div class=""cn"">" & _HighFmt & "</div><div class=""cf""><span class=""cp " & _HighClass & """>" & _HighArrow & " " & _HighGFmt & "</span><span class=""cy"">vs PY: " & _HighPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Players Tracked</div><div class=""cn"">" & _PlayersFmt & "</div><div class=""cf""><span class=""cp " & _PlayersClass & """>" & _PlayersArrow & " " & _PlayersGFmt & "</span><span class=""cy"">vs PY: " & _PlayersPYFmt & "</span></div></div>
</div>"
```

## VIS HTML Wage Snapshot

Good for `Squad & Wages`. Wage bill, wage/revenue ratio, and wage per appearance treat increases as negative movement because they signal higher cost pressure.

```DAX
VIS HTML Wage Snapshot =
VAR _CurrentStartYear = SELECTEDVALUE(dim_season[start_year])
VAR _PrevStartYear = _CurrentStartYear - 1
VAR _HasSingleSeason = NOT ISBLANK(_CurrentStartYear)

VAR _Annual = [$ Total Annual Wage Bill (£)]
VAR _AnnualPY = IF(_HasSingleSeason, CALCULATE([$ Total Annual Wage Bill (£)], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _AnnualG = DIVIDE(_Annual - _AnnualPY, ABS(_AnnualPY))
VAR _AnnualClass = IF(ISBLANK(_AnnualG) || _AnnualG <= 0, "pos", "neg")
VAR _AnnualArrow = IF(ISBLANK(_AnnualG), "•", IF(_AnnualG >= 0, "↑", "↓"))
VAR _AnnualFmt = IF(ABS(_Annual) >= 1000000000, "£" & FORMAT(DIVIDE(_Annual, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_Annual, 1000000), "#,##0.0") & "m")
VAR _AnnualPYFmt = IF(ISBLANK(_AnnualPY), "—", IF(ABS(_AnnualPY) >= 1000000000, "£" & FORMAT(DIVIDE(_AnnualPY, 1000000000), "0.00") & "bn", "£" & FORMAT(DIVIDE(_AnnualPY, 1000000), "#,##0.0") & "m"))
VAR _AnnualGFmt = IF(ISBLANK(_AnnualG), "—", FORMAT(ABS(_AnnualG), "0.0%"))

VAR _Weekly = [$ Avg Weekly Wage Bill (£)]
VAR _WeeklyPY = IF(_HasSingleSeason, CALCULATE([$ Avg Weekly Wage Bill (£)], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _WeeklyG = DIVIDE(_Weekly - _WeeklyPY, ABS(_WeeklyPY))
VAR _WeeklyClass = IF(ISBLANK(_WeeklyG) || _WeeklyG <= 0, "pos", "neg")
VAR _WeeklyArrow = IF(ISBLANK(_WeeklyG), "•", IF(_WeeklyG >= 0, "↑", "↓"))
VAR _WeeklyFmt = "£" & FORMAT(DIVIDE(_Weekly, 1000), "#,##0.0") & "k"
VAR _WeeklyPYFmt = IF(ISBLANK(_WeeklyPY), "—", "£" & FORMAT(DIVIDE(_WeeklyPY, 1000), "#,##0.0") & "k")
VAR _WeeklyGFmt = IF(ISBLANK(_WeeklyG), "—", FORMAT(ABS(_WeeklyG), "0.0%"))

VAR _Ratio = [% Wage to Revenue Ratio]
VAR _RatioPY = IF(_HasSingleSeason, CALCULATE([% Wage to Revenue Ratio], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _RatioDelta = _Ratio - _RatioPY
VAR _RatioClass = IF(ISBLANK(_RatioDelta) || _RatioDelta <= 0, "pos", "neg")
VAR _RatioArrow = IF(ISBLANK(_RatioDelta), "•", IF(_RatioDelta >= 0, "↑", "↓"))
VAR _RatioFmt = FORMAT(_Ratio, "0.0%")
VAR _RatioPYFmt = IF(ISBLANK(_RatioPY), "—", FORMAT(_RatioPY, "0.0%"))
VAR _RatioGFmt = IF(ISBLANK(_RatioDelta), "—", FORMAT(ABS(_RatioDelta) * 100, "0.0") & " pp")

VAR _PerApp = [$ Wage per Appearance (£)]
VAR _PerAppPY = IF(_HasSingleSeason, CALCULATE([$ Wage per Appearance (£)], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _PerAppG = DIVIDE(_PerApp - _PerAppPY, ABS(_PerAppPY))
VAR _PerAppClass = IF(ISBLANK(_PerAppG) || _PerAppG <= 0, "pos", "neg")
VAR _PerAppArrow = IF(ISBLANK(_PerAppG), "•", IF(_PerAppG >= 0, "↑", "↓"))
VAR _PerAppFmt = "£" & FORMAT(DIVIDE(_PerApp, 1000), "#,##0.0") & "k"
VAR _PerAppPYFmt = IF(ISBLANK(_PerAppPY), "—", "£" & FORMAT(DIVIDE(_PerAppPY, 1000), "#,##0.0") & "k")
VAR _PerAppGFmt = IF(ISBLANK(_PerAppG), "—", FORMAT(ABS(_PerAppG), "0.0%"))

VAR _Highest = IF(ISBLANK([$ Highest Paid Player (£)]), "—", [$ Highest Paid Player (£)])
RETURN
"<style>
.cv{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ci{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.cl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cn{color:#fff;font-size:18px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.cf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.cp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #00A651;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #D62D20;color:#f87171;}
.neu{background:#172a43;border:1px solid #416f9f;color:#9cc5ee;}
.cy{font-size:10px;color:#7FA4CF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""cv"">
  <div class=""ci""><div class=""cl"">Annual Wage Bill</div><div class=""cn"">" & _AnnualFmt & "</div><div class=""cf""><span class=""cp " & _AnnualClass & """>" & _AnnualArrow & " " & _AnnualGFmt & "</span><span class=""cy"">vs PY: " & _AnnualPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Avg Weekly Wage</div><div class=""cn"">" & _WeeklyFmt & "</div><div class=""cf""><span class=""cp " & _WeeklyClass & """>" & _WeeklyArrow & " " & _WeeklyGFmt & "</span><span class=""cy"">vs PY: " & _WeeklyPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Wage / Revenue</div><div class=""cn"">" & _RatioFmt & "</div><div class=""cf""><span class=""cp " & _RatioClass & """>" & _RatioArrow & " " & _RatioGFmt & "</span><span class=""cy"">vs PY: " & _RatioPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Wage / Appearance</div><div class=""cn"">" & _PerAppFmt & "</div><div class=""cf""><span class=""cp " & _PerAppClass & """>" & _PerAppArrow & " " & _PerAppGFmt & "</span><span class=""cy"">vs PY: " & _PerAppPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Highest Paid</div><div class=""cn"">" & _Highest & "</div><div class=""cf""><span class=""cp neu"">player</span><span class=""cy"">current selection</span></div></div>
</div>"
```

## VIS HTML Player Performance Snapshot

Good for `Player Performance`. It uses season-grain previous-season comparisons for attacking output, rating, and pass accuracy.

```DAX
VIS HTML Player Performance Snapshot =
VAR _CurrentStartYear = SELECTEDVALUE(dim_season[start_year])
VAR _PrevStartYear = _CurrentStartYear - 1
VAR _HasSingleSeason = NOT ISBLANK(_CurrentStartYear)

VAR _Goals = [# Total Goals]
VAR _GoalsPY = IF(_HasSingleSeason, CALCULATE([# Total Goals], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _GoalsG = DIVIDE(_Goals - _GoalsPY, ABS(_GoalsPY))
VAR _GoalsClass = IF(ISBLANK(_GoalsG) || _GoalsG >= 0, "pos", "neg")
VAR _GoalsArrow = IF(ISBLANK(_GoalsG), "•", IF(_GoalsG >= 0, "↑", "↓"))
VAR _GoalsFmt = FORMAT(_Goals, "#,##0")
VAR _GoalsPYFmt = IF(ISBLANK(_GoalsPY), "—", FORMAT(_GoalsPY, "#,##0"))
VAR _GoalsGFmt = IF(ISBLANK(_GoalsG), "—", FORMAT(ABS(_GoalsG), "0.0%"))

VAR _Assists = [# Total Assists]
VAR _AssistsPY = IF(_HasSingleSeason, CALCULATE([# Total Assists], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _AssistsG = DIVIDE(_Assists - _AssistsPY, ABS(_AssistsPY))
VAR _AssistsClass = IF(ISBLANK(_AssistsG) || _AssistsG >= 0, "pos", "neg")
VAR _AssistsArrow = IF(ISBLANK(_AssistsG), "•", IF(_AssistsG >= 0, "↑", "↓"))
VAR _AssistsFmt = FORMAT(_Assists, "#,##0")
VAR _AssistsPYFmt = IF(ISBLANK(_AssistsPY), "—", FORMAT(_AssistsPY, "#,##0"))
VAR _AssistsGFmt = IF(ISBLANK(_AssistsG), "—", FORMAT(ABS(_AssistsG), "0.0%"))

VAR _GC = [# Total Goal Contributions]
VAR _GCPY = IF(_HasSingleSeason, CALCULATE([# Total Goal Contributions], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _GCG = DIVIDE(_GC - _GCPY, ABS(_GCPY))
VAR _GCClass = IF(ISBLANK(_GCG) || _GCG >= 0, "pos", "neg")
VAR _GCArrow = IF(ISBLANK(_GCG), "•", IF(_GCG >= 0, "↑", "↓"))
VAR _GCFmt = FORMAT(_GC, "#,##0")
VAR _GCPYFmt = IF(ISBLANK(_GCPY), "—", FORMAT(_GCPY, "#,##0"))
VAR _GCGFmt = IF(ISBLANK(_GCG), "—", FORMAT(ABS(_GCG), "0.0%"))

VAR _Rating = [# Avg Player Rating]
VAR _RatingPY = IF(_HasSingleSeason, CALCULATE([# Avg Player Rating], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _RatingDelta = _Rating - _RatingPY
VAR _RatingClass = IF(ISBLANK(_RatingDelta) || _RatingDelta >= 0, "pos", "neg")
VAR _RatingArrow = IF(ISBLANK(_RatingDelta), "•", IF(_RatingDelta >= 0, "↑", "↓"))
VAR _RatingFmt = FORMAT(_Rating, "0.00")
VAR _RatingPYFmt = IF(ISBLANK(_RatingPY), "—", FORMAT(_RatingPY, "0.00"))
VAR _RatingGFmt = IF(ISBLANK(_RatingDelta), "—", FORMAT(ABS(_RatingDelta), "0.00"))
VAR _Apps = [# Total Appearances]
VAR _AppsPY = IF(_HasSingleSeason, CALCULATE([# Total Appearances], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _AppsFmt = FORMAT(_Apps, "#,##0")
VAR _AppsPYFmt = IF(ISBLANK(_AppsPY), "—", FORMAT(_AppsPY, "#,##0"))

VAR _Pass = [% Avg Pass Accuracy]
VAR _PassPY = IF(_HasSingleSeason, CALCULATE([% Avg Pass Accuracy], REMOVEFILTERS(dim_season), dim_season[start_year] = _PrevStartYear))
VAR _PassRate = DIVIDE(_Pass, IF(_Pass > 1, 100, 1))
VAR _PassPYRate = DIVIDE(_PassPY, IF(_PassPY > 1, 100, 1))
VAR _PassDelta = _PassRate - _PassPYRate
VAR _PassClass = IF(ISBLANK(_PassDelta) || _PassDelta >= 0, "pos", "neg")
VAR _PassArrow = IF(ISBLANK(_PassDelta), "•", IF(_PassDelta >= 0, "↑", "↓"))
VAR _PassFmt = FORMAT(_PassRate, "0.0%")
VAR _PassPYFmt = IF(ISBLANK(_PassPY), "—", FORMAT(_PassPYRate, "0.0%"))
VAR _PassGFmt = IF(ISBLANK(_PassDelta), "—", FORMAT(ABS(_PassDelta) * 100, "0.0") & " pp")
RETURN
"<style>
.cv{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ci{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.cl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cn{color:#fff;font-size:18px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.cs{color:#7FA4CF;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.cf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.cp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #00A651;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #D62D20;color:#f87171;}
.cy{font-size:10px;color:#7FA4CF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""cv"">
  <div class=""ci""><div class=""cl"">Goals</div><div class=""cn"">" & _GoalsFmt & "</div><div class=""cf""><span class=""cp " & _GoalsClass & """>" & _GoalsArrow & " " & _GoalsGFmt & "</span><span class=""cy"">vs PY: " & _GoalsPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Assists</div><div class=""cn"">" & _AssistsFmt & "</div><div class=""cf""><span class=""cp " & _AssistsClass & """>" & _AssistsArrow & " " & _AssistsGFmt & "</span><span class=""cy"">vs PY: " & _AssistsPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Goal Contributions</div><div class=""cn"">" & _GCFmt & "</div><div class=""cf""><span class=""cp " & _GCClass & """>" & _GCArrow & " " & _GCGFmt & "</span><span class=""cy"">vs PY: " & _GCPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Avg Rating</div><div class=""cn"">" & _RatingFmt & "</div><div class=""cs"">Apps: " & _AppsFmt & " · vs PY: " & _AppsPYFmt & "</div><div class=""cf""><span class=""cp " & _RatingClass & """>" & _RatingArrow & " " & _RatingGFmt & "</span><span class=""cy"">vs PY: " & _RatingPYFmt & "</span></div></div>
  <div class=""ci""><div class=""cl"">Pass Accuracy</div><div class=""cn"">" & _PassFmt & "</div><div class=""cf""><span class=""cp " & _PassClass & """>" & _PassArrow & " " & _PassGFmt & "</span><span class=""cy"">vs PY: " & _PassPYFmt & "</span></div></div>
</div>"
```

## VIS HTML Chelsea Top Highlights

Good as a compact narrative strip. It does not use YoY comparison because the values are names/context rather than scalar KPIs.

Good as a compact narrative strip. It does not use YoY comparison because the values are names/context rather than scalar KPIs.

```DAX
VIS HTML Chelsea Top Highlights =
VAR _Season = IF(ISBLANK([REF Current Season]), "—", [REF Current Season])
VAR _TopScorer = IF(ISBLANK([REF Top Scorer Name]), "—", [REF Top Scorer Name] & " (" & FORMAT([# Top Scorer Goals], "#,##0") & " goals)")
VAR _MVP = IF(ISBLANK([$ Most Valuable Player (£)]), "—", [$ Most Valuable Player (£)])
VAR _Paid = IF(ISBLANK([$ Highest Paid Player (£)]), "—", [$ Highest Paid Player (£)])
RETURN
"<style>
.hi{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.hc{background:#141E30;border-radius:8px;border:1px solid #2c3b54;border-left:3px solid #D4AF37;padding:14px 12px;display:flex;flex-direction:column;justify-content:center;overflow:hidden;min-width:0;}
.hl{color:#D4AF37;font-size:9px;text-transform:uppercase;letter-spacing:1.4px;margin-bottom:6px;white-space:nowrap;}
.hv{color:#fff;font-size:13px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.hb{color:#7FA4CF;}
</style>
<div class=""hi"">
  <div class=""hc""><div class=""hl"">Season</div><div class=""hv"">" & _Season & "</div></div>
  <div class=""hc""><div class=""hl"">Top Scorer</div><div class=""hv"">" & _TopScorer & "</div></div>
  <div class=""hc""><div class=""hl"">Most Valuable</div><div class=""hv hb"">" & _MVP & "</div></div>
  <div class=""hc""><div class=""hl"">Highest Paid</div><div class=""hv"">" & _Paid & "</div></div>
</div>"
```
