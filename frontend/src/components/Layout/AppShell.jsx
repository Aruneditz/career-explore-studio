import React from 'react';
import Header from './Header';

export default function AppShell({ children, backendStatus }) {
  return (
    <div className="app-container">
      <Header backendStatus={backendStatus} />
      
      <main className="main-content">
        {children}
      </main>

      <footer style={{
        borderTop: '1px solid var(--border-subtle)',
        padding: '1.5rem',
        textAlign: 'center',
        color: 'var(--text-muted)',
        fontSize: '0.8125rem'
      }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div>
            <strong>CAREER EXPLORE STUDIO</strong> &bull; Phase 1 Architecture Shell
          </div>
          <div>
            FastAPI + SQLAlchemy + React + React Router
          </div>
        </div>
      </footer>
    </div>
  );
}
