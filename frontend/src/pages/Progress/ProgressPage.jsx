import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Award,
  CheckCircle2,
  Clock,
  BarChart3,
  ArrowRight,
  Target,
  Loader2,
  BookOpen,
  AlertCircle,
  FileCheck,
  Trophy,
  Sparkles,
  Layers,
  Printer,
  ChevronRight,
  HelpCircle,
  Check,
  Lock,
  Compass,
  Briefcase,
  ShieldCheck
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import CertificateModal from '../../components/Certificate/CertificateModal';
import LoadingState from '../../components/Common/LoadingState';
import api from '../../services/api';

export default function ProgressPage() {
  const { user } = useAuth();

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterSkillStatus, setFilterSkillStatus] = useState('all'); // 'all', 'completed', 'in_progress', 'not_started'
  const [certificates, setCertificates] = useState([]);
  const [selectedCertificate, setSelectedCertificate] = useState(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.request('/progress/dashboard');
      setDashboard(data);

      try {
        const certData = await api.request('/certificates');
        setCertificates(certData?.certificates || []);
      } catch (e) {
        // user may have no certificates yet
      }
    } catch (err) {
      console.error('Failed to load dashboard:', err);
      setError(err.message || 'Failed to load progress dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handlePrintTranscript = () => {
    window.print();
  };

  // Filter skills
  const filteredSkills = (dashboard?.skills || []).filter((s) => {
    if (filterSkillStatus === 'completed') return s.is_completed;
    if (filterSkillStatus === 'in_progress') return !s.is_completed && s.completed_topics > 0;
    if (filterSkillStatus === 'not_started') return s.completed_topics === 0;
    return true;
  });

  const getReadinessBadgeClass = (tier) => {
    if (!tier) return 'badge-secondary';
    if (tier.includes('Advanced') || tier.includes('Exceptional')) return 'badge-success';
    if (tier.includes('Interview-Ready')) return 'badge-indigo';
    if (tier.includes('Developing')) return 'badge-warning';
    return 'badge-secondary';
  };

  if (loading) {
    return (
      <LoadingState 
        message="Calculating real-time analytics..." 
        subtext="Aggregating curriculum milestones, evaluation diagnostics, and capstone progress."
        variant="skeleton"
      />
    );
  }

  if (error) {
    return (
      <div role="alert" className="card" style={{ maxWidth: '640px', margin: '2rem auto', textAlign: 'center', borderColor: 'var(--error)' }}>
        <AlertCircle size={44} style={{ color: 'var(--error)', margin: '0 auto 1rem' }} />
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Dashboard</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.875rem' }}>{error}</p>
        <button type="button" onClick={fetchDashboardData} className="btn btn-primary">
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', paddingBottom: '4rem' }}>
      {/* Top Banner / Header */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%)',
          border: '1px solid rgba(99, 102, 241, 0.3)',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1.5rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.75rem' }}>
              <div className="badge badge-indigo" style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <TrendingUp size={14} />
                <span>Learning Analytics & Progress Dashboard</span>
              </div>
              <div className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <Target size={14} />
                <span>{dashboard?.goal_title || 'Active Track'}</span>
              </div>
            </div>

            <h1 style={{ fontSize: '2rem', fontWeight: 800, letterSpacing: '-0.025em', marginBottom: '0.5rem', color: '#f8fafc' }}>
              {dashboard?.goal_title} Learning Roadmap
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', maxWidth: '720px', lineHeight: 1.6 }}>
              {dashboard?.goal_description || 'Track your live progress across chosen skills, completed topic milestones, diagnostic evaluations, and capstone interview preparation.'}
            </p>
          </div>

          {/* Action: Print Transcript */}
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <button
              onClick={handlePrintTranscript}
              className="btn btn-secondary"
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8125rem' }}
              title="Print official learning transcript"
            >
              <Printer size={15} />
              <span>Print Transcript</span>
            </button>
            <Link
              to="/profile"
              className="btn btn-secondary"
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8125rem' }}
            >
              <span>View Profile</span>
            </Link>
          </div>
        </div>

        {/* Global Progress Gauge Ribbon */}
        <div
          style={{
            marginTop: '2rem',
            padding: '1.25rem 1.5rem',
            background: 'rgba(15, 23, 42, 0.75)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Award size={18} color="#6366f1" />
              <span style={{ fontWeight: 700, fontSize: '1rem', color: '#f8fafc' }}>
                Curriculum Mastery Progress:
              </span>
              <span style={{ fontWeight: 800, color: '#10b981', fontSize: '1.125rem' }}>
                {dashboard?.overall_skill_percentage || 0}% Complete
              </span>
            </div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              <strong>{dashboard?.completed_skills || 0}</strong> of {dashboard?.total_skills || 0} Skills Mastered
            </div>
          </div>

          <div
            style={{
              height: '12px',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '999px',
              overflow: 'hidden',
              position: 'relative',
            }}
          >
            <div
              style={{
                height: '100%',
                width: `${Math.min(dashboard?.overall_skill_percentage || 0, 100)}%`,
                background: 'linear-gradient(90deg, #6366f1 0%, #10b981 100%)',
                borderRadius: '999px',
                transition: 'width 0.5s ease-out',
              }}
            />
          </div>
        </div>
      </div>

      {/* 4-Column Metric Highlights Grid */}
      <div className="grid-4" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(220px, 100%), 1fr))', gap: '1.25rem' }}>
        {/* Card 1: Skills Mastered */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Skills Mastered</span>
            <div style={{ padding: '0.4rem', borderRadius: '8px', background: 'rgba(99, 102, 241, 0.1)', color: '#818cf8' }}>
              <Layers size={18} />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>
            {dashboard?.completed_skills} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 500 }}>/ {dashboard?.total_skills}</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            {dashboard?.in_progress_skills} in progress, {dashboard?.total_skills - dashboard?.completed_skills - dashboard?.in_progress_skills} not started
          </div>
        </div>

        {/* Card 2: Topics Mastered */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Topic Milestones</span>
            <div style={{ padding: '0.4rem', borderRadius: '8px', background: 'rgba(16, 185, 129, 0.1)', color: '#34d399' }}>
              <BookOpen size={18} />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>
            {dashboard?.completed_topics} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 500 }}>/ {dashboard?.total_topics}</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            {dashboard?.completed_must_know_topics} / {dashboard?.must_know_topics} Must-Know topics finished ({dashboard?.topic_percentage}%)
          </div>
        </div>

        {/* Card 3: Learning Time */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Learning Time</span>
            <div style={{ padding: '0.4rem', borderRadius: '8px', background: 'rgba(245, 158, 11, 0.1)', color: '#fbbf24' }}>
              <Clock size={18} />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>
            {dashboard?.estimated_completed_hours}h <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 500 }}>/ {Math.round(dashboard?.estimated_total_minutes / 60)}h</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            {dashboard?.estimated_completed_minutes} active minutes invested
          </div>
        </div>

        {/* Card 4: Capstone Interview Practice */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Interview Prep</span>
            <div style={{ padding: '0.4rem', borderRadius: '8px', background: 'rgba(168, 85, 247, 0.1)', color: '#c084fc' }}>
              <Trophy size={18} />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>
            {dashboard?.practiced_interview_questions} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 500 }}>/ 15</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            {dashboard?.interview_progress_percentage}% of must-know questions practiced
          </div>
        </div>
      </div>

      {/* Diagnostic Readiness & Overall Assessment Summary */}
      <div
        className="card"
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1.5rem',
          borderLeft: '4px solid var(--accent-primary)',
          background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.7) 100%)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div
            style={{
              width: '50px',
              height: '50px',
              borderRadius: '12px',
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--accent-primary)',
            }}
          >
            <BarChart3 size={26} />
          </div>
          <div>
            <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
              CROSS-SKILL ARCHITECTURAL EVALUATION
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.25rem' }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
                {dashboard?.has_overall_evaluation ? (
                  <span>Score: {dashboard.overall_eval_score} / 10 ({dashboard.overall_eval_percentage}%)</span>
                ) : (
                  <span>Overall Evaluation Pending</span>
                )}
              </h3>
              {dashboard?.has_overall_evaluation && (
                <span className={`badge ${getReadinessBadgeClass(dashboard.overall_readiness_level)}`}>
                  {dashboard.overall_readiness_level}
                </span>
              )}
            </div>
          </div>
        </div>

        <div>
          <Link
            to="/overall-evaluation"
            className="btn btn-primary"
            style={{ fontSize: '0.875rem' }}
          >
            <span>{dashboard?.has_overall_evaluation ? 'Review Diagnostic Report' : 'Take Overall Evaluation'}</span>
            <ArrowRight size={16} />
          </Link>
        </div>
      </div>

      {/* Skills Roadmap Matrix */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 style={{ fontSize: '1.375rem', fontWeight: 800, color: '#f8fafc' }}>
              Curriculum Skills Roadmap
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Detailed breakdown of each skill milestone and individual diagnostic results.
            </p>
          </div>

          {/* Filter Tabs */}
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {[
              { id: 'all', label: 'All Skills' },
              { id: 'completed', label: 'Completed' },
              { id: 'in_progress', label: 'In Progress' },
              { id: 'not_started', label: 'Not Started' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setFilterSkillStatus(tab.id)}
                className={`btn ${filterSkillStatus === tab.id ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.4rem 0.85rem', fontSize: '0.8125rem', borderRadius: 'var(--radius-sm)' }}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Skills Cards Grid */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {filteredSkills.map((s) => (
            <div
              key={s.skill_id}
              className="card"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '1.25rem',
                borderLeft: s.is_completed ? '4px solid #10b981' : s.completed_topics > 0 ? '4px solid #f59e0b' : '4px solid var(--border-color)',
                padding: '1.25rem 1.5rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', minWidth: 'min(240px, 100%)' }}>
                <span
                  style={{
                    background: s.is_completed ? '#10b981' : 'var(--bg-primary)',
                    color: s.is_completed ? '#fff' : 'var(--text-secondary)',
                    border: '1px solid var(--border-subtle)',
                    width: '36px',
                    height: '36px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 700,
                    fontSize: '0.875rem',
                    flexShrink: 0,
                  }}
                >
                  {s.is_completed ? <Check size={18} /> : s.order_index}
                </span>

                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc' }}>
                      {s.skill_name}
                    </h3>
                    <span className="badge badge-secondary" style={{ fontSize: '0.6875rem' }}>
                      {s.skill_category}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                    {s.completed_topics} / {s.total_topics} topics mastered ({s.progress_percentage}%)
                    {s.evaluation_score !== null && (
                      <span style={{ marginLeft: '0.75rem', color: '#818cf8', fontWeight: 600 }}>
                        • Diagnostic: {s.evaluation_score}/5 ({s.evaluation_percentage}%)
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Skill Progress Bar & Links */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
                <div style={{ width: '120px' }}>
                  <div style={{ height: '6px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '999px', overflow: 'hidden' }}>
                    <div
                      style={{
                        height: '100%',
                        width: `${s.progress_percentage}%`,
                        background: s.is_completed ? '#10b981' : '#6366f1',
                      }}
                    />
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <Link
                    to={`/skills/${s.skill_id}/overview`}
                    className="btn btn-secondary"
                    style={{ fontSize: '0.75rem', padding: '0.4rem 0.75rem' }}
                  >
                    Overview
                  </Link>
                  <Link
                    to={`/skills/${s.skill_id}/topics`}
                    className="btn btn-secondary"
                    style={{ fontSize: '0.75rem', padding: '0.4rem 0.75rem' }}
                  >
                    Topics
                  </Link>
                  <Link
                    to={`/skills/${s.skill_id}/learn`}
                    className="btn btn-primary"
                    style={{ fontSize: '0.75rem', padding: '0.4rem 0.75rem' }}
                  >
                    {s.is_completed ? 'Completed' : 'Learn'}
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Official Verified Certificates Showcase (Upgrade #5) */}
      <div className="card" style={{ padding: '1.75rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Award size={24} style={{ color: '#10b981' }} />
            <div>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f8fafc', margin: 0 }}>
                Official Verified Certificates ({certificates.length})
              </h2>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem', margin: '0.25rem 0 0' }}>
                Credentials earned through 100% genuine completion of topics, practical labs, diagnostic evaluations, and interview prep.
              </p>
            </div>
          </div>
        </div>

        {certificates.length === 0 ? (
          <div
            style={{
              padding: '2rem',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(255, 255, 255, 0.02)',
              border: '1px dashed var(--border-medium)',
              textAlign: 'center',
            }}
          >
            <Lock size={32} style={{ color: 'var(--text-muted)', margin: '0 auto 0.75rem' }} />
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.375rem' }}>
              No Certificates Earned Yet
            </h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', maxWidth: '520px', margin: '0 auto 1.25rem', lineHeight: 1.5 }}>
              Complete all required stages to unlock your certificate. Certificates unlock only after completing all 4 required learning stages for a skill: Must-Know Topics, Practical Labs, Diagnostic Self-Evaluation, and Interview Preparation.
            </p>
            <Link to="/skills" className="btn btn-primary" style={{ fontSize: '0.8125rem' }}>
              Browse Skills Curriculum &rarr;
            </Link>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
            {certificates.map((cert) => (
              <div
                key={cert.id}
                className="card"
                style={{
                  padding: '1.5rem',
                  background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(15, 23, 42, 0.9) 100%)',
                  border: '1px solid rgba(16, 185, 129, 0.35)',
                  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.25)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  gap: '1rem',
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                    <span className="badge badge-success" style={{ fontSize: '0.7rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                      <ShieldCheck size={12} /> Verified Credential
                    </span>
                    <span style={{ fontSize: '0.7rem', fontFamily: 'monospace', color: '#94a3b8' }}>
                      {cert.certificate_id}
                    </span>
                  </div>

                  <h3 style={{ fontSize: '1.125rem', fontWeight: 800, color: '#f8fafc', margin: '0 0 0.5rem', lineHeight: 1.4 }}>
                    {cert.title}
                  </h3>

                  <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                    Recipient: <strong style={{ color: '#e2e8f0' }}>{cert.recipient_name}</strong>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                    Issued: {new Date(cert.issued_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => setSelectedCertificate(cert)}
                  className="btn btn-primary"
                  style={{
                    background: 'var(--success)',
                    borderColor: 'var(--success)',
                    fontSize: '0.8125rem',
                    gap: '0.5rem',
                    width: '100%',
                    justifyContent: 'center',
                  }}
                >
                  <Award size={15} />
                  <span>View & Print Official Certificate</span>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Milestone & Achievement Badges Showcase */}
      <div className="card" style={{ padding: '1.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
          <Trophy size={24} style={{ color: '#f59e0b' }} />
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f8fafc' }}>
              Milestone & Achievement Badges
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>
              Earn badges as you advance through the curriculum, pass self-evaluations, and master interview questions.
            </p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
          {(dashboard?.achievements || []).map((badge) => (
            <div
              key={badge.id}
              style={{
                padding: '1.25rem',
                borderRadius: 'var(--radius-md)',
                background: badge.is_unlocked
                  ? 'linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(16, 185, 129, 0.08) 100%)'
                  : 'rgba(15, 23, 42, 0.4)',
                border: badge.is_unlocked
                  ? '1px solid rgba(16, 185, 129, 0.4)'
                  : '1px solid rgba(255, 255, 255, 0.06)',
                display: 'flex',
                gap: '1rem',
                alignItems: 'flex-start',
                opacity: badge.is_unlocked ? 1 : 0.65,
                transition: 'transform 0.2s ease',
              }}
            >
              <div
                style={{
                  width: '44px',
                  height: '44px',
                  borderRadius: '10px',
                  background: badge.is_unlocked ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                  color: badge.is_unlocked ? '#10b981' : 'var(--text-tertiary)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                }}
              >
                {badge.is_unlocked ? <Sparkles size={22} /> : <Lock size={20} />}
              </div>

              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', marginBottom: '0.25rem' }}>
                  <h4 style={{ fontSize: '0.9375rem', fontWeight: 700, color: badge.is_unlocked ? '#f8fafc' : 'var(--text-secondary)' }}>
                    {badge.title}
                  </h4>
                  {badge.is_unlocked && <CheckCircle2 size={14} color="#10b981" />}
                </div>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                  {badge.description}
                </p>
                <span
                  style={{
                    display: 'inline-block',
                    marginTop: '0.5rem',
                    fontSize: '0.6875rem',
                    fontWeight: 600,
                    color: badge.is_unlocked ? '#34d399' : 'var(--text-tertiary)',
                  }}
                >
                  {badge.is_unlocked ? 'Unlocked' : 'In Progress'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {selectedCertificate && (
        <CertificateModal
          certificate={selectedCertificate}
          onClose={() => setSelectedCertificate(null)}
        />
      )}
    </div>
  );
}
