"""
recommender.py — Pure Python skill-gap detection. No AI involved.

Logic:
  1. Load all submissions for this session
  2. Group by problem category
  3. Compute optimal% per category
  4. Find the weakest category (lowest optimal%)
  5. Return the next unsolved problem in that category
  
Why no AI? Deterministic logic on structured data is more reliable,
debuggable, and explainable than asking an LLM to count categories.
"""

from collections import defaultdict
from sqlalchemy.orm import Session
import models

# Maps each category to an ordered list of problem slugs (easier → harder)
CATEGORY_PROBLEMS: dict[str, list[str]] = {
    "Arrays": [
        "two_sum",
        "best_time_to_buy_stock",
        "maximum_subarray",
        "product_except_self",
        "container_with_most_water",
    ],
    "Sliding Window": [
        "longest_substring_without_repeating",
        "minimum_window_substring",
    ],
    "Two Pointers": [
        "three_sum",
        "trapping_rain_water",
    ],
    "Binary Search": [
        "search_rotated_sorted_array",
        "find_min_rotated_array",
    ],
    "Linked Lists": [
        "reverse_linked_list",
        "merge_two_sorted_lists",
        "detect_cycle",
    ],
    "Trees": [
        "inorder_traversal",
        "max_depth_binary_tree",
        "validate_bst",
        "lowest_common_ancestor",
    ],
    "Graphs": [
        "number_of_islands",
        "clone_graph",
        "course_schedule",
    ],
    "Dynamic Programming": [
        "climbing_stairs",
        "house_robber",
        "coin_change",
        "longest_common_subsequence",
    ],
    "Tries": [
        "implement_trie",
    ],
    "Heaps": [
        "kth_largest_element",
    ],
}


def get_recommendation(session_id: str, db: Session) -> dict:
    """
    Analyze a user's submission history and recommend what to practice next.
    
    Returns:
        weak_category: category with the lowest optimal submission rate
        stats: per-category breakdown of { total, optimal, optimal_rate }
        next_problem: slug of the next recommended problem
        message: human-readable recommendation string
    """
    submissions = (
        db.query(models.Submission)
        .filter(models.Submission.session_id == session_id)
        .all()
    )

    if not submissions:
        return {
            "message": "No submissions yet. Start with Two Sum!",
            "weak_category": None,
            "stats": {},
            "next_problem": "two_sum",
        }

    # Map each submitted slug to its category via the DB
    slugs = {s.problem_slug for s in submissions}
    problems = db.query(models.Problem).filter(models.Problem.slug.in_(slugs)).all()
    slug_to_category = {p.slug: p.category for p in problems}

    # Aggregate stats per category
    category_stats: dict[str, dict] = defaultdict(lambda: {"total": 0, "optimal": 0})
    for sub in submissions:
        cat = slug_to_category.get(sub.problem_slug, "Unknown")
        category_stats[cat]["total"] += 1
        if sub.is_optimal:
            category_stats[cat]["optimal"] += 1

    # Add optimal_rate for frontend display
    for cat, stats in category_stats.items():
        stats["optimal_rate"] = round(
            stats["optimal"] / stats["total"] * 100 if stats["total"] > 0 else 0, 1
        )

    # Find weakest category (lowest optimal rate, minimum 1 attempt)
    weakest = min(
        category_stats,
        key=lambda c: category_stats[c]["optimal"] / max(category_stats[c]["total"], 1),
    )

    # Find next unsolved-optimally problem in the weakest category
    solved_optimally = {s.problem_slug for s in submissions if s.is_optimal}
    next_problem = None

    for slug in CATEGORY_PROBLEMS.get(weakest, []):
        if slug not in solved_optimally:
            # Verify it exists in the DB (was seeded)
            p = db.query(models.Problem).filter(models.Problem.slug == slug).first()
            if p:
                next_problem = slug
                break

    weak_rate = category_stats[weakest]["optimal_rate"]
    message = (
        f"Your weakest area is {weakest} ({weak_rate}% optimal rate). "
        + (f"Try: {next_problem.replace('_', ' ').title()}" if next_problem else "You've solved all problems in this category optimally!")
    )

    return {
        "weak_category": weakest,
        "stats": dict(category_stats),
        "next_problem": next_problem,
        "message": message,
    }
