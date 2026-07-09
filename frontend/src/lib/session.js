// Generates or retrieves a persistent anonymous session ID.
// Stored in localStorage so submissions persist across browser refreshes.
// Week 4: replace this with Supabase Auth user ID.

const SESSION_KEY = 'dsa_mentor_session_id';

export function getSessionId() {
  let sessionId = localStorage.getItem(SESSION_KEY);
  if (!sessionId) {
    // Generate a UUID v4
    sessionId = crypto.randomUUID
      ? crypto.randomUUID()
      : 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
          const r = (Math.random() * 16) | 0;
          return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
        });
    localStorage.setItem(SESSION_KEY, sessionId);
  }
  return sessionId;
}
