# NWSL Data Platform Architecture Diagrams

## Diagram 1: System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      🌐 EXTERNAL DATA SOURCES                               │
├─────────────────────────────────┬───────────────────────────────────────────┤
│  ┌──────────────────────────┐   │   ┌──────────────────────────┐           │
│  │   Opta Sports API        │   │   │   FootyStats API         │           │
│  │   Event Data             │   │   │   Match Metadata         │           │
│  └────────────┬─────────────┘   │   └────────────┬─────────────┘           │
└───────────────┼─────────────────┴────────────────┼─────────────────────────┘
                │                                   │
                │         Raw JSON                  │ Match Data
                │                                   │
                └───────────────┬───────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📊 DATA FOUNDATION LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐         ┌──────────────────────────┐         │
│  │   nwsl-loader            │────────>│   PostgreSQL             │         │
│  │   ETL Pipeline           │         │   Data Warehouse         │         │
│  │                          │<────────│   7.5 GB                 │         │
│  └──────────────────────────┘         └────────────┬─────────────┘         │
└─────────────────────────────────────────────────────┼─────────────────────────┘
                                                      │
                    ┌─────────────────────────────────┼─────────────────────┐
                    │                                 │                     │
                    ↓                                 ↓                     ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🧠 ANALYTICS & ML LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌──────────────────────────┐               │
│  │   nwsl-ml                │  │   nwsl-mcp-py            │               │
│  │   Model Training         │  │   Research Tools         │               │
│  │   xG, VAEP, xT          │  │   20 Statistical Tools   │               │
│  └────────────┬─────────────┘  └──────────────────────────┘               │
│               │                                                             │
│               ↓                                                             │
│  ┌──────────────────────────┐                                              │
│  │   Model Artifacts        │                                              │
│  │   .joblib, .pkl files    │                                              │
│  └────────────┬─────────────┘                                              │
└───────────────┼─────────────────────────────────────────────────────────────┘
                │
                │ Predictions
                ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🚀 SERVICE LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌──────────────────────────┐               │
│  │   nwsl-api               │  │   nwsl-viz               │               │
│  │   Gateway API            │  │   Visualization Service  │               │
│  │   SQL + Natural Language │  │   Shot Maps, Heatmaps    │               │
│  └────────────┬─────────────┘  └────────────┬─────────────┘               │
│               │                              │                              │
│               │                              ↓                              │
│               │                 ┌──────────────────────────┐               │
│               │                 │   Cloud Storage          │               │
│               │                 │   Image URLs             │               │
│               │                 └────────────┬─────────────┘               │
└───────────────┼──────────────────────────────┼─────────────────────────────┘
                │                              │
                │ JSON Data                    │ Image URLs
                │                              │
                └───────────────┬──────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    💻 PRESENTATION LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │   nwsl-app                                                           │  │
│  │   Next.js Dashboard                                                  │  │
│  │   Interactive UI                                                     │  │
│  └────────────┬───────────────────────────────────────────────────┬─────┘  │
└───────────────┼───────────────────────────────────────────────────┼─────────┘
                │                                                   │
                ↓                                                   ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                         👥 END USERS                                        │
├─────────────┬──────────────┬──────────────┬──────────────┬─────────────────┤
│ ⚽ Soccer   │ 📊 Data      │ 🤖 AI        │ 👨‍💻 ML       │ 🏗️ Developers  │
│   Fans     │   Analysts   │   Agents     │   Engineers  │                 │
└─────────────┴──────────────┴──────────────┴──────────────┴─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    ⚙️ OPERATIONS LAYER (Cross-cutting)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │   nwsl-ops                                                           │  │
│  │   Infrastructure, Runbooks & CI/CD                                   │  │
│  │   Manages: nwsl-loader, nwsl-ml, nwsl-api, nwsl-viz, nwsl-app       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagram 2: Data Flow Pipeline

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│ 1️⃣ EXTRACT │───>│ 2️⃣ RAW     │───>│ 3️⃣ TRANSFORM│───>│ 4️⃣ ML      │
│            │    │  STORAGE   │    │            │    │  TRAINING  │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
     │                  │                  │                  │
     │                  │                  │                  │
     v                  v                  v                  v

┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│ Opta API │      │ raw_feed │      │ Parse    │      │ nwsl-ml/ │
│  Events  │      │  table   │      │  JSON    │      │   xg     │
└──────────┘      │          │      └──────────┘      └──────────┘
                  │  JSONB   │            │                 │
┌──────────┐      │ payloads │      ┌──────────┐      ┌──────────┐
│FootyStats│      │          │      │Normalize │      │ nwsl-ml/ │
│   API    │      │ ~1.3K    │      │  Data    │      │  vaep    │
└──────────┘      │ matches  │      └──────────┘      └──────────┘
                  └──────────┘            │                 │
                                    ┌──────────┐      ┌──────────┐
                                    │ Convert  │      │  Save    │
                                    │  SPADL   │      │Artifacts │
                                    │ 2.93M    │      │ .joblib  │
                                    │ actions  │      │  .pkl    │
                                    └──────────┘      └──────────┘

                      ↓                                     ↓

┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│ 5️⃣ PREDICT │───>│ 6️⃣ AGGREGATE│───>│ 7️⃣ SERVE   │───>│ 8️⃣ CONSUME │
│            │    │            │    │            │    │            │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
     │                  │                  │                  │
     │                  │                  │                  │
     v                  v                  v                  v

┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│Apply xG  │      │  Match   │      │ nwsl-api │      │ nwsl-app │
│  Model   │      │  Grain   │      │   /sql   │      │Dashboard │
└──────────┘      │          │      └──────────┘      └──────────┘
     │            │ player_  │            │                 │
┌──────────┐      │  match   │      ┌──────────┐      ┌──────────┐
│Apply VAEP│      │          │      │ nwsl-api │      │   Data   │
│  Model   │      │ team_    │      │/dashboard│      │Scientists│
└──────────┘      │  match   │      └──────────┘      └──────────┘
     │            └──────────┘            │                 │
┌──────────┐            │           ┌──────────┐      ┌──────────┐
│Calculate │      ┌──────────┐      │ nwsl-mcp │      │   AI     │
│   xT     │      │  Season  │      │  -py     │      │ Agents   │
│          │      │  Grain   │      │ Research │      │          │
│ 313 MB   │      │          │      │  Tools   │      │          │
│  grid    │      │ player_  │      └──────────┘      └──────────┘
└──────────┘      │  season  │
                  │          │
                  │ team_    │
                  │  season  │
                  └──────────┘
                        │
                  ┌──────────┐
                  │ Career   │
                  │ Totals   │
                  │          │
                  │ player_  │
                  │  career  │
                  └──────────┘
```

---

## Diagram 3: Layer Responsibilities & User Personas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         👥 USER PERSONAS                                    │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────────┤
│ ⚽ Soccer    │ 📊 Data      │ 🤖 AI        │ 👨‍💻 ML       │ 🏗️ Developers │
│   Fans      │   Analysts   │   Agents     │   Engineers  │                │
│             │              │              │              │                │
│ Browse      │ Run custom   │ Statistical  │ Train        │ Build          │
│ stats       │ queries      │ analysis     │ models       │ applications   │
└──────┬──────┴──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────┘
       │             │              │              │                │
       │ Web UI      │ SQL Queries  │ MCP Tools    │ Train Models   │ REST API
       │             │              │              │                │
       v             v              │              │                v
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 6: PRESENTATION LAYER                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Repository:      nwsl-app (Next.js)                                        │
│                                                                              │
│  Responsibilities:                                                           │
│    ✓ Interactive dashboards                                                 │
│    ✓ Data visualization                                                     │
│    ✓ AI notebook                                                            │
│    ✓ User authentication                                                    │
│                                                                              │
│  Technology:                                                                 │
│    Next.js 14, React 18, Ant Design, Zustand                               │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ HTTP Requests
                                 v
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 5: API GATEWAY LAYER                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  Repository:      nwsl-api (Flask)                                          │
│                                                                              │
│  Responsibilities:                                                           │
│    ✓ SQL query gateway                                                      │
│    ✓ Natural language routing                                               │
│    ✓ Rate limiting                                                          │
│    ✓ Authentication & logging                                               │
│                                                                              │
│  Technology:                                                                 │
│    Flask, PostgreSQL, Cloud Run, Cloud SQL                                  │
└────────────────┬───────────────────────┬────────────────────────────────────┘
                 │                       │
                 │ Database Queries      │ Tool Invocation
                 v                       v
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 4: SERVICE LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Repository:      nwsl-viz (Python)                                         │
│                                                                              │
│  Responsibilities:                                                           │
│    ✓ Shot map generation                                                    │
│    ✓ Heatmap rendering                                                      │
│    ✓ Cloud Storage uploads                                                  │
│                                                                              │
│  Technology:                                                                 │
│    Flask, matplotsoccer, matplotlib, GCS                                    │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ Spatial Queries
                                 v
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 3: ANALYTICS LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Repository:      nwsl-ml + nwsl-mcp-py                                     │
│                                      ↑                                       │
│  Responsibilities:                   │                                       │
│    ✓ Train ML models                 │ MCP Tools                            │
│    ✓ Research tools                  │                                      │
│    ✓ Statistical tests               └──────────────────────────────────────┤
│    ✓ Model versioning                         ↑                             │
│                                                │ Train Models                │
│  Technology:                                   │                             │
│    scikit-learn, CatBoost, MCP protocol, asyncpg                            │
└────────────────────────────────┬───────────────────────────────────────────┘
                                 │
                                 │ Training Data + Predictions
                                 v
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 2: DATA FOUNDATION LAYER                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  Repository:      nwsl-loader (ETL)                                         │
│                                                                              │
│  Responsibilities:                                                           │
│    ✓ Data ingestion                                                         │
│    ✓ SPADL transformation                                                   │
│    ✓ Aggregation pipelines                                                  │
│    ✓ Data quality                                                           │
│                                                                              │
│  Technology:                                                                 │
│    Python, PostgreSQL, asyncpg, Kimball schema                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                 ↑
                                 │ Manages All Layers
                                 │
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 1: OPERATIONS LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Repository:      nwsl-ops                                                  │
│                                                                              │
│  Responsibilities:                                                           │
│    ✓ Infrastructure as code                                                 │
│    ✓ Deployment automation                                                  │
│    ✓ Secret management                                                      │
│    ✓ Monitoring & runbooks                                                  │
│                                                                              │
│  Technology:                                                                 │
│    Terraform, Cloud Build, Secret Manager, Make                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Table

| Layer | Repository | Primary Language | Deployment | Purpose |
|-------|-----------|------------------|------------|---------|
| **Operations** | nwsl-ops | Shell, YAML | N/A | Infrastructure & runbooks |
| **Data Foundation** | nwsl-loader | Python, SQL | Cloud SQL | ETL & data warehouse |
| **Analytics** | nwsl-ml | Python | Local/Cloud Run | Model training |
| **Analytics** | nwsl-mcp-py | Python | Cloud Run | Research tools |
| **Service** | nwsl-viz | Python | Cloud Run | Visualization rendering |
| **API Gateway** | nwsl-api | Python (Flask) | Cloud Run | Data access gateway |
| **Presentation** | nwsl-app | TypeScript (Next.js) | Vercel | User interface |

---

## Technology Stack Summary

```
Frontend:       Next.js 14 + React 18 + TypeScript + Ant Design
API Gateway:    Flask + PostgreSQL + Cloud Run
Analytics:      Python + scikit-learn + MCP Protocol
Visualization:  matplotsoccer + matplotlib + Cloud Storage
Data Warehouse: PostgreSQL 14 + Kimball Star Schema
ML Training:    Python + CatBoost + joblib
Infrastructure: Google Cloud (Cloud Run, Cloud SQL, Secret Manager)
CI/CD:          Cloud Build + Vercel
```

---

## Key Metrics

- **Database Size:** 7.5 GB
- **Match Coverage:** 1,328 matches (100%)
- **Event Coverage:** 2.58M events
- **SPADL Actions:** 2.93M standardized actions
- **Players Tracked:** 895 unique players
- **Seasons:** 2013-2025 (13 years)
- **Tables:** 76 total (10 dim, 40+ fact, 17 agg)
- **ML Models:** 3 production (xG, VAEP, xT)
- **MCP Tools:** 20 research-grade analytics functions
- **API Endpoints:** 15+ public endpoints

---

**Generated:** 2025-10-24
**Platform Version:** 2.0.0
**Documentation:** See individual repository READMEs for detailed documentation
