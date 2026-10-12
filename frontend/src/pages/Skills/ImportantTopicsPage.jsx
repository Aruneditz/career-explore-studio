import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  Star, 
  ArrowLeft, 
  ArrowRight, 
  CheckCircle2, 
  Circle, 
  Clock, 
  Loader2, 
  AlertCircle, 
  Sparkles,
  ShieldAlert,
  Flame
} from 'lucide-react';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import AISearchTrigger from '../../components/AI/AISearchTrigger';
import { useAuth } from '../../context/AuthContext';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import api from '../../services/api';

export default function ImportantTopicsPage() {
  const { skillId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [skill, setSkill] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterMode, setFilterMode] = useState('all'); // 'all', 'completed', 'remaining'
  const [togglingId, setTogglingId] = useState(null);

  const fetchSkillAndImportantTopics = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch skill overview for metadata
      const skillData = await api.request(`/skills/${skillId}`);
      setSkill(skillData);

      // 2. Fetch only Must-Know important topics
      const importantData = await api.request(`/skills/${skillId}/important-topics`);
      setTopics(importantData || []);
    } catch (err) {
      setError(err.message || 'Failed to load important topics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillAndImportantTopics();
  }, [skillId]);

  const handleToggleTopic = async (topic) => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/skills/${skillId}/important-topics` } } });
      return;
    }

    setTogglingId(topic.id);
    const targetState = !topic.is_completed;

    try {
      await api.request(`/skills/${skillId}/topics/${topic.id}/toggle`, {
        method: 'POST',
        body: JSON.stringify({ is_completed: targetState }),
      });

      // Update local state optimistically
      setTopics((prev) =>
        prev.map((t) => (t.id === topic.id ? { ...t, is_completed: targetState } : t))
      );
    } catch (err) {
      alert(`Could not update topic progress: ${err.message}`);
    } finally {
      setTogglingId(null);
    }
  };

  const completedCount = topics.filter((t) => t.is_completed).length;
  const totalCount = topics.length;
  const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  const filteredTopics = topics.filter((t) => {
    if (filterMode === 'completed') return t.is_completed;
    if (filterMode === 'remaining') return !t.is_completed;
    return true;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Top Workflow Progress Indicator */}
      <WorkflowProgressIndicator 
        currentStage="important" 
        skillId={skillId} 
        skillName={skill?.name} 
      />

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div className="badge badge-amber" style={{ marginBottom: '0.75rem', gap: '0.375rem' }}>
            <Star size={13} fill="currentColor" />
            <span>Stage 3: Must-Know Essential Topics</span>
          </div>
          <h1 style={{ fontSize: 'clamp(1.75rem, 3.5vw, 2.25rem)', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
            {skill ? `${skill.name} — Must-Know Focus` : 'Important Topics'}
          </h1>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '750px', fontSize: '1rem', lineHeight: 1.6 }}>
            The most critical high-yield concepts required for daily engineering or strategic execution. Technical and behavioral interviews target these areas with the highest frequency.
          </p>
        </div>

        {/* Header Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          <AISearchTrigger skillId={parseInt(skillId, 10)} />
          <Link to={`/skills/${skillId}/topics`} className="btn btn-outline" style={{ fontSize: '0.8125rem' }}>
            <ArrowLeft size={14} />
            <span>Full Curriculum</span>
          </Link>
        </div>
      </div>

      {/* Prominent High-Priority Alert Banner */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(217, 119, 6, 0.05))',
          border: '1px solid rgba(245, 158, 11, 0.35)',
          padding: '1.25rem 1.5rem',
          display: 'flex',
          gap: '1.25rem',
          alignItems: 'flex-start',
        }}
      >
        <div
          style={{
            width: '42px',
            height: '42px',
            borderRadius: '10px',
            background: 'rgba(245, 158, 11, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fbbf24',
            flexShrink: 0,
          }}
        >
          <Flame size={22} />
        </div>
        <div>
          <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#fef3c7', marginBottom: '0.35rem' }}>
            Why Prioritize These Topics?
          </h4>
          <p style={{ color: '#d1d5db', fontSize: '0.9rem', lineHeight: 1.6, margin: 0 }}>
            Mastering these topics guarantees you understand the 20% of concepts that drive 80% of real-world results. Hiring managers and technical interviewers test these fundamentals extensively to differentiate senior practitioners from novices.
          </p>
        </div>
      </div>

      {/* Topic Completion Stats Card */}
      <div className="card" style={{ background: 'var(--bg-secondary)', padding: '1.25rem 1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ fontSize: '1rem', fontWeight: 700 }}>
              Must-Know Mastery: {completedCount} of {totalCount} Topics Mastered
            </div>
            <span className="badge badge-amber" style={{ fontWeight: 700 }}>
              {progressPercent}% Mastered
            </span>
          </div>

          {/* Filter Pills */}
          <div style={{ display: 'flex', gap: '0.375rem' }}>
            {[
              { id: 'all', label: `All Must-Know (${totalCount})` },
              { id: 'completed', label: `Mastered (${completedCount})` },
              { id: 'remaining', label: `Remaining (${totalCount - completedCount})` },
            ].map((f) => (
              <button
                key={f.id}
                onClick={() => setFilterMode(f.id)}
                className={`btn ${filterMode === f.id ? 'btn-primary' : 'btn-outline'}`}
                style={{ padding: '0.3rem 0.65rem', minHeight: '30px', height: '30px', fontSize: '0.75rem' }}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* Progress Bar */}
        <div style={{ height: '8px', background: 'var(--bg-primary)', borderRadius: '9999px', overflow: 'hidden' }}>
          <div
            style={{
              height: '100%',
              width: `${progressPercent}%`,
              background: progressPercent === 100 ? 'var(--success)' : 'linear-gradient(90deg, #f59e0b, #fbbf24)',
              borderRadius: '9999px',
              transition: 'width 400ms cubic-bezier(0.4, 0, 0.2, 1)',
            }}
          />
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingState 
          message="Loading must-know topics..." 
          subtext="Filtering core essential concepts for interview readiness."
          variant="skeleton"
        />
      )}

      {/* Error State */}
      {error && !loading && (
        <div role="alert" className="card" style={{ textAlign: 'center', padding: '2.5rem', borderLeft: '4px solid var(--danger)' }}>
          <AlertCircle size={36} style={{ color: 'var(--danger)', margin: '0 auto 0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Topics</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>{error}</p>
          <button type="button" onClick={fetchSkillAndImportantTopics} className="btn btn-primary">
            Retry
          </button>
        </div>
      )}

      {/* Topic Cards List */}
      {!loading && !error && filteredTopics.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {filteredTopics.map((topic, index) => {
            const isToggling = togglingId === topic.id;
            return (
              <div
                key={topic.id}
                className="card"
                style={{
                  padding: '1.35rem 1.5rem',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  gap: '1.25rem',
                  background: topic.is_completed ? 'rgba(16, 185, 129, 0.03)' : 'var(--bg-secondary)',
                  borderColor: topic.is_completed ? 'rgba(16, 185, 129, 0.3)' : 'rgba(245, 158, 11, 0.25)',
                  transition: 'all 200ms ease',
                  flexWrap: 'wrap',
                }}
              >
                {/* Left Topic Details */}
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', flex: 1, minWidth: 'min(240px, 100%)' }}>
                  <div
                    style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      background: topic.is_completed ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                      color: topic.is_completed ? 'var(--success)' : '#f59e0b',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '0.8125rem',
                      fontWeight: 700,
                      flexShrink: 0,
                      marginTop: '0.15rem',
                    }}
                  >
                    {topic.is_completed ? <CheckCircle2 size={18} /> : index + 1}
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', minWidth: 0, flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
                      <h3
                        style={{
                          fontSize: '1.05rem',
                          fontWeight: 700,
                          color: topic.is_completed ? 'var(--text-muted)' : 'var(--text-primary)',
                          textDecoration: topic.is_completed ? 'line-through' : 'none',
                          margin: 0,
                          wordBreak: 'break-word',
                        }}
                      >
                        {topic.title}
                      </h3>
                      <span className="badge badge-amber" style={{ fontSize: '0.6875rem', gap: '0.25rem' }}>
                        <Star size={11} fill="currentColor" />
                        Must-Know
                      </span>
                    </div>

                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.5, margin: 0 }}>
                      {topic.description}
                    </p>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.25rem', flexWrap: 'wrap' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                        <Clock size={12} />
                        <span>~{topic.estimated_minutes} mins to master</span>
                      </div>
                      {topic.is_completed && (
                        <span style={{ color: 'var(--success)', fontSize: '0.75rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                          <CheckCircle2 size={12} />
                          Mastered
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Right Completion Toggle Button */}
                <button
                  onClick={() => handleToggleTopic(topic)}
                  disabled={isToggling}
                  className={`btn ${topic.is_completed ? 'btn-outline' : 'btn-primary'}`}
                  style={{
                    minWidth: '140px',
                    minHeight: '38px',
                    fontSize: '0.8125rem',
                    padding: '0.5rem 1rem',
                    flexShrink: 0,
                    borderColor: topic.is_completed ? 'rgba(16, 185, 129, 0.4)' : undefined,
                    color: topic.is_completed ? 'var(--success)' : undefined,
                  }}
                  title={topic.is_completed ? 'Mark as incomplete' : 'Mark as mastered'}
                >
                  {isToggling ? (
                    <Loader2 size={14} className="spinner" />
                  ) : topic.is_completed ? (
                    <>
                      <CheckCircle2 size={15} color="var(--success)" />
                      <span>Mastered</span>
                    </>
                  ) : (
                    <>
                      <Circle size={15} />
                      <span>Mark Mastered</span>
                    </>
                  )}
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && filteredTopics.length === 0 && (
        <EmptyState
          icon={Star}
          title="No Must-Know Topics Found"
          description="No must-know topics match your current filter. Switch to 'All Must-Know' to view the essential topics list."
          actionLabel="Show All Must-Know Topics"
          onAction={() => setFilterMode('all')}
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
          onClick={() => navigate(`/skills/${skillId}/topics`)}
          className="btn btn-secondary"
        >
          <ArrowLeft size={16} />
          <span>&larr; Previous Stage: Complete Topics</span>
        </button>

        <button
          onClick={() => navigate(`/skills/${skillId}/practical`)}
          className="btn btn-primary"
        >
          <span>Move to Next Stage: Practical Section</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}
