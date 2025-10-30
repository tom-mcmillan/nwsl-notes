# NWSL Terminal - DATA, LAB, REPORT Vision

**Version**: 2.0
**Date**: 2025-10-25
**Tab Structure**: DATA → LAB → REPORT

---

## Overview

The NWSL Terminal Index page uses three clearly differentiated tabs:

1. **DATA** - Tabular information (standings, stats, rankings)
2. **LAB** - Interactive features and experiments (visualizations, testing, analysis)
3. **REPORT** - Written reports and narratives (finished intelligence)

Each tab offers a fundamentally different experience - not just different data, but different **modes of interaction**.

---

## Design Philosophy

### Clear Differentiation

**DATA** = **What you see**: Tables of numbers
- Pure information presentation
- Scanning and lookup
- No interaction beyond sorting/filtering
- Bloomberg-style dense tables

**LAB** = **What you do**: Tools and experiments
- Active hands-on exploration
- Generate, test, analyze
- Interactive controls and forms
- Playful experimentation

**REPORT** = **What you read**: Written narratives
- Finished analysis and insights
- Consumption, not creation
- Exportable intelligence
- Briefing-style documents

---

## TAB 1: DATA

### Tagline
**"See the numbers - standings, stats, rankings"**

### User Experience
- Scanning tables
- Looking up specific stats
- Monitoring league state
- Watching live scores

### Key Principle
**Information density** - Pack as much data as possible into view without scrolling

---

### DATA Tab Layout (8 Panels)

```
┌──────────────────────────────────────────────────────────────────────┐
│  LEAGUE STANDINGS   │  RECENT MATCHES      │  THIS WEEK'S LEADERS   │
├──────────────────────────────────────────────────────────────────────┤
│  POWER RANKINGS     │  LIVE MATCHES        │  LEAGUE ALERTS         │
├──────────────────────────────────────────────────────────────────────┤
│  TEAM STATS         │  WATCHLIST                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### Panel Specifications

#### 1. League Standings
**Format**: Table
**Columns**: Pos | Team | GP | W | D | L | GF | GA | GD | Pts | Form
**Features**:
- Color-coded form (WWDLL with green W, red L, gray D)
- Sortable columns
- Season selector
- Click team → filters other panels

#### 2. Recent Matches
**Format**: Table
**Columns**: Date | Home | Score | xG | Away | xG | Venue
**Features**:
- Last 10-20 matches
- xG shown in smaller text
- Color-coded results
- Click match → match detail view (future)

#### 3. This Week's Leaders
**Format**: Tabbed mini-tables
**Tabs**: Goals | Assists | Point Shares | VAEP
**Display**: Top 5 in each category from last 7 days
**Features**: Click player → filters other panels

#### 4. Power Rankings
**Format**: Table
**Columns**: Rank | Player | Team | Pos | VAEP | xG | G+A | PS | Per90
**Features**:
- Full season leaderboard
- Position filter (FW/MF/DF/GK)
- Sortable by any metric
- Color-coded VAEP (green above avg, red below)

#### 5. Live Matches
**Format**: Live feed
**Display**:
- Current score and minute
- xG timeline (horizontal bars)
- Recent events (goals, cards, subs)
- If no live matches: "Next Match" info

#### 6. League Alerts
**Format**: Alert list
**Display**: Icon | Headline | Timestamp
**Types**: 🔴 Injuries, 🟢 Milestones, 🟠 Transfers, 🔵 Roster moves
**Features**: Color-coded, reverse chronological

#### 7. Team Stats
**Format**: Table
**Columns**: Team | Possession % | Shots/Game | xG/Game | Pass % | etc.
**Purpose**: Team-level performance metrics
**Features**: Sortable, full season data

#### 8. Watchlist
**Format**: Custom list
**Display**: User's saved teams and players with recent stats
**Features**: Add/remove, localStorage persistence, click to filter

---

## TAB 2: LAB

### Tagline
**"Test your theories - explore, visualize, analyze"**

### User Experience
- Generating visualizations
- Testing hypotheses
- Running experiments
- Querying custom data
- Interpreting ML models

### Key Principle
**Interactivity** - User controls inputs, system generates outputs

---

### LAB Tab Layout (7 Panels)

```
┌────────────────────────────────────────────────────────────────┐
│  VISUALIZATION GENERATOR           │  HYPOTHESIS TESTER       │
├────────────────────────────────────────────────────────────────┤
│  CORRELATION EXPLORER │  QUERY BUILDER  │  ML SANDBOX         │
├────────────────────────────────────────────────────────────────┤
│  EXPERIMENT RESULTS (Large display panel)                     │
└────────────────────────────────────────────────────────────────┘
```

### Panel Specifications

#### 1. Visualization Generator
**Type**: Form → Image
**Inputs**:
- Entity selector (player/team)
- Viz type (9 options: shot map, heatmap, pass network, etc.)
- Season selector

**Output**: Generated pitch visualization from nwsl-viz service
**Features**: Export PNG, show metrics

#### 2. Hypothesis Tester
**Type**: Form → Statistical test
**Inputs**:
- Hypothesis text
- Group A / Group B
- Metric
- Test type (t-test, Mann-Whitney U, etc.)

**Output**: p-value, effect size, conclusion
**Display in**: Experiment Results panel

#### 3. Correlation Explorer
**Type**: Form → Scatter plot + statistics
**Inputs**:
- X-axis metric
- Y-axis metric
- Cohort filter
- Method (Pearson/Spearman)

**Output**: r, p-value, scatter plot with regression line
**Display in**: Experiment Results panel

#### 4. Query Builder
**Type**: SQL editor → Table results
**Inputs**:
- SQL text area (syntax highlighting)
- Template selector
- Row limit

**Output**: Query results in table format
**Features**: Export CSV, execution time display

#### 5. ML Sandbox
**Type**: Tabbed interactive tools
**Tabs**:
- **xG Explainer**: Input shot details → see feature importance
- **VAEP Breakdown**: Select player → see offensive/defensive split
- **PMI Predictor**: Input player stats → predict match outcome

**Display in**: Experiment Results panel

#### 6. Distribution Analyzer
**Type**: Form → Histogram + stats
**Inputs**:
- Metric
- Cohort
- Optional player highlight

**Output**: Mean, median, percentiles, histogram
**Display in**: Experiment Results panel

#### 7. Experiment Results
**Type**: Dynamic output display
**Purpose**: Large panel showing outputs from all LAB tools
**Features**:
- Statistical test results
- Charts and plots
- Tables
- Export buttons (CSV, PNG)

---

## TAB 3: REPORT

### Tagline
**"Read the briefing - curated insights and analysis"**

### User Experience
- Reading pre-written analysis
- Consuming narrative insights
- Generating custom reports
- Exporting finished products

### Key Principle
**Narratives** - Written intelligence with embedded data/visuals

---

### REPORT Tab Layout (4 Panels)

```
┌──────────────────────────────────────────────────────────────────┐
│  REPORT LIBRARY       │  REPORT VIEWER (Large, 2x width)        │
├──────────────────────────────────────────────────────────────────┤
│  CUSTOM GENERATOR     │  EXPORT CONTROLS                         │
└──────────────────────────────────────────────────────────────────┘
```

### Panel Specifications

#### 1. Report Library
**Type**: Categorized list
**Categories**:
- Weekly Reports (Point Shares leaders, match recaps)
- Monthly Reports (State of the league, tactical trends)
- Season Reports (Mid-season review, playoffs preview)
- Scouting Reports (Player profiles, team analysis)

**Features**: Search, filter, date sorting

#### 2. Report Viewer
**Type**: Document display
**Format**: Markdown → HTML with embedded:
- Tables
- Visualizations
- Statistical callouts
- Narrative text

**Features**: Clean typography, print-friendly

#### 3. Custom Generator
**Type**: Form → Generated report
**Inputs**:
- Report type (player scouting, team analysis, match recap)
- Subject (player/team name)
- Date range
- Sections to include (checkboxes)

**Output**: Auto-generated report from templates + live data
**Display in**: Report Viewer

#### 4. Export Controls
**Type**: Export options
**Formats**: PDF, PNG, HTML, Markdown
**Features**: Quality settings, watermark options

---

## Visual Design System

### Bloomberg Terminal Aesthetic

**Color Palette**:
```css
--bg-primary: #000000;
--bg-secondary: #0a0a0a;
--bg-panel: #1a1a1a;
--border: #333333;

--text-primary: #ffffff;
--text-secondary: #cccccc;
--text-dim: #888888;

--green: #00ff00;  /* positive, win */
--red: #ff0000;    /* negative, loss */
--orange: #ff8800; /* alerts, warnings */
--blue: #0088ff;   /* selected, highlights */
--gray: #666666;   /* draws, neutral */
```

**Typography**:
- Monospace: Monaco, Consolas, Courier New
- Headers: 10-12px, all-caps, bold
- Body: 9-11px
- Data: Tabular numerals

**Information Density**:
- Small fonts
- Tight padding (4-8px)
- Minimal margins
- Every pixel has purpose

---

## Tab Visual Identity

### DATA Tab
- **Color accent**: Blue (#0088ff)
- **Icon**: 📊 (bar chart)
- **Vibe**: Serious, professional, dense
- **Interaction**: Minimal (sorting, filtering only)

### LAB Tab
- **Color accent**: Green (#00ff00)
- **Icon**: 🧪 (test tube)
- **Vibe**: Experimental, playful, exploratory
- **Interaction**: High (forms, buttons, generators)

### REPORT Tab
- **Color accent**: Orange (#ff8800)
- **Icon**: 📄 (document)
- **Vibe**: Polished, narrative, consumable
- **Interaction**: Medium (reading, exporting)

---

## User Journeys

### Casual Fan
1. Opens **DATA** → sees standings, recent results
2. Curious about a player → checks Power Rankings
3. Wants to see visually → switches to **LAB** → generates shot map
4. Impressed, wants to share → **REPORT** → exports player profile

### Journalist
1. Starts in **DATA** → checks This Week's Leaders for article inspiration
2. Needs statistical proof → **LAB** → runs hypothesis test
3. Generates custom visualizations → exports
4. Writes article with data-backed insights

### Coach
1. **DATA** → checks opponent's recent stats
2. **LAB** → generates opponent's pass network and heatmap
3. **LAB** → tests "Do they perform worse in rain?" (hypothesis tester)
4. **REPORT** → reads scouting report on opponent's key player
5. Develops game plan based on insights

### Analyst/Researcher
1. **LAB** → runs correlation analyses
2. **LAB** → custom SQL queries to extract data
3. **LAB** → statistical tests for paper
4. Exports data and results

---

## Technical Stack

### Frontend
- Next.js 14 (App Router)
- React 18, TypeScript
- Ant Design + Tailwind CSS
- Zustand (state management)
- TanStack Query (data fetching)

### APIs
- `https://api.nwsldata.com` - Data endpoints
- `nwsl-viz` - Visualization generation
- `nwsl-mcp-py` - Statistical tools

### Styling
- CSS Modules for terminal styles
- Tailwind for layout
- CSS variables for theming

---

## Implementation Priority

### Phase 1: DATA Tab (Most Important)
- 8 panels with real API data
- Bloomberg aesthetic
- Cross-panel filtering

### Phase 2: LAB Tab
- Visualization Generator (highest value)
- Query Builder (power users)
- Hypothesis Tester (unique differentiator)
- Other tools can be simplified initially

### Phase 3: REPORT Tab
- Report Library with 5-10 sample reports
- Report Viewer with good typography
- Custom Generator can be Phase 2 enhancement

---

## Success Metrics

### User Outcomes
- "I can quote stats after using DATA tab"
- "I can generate custom visualizations in LAB tab"
- "I can export finished analysis from REPORT tab"
- "I feel like a professional analyst"

### Technical Metrics
- Page load < 2 seconds
- Tab switch < 100ms
- Visualization generation < 500ms (cached < 100ms)
- API calls cached appropriately

---

## Key Differentiators

What makes this different from other sports analytics sites:

1. **DATA tab**: Bloomberg-level information density (8 panels visible simultaneously)
2. **LAB tab**: Interactive exploration not possible elsewhere (9 viz types, 20+ statistical tools)
3. **REPORT tab**: Finished intelligence products ready to use
4. **Unique metrics**: Point Shares, VAEP, Bayesian xG
5. **Professional tools**: SQL queries, hypothesis testing, ML sandboxes

Users leave thinking: "This is a professional research platform, not just a stats website."

---

## Final Notes

### Naming Clarity
- **DATA** = See it (passive viewing)
- **LAB** = Do it (active experimentation)
- **REPORT** = Read it (narrative consumption)

This is crystal clear to users - no ambiguity about what to expect from each tab.

The progression is natural:
1. Start with **DATA** to get informed
2. Explore deeper with **LAB** to test theories
3. Consume polished insights in **REPORT** or export your own

🎯 Clear. Differentiated. Professional. Fun.
