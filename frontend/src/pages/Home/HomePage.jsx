import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Compass, 
  Terminal, 
  Database, 
  Layers, 
  CheckCircle2, 
  RefreshCw, 
  Sparkles, 
  BookOpen, 
  Award,
  User,
  ShieldCheck,
  LogIn,
  UserPlus,
  Target,
  TrendingUp,
  HelpCircle,
  ArrowRight,
  ListChecks
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import AISearchAssistant from '../../components/AI/AISearchAssistant';

export default function HomePage({ backendHealth, onRefreshHealth, healthLoading }) {
  const { user, isAuthenticated } = useAuth();
  const [testResult, setTestResult] = useState(null);
  const [pinging, setPinging] = useState(false);

  const handleTestPing = async () => {
    setPinging(true);
    try {
      const res = await api.checkHealth();
      setTestResult({
        success: true,
        data: res,
        time: new Date().toLocaleTimeString(),
      });
    } catch (err) {
      setTestResult({
        success: false,
        error: err.message,
        time: new Date().toLocaleTimeString(),
      });
    } finally {
      setPinging(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Hero Section */}
      <section
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(30, 41, 66, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%)',
          border: '1px solid var(--border-medium)',
          padding: '2.5rem 2rem',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <div style={{ maxWidth: '820px' }}>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
            <div className="badge badge-success">
              <CheckCircle2 size={14} />
              <span>Full-Stack Platform Active</span>
            </div>
            <div className="badge badge-indigo">
              <Sparkles size={14} />
              <span>AI Guidance & Certified Mastery</span>
            </div>
          </div>

          <h1
            style={{
              fontSize: 'clamp(1.75rem, 4vw, 2.75rem)',
              fontWeight: 800,
              lineHeight: 1.15,
              letterSpacing: '-0.03em',
              marginBottom: '1rem',
              color: '#ffffff',
            }}
          >
            {isAuthenticated ? `Welcome back, ${user.name}!` : 'CAREER EXPLORE STUDIO'}
          </h1>

          <p
            style={{
              fontSize: 'clamp(1rem, 2vw, 1.1875rem)',
              color: 'var(--text-secondary)',
              lineHeight: 1.6,
              marginBottom: '1.75rem',
            }}
          >
            A personal skill learning, roadmap, and interview preparation platform supporting both 
            <strong> technical engineering</strong> and <strong>non-technical business/creative</strong> careers.
          </p>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'center' }}>
            {isAuthenticated ? (
              <>
                <Link to="/skills" className="btn btn-primary">
                  <BookOpen size={16} />
                  <span>Start Learning Skills</span>
                </Link>
                <Link to="/goals" className="btn btn-secondary">
                  <Target size={16} />
                  <span>Explore Goals</span>
                </Link>
              </>
            ) : (
              <>
                <Link to="/register" className="btn btn-primary">
                  <UserPlus size={16} />
                  <span>Create Account</span>
                </Link>
                <Link to="/login" className="btn btn-secondary">
                  <LogIn size={16} />
                  <span>Sign In</span>
                </Link>
              </>
            )}

            <button
              className="btn btn-outline"
              onClick={handleTestPing}
              disabled={pinging}
            >
              <RefreshCw size={16} className={pinging ? 'status-dot loading' : ''} />
              <span>{pinging ? 'Pinging API...' : 'Ping API'}</span>
            </button>
          </div>
        </div>
      </section>

      {/* AI Assistant Search Bar Section (Upgrade #6) */}
      <section aria-label="Career AI Assistant">
        <AISearchAssistant
          title="Career Explore Studio AI Mentor"
        />
      </section>

      {/* Navigation Modules Grid */}
      <section>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Layers size={18} color="var(--accent-primary)" />
          <span>Active Learning Modules</span>
        </h2>

        <div className="grid-3">
          <Link to="/goals" className="card card-interactive" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: 'var(--accent-light)', color: '#818cf8', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Target size={20} />
              </div>
              <ArrowRight size={16} color="var(--text-muted)" />
            </div>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.375rem' }}>Goal Selection</h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
              Choose your career track from 6 diverse technical and business goals.
            </p>
          </Link>

          <Link to="/skills" className="card card-interactive" style={{ textDecoration: 'none', color: 'inherit', borderColor: 'var(--accent-primary)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: 'rgba(16, 185, 129, 0.15)', color: '#10b981', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <BookOpen size={20} />
              </div>
              <span className="badge badge-success" style={{ fontSize: '0.6875rem' }}>Phase 5 Live</span>
            </div>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.375rem' }}>Skills & Topics</h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
              Step-by-step skill selection, detailed 7-point overview, and complete topic lists.
            </p>
          </Link>

          <Link to="/progress" className="card card-interactive" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <TrendingUp size={20} />
              </div>
              <ArrowRight size={16} color="var(--text-muted)" />
            </div>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.375rem' }}>Progress</h3>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
              Live topic completion percentages and milestone tracking.
            </p>
          </Link>
        </div>
      </section>

      {/* Roadmap Progress Status */}
      <section className="card">
        <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <CheckCircle2 size={18} color="var(--success)" />
          <span>Implementation Plan Roadmap Status</span>
        </h2>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
          {[
            { phase: 'Phase 1', title: 'Project Setup & Unified App Shell', status: 'Complete' },
            { phase: 'Phase 2', title: 'Streamlined Intro Flow & Core Authentication', status: 'Complete' },
            { phase: 'Phase 3', title: 'CES Brand Identity & Unified Logo System', status: 'Complete' },
            { phase: 'Phase 4', title: '4-Part Interview Questions with Syntax & Practical Copy', status: 'Complete' },
            { phase: 'Phase 5', title: '4-Stage Skill Completion & Certificate Generation', status: 'Complete' },
            { phase: 'Phase 6', title: 'CES AI Search Assistant & Instant Guidance Modal', status: 'Complete' },
            { phase: 'Phase 7', title: 'User-Specific Database Architecture & Constraints', status: 'Complete' },
            { phase: 'Phase 8', title: 'FastAPI AI Backend Service & Gemini Integration', status: 'Complete' },
            { phase: 'Phase 9', title: 'Personalized AI Learning Context & SQLite Grounding', status: 'Complete' },
            { phase: 'Phase 10', title: 'Database Integrity Audit & Multi-User Isolation', status: 'Complete' },
            { phase: 'Phase 11', title: 'Complete Responsive UI Improvement across All Pages', status: 'Complete' },
            { phase: 'Phase 12', title: 'Performance Optimization, Loading/Error States & A11y', status: 'Complete' },
            { phase: 'Phase 13', title: 'Complete Integration Testing & Full-Stack Regressions', status: 'Complete' },
            { phase: 'Phase 14', title: 'Final Production-Quality Review & Build Verification', status: 'Production Ready' },
          ].map((item, idx) => (
            <div
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.75rem 1rem',
                background: item.status.includes('Active')
                  ? 'rgba(99, 102, 241, 0.12)'
                  : 'rgba(16, 185, 129, 0.08)',
                border: item.status.includes('Active')
                  ? '1px solid rgba(99, 102, 241, 0.35)'
                  : '1px solid rgba(16, 185, 129, 0.25)',
                borderRadius: 'var(--radius-md)',
                flexWrap: 'wrap',
                gap: '0.5rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
                <span className={`status-dot ${item.status.includes('Active') ? 'loading' : 'active'}`}></span>
                <strong style={{ fontSize: '0.875rem' }}>{item.phase}: {item.title}</strong>
              </div>
              <span className={`badge ${item.status.includes('Active') ? 'badge-indigo' : 'badge-success'}`}>
                {item.status}
              </span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
