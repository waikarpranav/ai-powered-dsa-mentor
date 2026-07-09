# AI-Powered DSA Mentor — Walkthrough

We have successfully built the **AI-Powered DSA Mentor** project end-to-end. The codebase is clean, well-documented, and fully functional. It operates in two modes:
1. **Local Anonymous Mode**: Uses a persistent browser UUID in `localStorage` and a local SQLite database (`dsa_mentor.db`) for immediate out-of-the-box local runs.
2. **Production Cloud Mode**: Uses **Supabase Auth** (passwordless email Magic Links) and **Supabase PostgreSQL** for full cloud deployment.

---

## ⚡ Core Features Completed

1. **Structured LLM Evaluation Pipeline (`analyzer.py`)**
   * Uses LangChain to inject hand-authored reference documents (`problems/*.md`) into prompts to ground the AI model and prevent hallucinations.
   * Built-in **fallback chain** using `.with_fallbacks()`: Groq (`llama-3.3-70b-versatile`) → Google Gemini (`gemini-2.0-flash`) → Groq small (`llama-3.1-8b-instant`).
   * Strict JSON output parsing with structured retry logic.

2. **Deterministic Recommendation Engine (`recommender.py`)**
   * Aggregates user submission histories to compute optimal solve rates per category.
   * Pinpoints the weakest area and recommends the next unsolved problem in that category.

3. **Workspace Editor**
   * Fully responsive layout with Monaco Editor (supporting Java and Python syntax out-of-the-box).
   * Feedback panel displaying verdicts, time/space complexity badges, missed edge cases, and concrete hints.

4. **Category-Level Dashboard**
   * Radar chart mapping your DSA competency across all categories (Arrays, Trees, DP, etc.).
   * Submission history table detailing verdicts, complexities, and submission times.

---

## 📁 Final Project Architecture

```
dsa-mentor/
├── backend/
│   ├── main.py                 ← FastAPI entry point & CORS
│   ├── analyzer.py             ← LangChain prompts & fallback chain
│   ├── recommender.py          ← Python category skill-gap logic
│   ├── models.py               ← SQL Database tables
│   ├── database.py             ← SQLAlchemy connector (SQLite / Postgres)
│   ├── schemas.py              ← Pydantic contract validation
│   ├── seed.py                 ← Idempotent seeder (27 problems)
│   ├── problems/               ← 27 hand-authored expert references
│   │   ├── two_sum.md
│   │   └── ...
│   ├──requirements.txt
│   └── .env                    ← Keys (Groq, Gemini, DB)
│
└── frontend/
    ├── src/
    │   ├── components/         ← ProblemCard, Navbar, FeedbackPanel, Login
    │   ├── lib/                ← api.js (Axios), session.js, supabase.js
    │   ├── pages/              ← Home (Grid), Workspace, Dashboard (Radar)
    │   ├── App.jsx             ← Router config
    │   ├── index.css           ← Dark design system tokens & animations
    │   └── main.jsx
    ├── index.html
    └── .env                    ← Frontend API and Supabase config keys
```

---

## 🛠️ Validation & Local Testing

* **Tested optimal solutions**: Submitting optimal $O(N)$ hash-map code correctly prints `Optimal` verdict and green badges.
* **Tested suboptimal solutions**: Submitting $O(N^2)$ brute-force code successfully triggers `Suboptimal` verdict and warns about time complexity.
* **Tested fallback chain**: Disabling the Groq key correctly forces the backend to run on Google Gemini Flash, returning the response seamlessly.

---

## 🚀 Step-by-Step Cloud Deployment Guide

When you are ready to put this on your resume and share it with recruiters, follow these three steps:

### Step 1: Create a Supabase Project (Auth + DB)
1. Sign up on [Supabase](https://supabase.com) (free).
2. Create a new project.
3. Under **Project Settings -> API**, copy:
   * **Project URL**
   * **API Anon Key**
4. Under **Project Settings -> Database**, copy the **Transaction Connection String** (under URI tab). It will look like:
   `postgres://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`

### Step 2: Deploy Frontend on Vercel
1. Push your project to GitHub.
2. Sign up on [Vercel](https://vercel.com) (free) and import the repository.
3. In configuration, set **Root Directory** to `frontend`.
4. Add the following **Environment Variables**:
   * `VITE_API_URL` = (Your Backend Render URL, see Step 3)
   * `VITE_SUPABASE_URL` = (From Step 1)
   * `VITE_SUPABASE_ANON_KEY` = (From Step 1)
5. Deploy!

### Step 3: Deploy Backend on Render
1. Create a Web Service on [Render](https://render.com) (free).
2. Set **Root Directory** to `backend`.
3. Set **Start Command** to: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add the following **Environment Variables**:
   * `DATABASE_URL` = (Copy the connection string from Step 1, swap `postgres://` to `postgresql://`)
   * `GROQ_API_KEY` = (Your Groq API key)
   * `GOOGLE_API_KEY` = (Your Gemini API key)
   * `ALLOWED_ORIGINS` = `http://localhost:5173,https://your-vercel-app-url.vercel.app`
5. Deploy!

> [!TIP]
> **Cold Start Mitigation**: Since Render free instances spin down after 15 minutes of inactivity, you can create a free account at [cron-job.org](https://cron-job.org) and set up a schedule to ping your backend's `/health` endpoint every 14 minutes.
