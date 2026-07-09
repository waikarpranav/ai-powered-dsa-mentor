import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip,
} from 'recharts';
import { getSubmissions, getRecommendations } from '../lib/api';
import { getSessionId } from '../lib/session';
import { supabase, hasSupabaseConfig } from '../lib/supabase';
import Login from '../components/Login';

const VERDICT_COLOR = {
  Optimal:    'var(--green)',
  Acceptable: 'var(--blue)',
  Suboptimal: 'var(--yellow)',
  Incorrect:  'var(--red)',
};

function buildRadarData(stats) {
  return Object.entries(stats).map(([category, data]) => ({
    category: category.length > 12 ? category.split(' ')[0] : category,
    fullCategory: category,
    optimalRate: data.optimal_rate || 0,
  }));
}

export default function Dashboard() {
  const [submissions, setSubmissions] = useState([]);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    if (!hasSupabaseConfig()) {
      setAuthChecked(true);
      fetchDashboardData(getSessionId());
      return;
    }

    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setAuthChecked(true);
      if (session?.user) {
        fetchDashboardData(session.user.id);
      } else {
        setLoading(false);
      }
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
      if (session?.user) {
        setLoading(true);
        fetchDashboardData(session.user.id);
      } else {
        setSubmissions([]);
        setRecommendation(null);
        setLoading(false);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const fetchDashboardData = (uid) => {
    Promise.all([getSubmissions(uid), getRecommendations(uid)])
      .then(([subsRes, recRes]) => {
        setSubmissions(subsRes.data);
        setRecommendation(recRes.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  if (!authChecked || loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <span>Loading your dashboard…</span>
      </div>
    );
  }

  // If Supabase is active but no active user session, force Login screen
  if (hasSupabaseConfig() && !user) {
    return <Login onLoginComplete={() => window.location.reload()} />;
  }

  const totalSubs = submissions.length;
  const optimalCount = submissions.filter((s) => s.is_optimal).length;
  const optimalRate = totalSubs > 0 ? Math.round((optimalCount / totalSubs) * 100) : 0;
  const uniqueProblems = new Set(submissions.map((s) => s.problem_slug)).size;

  const radarData = recommendation?.stats ? buildRadarData(recommendation.stats) : [];

  return (
    <div className="dashboard-page">
      <h1>Your Progress</h1>

      {/* Recommendation card */}
      {recommendation && recommendation.next_problem && (
        <div className="recommendation-card">
          <h3>🎯 Recommended Next</h3>
          <p className="recommendation-message">{recommendation.message}</p>
          <Link
            to={`/problem/${recommendation.next_problem}`}
            className="btn-practice"
          >
            Practice Now →
          </Link>
        </div>
      )}

      {/* Stats grid */}
      <div className="dashboard-grid">
        {/* Stat cards */}
        <div className="dashboard-card">
          <h3>Total Submissions</h3>
          <div className="stat-number">{totalSubs}</div>
          <div className="stat-sub">{uniqueProblems} unique problems</div>
        </div>

        <div className="dashboard-card">
          <h3>Optimal Rate</h3>
          <div className="stat-number" style={{ color: optimalRate >= 60 ? 'var(--green)' : 'var(--yellow)' }}>
            {optimalRate}%
          </div>
          <div className="stat-sub">{optimalCount} of {totalSubs} submissions</div>
        </div>

        {/* Radar chart */}
        {radarData.length > 0 && (
          <div className="dashboard-card full-width">
            <h3>Performance by Category</h3>
            <ResponsiveContainer width="100%" height={280}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="var(--border)" />
                <PolarAngleAxis
                  dataKey="category"
                  tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
                />
                <PolarRadiusAxis
                  domain={[0, 100]}
                  tick={{ fill: 'var(--text-muted)', fontSize: 10 }}
                  tickCount={5}
                />
                <Radar
                  name="Optimal Rate"
                  dataKey="optimalRate"
                  stroke="var(--accent)"
                  fill="var(--accent)"
                  fillOpacity={0.25}
                  strokeWidth={2}
                />
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border)',
                    borderRadius: 8,
                    color: 'var(--text-primary)',
                    fontSize: '0.85rem',
                  }}
                  formatter={(val, name, props) => [
                    `${val}%`,
                    props.payload.fullCategory,
                  ]}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Recent submissions table */}
        {submissions.length > 0 && (
          <div className="dashboard-card full-width">
            <h3>Recent Submissions</h3>
            <table className="history-table">
              <thead>
                <tr>
                  <th>Problem</th>
                  <th>Language</th>
                  <th>Verdict</th>
                  <th>Time</th>
                  <th>Space</th>
                  <th>Submitted</th>
                </tr>
              </thead>
              <tbody>
                {submissions.slice(0, 20).map((sub) => (
                  <tr key={sub.id}>
                    <td>
                      <Link
                        to={`/problem/${sub.problem_slug}`}
                        style={{ color: 'var(--accent-light)', textDecoration: 'none' }}
                      >
                        {sub.problem_slug.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                      </Link>
                    </td>
                    <td className="mono" style={{ textTransform: 'capitalize' }}>{sub.language}</td>
                    <td>
                      <span style={{ color: VERDICT_COLOR[sub.verdict] || 'var(--text-secondary)', fontWeight: 600 }}>
                        {sub.verdict || '—'}
                      </span>
                    </td>
                    <td className="mono" style={{ fontSize: '0.8rem' }}>{sub.time_complexity || '—'}</td>
                    <td className="mono" style={{ fontSize: '0.8rem' }}>{sub.space_complexity || '—'}</td>
                    <td style={{ fontSize: '0.8rem' }}>
                      {new Date(sub.submitted_at).toLocaleDateString('en-IN', {
                        day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
                      })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {submissions.length === 0 && (
          <div className="dashboard-card full-width" style={{ textAlign: 'center', padding: '3rem' }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📊</div>
            <div style={{ color: 'var(--text-secondary)' }}>
              No submissions yet. <Link to="/" style={{ color: 'var(--accent-light)' }}>Solve a problem</Link> to see your stats here.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
