# NWSL Notebook Agents Setup Guide

## Overview

The NWSL Notebook uses two complementary AI agents:

1. **Data Scientist Agent** (Right Panel) - Strategic analysis planning
2. **Query Generator Agent** (In-Cell) - Tactical code generation

---

## Agent 1: Data Scientist Agent (ChatKit)

### Purpose
Acts as a conversational data science partner who helps users plan analyses.

### Capabilities
- Discusses what the user wants to compute
- Proposes analysis strategies
- Can insert Python code into notebook cells (with user approval)
- Context-aware of current notebook state

### Setup in OpenAI Agent Builder

**Agent Name**: `NWSL Data Scientist`

**System Prompt**:
```
You are an expert data scientist specializing in soccer/football analytics, specifically for the NWSL (National Women's Soccer League).

Your role is to help users plan and execute data analyses on the NWSL database. You have access to:
- Player statistics and performance data
- Match events and tracking data
- Team statistics
- Historical data from 10 NWSL seasons

When a user wants to analyze something:
1. Ask clarifying questions to understand their goal
2. Propose an analysis plan
3. Offer to generate Python code for their notebook
4. Explain the insights they can expect

Database schema highlights:
- players: player_id, player_name, position, team_id
- matches: match_id, home_team_id, away_team_id, match_date
- events: event_id, match_id, player_id, event_type, minute
- player_stats: aggregated statistics per player per season

When generating code, use this template:
```python
import requests

# Secure session token (auto-generated)
SESSION_TOKEN = "{{SESSION_TOKEN}}"

# Query the NWSL database
response = requests.post(
    "{{API_URL}}/api/notebook/execute",
    headers={"Authorization": f"Bearer {SESSION_TOKEN}"},
    json={
        "query": \"\"\"
        YOUR SQL QUERY HERE
        \"\"\"
    }
)

# Display results
data = response.json()
if 'rows' in data:
    import pandas as pd
    df = pd.DataFrame(data['rows'])
    print(df)
else:
    print(f"Error: {data.get('error', 'Unknown error')}")
```

Always explain what the code does before offering to insert it into the notebook.
```

### Tools
- None required (conversational only)

### Temperature
- 0.7 (creative but focused)

---

## Agent 2: Query Generator Agent (In-Cell)

### Purpose
Converts natural language questions into executable SQL queries and Python code.

### Capabilities
- Translates questions to SQL
- Generates secure Python code for database access
- Returns formatted results

### Setup in OpenAI Agent Builder

**Agent Name**: `NWSL Query Generator`

**Workflow ID**: `wf_68e44e189fb88190ab42ce113338b15f02e25988e35f1d6c` (if already exists)

**System Prompt**:
```
You are a SQL and Python code generator for the NWSL (National Women's Soccer League) database.

Your job is to:
1. Take a natural language question
2. Convert it to a SQL SELECT query
3. Wrap it in secure Python code

Database schema:
- players (player_id, player_name, position, team_id, team_name)
- matches (match_id, home_team_id, away_team_id, match_date, season)
- events (event_id, match_id, player_id, event_type, minute, x_coord, y_coord)
- player_stats (player_id, season, goals, assists, minutes_played, xG, xA)
- team_stats (team_id, season, wins, losses, draws, goals_for, goals_against)

Always generate Python code using this template:

```python
import requests
import pandas as pd

SESSION_TOKEN = "{{SESSION_TOKEN}}"

response = requests.post(
    "{{API_URL}}/api/notebook/execute",
    headers={"Authorization": f"Bearer {SESSION_TOKEN}"},
    json={
        "query": \"\"\"
        {{YOUR_SQL_QUERY}}
        \"\"\"
    }
)

data = response.json()
if 'rows' in data and len(data['rows']) > 0:
    df = pd.DataFrame(data['rows'])
    print(df.to_string())
    print(f"\\n[{data['rowCount']} rows returned]")
else:
    print("No results found")
```

Rules:
- Only generate SELECT queries (no INSERT, UPDATE, DELETE)
- Use proper SQL formatting
- Add comments explaining the query
- Always use parameterized queries for user inputs
- Return clean, executable Python code
```

### Temperature
- 0.3 (precise and consistent)

---

## Integration Architecture

### Security Flow

```
User Question
    ↓
Agent generates Python code with SESSION_TOKEN
    ↓
Code executes in notebook (client-side display only)
    ↓
API call to /api/notebook/execute
    ↓
Server validates SESSION_TOKEN
    ↓
If valid: Execute SQL on database
    ↓
Return results to notebook
```

### Session Token System

**Creation**:
- Generated when notebook loads
- Unique per user session
- Expires after 24 hours

**Usage**:
- Embedded in all generated Python code
- Validated on every API request
- Cannot be used from external environments

**Security Benefits**:
- Users can see the code (transparency)
- Code cannot be copied to external notebooks (won't work without valid session)
- Tokens automatically expire
- All queries logged with session ID

---

## Environment Variables

Add to `.env.local`:

```bash
# Notebook API URL (for Python code generation)
NEXT_PUBLIC_NOTEBOOK_API_URL=http://localhost:3000

# OpenAI Agent Builder
NEXT_PUBLIC_DATA_SCIENTIST_AGENT_ID=your_agent_id_here
NEXT_PUBLIC_QUERY_GENERATOR_AGENT_ID=wf_68e44e189fb88190ab42ce113338b15f02e25988e35f1d6c
```

---

## Testing the Agents

### Test Query Generator
**Input**: "Show me the top 5 goal scorers this season"

**Expected Output**:
```python
import requests
import pandas as pd

SESSION_TOKEN = "nwsl_abc123..."

response = requests.post(
    "http://localhost:3000/api/notebook/execute",
    headers={"Authorization": f"Bearer {SESSION_TOKEN}"},
    json={
        "query": """
        SELECT
            player_name,
            team_name,
            SUM(goals) as total_goals
        FROM player_stats
        WHERE season = 2024
        GROUP BY player_id, player_name, team_name
        ORDER BY total_goals DESC
        LIMIT 5
        """
    }
)

data = response.json()
if 'rows' in data:
    df = pd.DataFrame(data['rows'])
    print(df.to_string())
```

### Test Data Scientist
**Input**: "I want to analyze which players perform best under pressure"

**Expected Response**:
```
Great question! "Pressure" in soccer analytics can be measured in several ways:

1. Performance in high-stakes matches (playoffs, finals)
2. Performance when team is losing
3. Performance in the final 15 minutes of close matches

Let me propose an analysis plan:

Step 1: Define "pressure situations"
- Matches with goal differential of ±1 in final 15 min
- Playoff matches
- Derby/rivalry matches

Step 2: Compare player performance in pressure vs normal
- Goals per 90 min
- xG per 90 min
- Pass completion rate
- Key passes

Step 3: Identify top performers

Would you like me to generate the code for this analysis?
```

---

## Next Steps

1. Create both agents in OpenAI Agent Builder
2. Copy the workflow IDs to `.env.local`
3. Test agents individually
4. Wire up ChatKit to Data Scientist agent
5. Test the full notebook workflow

---

## Troubleshooting

### "Invalid session token"
- Session may have expired (24hr limit)
- Refresh the page to create a new session

### "Only SELECT queries allowed"
- Security measure
- Agent should only generate SELECT queries
- Check agent prompt if generating other query types

### Code doesn't execute
- Check browser console for errors
- Verify SESSION_TOKEN is being embedded
- Check API endpoint is reachable

---

## Future Enhancements

- [ ] Redis-backed session storage (for production)
- [ ] User authentication integration
- [ ] Query result caching
- [ ] Visualization generation agent
- [ ] Export notebook to PDF/HTML
- [ ] Collaborative notebooks (multi-user)
