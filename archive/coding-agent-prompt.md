# NWSL Terminal - Coding Agent Implementation Prompt

## Mission

Transform `nwsl-app` into a Bloomberg Terminal-style NWSL analytics platform with three clearly differentiated tabs:

1. **DATA** - Tabular information (standings, stats, rankings)
2. **LAB** - Interactive features (visualizations, testing, experiments)
3. **REPORT** - Written reports and narratives

---

## Key Documents (READ THESE FIRST)

1. **Vision Document**: `/Users/thomasmcmillan/projects/nwsl-notes/data-lab-report-vision.md`
   - Complete specifications for all three tabs
   - Panel layouts and content
   - User experiences and outcomes

2. **Bloomberg Aesthetic Reference**: `/Users/thomasmcmillan/projects/nwsl-notes/bloomberg-terminal-interface-observations.md`
   - Dark theme, high density, color coding
   - Information density principles
   - Professional terminal design

3. **Tab Structure**: `/Users/thomasmcmillan/projects/nwsl-notes/three-tab-structure.md`
   - Quick reference for tab purposes

---

## Project Location

**Codebase**: `/Users/thomasmcmillan/projects/nwsl-app`

**Tech Stack**:
- Next.js 14 (App Router)
- React 18 + TypeScript
- Ant Design + Tailwind CSS
- Zustand (state)
- TanStack Query (data fetching)

---

## Tab Differentiation (Critical!)

### DATA Tab = **Tables**
- Pure information presentation
- Dense Bloomberg-style tables
- 8 panels: Standings, Recent Matches, Power Rankings, etc.
- Minimal interaction (just sorting/filtering)
- User **sees** the numbers

### LAB Tab = **Tools**
- Interactive experimentation
- Forms → Outputs
- Visualization generator, hypothesis tester, SQL query builder
- User **does** experiments

### REPORT Tab = **Documents**
- Written narratives
- Report library + viewer
- Exportable finished intelligence
- User **reads** analysis

---

## Implementation Phases

### Phase 1: Foundation (Start Here)
**Time**: 2-3 days

1. **Create terminal styling system**
   - File: `src/styles/terminal.module.css`
   - Bloomberg color palette (black bg, green/red/orange accents)
   - Reusable classes: `.panel`, `.table`, `.positive`, `.negative`

2. **Set up API client**
   - File: `src/lib/api.ts`
   - Functions for all endpoints (see API Reference below)
   - Base URL: `https://api.nwsldata.com`
   - Error handling, rate limits

3. **Configure React Query**
   - Wrap app with QueryClientProvider
   - Create custom hooks: `useStandings()`, `usePowerRankings()`, etc.
   - Cache times: 5 min (standings), 1 hour (player stats), etc.

4. **Update Zustand store**
   - File: `src/lib/store.ts`
   - State: `activeTab`, `selectedTeam`, `selectedPlayer`, `watchlist`
   - Actions: tab switching, entity selection

5. **Create base components**
   - `src/components/shared/Panel.tsx` - Panel wrapper
   - `src/components/shared/TerminalTable.tsx` - Reusable table
   - `src/components/shared/LoadingSpinner.tsx` - Loading states

6. **Build tab navigation**
   - File: `src/app/page.tsx`
   - Three tabs: DATA, LAB, REPORT
   - Tab switching with Zustand state

---

### Phase 2: DATA Tab (Priority 1)
**Time**: 5-7 days

**Goal**: Implement all 8 panels with real API data

#### Grid Layout
```
┌─────────────────────────────────────────────┐
│  Standings  │  Recent Matches │  Leaders   │
├─────────────────────────────────────────────┤
│  Rankings   │  Live Matches   │  Alerts    │
├─────────────────────────────────────────────┤
│  Team Stats │  Watchlist                   │
└─────────────────────────────────────────────┘
```

#### Implement Panels (In Order)

1. **League Standings** (`LeagueStandings.tsx`)
   - API: `GET /dashboard/team-overview?season=2025`
   - Table: Pos | Team | GP | W | D | L | GF | GA | GD | Pts | Form
   - Color-coded form (WWDLL - green/red/gray)
   - Click team → set `selectedTeam` in store

2. **Recent Matches** (`RecentMatches.tsx`)
   - API: SQL query to `agg_team_match`
   - Table: Date | Home | Score | xG | Away | xG
   - Show xG in smaller text
   - Color-code results

3. **This Week's Leaders** (`ThisWeeksLeaders.tsx`)
   - API: `agg_player_match` filtered by last 7 days
   - Tabs: Goals | Assists | Point Shares | VAEP
   - Top 5 in each

4. **Power Rankings** (`PowerRankings.tsx`)
   - API: `GET /dashboard/player-valuation?season=2025`
   - Table: Rank | Player | Team | VAEP | xG | G+A | PS
   - Sortable columns
   - Position filter

5. **Live Matches** (`LiveMatches.tsx`)
   - Poll every 30s during match windows
   - Show xG timeline, recent events
   - If no live matches: show "Next Match"

6. **League Alerts** (`LeagueAlerts.tsx`)
   - Mock data initially
   - Format: Icon | Headline | Timestamp
   - Color-coded by type

7. **Team Stats** (`TeamStats.tsx`)
   - Season-level team metrics
   - Sortable table

8. **Watchlist** (`Watchlist.tsx`)
   - localStorage for saved teams/players
   - Show recent stats
   - Click to filter dashboard

---

### Phase 3: LAB Tab (Priority 2)
**Time**: 4-5 days

**Goal**: Interactive tools for exploration

#### Panels to Implement

1. **Visualization Generator** (HIGHEST PRIORITY)
   - Dropdowns: Entity, Type (9 options), Season
   - Call nwsl-viz service: `POST /generate_shot_map`
   - Display returned image
   - Export PNG button

2. **Query Builder**
   - SQL editor with syntax highlighting
   - API: `POST /sql`
   - Display results in table
   - Export CSV

3. **Hypothesis Tester**
   - Form: Hypothesis, Group A/B, Metric, Test type
   - Call MCP service: `compare_distributions`
   - Show p-value, effect size, conclusion

4. **Correlation Explorer**
   - Form: X-axis, Y-axis, Method
   - Generate scatter plot with regression line
   - Show r, p-value, R²

5. **ML Sandbox**
   - Tabs: xG Explainer, VAEP Breakdown, PMI Predictor
   - Show feature importance, breakdowns

6. **Experiment Results Panel**
   - Large display area for all LAB outputs
   - Dynamic rendering based on tool used

---

### Phase 4: REPORT Tab (Priority 3)
**Time**: 3-4 days

**Goal**: Report library and viewer

#### Panels to Implement

1. **Report Library**
   - List of pre-written reports (markdown files in `src/data/reports/`)
   - Categories: Weekly, Monthly, Season, Scouting
   - Click to load in viewer

2. **Report Viewer**
   - Render markdown to HTML (`react-markdown`)
   - Clean typography
   - Embedded visualizations

3. **Custom Generator**
   - Form: Type, Subject, Sections
   - Generate from templates + live data

4. **Export Controls**
   - Formats: PDF, PNG, HTML
   - Export current report

---

## API Reference

### Dashboard Endpoints
```
GET /dashboard/lookups                    - Dropdowns (teams, players, seasons)
GET /dashboard/summary?season=2025        - League totals
GET /dashboard/team-overview?season=2025  - Standings
GET /dashboard/player-valuation?season=2025 - Player metrics
GET /dashboard/goalkeepers?season=2025    - GK stats
```

### SQL Endpoint
```
POST /sql
Body: { "query": "SELECT * FROM agg_player_season LIMIT 10" }
Response: { "rows": [...], "columns": [...] }
```

### Visualization Service
```
POST https://nwsl-viz-service.com/generate_shot_map
Body: { "team_name": "Orlando Pride", "season": 2025 }
Response: { "render": { "url": "https://..." }, "data": { "metrics": {...} } }
```

### MCP Statistical Tools
```
POST https://nwsl-mcp-service.com/tools/calculate_correlation
POST https://nwsl-mcp-service.com/tools/compare_cohorts
(20+ tools available)
```

---

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=https://api.nwsldata.com
NEXT_PUBLIC_API_KEY=your_api_key
NEXT_PUBLIC_VIZ_SERVICE_URL=https://nwsl-viz-service.com
NEXT_PUBLIC_MCP_SERVICE_URL=https://nwsl-mcp-service.com
```

---

## Styling Guidelines

### Bloomberg Terminal Aesthetic

**Colors**:
```css
--bg: #000000;
--panel-bg: #0a0a0a;
--panel-header: #1a1a1a;
--border: #333333;

--text: #ffffff;
--text-dim: #888888;

--green: #00ff00;  /* wins, positive */
--red: #ff0000;    /* losses, negative */
--orange: #ff8800; /* alerts */
--blue: #0088ff;   /* selected */
```

**Typography**:
- Font: Monaco, Consolas, Courier New (monospace)
- Sizes: 9-12px (small!)
- Headers: All-caps, bold

**Layout**:
- Dense grids (6-8 panels visible)
- Small padding (4-8px)
- Thin borders (1px)
- Dark theme throughout

---

## Key Implementation Notes

### Cross-Panel Filtering
When user clicks a team in DATA tab:
1. Set `selectedTeam` in Zustand store
2. All panels re-query filtered by that team
3. Show "Filtered to: Orlando Pride" indicator
4. Clear filter button

### Caching Strategy
Use React Query with these cache times:
- Standings: 5 minutes
- Player stats: 1 hour
- Match results: Infinite (historical)
- Live matches: 30 seconds

### Performance
- Lazy load tabs (only render active tab)
- Virtualize long tables (>100 rows)
- Memoize expensive computations
- Skeleton loading states

---

## Success Criteria

Before considering MVP complete:

1. ✅ All three tabs render without errors
2. ✅ DATA tab shows real API data (not mocks)
3. ✅ At least 6/8 DATA panels functional
4. ✅ LAB Visualization Generator works
5. ✅ LAB Query Builder works
6. ✅ REPORT tab can display 3+ reports
7. ✅ Bloomberg aesthetic maintained (dark, dense, color-coded)
8. ✅ Page loads in <2 seconds

---

## Don't Do

❌ Don't modify Notebook page (separate feature)
❌ Don't create new backend APIs (use existing)
❌ Don't add user authentication yet
❌ Don't make it "pretty" - prioritize information density
❌ Don't add animations/transitions (keep it fast)

---

## Development Workflow

1. **Read vision document thoroughly**
2. **Set up environment** (.env.local, npm install)
3. **Start with Phase 1** (foundation - styling, API, state)
4. **Build DATA tab panels one by one**
5. **Test with real API data frequently**
6. **Move to LAB tab** (start with Viz Generator)
7. **Finish with REPORT tab**

---

## Questions?

If stuck:
1. Check vision document first
2. Look at Bloomberg reference for aesthetic guidance
3. Examine existing nwsl-app code for patterns
4. Prioritize **information density** over polish

---

## Final Note

This is a **professional analytics terminal**, not a consumer website.

Prioritize:
- Information density > white space
- Functionality > aesthetics
- Speed > animations
- Data accuracy > visual polish

Users should feel like they're using Bloomberg Terminal or professional trading software, not ESPN.com.

Good luck! 🚀

**Start with**: Phase 1 → DATA Tab Panel 1 (League Standings)
