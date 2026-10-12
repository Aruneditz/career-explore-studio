import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  Sliders, 
  ArrowLeft, 
  ArrowRight, 
  CheckCircle2, 
  XCircle, 
  AlertCircle, 
  Award, 
  TrendingUp, 
  RotateCcw, 
  Loader2, 
  HelpCircle, 
  Sparkles, 
  Check, 
  BookOpen, 
  CheckCheck,
  Lightbulb,
  Target
} from 'lucide-react';
import WorkflowProgressIndicator from '../../components/Navigation/WorkflowProgressIndicator';
import LoadingState from '../../components/Common/LoadingState';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

export default function SelfEvaluationPage() {
  const { skillId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [skill, setSkill] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [isRetaking, setIsRetaking] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [validationWarning, setValidationWarning] = useState(null);

  // Load skill, questions, and latest evaluation
  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch skill details
      const skillData = await api.request(`/skills/${skillId}`);
      setSkill(skillData);

      // 2. Fetch evaluation questions
      const questionsData = await api.request(`/skills/${skillId}/evaluation/questions`);
      setQuestions(questionsData || []);

      // 3. Fetch user's latest evaluation if authenticated
      if (isAuthenticated) {
        try {
          const latestEval = await api.request(`/skills/${skillId}/evaluation/latest`);
          if (latestEval) {
            setEvaluationResult(latestEval);
          }
        } catch {
          // If 401 or not found, proceed without existing result
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to load evaluation data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    setIsRetaking(false);
    setSelectedAnswers({});
    setValidationWarning(null);
  }, [skillId, isAuthenticated]);

  const handleSelectOption = (questionId, optionId) => {
    setValidationWarning(null);
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  const handleSubmitEvaluation = async () => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/skills/${skillId}/evaluation` } } });
      return;
    }

    const answeredCount = Object.keys(selectedAnswers).length;
    if (answeredCount < questions.length) {
      setValidationWarning(`Please answer all ${questions.length} questions before submitting (currently answered ${answeredCount}/${questions.length}).`);
      return;
    }

    setSubmitting(true);
    setError(null);
    setValidationWarning(null);

    try {
      const payload = {
        answers: selectedAnswers
      };

      const result = await api.request(`/skills/${skillId}/evaluation/submit`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      setEvaluationResult(result);
      setIsRetaking(false);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      setError(err.message || 'Failed to submit self-evaluation.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleStartRetake = () => {
    setSelectedAnswers({});
    setIsRetaking(true);
    setValidationWarning(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) {
    return (
      <LoadingState 
        message="Loading self-evaluation questions & diagnostics..." 
        subtext="Preparing diagnostic evaluation questions and scoring rubrics."
        variant="skeleton"
      />
    );
  }

  const answeredCount = Object.keys(selectedAnswers).length;
  const progressPercent = questions.length > 0 ? Math.round((answeredCount / questions.length) * 100) : 0;
  const showResults = evaluationResult && !isRetaking;

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto' }}>
      {/* 1. Workflow Progress Indicator (Stage 8: Evaluation) */}
      <WorkflowProgressIndicator 
        currentStage="evaluation" 
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
          overflow: 'hidden',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
          <div className="badge badge-indigo">
            <Sliders size={14} />
            Stage 8: Personal Self-Evaluation
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

        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, marginBottom: '0.625rem', letterSpacing: '-0.02em', color: '#fff' }}>
          {skill?.name}: Self-Evaluation & Diagnostic Feedback
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', lineHeight: 1.6, maxWidth: '750px' }}>
          Evaluate your conceptual command, practical problem-solving, and edge-case comprehension. 
          Gain individualized diagnostics highlighting confirmed strengths and high-priority improvement areas before technical interview rounds.
        </p>
      </div>

      {/* Error or Warning Alerts */}
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

      {validationWarning && (
        <div
          className="card"
          style={{
            background: 'var(--warning-bg)',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            color: '#fcd34d',
            padding: '1rem 1.25rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
          }}
        >
          <AlertCircle size={20} color="var(--warning)" style={{ flexShrink: 0 }} />
          <span style={{ fontSize: '0.875rem' }}>{validationWarning}</span>
        </div>
      )}

      {/* ========================================================================= */}
      {/* VIEW A: COMPREHENSIVE DIAGNOSTIC REPORT (When user has completed evaluation) */}
      {/* ========================================================================= */}
      {showResults ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '2rem' }}>
          {/* 1. Hero Score Card */}
          <div
            className="card"
            style={{
              padding: '2rem',
              background: 'linear-gradient(135deg, rgba(22, 31, 51, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%)',
              border: `1px solid ${
                evaluationResult.percentage >= 80 
                  ? 'rgba(16, 185, 129, 0.4)' 
                  : evaluationResult.percentage >= 60 
                    ? 'rgba(99, 102, 241, 0.4)' 
                    : 'rgba(245, 158, 11, 0.4)'
              }`,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.5rem', marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
                <div
                  style={{
                    width: '76px',
                    height: '76px',
                    borderRadius: '50%',
                    background: evaluationResult.percentage >= 80 
                      ? 'rgba(16, 185, 129, 0.15)' 
                      : evaluationResult.percentage >= 60 
                        ? 'rgba(99, 102, 241, 0.15)' 
                        : 'rgba(245, 158, 11, 0.15)',
                    border: `2px solid ${
                      evaluationResult.percentage >= 80 
                        ? 'var(--success)' 
                        : evaluationResult.percentage >= 60 
                          ? 'var(--accent-primary)' 
                          : 'var(--warning)'
                    }`,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 800,
                  }}
                >
                  <span style={{ fontSize: '1.375rem', lineHeight: 1 }}>{evaluationResult.percentage}%</span>
                  <span style={{ fontSize: '0.625rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Score</span>
                </div>

                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.25rem' }}>
                    <h2 style={{ fontSize: '1.375rem', fontWeight: 800 }}>Evaluation Results</h2>
                    <span 
                      className={`badge ${
                        evaluationResult.performance_level === 'Mastery' 
                          ? 'badge-success' 
                          : evaluationResult.performance_level === 'Proficient' 
                            ? 'badge-indigo' 
                            : 'badge-warning'
                      }`}
                      style={{ fontSize: '0.75rem', padding: '0.25rem 0.625rem' }}
                    >
                      {evaluationResult.performance_level === 'Mastery' && <Award size={14} />}
                      {evaluationResult.performance_level === 'Proficient' && <CheckCircle2 size={14} />}
                      {evaluationResult.performance_level === 'Developing' && <TrendingUp size={14} />}
                      {evaluationResult.performance_level} Rating
                    </span>
                  </div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    Correct Answers: <strong>{evaluationResult.score}</strong> of <strong>{evaluationResult.total_questions}</strong> questions
                  </p>
                </div>
              </div>

              <button
                onClick={handleStartRetake}
                className="btn btn-secondary"
                style={{ fontSize: '0.8125rem' }}
              >
                <RotateCcw size={14} />
                <span>Retake Evaluation</span>
              </button>
            </div>

            {/* Diagnostic Feedback Summary */}
            <div
              style={{
                padding: '1rem 1.25rem',
                borderRadius: '8px',
                background: 'rgba(0, 0, 0, 0.25)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                fontSize: '0.9375rem',
                lineHeight: 1.6,
              }}
            >
              {evaluationResult.feedback_summary}
            </div>
          </div>

          {/* 2. Strengths vs Weak Areas Diagnostics Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
            {/* Identified Strengths */}
            <div
              className="card"
              style={{
                background: 'rgba(16, 185, 129, 0.05)',
                border: '1px solid rgba(16, 185, 129, 0.25)',
                padding: '1.5rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
                <CheckCircle2 size={20} color="var(--success)" />
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, color: '#6ee7b7' }}>
                  Identified Strengths ({evaluationResult.strong_areas.length})
                </h3>
              </div>
              
              {evaluationResult.strong_areas.length > 0 ? (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {evaluationResult.strong_areas.map((area, idx) => (
                    <span 
                      key={idx}
                      className="badge badge-success"
                      style={{ fontSize: '0.8125rem', padding: '0.375rem 0.75rem' }}
                    >
                      <Sparkles size={12} />
                      {area}
                    </span>
                  ))}
                </div>
              ) : (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  No dominant strengths recorded in this attempt. Reviewing the Must-Know concepts will help solidify core knowledge.
                </p>
              )}
            </div>

            {/* Identified Weak Areas */}
            <div
              className="card"
              style={{
                background: 'rgba(245, 158, 11, 0.05)',
                border: '1px solid rgba(245, 158, 11, 0.25)',
                padding: '1.5rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
                <Target size={20} color="var(--warning)" />
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, color: '#fcd34d' }}>
                  Growth Focus Areas ({evaluationResult.weak_areas.length})
                </h3>
              </div>

              {evaluationResult.weak_areas.length > 0 ? (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {evaluationResult.weak_areas.map((area, idx) => (
                    <span 
                      key={idx}
                      className="badge badge-warning"
                      style={{ fontSize: '0.8125rem', padding: '0.375rem 0.75rem' }}
                    >
                      <AlertCircle size={12} />
                      {area}
                    </span>
                  ))}
                </div>
              ) : (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  Zero weak areas detected! All tested topic domains met full correctness criteria.
                </p>
              )}
            </div>
          </div>

          {/* 3. Actionable Improvement Suggestions */}
          {evaluationResult.improvement_suggestions && evaluationResult.improvement_suggestions.length > 0 && (
            <div
              className="card"
              style={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-medium)',
                padding: '1.5rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
                <Lightbulb size={20} color="#818cf8" />
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700 }}>
                  Tailored Improvement Recommendations
                </h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {evaluationResult.improvement_suggestions.map((suggestion, idx) => (
                  <div 
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '0.75rem',
                      fontSize: '0.875rem',
                      color: 'var(--text-secondary)',
                      lineHeight: 1.5,
                    }}
                  >
                    <span 
                      style={{
                        width: '20px',
                        height: '20px',
                        borderRadius: '50%',
                        background: 'rgba(99, 102, 241, 0.15)',
                        color: '#a5b4fc',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.6875rem',
                        fontWeight: 700,
                        flexShrink: 0,
                        marginTop: '2px',
                      }}
                    >
                      {idx + 1}
                    </span>
                    <span>{suggestion}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 4. Question-by-Question Deep Review */}
          <div>
            <h3 style={{ fontSize: '1.1875rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <BookOpen size={18} color="var(--accent-primary)" />
              Question-by-Question Deep Review
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {evaluationResult.question_breakdown.map((item, index) => {
                const isCorrect = item.is_correct;
                return (
                  <div
                    key={item.question_id}
                    className="card"
                    style={{
                      background: 'var(--bg-secondary)',
                      border: `1px solid ${isCorrect ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                      padding: '1.25rem 1.5rem',
                    }}
                  >
                    {/* Header */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                          Question {index + 1}
                        </span>
                        {item.topic_area && (
                          <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.05)', color: 'var(--text-secondary)', fontSize: '0.7rem' }}>
                            {item.topic_area}
                          </span>
                        )}
                      </div>

                      <div className={`badge ${isCorrect ? 'badge-success' : 'badge-warning'}`} style={{ fontSize: '0.75rem' }}>
                        {isCorrect ? (
                          <>
                            <Check size={14} /> Correct
                          </>
                        ) : (
                          <>
                            <XCircle size={14} /> Incorrect
                          </>
                        )}
                      </div>
                    </div>

                    {/* Question text */}
                    <div style={{ fontSize: '0.9375rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '1rem' }}>
                      {item.question_text}
                    </div>

                    {/* Answers Summary */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem', marginBottom: '1rem' }}>
                      <div
                        style={{
                          padding: '0.625rem 0.875rem',
                          borderRadius: '6px',
                          background: isCorrect ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                          border: `1px solid ${isCorrect ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                          fontSize: '0.8125rem',
                        }}
                      >
                        <span style={{ color: 'var(--text-muted)' }}>Your Choice: </span>
                        <strong>Option {item.selected_option || 'None'}</strong>
                      </div>

                      <div
                        style={{
                          padding: '0.625rem 0.875rem',
                          borderRadius: '6px',
                          background: 'rgba(16, 185, 129, 0.1)',
                          border: '1px solid rgba(16, 185, 129, 0.3)',
                          fontSize: '0.8125rem',
                        }}
                      >
                        <span style={{ color: 'var(--text-muted)' }}>Correct Answer: </span>
                        <strong>Option {item.correct_option}</strong>
                      </div>
                    </div>

                    {/* Explanation Callout */}
                    <div
                      style={{
                        padding: '0.875rem 1rem',
                        borderRadius: '6px',
                        background: 'rgba(0, 0, 0, 0.25)',
                        borderLeft: '3px solid var(--accent-primary)',
                        fontSize: '0.8125rem',
                        color: 'var(--text-secondary)',
                        lineHeight: 1.5,
                      }}
                    >
                      <strong style={{ color: '#a5b4fc' }}>Explanation: </strong>
                      {item.explanation}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      ) : (
        /* ========================================================================= */
        /* VIEW B: TAKING THE EVALUATION (Questions Form)                           */
        /* ========================================================================= */
        <div>
          {/* Progress Banner */}
          <div
            className="card"
            style={{
              padding: '1.25rem 1.5rem',
              marginBottom: '1.75rem',
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border-medium)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.625rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-main)' }}>
                Assessment Progress: {answeredCount} of {questions.length} Questions Answered
              </span>
              <span className="badge badge-indigo" style={{ fontSize: '0.75rem' }}>
                {progressPercent}% Complete
              </span>
            </div>

            <div
              style={{
                width: '100%',
                height: '8px',
                background: 'rgba(255, 255, 255, 0.08)',
                borderRadius: '9999px',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${progressPercent}%`,
                  height: '100%',
                  background: progressPercent === 100 ? 'var(--success)' : 'linear-gradient(90deg, #6366f1, #10b981)',
                  borderRadius: '9999px',
                  transition: 'width 250ms ease',
                }}
              />
            </div>
          </div>

          {/* Question List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '2rem' }}>
            {questions.map((q, qIndex) => {
              const selectedOpt = selectedAnswers[q.id];

              return (
                <div
                  key={q.id}
                  className="card"
                  style={{
                    background: 'var(--bg-secondary)',
                    border: `1px solid ${selectedOpt ? 'rgba(99, 102, 241, 0.4)' : 'var(--border-subtle)'}`,
                    padding: '1.5rem',
                    boxShadow: selectedOpt ? '0 0 16px -4px rgba(99, 102, 241, 0.2)' : 'var(--shadow-md)',
                    transition: 'all 200ms ease',
                  }}
                >
                  {/* Question Header */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.875rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span
                        style={{
                          width: '28px',
                          height: '28px',
                          borderRadius: '6px',
                          background: 'rgba(99, 102, 241, 0.2)',
                          color: '#a5b4fc',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '0.8125rem',
                          fontWeight: 700,
                        }}
                      >
                        {qIndex + 1}
                      </span>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                        {q.question_type ? q.question_type.replace('_', ' ') : 'Question'}
                      </span>
                    </div>

                    {q.topic_area && (
                      <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.05)', color: 'var(--text-secondary)', fontSize: '0.7rem' }}>
                        {q.topic_area}
                      </span>
                    )}
                  </div>

                  {/* Question Text */}
                  <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', lineHeight: 1.55 }}>
                    {q.question_text}
                  </h3>

                  {/* Options List */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
                    {q.options.map(option => {
                      const isSelected = selectedOpt === option.id;

                      return (
                        <div
                          key={option.id}
                          onClick={() => handleSelectOption(q.id, option.id)}
                          style={{
                            padding: '0.875rem 1rem',
                            borderRadius: '8px',
                            background: isSelected ? 'rgba(99, 102, 241, 0.15)' : 'rgba(0, 0, 0, 0.2)',
                            border: `1.5px solid ${isSelected ? 'var(--accent-primary)' : 'var(--border-subtle)'}`,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.875rem',
                            transition: 'all 150ms ease',
                          }}
                        >
                          {/* Option Badge */}
                          <div
                            style={{
                              width: '28px',
                              height: '28px',
                              borderRadius: '50%',
                              background: isSelected ? 'var(--accent-primary)' : 'rgba(255, 255, 255, 0.06)',
                              color: isSelected ? '#ffffff' : 'var(--text-secondary)',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              fontSize: '0.8125rem',
                              fontWeight: 700,
                              flexShrink: 0,
                            }}
                          >
                            {option.id}
                          </div>

                          {/* Option Text */}
                          <div style={{ flex: 1, fontSize: '0.875rem', color: isSelected ? '#ffffff' : 'var(--text-main)', lineHeight: 1.45 }}>
                            {option.text}
                          </div>

                          {isSelected && (
                            <Check size={18} color="var(--accent-primary)" style={{ flexShrink: 0 }} />
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Submission Bar */}
          <div
            className="card"
            style={{
              padding: '1.5rem',
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border-medium)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '1rem',
              marginBottom: '2rem',
            }}
          >
            <div>
              <div style={{ fontSize: '0.9375rem', fontWeight: 600 }}>
                Ready to evaluate your readiness?
              </div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                {answeredCount === questions.length 
                  ? 'All questions answered! Click submit to calculate your score & diagnostics.' 
                  : `${questions.length - answeredCount} questions remaining.`}
              </div>
            </div>

            <button
              onClick={handleSubmitEvaluation}
              disabled={submitting}
              className="btn btn-primary"
              style={{
                padding: '0.75rem 1.5rem',
                fontSize: '0.9375rem',
                minWidth: '220px',
              }}
            >
              {submitting ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  <span>Grading Answers...</span>
                </>
              ) : (
                <>
                  <CheckCheck size={18} />
                  <span>Submit Self-Evaluation</span>
                </>
              )}
            </button>
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
          onClick={() => navigate(`/skills/${skillId}/learn`)}
          className="btn btn-secondary"
        >
          <ArrowLeft size={16} />
          <span>&larr; Previous Stage: Learn & Complete</span>
        </button>

        <button
          onClick={() => navigate(`/skills/${skillId}/interview-prep`)}
          className="btn btn-primary"
        >
          <span>Move to Next Stage: Interview Preparation</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}
