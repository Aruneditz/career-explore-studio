import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  HelpCircle, 
  ArrowLeft, 
  ArrowRight, 
  ChevronDown, 
  ChevronUp, 
  CheckCircle2, 
  AlertTriangle, 
  Lightbulb, 
  Sparkles, 
  BookOpen, 
  Award, 
  Layers, 
  Loader2, 
  AlertCircle,
  FileText,
  Compass,
  Code2,
  Terminal,
  Copy,
  Check
} from 'lucide-react';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import CertificateStatusCard from '../../components/Certificate/CertificateStatusCard';
import AISearchTrigger from '../../components/AI/AISearchTrigger';
import LoadingState from '../../components/Common/LoadingState';
import EmptyState from '../../components/Common/EmptyState';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

export default function SkillInterviewPrepPage() {
  const { skillId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [skill, setSkill] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [sequence, setSequence] = useState(null);
  const [activeDifficulty, setActiveDifficulty] = useState('All');
  const [expandedQuestions, setExpandedQuestions] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copiedSnippetId, setCopiedSnippetId] = useState(null);

  const handleCopyCode = async (snippetId, text) => {
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      setCopiedSnippetId(snippetId);
      setTimeout(() => setCopiedSnippetId(null), 2000);
    } catch (err) {
      console.error('Failed to copy text', err);
    }
  };

  // Load skill, questions, and sequence progression
  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch skill details
      const skillData = await api.request(`/skills/${skillId}`);
      setSkill(skillData);

      // 2. Fetch interview questions
      const questionsData = await api.request(`/skills/${skillId}/interview-questions`);
      setQuestions(questionsData || []);

      // Expand all questions by default for easy scanning
      const initialExpanded = {};
      (questionsData || []).forEach(q => {
        initialExpanded[q.id] = true;
      });
      setExpandedQuestions(initialExpanded);

      // 3. Fetch sequence progression info (Section 19)
      const sequenceData = await api.request(`/skills/${skillId}/sequence`);
      setSequence(sequenceData);

      // Record interview stage interaction
      api.request(`/skills/${skillId}/record-stage`, {
        method: 'POST',
        body: JSON.stringify({ stage: 'interview' }),
      }).catch(() => {});
    } catch (err) {
      setError(err.message || 'Failed to load interview preparation data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    setActiveDifficulty('All');
  }, [skillId]);

  const toggleExpand = (questionId) => {
    setExpandedQuestions(prev => ({
      ...prev,
      [questionId]: !prev[questionId]
    }));
  };

  const expandAll = () => {
    const allExpanded = {};
    questions.forEach(q => {
      allExpanded[q.id] = true;
    });
    setExpandedQuestions(allExpanded);
  };

  const collapseAll = () => {
    setExpandedQuestions({});
  };

  // Filter questions based on active difficulty tab
  const filteredQuestions = activeDifficulty === 'All'
    ? questions
    : questions.filter(q => q.difficulty.toLowerCase() === activeDifficulty.toLowerCase());

  // Count per difficulty
  const counts = {
    All: questions.length,
    Basic: questions.filter(q => q.difficulty.toLowerCase() === 'basic').length,
    Intermediate: questions.filter(q => q.difficulty.toLowerCase() === 'intermediate').length,
    Advanced: questions.filter(q => q.difficulty.toLowerCase() === 'advanced').length,
  };

  if (loading) {
    return (
      <LoadingState 
        message="Loading interview questions..." 
        subtext="Fetching structured questions, syntax, and model responses."
        variant="skeleton"
      />
    );
  }

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto' }}>
      {/* 1. Workflow Progress Indicator (Stage 9: Interview) */}
      <WorkflowProgressIndicator 
        currentStage="interview" 
        skillId={skillId} 
        skillName={skill?.name} 
      />

      {/* Header Banner */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(30, 41, 66, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%)',
          border: '1px solid var(--border-medium)',
          padding: '1.75rem',
          marginBottom: '1.75rem',
          position: 'relative',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.75rem', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
            <div className="badge badge-indigo">
              <HelpCircle size={14} />
              Stage 9: Skill Interview Preparation
            </div>
            {skill?.category && (
              <div className="badge" style={{ background: 'rgba(255, 255, 255, 0.05)', color: 'var(--text-secondary)' }}>
                {skill.category}
              </div>
            )}
            <div className="badge" style={{ background: skill?.is_technical ? 'rgba(99, 102, 241, 0.15)' : 'rgba(16, 185, 129, 0.15)', color: skill?.is_technical ? '#a5b4fc' : '#6ee7b7' }}>
              {skill?.is_technical ? 'Technical Skill Track' : 'Non-Technical Skill Track'}
            </div>
          </div>
          <AISearchTrigger skillId={parseInt(skillId, 10)} />
        </div>

        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, marginBottom: '0.625rem', letterSpacing: '-0.02em', color: '#fff' }}>
          {skill?.name}: Core Interview Questions & Model Answers
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', lineHeight: 1.6, maxWidth: '750px' }}>
          Master the exact questions engineering and hiring managers ask for {skill?.name}. 
          Review structured model answers, in-depth architectural reasoning, answering tips, and common pitfalls to avoid.
        </p>
      </div>

      {/* Error Callout */}
      {error && (
        <div
          className="card"
          style={{
            background: 'var(--danger-bg)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            color: '#fca5a5',
            padding: '1rem 1.25rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
          }}
        >
          <AlertCircle size={20} color="var(--danger)" style={{ flexShrink: 0 }} />
          <span style={{ fontSize: '0.875rem' }}>{error}</span>
        </div>
      )}

      {/* 2. Difficulty Filter & Action Toolbar */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
          marginBottom: '1.5rem',
        }}
      >
        {/* Difficulty Pills */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {['All', 'Basic', 'Intermediate', 'Advanced'].map(diff => {
            const isActive = activeDifficulty === diff;
            const count = counts[diff] || 0;

            return (
              <button
                key={diff}
                onClick={() => setActiveDifficulty(diff)}
                style={{
                  padding: '0.5rem 1rem',
                  borderRadius: '8px',
                  border: `1px solid ${isActive ? 'var(--accent-primary)' : 'var(--border-subtle)'}`,
                  background: isActive ? 'var(--accent-light)' : 'var(--bg-secondary)',
                  color: isActive ? '#a5b4fc' : 'var(--text-secondary)',
                  fontWeight: isActive ? 700 : 500,
                  fontSize: '0.8125rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 150ms ease',
                }}
              >
                <span>{diff}</span>
                <span
                  style={{
                    padding: '0.125rem 0.375rem',
                    borderRadius: '9999px',
                    background: isActive ? 'var(--accent-primary)' : 'rgba(255, 255, 255, 0.08)',
                    color: isActive ? '#ffffff' : 'var(--text-muted)',
                    fontSize: '0.6875rem',
                  }}
                >
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Expand / Collapse Toggle Buttons */}
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={expandAll}
            className="btn btn-outline"
            style={{ fontSize: '0.75rem', padding: '0.375rem 0.75rem', minHeight: '32px' }}
          >
            Expand All
          </button>
          <button
            onClick={collapseAll}
            className="btn btn-outline"
            style={{ fontSize: '0.75rem', padding: '0.375rem 0.75rem', minHeight: '32px' }}
          >
            Collapse All
          </button>
        </div>
      </div>

      {/* 3. Interview Questions Accordion List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '2.5rem' }}>
        {filteredQuestions.length === 0 ? (
          <EmptyState
            icon={HelpCircle}
            title="No Interview Questions Found"
            description="No interview questions found for the selected difficulty level."
            actionLabel="Show All Difficulty Levels"
            onAction={() => setActiveDifficulty('All')}
          />
        ) : (
          filteredQuestions.map((q, idx) => {
            const isExpanded = !!expandedQuestions[q.id];

            const diffBadgeClass = 
              q.difficulty.toLowerCase() === 'basic' 
                ? 'badge-success' 
                : q.difficulty.toLowerCase() === 'intermediate' 
                  ? 'badge-warning' 
                  : 'badge-indigo';

            return (
              <div
                key={q.id}
                className="card"
                style={{
                  background: 'var(--bg-secondary)',
                  border: '1px solid var(--border-subtle)',
                  padding: 0,
                  overflow: 'hidden',
                  transition: 'all 200ms ease',
                }}
              >
                {/* Accordion Card Header */}
                <div
                  onClick={() => toggleExpand(q.id)}
                  style={{
                    padding: '1.25rem 1.5rem',
                    cursor: 'pointer',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    gap: '1rem',
                    background: isExpanded ? 'rgba(255, 255, 255, 0.02)' : 'transparent',
                    borderBottom: isExpanded ? '1px solid var(--border-subtle)' : 'none',
                  }}
                >
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', flexWrap: 'wrap' }}>
                      <span className={`badge ${diffBadgeClass}`} style={{ fontSize: '0.7rem' }}>
                        {q.difficulty}
                      </span>
                      {q.category && (
                        <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.05)', color: 'var(--text-secondary)', fontSize: '0.7rem' }}>
                          {q.category}
                        </span>
                      )}
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        Question {idx + 1} of {filteredQuestions.length}
                      </span>
                    </div>

                    <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, color: '#f8fafc', lineHeight: 1.45 }}>
                      {q.question}
                    </h3>
                  </div>

                  <div
                    style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      background: 'rgba(255, 255, 255, 0.04)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'var(--text-secondary)',
                      flexShrink: 0,
                    }}
                  >
                    {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                  </div>
                </div>

                {/* Accordion Card Body */}
                {isExpanded && (
                  <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                    {/* 1. Simple Answer / Core Model Answer */}
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <CheckCircle2 size={16} color="var(--success)" />
                        <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#6ee7b7', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                          1. Simple Answer & Core Explanation
                        </span>
                      </div>
                      <div
                        style={{
                          padding: '1rem 1.25rem',
                          borderRadius: '8px',
                          background: 'rgba(16, 185, 129, 0.08)',
                          border: '1px solid rgba(16, 185, 129, 0.25)',
                          fontSize: '0.9375rem',
                          color: 'var(--text-main)',
                          lineHeight: 1.6,
                        }}
                      >
                        {q.expected_answer}
                      </div>
                    </div>

                    {/* 2. Simple Syntax / Framework Structure (when provided) */}
                    {q.simple_syntax && (
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                          <Code2 size={16} color="#818cf8" />
                          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                            {skill?.is_technical ? '2. Simple Syntax / Pattern Structure' : '2. Simple Framework / Execution Structure'}
                          </span>
                        </div>
                        <div
                          style={{
                            background: '#0d1117',
                            border: '1px solid #30363d',
                            borderRadius: '8px',
                            padding: '0.875rem 1.25rem',
                            fontFamily: 'Consolas, Monaco, "Andale Mono", monospace',
                            fontSize: '0.875rem',
                            lineHeight: 1.6,
                            color: '#79c0ff',
                            whiteSpace: 'pre-wrap',
                            overflowX: 'auto',
                          }}
                        >
                          {q.simple_syntax}
                        </div>
                      </div>
                    )}

                    {/* 3. Small Practical Example / Code (when provided) */}
                    {q.small_example && (
                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <Sparkles size={16} color="#38bdf8" />
                            <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#7dd3fc', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                              {skill?.is_technical ? '3. Small Practical Example (Short Code)' : '3. Small Practical Example (Real-World Case)'}
                            </span>
                          </div>
                          <button
                            onClick={() => handleCopyCode(`example-${q.id}`, q.small_example)}
                            className="btn btn-outline"
                            style={{
                              padding: '0.2rem 0.55rem',
                              minHeight: '26px',
                              height: '26px',
                              fontSize: '0.75rem',
                              gap: '0.3rem',
                              borderColor: '#30363d',
                              color: copiedSnippetId === `example-${q.id}` ? 'var(--success)' : '#c9d1d9',
                            }}
                          >
                            {copiedSnippetId === `example-${q.id}` ? <Check size={12} color="var(--success)" /> : <Copy size={12} />}
                            <span>{copiedSnippetId === `example-${q.id}` ? 'Copied!' : 'Copy'}</span>
                          </button>
                        </div>
                        <div
                          style={{
                            background: '#090d16',
                            border: '1px solid rgba(56, 189, 248, 0.25)',
                            borderRadius: '8px',
                            padding: '1rem 1.25rem',
                            fontFamily: skill?.is_technical ? 'Consolas, Monaco, "Andale Mono", monospace' : 'inherit',
                            fontSize: '0.875rem',
                            lineHeight: 1.6,
                            color: '#e6edf3',
                            whiteSpace: 'pre-wrap',
                            overflowX: 'auto',
                          }}
                        >
                          {q.small_example}
                        </div>
                      </div>
                    )}

                    {/* 4. Practical & Architectural Explanation */}
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <BookOpen size={16} color="#c084fc" />
                        <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#d8b4fe', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                          4. Practical Explanation & Architectural Context
                        </span>
                      </div>
                      <div
                        style={{
                          padding: '1rem 1.25rem',
                          borderRadius: '8px',
                          background: 'rgba(0, 0, 0, 0.25)',
                          border: '1px solid var(--border-subtle)',
                          fontSize: '0.875rem',
                          color: 'var(--text-secondary)',
                          lineHeight: 1.6,
                        }}
                      >
                        {q.explanation}
                      </div>
                    </div>

                    {/* Practical Scenario (if provided) */}
                    {q.practical_scenario && (
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                          <Compass size={16} color="#f59e0b" />
                          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#fcd34d', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                            Practical Real-World Scenario
                          </span>
                        </div>
                        <div
                          style={{
                            padding: '1rem 1.25rem',
                            borderRadius: '8px',
                            background: 'rgba(245, 158, 11, 0.08)',
                            border: '1px solid rgba(245, 158, 11, 0.25)',
                            fontSize: '0.875rem',
                            color: 'var(--text-main)',
                            lineHeight: 1.6,
                          }}
                        >
                          {q.practical_scenario}
                        </div>
                      </div>
                    )}

                    {/* Two-Column Grid: Pro Tips vs Pitfalls */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
                      {/* Tips for Answering */}
                      <div
                        style={{
                          padding: '1rem 1.25rem',
                          borderRadius: '8px',
                          background: 'rgba(99, 102, 241, 0.06)',
                          border: '1px solid rgba(99, 102, 241, 0.25)',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                          <Lightbulb size={16} color="#818cf8" />
                          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase' }}>
                            Tips for Structuring Your Answer
                          </span>
                        </div>
                        <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                          {q.tips_for_answering}
                        </p>
                      </div>

                      {/* Common Mistakes to Avoid */}
                      <div
                        style={{
                          padding: '1rem 1.25rem',
                          borderRadius: '8px',
                          background: 'rgba(239, 68, 68, 0.06)',
                          border: '1px solid rgba(239, 68, 68, 0.25)',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                          <AlertTriangle size={16} color="var(--danger)" />
                          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#fca5a5', textTransform: 'uppercase' }}>
                            Common Mistakes to Avoid
                          </span>
                        </div>
                        <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                          {q.common_mistakes}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Official Skill Certificate Status (Upgrade #5) */}
      <div style={{ marginBottom: '2rem' }}>
        <CertificateStatusCard 
          skillId={skillId} 
          skillName={skill?.name} 
        />
      </div>

      {/* 4. Sequence Progression Action Banner (Section 19: Move to Next Skill) */}
      {sequence && (
        <div
          className="card"
          style={{
            padding: '2rem',
            marginBottom: '2rem',
            background: sequence.is_last_skill 
              ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%)'
              : 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%)',
            border: `1px solid ${sequence.is_last_skill ? 'rgba(16, 185, 129, 0.35)' : 'rgba(99, 102, 241, 0.35)'}`,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '1.5rem',
          }}
        >
          <div style={{ maxWidth: '580px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              {sequence.is_last_skill ? (
                <Award size={18} color="var(--success)" />
              ) : (
                <Sparkles size={18} color="#818cf8" />
              )}
              <span 
                style={{ 
                  fontSize: '0.8125rem', 
                  fontWeight: 700, 
                  textTransform: 'uppercase', 
                  letterSpacing: '0.06em', 
                  color: sequence.is_last_skill ? 'var(--success)' : '#a5b4fc' 
                }}
              >
                {sequence.is_last_skill 
                  ? 'All Goal Skills Completed!' 
                  : `Curriculum Milestone: Skill ${sequence.current_skill_index} of ${sequence.total_skills_in_goal}`}
              </span>
            </div>

            <h3 style={{ fontSize: '1.375rem', fontWeight: 800, marginBottom: '0.5rem', color: '#fff' }}>
              {sequence.is_last_skill 
                ? 'Ready for the Final Capstone Evaluation?' 
                : `Next Skill: ${sequence.next_skill_name}`}
            </h3>

            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
              {sequence.is_last_skill
                ? `You have thoroughly reviewed all ${sequence.total_skills_in_goal} skills in your ${sequence.goal_title} journey. Proceed to the comprehensive final evaluation and the exactly 15 Must-Know interview questions.`
                : `Proceed to explore the next skill on your path. You will be guided through overview, topics, practical exercises, self-evaluation, and interview preparation.`}
            </p>
          </div>

          <div>
            {sequence.has_next_skill ? (
              <button
                onClick={() => navigate(`/skills/${sequence.next_skill_id}/overview`)}
                className="btn btn-primary"
                style={{
                  padding: '0.875rem 1.75rem',
                  fontSize: '0.9375rem',
                  boxShadow: '0 4px 14px rgba(99, 102, 241, 0.4)',
                }}
              >
                <span>Move to Next Skill: {sequence.next_skill_name}</span>
                <ArrowRight size={18} />
              </button>
            ) : (
              <button
                onClick={() => navigate('/overall-evaluation')}
                className="btn btn-primary"
                style={{
                  padding: '0.875rem 1.75rem',
                  fontSize: '0.9375rem',
                  background: 'var(--success)',
                  borderColor: 'var(--success)',
                  boxShadow: '0 4px 14px rgba(16, 185, 129, 0.4)',
                }}
              >
                <span>Proceed to Overall Self-Evaluation</span>
                <ArrowRight size={18} />
              </button>
            )}
          </div>
        </div>
      )}

      {/* 5. Bottom Workflow Navigation */}
      <div
        className="card responsive-actions stack-on-mobile"
        style={{
          padding: '1.25rem 1.5rem',
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-subtle)',
        }}
      >
        <button
          onClick={() => navigate(`/skills/${skillId}/evaluation`)}
          className="btn btn-secondary"
        >
          <ArrowLeft size={16} />
          <span>&larr; Previous Stage: Personal Self-Evaluation</span>
        </button>

        {sequence?.has_next_skill ? (
          <button
            onClick={() => navigate(`/skills/${sequence.next_skill_id}/overview`)}
            className="btn btn-primary"
          >
            <span>Move to Next Skill: {sequence.next_skill_name}</span>
            <ArrowRight size={16} />
          </button>
        ) : (
          <button
            onClick={() => navigate('/overall-evaluation')}
            className="btn btn-primary"
            style={{ background: 'var(--success)', borderColor: 'var(--success)' }}
          >
            <span>Proceed to Overall Evaluation</span>
            <ArrowRight size={16} />
          </button>
        )}
      </div>
    </div>
  );
}
