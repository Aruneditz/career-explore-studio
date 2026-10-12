import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Target, 
  Code, 
  Briefcase, 
  Megaphone, 
  Palette, 
  Terminal, 
  ClipboardList, 
  CheckCircle2, 
  ArrowRight, 
  Search, 
  Loader2, 
  AlertCircle, 
  Sparkles,
  Layers,
  Filter
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import api from '../../services/api';

const ICON_MAP = {
  Code,
  Briefcase,
  Megaphone,
  Palette,
  Terminal,
  ClipboardList,
  Target,
};

export default function GoalsPage() {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [goals, setGoals] = useState([]);
  const [selectedGoalId, setSelectedGoalId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');
  const [selectingId, setSelectingId] = useState(null);
  const [successToast, setSuccessToast] = useState('');

  const fetchGoalsAndCurrent = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch all available goals from database
      const goalsData = await api.request('/goals');
      setGoals(goalsData || []);

      // 2. If authenticated, fetch user's active goal
      if (isAuthenticated) {
        try {
          const currentSelection = await api.request('/goals/current');
          if (currentSelection && currentSelection.goal_id) {
            setSelectedGoalId(currentSelection.goal_id);
          }
        } catch (currentErr) {
          console.warn('Could not fetch active goal:', currentErr.message);
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to load career goals from server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGoalsAndCurrent();
  }, [isAuthenticated]);

  const handleSelectGoal = async (goal) => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: '/goals' } } });
      return;
    }

    setSelectingId(goal.id);
    try {
      await api.request('/goals/select', {
        method: 'POST',
        body: JSON.stringify({ goal_id: goal.id }),
      });
      setSelectedGoalId(goal.id);
      setSuccessToast(`Active goal set to "${goal.title}"!`);
      setTimeout(() => setSuccessToast(''), 4000);
    } catch (err) {
      alert(`Could not set active goal: ${err.message}`);
    } finally {
      setSelectingId(null);
    }
  };

  // Filter categories
  const categories = ['All', 'Technical', 'Business', 'Marketing', 'Design'];

  const filteredGoals = goals.filter((g) => {
    const matchesCategory = activeCategory === 'All' || g.category === activeCategory;
    const matchesSearch = 
      g.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      g.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      g.skills?.some(s => s.name.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header Banner */}
      <div>
        <div className="badge badge-indigo" style={{ marginBottom: '0.75rem' }}>
          <Target size={14} />
          <span>Step 1: Choose Your Career Direction</span>
        </div>
        <h1 style={{ fontSize: 'clamp(1.75rem, 3.5vw, 2.25rem)', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>
          Career & Skill Goals
        </h1>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '750px', fontSize: '1rem', lineHeight: 1.6 }}>
          Select a career track to generate your personalized learning journey. The studio supports both 
          <strong> technical engineering</strong> and <strong>non-technical business/creative</strong> careers.
        </p>
      </div>

      {/* Success Notification */}
      {successToast && (
        <div
          style={{
            background: 'var(--success-bg)',
            border: '1px solid rgba(16, 185, 129, 0.35)',
            padding: '1rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1rem',
            animation: 'fadeIn 200ms ease',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#34d399', fontWeight: 600, fontSize: '0.9375rem' }}>
            <CheckCircle2 size={20} />
            <span>{successToast}</span>
          </div>
          <button
            onClick={() => navigate('/skills')}
            className="btn btn-primary"
            style={{ padding: '0.4rem 0.875rem', minHeight: '34px', height: '34px', fontSize: '0.8125rem' }}
          >
            <span>Proceed to Skills</span>
            <ArrowRight size={14} />
          </button>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div
        className="card"
        style={{
          padding: '1.25rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
          background: 'var(--bg-secondary)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          {/* Category Tabs */}
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`btn ${activeCategory === cat ? 'btn-primary' : 'btn-outline'}`}
                style={{ padding: '0.4rem 0.85rem', minHeight: '34px', height: '34px', fontSize: '0.8125rem' }}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Search Input */}
          <div style={{ position: 'relative', width: 'min(320px, 100%)' }}>
            <Search
              size={16}
              style={{ position: 'absolute', left: '0.875rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}
            />
            <input
              type="text"
              placeholder="Search goals or skills..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem 0.875rem 0.5rem 2.375rem',
                background: 'var(--bg-primary)',
                border: '1px solid var(--border-medium)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--text-main)',
                fontSize: '0.875rem',
                outline: 'none',
              }}
            />
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <LoadingState 
          message="Loading career goals..." 
          subtext="Fetching data-driven engineering and non-technical career tracks from database."
          variant="skeleton"
        />
      )}

      {/* Error State */}
      {error && !loading && (
        <div role="alert" className="card" style={{ textAlign: 'center', padding: '2.5rem', borderLeft: '4px solid var(--danger)' }}>
          <AlertCircle size={36} style={{ color: 'var(--danger)', margin: '0 auto 0.75rem' }} />
          <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Goals</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>{error}</p>
          <button type="button" onClick={fetchGoalsAndCurrent} className="btn btn-primary">
            Retry Connection
          </button>
        </div>
      )}

      {/* Goals Cards Grid */}
      {!loading && !error && filteredGoals.length > 0 && (
        <div className="grid-2">
          {filteredGoals.map((goal) => {
            const Icon = ICON_MAP[goal.icon] || Target;
            const isSelected = selectedGoalId === goal.id;
            const isSelecting = selectingId === goal.id;

            return (
              <div
                key={goal.id}
                className="card card-interactive"
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  borderColor: isSelected ? 'var(--accent-primary)' : 'var(--border-subtle)',
                  background: isSelected 
                    ? 'linear-gradient(135deg, rgba(22, 31, 51, 0.98) 0%, rgba(99, 102, 241, 0.08) 100%)' 
                    : 'var(--bg-card)',
                  boxShadow: isSelected ? '0 0 20px -2px rgba(99, 102, 241, 0.35)' : 'var(--shadow-md)',
                }}
              >
                {/* Card Header */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                  <div
                    style={{
                      width: '46px',
                      height: '46px',
                      borderRadius: '12px',
                      background: isSelected ? 'var(--accent-primary)' : 'var(--accent-light)',
                      color: isSelected ? '#ffffff' : '#a5b4fc',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: isSelected ? '0 4px 12px rgba(99, 102, 241, 0.4)' : 'none',
                    }}
                  >
                    <Icon size={24} />
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span className="badge badge-indigo">{goal.category}</span>
                    {isSelected && (
                      <span className="badge badge-success">
                        <CheckCircle2 size={12} />
                        <span>Active Goal</span>
                      </span>
                    )}
                  </div>
                </div>

                {/* Title & Description */}
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem', color: isSelected ? '#ffffff' : 'var(--text-main)' }}>
                  {goal.title}
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.55, marginBottom: '1.25rem' }}>
                  {goal.description}
                </p>

                {/* Career Relevance */}
                <div
                  style={{
                    background: 'var(--bg-primary)',
                    padding: '0.875rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-subtle)',
                    marginBottom: '1.25rem',
                  }}
                >
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#818cf8', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
                    Industry Relevance
                  </div>
                  <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                    {goal.career_relevance}
                  </p>
                </div>

                {/* Skills Preview */}
                <div style={{ flex: 1, marginBottom: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      Roadmap Skills ({goal.skills?.length || 0})
                    </span>
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
                    {goal.skills?.map((s) => (
                      <span
                        key={s.id}
                        style={{
                          fontSize: '0.75rem',
                          background: 'var(--bg-secondary)',
                          border: '1px solid var(--border-subtle)',
                          padding: '0.2rem 0.55rem',
                          borderRadius: 'var(--radius-sm)',
                          color: s.is_technical ? '#93c5fd' : '#86efac',
                        }}
                      >
                        {s.name}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Card Action Buttons */}
                <div style={{ paddingTop: '1.25rem', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
                  {isSelected ? (
                    <>
                      <span style={{ fontSize: '0.8125rem', color: '#10b981', display: 'flex', alignItems: 'center', gap: '0.35rem', fontWeight: 600 }}>
                        <CheckCircle2 size={16} /> Selected as Active Goal
                      </span>
                      <button
                        onClick={() => navigate('/skills')}
                        className="btn btn-primary"
                        style={{ padding: '0.5rem 1rem', fontSize: '0.8125rem' }}
                      >
                        <span>Start Learning Skills</span>
                        <ArrowRight size={14} />
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => handleSelectGoal(goal)}
                      disabled={isSelecting}
                      className="btn btn-secondary"
                      style={{ width: '100%', fontSize: '0.875rem' }}
                    >
                      {isSelecting ? (
                        <>
                          <Loader2 size={16} className="status-dot loading" />
                          <span>Setting Active Goal...</span>
                        </>
                      ) : (
                        <>
                          <Target size={16} />
                          <span>Select This Career Goal</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && filteredGoals.length === 0 && (
        <EmptyState
          icon={Target}
          title="No Goals Match Your Search"
          description="Try adjusting your search query keywords or switching between Technical, Business, Marketing, and Design categories."
          actionLabel="Clear Search & Reset Filters"
          onAction={() => { setSearchQuery(''); setActiveCategory('All'); }}
        />
      )}
    </div>
  );
}
