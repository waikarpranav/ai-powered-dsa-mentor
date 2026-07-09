import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { getProblem, analyzeCode } from '../lib/api';
import { getSessionId } from '../lib/session';
import { supabase, hasSupabaseConfig } from '../lib/supabase';
import FeedbackPanel from '../components/FeedbackPanel';

const DEFAULT_CODE = {
  java: `class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Write your solution here
        
    }
}`,
  python: `class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Write your solution here
        pass`,
};

export default function Workspace() {
  const { slug } = useParams();
  const navigate = useNavigate();

  const [problem, setProblem] = useState(null);
  const [language, setLanguage] = useState('java');
  const [code, setCode] = useState(DEFAULT_CODE.java);
  const [feedback, setFeedback] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [pageLoading, setPageLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getProblem(slug)
      .then((res) => setProblem(res.data))
      .catch(() => navigate('/'))
      .finally(() => setPageLoading(false));
  }, [slug, navigate]);

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
    setCode(DEFAULT_CODE[e.target.value]);
    setFeedback(null);
  };

  const handleSubmit = async () => {
    if (!code.trim()) return;
    setIsLoading(true);
    setError(null);
    setFeedback(null);
    try {
      let uid = getSessionId();
      if (hasSupabaseConfig()) {
        const { data: { session } } = await supabase.auth.getSession();
        if (session?.user) {
          uid = session.user.id;
        }
      }

      const res = await analyzeCode({
        problem_slug: slug,
        language,
        code,
        session_id: uid,
      });
      setFeedback(res.data.feedback);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Analysis failed. Check that the backend is running.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (pageLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <span>Loading problem…</span>
      </div>
    );
  }

  return (
    <div className="workspace-page">
      {/* ── Left: Problem statement ── */}
      <aside className="problem-panel">
        <button
          onClick={() => navigate('/')}
          style={{
            background: 'none', border: 'none', color: 'var(--text-muted)',
            cursor: 'pointer', fontSize: '0.85rem', padding: 0, marginBottom: '0.25rem',
            display: 'flex', alignItems: 'center', gap: '4px', fontFamily: 'inherit'
          }}
        >
          ← Back
        </button>

        {problem && (
          <>
            <h2>{problem.title}</h2>
            <div className="problem-tags">
              <span className={`badge badge-${problem.difficulty?.toLowerCase()}`}>
                {problem.difficulty}
              </span>
              <span className="badge badge-category">{problem.category}</span>
            </div>
            <p className="problem-description">{problem.description}</p>
          </>
        )}
      </aside>

      {/* ── Right: Editor + Feedback ── */}
      <div className="editor-panel">
        <div className="editor-toolbar">
          <select
            id="language-select"
            className="lang-select"
            value={language}
            onChange={handleLanguageChange}
          >
            <option value="java">Java</option>
            <option value="python">Python</option>
          </select>

          {error && (
            <div className="error-box" style={{ flex: 1, padding: '6px 12px' }}>
              {error}
            </div>
          )}

          <button
            id="submit-code-btn"
            className={`btn-submit ${isLoading ? 'loading' : ''}`}
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <div className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }} />
                Analyzing…
              </>
            ) : (
              <>⚡ Submit</>
            )}
          </button>
        </div>

        {/* Monaco Editor */}
        <div className="editor-wrapper">
          <Editor
            height="100%"
            language={language === 'java' ? 'java' : 'python'}
            value={code}
            onChange={(val) => setCode(val || '')}
            theme="vs-dark"
            options={{
              fontSize: 14,
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
              minimap: { enabled: false },
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
              tabSize: language === 'python' ? 4 : 4,
              wordWrap: 'on',
              padding: { top: 16 },
            }}
          />
        </div>

        {/* Feedback panel */}
        <div className="feedback-panel">
          <FeedbackPanel feedback={feedback} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}
