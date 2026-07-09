from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from sqlalchemy.sql import func
from database import Base


class Problem(Base):
    """Seeded from problems/*.md files. Represents a curated DSA problem."""
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)       # e.g. "two_sum"
    title = Column(String, nullable=False)               # e.g. "Two Sum"
    category = Column(String, nullable=False)            # e.g. "Arrays"
    difficulty = Column(String, nullable=False)          # "Easy" | "Medium" | "Hard"
    description = Column(Text, nullable=False)           # Problem statement shown in UI
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Submission(Base):
    """One row per code submission. Stores both the code and the AI feedback."""
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)   # UUID from localStorage / Supabase user id
    problem_slug = Column(String, index=True, nullable=False)
    language = Column(String, nullable=False)                  # "java" | "python"
    code = Column(Text, nullable=False)

    # AI feedback fields (parsed from LLM JSON response)
    time_complexity = Column(String)
    space_complexity = Column(String)
    is_optimal = Column(Boolean, default=False)
    edge_cases_missed = Column(JSON, default=list)            # list of strings
    verdict = Column(String)                                  # "Optimal" | "Acceptable" | "Suboptimal" | "Incorrect"
    improvement_hint = Column(Text)
    approach_identified = Column(String)
    confidence = Column(String)                               # "high" | "medium" | "low"
    feedback_text = Column(Text)                              # raw JSON string for debugging

    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
