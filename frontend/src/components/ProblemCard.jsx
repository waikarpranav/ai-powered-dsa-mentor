import { Link } from 'react-router-dom';

const DIFFICULTY_CLASS = {
  Easy: 'badge-easy',
  Medium: 'badge-medium',
  Hard: 'badge-hard',
};

// Determines solve status from user's submissions for this problem
function getSolveStatus(slug, submissions) {
  if (!submissions || submissions.length === 0) return 'unsolved';
  const matching = submissions.filter((s) => s.problem_slug === slug);
  if (matching.length === 0) return 'unsolved';
  if (matching.some((s) => s.is_optimal)) return 'optimal';
  return 'attempted';
}

const STATUS_LABEL = {
  optimal: '✓ Optimal',
  attempted: '~ Attempted',
  unsolved: 'Unsolved',
};
const STATUS_CLASS = {
  optimal: 'badge-optimal',
  attempted: 'badge-attempted',
  unsolved: 'badge-unsolved',
};

export default function ProblemCard({ problem, submissions }) {
  const status = getSolveStatus(problem.slug, submissions);

  return (
    <Link to={`/problem/${problem.slug}`} className="problem-card">
      <div className="card-header">
        <span className="card-title">{problem.title}</span>
        <span className={`badge ${STATUS_CLASS[status]}`}>{STATUS_LABEL[status]}</span>
      </div>
      <div className="card-meta">
        <span className={`badge ${DIFFICULTY_CLASS[problem.difficulty] || 'badge-medium'}`}>
          {problem.difficulty}
        </span>
        <span className="badge badge-category">{problem.category}</span>
      </div>
    </Link>
  );
}
