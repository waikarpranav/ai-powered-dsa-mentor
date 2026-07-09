# AI-Powered DSA Mentor — Full Implementation Plan

## What You're Building
A web app where users paste their DSA code, get structured AI feedback grounded in your hand-authored reference docs, and track their skill gaps over time. Your DSA knowledge is the product — not just an LLM wrapper.

---

## Project Structure (Final)

```
dsa-mentor/
├── backend/
│   ├── main.py                 ← FastAPI app entry point
│   ├── analyzer.py             ← LangChain + Groq prompt pipeline
│   ├── recommender.py          ← Pure Python skill-gap logic
│   ├── models.py               ← SQLAlchemy DB models
│   ├── database.py             ← DB connection setup
│   ├── schemas.py              ← Pydantic request/response schemas
│   ├── seed.py                 ← Seeds problem table from .md files
│   ├── problems/               ← Your hand-authored reference docs (THE MOAT)
│   │   ├── two_sum.md
│   │   ├── best_time_to_buy_stock.md
│   │   └── ... (30 total)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx        ← Problem selector grid
│   │   │   ├── Workspace.jsx   ← Monaco editor + feedback panel
│   │   │   └── Dashboard.jsx   ← Radar chart + submission history
│   │   ├── components/
│   │   │   ├── ProblemCard.jsx
│   │   │   ├── FeedbackPanel.jsx
│   │   │   ├── RadarChart.jsx
│   │   │   └── Navbar.jsx
│   │   ├── lib/
│   │   │   └── api.js          ← Axios API calls
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
│
└── README.md
```

---

## Week 1 — Foundation & Content (Days 1–7)

**Goal**: Project scaffold + all 15 reference docs + backend skeleton running locally

### Day 1–2: Project Setup
- [ ] Create Vite + React frontend project
- [ ] Create FastAPI backend with virtual environment
- [ ] Set up SQLite database with SQLAlchemy
- [ ] Test that FastAPI `/health` endpoint works
- [ ] Test that frontend can talk to backend (CORS setup)

### Day 3–5: Write Reference Docs (THE MOST IMPORTANT WORK)
Write 15 `.md` files in `backend/problems/`. Each file is ~30–50 lines.

**Batch 1 — Arrays & Sliding Window (5 problems)**
- `two_sum.md`
- `best_time_to_buy_stock.md`
- `maximum_subarray.md`
- `product_except_self.md`
- `longest_substring_without_repeating.md`

**Batch 2 — Two Pointers & Binary Search (4 problems)**
- `three_sum.md`
- `trapping_rain_water.md`
- `search_rotated_sorted_array.md`
- `find_min_rotated_array.md`

**Batch 3 — Linked Lists & Trees (6 problems)**
- `reverse_linked_list.md`
- `merge_two_sorted_lists.md`
- `detect_cycle.md`
- `max_depth_binary_tree.md`
- `validate_bst.md`
- `lowest_common_ancestor.md`

### Day 6–7: Backend Skeleton
- [ ] `database.py` — SQLAlchemy engine + session
- [ ] `models.py` — User, Problem, Submission tables
- [ ] `seed.py` — Parse .md files → populate problems table
- [ ] `/problems` GET endpoint — returns all problems
- [ ] `/health` GET endpoint

---

## Week 2 — Backend Core (Days 8–14)

**Goal**: The analyzer working end-to-end, all endpoints, 15 more reference docs

### Day 8–9: The Analyzer (Most Important Code)
Build `analyzer.py` with LangChain + Groq:
1. Load the problem's `.md` reference doc
2. Build a prompt that injects the reference doc as context
3. Call Groq (llama-3.3-70b)
4. Parse the JSON response with Pydantic
5. Retry with a stricter prompt if JSON parsing fails

### Day 10: The `/analyze` Endpoint
- Accept: `{ problem_slug, language, code, user_id }`
- Returns structured JSON feedback
- Stores result in `submissions` table

### Day 11: The Recommender
Build `recommender.py`:
- Groups submissions by category
- Finds weakest category (lowest optimal%)
- Returns next unsolved problem in that category

### Day 12: History & User Endpoints
- `/submissions/{user_id}` — GET all submissions
- `/recommendations/{user_id}` — GET skill-gap analysis

### Day 13–14: 15 More Reference Docs
**Batch 4 — Graphs & DP (10 problems)**
- `number_of_islands.md`
- `clone_graph.md`
- `course_schedule.md`
- `climbing_stairs.md`
- `coin_change.md`
- `house_robber.md`
- `longest_common_subsequence.md`
- `container_with_most_water.md`
- `kth_largest_element.md`
- `implement_trie.md`

---

## Week 3 — Frontend (Days 15–21)

**Goal**: Full working frontend — problem selector, Monaco editor, feedback UI, dashboard

### Day 15–16: Home Page
- Problem card grid (filterable by category/difficulty)
- Each card shows: title, category tag, difficulty badge, solve status (unsolved/attempted/optimal)
- Clicking a card navigates to `/problem/:slug`

### Day 17–18: Workspace Page (The Core UX)
- Left panel: problem statement, category tags, difficulty
- Right panel: Monaco Editor (language switcher for Java/Python)
- Submit button → calls `/analyze` → shows loading state
- Feedback panel below editor

### Day 19: Feedback Panel (Most Important UI Component)
Display each JSON field distinctly:
| Field | UI Treatment |
|---|---|
| `time_complexity` / `space_complexity` | Colored badges (green=O(n), yellow=O(n log n), red=O(n²)) |
| `verdict` | Prominent banner (Optimal=green, Suboptimal=red) |
| `is_optimal` | Green check / Red X |
| `edge_cases_missed` | Chip/tag list |
| `improvement_hint` | Callout box (styled differently from solution) |
| `confidence` | Small badge |

### Day 20–21: Dashboard
- Radar chart (Recharts) — performance by category
- Recent submissions table
- Recommendation card: "You struggle with Sliding Window. Try: Minimum Window Substring"
- Supabase Auth integration (magic link login)

---

## Week 4 — Polish & Deployment (Days 22–28)

**Goal**: Production-ready deployment, README, interview talking points

### Day 22: Auth Integration
- Supabase Auth setup (email + magic link)
- Replace anonymous session with real user IDs
- Protect submission history behind auth

### Day 23–24: Deployment
- Frontend → Vercel (connect GitHub, auto-deploys on push)
- Backend → Render Web Service
- DB → Render PostgreSQL (switch from SQLite)
- Set all environment variables

### Day 25: Keep-Alive Cron Job
Prevent Render cold starts (30–50 second delay):
```python
# In main.py — or use Render's built-in cron
@app.get("/health")
async def health(): return {"status": "ok"}
```
Set up a Render Cron Job to ping `/health` every 14 minutes.

### Day 26–27: Polish
- Mobile responsiveness
- Loading skeletons for cold start delay
- Error states (LLM timeout, invalid code, etc.)
- Favicon, page titles, meta descriptions

### Day 28: README + Demo
- Architecture diagram
- Setup instructions
- Screenshot/GIF of the feedback panel
- Live demo link

---

## Tech Stack Summary

| Layer | Technology | Why |
|---|---|---|
| Frontend | React + Vite | Fast dev, industry standard |
| Editor | `@monaco-editor/react` | Same as VS Code + LeetCode |
| Charts | Recharts | Easiest radar chart for React |
| Styling | Vanilla CSS (custom) | Full control, no Tailwind overhead |
| Backend | FastAPI | Auto Swagger docs, async, Pydantic |
| Prompt Pipeline | LangChain + Groq → Gemini Flash → Groq small | Multi-provider fallback chain, all free |
| Auth | Supabase Auth | Magic link, free tier, 50k MAU |
| DB (dev) | SQLite + SQLAlchemy | Zero setup |
| DB (prod) | PostgreSQL (Render) | One-line `DATABASE_URL` change |
| Deployment | Vercel + Render | 100% free tier |

---

## LLM Provider Fallback Chain

Since all free-tier LLMs have weekly/monthly quota limits, the analyzer uses LangChain's `.with_fallbacks()` to chain providers:

```
Primary:    Groq (llama-3.3-70b)      → ~500 tok/s, generous free tier
Fallback 1: Google Gemini Flash 2.0   → 1,500 req/day free
Fallback 2: Groq (llama-3.1-8b)       → smaller model, same API key
```

In `analyzer.py`, this looks like:

```python
primary   = ChatGroq(model="llama-3.3-70b-versatile")
fallback1 = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
fallback2 = ChatGroq(model="llama-3.1-8b-instant")

# LangChain automatically tries each on RateLimitError / quota exhaustion
llm = primary.with_fallbacks([fallback1, fallback2])
```

This means:
- **Groq quota runs out?** → Gemini Flash picks up seamlessly, user notices nothing
- **Gemini quota runs out?** → Falls to the smaller Groq model (still good quality)
- **All quota exhausted?** → Returns a friendly error message, not a crash

### API Keys Needed (all free, no credit card)
| Provider | Where to get key | Free limit |
|---|---|---|
| Groq | https://console.groq.com | 14,400 req/day |
| Gemini | https://aistudio.google.com | 1,500 req/day |
| Supabase | https://supabase.com | Free tier, Week 4 only |

---

## Environment Variables

```bash
# backend/.env
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
DATABASE_URL=sqlite:///./dsa_mentor.db   # dev
# DATABASE_URL=postgresql://...          # prod (Week 4)
ALLOWED_ORIGINS=http://localhost:5173,https://your-app.vercel.app
SUPABASE_URL=...                         # Week 4 only
SUPABASE_SERVICE_KEY=...                 # Week 4 only

# frontend/.env
VITE_API_URL=http://localhost:8000       # dev
# VITE_API_URL=https://your-app.onrender.com  # prod
VITE_SUPABASE_URL=...                    # Week 4 only
VITE_SUPABASE_ANON_KEY=...              # Week 4 only
```

---

## Resume Framing

> **AI-Powered DSA Mentor** | React, FastAPI, LangChain, Groq (Llama 3.3), PostgreSQL
> - Designed a structured LLM evaluation pipeline that grounds AI feedback in hand-authored reference documents for 30 curated DSA problems, achieving reliable complexity analysis and edge case detection
> - Built a multi-provider LLM fallback chain (Groq → Gemini Flash → Groq small) using LangChain's `.with_fallbacks()` to ensure zero-downtime across weekly quota resets
> - Built a pattern-detection recommendation engine in pure Python that analyzes submission history to surface per-category skill gaps (no AI dependency — deterministic and explainable)
> - Implemented a full-stack submission tracking system with a Monaco-based code editor, category-level performance dashboard (radar chart), and structured JSON feedback rendering
> - Deployed on Vercel + Render with free-tier-only infrastructure; cold-start mitigation via keep-alive cron job

---

## Key Interview Talking Points

1. **"Why hand-authored reference docs?"**
   → "LLMs hallucinate complexity values for non-trivial code. My reference docs inject ground truth into the prompt — same principle as RAG, except I use curated structured knowledge, not a vector DB, because I know exactly what the LLM needs for each problem."

2. **"Why is the recommendation engine not AI?"**
   → "Deterministic logic on structured data is more reliable, debuggable, and explainable than asking an LLM to count categories. I used AI where it adds value — analyzing unstructured code — and kept business logic in Python where it belongs."

3. **"What's the hardest part you solved?"**
   → "Getting consistent JSON output from the LLM. I solved it by making the JSON schema explicit in the prompt, validating with Pydantic on the backend, and adding a retry with a stricter prompt if parsing fails."

4. **"What happens when your free API quota runs out?"**
   → "I built a multi-provider fallback chain using LangChain's `.with_fallbacks()`. Groq is primary, Gemini Flash is fallback, a smaller Groq model is the last resort. The user sees nothing — it's fully transparent."
