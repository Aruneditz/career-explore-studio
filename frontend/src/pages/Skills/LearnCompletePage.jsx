import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  CheckCircle2, 
  Circle, 
  ArrowLeft, 
  ArrowRight, 
  Award, 
  AlertCircle, 
  Loader2, 
  Sparkles, 
  RotateCcw, 
  CheckCheck, 
  BookOpen, 
  Star, 
  Flame, 
  Sliders
} from 'lucide-react';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import CertificateStatusCard from '../../components/Certificate/CertificateStatusCard';
import LoadingState from '../../components/Common/LoadingState';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

export default function LearnCompletePage() {
  const { skillId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState(null);

  const fetchProgress = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.request(`/skills/${skillId}/progress`);
      setProgress(data);
    } catch (err) {
      setError(err.message || 'Failed to load skill progress.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProgress();
  }, [skillId]);

  const handleCompleteSkill = async (completeAllTopics = false) => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/skills/${skillId}/learn` } } });
      return;
    }

    setActionLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const updated = await api.request(`/skills/${skillId}/complete`, {
        method: 'POST',
        body: JSON.stringify({ complete_all_topics: completeAllTopics }),
      });
      setProgress(updated);
      setSuccessMessage(
        completeAllTopics
          ? 'All topics marked as completed and skill successfully certified!'
          : 'Congratulations! Skill milestone officially completed.'
      );
    } catch (err) {
      setError(err.message || 'Failed to complete skill.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleResetProgress = async () => {
    if (!window.confirm('Are you sure you want to reset your progress for this skill and its topics?')) {
      return;
    }

    setActionLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const updated = await api.request(`/skills/${skillId}/reset-progress`, {
        method: 'POST',
      });
      setProgress(updated);
      setSuccessMessage('Progress for this skill has been reset.');
    } catch (err) {
      setError(err.message || 'Failed to reset progress.');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Top Workflow Progress Indicator */}
      <WorkflowProgressIndicator 
        currentStage="learn" 
        skillId={skillId} 
        skillName={progress?.skill_name} 
      />

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div className="badge badge-indigo" style={{ marginBottom: '0.75rem', gap: '0.375rem' }}>
            <CheckCircle2 size={13} />
            <span>Stage 5: Learn & Complete</span>
          </div>
          <h1 style={{ fontSize: 'clamp(1.75rem, 3.5vw, 2.25rem)', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
            {progress ? `${progress.skill_name} — Milestone Completion` : 'Learn & Complete'}
          </h1>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '750px', fontSize: '1rem', lineHeight: 1.6 }}>
            Verify that you have fulfilled all required curriculum topics, reviewed must-know concepts, and practiced hands-on exercises before recording your official completion.
          </p>
        </div>

        {/* Back Link */}
        <Link to={`/skills/${skillId}/practical`} className="btn btn-outline" style={{ fontSize: '0.8125rem' }}>
          <ArrowLeft size={14} />
          <span>Practical Section</span>
        </Link>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingState 
          message="Loading skill progress & milestones..." 
          subtext="Calculating curriculum stage completion and certificate readiness."
          variant="skeleton"
        />
      )}

      {/* Error Alert */}
      {error && (
        <div role="alert" className="card" style={{ borderColor: 'var(--danger)', background: 'rgba(239, 68, 68, 0.05)', padding: '1.5rem', display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
          <AlertCircle size={24} color="var(--danger)" style={{ flexShrink: 0, marginTop: '0.1rem' }} />
          <div>
            <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--danger)', margin: '0 0 0.25rem' }}>Action Notice</h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: 0 }}>{error}</p>
          </div>
        </div>
      )}

      {/* Success Alert */}
      {successMessage && (
        <div role="status" aria-live="polite" className="card" style={{ borderColor: 'var(--success)', background: 'rgba(16, 185, 129, 0.08)', padding: '1.5rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <Sparkles size={24} color="var(--success)" style={{ flexShrink: 0 }} />
          <div style={{ color: 'var(--text-primary)', fontWeight: 600, fontSize: '0.95rem' }}>
            {successMessage}
          </div>
        </div>
      )}

      {/* Main Progress & Checklist Details */}
      {!loading && progress && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          {/* Progress Overview Card */}
          <div className="card" style={{ background: 'var(--bg-secondary)', padding: '1.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 700 }}>
                  Curriculum Completion Status
                </span>
                <h3 style={{ fontSize: '1.35rem', fontWeight: 800, margin: '0.25rem 0 0' }}>
                  {progress.is_completed ? 'Skill Certified & Completed' : `${progress.progress_percentage}% Coursework Mastered`}
                </h3>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span className={`badge ${progress.is_completed ? 'badge-success' : progress.can_complete ? 'badge-indigo' : 'badge-amber'}`} style={{ fontSize: '0.8125rem' }}>
                  {progress.is_completed ? 'Completed' : progress.can_complete ? 'Ready to Complete' : 'In Progress'}
                </span>
              </div>
            </div>

            {/* Dynamic Progress Bar */}
            <div style={{ height: '10px', background: 'var(--bg-primary)', borderRadius: '9999px', overflow: 'hidden', marginBottom: '1.25rem' }}>
              <div
                style={{
                  height: '100%',
                  width: `${progress.progress_percentage}%`,
                  background: progress.is_completed 
                    ? 'var(--success)' 
                    : progress.can_complete 
                      ? 'linear-gradient(90deg, #6366f1, #10b981)' 
                      : 'linear-gradient(90deg, #f59e0b, #6366f1)',
                  borderRadius: '9999px',
                  transition: 'width 400ms ease',
                }}
              />
            </div>

            {/* Requirement Feedback Callout */}
            <div
              style={{
                padding: '1rem 1.25rem',
                borderRadius: '8px',
                background: progress.is_completed
                  ? 'rgba(16, 185, 129, 0.1)'
                  : progress.can_complete
                    ? 'rgba(99, 102, 241, 0.1)'
                    : 'rgba(245, 158, 11, 0.1)',
                border: `1px solid ${
                  progress.is_completed
                    ? 'rgba(16, 185, 129, 0.3)'
                    : progress.can_complete
                      ? 'rgba(99, 102, 241, 0.3)'
                      : 'rgba(245, 158, 11, 0.3)'
                }`,
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
              }}
            >
              {progress.is_completed ? (
                <CheckCircle2 size={20} color="var(--success)" style={{ flexShrink: 0 }} />
              ) : progress.can_complete ? (
                <Award size={20} color="#818cf8" style={{ flexShrink: 0 }} />
              ) : (
                <Flame size={20} color="#f59e0b" style={{ flexShrink: 0 }} />
              )}
              <div style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.5 }}>
                {progress.completion_requirements}
              </div>
            </div>
          </div>

          {/* Milestone Verification Breakdown Grid */}
          <div className="grid-3">
            {/* Metric 1: Curriculum Topics */}
            <div className="card" style={{ background: 'var(--bg-secondary)', padding: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>
                  All Topics
                </span>
                <BookOpen size={16} color="var(--text-muted)" />
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '0.25rem' }}>
                {progress.completed_topics} / {progress.total_topics}
              </div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                {progress.completed_topics === progress.total_topics ? 'All curriculum topics finished' : `${progress.total_topics - progress.completed_topics} topics remaining`}
              </div>
            </div>

            {/* Metric 2: Must-Know Focus */}
            <div className="card" style={{ background: 'var(--bg-secondary)', padding: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>
                  Must-Know Topics
                </span>
                <Star size={16} color="#f59e0b" fill="#f59e0b" />
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: progress.completed_must_know_topics === progress.must_know_topics ? 'var(--success)' : '#f59e0b', marginBottom: '0.25rem' }}>
                {progress.completed_must_know_topics} / {progress.must_know_topics}
              </div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                {progress.completed_must_know_topics === progress.must_know_topics ? 'Prerequisite criterion satisfied!' : 'Core interview threshold'}
              </div>
            </div>

            {/* Metric 3: Practical Application */}
            <div className="card" style={{ background: 'var(--bg-secondary)', padding: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>
                  Practical Labs
                </span>
                <Award size={16} color="var(--accent-primary)" />
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-primary)', marginBottom: '0.25rem' }}>
                Reviewed
              </div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                {progress.is_technical ? 'Code syntax & exercises' : 'Commercial scenarios & case studies'}
              </div>
            </div>
          </div>

          {/* Action Control Panel */}
          <div
            className="card"
            style={{
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border-medium)',
              padding: '1.75rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1.25rem',
            }}
          >
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700, margin: '0 0 0.25rem' }}>
                Completion Control Center
              </h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', margin: 0 }}>
                Section 16 requires verifying your learning progress before certifying skill completion.
              </p>
            </div>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center' }}>
              {/* Primary Complete Skill Button */}
              <button
                type="button"
                onClick={() => handleCompleteSkill(false)}
                disabled={actionLoading || !progress.can_complete || progress.is_completed}
                className="btn btn-primary"
                style={{
                  background: progress.is_completed ? 'var(--bg-primary)' : undefined,
                  borderColor: progress.is_completed ? 'var(--border-subtle)' : undefined,
                  color: progress.is_completed ? 'var(--text-muted)' : undefined,
                  padding: '0.65rem 1.5rem',
                  fontSize: '0.9375rem',
                  fontWeight: 700,
                  gap: '0.5rem',
                }}
              >
                {actionLoading ? (
                  <Loader2 size={16} className="spinner" />
                ) : progress.is_completed ? (
                  <>
                    <CheckCircle2 size={16} color="var(--success)" />
                    <span>Skill Already Completed</span>
                  </>
                ) : (
                  <>
                    <Award size={16} />
                    <span>Complete Skill</span>
                  </>
                )}
              </button>

              {/* Fast-Track: Mark All Topics as Studied & Complete */}
              {!progress.is_completed && (
                <button
                  type="button"
                  onClick={() => handleCompleteSkill(true)}
                  disabled={actionLoading}
                  className="btn btn-outline"
                  style={{
                    padding: '0.65rem 1.25rem',
                    fontSize: '0.875rem',
                    gap: '0.5rem',
                  }}
                  title="Mark all topics in this skill as completed and certify"
                >
                  <CheckCheck size={16} color="var(--success)" />
                  <span>Mark All Topics Studied & Complete</span>
                </button>
              )}

              {/* Reset Progress Button */}
              {progress.progress_percentage > 0 && (
                <button
                  type="button"
                  onClick={handleResetProgress}
                  disabled={actionLoading}
                  className="btn btn-outline"
                  style={{
                    padding: '0.65rem 1rem',
                    fontSize: '0.8125rem',
                    gap: '0.4rem',
                    color: 'var(--text-muted)',
                    marginLeft: 'auto',
                  }}
                >
                  <RotateCcw size={14} />
                  <span>Reset Progress</span>
                </button>
              )}
            </div>
          </div>

          {/* Official Course / Skill Certificate Experience (Upgrade #5) */}
          <CertificateStatusCard 
            skillId={skillId} 
            skillName={progress.skill_name} 
            onUnlocked={() => fetchProgress()}
          />
        </div>
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
          onClick={() => navigate(`/skills/${skillId}/practical`)}
          className="btn btn-secondary"
        >
          <ArrowLeft size={16} />
          <span>&larr; Previous Stage: Practical Section</span>
        </button>

        <button
          onClick={() => navigate(`/skills/${skillId}/evaluation`)}
          className="btn btn-primary"
        >
          <span>Move to Next Stage: Personal Self-Evaluation</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}
