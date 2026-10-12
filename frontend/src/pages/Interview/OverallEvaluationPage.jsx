import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { 
  Award, 
  ArrowLeft, 
  ArrowRight, 
  CheckCircle2, 
  XCircle, 
  AlertCircle, 
  TrendingUp, 
  RotateCcw, 
  Loader2, 
  Sparkles, 
  Check, 
  BookOpen, 
  CheckCheck,
  Lightbulb,
  Target,
  Layers,
  Compass,
  Briefcase
} from 'lucide-react';
import LoadingState from '../../components/Common/LoadingState';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

export default function OverallEvaluationPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const goalIdParam = searchParams.get('goalId');
  const { isAuthenticated } = useAuth();

  const [activeGoal, setActiveGoal] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [isRetaking, setIsRetaking] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [validationWarning, setValidationWarning] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch user's active goal or list of goals
      const goals = await api.request('/goals');
      let targetGoal = null;
      if (goalIdParam) {
        targetGoal = goals.find(g => String(g.id) === String(goalIdParam));
      } else {
        targetGoal = goals.find(g => g.is_selected) || goals[0];
      }
      setActiveGoal(targetGoal);

      const targetGoalId = targetGoal ? targetGoal.id : null;
      const queryParam = targetGoalId ? `?goal_id=${targetGoalId}` : '';

      // 2. Fetch cross-skill questions
      const questionsData = await api.request(`/overall-evaluation/questions${queryParam}`);
      setQuestions(questionsData || []);

      // 3. Fetch latest overall evaluation if authenticated
      if (isAuthenticated) {
        try {
          const latestEval = await api.request(`/overall-evaluation/latest${queryParam}`);
          if (latestEval) {
            setEvaluationResult(latestEval);
          }
        } catch {
          // If not completed yet, proceed to taking mode
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to load overall evaluation data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    setIsRetaking(false);
    setSelectedAnswers({});
    setValidationWarning(null);
  }, [goalIdParam, isAuthenticated]);

  const handleSelectOption = (questionId, optionId) => {
    setValidationWarning(null);
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  const handleSubmit = async () => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: '/overall-evaluation' } } });
      return;
    }

    const answeredCount = Object.keys(selectedAnswers).length;
    if (answeredCount < questions.length) {
      setValidationWarning(`Please answer all ${questions.length} cross-skill scenarios before submitting (currently answered ${answeredCount}/${questions.length}).`);
      return;
    }

    setSubmitting(true);
    setError(null);
    setValidationWarning(null);

    try {
      const queryParam = activeGoal ? `?goal_id=${activeGoal.id}` : '';
      const payload = {
        answers: selectedAnswers
      };

      const result = await api.request(`/overall-evaluation/submit${queryParam}`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      setEvaluationResult(result);
      setIsRetaking(false);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      setError(err.message || 'Failed to submit overall evaluation.');
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
        message="Loading cross-skill evaluation & readiness metrics..." 
        subtext="Analyzing end-to-end architecture scenarios and interview readiness."
        variant="skeleton"
      />
    );
  }

  const answeredCount = Object.keys(selectedAnswers).length;
  const progressPercent = questions.length > 0 ? Math.round((answeredCount / questions.length) * 100) : 0;
  const showResults = evaluationResult && !isRetaking;

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(30, 41, 66, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%)',
          border: '1px solid var(--border-medium)',
          padding: '2rem',
          marginBottom: '1.75rem',
          position: 'relative',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
          <div className="badge badge-indigo">
            <Award size={14} />
            Capstone Milestone: Overall Self-Evaluation (Section 20)
          </div>
          {activeGoal?.category && (
            <div className="badge" style={{ background: 'rgba(255, 255, 255, 0.05)', color: 'var(--text-secondary)' }}>
              {activeGoal.category} Track
            </div>
          )}
        </div>

        <h1 style={{ fontSize: '1.875rem', fontWeight: 800, marginBottom: '0.625rem', letterSpacing: '-0.02em', color: '#fff' }}>
          {activeGoal?.title}: Comprehensive Career Readiness Evaluation
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', lineHeight: 1.6, maxWidth: '780px' }}>
          Evaluate your holistic capability across all completed skills. This cross-skill assessment tests end-to-end data flow, 
          multi-tier debugging, architectural synchronization, and realistic situational problem-solving to determine your professional interview readiness.
        </p>
      </div>

      {/* Error & Warning Alerts */}
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
      {/* VIEW A: DIAGNOSTIC READINESS REPORT (When user has completed evaluation)  */}
      {/* ========================================================================= */}
      {showResults ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '2.5rem' }}>
          {/* 1. Hero Score & Readiness Level Card */}
          <div
            className="card"
            style={{
              padding: '2rem',
              background: 'linear-gradient(135deg, rgba(22, 31, 51, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%)',
              border: `1px solid ${
                evaluationResult.percentage >= 85 
                  ? 'rgba(16, 185, 129, 0.4)' 
                  : evaluationResult.percentage >= 70 
                    ? 'rgba(99, 102, 241, 0.4)' 
                    : 'rgba(245, 158, 11, 0.4)'
              }`,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.5rem', marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
                <div
                  style={{
                    width: '84px',
                    height: '84px',
                    borderRadius: '50%',
                    background: evaluationResult.percentage >= 70 
                      ? 'rgba(16, 185, 129, 0.15)' 
                      : 'rgba(245, 158, 11, 0.15)',
                    border: `2px solid ${
                      evaluationResult.percentage >= 70 
                        ? 'var(--success)' 
                        : 'var(--warning)'
                    }`,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 800,
                  }}
                >
                  <span style={{ fontSize: '1.5rem', lineHeight: 1 }}>{evaluationResult.percentage}%</span>
                  <span style={{ fontSize: '0.625rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Readiness</span>
                </div>

                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.25rem', flexWrap: 'wrap' }}>
                    <h2 style={{ fontSize: '1.375rem', fontWeight: 800 }}>Overall Career Readiness Report</h2>
                    <span 
                      className={`badge ${
                        evaluationResult.readiness_level.includes('Exceptional') || evaluationResult.readiness_level.includes('Interview-Ready')
                          ? 'badge-success' 
                          : 'badge-warning'
                      }`}
                      style={{ fontSize: '0.75rem', padding: '0.25rem 0.625rem' }}
                    >
                      <Award size={14} />
                      {evaluationResult.readiness_level}
                    </span>
                  </div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    Cross-Skill Scenarios Correct: <strong>{evaluationResult.score}</strong> of <strong>{evaluationResult.total_questions}</strong>
                  </p>
                </div>
              </div>

              <button
                onClick={handleStartRetake}
                className="btn btn-secondary"
                style={{ fontSize: '0.8125rem' }}
              >
                <RotateCcw size={14} />
                <span>Retake Overall Evaluation</span>
              </button>
            </div>

            {/* Qualitative Readiness Summary */}
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
              {evaluationResult.readiness_summary}
            </div>
          </div>

          {/* 2. Strong Skills vs Skills Needing Improvement Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
            {/* Confirmed Strong Skills */}
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
                  Demonstrated Strong Skills ({evaluationResult.strong_skills.length})
                </h3>
              </div>
              
              {evaluationResult.strong_skills.length > 0 ? (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {evaluationResult.strong_skills.map((skillName, idx) => (
                    <span 
                      key={idx}
                      className="badge badge-success"
                      style={{ fontSize: '0.8125rem', padding: '0.375rem 0.75rem' }}
                    >
                      <Sparkles size={12} />
                      {skillName}
                    </span>
                  ))}
                </div>
              ) : (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  No dominant cross-skill strengths recorded yet. Reviewing multi-tier data flow will build synthesis.
                </p>
              )}
            </div>

            {/* Skills Needing Improvement */}
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
                  Skills Needing Improvement ({evaluationResult.skills_needing_improvement.length})
                </h3>
              </div>

              {evaluationResult.skills_needing_improvement.length > 0 ? (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {evaluationResult.skills_needing_improvement.map((skillName, idx) => (
                    <span 
                      key={idx}
                      className="badge badge-warning"
                      style={{ fontSize: '0.8125rem', padding: '0.375rem 0.75rem' }}
                    >
                      <AlertCircle size={12} />
                      {skillName}
                    </span>
                  ))}
                </div>
              ) : (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  Zero weak integration points detected! All cross-skill scenarios answered correctly.
                </p>
              )}
            </div>
          </div>

          {/* 3. Cross-Skill Architecture Insights */}
          {evaluationResult.cross_skill_insights && evaluationResult.cross_skill_insights.length > 0 && (
            <div
              className="card"
              style={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-medium)',
                padding: '1.5rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
                <Layers size={20} color="#818cf8" />
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700 }}>
                  Cross-Skill Architectural Synthesis
                </h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {evaluationResult.cross_skill_insights.map((insight, idx) => (
                  <div 
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '0.75rem',
                      fontSize: '0.875rem',
                      color: 'var(--text-main)',
                      lineHeight: 1.55,
                    }}
                  >
                    <CheckCircle2 size={16} color="var(--accent-primary)" style={{ flexShrink: 0, marginTop: '3px' }} />
                    <span>{insight}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 4. Actionable Pre-Interview Recommendations */}
          {evaluationResult.recommendations && evaluationResult.recommendations.length > 0 && (
            <div
              className="card"
              style={{
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-medium)',
                padding: '1.5rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
                <Lightbulb size={20} color="#f59e0b" />
                <h3 style={{ fontSize: '1.0625rem', fontWeight: 700 }}>
                  Strategic Recommendations Before Final Interview Prep
                </h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {evaluationResult.recommendations.map((rec, idx) => (
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
                        background: 'rgba(245, 158, 11, 0.15)',
                        color: '#fcd34d',
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
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 5. Question-by-Question Deep Review */}
          <div>
            <h3 style={{ fontSize: '1.1875rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <BookOpen size={18} color="var(--accent-primary)" />
              Scenario-by-Scenario Diagnostic Breakdown
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
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                          Scenario {index + 1}
                        </span>
                        {item.integrated_skills && item.integrated_skills.map((sk, skIdx) => (
                          <span key={skIdx} className="badge badge-indigo" style={{ fontSize: '0.6875rem' }}>
                            {sk}
                          </span>
                        ))}
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
                        lineHeight: 1.55,
                      }}
                    >
                      <strong style={{ color: '#a5b4fc' }}>Cross-Skill Explanation: </strong>
                      {item.explanation}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 6. Section 21 Capstone Transition Banner */}
          <div
            className="card"
            style={{
              padding: '2rem',
              background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%)',
              border: '1px solid rgba(99, 102, 241, 0.35)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '1.5rem',
              marginTop: '1rem',
            }}
          >
            <div style={{ maxWidth: '580px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <Briefcase size={18} color="#818cf8" />
                <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Next Phase: Final Interview Preparation (Section 21)
                </span>
              </div>
              <h3 style={{ fontSize: '1.375rem', fontWeight: 800, color: '#fff', marginBottom: '0.5rem' }}>
                Master the Exactly 15 Must-Know Interview Questions
              </h3>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                Your cross-skill evaluation is complete. Now review the comprehensive capstone questions for {activeGoal?.title}, featuring detailed answers, code snippets, practical scenarios, and interviewer rating expectations.
              </p>
            </div>

            <button
              onClick={() => navigate('/interview-prep')}
              className="btn btn-primary"
              style={{
                padding: '0.875rem 1.75rem',
                fontSize: '0.9375rem',
                boxShadow: '0 4px 14px rgba(99, 102, 241, 0.4)',
              }}
            >
              <span>Proceed to Final Interview Preparation</span>
              <ArrowRight size={18} />
            </button>
          </div>
        </div>
      ) : (
        /* ========================================================================= */
        /* VIEW B: TAKING THE OVERALL EVALUATION (Scenarios Form)                   */
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
                Assessment Progress: {answeredCount} of {questions.length} Scenarios Completed
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

          {/* Scenarios List */}
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
                  {/* Scenario Header */}
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
                        {q.question_type ? q.question_type.replace(/_/g, ' ') : 'Integration Scenario'}
                      </span>
                    </div>

                    <div style={{ display: 'flex', gap: '0.375rem', flexWrap: 'wrap' }}>
                      {q.integrated_skills && q.integrated_skills.map((sk, skIdx) => (
                        <span key={skIdx} className="badge badge-indigo" style={{ fontSize: '0.7rem' }}>
                          {sk}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Context box if available */}
                  {q.scenario_context && (
                    <div
                      style={{
                        padding: '0.75rem 1rem',
                        borderRadius: '6px',
                        background: 'rgba(99, 102, 241, 0.05)',
                        borderLeft: '3px solid var(--accent-primary)',
                        fontSize: '0.8125rem',
                        color: 'var(--text-secondary)',
                        marginBottom: '1rem',
                      }}
                    >
                      <strong style={{ color: '#a5b4fc' }}>Scenario Context: </strong>
                      {q.scenario_context}
                    </div>
                  )}

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

          {/* Submit Action Bar */}
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
                Ready to evaluate your holistic readiness?
              </div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
                {answeredCount === questions.length 
                  ? 'All cross-skill scenarios answered! Click submit to calculate your readiness rating & insights.' 
                  : `${questions.length - answeredCount} scenarios remaining.`}
              </div>
            </div>

            <button
              onClick={handleSubmit}
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
                  <span>Evaluating Readiness...</span>
                </>
              ) : (
                <>
                  <CheckCheck size={18} />
                  <span>Submit Overall Evaluation</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Bottom Navigation */}
      <div
        className="card responsive-actions stack-on-mobile"
        style={{
          padding: '1.25rem 1.5rem',
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-subtle)',
        }}
      >
        <button
          onClick={() => navigate('/skills')}
          className="btn btn-secondary"
        >
          <ArrowLeft size={16} />
          <span>&larr; Back to Skills Roadmap</span>
        </button>

        <button
          onClick={() => navigate('/interview-prep')}
          className="btn btn-primary"
        >
          <span>Proceed to Final Interview Preparation</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
}
