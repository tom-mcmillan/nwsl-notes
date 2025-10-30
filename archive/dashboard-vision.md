# NWSL Terminal - Dashboard Vision Document

**Version**: 1.0
**Date**: 2025-10-25
**Purpose**: Define the comprehensive vision for the Index page with three-tab structure

---

## Overview

The NWSL Terminal Index page is a Bloomberg Terminal-inspired analytics workbench designed to transform users from casual observers into informed analysts. The page consists of three experientially distinct tabs that guide users through a knowledge creation journey:

**DASHBOARD → RESEARCH → REPORT**

Each tab offers fundamentally different technology, visual frameworks, and user experiences - not just increasing complexity, but distinct modes of engagement with NWSL data.

---

## Page Architecture

### Top-Level Navigation
```
┌─────────────────────────────────────────────────────────────────┐
│  NWSL TERMINAL                        [Index] [Notebook]        │
└─────────────────────────────────────────────────────────────────┘
```

### Index Page Tab Structure
```
┌─────────────────────────────────────────────────────────────────┐
│  [Dashboard] [Research] [Report]                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│              (Tab Content - Dense Multi-Panel Layout)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Design Principles

### 1. Bloomberg Terminal Aesthetic
- **Dark theme**: Black background (#000000 or #0a0a0a)
- **High contrast**: White/green/red/orange text on dark background
- **Information density**: Every pixel serves a purpose, zero wasted space
- **Monospace typography**: Professional, data-focused
- **Color coding**: Green (positive/buy), Red (negative/sell), Orange (alerts), Blue (selected)
- **Modular panels**: Resizable, draggable windows (future enhancement)

### 2. Progressive Knowledge Creation
Each tab represents a different epistemic stage:
- **DASHBOARD**: Acquaintance with facts + Understanding patterns
- **RESEARCH**: Testing hypotheses + Statistical validation
- **REPORT**: Consuming finished intelligence

### 3. Multi-Panel Layouts
Each tab displays 6-10 simultaneous panels in a grid layout, allowing users to see multiple data perspectives at once without scrolling.

### 4. Real-Time Data Integration
All panels pull from production APIs:
- `https://api.nwsldata.com/sql` - Direct SQL queries
- `https://api.nwsldata.com/dashboard/*` - Dashboard endpoints
- `nwsl-viz` service - On-demand visualizations
- `nwsl-mcp-py` - Statistical research tools

---

## TAB 1: DASHBOARD

### Tagline
**"The comprehensive view - everything important, right now"**

### User Mode
Scanning, looking up, monitoring

### Rhetorical Question
"What do I need to know?"

### User Outcome
User leaves feeling informed about league state and sees interesting patterns to explore deeper

### Experience Type
- Witnessing facts
- Recognizing patterns
- Monitoring current state
- Exploring spatial tactics

### Technology Stack
- Dense tables with sortable columns
- Real-time numerical displays
- Spatial visualizations (shot maps, heatmaps, pass networks)
- Color-coded results
- Live updates
- Interactive filters

### Visual Framework
Combination of structured tables + spatial pitch diagrams

---

### DASHBOARD Panel Layout (8 Panels)

```
┌──────────────────────────────────────────────────────────────────────┐
│  LEAGUE STANDINGS   │  RECENT MATCHES      │  THIS WEEK'S LEADERS   │
│  (Table)            │  (Table)             │  (Table)               │
├──────────────────────────────────────────────────────────────────────┤
│  POWER RANKINGS     │  LIVE MATCHES        │  LEAGUE ALERTS         │
│  (Table)            │  (Live Feed)         │  (Alert List)          │
├──────────────────────────────────────────────────────────────────────┤
│  VISUALIZATION GENERATOR              │  WATCHLIST                 │
│  (Interactive Builder)                │  (Custom Tracking)         │
└──────────────────────────────────────────────────────────────────────┘
```

---

### Panel Specifications

#### Panel 1: LEAGUE STANDINGS
**Purpose**: Current standings with form indicators

**Data Source**: `GET /dashboard/team-overview?season=2025`

**Columns**:
```
Pos | Team | GP | W | D | L | GF | GA | GD | Pts | Form
1   | ORL  | 24 | 16| 4 | 4 | 52 | 28 | +24| 52  | WWDWW
```

**Formatting**:
- Color-coded form: W (green), L (red), D (gray)
- Bold text for user's watchlisted teams
- Click team name → filters other panels to that team
- Sortable by any column

**Technical Notes**:
- Use `agg_team_season` table via API
- Update frequency: Every 5 minutes during match days, hourly otherwise
- Show current season by default, dropdown to select historical seasons

---

#### Panel 2: RECENT MATCHES
**Purpose**: Last 10 completed matches with xG context

**Data Source**: SQL query to `agg_team_match` + `fact_event_xg`

**Display Format**:
```
Date       | Home Team    | Score | xG   | Away Team      | xG   | Venue
10/20/2025 | Orlando      | 2-1   | 1.8  | Kansas City    | 0.9  | Inter&Co
10/19/2025 | Portland     | 1-1   | 1.2  | San Diego      | 1.4  | Providence
```

**Formatting**:
- Color-coded results: Home win (green home team), Away win (green away team), Draw (gray both)
- xG in smaller, lighter text below score
- Click match → opens detailed match view (future enhancement)
- Hover → tooltip with top scorers, attendance

**Technical Notes**:
- Query: `SELECT * FROM agg_team_match ORDER BY match_date DESC LIMIT 10`
- Include xG totals from aggregated shot data
- Real-time updates during live matches

---

#### Panel 3: THIS WEEK'S LEADERS
**Purpose**: Top performers from last 7 days

**Data Source**: `agg_player_match` filtered by last 7 days

**Categories** (Tabs within panel):
- Goals (Top 5)
- Assists (Top 5)
- Point Shares (Top 5)
- VAEP (Top 5)

**Display Format**:
```
GOALS (Last 7 Days)
1. Temwa Chawinga (KC)    3 goals
2. Barbra Banda (ORL)     2 goals
3. Sophia Smith (POR)     2 goals
```

**Formatting**:
- Small avatar images if available (future)
- Team abbreviation in parentheses
- Click player → filters other panels to that player

**Technical Notes**:
- Window: `match_date >= CURRENT_DATE - INTERVAL '7 days'`
- Aggregation: `SUM(goals), SUM(assists), SUM(point_shares), SUM(vaep_value)`

---

#### Panel 4: POWER RANKINGS
**Purpose**: Season-long player evaluation with advanced metrics

**Data Source**: `GET /dashboard/player-valuation?season=2025`

**Columns**:
```
Rank | Player           | Team | Pos | VAEP | xG   | G+A | PS  | Per90
1    | Sophia Smith     | POR  | FW  | 14.2 | 18.3 | 23  | 42  | 0.98
2    | Trinity Rodman   | WAS  | FW  | 12.8 | 14.1 | 19  | 38  | 0.87
```

**Formatting**:
- VAEP: Green if above league average, red if below
- xG vs Actual: Show differential (e.g., "+2.7" for overperformance)
- Sortable by any metric
- Filter by position (FW/MF/DF/GK)

**Technical Notes**:
- Source: `agg_player_season` joined with ML metrics
- Per90 normalization: `(metric / minutes_played) * 90`
- League averages calculated for color coding

---

#### Panel 5: LIVE MATCHES
**Purpose**: Real-time match updates with xG timeline

**Data Source**: `fact_event` + `fact_event_xg` for live matches (future: WebSocket)

**Display Format** (When Match Active):
```
LIVE: Orlando Pride 1-0 Kansas City Current    67'

xG Timeline:
ORL: ███████████░░░░░ 1.4
KC:  ████░░░░░░░░░░░░ 0.6

Recent Events:
67' 🟨 Chawinga (KC) - Yellow Card
52' ⚽ Marta (ORL) - Goal (0.12 xG)
23' 🟨 Strom (ORL) - Yellow Card
```

**Display Format** (When No Live Matches):
```
NO LIVE MATCHES

Next Match:
Portland Thorns vs San Diego Wave
Tomorrow, 10:00 PM ET
```

**Formatting**:
- xG timeline as horizontal bars (home vs away)
- Events reverse chronological
- Icons: ⚽ (goal), 🟨 (yellow), 🟥 (red), 🔄 (sub)
- Live minute pulsing orange

**Technical Notes**:
- Poll every 30 seconds during match windows
- xG accumulates in real-time
- WebSocket integration (future enhancement)

---

#### Panel 6: LEAGUE ALERTS
**Purpose**: Important news, injuries, transfers, milestones

**Data Source**: Custom feed (initially manually curated, future: automated)

**Display Format**:
```
🔴 INJURY: Sophia Smith (POR) - Questionable for Sunday
🟢 MILESTONE: Marta (ORL) - 200th career assist
🟠 TRANSFER: Sam Coffey (POR) - New contract through 2027
🔵 ROSTER: Chicago Red Stars sign goalkeeper Alyssa Naeher
```

**Formatting**:
- Color-coded by type (injury=red, milestone=green, transfer=orange, roster=blue)
- Timestamp: "2 hours ago"
- Click → expands to full details (future)

**Technical Notes**:
- Store in `league_alerts` table (to be created)
- Fields: `timestamp`, `type`, `team_id`, `player_id`, `headline`, `details`
- Show last 15 alerts

---

#### Panel 7: VISUALIZATION GENERATOR
**Purpose**: On-demand pitch visualizations using nwsl-viz service

**Layout**:
```
┌────────────────────────────────────────────────┐
│ Select Player/Team:  [Dropdown]                │
│ Visualization Type:  [Dropdown]                │
│ Season:              [Dropdown - Default 2025] │
│ [Generate] button                              │
├────────────────────────────────────────────────┤
│                                                │
│       (Rendered Visualization Display)         │
│                                                │
└────────────────────────────────────────────────┘
```

**Visualization Types**:
1. Shot Map
2. Heatmap
3. Pass Network
4. Pass Flow
5. xT Grid
6. Pass Lines
7. Convex Hull
8. Action Sequences

**API Integration**:
```javascript
POST https://nwsl-viz-service.com/generate_shot_map
{
  "team_name": "Orlando Pride",
  "season": 2025
}

Response:
{
  "render": {
    "url": "https://storage.googleapis.com/nwsl-visualizations/..."
  }
}
```

**Formatting**:
- Display image at full panel width
- Show metrics below image (e.g., "119 shots, 21 goals, 17.6% conversion")
- Export button (download PNG)
- Cache images to avoid re-generation

**Technical Notes**:
- Call nwsl-viz service API
- Cache responses by request fingerprint (service provides this)
- Loading state while generating (300-500ms first render, <100ms cached)

---

#### Panel 8: WATCHLIST
**Purpose**: User's custom tracking of favorite players/teams

**Data Source**: Local storage (client-side) or user profile (future)

**Display Format**:
```
MY WATCHLIST

Teams:
⭐ Orlando Pride        52 pts  (+3 this week)
⭐ Portland Thorns     48 pts  (+1 this week)

Players:
⭐ Sophia Smith (POR)  2 goals, 1 assist (Last 7 days)
⭐ Marta (ORL)         1 goal, 2 assists (Last 7 days)

[+ Add Player/Team]
```

**Formatting**:
- Star icon for each watchlist item
- Recent performance in parentheses
- Click item → filters entire dashboard to that entity
- Remove button (X) on hover

**Technical Notes**:
- Store as JSON in localStorage: `{"teams": ["ORL", "POR"], "players": [123, 456]}`
- Join with current stats on render
- Max 5 teams, 10 players

---

## TAB 2: RESEARCH

### Tagline
**"The laboratory - test your theories with statistical rigor"**

### User Mode
Investigating, testing, querying, exploring hypotheses

### Rhetorical Question
"Is my theory true?"

### User Outcome
User leaves with statistically validated insights, can prove/disprove hypotheses with data

### Experience Type
- Active exploration
- Hypothesis testing
- Custom data querying
- ML model interpretation

### Technology Stack
- 20 MCP statistical tools (via nwsl-mcp-py)
- Query builder (SQL interface)
- ML model sandbox (xG, VAEP, PMI explanations)
- Interactive statistical tests (t-tests, correlations, ANOVA)
- Custom visualization generation

### Visual Framework
Forms, interactive controls, statistical outputs, hypothesis testing UI

---

### RESEARCH Panel Layout (7 Panels)

```
┌──────────────────────────────────────────────────────────────────┐
│  HYPOTHESIS TESTER    │  CORRELATION EXPLORER │  QUERY BUILDER  │
├──────────────────────────────────────────────────────────────────┤
│  DISTRIBUTION ANALYZER│  COHORT COMPARISON    │  ML SANDBOX     │
├──────────────────────────────────────────────────────────────────┤
│  RESULTS DISPLAY (Large panel spanning full width)              │
└──────────────────────────────────────────────────────────────────┘
```

---

### Panel Specifications

#### Panel 1: HYPOTHESIS TESTER
**Purpose**: Statistical testing of user hypotheses

**UI Components**:
```
Hypothesis: [Text input - e.g., "Home teams score more goals"]

Group A: [Dropdown - e.g., "Home Teams"]
Group B: [Dropdown - e.g., "Away Teams"]
Metric:  [Dropdown - e.g., "Goals per game"]

Test Type: [Dropdown - t-test, Mann-Whitney U, Chi-square]

[Run Test] button
```

**Output** (in Results Display panel):
```
HYPOTHESIS TEST RESULTS

Null Hypothesis: No difference in goals per game between home and away teams
Alternative: Home teams score significantly more

Group A (Home): Mean = 1.84 goals/game, SD = 1.12, n = 664
Group B (Away): Mean = 1.52 goals/game, SD = 1.03, n = 664

t-statistic: 4.23
p-value: < 0.001
Effect size (Cohen's d): 0.29 (small-to-medium)
95% CI for difference: [0.17, 0.47]

CONCLUSION: Reject null hypothesis. Home teams score significantly more
goals per game (p < 0.001). The effect is small-to-medium.
```

**Technical Notes**:
- Use MCP tool: `compare_entities` or `compare_distributions`
- Pre-built templates: "Home vs Away", "Winners vs Losers", "First Half vs Second Half"
- Automatically choose parametric vs non-parametric based on normality tests

---

#### Panel 2: CORRELATION EXPLORER
**Purpose**: Discover relationships between metrics

**UI Components**:
```
X-Axis Metric: [Dropdown - e.g., "Possession %"]
Y-Axis Metric: [Dropdown - e.g., "Goals"]
Cohort:        [Dropdown - e.g., "All teams, 2024 season"]
Method:        [Dropdown - Pearson / Spearman]

[Calculate Correlation] button
```

**Output** (in Results Display panel):
```
CORRELATION ANALYSIS

Variables: Possession % (X) vs Goals (Y)
Sample: All teams, 2024 season (n = 191 team-matches)
Method: Pearson correlation

r = 0.34
p-value = 0.002
R² = 0.12 (12% of variance explained)
95% CI: [0.13, 0.52]

INTERPRETATION: Weak-to-moderate positive correlation. Teams with higher
possession tend to score more goals, but only 12% of goal variance is
explained by possession alone.

[Scatter plot with regression line displayed below]
```

**Technical Notes**:
- Use MCP tool: `calculate_correlation`
- Auto-detect outliers and offer to remove
- Generate scatter plot with regression line
- Offer to download data as CSV

---

#### Panel 3: QUERY BUILDER
**Purpose**: Custom SQL queries for advanced users

**UI Components**:
```
SQL Query:
[Text area - SQL editor with syntax highlighting]

Example queries: [Dropdown with templates]
- Top 10 goal scorers
- Team performance by venue
- Player consistency analysis

Row Limit: [Input - default 1000, max 10000]

[Execute Query] button    [Export CSV] button
```

**Safety Features**:
- Read-only queries (blocks INSERT, UPDATE, DELETE, DROP)
- Query timeout: 60 seconds
- Row limit enforcement
- Show execution time

**Output** (in Results Display panel):
```
QUERY RESULTS (executed in 234ms, 147 rows returned)

[Interactive table with results]

[Download CSV] button
```

**Technical Notes**:
- Use `/sql` API endpoint
- Syntax highlighting with CodeMirror or Monaco Editor
- Save query history (localStorage)
- Template library for common queries

---

#### Panel 4: DISTRIBUTION ANALYZER
**Purpose**: Understand distributions and percentile ranks

**UI Components**:
```
Metric:  [Dropdown - e.g., "Goals per 90"]
Cohort:  [Dropdown - e.g., "Forwards, 2024 season"]
Player:  [Optional - highlight specific player]

[Analyze Distribution] button
```

**Output** (in Results Display panel):
```
DISTRIBUTION ANALYSIS: Goals per 90 (Forwards, 2024)

Summary Statistics:
- Mean: 0.52, Median: 0.48
- SD: 0.31, IQR: 0.45
- Min: 0.00, Max: 1.24
- Skewness: 0.34 (slightly right-skewed)
- Kurtosis: -0.12 (platykurtic)

Normality Tests:
- Shapiro-Wilk: W = 0.96, p = 0.08 (approximately normal)

Percentiles:
25th: 0.28
50th: 0.48
75th: 0.73
90th: 0.91
95th: 1.02

PLAYER HIGHLIGHT: Sophia Smith (0.89 goals/90)
- Percentile rank: 88th
- 1.2 SD above mean
- Top 12% of all forwards

[Histogram with player highlighted displayed below]
```

**Technical Notes**:
- Use MCP tool: `calculate_distribution` + `calculate_percentile_rank`
- Generate histogram with matplotlib-style rendering
- Color-code player position on distribution

---

#### Panel 5: COHORT COMPARISON
**Purpose**: Compare multiple groups simultaneously

**UI Components**:
```
Metric:    [Dropdown - e.g., "VAEP per 90"]
Cohorts:   [Multi-select - e.g., "FW, MF, DF"]
Test Type: [Dropdown - ANOVA / Kruskal-Wallis]

[Compare Cohorts] button
```

**Output** (in Results Display panel):
```
COHORT COMPARISON: VAEP per 90 by Position

Groups:
- Forwards (n=87):    Mean = 0.12, SD = 0.08
- Midfielders (n=124): Mean = 0.09, SD = 0.06
- Defenders (n=142):   Mean = 0.05, SD = 0.05

ANOVA Results:
F-statistic: 23.4
p-value: < 0.001
Effect size (η²): 0.12 (medium effect)

Post-hoc (Tukey HSD):
- FW vs MF: p = 0.03 (significant)
- FW vs DF: p < 0.001 (significant)
- MF vs DF: p = 0.002 (significant)

CONCLUSION: Positions differ significantly in VAEP contribution.
Forwards > Midfielders > Defenders (all pairwise comparisons significant).

[Box plot showing distributions displayed below]
```

**Technical Notes**:
- Use MCP tool: `compare_cohorts`
- Automatically run post-hoc tests if ANOVA significant
- Generate box plots or violin plots
- Handle non-normal data with Kruskal-Wallis

---

#### Panel 6: ML SANDBOX
**Purpose**: Interpret ML model predictions and feature importance

**UI Components** (Tabbed):

**Tab 1: xG Explainer**
```
Select Shot: [Dropdown - recent shots or custom input]

Shot Details:
- Distance: 18 yards
- Angle: 23°
- Body part: Right foot
- Assist type: Through ball
- Game state: Tied

xG Prediction: 0.24

[Show Feature Importance] button
```

**Output**:
```
FEATURE IMPORTANCE FOR THIS SHOT

Distance to goal:    +0.15 (biggest contributor)
Angle:               +0.04
Assist type:         +0.03
Body part:           +0.02
Game state:          +0.00

Model confidence: High (0.89)
Similar shots: 247 in training data
Actual conversion: 26% (close to predicted 24%)
```

**Tab 2: VAEP Breakdown**
```
Select Player: [Dropdown]
Season: [Dropdown]

[Analyze VAEP] button
```

**Output**:
```
VAEP BREAKDOWN: Sophia Smith (2024)

Total VAEP: 14.2
- Offensive VAEP: 10.8 (76%)
- Defensive VAEP: 3.4 (24%)

VAEP by Action Type:
- Shots: 6.2 (44%)
- Passes: 3.8 (27%)
- Dribbles: 2.4 (17%)
- Other: 1.8 (12%)

Per 90: 0.52 (95th percentile among forwards)

[Action-by-action breakdown table displayed below]
```

**Tab 3: Player Match Impact (PMI)**
```
Predict Match Outcome:

Team: [Dropdown]
Expected Player Stats: [Form with inputs - goals, assists, VAEP, etc.]

[Predict Outcome] button
```

**Output**:
```
MATCH OUTCOME PREDICTION

Predicted Result: Win (probability: 67%)
- Win: 67%
- Draw: 18%
- Loss: 15%

Most Important Features:
1. Is home: +12%
2. Expected goals: +8%
3. Expected assists: +5%

Model confidence: Medium (normalized Brier: 0.93)
```

**Technical Notes**:
- Load ML artifacts from `nwsl-ml/artifacts/`
- xG model: `xg/nwsl_xg_beta.joblib`
- VAEP model: `vaep/p_scores_v1.pkl`, `vaep/p_concedes_v1.pkl`
- PMI model: `pmi/pmi_xgboost_model.pkl`
- Use SHAP or feature importance from models

---

#### Panel 7: RESULTS DISPLAY
**Purpose**: Large panel to display outputs from all research tools

**Behavior**:
- Starts empty with message: "Run a test or query to see results here"
- Updates when any research tool executes
- Shows formatted statistical outputs
- Displays generated visualizations (charts, plots)
- Includes export buttons (CSV, PNG, PDF)

**Technical Notes**:
- Dynamically renders based on tool output
- Syntax highlighting for statistical results
- Chart rendering with Recharts or D3
- Responsive layout (full panel width)

---

## TAB 3: REPORT

### Tagline
**"The briefing - curated insights ready to use"**

### User Mode
Reading, consuming, exporting finished analysis

### Rhetorical Question
"What should I know/share?"

### User Outcome
User leaves with finished analytical products ready to broadcast, write, or coach with

### Experience Type
- Consuming pre-written analysis
- Generating custom reports
- Exporting dashboards
- Reading narrative insights

### Technology Stack
- Pre-generated analytical reports (stored as markdown/HTML)
- Dynamic report generator (templates + live data)
- PDF/PNG export
- Embeddable visualizations
- Narrative generation (future: LLM-assisted)

### Visual Framework
Document-style layout, narrative text with embedded charts/tables, export-ready formatting

---

### REPORT Panel Layout (5 Panels)

```
┌──────────────────────────────────────────────────────────────────┐
│  REPORT LIBRARY       │  REPORT VIEWER (Large, 2x width)        │
├──────────────────────────────────────────────────────────────────┤
│  CUSTOM GENERATOR     │  EXPORT CONTROLS                         │
└──────────────────────────────────────────────────────────────────┘
```

---

### Panel Specifications

#### Panel 1: REPORT LIBRARY
**Purpose**: Browse available pre-generated reports

**UI Components**:
```
WEEKLY REPORTS
▸ Point Shares Leaders - Week 24
▸ Match Recap: ORL vs KC - Oct 20
▸ Power Rankings - Oct 2025

MONTHLY REPORTS
▸ State of the League - October 2025
▸ Breakout Players - October
▸ Tactical Trends - October

SEASON REPORTS
▸ 2025 Mid-Season Review
▸ xG Overperformers - 2025
▸ VAEP Leaders - 2025

SCOUTING REPORTS
▸ Sophia Smith - Full Profile
▸ Orlando Pride - Team Analysis
▸ Goalkeeper Rankings - 2025

[Filter by Type] [Search]
```

**Formatting**:
- Click report → loads in Report Viewer panel
- New reports highlighted (orange dot)
- Date stamps visible
- Categories collapsible

**Technical Notes**:
- Reports stored as markdown with frontmatter:
  ```yaml
  ---
  title: "Point Shares Leaders - Week 24"
  date: "2025-10-20"
  type: "weekly"
  author: "NWSL Terminal"
  ---
  ```
- Render markdown to HTML in viewer
- Store in `/reports/` directory or database

---

#### Panel 2: REPORT VIEWER
**Purpose**: Display selected report with formatted text, charts, tables

**Display Format**:
```
┌────────────────────────────────────────────────┐
│  POINT SHARES LEADERS - WEEK 24                │
│  Published: October 20, 2025                   │
├────────────────────────────────────────────────┤
│                                                │
│  Orlando Pride's 2-1 victory over Kansas City │
│  Current saw several standout performances,   │
│  with Marta leading Point Shares attribution. │
│                                                │
│  TOP PERFORMERS                                │
│  1. Marta (ORL) - 2.8 Point Shares            │
│     - 1 goal (0.12 xG)                        │
│     - 3.2 VAEP (offensive actions)            │
│     - 89% pass completion in final third      │
│                                                │
│  [Embedded shot map visualization]            │
│                                                │
│  2. Barbra Banda (ORL) - 2.1 Point Shares     │
│  ...                                           │
│                                                │
│  STATISTICAL CONTEXT                           │
│  Marta's 2.8 PS represents 31% of Orlando's   │
│  total distributed shares (9.0). This marks   │
│  her highest single-match contribution of     │
│  the season (previous high: 2.4 PS).          │
│                                                │
│  [Embedded bar chart of PS distribution]      │
│                                                │
└────────────────────────────────────────────────┘

[Export PDF] [Export PNG] [Share URL]
```

**Formatting**:
- Clean, readable typography (serif for body, sans for data)
- Embedded visualizations from nwsl-viz
- Tables with consistent styling
- Narrative text with data callouts
- Professional layout suitable for export

**Technical Notes**:
- Markdown rendering with embedded components
- Charts rendered with Recharts
- Tables from data queries
- PDF export via browser print or library
- URL sharing (future: shareable permalinks)

---

#### Panel 3: CUSTOM GENERATOR
**Purpose**: Generate custom reports on-demand

**UI Components**:
```
GENERATE CUSTOM REPORT

Report Type: [Dropdown]
- Player Scouting Report
- Team Analysis
- Match Recap
- Position Comparison

Subject: [Dropdown - depends on type]
  e.g., "Sophia Smith" for player report

Season/Date Range: [Date picker]

Include Sections: [Checkboxes]
☑ Summary Statistics
☑ Advanced Metrics (xG, VAEP, PS)
☑ Visualizations (shot map, heatmap)
☑ Statistical Comparisons
☑ Historical Context

[Generate Report] button
```

**Generated Report Example** (Player Scouting Report):
```
SOPHIA SMITH - SCOUTING REPORT
Portland Thorns FC | Forward | #9
2025 Season

SUMMARY
Sophia Smith is an elite forward performing at the 95th percentile
across multiple metrics. Her 14.2 VAEP leads all NWSL forwards,
combining elite finishing (0.89 goals/90) with creative playmaking.

STATISTICS (2025 Season)
Games: 22 | Minutes: 1,847
Goals: 18 | Assists: 5 | G+A/90: 1.12

ADVANCED METRICS
VAEP: 14.2 (1st among forwards)
xG: 18.3 | Actual Goals: 18 (perfectly on target)
Point Shares: 42 (2nd in league)

[Embedded shot map]
[Embedded heatmap]

STRENGTHS
- Elite finishing from all zones (17.6% conversion)
- High VAEP offensive actions (10.8)
- Consistent performer (CV: 0.23, low variance)

COMPARISONS
vs League Avg FW: +3.8 VAEP, +0.4 goals/90
vs Trinity Rodman: Similar xG, higher VAEP
Percentile ranks: 95th (VAEP), 88th (goals/90)

RECOMMENDATION
Smith is a top-tier forward with elite metrics across
finishing, chance creation, and overall value. Strong
candidate for MVP consideration.
```

**Technical Notes**:
- Use templates with placeholders
- Query data from API/database based on inputs
- Generate visualizations via nwsl-viz
- Render to Report Viewer panel
- Save to Report Library (optional)

---

#### Panel 4: EXPORT CONTROLS
**Purpose**: Export current report in various formats

**UI Components**:
```
EXPORT OPTIONS

Format: [Radio buttons]
○ PDF (print-ready)
○ PNG (image)
○ HTML (web-ready)
○ Markdown (source)

Quality: [Dropdown - Draft / Standard / High]

Include: [Checkboxes]
☑ Visualizations (embedded)
☑ Raw data tables
☑ Footnotes/sources

[Export] button
[Email Report] button (future)
```

**Technical Notes**:
- PDF: Use browser print API or jsPDF library
- PNG: HTML to canvas with html2canvas
- HTML: Pre-rendered, embeddable
- Markdown: Original source with frontmatter
- Watermark with "Generated by NWSL Terminal"

---

## Technical Implementation Notes

### API Integration Points

**Primary APIs**:
1. `https://api.nwsldata.com/sql` - Direct SQL queries
2. `https://api.nwsldata.com/dashboard/lookups` - Selector data
3. `https://api.nwsldata.com/dashboard/summary` - League metrics
4. `https://api.nwsldata.com/dashboard/team-overview` - Standings
5. `https://api.nwsldata.com/dashboard/player-valuation` - Player metrics
6. `nwsl-viz` service - Visualization generation
7. `nwsl-mcp-py` service - Statistical research tools

**Authentication**:
- API key: Use `DEFAULT_PUBLIC_API_KEY` for development
- Future: User authentication with personal API keys

**Rate Limiting**:
- `/sql`: 60 requests/hour
- Dashboard endpoints: Higher limits
- Handle rate limit errors gracefully

### Data Caching Strategy

**Client-side Cache** (React Query / TanStack Query):
```javascript
// Example for standings
useQuery({
  queryKey: ['standings', season],
  queryFn: () => fetchStandings(season),
  staleTime: 5 * 60 * 1000, // 5 minutes
  cacheTime: 30 * 60 * 1000, // 30 minutes
})
```

**Cache Durations**:
- Standings: 5 minutes
- Player stats: 1 hour
- Visualizations: 24 hours (server provides caching)
- Match results: Infinite (historical data doesn't change)
- Live matches: 30 seconds

### State Management

**Use Zustand for Global State**:
```javascript
// lib/store.ts
const useStore = create((set) => ({
  // Active tab
  activeTab: 'dashboard',
  setActiveTab: (tab) => set({ activeTab: tab }),

  // Watchlist
  watchlist: { teams: [], players: [] },
  addToWatchlist: (type, id) => { /* ... */ },

  // Selected entities (for cross-panel filtering)
  selectedTeam: null,
  selectedPlayer: null,
  selectedMatch: null,

  // User preferences
  theme: 'dark',
  preferredMetrics: ['vaep', 'xg', 'point_shares'],
}))
```

### Component Architecture

**Structure**:
```
components/
  dashboard/
    DashboardTab.tsx          - Main container
    LeagueStandings.tsx       - Panel 1
    RecentMatches.tsx         - Panel 2
    ThisWeeksLeaders.tsx      - Panel 3
    PowerRankings.tsx         - Panel 4
    LiveMatches.tsx           - Panel 5
    LeagueAlerts.tsx          - Panel 6
    VisualizationGenerator.tsx - Panel 7
    Watchlist.tsx             - Panel 8
  research/
    ResearchTab.tsx           - Main container
    HypothesisTester.tsx      - Panel 1
    CorrelationExplorer.tsx   - Panel 2
    QueryBuilder.tsx          - Panel 3
    DistributionAnalyzer.tsx  - Panel 4
    CohortComparison.tsx      - Panel 5
    MLSandbox.tsx             - Panel 6
    ResultsDisplay.tsx        - Panel 7
  report/
    ReportTab.tsx             - Main container
    ReportLibrary.tsx         - Panel 1
    ReportViewer.tsx          - Panel 2
    CustomGenerator.tsx       - Panel 3
    ExportControls.tsx        - Panel 4
  shared/
    TerminalTable.tsx         - Reusable table component
    TerminalChart.tsx         - Reusable chart component
    Panel.tsx                 - Base panel wrapper
    PanelHeader.tsx           - Panel title bar
```

### Styling Strategy

**Tailwind + CSS Modules** for Bloomberg aesthetic:

```css
/* styles/terminal.module.css */
.panel {
  background: #0a0a0a;
  border: 1px solid #333;
  color: #ffffff;
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 11px;
}

.panelHeader {
  background: #1a1a1a;
  border-bottom: 1px solid #333;
  padding: 8px 12px;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 10px;
  letter-spacing: 0.5px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  background: #1a1a1a;
  padding: 6px 8px;
  text-align: left;
  border-bottom: 1px solid #333;
  font-size: 9px;
  text-transform: uppercase;
  color: #888;
}

.table td {
  padding: 6px 8px;
  border-bottom: 1px solid #222;
}

.positive {
  color: #00ff00;
}

.negative {
  color: #ff0000;
}

.alert {
  color: #ff8800;
}

.selected {
  background: rgba(0, 136, 255, 0.2);
}
```

### Color Palette

```css
:root {
  --bg-primary: #000000;
  --bg-secondary: #0a0a0a;
  --bg-tertiary: #1a1a1a;
  --border-primary: #333333;
  --border-secondary: #222222;

  --text-primary: #ffffff;
  --text-secondary: #cccccc;
  --text-tertiary: #888888;

  --accent-green: #00ff00;
  --accent-red: #ff0000;
  --accent-orange: #ff8800;
  --accent-blue: #0088ff;

  --highlight: rgba(0, 136, 255, 0.2);
}
```

---

## Success Metrics

### User Engagement
- Time on site per session
- Tab switching frequency
- Tools used per session
- Repeat visitors

### Feature Usage
- Most viewed panels (Dashboard)
- Most used research tools (Research)
- Most downloaded reports (Report)
- Visualization generation frequency

### User Outcomes
- User survey: "Can you make better decisions after using this?"
- Social sharing of insights
- Export/download frequency
- Quoted in articles/broadcasts

---

## Future Enhancements

### Phase 2 (Post-MVP)
- Drag-and-drop panel layouts (customizable dashboards)
- WebSocket live match updates
- User accounts with saved preferences
- Collaborative features (share watchlists)
- Mobile responsive layouts

### Phase 3 (Advanced)
- LLM-generated narrative reports
- Predictive models in DASHBOARD tab
- Historical comparison tools ("2024 vs 2023")
- Custom alert creation
- API access for power users

---

## Design Inspiration Sources

1. **Bloomberg Terminal** - Multi-panel layouts, information density, color coding
2. **Tableau Dashboards** - Interactive filtering, cross-panel connections
3. **Jupyter Notebooks** - Research/exploration workflow
4. **FBref/StatsBomb** - Soccer-specific metrics presentation
5. **Financial dashboards** - Real-time updates, watchlists

---

## Conclusion

The NWSL Terminal Index page transforms users from passive observers into informed analysts through three experientially distinct tabs:

- **DASHBOARD**: Witness facts, understand patterns (tables + visualizations)
- **RESEARCH**: Test hypotheses, validate theories (statistical tools + queries)
- **REPORT**: Consume/generate finished intelligence (narratives + exports)

Each tab leverages your unique technical assets (Point Shares, VAEP, xG models, 9 visualization types, 20 statistical tools) to deliver value no other NWSL platform provides.

Users leave feeling they can **win more games, write better, broadcast better, or coach better** than people who haven't used the platform - because they have access to objective knowledge created through a rigorous, multi-stage process.
