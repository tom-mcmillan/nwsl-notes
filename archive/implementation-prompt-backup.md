# Implementation Prompt for nwsl-app Coding Agent

## Context

You are working on `nwsl-app`, a Next.js 14 application that serves as a Bloomberg Terminal-style analytics workbench for the NWSL (National Women's Soccer League). The application provides professional-grade analytics combining real-time data, machine learning models (xG, VAEP, Point Shares), spatial visualizations, and statistical research tools.

**Current State**: The app exists at `/Users/thomasmcmillan/projects/nwsl-app` with basic components and mock data. It needs to be redesigned to match the vision document.

**Your Task**: Implement the three-tab structure (Dashboard, Research, Report) with Bloomberg Terminal aesthetic and real API integration.

---

## Vision Document Location

**READ THIS FIRST**: `/Users/thomasmcmillan/projects/nwsl-notes/dashboard-vision.md`

This document contains the complete specification including:
- Tab structure and purposes
- Panel layouts for each tab
- UI specifications for every panel
- API integration points
- Technical implementation notes
- Color palette and styling guidelines

---

## Design Reference

**Bloomberg Terminal Aesthetic**: `/Users/thomasmcmillan/projects/nwsl-notes/bloomberg-terminal-interface-observations.md`

Key principles:
- Dark theme (black background #000000 or #0a0a0a)
- High information density (8-10 panels visible simultaneously)
- Color coding: Green (positive), Red (negative), Orange (alerts), Blue (selected)
- Monospace typography (Monaco, Consolas)
- Zero wasted space - every pixel has purpose

---

## Project Structure

**Current Location**: `/Users/thomasmcmillan/projects/nwsl-app`

**Key Files/Directories**:
```
nwsl-app/
├── src/
│   ├── app/
│   │   ├── page.tsx              - Index page (needs 3-tab structure)
│   │   ├── notebook/page.tsx     - Notebook page (separate, don't touch)
│   │   └── api/                  - API routes (may need new ones)
│   ├── components/
│   │   ├── dashboard/            - Create: Dashboard tab components
│   │   ├── research/             - Create: Research tab components
│   │   ├── report/               - Create: Report tab components
│   │   └── shared/               - Shared components (tables, panels)
│   ├── lib/
│   │   ├── store.ts              - Zustand state management (update)
│   │   ├── api.ts                - API client functions (create/update)
│   │   └── data.ts               - Mock data (replace with real API calls)
│   └── styles/
│       ├── globals.css           - Global styles
│       └── terminal.module.css   - Create: Terminal-specific styles
├── public/
└── package.json
```

**Tech Stack**:
- Next.js 14 (App Router)
- React 18
- TypeScript
- Ant Design + Tailwind CSS
- Zustand (state management)
- TanStack Query / React Query (data fetching)

---

## Implementation Phases

### PHASE 1: Foundation & Infrastructure
**Goal**: Set up tab structure, styling system, and API integration layer

**Tasks**:

1. **Create Terminal Styling System**
   - File: `src/styles/terminal.module.css`
   - Implement Bloomberg color palette (see vision doc)
   - Create reusable classes: `.panel`, `.panelHeader`, `.table`, `.positive`, `.negative`, `.alert`
   - Set up CSS variables for theme colors

2. **Update Global State (Zustand)**
   - File: `src/lib/store.ts`
   - Add state for: `activeTab`, `selectedTeam`, `selectedPlayer`, `watchlist`
   - Add actions for tab switching, entity selection, watchlist management
   - Reference existing implementation, extend as needed

3. **Create API Client Layer**
   - File: `src/lib/api.ts`
   - Functions for each API endpoint:
     - `fetchStandings(season)`
     - `fetchRecentMatches(limit)`
     - `fetchPowerRankings(season, position?)`
     - `fetchPlayerStats(playerId, season)`
     - `executeSQL(query)` - for Research tab
     - `generateVisualization(type, entityId, season)` - calls nwsl-viz service
   - Base URL: `https://api.nwsldata.com`
   - Include error handling and rate limit management

4. **Set Up React Query**
   - File: `src/app/layout.tsx` (wrap with QueryClientProvider)
   - Configure default stale/cache times per vision doc
   - Create custom hooks in `src/hooks/useNWSLData.ts`:
     - `useStandings(season)`
     - `useRecentMatches()`
     - `usePowerRankings(season)`
     - `usePlayerStats(playerId)`

5. **Create Base Components**
   - `src/components/shared/Panel.tsx` - Base panel wrapper with header
   - `src/components/shared/TerminalTable.tsx` - Reusable table with sorting
   - `src/components/shared/TerminalChart.tsx` - Chart wrapper (Recharts)
   - `src/components/shared/LoadingSpinner.tsx` - Loading states

6. **Update Index Page Structure**
   - File: `src/app/page.tsx`
   - Create tab navigation: `<Tabs>` with Dashboard, Research, Report
   - Use Ant Design Tabs or custom tab component
   - Render active tab content based on Zustand state
   - Bloomberg-style header with "NWSL TERMINAL" branding

---

### PHASE 2: Dashboard Tab (Priority 1)
**Goal**: Implement all 8 panels of the Dashboard tab with real data

**Tasks**:

1. **Create Dashboard Tab Container**
   - File: `src/components/dashboard/DashboardTab.tsx`
   - Grid layout for 8 panels (see vision doc for layout)
   - Responsive grid (CSS Grid or Tailwind grid)

2. **Panel 1: League Standings**
   - File: `src/components/dashboard/LeagueStandings.tsx`
   - API: `GET /dashboard/team-overview?season=2025`
   - Columns: Pos, Team, GP, W, D, L, GF, GA, GD, Pts, Form
   - Color-coded form badges (W=green, L=red, D=gray)
   - Sortable columns
   - Click team → update global state `selectedTeam`

3. **Panel 2: Recent Matches**
   - File: `src/components/dashboard/RecentMatches.tsx`
   - API: SQL query to `agg_team_match` for last 10 matches
   - Display: Date, Home, Score, xG, Away, xG, Venue
   - Color-code results (home win = green home team, etc.)
   - Show xG in smaller text below score

4. **Panel 3: This Week's Leaders**
   - File: `src/components/dashboard/ThisWeeksLeaders.tsx`
   - API: Query `agg_player_match` filtered by last 7 days
   - Tabs: Goals, Assists, Point Shares, VAEP
   - Top 5 in each category
   - Click player → update global state `selectedPlayer`

5. **Panel 4: Power Rankings**
   - File: `src/components/dashboard/PowerRankings.tsx`
   - API: `GET /dashboard/player-valuation?season=2025`
   - Columns: Rank, Player, Team, Pos, VAEP, xG, G+A, PS, Per90
   - Sortable by any metric
   - Position filter (FW/MF/DF/GK)
   - Color-code VAEP (green if above avg, red if below)

6. **Panel 5: Live Matches**
   - File: `src/components/dashboard/LiveMatches.tsx`
   - API: Query `fact_event` for live matches (poll every 30s with React Query)
   - Display: Score, minute, xG timeline (horizontal bars), recent events
   - If no live matches: show "Next Match" with date/time
   - Orange pulsing indicator for live minute

7. **Panel 6: League Alerts**
   - File: `src/components/dashboard/LeagueAlerts.tsx`
   - Mock data initially (create `src/data/mockAlerts.ts`)
   - Display: Icon (🔴 injury, 🟢 milestone, 🟠 transfer), headline, timestamp
   - Color-coded by type
   - Future: Create `league_alerts` table and API

8. **Panel 7: Visualization Generator**
   - File: `src/components/dashboard/VisualizationGenerator.tsx`
   - Dropdowns: Entity (player/team), Type (9 viz types), Season
   - "Generate" button calls nwsl-viz service
   - API: `POST https://nwsl-viz-service.com/generate_{type}`
   - Display returned image URL
   - Show metrics below image (from API response)
   - Export button (download PNG)
   - Loading state during generation (300-500ms)

9. **Panel 8: Watchlist**
   - File: `src/components/dashboard/Watchlist.tsx`
   - Store in Zustand state + localStorage
   - Display teams and players with recent stats
   - Add/remove buttons
   - Click item → filters entire dashboard to that entity
   - Max 5 teams, 10 players

---

### PHASE 3: Research Tab (Priority 2)
**Goal**: Implement statistical research tools using MCP service

**Tasks**:

1. **Create Research Tab Container**
   - File: `src/components/research/ResearchTab.tsx`
   - Grid layout for 7 panels (see vision doc)
   - Large Results Display panel at bottom

2. **Panel 1: Hypothesis Tester**
   - File: `src/components/research/HypothesisTester.tsx`
   - Form: Hypothesis text, Group A/B dropdowns, Metric dropdown, Test type
   - API: Call MCP tool `compare_distributions` or `compare_entities`
   - Output to Results Display: t-statistic, p-value, effect size, interpretation

3. **Panel 2: Correlation Explorer**
   - File: `src/components/research/CorrelationExplorer.tsx`
   - Form: X-axis metric, Y-axis metric, Cohort, Method (Pearson/Spearman)
   - API: Call MCP tool `calculate_correlation`
   - Output: r, p-value, R², scatter plot with regression line
   - Use Recharts for scatter plot

4. **Panel 3: Query Builder**
   - File: `src/components/research/QueryBuilder.tsx`
   - SQL editor with syntax highlighting (CodeMirror or Monaco)
   - Template dropdown (common queries)
   - Execute button → API: `POST /sql`
   - Display results in table
   - Export CSV button
   - Show execution time, row count

5. **Panel 4: Distribution Analyzer**
   - File: `src/components/research/DistributionAnalyzer.tsx`
   - Form: Metric, Cohort, Optional player highlight
   - API: Call MCP tool `calculate_distribution` + `calculate_percentile_rank`
   - Output: Summary stats, normality tests, percentiles, histogram
   - Highlight player position on histogram

6. **Panel 5: Cohort Comparison**
   - File: `src/components/research/CohortComparison.tsx`
   - Form: Metric, Multiple cohorts (multi-select), Test type (ANOVA/Kruskal-Wallis)
   - API: Call MCP tool `compare_cohorts`
   - Output: Group statistics, ANOVA results, post-hoc tests, box plots

7. **Panel 6: ML Sandbox**
   - File: `src/components/research/MLSandbox.tsx`
   - Tabs: xG Explainer, VAEP Breakdown, PMI Predictor
   - xG Explainer: Show feature importance for selected shot
   - VAEP Breakdown: Show offensive/defensive VAEP split by action type
   - PMI Predictor: Input player stats, predict match outcome
   - Load ML artifacts or call API endpoints

8. **Panel 7: Results Display**
   - File: `src/components/research/ResultsDisplay.tsx`
   - Large panel, initially empty
   - Dynamically renders output from other research tools
   - Formatted statistical results (tables, charts)
   - Export buttons (CSV, PNG)

---

### PHASE 4: Report Tab (Priority 3)
**Goal**: Create report library and custom report generator

**Tasks**:

1. **Create Report Tab Container**
   - File: `src/components/report/ReportTab.tsx`
   - Layout: Report Library (left), Report Viewer (center, large), Export Controls (bottom-right)

2. **Panel 1: Report Library**
   - File: `src/components/report/ReportLibrary.tsx`
   - Create mock reports in `src/data/reports/` (markdown files)
   - Categories: Weekly, Monthly, Season, Scouting
   - Click report → loads in Report Viewer
   - Search and filter functionality

3. **Panel 2: Report Viewer**
   - File: `src/components/report/ReportViewer.tsx`
   - Render markdown to HTML (use `react-markdown`)
   - Embed visualizations from nwsl-viz
   - Professional typography (serif body, sans data)
   - Print-friendly layout

4. **Panel 3: Custom Generator**
   - File: `src/components/report/CustomGenerator.tsx`
   - Form: Report type, Subject, Date range, Sections (checkboxes)
   - Templates for: Player Scouting, Team Analysis, Match Recap
   - Generate button → populate template with live data
   - Render to Report Viewer

5. **Panel 4: Export Controls**
   - File: `src/components/report/ExportControls.tsx`
   - Export formats: PDF, PNG, HTML, Markdown
   - Quality settings
   - Email report button (future)
   - Use browser print API or jsPDF for PDF generation

6. **Create Report Templates**
   - Files: `src/templates/player-scouting.md`, `team-analysis.md`, etc.
   - Markdown with placeholders: `{{player.name}}`, `{{player.vaep}}`
   - Template engine to populate with data

---

### PHASE 5: Polish & Integration
**Goal**: Cross-panel communication, responsive design, performance optimization

**Tasks**:

1. **Cross-Panel Filtering**
   - When user clicks team in Standings → filter all panels to that team
   - When user clicks player in Leaders → filter all panels to that player
   - Use Zustand state (`selectedTeam`, `selectedPlayer`)
   - Visual indicator showing active filter (e.g., "Filtered to: Orlando Pride")

2. **Responsive Design**
   - Ensure panels stack vertically on mobile
   - Adjust font sizes for readability
   - Collapsible panels on small screens
   - Test on tablet and mobile

3. **Loading States**
   - Skeleton screens for panels while loading
   - Error boundaries for failed API calls
   - Retry logic for rate-limited requests

4. **Performance Optimization**
   - Lazy load tab content (only render active tab)
   - Virtualize long tables (react-window)
   - Optimize chart rendering
   - Memoize expensive computations

5. **Accessibility**
   - Keyboard navigation for tabs
   - ARIA labels for panels
   - Focus management
   - Color contrast checks (ensure readability on dark theme)

6. **Testing**
   - Unit tests for API client functions
   - Component tests for key panels
   - Integration tests for tab switching
   - E2E tests for critical user flows

---

## API Endpoints Reference

### Dashboard Endpoints
```
GET /dashboard/lookups                    - Seasons, teams, players, matches
GET /dashboard/summary?season=2025        - League headline metrics
GET /dashboard/team-overview?season=2025  - Standings + stats
GET /dashboard/player-valuation?season=2025 - Player metrics
GET /dashboard/player-style?player_id=123  - Style profiles
GET /dashboard/goalkeepers?season=2025    - GK metrics
```

### SQL Endpoint
```
POST /sql
Body: { "query": "SELECT * FROM agg_player_season LIMIT 10" }
Headers: { "Authorization": "Bearer API_KEY" }
```

### Visualization Service
```
POST https://nwsl-viz-service.com/generate_shot_map
Body: { "team_name": "Orlando Pride", "season": 2025 }
Response: { "render": { "url": "https://storage.googleapis.com/..." } }
```

### MCP Tools (Statistical Research)
```
POST https://nwsl-mcp-service.com/tools/calculate_correlation
POST https://nwsl-mcp-service.com/tools/compare_cohorts
POST https://nwsl-mcp-service.com/tools/calculate_distribution
(20 total tools available - see nwsl-mcp-py README)
```

---

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=https://api.nwsldata.com
NEXT_PUBLIC_API_KEY=your_api_key_here
NEXT_PUBLIC_VIZ_SERVICE_URL=https://nwsl-viz-service.com
NEXT_PUBLIC_MCP_SERVICE_URL=https://nwsl-mcp-service.com
```

---

## Key Decisions & Constraints

### Must-Haves
1. **Bloomberg aesthetic** - Dark theme, high density, monospace fonts, color coding
2. **Real API integration** - Replace all mock data with live API calls
3. **Three-tab structure** - Dashboard, Research, Report
4. **8 panels in Dashboard** - All specified in vision doc
5. **Responsive but desktop-first** - Optimized for wide screens, graceful degradation

### Nice-to-Haves (Future Phases)
1. Drag-and-drop panel layouts
2. WebSocket live updates
3. User accounts with saved preferences
4. LLM-generated narratives
5. Mobile app

### Don't Do
1. Don't modify Notebook page (separate feature)
2. Don't create backend APIs (use existing endpoints)
3. Don't implement user authentication yet (use public API key)
4. Don't add animations/transitions (keep it fast and functional)

---

## Implementation Order (Recommended)

1. **Start with Foundation** (Phase 1) - 2-3 days
   - Styling system, API client, state management
   - Get basic tab structure working

2. **Dashboard Tab** (Phase 2) - 5-7 days
   - Implement panels in order (1-8)
   - Start with simple tables, add visualizations later
   - This is the most important tab - get it right

3. **Research Tab** (Phase 3) - 4-5 days
   - Focus on Hypothesis Tester and Query Builder first
   - Other tools can be simplified versions initially

4. **Report Tab** (Phase 4) - 3-4 days
   - Start with Report Viewer and Library
   - Custom Generator can be Phase 2 enhancement

5. **Polish** (Phase 5) - 2-3 days
   - Cross-panel filtering, responsive design, testing

**Total Estimated Time**: 16-22 days

---

## Success Criteria

### Must Pass Before Launch
1. ✅ All three tabs render without errors
2. ✅ Dashboard tab shows real data from API (not mocks)
3. ✅ At least 6/8 Dashboard panels fully functional
4. ✅ Research tab Query Builder works
5. ✅ Report tab can display at least 3 pre-written reports
6. ✅ Bloomberg aesthetic maintained (dark theme, color coding, density)
7. ✅ No console errors or warnings
8. ✅ Page loads in <2 seconds on desktop

### Bonus Points
1. 🌟 All 8 Dashboard panels fully functional
2. 🌟 Visualization Generator working with real nwsl-viz service
3. 🌟 Statistical tools in Research tab operational
4. 🌟 Cross-panel filtering working
5. 🌟 Responsive design for tablet

---

## Questions & Clarifications

If you encounter ambiguity:
1. Check vision document first: `/Users/thomasmcmillan/projects/nwsl-notes/dashboard-vision.md`
2. Check Bloomberg reference: `/Users/thomasmcmillan/projects/nwsl-notes/bloomberg-terminal-interface-observations.md`
3. Refer to existing `nwsl-app` code for patterns
4. When in doubt: prioritize information density and simplicity over fancy UI

---

## Getting Started

1. **Read the vision document thoroughly**
2. **Explore existing nwsl-app codebase** to understand current structure
3. **Set up environment** (.env.local with API keys)
4. **Start with Phase 1** (Foundation)
5. **Implement Dashboard panels one by one** (Phase 2)
6. **Test frequently** with real data

---

## Final Notes

This is a professional analytics platform, not a consumer website. Prioritize:
- **Information density** over white space
- **Functionality** over aesthetics
- **Data accuracy** over visual polish
- **Performance** over fancy animations

The goal: Users should feel like they have a professional-grade research tool that gives them insights unavailable anywhere else.

Good luck! 🚀
