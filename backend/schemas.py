from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Request schemas (what the frontend sends) ──────────────────────────────

class AnalyzeRequest(BaseModel):
    problem_slug: str
    language: str        # "java" or "python"
    code: str
    session_id: str      # UUID stored in localStorage


# ── Response schemas (what the backend returns) ────────────────────────────

class FeedbackResponse(BaseModel):
    time_complexity: str
    space_complexity: str
    is_optimal: bool
    approach_identified: str
    edge_cases_missed: List[str]
    verdict: str           # "Optimal" | "Acceptable" | "Suboptimal" | "Incorrect"
    improvement_hint: str
    confidence: str        # "high" | "medium" | "low"


class AnalyzeResponse(BaseModel):
    submission_id: int
    feedback: FeedbackResponse


class ProblemResponse(BaseModel):
    id: int
    slug: str
    title: str
    category: str
    difficulty: str
    description: str

    class Config:
        from_attributes = True


class SubmissionResponse(BaseModel):
    id: int
    problem_slug: str
    language: str
    verdict: Optional[str]
    is_optimal: bool
    time_complexity: Optional[str]
    space_complexity: Optional[str]
    edge_cases_missed: Optional[List[str]]
    improvement_hint: Optional[str]
    approach_identified: Optional[str]
    submitted_at: datetime

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    weak_category: Optional[str]
    stats: dict
    next_problem: Optional[str]
    message: str
