import React, { useState, useEffect } from 'react';
import {
  User,
  Mail,
  Calendar,
  ShieldCheck,
  LogOut,
  Target,
  BookOpen,
  CheckCircle2,
  Edit2,
  Check,
  X,
  Award,
  Trophy,
  Printer,
  Sparkles,
  ArrowRight,
  Loader2,
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import LoadingState from '../../components/Common/LoadingState';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [profileSummary, setProfileSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Name Editing State
  const [isEditingName, setIsEditingName] = useState(false);
  const [newName, setNewName] = useState('');
  const [savingName, setSavingName] = useState(false);

  // Certificate Modal / View State
  const [showCertificate, setShowCertificate] = useState(false);

  const fetchProfileSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.request('/auth/profile-summary');
      setProfileSummary(data);
      setNewName(data?.user?.name || user?.name || '');
    } catch (err) {
      console.error('Failed to load profile summary:', err);
      setError(err.message || 'Failed to load profile data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfileSummary();
  }, []);

  const handleSaveName = async () => {
    if (!newName.trim()) return;
    setSavingName(true);
    try {
      const updatedUser = await api.request('/auth/profile', {
        method: 'PUT',
        body: JSON.stringify({ name: newName.trim() }),
      });
      setProfileSummary((prev) => ({
        ...prev,
        user: { ...prev.user, name: updatedUser.name },
      }));
      setIsEditingName(false);
    } catch (err) {
      alert(`Error updating profile: ${err.message}`);
    } finally {
      setSavingName(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const formattedDate = profileSummary?.user?.created_at
    ? new Date(profileSummary.user.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : user?.created_at
    ? new Date(user.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : 'Active Session';

  const certificateDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '860px', paddingBottom: '4rem' }}>
      {/* Header */}
      <div>
        <div className="badge badge-indigo" style={{ marginBottom: '0.75rem' }}>
          <User size={14} />
          <span>User Profile & Portfolio</span>
        </div>
        <h1 style={{ fontSize: '1.875rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
          Account & Learning Profile
        </h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          Manage your credentials, verify your active career track, review earned certifications, and showcase learning achievements.
        </p>
      </div>

      {loading ? (
        <LoadingState
          message="Loading Profile Information..."
          subtext="Retrieving candidate details, active career track, and credentials."
          variant="skeleton"
        />
      ) : error ? (
        <div role="alert" className="card" style={{ borderColor: 'var(--error)', textAlign: 'center', padding: '2rem' }}>
          <AlertCircle size={36} style={{ color: 'var(--error)', margin: '0 auto 0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Profile</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem', fontSize: '0.875rem' }}>{error}</p>
          <button onClick={fetchProfileSummary} className="btn btn-secondary">
            <RefreshCw size={15} /> Retry
          </button>
        </div>
      ) : (
        <>
          {/* User Information Card */}
          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
              <div
                style={{
                  width: '68px',
                  height: '68px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #6366f1 0%, #4338ca 100%)',
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.75rem',
                  fontWeight: 800,
                  boxShadow: '0 4px 14px rgba(99, 102, 241, 0.35)',
                }}
              >
                {profileSummary?.user?.name ? profileSummary.user.name.charAt(0).toUpperCase() : 'U'}
              </div>

              <div style={{ flex: 1, minWidth: 'min(200px, 100%)' }}>
                {isEditingName ? (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', flexWrap: 'wrap' }}>
                    <input
                      type="text"
                      value={newName}
                      onChange={(e) => setNewName(e.target.value)}
                      className="input-field"
                      style={{ maxWidth: '280px', width: '100%', padding: '0.4rem 0.75rem', fontSize: '1rem' }}
                      autoFocus
                    />
                    <button
                      onClick={handleSaveName}
                      disabled={savingName}
                      className="btn btn-primary"
                      style={{ padding: '0.4rem 0.75rem', fontSize: '0.8125rem' }}
                    >
                      {savingName ? <Loader2 size={14} className="animate-spin" /> : <Check size={14} />}
                      <span>Save</span>
                    </button>
                    <button
                      onClick={() => {
                        setIsEditingName(false);
                        setNewName(profileSummary?.user?.name || '');
                      }}
                      className="btn btn-secondary"
                      style={{ padding: '0.4rem 0.6rem' }}
                    >
                      <X size={14} />
                    </button>
                  </div>
                ) : (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem', flexWrap: 'wrap' }}>
                    <h2 style={{ fontSize: '1.375rem', fontWeight: 700 }}>
                      {profileSummary?.user?.name || user?.name || 'Candidate'}
                    </h2>
                    <button
                      onClick={() => setIsEditingName(true)}
                      className="btn btn-secondary"
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                      title="Edit Display Name"
                    >
                      <Edit2 size={12} />
                      <span>Edit</span>
                    </button>
                  </div>
                )}

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                  <Mail size={14} />
                  <span>{profileSummary?.user?.email || user?.email}</span>
                </div>
              </div>

              {/* Achievements Badge Counter */}
              <div
                style={{
                  padding: '0.75rem 1.25rem',
                  background: 'rgba(245, 158, 11, 0.08)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid rgba(245, 158, 11, 0.25)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                }}
              >
                <Trophy size={24} color="#f59e0b" />
                <div>
                  <div style={{ fontSize: '1.125rem', fontWeight: 800, color: '#f8fafc' }}>
                    {profileSummary?.achievements_count || 0} / {profileSummary?.total_achievements || 8}
                  </div>
                  <div style={{ fontSize: '0.6875rem', color: '#fbbf24', fontWeight: 600, textTransform: 'uppercase' }}>
                    Badges Unlocked
                  </div>
                </div>
              </div>
            </div>

            {/* Profile Meta Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(180px, 100%), 1fr))', gap: '1rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '1.25rem' }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.25rem', fontWeight: 600 }}>
                  Member Since
                </div>
                <div style={{ fontSize: '0.875rem', display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                  <Calendar size={14} color="var(--text-secondary)" />
                  <span>{formattedDate}</span>
                </div>
              </div>

              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.25rem', fontWeight: 600 }}>
                  Account Status
                </div>
                <span className="badge badge-success">
                  <ShieldCheck size={12} />
                  <span>Verified Candidate</span>
                </span>
              </div>

              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.25rem', fontWeight: 600 }}>
                  Readiness Evaluation
                </div>
                <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#818cf8' }}>
                  {profileSummary?.readiness_level || 'Evaluation Pending'}
                </div>
              </div>
            </div>
          </div>

          {/* Active Career Goal Overview */}
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Target size={18} color="var(--accent-primary)" />
                <span>Active Career Goal</span>
              </h3>
              <Link to="/goals" className="btn btn-secondary" style={{ fontSize: '0.75rem', padding: '0.35rem 0.75rem' }}>
                <span>Change Career Goal</span>
              </Link>
            </div>

            <div style={{ padding: '1.25rem', background: 'var(--bg-primary)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                <strong style={{ fontSize: '1.125rem', color: '#f8fafc' }}>
                  {profileSummary?.active_goal_title || 'No Goal Selected'}
                </strong>
                <span className="badge badge-indigo">
                  {profileSummary?.active_goal_category || 'Active Track'}
                </span>
              </div>

              {/* Progress Summary Stats Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.75rem', marginTop: '1rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--bg-card)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Skills Mastered</div>
                  <div style={{ fontSize: '1.125rem', fontWeight: 800, marginTop: '0.25rem' }}>
                    {profileSummary?.skills_completed} / {profileSummary?.total_skills}
                  </div>
                </div>

                <div style={{ padding: '0.75rem', background: 'var(--bg-card)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Topics Finished</div>
                  <div style={{ fontSize: '1.125rem', fontWeight: 800, marginTop: '0.25rem' }}>
                    {profileSummary?.topics_completed} / {profileSummary?.total_topics}
                  </div>
                </div>

                <div style={{ padding: '0.75rem', background: 'var(--bg-card)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Interview Qs</div>
                  <div style={{ fontSize: '1.125rem', fontWeight: 800, marginTop: '0.25rem' }}>
                    {profileSummary?.interview_practiced_count} / 15
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Action Buttons */}
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
              <Link to="/progress" className="btn btn-primary" style={{ fontSize: '0.8125rem' }}>
                <span>View Full Roadmap Progress</span>
                <ArrowRight size={14} />
              </Link>
              <button
                onClick={() => setShowCertificate(!showCertificate)}
                className="btn btn-secondary"
                style={{ fontSize: '0.8125rem', display: 'flex', alignItems: 'center', gap: '0.375rem' }}
              >
                <Award size={15} color="#10b981" />
                <span>{showCertificate ? 'Hide Certificate' : 'View Readiness Certificate'}</span>
              </button>
            </div>
          </div>

          {/* Digital Certificate of Readiness (Section 23 & Phase 12) */}
          {showCertificate && (
            <div
              className="card"
              style={{
                border: '2px solid rgba(16, 185, 129, 0.5)',
                background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 41, 59, 0.95) 100%)',
                padding: '2.5rem 2rem',
                textAlign: 'center',
                position: 'relative',
              }}
            >
              <div style={{ maxWidth: '640px', margin: '0 auto' }}>
                <Award size={54} color="#10b981" style={{ margin: '0 auto 1rem' }} />
                <div style={{ fontSize: '0.75rem', letterSpacing: '0.2em', textTransform: 'uppercase', color: '#10b981', fontWeight: 800, marginBottom: '0.5rem' }}>
                  CAREER EXPLORE STUDIO
                </div>
                <h2 style={{ fontSize: '1.75rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '1rem', color: '#f8fafc' }}>
                  Certificate of Career Readiness
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', marginBottom: '1.5rem', lineHeight: 1.6 }}>
                  This document officially certifies that
                </p>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#a5b4fc', textDecoration: 'underline', marginBottom: '1.5rem' }}>
                  {profileSummary?.user?.name || user?.name}
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', marginBottom: '1.5rem', lineHeight: 1.6 }}>
                  has completed comprehensive curriculum milestones, practical labs, diagnostic evaluations, and interview preparation for the career track:
                </p>
                <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f8fafc', marginBottom: '1.5rem' }}>
                  {profileSummary?.active_goal_title}
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-around', borderTop: '1px solid var(--border-subtle)', paddingTop: '1.25rem', marginTop: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
                  <div>
                    <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Verified Status</div>
                    <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#10b981' }}>Authenticated Candidate</div>
                  </div>
                  <div>
                    <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Issue Date</div>
                    <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc' }}>{certificateDate}</div>
                  </div>
                  <div>
                    <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Readiness Level</div>
                    <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#818cf8' }}>
                      {profileSummary?.readiness_level || 'Active Candidate'}
                    </div>
                  </div>
                </div>

                <div style={{ marginTop: '2rem' }}>
                  <button
                    onClick={() => window.print()}
                    className="btn btn-primary"
                    style={{ fontSize: '0.8125rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}
                  >
                    <Printer size={15} />
                    <span>Print / Save Certificate as PDF</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Account Security & Sign Out Card */}
          <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.25rem' }}>Account Session</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>
                Sign out of your active learning session on this device.
              </p>
            </div>

            <button
              onClick={handleLogout}
              className="btn btn-outline"
              style={{ color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.3)', fontSize: '0.8125rem' }}
            >
              <LogOut size={15} />
              <span>Sign Out</span>
            </button>
          </div>
        </>
      )}
    </div>
  );
}
