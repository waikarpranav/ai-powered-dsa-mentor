"""
analyzer.py — The core LLM evaluation pipeline.

Architecture:
  1. Load the hand-authored reference doc for the problem (the "ground truth")
  2. Inject it into a structured prompt via LangChain
  3. Call Groq (llama-3.3-70b) as primary LLM
  4. If Groq quota is exhausted → automatically fall back to Gemini Flash 2.0
  5. If Gemini quota is exhausted → fall back to Groq llama-3.1-8b-instant (smaller, same key)
  6. Parse the JSON response with LangChain's JsonOutputParser
  7. If JSON parsing fails → retry once with a stricter prompt
  8. If retry also fails → return a structured error dict (never crash the endpoint)
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

logger = logging.getLogger(__name__)

PROBLEMS_DIR = Path(__file__).parent / "problems"

# ── Prompts ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a strict DSA interviewer. You will analyze a candidate's code solution \
against a reference answer. You must respond ONLY with valid JSON — no markdown \
fences, no explanation text, just a raw JSON object.

Your analysis must be grounded in the reference document provided below. \
Do NOT invent complexity values — derive them from the actual code logic.

Reference Document for this problem:
{reference_doc}
"""

HUMAN_PROMPT = """\
Problem: {problem_title}
Language: {language}

Candidate's Code:
```
{user_code}
```

Analyze this code and return a JSON object with EXACTLY these fields. \
Start your response with {{ and end with }}. No other text.

{{
  "time_complexity": "O(...) — brief one-line explanation",
  "space_complexity": "O(...) — brief one-line explanation",
  "is_optimal": true or false,
  "approach_identified": "brief description of what the candidate did (1-2 sentences)",
  "edge_cases_missed": ["list", "of", "specific", "edge cases the code would fail on"],
  "verdict": "Optimal" or "Acceptable" or "Suboptimal" or "Incorrect",
  "improvement_hint": "one concrete actionable hint without revealing the full solution",
  "confidence": "high" or "medium" or "low"
}}"""

RETRY_SYSTEM_SUFFIX = (
    "\n\nCRITICAL: Your previous response was not valid JSON. "
    "Return ONLY the JSON object. Start with { and end with }. "
    "Absolutely no other text before or after."
)


# ── LLM setup ─────────────────────────────────────────────────────────────

def _build_llm():
    """
    Build the LLM chain with automatic fallbacks.
    
    Primary   → Groq llama-3.3-70b-versatile  (~500 tok/s, 14,400 req/day free)
    Fallback1 → Gemini Flash 2.0              (~1,500 req/day free)
    Fallback2 → Groq llama-3.1-8b-instant     (same API key, smaller model)
    
    LangChain's .with_fallbacks() triggers on any exception from the primary,
    including RateLimitError and quota exhaustion — fully transparent to callers.
    """
    primary = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,   # Low temp = deterministic, consistent JSON
        max_retries=2,
    )
    fallback1 = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1,
    )
    fallback2 = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
        max_retries=2,
    )
    return primary.with_fallbacks([fallback1, fallback2])


def _build_chain(system_suffix: str = ""):
    """Build a LangChain chain: prompt → LLM (with fallbacks) → JSON parser."""
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT + system_suffix),
        ("human", HUMAN_PROMPT),
    ])
    parser = JsonOutputParser()
    return prompt | llm | parser


# ── Reference doc loader ──────────────────────────────────────────────────

def _load_reference_doc(problem_slug: str) -> str:
    """Load the hand-authored .md reference doc for this problem."""
    doc_path = PROBLEMS_DIR / f"{problem_slug}.md"
    if doc_path.exists():
        return doc_path.read_text(encoding="utf-8")
    logger.warning(f"No reference doc found for slug: {problem_slug}")
    return (
        "No reference document available for this problem. "
        "Use your general DSA knowledge to evaluate the code."
    )


# ── Main entry point ──────────────────────────────────────────────────────

async def analyze_code(
    problem_slug: str,
    problem_title: str,
    language: str,
    code: str,
) -> dict:
    """
    Analyze a user's code submission against the reference doc.
    
    Returns a dict with keys:
      time_complexity, space_complexity, is_optimal, approach_identified,
      edge_cases_missed, verdict, improvement_hint, confidence
    
    Never raises — always returns a valid dict (with error info if all else fails).
    """
    reference_doc = _load_reference_doc(problem_slug)
    inputs = {
        "reference_doc": reference_doc,
        "problem_title": problem_title,
        "language": language,
        "user_code": code,
    }

    # First attempt
    try:
        chain = _build_chain()
        result = await chain.ainvoke(inputs)
        logger.info(f"Analysis succeeded for {problem_slug} ({language})")
        return result

    except Exception as first_error:
        logger.warning(f"First attempt failed for {problem_slug}: {first_error}. Retrying...")

    # Retry with stricter JSON instructions
    try:
        chain = _build_chain(system_suffix=RETRY_SYSTEM_SUFFIX)
        result = await chain.ainvoke(inputs)
        logger.info(f"Retry succeeded for {problem_slug}")
        return result

    except Exception as retry_error:
        logger.error(f"Both attempts failed for {problem_slug}: {retry_error}")
        # Return a graceful degradation response — never crash the endpoint
        return {
            "time_complexity": "Analysis unavailable",
            "space_complexity": "Analysis unavailable",
            "is_optimal": False,
            "approach_identified": "Could not analyze — all LLM providers may be rate-limited.",
            "edge_cases_missed": [],
            "verdict": "Incorrect",
            "improvement_hint": (
                "The AI analyzer is temporarily unavailable (likely quota exhaustion). "
                "Please try again in a few minutes."
            ),
            "confidence": "low",
        }
