import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ListChecks, 
  ArrowLeft, 
  ArrowRight, 
  CheckCircle2, 
  Circle, 
  Star, 
  Clock, 
  Loader2, 
  AlertCircle,
  Filter,
  Check,
  Sparkles
} from 'lucide-react';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import AISearchTrigger from '../../components/AI/AISearchTrigger';
import { useAuth } from '../../context/AuthContext';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import api from '../../services/api';

export default function CompleteTopicsPage() {
  const { skillId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [skill, setSkill] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterMode, setFilterMode] = useState('all'); // 'all', 'completed', 'remaining'
  const [togglingId, setTogglingId] = useState(null);

  const fetchSkillAndTopics = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch skill overview for metadata
      const skillData = await api.request(`/skills/${skillId}`);
      setSkill(skillData);

      // 2. Fetch complete topics list
      const topicsData = await api.request(`/skills/${skillId}/topics`);
      setTopics(topicsData || []);
    } catch (err) {
      setError(err.message || 'Failed to load topics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillAndTopics();
  }, [skillId]);

  const handleToggleTopic = async (topic) => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/skills/${skillId}/topics` } } });
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
        currentStage="topics" 
        skillId={skillId} 
        skillName={skill?.name} 
      />

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div className="badge badge-indigo" style={{ marginBottom: '0.75rem' }}>
            <ListChecks size={13} />
            <span>Stage 2: Complete Topic List</span>
          </div>
          <h1 style={{ fontSize: 'clamp(1.75rem, 3.5vw, 2.25rem)', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
            {skill ? `${skill.name} — Complete Curriculum` : 'Complete Topic List'}
          </h1>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '750px', fontSize: '1rem', lineHeight: 1.6 }}>
            Every foundational and advanced concept required to thoroughly understand this skill. Mark topics as completed as you progress through your learning.
          </p>
        </div>

        {/* Header Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          <AISearchTrigger skillId={parseInt(skillId, 10)} />
          <Link to={`/skills/${skillId}/overview`} className="btn btn-outline" style={{ fontSize: '0.8125rem' }}>
            <ArrowLeft size={14} />
            <span>Skill Overview</span>
          </Link>
        </div>
      </div>

      {/* Topic Completion Stats Card */}
      <div className="card" style={{ background: 'var(--bg-secondary)', padding: '1.25rem 1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ fontSize: '1rem', fontWeight: 700 }}>
              Curriculum Mastery: {completedCount} of {totalCount} Topics Completed
            </div>
            <span className="badge badge-success">
              {progressPercent}% Complete
            </span>
          </div>

          {/* Filter Pills */}
          <div style={{ display: 'flex', gap: '0.375rem' }}>
            {[
              { id: 'all', label: `All (${totalCount})` },
              { id: 'completed', label: `Completed (${completedCount})` },
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
              background: progressPercent === 100 ? 'var(--success)' : 'linear-gradient(90deg, #6366f1, #38bdf8)',
              borderRadius: '9999px',
              transition: 'width 250ms ease-out',
            }}
          />
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingState 
          message="Loading complete topic hierarchy..." 
          subtext="Retrieving full curriculum breakdown and completion milestones."
          variant="skeleton"
        />
      )}

      {/* Error State */}
      {error && !loading && (
        <div role="alert" className="card" style={{ textAlign: 'center', padding: '2.5rem', borderLeft: '4px solid var(--danger)' }}>
          <AlertCircle size={36} style={{ color: 'var(--danger)', margin: '0 auto 0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Topics</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>{error}</p>
          <button type="button" onClick={fetchSkillAndTopics} className="btn btn-primary">Retry</button>
        </div>
      )}

      {/* Topics List */}
      {!loading && !error && filteredTopics.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
          {filteredTopics.map((topic, index) => {
            const isCompleted = topic.is_completed;
            const isToggling = togglingId === topic.id;

            return (
              <div
                key={topic.id}
                className="card"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '1.125rem 1.25rem',
                  gap: '1rem',
                  borderLeft: isCompleted ? '4px solid var(--success)' : '4px solid var(--border-medium)',
                  background: isCompleted ? 'rgba(16, 185, 129, 0.04)' : 'var(--bg-card)',
                  transition: 'all var(--transition-fast)',
                  flexWrap: 'wrap',
                }}
              >
                {/* Topic Info */}
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.875rem', flex: 1, minWidth: 'min(240px, 100%)' }}>
                  <div
                    style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '8px',
                      background: isCompleted ? 'var(--success-bg)' : 'var(--bg-primary)',
                      color: isCompleted ? 'var(--success)' : 'var(--text-muted)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 700,
                      fontSize: '0.8125rem',
                      flexShrink: 0,
                    }}
                  >
                    {topic.order_index || index + 1}
                  </div>

                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.25rem' }}>
                      <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-main)', wordBreak: 'break-word' }}>
                        {topic.title}
                      </h4>

                      {topic.is_must_know && (
                        <span className="badge badge-warning" style={{ fontSize: '0.6875rem', gap: '0.25rem' }}>
                          <Star size={11} />
                          <span>Must-Know</span>
                        </span>
                      )}

                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        <Clock size={12} />
                        <span>~{topic.estimated_minutes} min</span>
                      </span>
                    </div>

                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem', lineHeight: 1.55 }}>
                      {topic.description}
                    </p>
                  </div>
                </div>

                {/* Completion Toggle Button */}
                <button
                  type="button"
                  onClick={() => handleToggleTopic(topic)}
                  disabled={isToggling}
                  className={`btn ${isCompleted ? 'btn-primary' : 'btn-outline'}`}
                  style={{
                    padding: '0.5rem 1rem',
                    minHeight: '38px',
                    fontSize: '0.8125rem',
                    background: isCompleted ? 'var(--success)' : 'transparent',
                    borderColor: isCompleted ? 'var(--success)' : 'var(--border-medium)',
                    color: isCompleted ? '#ffffff' : 'var(--text-secondary)',
                    flexShrink: 0,
                  }}
                  title={isCompleted ? 'Click to mark uncompleted' : 'Click to mark as completed'}
                >
                  {isToggling ? (
                    <Loader2 size={14} className="status-dot loading" />
                  ) : isCompleted ? (
                    <>
                      <Check size={14} />
                      <span>Completed</span>
                    </>
                  ) : (
                    <>
                      <Circle size={14} />
                      <span>Mark Complete</span>
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
          icon={ListChecks}
          title="No Topics Found"
          description="No topics match your selected completion filter. Switch to 'All' to review the full curriculum list."
          actionLabel="Show All Topics"
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
          onClick={() => navigate(`/skills/${skillId}/overview`)}
          className="btn btn-secondary"
        >
          <ArrowLeft size={16} />
          <span>&larr; Previous Stage: Skill Overview</span>
        </button>

        <button
          onClick={() => navigate(`/skills/${skillId}/important-topics`)}
          className="btn btn-primary"
        >
          <span>Move to Next Stage: Must-Know Topics</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}
