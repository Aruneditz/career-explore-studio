import React, { useState, useEffect, useRef } from 'react';
import {
  Search,
  Sparkles,
  Send,
  X,
  Loader2,
  Copy,
  Check,
  Compass,
  ArrowRight,
  BookOpen,
  Code,
  HelpCircle,
  AlertCircle,
  Lightbulb,
} from 'lucide-react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Link } from 'react-router-dom';

export default function AISearchAssistant({
  isModal = false,
  isOpen = true,
  onClose = null,
  skillId = null,
  topicId = null,
  title = "Career Explore Studio AI Mentor",
}) {
  const { isAuthenticated, token: authToken } = useAuth();
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [response, setResponse] = useState(null);
  const [suggestions, setSuggestions] = useState([
    "What should I learn next?",
    "Explain React useState simply",
    "What skills do I need for Full Stack Development?",
    "Give me Python interview questions",
    "Explain marketing in simple words",
  ]);
  const [copiedSection, setCopiedSection] = useState(null);
  const inputRef = useRef(null);

  // Fetch dynamic suggestions on mount
  useEffect(() => {
    const activeToken = authToken || localStorage.getItem('ces_auth_token') || localStorage.getItem('token') || localStorage.getItem('access_token');
    if (isAuthenticated || activeToken) {
      api.request('/ai/suggestions', {
        headers: activeToken ? { 'Authorization': `Bearer ${activeToken}` } : {},
      })
        .then((data) => {
          if (data?.suggestions?.length > 0) {
            setSuggestions(data.suggestions);
          }
        })
        .catch(() => {
          // Gracefully keep fallback suggestions
        });
    }
  }, [isAuthenticated, authToken]);

  // Focus input when modal opens
  useEffect(() => {
    if (isModal && isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isModal, isOpen]);

  // Handle escape key to close modal
  useEffect(() => {
    if (!isModal || !isOpen) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && onClose) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isModal, isOpen, onClose]);

  const handleAsk = async (queryText = null) => {
    const q = (queryText || prompt).trim();
    if (!q) return;

    const activeToken = authToken || localStorage.getItem('ces_auth_token') || localStorage.getItem('token') || localStorage.getItem('access_token');
    if (!activeToken && !isAuthenticated) {
      setError('Please sign in to ask the AI Mentor and access personalized guidance.');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const payload = {
        prompt: q,
        skill_id: skillId,
        topic_id: topicId,
      };
      const res = await api.request('/ai/ask', {
        method: 'POST',
        headers: activeToken ? { 'Authorization': `Bearer ${activeToken}` } : {},
        body: JSON.stringify(payload),
      });
      setResponse(res);
      if (res?.suggestions?.length > 0) {
        setSuggestions(res.suggestions);
      }
    } catch (err) {
      if (err.status === 401) {
        setError('Your session has expired or authentication is required. Please sign in to continue.');
      } else {
        setError(err.message || 'Something went wrong. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  const handleChipClick = (suggestionText) => {
    setPrompt(suggestionText);
    handleAsk(suggestionText);
  };

  const handleCopy = (text, sectionKey) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(sectionKey);
    setTimeout(() => setCopiedSection(null), 2000);
  };

  const handleClear = () => {
    setPrompt('');
    setResponse(null);
    setError(null);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  if (isModal && !isOpen) return null;

  const content = (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        width: '100%',
      }}
    >
      {/* Header bar in modal mode */}
      {isModal && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            paddingBottom: '0.875rem',
            borderBottom: '1px solid var(--border-medium)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
            <div
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Sparkles size={18} />
            </div>
            <div>
              <h3 id="ai-assistant-modal-title" style={{ fontSize: '1.0625rem', fontWeight: 800, color: '#f8fafc', margin: 0 }}>
                {title}
              </h3>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', margin: 0 }}>
                Instant career guidance, practical code, and interview mentoring
              </p>
            </div>
          </div>

          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="btn-icon"
              title="Close Assistant"
              aria-label="Close Assistant"
              style={{ width: '32px', height: '32px' }}
            >
              <X size={18} />
            </button>
          )}
        </div>
      )}

      {/* The Search Bar Box */}
      <div
        style={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          background: 'rgba(15, 23, 42, 0.75)',
          border: '1px solid rgba(99, 102, 241, 0.35)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: '0 4px 20px -2px rgba(0, 0, 0, 0.3)',
          transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
          padding: '0.35rem 0.5rem 0.35rem 1rem',
        }}
      >
        <div style={{ color: 'var(--accent)', display: 'flex', alignItems: 'center', marginRight: '0.75rem' }}>
          <Search size={20} />
        </div>

        <input
          ref={inputRef}
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask Career Explore Studio... (e.g., 'What should I learn next?', 'Explain useState simply')"
          disabled={loading}
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            outline: 'none',
            color: '#f8fafc',
            fontSize: '0.9375rem',
            padding: '0.5rem 0',
            fontFamily: 'inherit',
          }}
        />

        {/* Clear Button */}
        {prompt && (
          <button
            type="button"
            onClick={handleClear}
            className="btn-icon"
            title="Clear prompt"
            style={{ width: '28px', height: '28px', color: 'var(--text-tertiary)', marginRight: '0.25rem' }}
          >
            <X size={15} />
          </button>
        )}

        {/* Submit / Ask Button */}
        <button
          type="button"
          onClick={() => handleAsk()}
          disabled={loading || !prompt.trim()}
          className="btn btn-primary"
          style={{
            padding: '0.5rem 1.1rem',
            minHeight: '38px',
            height: '38px',
            fontSize: '0.8125rem',
            fontWeight: 700,
            gap: '0.4rem',
            background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
            boxShadow: '0 2px 10px rgba(99, 102, 241, 0.35)',
            flexShrink: 0,
          }}
        >
          {loading ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              <span>Thinking...</span>
            </>
          ) : (
            <>
              <Send size={15} />
              <span>Ask AI</span>
            </>
          )}
        </button>
      </div>

      {/* Empty State Prompt Cue (Section 13) */}
      {!response && !loading && !error && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.625rem 0.875rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px dashed var(--border-subtle)',
            color: 'var(--text-secondary)',
            fontSize: '0.8125rem',
          }}
        >
          <HelpCircle size={15} style={{ color: 'var(--accent-primary)', flexShrink: 0 }} />
          <span>Ask a question to get started. Explore career roadmaps, syntax breakdowns, and interview answers.</span>
        </div>
      )}

      {/* Suggested Prompt Chips */}
      {suggestions.length > 0 && !response && !loading && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            <Lightbulb size={13} style={{ color: '#f59e0b' }} />
            <span>Suggested questions:</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {suggestions.map((sugg, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleChipClick(sugg)}
                style={{
                  padding: '0.375rem 0.75rem',
                  borderRadius: '9999px',
                  background: 'rgba(30, 41, 59, 0.6)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  color: 'var(--text-secondary)',
                  fontSize: '0.75rem',
                  fontWeight: 500,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  textAlign: 'left',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.4)';
                  e.currentTarget.style.color = '#f8fafc';
                  e.currentTarget.style.background = 'rgba(99, 102, 241, 0.12)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)';
                  e.currentTarget.style.color = 'var(--text-secondary)';
                  e.currentTarget.style.background = 'rgba(30, 41, 59, 0.6)';
                }}
              >
                {sugg}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Unauthenticated User Friendly Banner */}
      {!isAuthenticated && !authToken && !localStorage.getItem('ces_auth_token') && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '0.75rem',
            padding: '0.625rem 0.875rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(99, 102, 241, 0.08)',
            border: '1px solid rgba(99, 102, 241, 0.25)',
            fontSize: '0.8125rem',
            color: '#c7d2fe',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={15} style={{ color: 'var(--accent)', flexShrink: 0 }} />
            <span>Sign in to unlock personalized AI mentoring tailored to your active goal.</span>
          </div>
          <Link
            to="/login"
            onClick={() => { if (onClose) onClose(); }}
            className="btn btn-primary"
            style={{
              padding: '0.35rem 0.75rem',
              fontSize: '0.75rem',
              textDecoration: 'none',
              whiteSpace: 'nowrap',
              flexShrink: 0,
            }}
          >
            Sign In
          </Link>
        </div>
      )}

      {/* Error state */}
      {error && (
        <div
          role="alert"
          style={{
            padding: '0.875rem 1rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.25)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '0.75rem',
            color: '#f87171',
            fontSize: '0.8125rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <span>{error}</span>
          </div>
          {(error.includes('sign in') || error.includes('Session')) && (
            <Link
              to="/login"
              onClick={() => { if (onClose) onClose(); }}
              className="btn btn-secondary"
              style={{
                padding: '0.3rem 0.65rem',
                fontSize: '0.75rem',
                textDecoration: 'none',
                whiteSpace: 'nowrap',
                flexShrink: 0,
              }}
            >
              Sign In &rarr;
            </Link>
          )}
        </div>
      )}

      {/* Loading Skeleton */}
      {loading && (
        <div
          role="status"
          aria-live="polite"
          style={{
            padding: '1.5rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(15, 23, 42, 0.6)',
            border: '1px solid var(--border-subtle)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.875rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
            <Loader2 size={18} className="animate-spin" style={{ color: 'var(--accent)' }} />
            <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
              Analyzing CES curriculum & synthesizing guidance...
            </span>
          </div>
          <div className="skeleton-bar" style={{ height: '14px', background: 'rgba(255,255,255,0.06)', borderRadius: '4px', width: '92%' }} />
          <div className="skeleton-bar" style={{ height: '14px', background: 'rgba(255,255,255,0.04)', borderRadius: '4px', width: '80%' }} />
          <div className="skeleton-bar" style={{ height: '14px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', width: '65%' }} />
          <span className="sr-only">Thinking...</span>
        </div>
      )}

      {/* Structured AI Response Area */}
      {response && !loading && (
        <div
          style={{
            padding: '1.25rem',
            borderRadius: 'var(--radius-md)',
            background: 'linear-gradient(180deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%)',
            border: '1px solid rgba(99, 102, 241, 0.3)',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
          }}
        >
          {/* Query header */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              paddingBottom: '0.75rem',
              borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Sparkles size={16} style={{ color: '#a5b4fc' }} />
              <span style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc' }}>
                {response.query}
              </span>
            </div>

            <button
              type="button"
              onClick={() => handleCopy(response.answer, 'all')}
              className="btn-icon"
              title="Copy answer"
              style={{ width: '28px', height: '28px', color: copiedSection === 'all' ? '#10b981' : 'var(--text-tertiary)' }}
            >
              {copiedSection === 'all' ? <Check size={14} /> : <Copy size={14} />}
            </button>
          </div>

          {/* Grounded CES Learning Context */}
          {response.context_used && (response.context_used.goal_title || response.context_used.current_skill) && (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                flexWrap: 'wrap',
                padding: '0.35rem 0.65rem',
                borderRadius: '6px',
                background: 'rgba(99, 102, 241, 0.08)',
                border: '1px solid rgba(99, 102, 241, 0.2)',
                fontSize: '0.75rem',
                color: '#a5b4fc',
              }}
            >
              <Compass size={13} style={{ color: '#818cf8', flexShrink: 0 }} />
              <span style={{ fontWeight: 600, color: 'var(--text-tertiary)' }}>Grounded Path:</span>
              {response.context_used.goal_title && (
                <span className="badge badge-indigo" style={{ fontSize: '0.6875rem', padding: '0.1rem 0.4rem' }}>
                  {response.context_used.goal_title}
                </span>
              )}
              {response.context_used.current_skill && (
                <span className="badge badge-info" style={{ fontSize: '0.6875rem', padding: '0.1rem 0.4rem' }}>
                  Active: {response.context_used.current_skill}
                </span>
              )}
              {response.context_used.topics_progress && response.context_used.topics_progress !== '0/0' && (
                <span className="badge" style={{ fontSize: '0.6875rem', padding: '0.1rem 0.4rem', background: 'rgba(255,255,255,0.06)', color: 'var(--text-secondary)' }}>
                  Topics: {response.context_used.topics_progress}
                </span>
              )}
              {response.context_used.evaluation_status && response.context_used.evaluation_status !== 'Pending' && (
                <span className="badge badge-success" style={{ fontSize: '0.6875rem', padding: '0.1rem 0.4rem' }}>
                  Quiz: {response.context_used.evaluation_status}
                </span>
              )}
            </div>
          )}

          {/* 1. Simple Explanation */}
          <div>
            <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.35rem' }}>
              Simple Explanation
            </div>
            <p style={{ fontSize: '0.875rem', color: '#e2e8f0', lineHeight: 1.6, margin: 0 }}>
              {response.answer}
            </p>
          </div>

          {/* 2. Simple Syntax / Framework */}
          {response.syntax_or_framework && (
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.35rem' }}>
                Simple Syntax / Structure
              </div>
              <div
                style={{
                  background: 'rgba(15, 23, 42, 0.8)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  borderRadius: '6px',
                  padding: '0.75rem 1rem',
                  fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                  fontSize: '0.8125rem',
                  color: '#38bdf8',
                  position: 'relative',
                  overflowX: 'auto',
                }}
              >
                {response.syntax_or_framework}
              </div>
            </div>
          )}

          {/* 3. Small Practical Example */}
          {response.code_example && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Small Practical Example
                </span>
                <button
                  type="button"
                  onClick={() => handleCopy(response.code_example, 'code')}
                  className="btn-icon"
                  style={{ width: '24px', height: '24px', color: copiedSection === 'code' ? '#10b981' : 'var(--text-tertiary)' }}
                  title="Copy example"
                >
                  {copiedSection === 'code' ? <Check size={13} /> : <Copy size={13} />}
                </button>
              </div>
              <pre
                style={{
                  background: 'rgba(15, 23, 42, 0.95)',
                  border: '1px solid rgba(255, 255, 255, 0.08)',
                  borderRadius: '6px',
                  padding: '0.875rem 1rem',
                  fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                  fontSize: '0.8125rem',
                  color: '#f1f5f9',
                  lineHeight: 1.5,
                  overflowX: 'auto',
                  margin: 0,
                }}
              >
                {response.code_example}
              </pre>
            </div>
          )}

          {/* 4. Practical Explanation */}
          {response.practical_explanation && (
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.35rem' }}>
                Practical Context
              </div>
              <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.55, margin: 0 }}>
                {response.practical_explanation}
              </p>
            </div>
          )}

          {/* 5. CES Recommendation Badge */}
          {response.ces_recommendation && (
            <div
              style={{
                marginTop: '0.25rem',
                padding: '0.875rem 1rem',
                borderRadius: 'var(--radius-md)',
                background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(16, 185, 129, 0.1) 100%)',
                border: '1px solid rgba(99, 102, 241, 0.35)',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.75rem',
              }}
            >
              <Compass size={18} style={{ color: '#818cf8', flexShrink: 0, marginTop: '2px' }} />
              <div>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#c7d2fe', textTransform: 'uppercase', letterSpacing: '0.04em', display: 'block', marginBottom: '0.2rem' }}>
                  CES Learning Recommendation
                </span>
                <span style={{ fontSize: '0.8125rem', color: '#f8fafc', lineHeight: 1.5 }}>
                  {response.ces_recommendation}
                </span>
              </div>
            </div>
          )}

          {/* Follow-up question chips */}
          {response.suggestions?.length > 0 && (
            <div style={{ marginTop: '0.25rem', paddingTop: '0.75rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
              <div style={{ fontSize: '0.6875rem', color: 'var(--text-tertiary)', marginBottom: '0.4rem', textTransform: 'uppercase', fontWeight: 600 }}>
                Follow-up questions:
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
                {response.suggestions.map((s, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleChipClick(s)}
                    style={{
                      padding: '0.25rem 0.625rem',
                      borderRadius: '9999px',
                      background: 'rgba(255, 255, 255, 0.05)',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      color: 'var(--text-secondary)',
                      fontSize: '0.6875rem',
                      cursor: 'pointer',
                    }}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );

  // If in modal mode, wrap in backdrop overlay
  if (isModal) {
    return (
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Career AI Assistant"
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(3, 7, 18, 0.75)',
          backdropFilter: 'blur(8px)',
          zIndex: 9999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 'clamp(0.5rem, 2.5vw, 1rem)',
          animation: 'fadeIn 0.2s ease',
        }}
        onClick={(e) => {
          if (e.target === e.currentTarget && onClose) {
            onClose();
          }
        }}
      >
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="ai-assistant-modal-title"
          style={{
            maxWidth: '680px',
            width: '100%',
            background: 'var(--bg-secondary)',
            border: '1px solid rgba(99, 102, 241, 0.4)',
            borderRadius: 'var(--radius-lg)',
            padding: 'clamp(0.875rem, 3vw, 1.5rem)',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.7)',
            maxHeight: '92vh',
            overflowY: 'auto',
          }}
          onClick={(e) => e.stopPropagation()}
        >
          {content}
        </div>
      </div>
    );
  }

  // Otherwise, return inline card container
  return (
    <div
      className="card"
      style={{
        padding: '1.25rem',
        background: 'rgba(15, 23, 42, 0.55)',
        border: '1px solid rgba(99, 102, 241, 0.25)',
      }}
    >
      {content}
    </div>
  );
}
