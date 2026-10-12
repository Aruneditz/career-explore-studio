import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  HelpCircle,
  Award,
  CheckCircle2,
  Check,
  Search,
  Filter,
  Eye,
  EyeOff,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  Lightbulb,
  Sparkles,
  BookOpen,
  ArrowRight,
  Loader2,
  AlertCircle,
  Copy,
  Layers,
  Compass,
  Briefcase,
  Target,
  RefreshCw,
  FolderCheck,
  Code2
} from 'lucide-react';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

export default function InterviewPrepPage() {
  const { user, isAuthenticated } = useAuth();

  const [hubData, setHubData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters & Search
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');
  const [filterPracticed, setFilterPracticed] = useState('all'); // 'all', 'practiced', 'unpracticed'

  // Card UI States
  const [expandedCards, setExpandedCards] = useState({});
  const [revealedAnswers, setRevealedAnswers] = useState({});
  const [copiedCodeId, setCopiedCodeId] = useState(null);
  const [updatingQuestionId, setUpdatingQuestionId] = useState(null);

  // Fetch Capstone Interview Hub Data
  const fetchHubData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.request('/interview-prep/hub');
      setHubData(data);

      // Initialize all cards expanded and answers revealed by default
      const initialExpanded = {};
      const initialRevealed = {};
      if (data && data.questions) {
        data.questions.forEach((q) => {
          initialExpanded[q.id] = true;
          initialRevealed[q.id] = true;
        });
      }
      setExpandedCards(initialExpanded);
      setRevealedAnswers(initialRevealed);
    } catch (err) {
      console.error('Failed to load final interview questions:', err);
      setError(err.message || 'Failed to load capstone interview preparation data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHubData();
  }, []);

  // Toggle Practice Status
  const handleTogglePracticed = async (questionId, currentPracticed) => {
    if (updatingQuestionId) return;
    setUpdatingQuestionId(questionId);

    const nextState = !currentPracticed;
    try {
      const res = await api.request('/interview-prep/toggle-practiced', {
        method: 'POST',
        body: JSON.stringify({
          question_id: questionId,
          is_practiced: nextState,
        }),
      });

      // Update local state
      setHubData((prev) => {
        if (!prev) return prev;
        const updatedQuestions = prev.questions.map((q) => {
          if (q.id === questionId) {
            return {
              ...q,
              is_practiced: res.is_practiced,
              practiced_at: res.practiced_at,
            };
          }
          return q;
        });

        const newPracticedCount = updatedQuestions.filter((q) => q.is_practiced).length;
        const newPercentage = Math.round((newPracticedCount / prev.total_questions) * 1000) / 10;

        return {
          ...prev,
          practiced_count: newPracticedCount,
          practiced_percentage: newPercentage,
          questions: updatedQuestions,
        };
      });
    } catch (err) {
      alert(`Error updating practice status: ${err.message}`);
    } finally {
      setUpdatingQuestionId(null);
    }
  };

  // Toggle Card Accordion
  const toggleCard = (questionId) => {
    setExpandedCards((prev) => ({
      ...prev,
      [questionId]: !prev[questionId],
    }));
  };

  // Toggle Answer Visibility
  const toggleAnswer = (questionId) => {
    setRevealedAnswers((prev) => ({
      ...prev,
      [questionId]: !prev[questionId],
    }));
  };

  // Global Expand / Collapse All
  const handleExpandAll = (expand) => {
    if (!hubData?.questions) return;
    const updated = {};
    hubData.questions.forEach((q) => {
      updated[q.id] = expand;
    });
    setExpandedCards(updated);
  };

  // Global Reveal / Hide All Answers
  const handleRevealAll = (reveal) => {
    if (!hubData?.questions) return;
    const updated = {};
    hubData.questions.forEach((q) => {
      updated[q.id] = reveal;
    });
    setRevealedAnswers(updated);
  };

  // Copy Code snippet helper
  const handleCopyCode = (text, id) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopiedCodeId(id);
    setTimeout(() => setCopiedCodeId(null), 2000);
  };

  // Category Badge Styler
  const getCategoryBadgeClass = (category) => {
    if (category.includes('Core')) return 'badge-indigo';
    if (category.includes('Practical') || category.includes('Scenario')) return 'badge-warning';
    return 'badge-purple';
  };

  // Filter questions
  const filteredQuestions = (hubData?.questions || []).filter((q) => {
    // Category filter
    if (activeCategory !== 'All' && q.category !== activeCategory) {
      return false;
    }

    // Practice status filter
    if (filterPracticed === 'practiced' && !q.is_practiced) return false;
    if (filterPracticed === 'unpracticed' && q.is_practiced) return false;

    // Search query filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      const matchQuestion = q.question.toLowerCase().includes(query);
      const matchCategory = q.category.toLowerCase().includes(query);
      const matchAnswer = q.detailed_answer.toLowerCase().includes(query);
      const matchLookingFor = q.interviewer_looking_for.toLowerCase().includes(query);
      return matchQuestion || matchCategory || matchAnswer || matchLookingFor;
    }

    return true;
  });

  // Calculate category counts
  const categoryCounts = {
    All: hubData?.questions?.length || 0,
    'Core Fundamentals': (hubData?.questions || []).filter((q) => q.category === 'Core Fundamentals').length,
    'Practical & Scenario-Based': (hubData?.questions || []).filter((q) => q.category === 'Practical & Scenario-Based').length,
    'Advanced & Problem Solving': (hubData?.questions || []).filter((q) => q.category === 'Advanced & Problem Solving').length,
  };

  if (loading) {
    return (
      <LoadingState 
        message="Loading Capstone Interview Questions..." 
        subtext="Retrieving the exactly 15 must-know interview questions for your career path."
        variant="skeleton"
      />
    );
  }

  if (error) {
    return (
      <div role="alert" className="card" style={{ maxWidth: '640px', margin: '2rem auto', textAlign: 'center', borderColor: 'var(--error)' }}>
        <AlertCircle size={44} style={{ color: 'var(--error)', margin: '0 auto 1rem' }} />
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>Failed to Load Interview Preparation</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.875rem' }}>{error}</p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button type="button" onClick={fetchHubData} className="btn btn-primary">
            <RefreshCw size={16} /> Retry
          </button>
          <Link to="/goals" className="btn btn-secondary">
            Change Selected Goal
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', paddingBottom: '4rem' }}>
      {/* Top Banner & Header */}
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
          <div style={{ maxWidth: '720px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.75rem' }}>
              <div className="badge badge-indigo" style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <Award size={14} />
                <span>Capstone Final Interview Hub</span>
              </div>
              <div className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                <Target size={14} />
                <span>Exactly 15 Must-Know Questions</span>
              </div>
            </div>

            <h1 style={{ fontSize: '2rem', fontWeight: 800, letterSpacing: '-0.025em', marginBottom: '0.5rem', color: '#f8fafc' }}>
              {hubData?.goal_title || 'Career Goal'} Interview Preparation
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', lineHeight: 1.6 }}>
              Comprehensive, high-impact interview preparation curated specifically for <strong>{hubData?.goal_title}</strong>. 
              Master the exact 15 questions interviewers ask: from core fundamentals and live scenarios to architectural decisions, 
              complete with model answers, practical code, STAR frameworks, and disqualifying traps to avoid.
            </p>
          </div>

          {/* Quick Actions / Link to Overall Evaluation */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', minWidth: '220px' }}>
            <Link
              to="/overall-evaluation"
              className="btn btn-secondary"
              style={{ fontSize: '0.8125rem', justifyContent: 'center' }}
            >
              <FolderCheck size={16} /> Review Overall Evaluation
            </Link>
            <Link
              to="/skills"
              className="btn btn-secondary"
              style={{ fontSize: '0.8125rem', justifyContent: 'center' }}
            >
              <Briefcase size={16} /> Explore Goal Skills
            </Link>
          </div>
        </div>

        {/* Practice Progress Bar Widget */}
        <div
          style={{
            marginTop: '1.75rem',
            padding: '1.25rem 1.5rem',
            background: 'rgba(15, 23, 42, 0.75)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.625rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <CheckCircle2 size={18} color="#10b981" />
              <span style={{ fontWeight: 600, fontSize: '0.9375rem', color: '#f8fafc' }}>
                Practice Progress:
              </span>
              <span style={{ fontWeight: 700, color: 'var(--accent-primary)', fontSize: '1rem' }}>
                {hubData?.practiced_count || 0} / {hubData?.total_questions || 15} Practiced
              </span>
            </div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
              {hubData?.practiced_percentage || 0}% Completed
            </div>
          </div>

          <div
            style={{
              height: '10px',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '999px',
              overflow: 'hidden',
              position: 'relative',
            }}
          >
            <div
              style={{
                height: '100%',
                width: `${Math.min(hubData?.practiced_percentage || 0, 100)}%`,
                background: 'linear-gradient(90deg, #6366f1 0%, #10b981 100%)',
                borderRadius: '999px',
                transition: 'width 0.4s ease-in-out',
              }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-tertiary)', flexWrap: 'wrap', gap: '0.35rem' }}>
            <span>Questions 1–5: Core Fundamentals</span>
            <span>Questions 6–10: Practical & Scenarios</span>
            <span>Questions 11–15: Advanced & Problem Solving</span>
          </div>
        </div>
      </div>

      {/* Control Bar: Filters, Search & Global Toggles */}
      <div
        className="card"
        style={{
          padding: '1.25rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
          background: 'var(--bg-card)',
        }}
      >
        {/* Top Row: Search & Status Filter */}
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
          {/* Search Input */}
          <div style={{ position: 'relative', flex: '1 1 320px', minWidth: '240px' }}>
            <Search
              size={18}
              style={{
                position: 'absolute',
                left: '0.875rem',
                top: '50%',
                transform: 'translateY(-50%)',
                color: 'var(--text-tertiary)',
              }}
            />
            <input
              type="text"
              placeholder="Search interview questions, keywords, model answers..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-field"
              style={{ paddingLeft: '2.5rem', width: '100%' }}
            />
          </div>

          {/* Practiced Filter Dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>Status:</span>
            <select
              value={filterPracticed}
              onChange={(e) => setFilterPracticed(e.target.value)}
              className="input-field"
              style={{ width: 'auto', padding: '0.45rem 1.75rem 0.45rem 0.75rem', fontSize: '0.8125rem' }}
            >
              <option value="all">All Statuses</option>
              <option value="practiced">Practiced Only</option>
              <option value="unpracticed">Unpracticed Only</option>
            </select>
          </div>

          {/* Global Toggle Buttons */}
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              onClick={() => handleExpandAll(true)}
              className="btn btn-secondary"
              style={{ padding: '0.45rem 0.75rem', fontSize: '0.75rem' }}
              title="Expand All Accordions"
            >
              Expand All
            </button>
            <button
              onClick={() => handleExpandAll(false)}
              className="btn btn-secondary"
              style={{ padding: '0.45rem 0.75rem', fontSize: '0.75rem' }}
              title="Collapse All Accordions"
            >
              Collapse All
            </button>
            <button
              onClick={() => handleRevealAll(true)}
              className="btn btn-secondary"
              style={{ padding: '0.45rem 0.75rem', fontSize: '0.75rem', color: '#10b981' }}
              title="Reveal All Answers"
            >
              <Eye size={14} /> Reveal Answers
            </button>
            <button
              onClick={() => handleRevealAll(false)}
              className="btn btn-secondary"
              style={{ padding: '0.45rem 0.75rem', fontSize: '0.75rem', color: '#f59e0b' }}
              title="Hide All Answers to Self-Test"
            >
              <EyeOff size={14} /> Hide Answers
            </button>
          </div>
        </div>

        {/* Bottom Row: Category Tabs */}
        <div
          style={{
            display: 'flex',
            gap: '0.5rem',
            flexWrap: 'wrap',
            borderTop: '1px solid var(--border-subtle)',
            paddingTop: '0.875rem',
          }}
        >
          {[
            { id: 'All', label: 'All Questions', count: categoryCounts['All'] },
            { id: 'Core Fundamentals', label: '1–5 Core Fundamentals', count: categoryCounts['Core Fundamentals'] },
            { id: 'Practical & Scenario-Based', label: '6–10 Practical & Scenarios', count: categoryCounts['Practical & Scenario-Based'] },
            { id: 'Advanced & Problem Solving', label: '11–15 Advanced & Problem Solving', count: categoryCounts['Advanced & Problem Solving'] },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveCategory(tab.id)}
              className={`btn ${activeCategory === tab.id ? 'btn-primary' : 'btn-secondary'}`}
              style={{
                padding: '0.4rem 0.85rem',
                fontSize: '0.8125rem',
                borderRadius: 'var(--radius-sm)',
              }}
            >
              <span>{tab.label}</span>
              <span
                style={{
                  background: activeCategory === tab.id ? 'rgba(255, 255, 255, 0.25)' : 'rgba(255, 255, 255, 0.08)',
                  padding: '0.1rem 0.45rem',
                  borderRadius: '999px',
                  fontSize: '0.6875rem',
                  fontWeight: 700,
                  marginLeft: '0.375rem',
                }}
              >
                {tab.count}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Results Header Count */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Showing <strong>{filteredQuestions.length}</strong> of {hubData?.total_questions || 15} interview questions
          {searchQuery && <span> matching "<em>{searchQuery}</em>"</span>}
        </p>
      </div>

      {/* Questions List */}
      {filteredQuestions.length === 0 ? (
        <EmptyState
          icon={Search}
          title="No Questions Match Your Filter"
          description="Try adjusting your search keywords, switching categories, or clearing status filters."
          actionLabel="Reset Search & Filters"
          onAction={() => {
            setSearchQuery('');
            setActiveCategory('All');
            setFilterPracticed('all');
          }}
        />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {filteredQuestions.map((q) => {
            const isExpanded = expandedCards[q.id] ?? true;
            const isAnswerRevealed = revealedAnswers[q.id] ?? true;
            const categoryBadgeClass = getCategoryBadgeClass(q.category);

            return (
              <div
                key={q.id}
                className="card"
                style={{
                  padding: '0',
                  overflow: 'hidden',
                  border: q.is_practiced ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid var(--border-color)',
                  boxShadow: q.is_practiced ? '0 0 15px rgba(16, 185, 129, 0.05)' : 'none',
                  transition: 'border-color 0.2s ease',
                }}
              >
                {/* Question Header Bar */}
                <div
                  style={{
                    padding: '1.25rem 1.5rem',
                    background: q.is_practiced
                      ? 'linear-gradient(180deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0) 100%)'
                      : 'var(--bg-card)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.75rem',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem', flexWrap: 'wrap' }}>
                    {/* Badges: Question Number & Category */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', flexWrap: 'wrap' }}>
                      <span
                        style={{
                          background: 'var(--accent-primary)',
                          color: '#fff',
                          fontWeight: 800,
                          fontSize: '0.75rem',
                          padding: '0.2rem 0.55rem',
                          borderRadius: '6px',
                          letterSpacing: '0.05em',
                        }}
                      >
                        Q{q.question_number}
                      </span>
                      <span className={`badge ${categoryBadgeClass}`} style={{ fontSize: '0.75rem' }}>
                        {q.category}
                      </span>
                      {q.is_practiced && (
                        <span className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                          <Check size={12} /> Practiced
                        </span>
                      )}
                    </div>

                    {/* Actions: Mark as Practiced & Reveal Answer */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      {/* Mark as Practiced Button */}
                      <button
                        onClick={() => handleTogglePracticed(q.id, q.is_practiced)}
                        disabled={updatingQuestionId === q.id}
                        className={`btn ${q.is_practiced ? 'btn-success' : 'btn-secondary'}`}
                        style={{
                          padding: '0.35rem 0.75rem',
                          fontSize: '0.75rem',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.375rem',
                        }}
                      >
                        {updatingQuestionId === q.id ? (
                          <Loader2 size={13} className="animate-spin" />
                        ) : q.is_practiced ? (
                          <CheckCircle2 size={14} color="#fff" />
                        ) : (
                          <Check size={14} />
                        )}
                        <span>{q.is_practiced ? 'Practiced ✓' : 'Mark as Practiced'}</span>
                      </button>

                      {/* Reveal Answer Toggle */}
                      <button
                        onClick={() => toggleAnswer(q.id)}
                        className="btn btn-secondary"
                        style={{
                          padding: '0.35rem 0.65rem',
                          fontSize: '0.75rem',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.35rem',
                        }}
                        title={isAnswerRevealed ? 'Hide Answer to test yourself' : 'Reveal Model Answer'}
                      >
                        {isAnswerRevealed ? <EyeOff size={14} /> : <Eye size={14} />}
                        <span>{isAnswerRevealed ? 'Hide Answer' : 'Reveal Answer'}</span>
                      </button>

                      {/* Accordion Expand/Collapse */}
                      <button
                        onClick={() => toggleCard(q.id)}
                        className="btn btn-secondary"
                        style={{ padding: '0.35rem', borderRadius: '6px' }}
                        aria-label="Toggle Question Details"
                      >
                        {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </button>
                    </div>
                  </div>

                  {/* Question Title */}
                  <h3
                    onClick={() => toggleCard(q.id)}
                    style={{
                      fontSize: '1.125rem',
                      fontWeight: 700,
                      color: '#f8fafc',
                      lineHeight: 1.45,
                      cursor: 'pointer',
                    }}
                  >
                    {q.question}
                  </h3>
                </div>

                {/* Collapsible Content Body */}
                {isExpanded && (
                  <div
                    style={{
                      padding: '1.5rem',
                      borderTop: '1px solid var(--border-subtle)',
                      background: 'var(--bg-primary)',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '1.25rem',
                    }}
                  >
                    {/* Section 1: Why Interviewers Ask This */}
                    <div
                      style={{
                        padding: '1rem',
                        background: 'rgba(99, 102, 241, 0.08)',
                        borderRadius: 'var(--radius-sm)',
                        borderLeft: '4px solid #6366f1',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
                        <Compass size={16} color="#818cf8" />
                        <h4 style={{ fontSize: '0.8125rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#818cf8' }}>
                          Why Interviewers Ask This
                        </h4>
                      </div>
                      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                        {q.why_asked}
                      </p>
                    </div>

                    {/* Section 2: What the Interviewer is Looking For */}
                    <div
                      style={{
                        padding: '1rem',
                        background: 'rgba(16, 185, 129, 0.08)',
                        borderRadius: 'var(--radius-sm)',
                        borderLeft: '4px solid #10b981',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
                        <Target size={16} color="#34d399" />
                        <h4 style={{ fontSize: '0.8125rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#34d399' }}>
                          What Interviewers Look For
                        </h4>
                      </div>
                      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                        {q.interviewer_looking_for}
                      </p>
                    </div>

                    {/* Section 3: Hidden Answer Self-Test Mode vs Model Answer */}
                    {!isAnswerRevealed ? (
                      <div
                        style={{
                          padding: '2rem',
                          textAlign: 'center',
                          background: 'rgba(255, 255, 255, 0.02)',
                          border: '1px dashed var(--border-color)',
                          borderRadius: 'var(--radius-md)',
                        }}
                      >
                        <Lightbulb size={32} style={{ color: '#f59e0b', margin: '0 auto 0.75rem' }} />
                        <h4 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.375rem' }}>
                          Answer Hidden for Self-Testing
                        </h4>
                        <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', maxWidth: '480px', margin: '0 auto 1.25rem' }}>
                          Try explaining your answer aloud or note down key points on paper first. Then reveal the model answer to compare!
                        </p>
                        <button
                          onClick={() => toggleAnswer(q.id)}
                          className="btn btn-primary"
                          style={{ fontSize: '0.8125rem' }}
                        >
                          <Eye size={15} /> Reveal Detailed Model Answer
                        </button>
                      </div>
                    ) : (
                      <>
                        {/* Section 4: Detailed Model Answer */}
                        <div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                            <BookOpen size={16} color="var(--accent-primary)" />
                            <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc' }}>
                              Detailed Model Answer
                            </h4>
                          </div>
                          <div
                            style={{
                              fontSize: '0.875rem',
                              color: 'var(--text-secondary)',
                              lineHeight: 1.7,
                              whiteSpace: 'pre-line',
                              background: 'var(--bg-card)',
                              padding: '1.25rem',
                              borderRadius: 'var(--radius-sm)',
                              border: '1px solid var(--border-subtle)',
                            }}
                          >
                            {q.detailed_answer}
                          </div>
                        </div>

                        {/* Simple Syntax / Framework Structure (when provided) */}
                        {q.simple_syntax && (
                          <div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                              <Code2 size={16} color="#818cf8" />
                              <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc' }}>
                                Simple Syntax / Pattern Structure
                              </h4>
                            </div>
                            <pre
                              style={{
                                background: '#0d1117',
                                color: '#79c0ff',
                                padding: '1rem 1.25rem',
                                borderRadius: 'var(--radius-sm)',
                                border: '1px solid #30363d',
                                overflowX: 'auto',
                                fontSize: '0.8125rem',
                                lineHeight: 1.6,
                                fontFamily: 'Consolas, Monaco, "Courier New", Courier, monospace',
                                whiteSpace: 'pre-wrap',
                              }}
                            >
                              <code>{q.simple_syntax}</code>
                            </pre>
                          </div>
                        )}

                        {/* Small Practical Example (when provided) */}
                        {q.small_example && (
                          <div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <Sparkles size={16} color="#38bdf8" />
                                <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc' }}>
                                  Small Practical Example
                                </h4>
                              </div>
                              <button
                                onClick={() => handleCopyCode(q.small_example, `small-${q.id}`)}
                                className="btn btn-secondary"
                                style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}
                              >
                                {copiedCodeId === `small-${q.id}` ? <Check size={12} color="#10b981" /> : <Copy size={12} />}
                                <span>{copiedCodeId === `small-${q.id}` ? 'Copied!' : 'Copy Code'}</span>
                              </button>
                            </div>
                            <pre
                              style={{
                                background: '#090d16',
                                color: '#e2e8f0',
                                padding: '1.25rem',
                                borderRadius: 'var(--radius-sm)',
                                border: '1px solid rgba(56, 189, 248, 0.25)',
                                overflowX: 'auto',
                                fontSize: '0.8125rem',
                                lineHeight: 1.6,
                                fontFamily: 'Consolas, Monaco, "Courier New", Courier, monospace',
                                whiteSpace: 'pre-wrap',
                              }}
                            >
                              <code>{q.small_example}</code>
                            </pre>
                          </div>
                        )}

                        {/* Section 5: Code Example OR Practical Example */}
                        {q.code_or_practical_example && (
                          <div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <Sparkles size={16} color="#a5b4fc" />
                                <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc' }}>
                                  Practical Code / Operational Example
                                </h4>
                              </div>
                              <button
                                onClick={() => handleCopyCode(q.code_or_practical_example, q.id)}
                                className="btn btn-secondary"
                                style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}
                              >
                                {copiedCodeId === q.id ? <Check size={12} color="#10b981" /> : <Copy size={12} />}
                                <span>{copiedCodeId === q.id ? 'Copied!' : 'Copy Code'}</span>
                              </button>
                            </div>
                            <pre
                              style={{
                                background: '#0b0f19',
                                color: '#e2e8f0',
                                padding: '1.25rem',
                                borderRadius: 'var(--radius-sm)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                overflowX: 'auto',
                                fontSize: '0.8125rem',
                                lineHeight: 1.6,
                                fontFamily: 'Consolas, Monaco, "Courier New", Courier, monospace',
                              }}
                            >
                              <code>{q.code_or_practical_example}</code>
                            </pre>
                          </div>
                        )}

                        {/* Section 6: Scenario / Edge Case Example */}
                        {q.scenario_example && (
                          <div
                            style={{
                              padding: '1rem',
                              background: 'rgba(245, 158, 11, 0.08)',
                              borderRadius: 'var(--radius-sm)',
                              borderLeft: '4px solid #f59e0b',
                            }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
                              <AlertCircle size={16} color="#fbbf24" />
                              <h4 style={{ fontSize: '0.8125rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#fbbf24' }}>
                                Realistic Scenario & Edge Case
                              </h4>
                            </div>
                            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                              {q.scenario_example}
                            </p>
                          </div>
                        )}

                        {/* Section 7: How to Structure Your Response (STAR Method) */}
                        <div
                          style={{
                            padding: '1rem',
                            background: 'rgba(168, 85, 247, 0.08)',
                            borderRadius: 'var(--radius-sm)',
                            borderLeft: '4px solid #a855f7',
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
                            <Layers size={16} color="#c084fc" />
                            <h4 style={{ fontSize: '0.8125rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#c084fc' }}>
                              How to Structure Your Response (STAR Framework)
                            </h4>
                          </div>
                          <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6, whiteSpace: 'pre-line' }}>
                            {q.response_structure_star}
                          </div>
                        </div>

                        {/* Section 8: What NOT to Say (Traps & Red Flags) */}
                        <div
                          style={{
                            padding: '1rem',
                            background: 'rgba(239, 68, 68, 0.08)',
                            borderRadius: 'var(--radius-sm)',
                            borderLeft: '4px solid #ef4444',
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
                            <AlertTriangle size={16} color="#f87171" />
                            <h4 style={{ fontSize: '0.8125rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#f87171' }}>
                              What NOT to Say (Traps & Red Flags)
                            </h4>
                          </div>
                          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                            {q.what_not_to_say}
                          </p>
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Capstone Completion Banner & Next Step */}
      <div
        className="card"
        style={{
          marginTop: '1.5rem',
          background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          textAlign: 'center',
          padding: '2.5rem 1.5rem',
        }}
      >
        <Award size={48} style={{ color: '#10b981', margin: '0 auto 1rem' }} />
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '0.5rem' }}>
          Ready to Ace Your Real-World Interview?
        </h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '640px', margin: '0 auto 1.5rem', fontSize: '0.9375rem' }}>
          You have reviewed {hubData?.practiced_count || 0} of {hubData?.total_questions || 15} questions. Keep practicing your live delivery, structure responses with the STAR method, and reinforce weaker topics in your skill roadmap.
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link to="/progress" className="btn btn-primary" style={{ padding: '0.625rem 1.25rem' }}>
            <span>View Full Journey Progress</span>
            <ArrowRight size={16} />
          </Link>
          <Link to="/profile" className="btn btn-secondary" style={{ padding: '0.625rem 1.25rem' }}>
            <span>My Profile & Achievements</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
