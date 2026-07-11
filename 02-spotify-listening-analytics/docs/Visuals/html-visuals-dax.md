# Spotify HTML Visuals - DAX Measure Library

Paste these measures into the `formulas` table and use them with an HTML Content visual. They follow the same visual language as the current Sound Overview cards: dark surface, muted labels, Spotify-green accent, small delta pills, and compact spacing.

## VIS HTML Behavior Snapshot

Good for `My Listening DNA`. It shows four behavior rates in one compact strip.

```DAX
VIS HTML Behavior Snapshot =
VAR _Completion = [% Completion Rate]
VAR _Skip       = [% Skip Rate]
VAR _Shuffle    = [% Shuffle Rate]
VAR _Manual     = [% Manual Start Rate]
VAR _CompletionFmt = FORMAT(_Completion, "0.0%")
VAR _SkipFmt       = FORMAT(_Skip,       "0.0%")
VAR _ShuffleFmt    = FORMAT(_Shuffle,    "0.0%")
VAR _ManualFmt     = FORMAT(_Manual,     "0.0%")
VAR _CompletionW = FORMAT(MIN(1, MAX(0, _Completion)), "0%")
VAR _SkipW       = FORMAT(MIN(1, MAX(0, _Skip)),       "0%")
VAR _ShuffleW    = FORMAT(MIN(1, MAX(0, _Shuffle)),    "0%")
VAR _ManualW     = FORMAT(MIN(1, MAX(0, _Manual)),     "0%")
RETURN
"<style>
.bv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.bi{background:#121212;border-radius:8px;border:1px solid #242424;padding:12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.bl{color:#6c7e93;font-size:9px;text-transform:uppercase;letter-spacing:1.3px;white-space:nowrap;}
.bn{color:#f4f4f4;font-size:22px;font-weight:700;line-height:1.05;margin:7px 0 8px;}
.bt{height:5px;border-radius:99px;background:#252525;overflow:hidden;}
.bf{height:100%;border-radius:99px;background:#22cc66;}
.br{background:#e22134;}
.by{background:#ffc862;}
</style>
<div class=""bv"">
  <div class=""bi""><div class=""bl"">Completion</div><div class=""bn"">" & _CompletionFmt & "</div><div class=""bt""><div class=""bf"" style=""width:" & _CompletionW & """></div></div></div>
  <div class=""bi""><div class=""bl"">Skip Rate</div><div class=""bn"">" & _SkipFmt & "</div><div class=""bt""><div class=""bf br"" style=""width:" & _SkipW & """></div></div></div>
  <div class=""bi""><div class=""bl"">Shuffle</div><div class=""bn"">" & _ShuffleFmt & "</div><div class=""bt""><div class=""bf by"" style=""width:" & _ShuffleW & """></div></div></div>
  <div class=""bi""><div class=""bl"">Manual Starts</div><div class=""bn"">" & _ManualFmt & "</div><div class=""bt""><div class=""bf"" style=""width:" & _ManualW & """></div></div></div>
</div>"
```

## VIS HTML Rhythm Snapshot

Good for `My Daily Rhythm`. It anchors the heatmap with four mini KPI cards, each showing current value, relative YoY change, and same period last year.

```DAX
VIS HTML Rhythm Snapshot =
VAR _Hours      = [# Total Hours Played]
VAR _HoursPY    = CALCULATE([# Total Hours Played], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _HoursG     = DIVIDE(_Hours - _HoursPY, _HoursPY)
VAR _HoursClass = IF(ISBLANK(_HoursG) || _HoursG >= 0, "pos", "neg")
VAR _HoursArrow = IF(ISBLANK(_HoursG), "•", IF(_HoursG >= 0, "↑", "↓"))
VAR _HoursFmt   = FORMAT(_Hours, "#,##0.0") & " h"
VAR _HoursPYFmt = IF(ISBLANK(_HoursPY), "—", FORMAT(_HoursPY, "#,##0.0") & " h")
VAR _HoursGFmt  = IF(ISBLANK(_HoursG), "—", FORMAT(ABS(_HoursG), "0.0%"))

VAR _Avg        = [# Avg Hours per Active Day]
VAR _AvgPY      = CALCULATE([# Avg Hours per Active Day], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _AvgG       = DIVIDE(_Avg - _AvgPY, _AvgPY)
VAR _AvgClass   = IF(ISBLANK(_AvgG) || _AvgG >= 0, "pos", "neg")
VAR _AvgArrow   = IF(ISBLANK(_AvgG), "•", IF(_AvgG >= 0, "↑", "↓"))
VAR _AvgFmt     = FORMAT(_Avg, "0.0") & " h"
VAR _AvgPYFmt   = IF(ISBLANK(_AvgPY), "—", FORMAT(_AvgPY, "0.0") & " h")
VAR _AvgGFmt    = IF(ISBLANK(_AvgG), "—", FORMAT(ABS(_AvgG), "0.0%"))

VAR _Streams    = [# Streams per Active Day]
VAR _StreamsPY  = CALCULATE([# Streams per Active Day], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _StreamsG   = DIVIDE(_Streams - _StreamsPY, _StreamsPY)
VAR _StreamsClass = IF(ISBLANK(_StreamsG) || _StreamsG >= 0, "pos", "neg")
VAR _StreamsArrow = IF(ISBLANK(_StreamsG), "•", IF(_StreamsG >= 0, "↑", "↓"))
VAR _StreamsFmt   = FORMAT(_Streams, "#,##0.0")
VAR _StreamsPYFmt = IF(ISBLANK(_StreamsPY), "—", FORMAT(_StreamsPY, "#,##0.0"))
VAR _StreamsGFmt  = IF(ISBLANK(_StreamsG), "—", FORMAT(ABS(_StreamsG), "0.0%"))

VAR _Days       = [# Active Listening Days]
VAR _DaysPY     = CALCULATE([# Active Listening Days], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _DaysG      = DIVIDE(_Days - _DaysPY, _DaysPY)
VAR _DaysClass  = IF(ISBLANK(_DaysG) || _DaysG >= 0, "pos", "neg")
VAR _DaysArrow  = IF(ISBLANK(_DaysG), "•", IF(_DaysG >= 0, "↑", "↓"))
VAR _DaysFmt    = FORMAT(_Days, "#,##0")
VAR _DaysPYFmt  = IF(ISBLANK(_DaysPY), "—", FORMAT(_DaysPY, "#,##0"))
VAR _DaysGFmt   = IF(ISBLANK(_DaysG), "—", FORMAT(ABS(_DaysG), "0.0%"))
RETURN
"<style>
.rv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.ri{background:#141414;border-radius:8px;border:1px solid #2a2a2a;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.rl{color:#6c7e93;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.rn{color:#fff;font-size:20px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.rf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.rp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #166534;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #991b1b;color:#f87171;}
.ry{font-size:10px;color:#5c6370;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""rv"">
  <div class=""ri""><div class=""rl"">Total Hours</div><div class=""rn"">" & _HoursFmt & "</div><div class=""rf""><span class=""rp " & _HoursClass & """>" & _HoursArrow & " " & _HoursGFmt & "</span><span class=""ry"">vs PY: " & _HoursPYFmt & "</span></div></div>
  <div class=""ri""><div class=""rl"">Avg Hours / Active Day</div><div class=""rn"">" & _AvgFmt & "</div><div class=""rf""><span class=""rp " & _AvgClass & """>" & _AvgArrow & " " & _AvgGFmt & "</span><span class=""ry"">vs PY: " & _AvgPYFmt & "</span></div></div>
  <div class=""ri""><div class=""rl"">Streams / Active Day</div><div class=""rn"">" & _StreamsFmt & "</div><div class=""rf""><span class=""rp " & _StreamsClass & """>" & _StreamsArrow & " " & _StreamsGFmt & "</span><span class=""ry"">vs PY: " & _StreamsPYFmt & "</span></div></div>
  <div class=""ri""><div class=""rl"">Active Days</div><div class=""rn"">" & _DaysFmt & "</div><div class=""rf""><span class=""rp " & _DaysClass & """>" & _DaysArrow & " " & _DaysGFmt & "</span><span class=""ry"">vs PY: " & _DaysPYFmt & "</span></div></div>
</div>"
```

## VIS HTML Platform Context Snapshot

Good for `Platforms & Context`. It keeps the platform page header consistent with the overview KPI cards, with current value, relative YoY change, and same period last year.

```DAX
VIS HTML Platform Context Snapshot =
VAR _Offline      = [% Offline Rate]
VAR _OfflinePY    = CALCULATE([% Offline Rate], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _OfflineG     = DIVIDE(_Offline - _OfflinePY, _OfflinePY)
VAR _OfflineClass = IF(ISBLANK(_OfflineG) || _OfflineG >= 0, "pos", "neg")
VAR _OfflineArrow = IF(ISBLANK(_OfflineG), "•", IF(_OfflineG >= 0, "↑", "↓"))
VAR _OfflineFmt   = FORMAT(_Offline, "0.0%")
VAR _OfflinePYFmt = IF(ISBLANK(_OfflinePY), "—", FORMAT(_OfflinePY, "0.0%"))
VAR _OfflineGFmt  = IF(ISBLANK(_OfflineG), "—", FORMAT(ABS(_OfflineG), "0.0%"))

VAR _Countries      = [# Countries Streamed From]
VAR _CountriesPY    = CALCULATE([# Countries Streamed From], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _CountriesG     = DIVIDE(_Countries - _CountriesPY, _CountriesPY)
VAR _CountriesClass = IF(ISBLANK(_CountriesG) || _CountriesG >= 0, "pos", "neg")
VAR _CountriesArrow = IF(ISBLANK(_CountriesG), "•", IF(_CountriesG >= 0, "↑", "↓"))
VAR _CountriesFmt   = FORMAT(_Countries, "#,##0")
VAR _CountriesPYFmt = IF(ISBLANK(_CountriesPY), "—", FORMAT(_CountriesPY, "#,##0"))
VAR _CountriesGFmt  = IF(ISBLANK(_CountriesG), "—", FORMAT(ABS(_CountriesG), "0.0%"))

VAR _Groups      = [# Platform Groups Used]
VAR _GroupsPY    = CALCULATE([# Platform Groups Used], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _GroupsG     = DIVIDE(_Groups - _GroupsPY, _GroupsPY)
VAR _GroupsClass = IF(ISBLANK(_GroupsG) || _GroupsG >= 0, "pos", "neg")
VAR _GroupsArrow = IF(ISBLANK(_GroupsG), "•", IF(_GroupsG >= 0, "↑", "↓"))
VAR _GroupsFmt   = FORMAT(_Groups, "#,##0")
VAR _GroupsPYFmt = IF(ISBLANK(_GroupsPY), "—", FORMAT(_GroupsPY, "#,##0"))
VAR _GroupsGFmt  = IF(ISBLANK(_GroupsG), "—", FORMAT(ABS(_GroupsG), "0.0%"))
RETURN
"<style>
.pv{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;width:100%;height:100%;font-family:'Segoe UI',sans-serif;padding:6px;box-sizing:border-box;}
.pi{background:#141414;border-radius:8px;border:1px solid #2a2a2a;padding:11px 12px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow:hidden;}
.pl{color:#6c7e93;font-size:9px;text-transform:uppercase;letter-spacing:1.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pn{color:#fff;font-size:20px;font-weight:700;line-height:1.05;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.pf{display:flex;align-items:center;gap:7px;justify-content:flex-end;min-width:0;}
.pp{font-size:10px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap;}
.pos{background:#052e16;border:1px solid #166534;color:#4ade80;}
.neg{background:#450a0a;border:1px solid #991b1b;color:#f87171;}
.py{font-size:10px;color:#5c6370;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
</style>
<div class=""pv"">
  <div class=""pi""><div class=""pl"">Offline Rate</div><div class=""pn"">" & _OfflineFmt & "</div><div class=""pf""><span class=""pp " & _OfflineClass & """>" & _OfflineArrow & " " & _OfflineGFmt & "</span><span class=""py"">vs PY: " & _OfflinePYFmt & "</span></div></div>
  <div class=""pi""><div class=""pl"">Countries</div><div class=""pn"">" & _CountriesFmt & "</div><div class=""pf""><span class=""pp " & _CountriesClass & """>" & _CountriesArrow & " " & _CountriesGFmt & "</span><span class=""py"">vs PY: " & _CountriesPYFmt & "</span></div></div>
  <div class=""pi""><div class=""pl"">Platform Groups</div><div class=""pn"">" & _GroupsFmt & "</div><div class=""pf""><span class=""pp " & _GroupsClass & """>" & _GroupsArrow & " " & _GroupsGFmt & "</span><span class=""py"">vs PY: " & _GroupsPYFmt & "</span></div></div>
</div>"
```

## VIS _HTML Card Completion Rate

Single KPI card. Uses percentage-point delta because relative growth on a rate is harder to read.

```DAX
VIS _HTML Card Completion Rate =
VAR _Value = [% Completion Rate]
VAR _PY    = CALCULATE([% Completion Rate], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _Delta = _Value - _PY
VAR _IsPos = _Delta >= 0
VAR _Color   = IF(_IsPos, "#4ade80", "#f87171")
VAR _BgColor = IF(_IsPos, "#052e16", "#450a0a")
VAR _Border  = IF(_IsPos, "#166534", "#991b1b")
VAR _Arrow   = IF(_IsPos, "↑", "↓")
VAR _ValueFmt = FORMAT(_Value, "0.0%")
VAR _PYFmt    = FORMAT(_PY, "0.0%")
VAR _DeltaFmt = FORMAT(ABS(_Delta) * 100, "0.0") & " pp"
VAR _Width    = FORMAT(MIN(1, MAX(0, _Value)), "0%")
RETURN
"<div style='font-family:Segoe UI,sans-serif;padding:12px 18px;border-radius:10px;border:1.5px solid #2a2a2a;background:#141414;width:100%;height:100%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;'>
  <div style='font-size:10px;font-weight:600;color:#5c6370;letter-spacing:.04em;'>Completion Rate</div>
  <div style='font-size:25px;font-weight:600;color:#f1f1f1;line-height:1.1;'>" & _ValueFmt & "</div>
  <div style='height:5px;border-radius:99px;background:#252525;overflow:hidden;'><div style='height:100%;width:" & _Width & ";background:#22cc66;border-radius:99px;'></div></div>
  <div style='display:flex;align-items:center;gap:8px;justify-content:flex-end;'>
    <span style='background:" & _BgColor & ";border:1px solid " & _Border & ";color:" & _Color & ";font-size:11px;font-weight:600;white-space:nowrap;padding:2px 8px;border-radius:99px;'>" & _Arrow & " " & _DeltaFmt & "</span>
    <span style='font-size:11px;color:#5c6370;'>vs PY: " & _PYFmt & "</span>
  </div>
</div>"
```

## VIS _HTML Card Offline Rate

Single KPI card for the platform page. Offline is treated as context rather than good/bad, so the bar stays green and the delta color only indicates direction.

```DAX
VIS _HTML Card Offline Rate =
VAR _Value = [% Offline Rate]
VAR _PY    = CALCULATE([% Offline Rate], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _Delta = _Value - _PY
VAR _IsPos = _Delta >= 0
VAR _Color   = IF(_IsPos, "#4ade80", "#f87171")
VAR _BgColor = IF(_IsPos, "#052e16", "#450a0a")
VAR _Border  = IF(_IsPos, "#166534", "#991b1b")
VAR _Arrow   = IF(_IsPos, "↑", "↓")
VAR _ValueFmt = FORMAT(_Value, "0.0%")
VAR _PYFmt    = FORMAT(_PY, "0.0%")
VAR _DeltaFmt = FORMAT(ABS(_Delta) * 100, "0.0") & " pp"
VAR _Width    = FORMAT(MIN(1, MAX(0, _Value)), "0%")
RETURN
"<div style='font-family:Segoe UI,sans-serif;padding:12px 18px;border-radius:10px;border:1.5px solid #2a2a2a;background:#141414;width:100%;height:100%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;'>
  <div style='font-size:10px;font-weight:600;color:#5c6370;letter-spacing:.04em;'>Offline Rate</div>
  <div style='font-size:25px;font-weight:600;color:#f1f1f1;line-height:1.1;'>" & _ValueFmt & "</div>
  <div style='height:5px;border-radius:99px;background:#252525;overflow:hidden;'><div style='height:100%;width:" & _Width & ";background:#22cc66;border-radius:99px;'></div></div>
  <div style='display:flex;align-items:center;gap:8px;justify-content:flex-end;'>
    <span style='background:" & _BgColor & ";border:1px solid " & _Border & ";color:" & _Color & ";font-size:11px;font-weight:600;white-space:nowrap;padding:2px 8px;border-radius:99px;'>" & _Arrow & " " & _DeltaFmt & "</span>
    <span style='font-size:11px;color:#5c6370;'>vs PY: " & _PYFmt & "</span>
  </div>
</div>"
```

## VIS _HTML Card Skip Rate

Single KPI card. Lower skip rate is treated as the positive movement.

```DAX
VIS _HTML Card Skip Rate =
VAR _Value = [% Skip Rate]
VAR _PY    = CALCULATE([% Skip Rate], SAMEPERIODLASTYEAR('dim_calendar'[Date]))
VAR _Delta = _Value - _PY
VAR _IsGood = _Delta <= 0
VAR _Color   = IF(_IsGood, "#4ade80", "#f87171")
VAR _BgColor = IF(_IsGood, "#052e16", "#450a0a")
VAR _Border  = IF(_IsGood, "#166534", "#991b1b")
VAR _Arrow   = IF(_Delta >= 0, "↑", "↓")
VAR _ValueFmt = FORMAT(_Value, "0.0%")
VAR _PYFmt    = FORMAT(_PY, "0.0%")
VAR _DeltaFmt = FORMAT(ABS(_Delta) * 100, "0.0") & " pp"
VAR _Width    = FORMAT(MIN(1, MAX(0, _Value)), "0%")
RETURN
"<div style='font-family:Segoe UI,sans-serif;padding:12px 18px;border-radius:10px;border:1.5px solid #2a2a2a;background:#141414;width:100%;height:100%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;'>
  <div style='font-size:10px;font-weight:600;color:#5c6370;letter-spacing:.04em;'>Skip Rate</div>
  <div style='font-size:25px;font-weight:600;color:#f1f1f1;line-height:1.1;'>" & _ValueFmt & "</div>
  <div style='height:5px;border-radius:99px;background:#252525;overflow:hidden;'><div style='height:100%;width:" & _Width & ";background:#e22134;border-radius:99px;'></div></div>
  <div style='display:flex;align-items:center;gap:8px;justify-content:flex-end;'>
    <span style='background:" & _BgColor & ";border:1px solid " & _Border & ";color:" & _Color & ";font-size:11px;font-weight:600;white-space:nowrap;padding:2px 8px;border-radius:99px;'>" & _Arrow & " " & _DeltaFmt & "</span>
    <span style='font-size:11px;color:#5c6370;'>vs PY: " & _PYFmt & "</span>
  </div>
</div>"
```
