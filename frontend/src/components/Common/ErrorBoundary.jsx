import React from 'react';
import { AlertTriangle, RefreshCw, Home, RotateCcw } from 'lucide-react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    console.error('[React Error Boundary]', error, errorInfo);
  }

  handleReload = () => {
    window.location.reload();
  };

  handleGoHome = () => {
    window.location.href = '/';
  };

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      // If used as an inline component/route error boundary
      if (this.props.inline) {
        return (
          <div
            role="alert"
            className="card"
            style={{
              padding: '2.5rem 1.5rem',
              textAlign: 'center',
              borderLeft: '4px solid var(--danger)',
              background: 'var(--bg-card)',
              margin: '1.5rem 0',
            }}
          >
            <div
              style={{
                width: '52px',
                height: '52px',
                borderRadius: '50%',
                background: 'rgba(239, 68, 68, 0.15)',
                color: '#ef4444',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem',
              }}
              aria-hidden="true"
            >
              <AlertTriangle size={26} />
            </div>

            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.5rem' }}>
              Something went wrong loading this section
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', maxWidth: '480px', margin: '0 auto 1.25rem', lineHeight: 1.55 }}>
              An unexpected interface error occurred. Please try again or return to the main dashboard.
            </p>

            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button
                type="button"
                onClick={this.handleReset}
                className="btn btn-primary"
                style={{ fontSize: '0.8125rem' }}
              >
                <RotateCcw size={14} />
                <span>Try Again</span>
              </button>
              <button
                type="button"
                onClick={this.handleGoHome}
                className="btn btn-secondary"
                style={{ fontSize: '0.8125rem' }}
              >
                <Home size={14} />
                <span>Go to Dashboard</span>
              </button>
            </div>
          </div>
        );
      }

      // Full-screen application fallback
      return (
        <div
          role="alert"
          style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2rem',
            background: 'var(--bg-primary, #0b0f19)',
            color: 'var(--text-main, #f8fafc)',
            fontFamily: 'var(--font-sans, sans-serif)',
          }}
        >
          <div
            style={{
              maxWidth: '560px',
              width: '100%',
              background: 'var(--bg-card, #161f33)',
              borderRadius: '16px',
              border: '1px solid rgba(239, 68, 68, 0.4)',
              padding: '2.5rem 2rem',
              textAlign: 'center',
              boxShadow: '0 20px 40px rgba(0, 0, 0, 0.5)',
            }}
          >
            <div
              style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                background: 'rgba(239, 68, 68, 0.15)',
                color: '#ef4444',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1.5rem',
              }}
              aria-hidden="true"
            >
              <AlertTriangle size={32} />
            </div>

            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '0.75rem', color: '#f8fafc' }}>
              Something went wrong
            </h1>
            <p style={{ color: 'var(--text-secondary, #94a3b8)', fontSize: '0.9375rem', marginBottom: '1.75rem', lineHeight: 1.6 }}>
              An unexpected interface error occurred. You can reload the application or return to the main dashboard.
            </p>

            {this.state.error && (
              <details
                style={{
                  textAlign: 'left',
                  background: 'rgba(11, 15, 25, 0.75)',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  marginBottom: '1.75rem',
                  fontSize: '0.8125rem',
                  color: '#f87171',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                }}
              >
                <summary style={{ cursor: 'pointer', fontWeight: 600 }}>Technical Details</summary>
                <pre style={{ marginTop: '0.5rem', whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
                  {this.state.error.toString()}
                </pre>
              </details>
            )}

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button
                type="button"
                onClick={this.handleReload}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.625rem 1.25rem',
                  background: 'var(--accent-primary, #6366f1)',
                  color: 'white',
                  borderRadius: '8px',
                  border: 'none',
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                }}
              >
                <RefreshCw size={16} />
                <span>Reload Application</span>
              </button>
              <button
                type="button"
                onClick={this.handleGoHome}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.625rem 1.25rem',
                  background: 'rgba(255, 255, 255, 0.08)',
                  color: 'var(--text-main, #f8fafc)',
                  borderRadius: '8px',
                  border: '1px solid var(--border-medium, #2d3b55)',
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                }}
              >
                <Home size={16} />
                <span>Go to Dashboard</span>
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
