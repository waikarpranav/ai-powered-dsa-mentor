"""
main.py — FastAPI application entry point.

Endpoints:
  GET  /health                    → Health check (keep-alive ping target)
  GET  /problems                  → All problems (for problem selector grid)
  GET  /problems/{slug}           → Single problem detail
  POST /analyze                   → Submit code, get AI feedback
  GET  /submissions/{session_id}  → Submission history for a user
  GET  /recommendations/{session_id} → Skill-gap analysis + next problem
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import engine, get_db
import models
from schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ProblemResponse,
    SubmissionResponse,
    RecommendationResponse,
)
from analyzer import analyze_code
from recommender import get_recommendation
from seed import seed_problems

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── App lifecycle ─────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run on startup: create tables + seed problems."""
    models.Base.metadata.create_all(bind=engine)
    db = next(get_db())
    seed_problems(db)
    logger.info("[OK] DSA Mentor API started")
    yield
    logger.info("DSA Mentor API shutting down")


app = FastAPI(
    title="DSA Mentor API",
    description="AI-powered DSA code analysis grounded in hand-authored reference docs.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS (allow frontend dev server + production domain) ──────────────────

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health():
    """Keep-alive endpoint. Render cron job pings this every 14 min to prevent cold starts."""
    return {"status": "ok", "message": "DSA Mentor API is running"}


@app.get("/problems", response_model=list[ProblemResponse], tags=["Problems"])
async def get_all_problems(db: Session = Depends(get_db)):
    """Return all curated problems for the problem selector grid."""
    return db.query(models.Problem).order_by(models.Problem.category, models.Problem.id).all()


@app.get("/problems/{slug}", response_model=ProblemResponse, tags=["Problems"])
async def get_problem(slug: str, db: Session = Depends(get_db)):
    """Return a single problem's details for the workspace page."""
    problem = db.query(models.Problem).filter(models.Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{slug}' not found")
    return problem


@app.post("/analyze", tags=["Analysis"])
async def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Core endpoint: submit code → get structured AI feedback.
    
    1. Validates the problem exists
    2. Calls the LangChain pipeline (Groq → Gemini → fallback)
    3. Persists the submission + feedback to DB
    4. Returns the structured feedback
    """
    # Validate problem exists
    problem = db.query(models.Problem).filter(
        models.Problem.slug == request.problem_slug
    ).first()
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem '{request.problem_slug}' not found")

    # Run AI analysis
    logger.info(f"Analyzing {request.problem_slug} ({request.language}) for session {request.session_id}")
    feedback = await analyze_code(
        problem_slug=request.problem_slug,
        problem_title=problem.title,
        language=request.language,
        code=request.code,
    )

    # Persist to DB
    submission = models.Submission(
        session_id=request.session_id,
        problem_slug=request.problem_slug,
        language=request.language,
        code=request.code,
        time_complexity=feedback.get("time_complexity"),
        space_complexity=feedback.get("space_complexity"),
        is_optimal=feedback.get("is_optimal", False),
        edge_cases_missed=feedback.get("edge_cases_missed", []),
        verdict=feedback.get("verdict"),
        improvement_hint=feedback.get("improvement_hint"),
        approach_identified=feedback.get("approach_identified"),
        confidence=feedback.get("confidence"),
        feedback_text=str(feedback),
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {"submission_id": submission.id, "feedback": feedback}


@app.get("/submissions/{session_id}", response_model=list[SubmissionResponse], tags=["History"])
async def get_submissions(session_id: str, db: Session = Depends(get_db)):
    """Return all submissions for a session, newest first."""
    return (
        db.query(models.Submission)
        .filter(models.Submission.session_id == session_id)
        .order_by(models.Submission.submitted_at.desc())
        .all()
    )


@app.get("/recommendations/{session_id}", response_model=RecommendationResponse, tags=["History"])
async def get_recommendations(session_id: str, db: Session = Depends(get_db)):
    """
    Pure-Python skill-gap analysis. No AI involved.
    Returns weakest category, per-category stats, and next recommended problem.
    """
    return get_recommendation(session_id, db)
