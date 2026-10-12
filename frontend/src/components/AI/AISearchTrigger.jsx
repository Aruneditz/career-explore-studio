import React, { useState, useEffect } from 'react';
import { Search, Sparkles } from 'lucide-react';
import AISearchAssistant from './AISearchAssistant';

export default function AISearchTrigger({ skillId = null, topicId = null }) {
  const [modalOpen, setModalOpen] = useState(false);

  // Keyboard shortcut '/' opens search if not inside an input/textarea
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (
        e.key === '/' &&
        !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)
      ) {
        e.preventDefault();
        setModalOpen(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <>
      <button
        type="button"
        onClick={() => setModalOpen(true)}
        className="ai-search-trigger"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '0.75rem',
          padding: '0.4rem 0.875rem',
          background: 'rgba(15, 23, 42, 0.65)',
          border: '1px solid rgba(99, 102, 241, 0.3)',
          borderRadius: 'var(--radius-md)',
          color: 'var(--text-secondary)',
          cursor: 'pointer',
          fontSize: '0.8125rem',
          transition: 'all 0.2s ease',
          boxShadow: '0 2px 6px rgba(0, 0, 0, 0.2)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.6)';
          e.currentTarget.style.color = '#f8fafc';
          e.currentTarget.style.background = 'rgba(30, 41, 59, 0.8)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.3)';
          e.currentTarget.style.color = 'var(--text-secondary)';
          e.currentTarget.style.background = 'rgba(15, 23, 42, 0.65)';
        }}
        title="Ask Career Explore Studio AI Mentor (or press /)"
        aria-label="Ask Career Explore Studio AI Mentor"
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', overflow: 'hidden' }}>
          <Search size={15} style={{ color: 'var(--accent)', flexShrink: 0 }} />
          <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            Ask Career Explore Studio...
          </span>
        </div>

        <div className="ai-search-shortcut" style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          <span
            style={{
              padding: '0.1rem 0.35rem',
              borderRadius: '4px',
              background: 'rgba(255, 255, 255, 0.08)',
              fontSize: '0.6875rem',
              color: 'var(--text-tertiary)',
              fontWeight: 600,
            }}
          >
            /
          </span>
          <Sparkles size={14} style={{ color: '#a5b4fc', flexShrink: 0 }} />
        </div>
      </button>

      {modalOpen && (
        <AISearchAssistant
          isModal={true}
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          skillId={skillId}
          topicId={topicId}
        />
      )}
    </>
  );
}
