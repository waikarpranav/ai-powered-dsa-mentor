import { useState, useEffect } from 'react';
import { getProblems, getSubmissions } from '../lib/api';
import { getSessionId } from '../lib/session';
import { supabase, hasSupabaseConfig } from '../lib/supabase';
import ProblemCard from '../components/ProblemCard';

const ALL_CATEGORIES = [
  'All', 'Arrays', 'Sliding Window', 'Two Pointers',
  'Binary Search', 'Linked Lists', 'Trees', 'Graphs',
  'Dynamic Programming', 'Tries', 'Heaps',
];

export default function Home() {
  const [problems, setProblems] = useState([]);
  const [submissions, setSubmissions] = useState([]);
  const [activeCategory, setActiveCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadHomeData = async () => {
      try {
        let uid = getSessionId();
        if (hasSupabaseConfig()) {
          const { data: { session } } = await supabase.auth.getSession();
          if (session?.user) {
            uid = session.user.id;
          }
        }
        const [problemsRes, subsRes] = await Promise.all([
          getProblems(),
          getSubmissions(uid),
        ]);
        setProblems(problemsRes.data);
        setSubmissions(subsRes.data);
      } catch (err) {
        setError('Could not reach the backend. Is the server running?');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadHomeData();
  }, []);

  const filtered = activeCategory === 'All'
    ? problems
    : problems.filter((p) => p.category === activeCategory);

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <span>Loading problems…</span>
      </div>
    );
  }

  return (
    <div className="home-page">
      <div className="home-hero">
        <h1>Master DSA with AI Feedback</h1>
        <p>
          Submit your solution, get structured analysis grounded in expert reference docs —
          not generic LLM guesses.
        </p>
      </div>

      {error && <div className="error-box" style={{ marginBottom: '1.5rem' }}>{error}</div>}

      {/* Category filter */}
      <div className="filters">
        {ALL_CATEGORIES.map((cat) => (
          <button
            key={cat}
            id={`filter-${cat.toLowerCase().replace(/\s+/g, '-')}`}
            className={`filter-btn ${activeCategory === cat ? 'active' : ''}`}
            onClick={() => setActiveCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Stats row */}
      <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
        <span>{filtered.length} problems</span>
        <span>·</span>
        <span>{submissions.filter(s => s.is_optimal).length} solved optimally</span>
        <span>·</span>
        <span>{new Set(submissions.map(s => s.problem_slug)).size} attempted</span>
      </div>

      <div className="problems-grid">
        {filtered.map((problem) => (
          <ProblemCard key={problem.slug} problem={problem} submissions={submissions} />
        ))}
      </div>
    </div>
  );
}
