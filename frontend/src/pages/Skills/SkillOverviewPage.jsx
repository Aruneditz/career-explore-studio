import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  BookOpen, 
  ArrowLeft, 
  ArrowRight, 
  HelpCircle, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  Compass, 
  Layers, 
  Loader2, 
  AlertCircle,
  FileText
} from 'lucide-react';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import AISearchTrigger from '../../components/AI/AISearchTrigger';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import api from '../../services/api';

export default function SkillOverviewPage() {
  const { skillId } = useParams();
  const navigate = useNavigate();

  const [skill, setSkill] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSkillOverview = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.request(`/skills/${skillId}`);
      setSkill(data);
    } catch (err) {
      setError(err.message || 'Failed to load skill overview.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillOverview();
  }, [skillId]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Top Workflow Progress Indicator */}
      <WorkflowProgressIndicator 
        currentStage="overview" 
        skillId={skillId} 
        skillName={skill?.name} 
      />

      {/* Loading State */}
      {loading && (
        <LoadingState 
          message="Loading skill overview..." 
          subtext="Retrieving skill scope, prerequisite stack, and industry relevance."
          variant="skeleton"
        />
      )}

      {/* Error State */}
      {error && !loading && (
        <div role="alert" className="card" style={{ textAlign: 'center', padding: '2.5rem', borderLeft: '4px solid var(--danger)' }}>
          <AlertCircle size={36} style={{ color: 'var(--danger)', margin: '0 auto 0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Overview</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>{error}</p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <button type="button" onClick={fetchSkillOverview} className="btn btn-primary">Retry</button>
            <Link to="/skills" className="btn btn-secondary">Back to Skills</Link>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && !skill && (
        <EmptyState
          icon={BookOpen}
          title="Skill Not Found"
          description="The requested skill could not be found or has not been configured in the curriculum."
          actionLabel="Back to Skills Sequence"
          actionTo="/skills"
        />
      )}

      {/* Skill Overview Content */}
      {!loading && !error && skill && (
        <>
          {/* Header Title Section */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '0.75rem' }}>
                <span className="badge badge-indigo">
                  <FileText size={13} />
                  <span>Stage 1: Skill Overview</span>
                </span>
                <span 
                  className="badge"
                  style={{
                    background: skill.is_technical ? 'rgba(59, 130, 246, 0.12)' : 'rgba(16, 185, 129, 0.12)',
                    color: skill.is_technical ? '#60a5fa' : '#34d399',
                    border: `1px solid ${skill.is_technical ? 'rgba(59, 130, 246, 0.25)' : 'rgba(16, 185, 129, 0.25)'}`
                  }}
                >
                  {skill.is_technical ? 'Technical' : 'Non-Technical'}
                </span>
              </div>

              <h1 style={{ fontSize: 'clamp(1.85rem, 3.5vw, 2.5rem)', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
                {skill.name}
              </h1>
              <p style={{ color: 'var(--text-secondary)', maxWidth: '780px', fontSize: '1.05rem', lineHeight: 1.6 }}>
                {skill.description}
              </p>
            </div>

            {/* Topic Count Stats Pill & AI Mentor Trigger */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.75rem' }}>
              <div className="card" style={{ padding: '0.875rem 1.25rem', background: 'var(--bg-secondary)', textAlign: 'right' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                  Total Structured Topics
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-main)' }}>
                  {skill.total_topics} Topics
                </div>
                <div style={{ fontSize: '0.75rem', color: '#818cf8' }}>
                  {skill.must_know_topics} Must-Know Essentials
                </div>
              </div>
              <AISearchTrigger skillId={parseInt(skillId, 10)} />
            </div>
          </div>

          {/* Section 12 Detailed Overview Cards */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {/* 1. What is this skill? */}
            <div className="card">
              <h2 style={{ fontSize: '1.1875rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ffffff' }}>
                <Sparkles size={18} color="var(--accent-primary)" />
                <span>1. What is this skill?</span>
              </h2>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', lineHeight: 1.7 }}>
                {skill.what_is_it || skill.description}
              </p>
            </div>

            {/* 2. Why is it important & Where is it used? */}
            <div className="grid-2">
              <div className="card">
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <CheckCircle2 size={18} color="#10b981" />
                  <span>2. Why is it important?</span>
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.65 }}>
                  {skill.why_important || 'Provides foundational competencies required to deliver scalable, reliable solutions.'}
                </p>
              </div>

              <div className="card">
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Compass size={18} color="#38bdf8" />
                  <span>3. Where is it used?</span>
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.65 }}>
                  {skill.where_used || 'Utilized widely across production systems, agile teams, and modern commercial projects.'}
                </p>
              </div>
            </div>

            {/* 4. Benefits & Challenges */}
            <div className="grid-2">
              <div className="card" style={{ borderLeft: '4px solid #10b981' }}>
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#34d399' }}>
                  <CheckCircle2 size={18} />
                  <span>4. What are its benefits?</span>
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.65 }}>
                  {skill.benefits || 'High performance, developer ergonomics, long-term maintainability, and broad industry adoption.'}
                </p>
              </div>

              <div className="card" style={{ borderLeft: '4px solid #f59e0b' }}>
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#fbbf24' }}>
                  <AlertTriangle size={18} />
                  <span>5. Key challenges & considerations</span>
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.65 }}>
                  {skill.challenges || 'Requires disciplined practice to master subtle edge cases, architectural patterns, and performance bottlenecks.'}
                </p>
              </div>
            </div>

            {/* 6. Useful Prerequisites & 7. Career Relevance */}
            <div className="grid-2">
              <div className="card">
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Layers size={18} color="#818cf8" />
                  <span>6. Useful Prerequisites</span>
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.65 }}>
                  {skill.prerequisites || 'Familiarity with foundational principles of the career track.'}
                </p>
              </div>

              <div className="card" style={{ background: 'linear-gradient(135deg, rgba(22, 31, 51, 0.95) 0%, rgba(99, 102, 241, 0.08) 100%)' }}>
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#a5b4fc' }}>
                  <Sparkles size={18} />
                  <span>7. Relevance to Career Goal</span>
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.65 }}>
                  {skill.career_relevance || 'Essential milestone on the roadmap to industry readiness and technical interview mastery.'}
                </p>
              </div>
            </div>
          </div>

          {/* Bottom Stage Navigation */}
          <div
            className="card responsive-actions stack-on-mobile"
            style={{
              padding: '1.25rem 1.5rem',
              background: 'var(--bg-secondary)',
            }}
          >
            <button
              onClick={() => navigate('/skills')}
              className="btn btn-secondary"
            >
              <ArrowLeft size={16} />
              <span>&larr; Previous Stage: Skill Selection</span>
            </button>

            <button
              onClick={() => navigate(`/skills/${skillId}/topics`)}
              className="btn btn-primary"
            >
              <span>Move to Next Stage: Complete Topic List</span>
              <ArrowRight size={16} />
            </button>
          </div>
        </>
      )}
    </div>
  );
}
