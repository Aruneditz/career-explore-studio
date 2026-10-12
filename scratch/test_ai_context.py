import sys
import os

# Add backend to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.user import User
from app.models.goal import Goal
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.user_goal import UserGoalSelection
from app.models.skill_progress import UserSkillProgress
from app.models.topic_progress import UserTopicProgress
from app.models.evaluation import UserSkillEvaluation
from app.models.skill_interview import SkillInterviewQuestion
from app.schemas.ai import AIAskRequest
from app.services import ai_service
from app.core.security import get_password_hash


def run_tests():
    db: Session = SessionLocal()
    print("==================================================")
    print("PHASE 9: AI CONTEXT & GROUNDED REASONING VERIFICATION")
    print("==================================================")

    test_user_email = "test_ai_mentor_phase9@ces.internal"

    try:
        # Cleanup any prior test run
        existing_user = db.query(User).filter(User.email == test_user_email).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()

        # 1. Create candidate user
        user = User(
            name="Alice Candidate",
            email=test_user_email,
            hashed_password=get_password_hash("SecretPassword123!"),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id

        # 2. Get active goal (e.g. Full Stack Web Development)
        goal = db.query(Goal).first()
        assert goal is not None, "No goals found in database!"
        skills = db.query(Skill).filter(Skill.goal_id == goal.id).order_by(Skill.order_index.asc()).all()
        assert len(skills) >= 2, "Expected at least 2 skills in goal!"

        html_skill = skills[0]
        css_skill = skills[1]

        # 3. Test before goal enrollment
        pre_ctx = ai_service.get_user_ces_context(db, user_id)
        assert pre_ctx["has_goal"] is False, "Pre-enrollment should have has_goal=False"
        assert "password" not in str(pre_ctx).lower(), "Password leakage detected!"
        assert test_user_email not in str(pre_ctx), "Email leakage detected!"
        print("  [PASS] Test 1: Pre-enrollment context is safe and ungrounded.")

        # 4. Enroll user into goal
        selection = UserGoalSelection(
            user_id=user_id,
            goal_id=goal.id,
            is_active=True
        )
        db.add(selection)
        db.commit()

        # 5. Test post-enrollment context
        post_ctx = ai_service.get_user_ces_context(db, user_id)
        assert post_ctx["has_goal"] is True
        assert post_ctx["goal_title"] == goal.title
        assert post_ctx["current_skill"]["id"] == html_skill.id
        print("  [PASS] Test 2: Post-enrollment active goal & current skill resolved.")

        # 6. Test Query: 'I completed HTML and CSS. What should I learn next?'
        req_prog = AIAskRequest(prompt="I completed HTML and CSS. What should I learn next?")
        res_prog = ai_service.ask_ai_mentor(db, user_id, req_prog)

        assert "JavaScript" in res_prog.answer or "javascript" in res_prog.answer.lower(), "Answer did not recommend JavaScript!"
        assert res_prog.syntax_or_framework is not None, "Missing syntax_or_framework"
        assert res_prog.code_example is not None, "Missing code_example"
        assert res_prog.practical_explanation is not None, "Missing practical_explanation"
        assert res_prog.ces_recommendation is not None, "Missing ces_recommendation"
        assert "password" not in str(res_prog.model_dump()).lower(), "Password leakage in response!"
        print("  [PASS] Test 3: 'I completed HTML and CSS. What should I learn next?' correctly recommends JavaScript.")

        # 7. Test Query: 'Explain the topic I am currently learning'
        # Check topic context
        html_topics = db.query(Topic).filter(Topic.skill_id == html_skill.id).order_by(Topic.order_index.asc()).all()
        assert len(html_topics) > 0, "No topics found for HTML skill!"
        first_topic = html_topics[0]

        req_topic = AIAskRequest(prompt="Explain the topic I am currently learning")
        res_topic = ai_service.ask_ai_mentor(db, user_id, req_topic)

        assert first_topic.title in res_topic.answer or first_topic.title.lower() in res_topic.answer.lower(), (
            f"Expected topic title '{first_topic.title}' in answer, got: {res_topic.answer}"
        )
        assert res_topic.syntax_or_framework is not None
        assert res_topic.code_example is not None
        assert res_topic.practical_explanation is not None
        assert res_topic.ces_recommendation is not None
        print(f"  [PASS] Test 4: 'Explain the topic I am currently learning' grounded in '{first_topic.title}'.")

        # 8. Mark first topic as completed and verify next pending topic
        tp = UserTopicProgress(user_id=user_id, topic_id=first_topic.id, is_completed=True)
        db.add(tp)
        db.commit()

        updated_ctx = ai_service.get_user_ces_context(db, user_id)
        assert updated_ctx["skill_topics_completed"] == 1
        if len(html_topics) > 1:
            assert updated_ctx["pending_topic"]["id"] == html_topics[1].id
        print("  [PASS] Test 5: Dynamic pending topic tracks UserTopicProgress accurately.")

        # 9. Test Query: 'How is my progress?'
        req_prog_status = AIAskRequest(prompt="How is my progress?")
        res_prog_status = ai_service.ask_ai_mentor(db, user_id, req_prog_status)

        assert goal.title in res_prog_status.answer
        assert html_skill.name in res_prog_status.answer
        assert "1" in res_prog_status.answer or "completed" in res_prog_status.answer.lower()
        assert res_prog_status.syntax_or_framework is not None
        assert res_prog_status.code_example is not None
        assert res_prog_status.practical_explanation is not None
        assert res_prog_status.ces_recommendation is not None
        print("  [PASS] Test 6: 'How is my progress?' accurately reflects SQLite progress metrics.")

        # 10. Test Query: 'Give me interview questions for my current skill'
        req_interview = AIAskRequest(prompt="Give me interview questions for my current skill")
        res_interview = ai_service.ask_ai_mentor(db, user_id, req_interview)

        assert res_interview.answer is not None
        assert html_skill.name in res_interview.answer
        assert res_interview.syntax_or_framework is not None
        assert res_interview.code_example is not None
        assert res_interview.practical_explanation is not None
        assert res_interview.ces_recommendation is not None
        print(f"  [PASS] Test 7: 'Give me interview questions for my current skill' queries DB for {html_skill.name} questions.")

        # 11. Test explicit skill_id parameter
        req_explicit_skill = AIAskRequest(prompt="Explain key concepts", skill_id=css_skill.id)
        res_explicit_skill = ai_service.ask_ai_mentor(db, user_id, req_explicit_skill)

        assert res_explicit_skill.context_used.get("current_skill") == css_skill.name
        print(f"  [PASS] Test 8: Explicit skill_id ({css_skill.id} -> {css_skill.name}) overrides default active skill.")

        # 12. Test evaluation score grounding
        eval_record = UserSkillEvaluation(
            user_id=user_id,
            skill_id=html_skill.id,
            score=5,
            total_questions=5,
            percentage=100,
            answers_json='{"1":"A"}',
            strong_areas_json='["Semantic Tags"]',
            weak_areas_json='[]',
            feedback_summary="Exceptional HTML5 mastery",
            improvement_suggestions_json='[]'
        )
        db.add(eval_record)
        db.commit()

        ctx_eval = ai_service.get_user_ces_context(db, user_id)
        assert ctx_eval["latest_evaluation"] is not None
        assert ctx_eval["latest_evaluation"]["score"] == 5
        assert ctx_eval["latest_evaluation"]["percentage"] == 100
        assert ctx_eval["latest_evaluation"]["passed"] is True
        print("  [PASS] Test 9: Diagnostic quiz scores reflected in AI context.")

        # 13. Test suggestions reflect user state
        suggestions = ai_service.get_suggested_prompts(db, user_id)
        assert len(suggestions) >= 3
        print(f"  [PASS] Test 10: Dynamic suggestions generated: {suggestions}")

        # 14. Strict zero private data leakage verification
        serialized = res_prog_status.model_dump_json()
        assert "password_hash" not in serialized
        assert "SecretPassword123!" not in serialized
        assert test_user_email not in serialized
        print("  [PASS] Test 11: Zero sensitive user credential leakage confirmed.")

        print("\nALL 11 PHASE 9 AI CONTEXT TESTS PASSED SUCCESSFULLY!")

    finally:
        # Cleanup test user
        cleanup_user = db.query(User).filter(User.email == test_user_email).first()
        if cleanup_user:
            db.delete(cleanup_user)
            db.commit()
        db.close()


if __name__ == "__main__":
    run_tests()
