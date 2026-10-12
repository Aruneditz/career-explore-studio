import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  Code, 
  Briefcase, 
  ArrowLeft, 
  ArrowRight, 
  Copy, 
  Check, 
  Eye, 
  EyeOff, 
  Compass, 
  Lightbulb, 
  Building2, 
  CheckCircle2, 
  Terminal, 
  BookOpen, 
  Loader2, 
  AlertCircle,
  HelpCircle,
  Sparkles,
  Layers
} from 'lucide-react';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import api from '../../services/api';

export default function PracticalSectionPage() {
  const { skillId } = useParams();
  const navigate = useNavigate();

  const [skill, setSkill] = useState(null);
  const [practicalItems, setPracticalItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Track which exercise solutions are revealed: { [itemId]: boolean }
  const [revealedSolutions, setRevealedSolutions] = useState({});
  // Track copy feedback: { [itemId]: boolean }
  const [copiedSnippetId, setCopiedSnippetId] = useState(null);

  const fetchSkillAndPractical = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch skill metadata to know if technical or non-technical
      const skillData = await api.request(`/skills/${skillId}`);
      setSkill(skillData);

      // 2. Fetch practical content items
      const practicalData = await api.request(`/skills/${skillId}/practical`);
      setPracticalItems(practicalData || []);

      // Record practical stage interaction
      api.request(`/skills/${skillId}/record-stage`, {
        method: 'POST',
        body: JSON.stringify({ stage: 'practical' }),
      }).catch(() => {});
    } catch (err) {
      setError(err.message || 'Failed to load practical content.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillAndPractical();
  }, [skillId]);

  const toggleSolution = (itemId) => {
    setRevealedSolutions((prev) => ({
      ...prev,
      [itemId]: !prev[itemId],
    }));
  };

  const handleCopyCode = async (itemId, codeText) => {
    if (!codeText) return;
    try {
      await navigator.clipboard.writeText(codeText);
      setCopiedSnippetId(itemId);
      setTimeout(() => setCopiedSnippetId(null), 2200);
    } catch (err) {
      console.error('Failed to copy code to clipboard', err);
    }
  };

  const isTechnical = skill?.is_technical ?? true;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Top Workflow Progress Indicator */}
      <WorkflowProgressIndicator 
        currentStage="practical" 
        skillId={skillId} 
        skillName={skill?.name} 
      />

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div className="badge badge-indigo" style={{ marginBottom: '0.75rem', gap: '0.375rem' }}>
            {isTechnical ? <Code size={13} /> : <Briefcase size={13} />}
            <span>Stage 4: Practical Application & Labs</span>
          </div>
          <h1 style={{ fontSize: 'clamp(1.75rem, 3.5vw, 2.25rem)', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
            {skill ? `${skill.name} — Practical Mastery` : 'Practical Section'}
          </h1>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '750px', fontSize: '1rem', lineHeight: 1.6 }}>
            {isTechnical
              ? 'Real-world code syntax, architectural patterns, and hands-on exercises with step-by-step reference solutions.'
              : 'Real-world commercial scenarios, case study breakdowns, and strategic situational activities with model approaches.'}
          </p>
        </div>

        {/* Back Link */}
        <Link to={`/skills/${skillId}/important-topics`} className="btn btn-outline" style={{ fontSize: '0.8125rem' }}>
          <ArrowLeft size={14} />
          <span>Must-Know Topics</span>
        </Link>
      </div>

      {/* Domain Badge Banner */}
      <div
        className="card"
        style={{
          background: isTechnical
            ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(56, 189, 248, 0.05))'
            : 'linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(20, 184, 166, 0.05))',
          border: `1px solid ${isTechnical ? 'rgba(99, 102, 241, 0.3)' : 'rgba(16, 185, 129, 0.3)'}`,
          padding: '1.25rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
          <div
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '10px',
              background: isTechnical ? 'rgba(99, 102, 241, 0.2)' : 'rgba(16, 185, 129, 0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: isTechnical ? '#818cf8' : '#34d399',
            }}
          >
            {isTechnical ? <Terminal size={22} /> : <Compass size={22} />}
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-primary)' }}>
              {isTechnical ? 'Technical Engineering Lab' : 'Strategic Business Case Lab'}
            </div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              {isTechnical
                ? 'Syntax-verified code implementations, real-world context, and interactive coding challenges.'
                : 'Scenario breakdowns, commercial risk analyses, and actionable executive frameworks without artificial code.'}
            </div>
          </div>
        </div>

        <span className={`badge ${isTechnical ? 'badge-indigo' : 'badge-success'}`}>
          {isTechnical ? 'Technical Track' : 'Non-Technical Track'}
        </span>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingState 
          message="Loading practical labs..." 
          subtext="Retrieving hands-on code examples, syntax blueprints, and reference implementations."
          variant="skeleton"
        />
      )}

      {/* Error State */}
      {error && !loading && (
        <div role="alert" className="card" style={{ borderColor: 'var(--danger)', background: 'rgba(239, 68, 68, 0.05)', padding: '2.5rem', textAlign: 'center' }}>
          <AlertCircle size={36} color="var(--danger)" style={{ margin: '0 auto 0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--danger)', marginBottom: '0.5rem' }}>Failed to Load Practical Content</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>{error}</p>
          <button type="button" onClick={fetchSkillAndPractical} className="btn btn-primary">
            Retry Connection
          </button>
        </div>
      )}

      {/* Practical Content Items */}
      {!loading && !error && practicalItems.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {practicalItems.map((item, index) => {
            const isRevealed = !!revealedSolutions[item.id];
            const isCopied = copiedSnippetId === item.id;

            return (
              <div
                key={item.id}
                className="card"
                style={{
                  background: 'var(--bg-secondary)',
                  border: '1px solid var(--border-medium)',
                  padding: '1.75rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '1.5rem',
                }}
              >
                {/* Item Header */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.75rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '8px',
                        background: 'var(--bg-primary)',
                        border: '1px solid var(--border-subtle)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 800,
                        fontSize: '0.875rem',
                        color: 'var(--accent-primary)',
                      }}
                    >
                      {index + 1}
                    </div>
                    <div>
                      <h2 style={{ fontSize: '1.25rem', fontWeight: 800, margin: 0 }}>
                        {item.title}
                      </h2>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'capitalize' }}>
                        Type: {item.content_type.replace('_', ' ')}
                      </span>
                    </div>
                  </div>

                  {item.language && (
                    <span className="badge badge-indigo" style={{ fontFamily: 'monospace', textTransform: 'uppercase', fontSize: '0.75rem' }}>
                      {item.language}
                    </span>
                  )}
                </div>

                {/* Technical: Code Snippet Viewer */}
                {isTechnical && item.code_snippet && (
                  <div>
                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        background: '#0d1117',
                        padding: '0.5rem 1rem',
                        borderTopLeftRadius: '8px',
                        borderTopRightRadius: '8px',
                        border: '1px solid #30363d',
                        borderBottom: 'none',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }} />
                        <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }} />
                        <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27c93f' }} />
                        <span style={{ fontSize: '0.75rem', color: '#8b949e', marginLeft: '0.5rem', fontFamily: 'monospace' }}>
                          syntax-pattern.{item.language || 'txt'}
                        </span>
                      </div>

                      <button
                        onClick={() => handleCopyCode(item.id, item.code_snippet)}
                        className="btn btn-outline"
                        style={{
                          padding: '0.25rem 0.6rem',
                          minHeight: '26px',
                          height: '26px',
                          fontSize: '0.75rem',
                          gap: '0.35rem',
                          borderColor: '#30363d',
                          color: isCopied ? 'var(--success)' : '#c9d1d9',
                        }}
                      >
                        {isCopied ? <Check size={13} color="var(--success)" /> : <Copy size={13} />}
                        <span>{isCopied ? 'Copied!' : 'Copy Code'}</span>
                      </button>
                    </div>

                    <pre
                      style={{
                        margin: 0,
                        padding: '1.25rem',
                        background: '#090d16',
                        border: '1px solid #30363d',
                        borderBottomLeftRadius: '8px',
                        borderBottomRightRadius: '8px',
                        overflowX: 'auto',
                        fontFamily: 'Consolas, Monaco, "Andale Mono", monospace',
                        fontSize: '0.875rem',
                        lineHeight: 1.6,
                        color: '#e6edf3',
                      }}
                    >
                      <code>{item.code_snippet}</code>
                    </pre>
                  </div>
                )}

                {/* Technical / Non-Technical: Explanation Box */}
                <div
                  style={{
                    background: 'var(--bg-primary)',
                    borderRadius: '8px',
                    padding: '1.25rem',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <Lightbulb size={16} color="var(--accent-primary)" />
                    <h4 style={{ fontSize: '0.9375rem', fontWeight: 700, margin: 0 }}>
                      {isTechnical ? 'Code Explanation & Mechanics' : 'Strategic Concept Breakdown'}
                    </h4>
                  </div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6, margin: 0 }}>
                    {item.explanation}
                  </p>
                </div>

                {/* Real-World Industry Context Box */}
                <div
                  style={{
                    background: 'rgba(56, 189, 248, 0.05)',
                    border: '1px solid rgba(56, 189, 248, 0.25)',
                    borderRadius: '8px',
                    padding: '1.25rem',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <Building2 size={16} color="#38bdf8" />
                    <h4 style={{ fontSize: '0.9375rem', fontWeight: 700, color: '#e0f2fe', margin: 0 }}>
                      {isTechnical ? 'Real-World Production Context' : 'Commercial Context & Case Study Environment'}
                    </h4>
                  </div>
                  <p style={{ color: '#cbd5e1', fontSize: '0.9rem', lineHeight: 1.6, margin: 0 }}>
                    {item.real_world_context}
                  </p>
                </div>

                {/* Interactive Practice Activity / Challenge */}
                {item.activity_prompt && (
                  <div
                    style={{
                      background: 'var(--bg-primary)',
                      border: '1px solid var(--border-medium)',
                      borderRadius: '8px',
                      padding: '1.25rem',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '1rem',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Sparkles size={16} color="#a5b4fc" />
                        <h4 style={{ fontSize: '0.9375rem', fontWeight: 700, margin: 0 }}>
                          {isTechnical ? 'Practice Exercise: Try It Yourself' : 'Strategic Scenario Exercise'}
                        </h4>
                      </div>

                      {/* Solution Reveal Toggle */}
                      {item.solution_or_guide && (
                        <button
                          type="button"
                          onClick={() => toggleSolution(item.id)}
                          className="btn btn-outline"
                          style={{
                            padding: '0.35rem 0.75rem',
                            fontSize: '0.78125rem',
                            minHeight: '30px',
                            gap: '0.4rem',
                          }}
                        >
                          {isRevealed ? <EyeOff size={14} /> : <Eye size={14} />}
                          <span>{isRevealed ? 'Hide Solution' : isTechnical ? 'Reveal Solution / Guide' : 'Reveal Model Approach'}</span>
                        </button>
                      )}
                    </div>

                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6, margin: 0 }}>
                      {item.activity_prompt}
                    </p>

                    {/* Collapsible Solution / Model Answer */}
                    {isRevealed && item.solution_or_guide && (
                      <div
                        style={{
                          marginTop: '0.5rem',
                          padding: '1rem 1.25rem',
                          background: 'rgba(16, 185, 129, 0.08)',
                          border: '1px solid rgba(16, 185, 129, 0.3)',
                          borderRadius: '8px',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '0.5rem',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--success)', fontWeight: 700, fontSize: '0.875rem' }}>
                          <CheckCircle2 size={16} />
                          <span>{isTechnical ? 'Reference Implementation & Solution Guide:' : 'Model Strategy & Action Plan:'}</span>
                        </div>
                        <div
                          style={{
                            color: 'var(--text-primary)',
                            fontSize: '0.875rem',
                            lineHeight: 1.65,
                            whiteSpace: 'pre-wrap',
                            fontFamily: isTechnical && item.solution_or_guide.includes(';') ? 'Consolas, Monaco, monospace' : 'inherit',
                          }}
                        >
                          {item.solution_or_guide}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && practicalItems.length === 0 && (
        <EmptyState
          icon={Code}
          title="Practical Labs in Preparation"
          description="Hands-on exercises and syntax guides are being prepared for this skill. You can move ahead to Learn & Complete."
          actionLabel="Move to Learn & Complete"
          actionTo={`/skills/${skillId}/learn`}
        />
      )}

      {/* Bottom Stage Navigation */}
      <div
        className="card responsive-actions stack-on-mobile"
        style={{
          padding: '1.25rem 1.5rem',
          background: 'var(--bg-secondary)',
        }}
      >
        <button
          onClick={() => navigate(`/skills/${skillId}/important-topics`)}
          className="btn btn-secondary"
        >
          <ArrowLeft size={16} />
          <span>&larr; Previous Stage: Must-Know Topics</span>
        </button>

        <button
          onClick={() => navigate(`/skills/${skillId}/learn`)}
          className="btn btn-primary"
        >
          <span>Move to Next Stage: Learn & Complete</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}
