# NWSL App - Current State Assessment

**Date**: 2025-10-26
**Status**: Three-tab structure implemented, needs panel development

---

## What's Already Built ✅

### Architecture
```
page.tsx
  └─> Dashboard.tsx (main container)
      ├─> TerminalHeader (nav: Index / Notebook)
      ├─> DashboardPage (Index page with 3 tabs)
      │   ├─> DATA tab → IndexPage (4-pane layout)
      │   ├─> LAB tab → Placeholder
      │   └─> REPORT tab → Placeholder
      └─> NotebookPage (separate page)
```

### Completed Components

1. **Three-Tab Navigation** ✅
   - Files: `DashboardPage.tsx`, `DashboardWithTabs.tsx` (duplicate?)
   - Tabs: DATA, LAB, REPORT
   - Tab switching with local state

2. **DATA Tab (Partial)** ⚠️
   - Currently shows `IndexPage.tsx`
   - 4-pane grid layout (A, B, C, D)
   - Mock data displayed
   - Clean Carbon Design System styling
   - **Gap**: Not the 8-panel Bloomberg-style layout from vision

3. **Database Query API** ✅
   - File: `src/app/api/db-query/route.ts`
   - Direct PostgreSQL connection
   - SQL safety checks (SELECT only, blocks dangerous keywords)
   - Connection pooling
   - **This is perfect for the LAB tab Query Builder!**

4. **Existing Terminal Components** ✅
   - `TerminalTable.tsx`
   - `TerminalChart.tsx`
   - `LiveMatches.tsx`
   - `PlayersTable.tsx`
   - `TeamsTable.tsx`
   - These can be reused!

5. **State Management** ✅
   - Zustand store in `lib/store.ts`
   - Already has: `activePanel`, `players`, `teams`, `matches`, `liveData`
   - Needs: `selectedTeam`, `selectedPlayer`, `watchlist`, `activeTab`

---

## What Needs to Be Built 🔨

### Priority 1: DATA Tab (Bloomberg-Style)

**Current**: 4-pane `IndexPage` with mock data
**Target**: 8 dense panels with real API data

#### Replace or Redesign?
**Option A**: Replace `IndexPage` entirely
**Option B**: Keep `IndexPage` as a "multi-pane" view and create separate "table" view

**Recommendation**: **Replace** with 8-panel Bloomberg layout

#### 8 Panels to Build

1. **League Standings** - API ready
2. **Recent Matches** - Can use existing `LiveMatches.tsx`
3. **This Week's Leaders** - Need new component
4. **Power Rankings** - Can adapt `PlayersTable.tsx`
5. **Live Matches** - Use existing `LiveMatches.tsx`
6. **League Alerts** - Mock data initially
7. **Team Stats** - Can adapt `TeamsTable.tsx`
8. **Watchlist** - New component with localStorage

---

### Priority 2: LAB Tab (Interactive Tools)

**Current**: Placeholder
**Target**: 6-7 interactive panels

#### Panels to Build

1. **Visualization Generator** 🔥 HIGHEST VALUE
   - Form: Entity selector, Viz type dropdown, Season selector
   - Call `nwsl-viz` service
   - Display generated image
   - Export button

2. **Query Builder** 🎯 ALREADY HAVE API!
   - SQL editor (Monaco or CodeMirror)
   - Use `/api/db-query` endpoint you just built!
   - Display results in table
   - Export CSV

3. **Hypothesis Tester**
   - Form inputs
   - Call MCP service
   - Display statistical results

4. **Correlation Explorer**
   - Scatter plot generator
   - Use MCP tools

5. **ML Sandbox**
   - xG explainer, VAEP breakdown

6. **Experiment Results Display**
   - Large panel for outputs

---

### Priority 3: REPORT Tab

**Current**: Placeholder
**Target**: Report library + viewer

#### Panels to Build

1. **Report Library** - List of markdown reports
2. **Report Viewer** - Markdown renderer
3. **Custom Generator** - Template-based
4. **Export Controls** - PDF/PNG export

---

## Key Decisions Needed

### 1. DATA Tab Layout
**Question**: Replace current 4-pane `IndexPage` or keep as alternative view?

**Options**:
- A) Replace entirely with 8-panel Bloomberg layout
- B) Add toggle: "Grid View" (current) vs "Table View" (Bloomberg)
- C) Move current `IndexPage` to LAB tab as "Multi-Pane Explorer"

**Recommendation**: **Option A** - Replace for consistency with vision

---

### 2. Duplicate Components
**Issue**: You have both `DashboardPage.tsx` and `DashboardWithTabs.tsx`

**Analysis**:
- Both are identical except for minor styling differences
- `DashboardPage` has fancier tab styling
- `Dashboard.tsx` imports `DashboardPage`

**Recommendation**:
- Delete `DashboardWithTabs.tsx` (not used)
- Keep `DashboardPage.tsx`

---

### 3. Color Scheme
**Current**: Carbon Design System (light theme, IBM colors)
**Vision**: Bloomberg Terminal (dark theme, green/red/orange accents)

**Mismatch**: Current implementation uses light theme, vision specifies dark

**Options**:
- A) Keep light theme, adjust vision
- B) Switch to dark theme per vision
- C) Offer theme toggle

**Recommendation**: Keep light theme for now (cleaner, more accessible), but increase information density to match Bloomberg

---

### 4. API Integration Strategy
**Current**: Mock data in `lib/data.ts`
**Target**: Real API calls

**Immediate Steps**:
1. Update `lib/data.ts` functions to call real APIs
2. Or create new `lib/api.ts` with dedicated API client
3. Use React Query for caching

**You Already Have**:
- `/api/db-query` for SQL
- Need to add:
  - `fetchStandings()` → call `https://api.nwsldata.com/dashboard/team-overview`
  - `fetchPowerRankings()` → call `/dashboard/player-valuation`
  - `fetchVisualization()` → call `nwsl-viz` service

---

## Next Steps (Recommended Order)

### Week 1: DATA Tab Foundation
1. ✅ Delete `DashboardWithTabs.tsx` (duplicate)
2. ✅ Update `lib/store.ts` - add `selectedTeam`, `selectedPlayer`, `watchlist`
3. ✅ Create `lib/api.ts` - real API client functions
4. ✅ Set up React Query in `layout.tsx`

### Week 2: DATA Tab Panels (Part 1)
5. ✅ Build Panel 1: League Standings (real API)
6. ✅ Build Panel 2: Recent Matches
7. ✅ Build Panel 3: This Week's Leaders
8. ✅ Build Panel 4: Power Rankings

### Week 3: DATA Tab Panels (Part 2)
9. ✅ Build Panel 5: Live Matches (adapt existing)
10. ✅ Build Panel 6: League Alerts (mock initially)
11. ✅ Build Panel 7: Team Stats
12. ✅ Build Panel 8: Watchlist

### Week 4: LAB Tab
13. ✅ Build Visualization Generator (calls nwsl-viz service)
14. ✅ Build Query Builder (uses your `/api/db-query`!)
15. ✅ Add Experiment Results display panel

### Week 5: REPORT Tab
16. ✅ Create report markdown files in `src/data/reports/`
17. ✅ Build Report Library + Viewer
18. ✅ Add export functionality

---

## Technical Recommendations

### Use What You Have
- ✅ Your `/api/db-query` is perfect for LAB tab!
- ✅ Reuse `TerminalTable.tsx`, `PlayersTable.tsx`, `TeamsTable.tsx`
- ✅ Adapt `LiveMatches.tsx` for Live Matches panel
- ✅ Zustand store already set up

### Add These Libraries
```bash
npm install react-markdown      # For REPORT tab
npm install @monaco-editor/react # For SQL editor in LAB tab
npm install recharts            # For charts (you might have this)
npm install react-query         # For data fetching with caching
```

### Create These New Files
```
src/lib/api.ts                  # Real API client
src/hooks/useNWSLData.ts        # React Query hooks
src/components/data/            # DATA tab panels
  LeagueStandings.tsx
  RecentMatches.tsx
  ThisWeeksLeaders.tsx
  PowerRankings.tsx
  LiveMatches.tsx
  LeagueAlerts.tsx
  TeamStats.tsx
  Watchlist.tsx
src/components/lab/             # LAB tab panels
  VisualizationGenerator.tsx
  QueryBuilder.tsx
  HypothesisTester.tsx
  ExperimentResults.tsx
src/components/report/          # REPORT tab panels
  ReportLibrary.tsx
  ReportViewer.tsx
  ExportControls.tsx
src/data/reports/               # Markdown reports
  week-24-point-shares.md
  sophia-smith-profile.md
```

---

## Quick Wins 🎯

### You Can Ship These Immediately

1. **LAB Query Builder** - You already have the API!
   - Build simple SQL editor component
   - Connect to `/api/db-query`
   - Display results in table
   - Done!

2. **DATA League Standings** - API exists
   - Call `https://api.nwsldata.com/dashboard/team-overview`
   - Display in `TerminalTable`
   - Done!

3. **DATA Power Rankings** - API exists
   - Call `https://api.nwsldata.com/dashboard/player-valuation`
   - Adapt `PlayersTable.tsx`
   - Done!

---

## Questions for You

1. **DATA tab layout**: Replace current 4-pane view or keep as alternative?
2. **Color scheme**: Keep light theme or switch to dark Bloomberg style?
3. **Implementation approach**:
   - Want me to start building these panels?
   - Or hand off to another coding agent with detailed specs?
4. **Priority**: Which tab should we complete first? (Recommend DATA)

---

## Summary

**Status**: 🟢 Good foundation, clear path forward

**What's Working**:
- Three-tab structure ✅
- Direct database API ✅
- Existing terminal components ✅
- State management ✅

**What Needs Work**:
- DATA tab: Replace 4-pane with 8-panel Bloomberg layout
- LAB tab: Build interactive tools (easy win with Query Builder!)
- REPORT tab: Create report library and viewer
- API integration: Replace mock data with real calls

**Estimated Time to MVP**:
- DATA tab: 2-3 weeks
- LAB tab: 1-2 weeks (Query Builder + Viz Generator)
- REPORT tab: 1 week
- **Total: 4-6 weeks for full implementation**

---

Let me know which direction you want to go and I can start building!
