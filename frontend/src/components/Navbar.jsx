import { Link, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { supabase, hasSupabaseConfig } from '../lib/supabase';

export default function Navbar() {
  const location = useLocation();
  const [user, setUser] = useState(null);

  const isActive = (path) => location.pathname === path ? 'active' : '';

  useEffect(() => {
    if (!hasSupabaseConfig()) return;

    // Get current user session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });

    // Listen to changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleSignOut = () => {
    if (hasSupabaseConfig()) {
      supabase.auth.signOut();
    }
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <div className="brand-icon">⚡</div>
        DSA Mentor
      </Link>
      <ul className="navbar-links">
        <li><Link to="/" className={isActive('/')}>Problems</Link></li>
        <li><Link to="/dashboard" className={isActive('/dashboard')}>Dashboard</Link></li>
        {user ? (
          <li>
            <a href="#signout" onClick={(e) => { e.preventDefault(); handleSignOut(); }} style={{ color: 'var(--red)' }}>
              Sign Out ({user.email.split('@')[0]})
            </a>
          </li>
        ) : (
          hasSupabaseConfig() && (
            <li><Link to="/dashboard" className={isActive('/dashboard')}>Sign In</Link></li>
          )
        )}
      </ul>
    </nav>
  );
}
