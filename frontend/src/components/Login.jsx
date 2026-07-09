import { useState } from 'react';
import { supabase, hasSupabaseConfig } from '../lib/supabase';

export default function Login({ onLoginComplete }) {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const isConfigured = hasSupabaseConfig();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!isConfigured) return;
    setLoading(true);
    setError(null);
    setMessage(null);

    const { error: authError } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: window.location.origin,
      },
    });

    if (authError) {
      setError(authError.message);
    } else {
      setMessage('✓ Magic link sent! Check your email inbox to sign in.');
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: '400px', margin: '4rem auto', padding: '2rem', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)' }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>Sign In</h2>
      <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        Enter your email to receive a passwordless Magic Link to log in or create an account.
      </p>

      {!isConfigured ? (
        <div className="error-box" style={{ fontSize: '0.8rem' }}>
          <strong>Supabase Auth not configured.</strong><br />
          Provide <code>VITE_SUPABASE_URL</code> and <code>VITE_SUPABASE_ANON_KEY</code> in your frontend <code>.env</code> file.
        </div>
      ) : (
        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Email Address</label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-sm)',
                color: '#fff',
                padding: '8px 12px',
                fontSize: '0.9rem',
                outline: 'none',
              }}
            />
          </div>

          {error && <div className="error-box" style={{ padding: '8px 12px' }}>{error}</div>}
          {message && <div style={{ color: 'var(--green)', fontSize: '0.85rem' }}>{message}</div>}

          <button
            type="submit"
            className="btn-submit"
            disabled={loading}
            style={{ width: '100%', justifyContent: 'center' }}
          >
            {loading ? 'Sending link...' : 'Send Magic Link ✉'}
          </button>
        </form>
      )}
    </div>
  );
}
