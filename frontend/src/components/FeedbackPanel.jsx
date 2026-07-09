// FeedbackPanel.jsx — Displays structured AI analysis results.
// Each JSON field from the LLM is rendered as its own distinct UI component.

const VERDICT_CLASS = {
  Optimal:    'optimal',
  Acceptable: 'acceptable',
  Suboptimal: 'suboptimal',
  Incorrect:  'incorrect',
};

const VERDICT_ICON = {
  Optimal:    '✓',
  Acceptable: '~',
  Suboptimal: '⚠',
  Incorrect:  '✕',
};

export default function FeedbackPanel({ feedback, isLoading }) {
  if (isLoading) {
    return (
      <div className="feedback-empty">
        <div className="spinner" />
        <span>Analyzing your code with AI…</span>
        <span className="text-muted" style={{ fontSize: '0.8rem' }}>
          Using Groq llama-3.3-70b · up to 10 seconds
        </span>
      </div>
    );
  }

  if (!feedback) {
    return (
      <div className="feedback-empty">
        <span style={{ fontSize: '1.5rem' }}>📋</span>
        <span>Submit your code to get AI feedback</span>
        <span className="text-muted" style={{ fontSize: '0.8rem' }}>
          Complexity analysis · edge cases · improvement hints
        </span>
      </div>
    );
  }

  const verdictClass = VERDICT_CLASS[feedback.verdict] || 'suboptimal';
  const verdictIcon  = VERDICT_ICON[feedback.verdict]  || '?';

  return (
    <div className="feedback-content">
      {/* Verdict banner */}
      <div className={`verdict-banner ${verdictClass}`}>
        <span style={{ fontSize: '1.2rem' }}>{verdictIcon}</span>
        <div>
          <div style={{ fontWeight: 700 }}>{feedback.verdict}</div>
          {feedback.confidence && (
            <div style={{ fontSize: '0.75rem', opacity: 0.75 }}>
              Confidence: {feedback.confidence}
            </div>
          )}
        </div>
      </div>

      {/* Complexity */}
      <div className="complexity-row">
        <div className="complexity-item">
          <div className="complexity-label">Time Complexity</div>
          <div className="complexity-value mono">{feedback.time_complexity}</div>
        </div>
        <div className="complexity-item">
          <div className="complexity-label">Space Complexity</div>
          <div className="complexity-value mono">{feedback.space_complexity}</div>
        </div>
      </div>

      {/* Approach identified */}
      {feedback.approach_identified && (
        <div className="approach-box">
          <div className="label">Approach Identified</div>
          <div className="value">{feedback.approach_identified}</div>
        </div>
      )}

      {/* Edge cases missed */}
      {feedback.edge_cases_missed && feedback.edge_cases_missed.length > 0 && (
        <div className="edge-cases-section">
          <div className="label">Edge Cases Missed</div>
          <div className="edge-case-chips">
            {feedback.edge_cases_missed.map((ec, i) => (
              <span key={i} className="edge-chip">{ec}</span>
            ))}
          </div>
        </div>
      )}

      {/* Improvement hint */}
      {feedback.improvement_hint && (
        <div className="hint-box">
          <div className="hint-label">
            <span>💡</span> Improvement Hint
          </div>
          <div className="hint-text">{feedback.improvement_hint}</div>
        </div>
      )}
    </div>
  );
}
