import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  BookOpen, 
  Target, 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  Loader2, 
  AlertCircle, 
  Sparkles, 
  Code, 
  Briefcase,
  Play
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import api from '../../services/api';

export default function SkillsPage() {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [activeGoal, setActiveGoal] = useState(null);
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchActiveGoalAndSkills = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch user's currently selected active goal
      let currentGoal = null;
      if (isAuthenticated) {
        try {
          const goalSelection = await api.request('/goals/current');
          if (goalSelection?.goal) {
            currentGoal = goalSelection.goal;
          }
        } catch (e) {
          console.warn('Could not fetch active goal:', e.message);
        }
      }

      // If no active goal yet, fallback to first goal (Full Stack Developer) for demonstration
      if (!currentGoal) {
        const allGoals = await api.request('/goals');
        if (allGoals?.length > 0) {
          currentGoal = allGoals[0];
        }
      }

      setActiveGoal(currentGoal);

      // 2. Fetch skills belonging to this goal
      if (currentGoal?.id) {
        const skillsData = await api.request(`/goals/${currentGoal.id}/skills`);
        setSkills(skillsData || []);
      }
    } catch (err) {
      setError(err.message || 'Failed to load skills for active goal.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActiveGoalAndSkills();
  }, [isAuthenticated]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Visual Workflow Progress Indicator */}
      <WorkflowProgressIndicator 
        currentStage="skill" 
        skillName={activeGoal ? `Track: ${activeGoal.title}` : null} 
      />

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div className="badge badge-indigo" style={{ marginBottom: '0.75rem' }}>
            <BookOpen size={14} />
            <span>Step 2: Skill Selection</span>
          </div>
          <h1 style={{ fontSize: 'clamp(1.75rem, 3.5vw, 2.25rem)', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
            {activeGoal ? `${activeGoal.title} — Skill Sequence` : 'Goal Skills Roadmap'}
          </h1>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '750px', fontSize: '1rem', lineHeight: 1.6 }}>
            Select a skill to begin its structured 7-stage learning journey: from comprehensive overview to topic breakdowns, hands-on practice, self-evaluation, and interview preparation.
          </p>
        </div>

        {/* Change Goal Shortcut */}
        <Link to="/goals" className="btn btn-outline" style={{ fontSize: '0.8125rem' }}>
          <Target size={16} />
          <span>Change Career Goal</span>
        </Link>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingState 
          message="Loading skills curriculum..." 
          subtext="Retrieving structured learning stages for your active career track."
          variant="skeleton"
        />
      )}

      {/* Error State */}
      {error && !loading && (
        <div role="alert" className="card" style={{ textAlign: 'center', padding: '2.5rem', borderLeft: '4px solid var(--danger)' }}>
          <AlertCircle size={36} style={{ color: 'var(--danger)', margin: '0 auto 0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Skills</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>{error}</p>
          <button type="button" onClick={fetchActiveGoalAndSkills} className="btn btn-primary">
            Retry Connection
          </button>
        </div>
      )}

      {/* Skills Grid */}
      {!loading && !error && skills.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {skills.map((skill, index) => (
            <div
              key={skill.id}
              className="card card-interactive"
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '1.5rem',
                gap: '1.5rem',
                flexWrap: 'wrap',
              }}
            >
              {/* Left Column: Index & Details */}
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.25rem', flex: '1 1 260px', minWidth: 0 }}>
                <div
                  style={{
                    width: '44px',
                    height: '44px',
                    borderRadius: '12px',
                    background: 'var(--accent-light)',
                    color: '#818cf8',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 800,
                    fontSize: '1.125rem',
                    flexShrink: 0,
                  }}
                >
                  {index + 1}
                </div>

                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.375rem' }}>
                    <h3 style={{ fontSize: '1.1875rem', fontWeight: 700, color: 'var(--text-main)', wordBreak: 'break-word' }}>
                      {skill.name}
                    </h3>
                    <span className="badge badge-indigo" style={{ fontSize: '0.6875rem' }}>
                      {skill.category}
                    </span>
                    <span 
                      className="badge" 
                      style={{ 
                        fontSize: '0.6875rem',
                        background: skill.is_technical ? 'rgba(59, 130, 246, 0.12)' : 'rgba(16, 185, 129, 0.12)',
                        color: skill.is_technical ? '#60a5fa' : '#34d399',
                        border: `1px solid ${skill.is_technical ? 'rgba(59, 130, 246, 0.25)' : 'rgba(16, 185, 129, 0.25)'}`
                      }}
                    >
                      {skill.is_technical ? 'Technical' : 'Non-Technical'}
                    </span>
                  </div>

                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.5, marginBottom: '0.75rem' }}>
                    {skill.description}
                  </p>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.8125rem', color: 'var(--text-muted)', flexWrap: 'wrap' }}>
                    <span>Sequence Step {index + 1} of {skills.length}</span>
                    <span>&bull;</span>
                    <span>7 Dedicated Learning Stages</span>
                  </div>
                </div>
              </div>

              {/* Right Column: Action Button */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
                <button
                  onClick={() => navigate(`/skills/${skill.id}/overview`)}
                  className="btn btn-primary"
                  style={{ padding: '0.6rem 1.25rem' }}
                >
                  <Play size={16} />
                  <span>Start Skill Journey</span>
                  <ArrowRight size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && skills.length === 0 && (
        <EmptyState
          icon={BookOpen}
          title="No Skills Found for this Track"
          description="There are currently no skills registered for this career goal. You can explore other technical or non-technical tracks."
          actionLabel="Explore Other Career Goals"
          actionTo="/goals"
        />
      )}
    </div>
  );
}
