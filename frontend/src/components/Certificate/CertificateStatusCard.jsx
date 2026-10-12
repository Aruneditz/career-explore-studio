import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Award, 
  Lock, 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  Loader2, 
  ShieldCheck, 
  Printer, 
  Copy, 
  Check, 
  Sparkles,
  BookOpen,
  Sliders,
  HelpCircle,
  Code
} from 'lucide-react';
import api from '../../services/api';
import CertificateModal from './CertificateModal';

export default function CertificateStatusCard({ skillId, skillName, onUnlocked }) {
  const [statusData, setStatusData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [claiming, setClaiming] = useState(false);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const fetchStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.request(`/skills/${skillId}/certificate`);
      setStatusData(data);
      if (data?.is_unlocked && onUnlocked) {
        onUnlocked(data);
      }
    } catch (err) {
      console.error('Failed to load certificate status', err);
      setError(err.message || 'Failed to load certificate status.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (skillId) {
      fetchStatus();
    }
  }, [skillId]);

  const handleClaimCertificate = async () => {
    setClaiming(true);
    setError(null);
    try {
      const cert = await api.request(`/skills/${skillId}/claim-certificate`, {
        method: 'POST',
      });
      setStatusData((prev) => ({
        ...prev,
        is_unlocked: true,
        certificate: cert,
        status_message: 'Certificate Earned — Official credential verified and issued.',
      }));
      setShowModal(true);
    } catch (err) {
      setError(err.message || 'Failed to generate certificate.');
    } finally {
      setClaiming(false);
    }
  };

  if (loading) {
    return (
      <div className="card" style={{ padding: '2rem', textAlign: 'center', background: 'var(--bg-secondary)' }}>
        <Loader2 size={28} className="spinner" style={{ margin: '0 auto 0.75rem', color: 'var(--accent-primary)' }} />
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', margin: 0 }}>
          Verifying backend completion criteria & certificate status...
        </p>
      </div>
    );
  }

  if (error && !statusData) {
    return null; // Silent graceful degradation if unauthenticated
  }

  if (!statusData) return null;

  const { is_unlocked, checklist, certificate } = statusData;

  return (
    <>
      <div
        className="card"
        style={{
          padding: '1.75rem',
          background: is_unlocked
            ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(15, 23, 42, 0.95) 100%)'
            : 'linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.95) 100%)',
          border: is_unlocked
            ? '1px solid rgba(16, 185, 129, 0.4)'
            : '1px solid var(--border-medium)',
          boxShadow: is_unlocked ? '0 0 25px rgba(16, 185, 129, 0.1)' : 'none',
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem',
          position: 'relative',
        }}
      >
        {/* Header Bar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div
              style={{
                width: '44px',
                height: '44px',
                borderRadius: '12px',
                background: is_unlocked ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                color: is_unlocked ? '#10b981' : 'var(--text-muted)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
              }}
            >
              {is_unlocked ? <Award size={24} /> : <Lock size={22} />}
            </div>

            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                <span className={`badge ${is_unlocked ? 'badge-success' : 'badge-amber'}`} style={{ fontSize: '0.7rem' }}>
                  {certificate ? 'Certificate Earned' : is_unlocked ? 'Certificate Available' : 'Certificate Locked'}
                </span>
                {certificate && (
                  <span style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 600 }}>
                    ID: {certificate.certificate_id}
                  </span>
                )}
              </div>

              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, margin: 0, color: '#f8fafc' }}>
                {is_unlocked ? 'Official Skill Certificate Earned' : 'Official Skill Certificate Locked'}
              </h3>
            </div>
          </div>

          {/* Action Buttons */}
          <div>
            {certificate ? (
              <button
                type="button"
                onClick={() => setShowModal(true)}
                className="btn btn-primary"
                style={{
                  background: 'var(--success)',
                  borderColor: 'var(--success)',
                  gap: '0.5rem',
                  fontSize: '0.875rem',
                }}
              >
                <Award size={16} />
                <span>View Official Certificate</span>
              </button>
            ) : is_unlocked ? (
              <button
                type="button"
                onClick={handleClaimCertificate}
                disabled={claiming}
                className="btn btn-primary"
                style={{
                  gap: '0.5rem',
                  fontSize: '0.875rem',
                  background: 'linear-gradient(135deg, #6366f1, #10b981)',
                }}
              >
                {claiming ? <Loader2 size={16} className="spinner" /> : <Sparkles size={16} />}
                <span>Claim Official Certificate</span>
              </button>
            ) : null}
          </div>
        </div>

        {/* Status Explanation */}
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.55, margin: 0 }}>
          {is_unlocked
            ? `Congratulations! Your certificate is ready. You have genuinely satisfied all 4 required learning stages for ${statusData.skill_name}.`
            : `Complete all required stages to unlock your certificate. To unlock your certificate for ${statusData.skill_name}, you must complete all 4 required learning workflow stages below.`}
        </p>

        {/* Progress Bar */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.375rem', fontWeight: 600 }}>
            <span>Verification Criteria</span>
            <span>{checklist.progress_percentage}% Requirements Satisfied</span>
          </div>
          <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '999px', overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                width: `${checklist.progress_percentage}%`,
                background: is_unlocked ? '#10b981' : 'linear-gradient(90deg, #f59e0b, #6366f1)',
                transition: 'width 300ms ease',
              }}
            />
          </div>
        </div>

        {/* 4-Stage Learning Checklist Breakdown */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.875rem' }}>
          {/* Stage 1: Topics */}
          <div
            style={{
              padding: '0.875rem 1rem',
              borderRadius: '8px',
              background: checklist.topics_completed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
              border: `1px solid ${checklist.topics_completed ? 'rgba(16, 185, 129, 0.25)' : 'rgba(255, 255, 255, 0.08)'}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <BookOpen size={14} color={checklist.topics_completed ? '#10b981' : 'var(--text-muted)'} />
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f8fafc' }}>
                  1. Must-Know Topics
                </span>
              </div>
              {checklist.topics_completed ? <CheckCircle2 size={15} color="#10b981" /> : <XCircle size={15} color="#f59e0b" />}
            </div>
            <div style={{ fontSize: '0.75rem', color: checklist.topics_completed ? '#34d399' : 'var(--text-secondary)' }}>
              {checklist.topics_summary}
            </div>
            {!checklist.topics_completed && (
              <Link to={`/skills/${skillId}/topics`} style={{ fontSize: '0.6875rem', color: '#818cf8', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '2px', marginTop: '0.25rem' }}>
                Complete Topics &rarr;
              </Link>
            )}
          </div>

          {/* Stage 2: Practical Labs */}
          <div
            style={{
              padding: '0.875rem 1rem',
              borderRadius: '8px',
              background: checklist.practical_completed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
              border: `1px solid ${checklist.practical_completed ? 'rgba(16, 185, 129, 0.25)' : 'rgba(255, 255, 255, 0.08)'}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <Code size={14} color={checklist.practical_completed ? '#10b981' : 'var(--text-muted)'} />
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f8fafc' }}>
                  2. Practical Labs
                </span>
              </div>
              {checklist.practical_completed ? <CheckCircle2 size={15} color="#10b981" /> : <XCircle size={15} color="#f59e0b" />}
            </div>
            <div style={{ fontSize: '0.75rem', color: checklist.practical_completed ? '#34d399' : 'var(--text-secondary)' }}>
              {checklist.practical_summary}
            </div>
            {!checklist.practical_completed && (
              <Link to={`/skills/${skillId}/practical`} style={{ fontSize: '0.6875rem', color: '#818cf8', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '2px', marginTop: '0.25rem' }}>
                Review Labs &rarr;
              </Link>
            )}
          </div>

          {/* Stage 3: Self-Evaluation */}
          <div
            style={{
              padding: '0.875rem 1rem',
              borderRadius: '8px',
              background: checklist.evaluation_completed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
              border: `1px solid ${checklist.evaluation_completed ? 'rgba(16, 185, 129, 0.25)' : 'rgba(255, 255, 255, 0.08)'}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <Sliders size={14} color={checklist.evaluation_completed ? '#10b981' : 'var(--text-muted)'} />
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f8fafc' }}>
                  3. Self-Evaluation
                </span>
              </div>
              {checklist.evaluation_completed ? <CheckCircle2 size={15} color="#10b981" /> : <XCircle size={15} color="#f59e0b" />}
            </div>
            <div style={{ fontSize: '0.75rem', color: checklist.evaluation_completed ? '#34d399' : 'var(--text-secondary)' }}>
              {checklist.evaluation_summary}
            </div>
            {!checklist.evaluation_completed && (
              <Link to={`/skills/${skillId}/evaluation`} style={{ fontSize: '0.6875rem', color: '#818cf8', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '2px', marginTop: '0.25rem' }}>
                Take Evaluation &rarr;
              </Link>
            )}
          </div>

          {/* Stage 4: Interview Prep */}
          <div
            style={{
              padding: '0.875rem 1rem',
              borderRadius: '8px',
              background: checklist.interview_completed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
              border: `1px solid ${checklist.interview_completed ? 'rgba(16, 185, 129, 0.25)' : 'rgba(255, 255, 255, 0.08)'}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <HelpCircle size={14} color={checklist.interview_completed ? '#10b981' : 'var(--text-muted)'} />
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#f8fafc' }}>
                  4. Interview Prep
                </span>
              </div>
              {checklist.interview_completed ? <CheckCircle2 size={15} color="#10b981" /> : <XCircle size={15} color="#f59e0b" />}
            </div>
            <div style={{ fontSize: '0.75rem', color: checklist.interview_completed ? '#34d399' : 'var(--text-secondary)' }}>
              {checklist.interview_summary}
            </div>
            {!checklist.interview_completed && (
              <Link to={`/skills/${skillId}/interview-prep`} style={{ fontSize: '0.6875rem', color: '#818cf8', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '2px', marginTop: '0.25rem' }}>
                Review Questions &rarr;
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Certificate Modal */}
      {showModal && certificate && (
        <CertificateModal
          certificate={certificate}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
}
