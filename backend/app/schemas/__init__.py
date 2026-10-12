from app.schemas.common import HealthCheckResponse, MessageResponse
from app.schemas.auth import (
    UserBase, UserCreate, UserLogin, UserResponse, Token, TokenPayload,
    UserProfileUpdateRequest, UserProfileSummaryResponse
)
from app.schemas.goal import SkillSummary, GoalBase, GoalResponse, GoalSelectRequest, UserGoalResponse
from app.schemas.topic import TopicBase, TopicResponse, TopicToggleRequest, TopicToggleResponse
from app.schemas.skill import SkillOverviewResponse, SkillDetailResponse
from app.schemas.practical import PracticalContentResponse
from app.schemas.skill_progress import (
    SkillCompletionRequest,
    SkillProgressResponse,
    OverallGoalProgressResponse,
)
from app.schemas.evaluation import (
    EvaluationOption,
    EvaluationQuestionResponse,
    EvaluationSubmissionRequest,
    QuestionResult,
    EvaluationResultResponse,
)
from app.schemas.skill_interview import (
    SkillInterviewQuestionResponse,
    SkillSequenceInfoResponse,
)
from app.schemas.overall_evaluation import (
    OverallQuestionOption,
    OverallQuestionResponse,
    OverallEvaluationSubmissionRequest,
    OverallQuestionResult,
    OverallEvaluationResultResponse,
)
from app.schemas.final_interview import (
    FinalInterviewQuestionResponse,
    FinalInterviewPracticeToggleRequest,
    FinalInterviewPracticeStatusResponse,
    FinalInterviewHubResponse,
)
from app.schemas.dashboard import (
    AchievementBadge,
    SkillDashboardSummary,
    ComprehensiveDashboardResponse,
)
from app.schemas.certificate import (
    CertificateResponse,
    SkillCertificateChecklist,
    SkillCertificateStatusResponse,
    UserCertificatesListResponse,
)
from app.schemas.ai import (
    AIAskRequest,
    AIAskResponse,
    AISuggestionResponse,
)

__all__ = [
    "HealthCheckResponse",
    "MessageResponse",
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenPayload",
    "SkillSummary",
    "GoalBase",
    "GoalResponse",
    "GoalSelectRequest",
    "UserGoalResponse",
    "TopicBase",
    "TopicResponse",
    "TopicToggleRequest",
    "TopicToggleResponse",
    "SkillOverviewResponse",
    "SkillDetailResponse",
    "PracticalContentResponse",
    "SkillCompletionRequest",
    "SkillProgressResponse",
    "OverallGoalProgressResponse",
    "EvaluationOption",
    "EvaluationQuestionResponse",
    "EvaluationSubmissionRequest",
    "QuestionResult",
    "EvaluationResultResponse",
    "SkillInterviewQuestionResponse",
    "SkillSequenceInfoResponse",
    "OverallQuestionOption",
    "OverallQuestionResponse",
    "OverallEvaluationSubmissionRequest",
    "OverallQuestionResult",
    "OverallEvaluationResultResponse",
    "FinalInterviewQuestionResponse",
    "FinalInterviewPracticeToggleRequest",
    "FinalInterviewPracticeStatusResponse",
    "FinalInterviewHubResponse",
    "UserProfileUpdateRequest",
    "UserProfileSummaryResponse",
    "AchievementBadge",
    "SkillDashboardSummary",
    "ComprehensiveDashboardResponse",
    "CertificateResponse",
    "SkillCertificateChecklist",
    "SkillCertificateStatusResponse",
    "UserCertificatesListResponse",
    "AIAskRequest",
    "AIAskResponse",
    "AISuggestionResponse",
]
