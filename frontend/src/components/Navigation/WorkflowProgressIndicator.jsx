import React, { memo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Target, 
  BookOpen, 
  FileText, 
  ListChecks, 
  Star, 
  Code, 
  Sliders, 
  HelpCircle,
  CheckCircle2
} from 'lucide-react';

export const WORKFLOW_STAGES = [
  { key: 'goal', label: 'Goal', icon: Target, route: (sId) => '/goals' },
  { key: 'skill', label: 'Skill', icon: BookOpen, route: (sId) => '/skills' },
  { key: 'overview', label: 'Overview', icon: FileText, route: (sId) => `/skills/${sId}/overview` },
  { key: 'topics', label: 'Topics', icon: ListChecks, route: (sId) => `/skills/${sId}/topics` },
  { key: 'important', label: 'Important', icon: Star, route: (sId) => `/skills/${sId}/important-topics` },
  { key: 'practical', label: 'Practical', icon: Code, route: (sId) => `/skills/${sId}/practical` },
  { key: 'learn', label: 'Complete', icon: CheckCircle2, route: (sId) => `/skills/${sId}/learn` },
  { key: 'evaluation', label: 'Evaluation', icon: Sliders, route: (sId) => `/skills/${sId}/evaluation` },
  { key: 'interview', label: 'Interview', icon: HelpCircle, route: (sId) => `/skills/${sId}/interview-prep` },
];

function WorkflowProgressIndicatorComponent({ currentStage, skillId, skillName }) {
  const navigate = useNavigate();
  const currentIndex = WORKFLOW_STAGES.findIndex(s => s.key === currentStage);

  return (
    <nav
      className="card"
      aria-label="Workflow Curriculum Stage Progress"
      style={{
        padding: '1rem 1.25rem',
        background: 'var(--bg-secondary)',
        border: '1px solid var(--border-medium)',
        marginBottom: '1.5rem',
      }}
    >
      {/* Skill Context Sub-header */}
      {skillName && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.875rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', fontWeight: 700 }}>
              Active Skill:
            </span>
            <span style={{ fontSize: '0.875rem', fontWeight: 700, color: '#a5b4fc' }}>
              {skillName}
            </span>
          </div>

          <div className="badge badge-indigo" style={{ fontSize: '0.6875rem' }}>
            Stage {currentIndex + 1} of {WORKFLOW_STAGES.length}: {WORKFLOW_STAGES[currentIndex]?.label}
          </div>
        </div>
      )}

      {/* Progress Steps Track */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          overflowX: 'auto',
          WebkitOverflowScrolling: 'touch',
          scrollbarWidth: 'thin',
          paddingBottom: '0.4rem',
          gap: '0.375rem',
        }}
      >
        {WORKFLOW_STAGES.map((stage, idx) => {
          const Icon = stage.icon;
          const isCompleted = idx < currentIndex;
          const isCurrent = idx === currentIndex;

          let badgeBg = 'var(--bg-primary)';
          let badgeBorder = 'var(--border-subtle)';
          let badgeColor = 'var(--text-muted)';

          if (isCurrent) {
            badgeBg = 'var(--accent-primary)';
            badgeBorder = 'var(--accent-primary)';
            badgeColor = '#ffffff';
          } else if (isCompleted) {
            badgeBg = 'rgba(16, 185, 129, 0.15)';
            badgeBorder = 'rgba(16, 185, 129, 0.3)';
            badgeColor = '#10b981';
          }

          const canClick = isCompleted || isCurrent || (skillId && idx <= 6);

          return (
            <React.Fragment key={stage.key}>
              {/* Step Node */}
              <button
                type="button"
                onClick={() => canClick && navigate(stage.route(skillId))}
                disabled={!canClick}
                aria-current={isCurrent ? 'step' : undefined}
                aria-label={`Stage ${idx + 1}: ${stage.label}${isCompleted ? ' (Completed)' : isCurrent ? ' (Current)' : ''}`}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.375rem',
                  padding: '0.35rem 0.65rem',
                  borderRadius: '9999px',
                  background: badgeBg,
                  border: `1px solid ${badgeBorder}`,
                  color: badgeColor,
                  fontSize: '0.75rem',
                  fontWeight: isCurrent ? 700 : 500,
                  whiteSpace: 'nowrap',
                  cursor: canClick ? 'pointer' : 'default',
                  transition: 'all 150ms ease',
                  flexShrink: 0,
                  outline: 'none',
                }}
                title={`Stage ${idx + 1}: ${stage.label}`}
              >
                {isCompleted ? (
                  <CheckCircle2 size={13} style={{ flexShrink: 0 }} />
                ) : (
                  <Icon size={13} style={{ flexShrink: 0 }} />
                )}
                <span>{stage.label}</span>
              </button>

              {/* Connecting Line between steps */}
              {idx < WORKFLOW_STAGES.length - 1 && (
                <div
                  style={{
                    height: '2px',
                    flex: '1 1 12px',
                    minWidth: '8px',
                    background: isCompleted ? 'var(--success)' : 'var(--border-subtle)',
                    transition: 'background 200ms ease',
                  }}
                  aria-hidden="true"
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </nav>
  );
}

export const WorkflowProgressIndicator = memo(WorkflowProgressIndicatorComponent);
export default WorkflowProgressIndicator;
