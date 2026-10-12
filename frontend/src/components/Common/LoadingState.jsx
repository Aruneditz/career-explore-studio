import React, { memo } from 'react';
import { Loader2 } from 'lucide-react';

function LoadingStateComponent({
  message = 'Loading data...',
  subtext = 'Please wait while we retrieve the latest information.',
  minHeight = '320px',
  variant = 'spinner', // 'spinner' | 'skeleton' | 'compact'
}) {
  if (variant === 'compact') {
    return (
      <div
        role="status"
        aria-live="polite"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.625rem',
          padding: '1.25rem 1rem',
          color: 'var(--text-secondary)',
          fontSize: '0.875rem',
        }}
      >
        <Loader2 size={18} className="animate-spin" style={{ color: 'var(--accent-primary)' }} aria-hidden="true" />
        <span>{message}</span>
        <span className="sr-only">Loading content...</span>
      </div>
    );
  }

  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight,
        padding: '3rem 1.5rem',
        textAlign: 'center',
        width: '100%',
      }}
    >
      <div
        style={{
          width: '56px',
          height: '56px',
          borderRadius: '16px',
          background: 'rgba(99, 102, 241, 0.1)',
          border: '1px solid rgba(99, 102, 241, 0.25)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: '1.25rem',
          boxShadow: '0 0 24px rgba(99, 102, 241, 0.2)',
        }}
        aria-hidden="true"
      >
        <Loader2
          size={30}
          className="animate-spin"
          style={{ color: 'var(--accent-primary)' }}
        />
      </div>

      <h3 style={{ fontSize: '1.1875rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.375rem' }}>
        {message}
      </h3>

      {subtext && (
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', maxWidth: '440px', lineHeight: 1.55 }}>
          {subtext}
        </p>
      )}

      {variant === 'skeleton' && (
        <div
          style={{
            marginTop: '2rem',
            width: 'min(500px, 90%)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem',
          }}
          aria-hidden="true"
        >
          <div className="skeleton-bar" style={{ height: '14px', width: '100%', borderRadius: '4px' }} />
          <div className="skeleton-bar" style={{ height: '14px', width: '85%', borderRadius: '4px' }} />
          <div className="skeleton-bar" style={{ height: '14px', width: '70%', borderRadius: '4px' }} />
        </div>
      )}

      <span className="sr-only">Loading content...</span>
    </div>
  );
}

export const LoadingState = memo(LoadingStateComponent);
export default LoadingState;
