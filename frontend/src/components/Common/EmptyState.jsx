import React, { memo } from 'react';
import { FolderOpen, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

function EmptyStateComponent({
  icon: Icon = FolderOpen,
  title = 'No items found',
  description = 'There are no records matching your current filter criteria.',
  actionLabel,
  actionTo,
  onAction,
}) {
  return (
    <div
      className="card"
      role="region"
      aria-label={title}
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3.5rem 1.5rem',
        textAlign: 'center',
        background: 'var(--bg-card)',
        border: '1px dashed var(--border-medium)',
        width: '100%',
      }}
    >
      <div
        style={{
          width: '56px',
          height: '56px',
          borderRadius: '16px',
          background: 'rgba(255, 255, 255, 0.04)',
          border: '1px solid rgba(255, 255, 255, 0.06)',
          color: 'var(--text-muted)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: '1rem',
        }}
        aria-hidden="true"
      >
        <Icon size={28} />
      </div>

      <h3 style={{ fontSize: '1.1875rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.375rem' }}>
        {title}
      </h3>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', maxWidth: '460px', lineHeight: 1.55, marginBottom: actionLabel ? '1.5rem' : '0' }}>
        {description}
      </p>

      {actionLabel && (
        actionTo ? (
          <Link to={actionTo} className="btn btn-primary" style={{ fontSize: '0.8125rem' }}>
            <span>{actionLabel}</span>
            <ArrowRight size={14} />
          </Link>
        ) : onAction ? (
          <button type="button" onClick={onAction} className="btn btn-secondary" style={{ fontSize: '0.8125rem' }}>
            <span>{actionLabel}</span>
          </button>
        ) : null
      )}
    </div>
  );
}

export const EmptyState = memo(EmptyStateComponent);
export default EmptyState;
