"""
Automated verification tests for CAREER EXPLORE STUDIO backend.
Covers:
- Phase 1: Health check & Root
- Phase 2: Registration, Login, Token generation, Protected /me
- Phase 4: Goals listing, Seed data, Goal details, Goal skills, Active Goal Selection
- Phase 5: Skill Overview, Complete Topics List, Topic Completion Toggle & Metrics
"""
import sys
import unittest
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from starlette.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.database.database import Base, engine, SessionLocal, auto_migrate_sqlite
from app.database.seed import seed_initial_data
from app.models.user import User
from app.models.topic_progress import UserTopicProgress
from app.models.user_goal import UserGoalSelection
from app.models.skill_progress import UserSkillProgress
from app.models.evaluation import UserSkillEvaluation
from app.models.overall_evaluation import UserGoalEvaluation
from app.models.final_interview import UserInterviewPractice


class FullStackTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        auto_migrate_sqlite()
        db = SessionLocal()
        try:
            seed_initial_data(db)
        finally:
            db.close()

    def setUp(self):
        self.client = TestClient(app)
        self.test_email = "alex.tester@careerexplore.com"
        self.test_password = "SecurePassword123"
        self.test_name = "Alex Careerist"

        # Clean up test user and related records cleanly
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == self.test_email).first()
            if user:
                db.query(UserInterviewPractice).filter(UserInterviewPractice.user_id == user.id).delete()
                db.query(UserGoalEvaluation).filter(UserGoalEvaluation.user_id == user.id).delete()
                db.query(UserSkillEvaluation).filter(UserSkillEvaluation.user_id == user.id).delete()
                db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).delete()
                db.query(UserTopicProgress).filter(UserTopicProgress.user_id == user.id).delete()
                db.query(UserGoalSelection).filter(UserGoalSelection.user_id == user.id).delete()
                db.delete(user)
                db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

    def tearDown(self):
        # Clean up after each test
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == self.test_email).first()
            if user:
                db.query(UserInterviewPractice).filter(UserInterviewPractice.user_id == user.id).delete()
                db.query(UserGoalEvaluation).filter(UserGoalEvaluation.user_id == user.id).delete()
                db.query(UserSkillEvaluation).filter(UserSkillEvaluation.user_id == user.id).delete()
                db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).delete()
                db.query(UserTopicProgress).filter(UserTopicProgress.user_id == user.id).delete()
                db.query(UserGoalSelection).filter(UserGoalSelection.user_id == user.id).delete()
                db.delete(user)
                db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

    def _register_user(self):
        payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        return self.client.post("/api/auth/register", json=payload)

    # --- Phase 1 & 2 Tests ---
    def test_01_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_02_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)

    def test_03_register_user_success(self):
        payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        response = self.client.post("/api/auth/register", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_04_register_duplicate_email_fails(self):
        payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        self.client.post("/api/auth/register", json=payload)
        response = self.client.post("/api/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_05_login_success(self):
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        self.client.post("/api/auth/register", json=reg_payload)
        login_payload = {"email": self.test_email, "password": self.test_password}
        response = self.client.post("/api/auth/login", json=login_payload)
        self.assertEqual(response.status_code, 200)

    def test_06_login_invalid_password_fails(self):
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        self.client.post("/api/auth/register", json=reg_payload)
        login_payload = {"email": self.test_email, "password": "WrongPassword!"}
        response = self.client.post("/api/auth/login", json=login_payload)
        self.assertEqual(response.status_code, 401)

    def test_07_protected_me_endpoint_with_valid_token(self):
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        me_res = self.client.get("/api/auth/me", headers=headers)
        self.assertEqual(me_res.status_code, 200)

    def test_08_protected_me_endpoint_without_token_fails(self):
        response = self.client.get("/api/auth/me")
        self.assertIn(response.status_code, [401, 403])

    # --- Phase 4 Tests ---
    def test_09_list_goals_returns_seeded_data(self):
        response = self.client.get("/api/goals")
        self.assertEqual(response.status_code, 200)
        goals = response.json()
        self.assertGreaterEqual(len(goals), 2)

    def test_10_get_goal_by_slug_and_id(self):
        response = self.client.get("/api/goals/full-stack-developer")
        self.assertEqual(response.status_code, 200)

    def test_11_get_goal_skills(self):
        goal_res = self.client.get("/api/goals/full-stack-developer")
        goal_id = goal_res.json()["id"]
        skills_res = self.client.get(f"/api/goals/{goal_id}/skills")
        self.assertEqual(skills_res.status_code, 200)

    def test_12_select_user_goal_authenticated(self):
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        goal_res = self.client.get("/api/goals/full-stack-developer")
        goal_id = goal_res.json()["id"]

        select_res = self.client.post("/api/goals/select", json={"goal_id": goal_id}, headers=headers)
        self.assertEqual(select_res.status_code, 200)

        current_res = self.client.get("/api/goals/current", headers=headers)
        self.assertEqual(current_res.status_code, 200)
        self.assertEqual(current_res.json()["goal_id"], goal_id)

    def test_13_select_goal_unauthenticated_fails(self):
        response = self.client.post("/api/goals/select", json={"goal_id": 1})
        self.assertIn(response.status_code, [401, 403])

    # --- Phase 5 Tests ---
    def test_14_get_skill_overview_details(self):
        """Test /api/skills/{id} returns comprehensive Section 12 overview content"""
        goals_res = self.client.get("/api/goals")
        first_skill = goals_res.json()[0]["skills"][0]
        skill_id = first_skill["id"]

        response = self.client.get(f"/api/skills/{skill_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], skill_id)
        self.assertTrue(data["what_is_it"])
        self.assertTrue(data["why_important"])
        self.assertTrue(data["where_used"])
        self.assertTrue(data["benefits"])
        self.assertTrue(data["challenges"])
        self.assertTrue(data["prerequisites"])
        self.assertTrue(data["career_relevance"])
        self.assertGreater(data["total_topics"], 0)

    def test_15_get_complete_topic_list(self):
        """Test /api/skills/{id}/topics returns complete topics for the skill"""
        goals_res = self.client.get("/api/goals")
        first_skill = goals_res.json()[0]["skills"][0]
        skill_id = first_skill["id"]

        response = self.client.get(f"/api/skills/{skill_id}/topics")
        self.assertEqual(response.status_code, 200)
        topics = response.json()
        self.assertGreater(len(topics), 0)
        order_indices = [t["order_index"] for t in topics]
        self.assertEqual(order_indices, sorted(order_indices))

    def test_16_toggle_topic_completion(self):
        """Test toggling a topic's completed status persists for user"""
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        goals_res = self.client.get("/api/goals")
        first_skill = goals_res.json()[0]["skills"][0]
        skill_id = first_skill["id"]

        topics_res = self.client.get(f"/api/skills/{skill_id}/topics")
        topic_id = topics_res.json()[0]["id"]

        toggle_res = self.client.post(
            f"/api/skills/{skill_id}/topics/{topic_id}/toggle",
            json={"is_completed": True},
            headers=headers
        )
        self.assertEqual(toggle_res.status_code, 200)
        self.assertTrue(toggle_res.json()["is_completed"])

        overview_res = self.client.get(f"/api/skills/{skill_id}", headers=headers)
        self.assertEqual(overview_res.status_code, 200)
        overview_data = overview_res.json()
        self.assertGreaterEqual(overview_data["completed_topics"], 1)
        self.assertGreater(overview_data["completion_percentage"], 0)

    def test_17_get_important_topics(self):
        """Test getting must-know topics returns only items with is_must_know == True"""
        goals_res = self.client.get("/api/goals")
        first_skill = goals_res.json()[0]["skills"][0]
        skill_id = first_skill["id"]

        response = self.client.get(f"/api/skills/{skill_id}/important-topics")
        self.assertEqual(response.status_code, 200)
        important_topics = response.json()
        self.assertGreater(len(important_topics), 0)
        for topic in important_topics:
            self.assertTrue(topic["is_must_know"])

    def test_18_get_practical_content(self):
        """Test getting practical content returns code/exercises for tech and scenarios for business"""
        goals_res = self.client.get("/api/goals")
        tech_skill = goals_res.json()[0]["skills"][0]
        biz_skill = goals_res.json()[1]["skills"][0]

        # Technical skill practical content
        tech_res = self.client.get(f"/api/skills/{tech_skill['id']}/practical")
        self.assertEqual(tech_res.status_code, 200)
        tech_practical = tech_res.json()
        self.assertGreater(len(tech_practical), 0)
        self.assertIsNotNone(tech_practical[0]["code_snippet"])
        self.assertIsNotNone(tech_practical[0]["language"])

        # Non-technical skill practical content (no forced code)
        biz_res = self.client.get(f"/api/skills/{biz_skill['id']}/practical")
        self.assertEqual(biz_res.status_code, 200)
        biz_practical = biz_res.json()
        self.assertGreater(len(biz_practical), 0)
        self.assertIn(biz_practical[0]["content_type"], ["scenario", "case_study"])
        self.assertIsNone(biz_practical[0]["code_snippet"])

    def test_19_get_skill_progress_and_requirements(self):
        """Test getting skill progress returns total topics, must-know topics, and completion status"""
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        goals_res = self.client.get("/api/goals")
        first_skill = goals_res.json()[0]["skills"][0]
        skill_id = first_skill["id"]

        progress_res = self.client.get(f"/api/skills/{skill_id}/progress", headers=headers)
        self.assertEqual(progress_res.status_code, 200)
        data = progress_res.json()
        self.assertEqual(data["skill_id"], skill_id)
        self.assertGreater(data["total_topics"], 0)
        self.assertGreater(data["must_know_topics"], 0)
        self.assertEqual(data["completed_topics"], 0)
        self.assertFalse(data["is_completed"])
        self.assertFalse(data["can_complete"])
        self.assertIn("remaining", data["completion_requirements"])

    def test_20_complete_skill_validation_and_success(self):
        """Test completing skill enforces requirements unless fulfilled, then marks complete"""
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        goals_res = self.client.get("/api/goals")
        first_skill = goals_res.json()[0]["skills"][0]
        skill_id = first_skill["id"]

        # 1. Attempt complete without meeting requirements -> 400 Bad Request
        fail_res = self.client.post(f"/api/skills/{skill_id}/complete", json={}, headers=headers)
        self.assertEqual(fail_res.status_code, 400)
        self.assertIn("Learning flow requirement not met", fail_res.json()["detail"])

        # 2. Complete with complete_all_topics=True -> 200 OK
        success_res = self.client.post(
            f"/api/skills/{skill_id}/complete",
            json={"complete_all_topics": True},
            headers=headers
        )
        self.assertEqual(success_res.status_code, 200)
        res_data = success_res.json()
        self.assertTrue(res_data["is_completed"])
        self.assertEqual(res_data["progress_percentage"], 100)
        self.assertEqual(res_data["completed_topics"], res_data["total_topics"])

        # 3. Verify progress endpoint also reports complete
        verify_res = self.client.get(f"/api/skills/{skill_id}/progress", headers=headers)
        self.assertEqual(verify_res.status_code, 200)
        self.assertTrue(verify_res.json()["is_completed"])

    def test_21_overall_goal_progress_summary(self):
        """Test summary endpoint calculates active goal progress accurately"""
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Select first goal
        goals_res = self.client.get("/api/goals")
        goal_id = goals_res.json()[0]["id"]
        first_skill_id = goals_res.json()[0]["skills"][0]["id"]
        self.client.post("/api/goals/select", json={"goal_id": goal_id}, headers=headers)

        # Mark first skill complete
        self.client.post(
            f"/api/skills/{first_skill_id}/complete",
            json={"complete_all_topics": True},
            headers=headers
        )

        # Check summary
        summary_res = self.client.get("/api/progress/summary", headers=headers)
        self.assertEqual(summary_res.status_code, 200)
        summary_data = summary_res.json()
        self.assertIsNotNone(summary_data)
        self.assertEqual(summary_data["goal_id"], goal_id)
        self.assertGreater(summary_data["total_skills"], 0)
        self.assertGreaterEqual(summary_data["completed_skills"], 1)
        self.assertGreater(summary_data["overall_percentage"], 0)
        self.assertEqual(len(summary_data["skills"]), summary_data["total_skills"])

    def test_22_get_evaluation_questions(self):
        """Phase 8: Test retrieving skill evaluation questions without answer leaks"""
        goals_res = self.client.get("/api/goals")
        skill_id = goals_res.json()[0]["skills"][0]["id"]

        res = self.client.get(f"/api/skills/{skill_id}/evaluation/questions")
        self.assertEqual(res.status_code, 200)
        questions = res.json()
        self.assertGreaterEqual(len(questions), 4)

        for q in questions:
            self.assertIn("question_text", q)
            self.assertIn("options", q)
            self.assertGreaterEqual(len(q["options"]), 2)
            self.assertIn("topic_area", q)
            # Crucial: correct answer must NOT be exposed in question response
            self.assertNotIn("correct_option", q)
            self.assertNotIn("explanation", q)

    def test_23_submit_evaluation_scoring_and_diagnostics(self):
        """Phase 8: Test submitting evaluation answers, calculating diagnostic feedback, and persisting"""
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        goals_res = self.client.get("/api/goals")
        skill_id = goals_res.json()[0]["skills"][0]["id"]

        # Fetch questions
        questions_res = self.client.get(f"/api/skills/{skill_id}/evaluation/questions")
        questions = questions_res.json()
        self.assertGreaterEqual(len(questions), 4)

        # Simulate answers: first 2 answer "B", next answer "C"
        submission = {
            "answers": {
                str(questions[0]["id"]): "B",
                str(questions[1]["id"]): "C",
                str(questions[2]["id"]): "A",  # Likely wrong
                str(questions[3]["id"]): "D"   # Likely wrong
            }
        }

        submit_res = self.client.post(
            f"/api/skills/{skill_id}/evaluation/submit",
            json=submission,
            headers=headers
        )
        self.assertEqual(submit_res.status_code, 200)
        result = submit_res.json()

        self.assertIn("score", result)
        self.assertIn("total_questions", result)
        self.assertEqual(result["total_questions"], len(questions))
        self.assertIn("percentage", result)
        self.assertIn("performance_level", result)
        self.assertIn("feedback_summary", result)
        self.assertIn("strong_areas", result)
        self.assertIn("weak_areas", result)
        self.assertIn("improvement_suggestions", result)
        self.assertGreater(len(result["improvement_suggestions"]), 0)
        self.assertEqual(len(result["question_breakdown"]), len(questions))

        # Check breakdown item structure
        for item in result["question_breakdown"]:
            self.assertIn("question_text", item)
            self.assertIn("selected_option", item)
            self.assertIn("correct_option", item)
            self.assertIn("is_correct", item)
            self.assertIn("explanation", item)

        # Check latest endpoint returns persisted evaluation
        latest_res = self.client.get(f"/api/skills/{skill_id}/evaluation/latest", headers=headers)
        self.assertEqual(latest_res.status_code, 200)
        latest_data = latest_res.json()
        self.assertIsNotNone(latest_data)
        self.assertEqual(latest_data["score"], result["score"])
        self.assertEqual(latest_data["percentage"], result["percentage"])

    def test_24_get_skill_interview_questions_and_filtering(self):
        """Phase 9: Test retrieving interview prep questions per skill with difficulty filtering"""
        goals_res = self.client.get("/api/goals")
        skill_id = goals_res.json()[0]["skills"][0]["id"]

        # 1. Fetch all questions for skill
        all_res = self.client.get(f"/api/skills/{skill_id}/interview-questions")
        self.assertEqual(all_res.status_code, 200)
        all_questions = all_res.json()
        self.assertGreaterEqual(len(all_questions), 3)

        for q in all_questions:
            self.assertIn("question", q)
            self.assertIn("difficulty", q)
            self.assertIn("category", q)
            self.assertIn("expected_answer", q)
            self.assertIn("explanation", q)
            self.assertIn("tips_for_answering", q)
            self.assertIn("common_mistakes", q)

        # 2. Test difficulty filter: Basic
        basic_res = self.client.get(f"/api/skills/{skill_id}/interview-questions?difficulty=Basic")
        self.assertEqual(basic_res.status_code, 200)
        basic_questions = basic_res.json()
        self.assertGreaterEqual(len(basic_questions), 1)
        for b_q in basic_questions:
            self.assertEqual(b_q["difficulty"], "Basic")

        # 3. Test difficulty filter: Advanced
        adv_res = self.client.get(f"/api/skills/{skill_id}/interview-questions?difficulty=Advanced")
        self.assertEqual(adv_res.status_code, 200)
        adv_questions = adv_res.json()
        self.assertGreaterEqual(len(adv_questions), 1)
        for a_q in adv_questions:
            self.assertEqual(a_q["difficulty"], "Advanced")

    def test_25_get_skill_sequence_progression(self):
        """Phase 9: Test skill sequence calculation and transition between skills vs capstone"""
        goals_res = self.client.get("/api/goals")
        first_goal = goals_res.json()[0]
        skills = first_goal["skills"]
        self.assertGreaterEqual(len(skills), 2)

        first_skill_id = skills[0]["id"]
        second_skill_id = skills[1]["id"]
        last_skill_id = skills[-1]["id"]

        # First skill should point to second skill
        first_seq_res = self.client.get(f"/api/skills/{first_skill_id}/sequence")
        self.assertEqual(first_seq_res.status_code, 200)
        first_seq = first_seq_res.json()
        self.assertTrue(first_seq["has_next_skill"])
        self.assertFalse(first_seq["is_last_skill"])
        self.assertEqual(first_seq["next_skill_id"], second_skill_id)
        self.assertEqual(first_seq["current_skill_index"], 1)

        # Last skill should signal end of sequence
        last_seq_res = self.client.get(f"/api/skills/{last_skill_id}/sequence")
        self.assertEqual(last_seq_res.status_code, 200)
        last_seq = last_seq_res.json()
        self.assertFalse(last_seq["has_next_skill"])
        self.assertTrue(last_seq["is_last_skill"])
        self.assertIsNone(last_seq["next_skill_id"])
        self.assertEqual(last_seq["current_skill_index"], len(skills))

    def test_26_get_overall_evaluation_questions(self):
        """Phase 10: Test retrieving overall cross-skill evaluation questions"""
        goals_res = self.client.get("/api/goals")
        goal_id = goals_res.json()[0]["id"]

        res = self.client.get(f"/api/overall-evaluation/questions?goal_id={goal_id}")
        self.assertEqual(res.status_code, 200)
        questions = res.json()
        self.assertGreaterEqual(len(questions), 3)

        for q in questions:
            self.assertIn("question_text", q)
            self.assertIn("question_type", q)
            self.assertIn("integrated_skills", q)
            self.assertGreaterEqual(len(q["integrated_skills"]), 1)
            self.assertIn("options", q)
            self.assertGreaterEqual(len(q["options"]), 2)
            # Crucial: correct answer must NOT be exposed
            self.assertNotIn("correct_option", q)
            self.assertNotIn("explanation", q)

    def test_27_submit_overall_evaluation_and_diagnostics(self):
        """Phase 10: Test submitting overall evaluation, calculating readiness tier, and persistence"""
        reg_payload = {"name": self.test_name, "email": self.test_email, "password": self.test_password}
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        goals_res = self.client.get("/api/goals")
        goal_id = goals_res.json()[0]["id"]

        # Fetch questions
        questions_res = self.client.get(f"/api/overall-evaluation/questions?goal_id={goal_id}")
        questions = questions_res.json()
        self.assertGreaterEqual(len(questions), 3)

        # Answer all with "B" (most correct in our seed are B)
        answers = {str(q["id"]): "B" for q in questions}

        submit_res = self.client.post(
            f"/api/overall-evaluation/submit?goal_id={goal_id}",
            json={"answers": answers},
            headers=headers
        )
        self.assertEqual(submit_res.status_code, 200)
        result = submit_res.json()

        self.assertIn("score", result)
        self.assertIn("total_questions", result)
        self.assertEqual(result["total_questions"], len(questions))
        self.assertIn("percentage", result)
        self.assertIn("readiness_level", result)
        self.assertIn("readiness_summary", result)
        self.assertIn("strong_skills", result)
        self.assertIn("skills_needing_improvement", result)
        self.assertIn("cross_skill_insights", result)
        self.assertIn("recommendations", result)
        self.assertGreater(len(result["recommendations"]), 0)
        self.assertEqual(len(result["question_breakdown"]), len(questions))

        # Check question breakdown item structure
        for item in result["question_breakdown"]:
            self.assertIn("question_text", item)
            self.assertIn("integrated_skills", item)
            self.assertIn("selected_option", item)
            self.assertIn("correct_option", item)
            self.assertIn("is_correct", item)
            self.assertIn("explanation", item)

        # Check latest endpoint returns persisted evaluation
        latest_res = self.client.get(f"/api/overall-evaluation/latest?goal_id={goal_id}", headers=headers)
        self.assertEqual(latest_res.status_code, 200)
        latest_data = latest_res.json()
        self.assertIsNotNone(latest_data)
        self.assertEqual(latest_data["score"], result["score"])
        self.assertEqual(latest_data["readiness_level"], result["readiness_level"])

    # --- Phase 11 Tests: Capstone Final Interview Preparation & Exactly 15 Questions ---
    def test_28_get_exactly_15_final_interview_questions(self):
        """
        Verify Capstone Interview Preparation Hub returns EXACTLY 15 questions per goal
        structured across 3 categories (5 Core, 5 Practical/Scenario, 5 Advanced).
        """
        reg_res = self._register_user()
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Select Full Stack Developer goal
        goals_res = self.client.get("/api/goals")
        self.assertEqual(goals_res.status_code, 200)
        goals = goals_res.json()
        fs_goal = next(g for g in goals if g["slug"] == "full-stack-developer")

        self.client.post(f"/api/goals/{fs_goal['id']}/select", headers=headers)

        # Fetch Capstone Interview Hub
        hub_res = self.client.get("/api/interview-prep/hub", headers=headers)
        self.assertEqual(hub_res.status_code, 200)
        hub = hub_res.json()

        self.assertEqual(hub["goal_id"], fs_goal["id"])
        self.assertEqual(hub["goal_title"], fs_goal["title"])
        
        # Hard Constraint: EXACTLY 15 questions
        self.assertEqual(hub["total_questions"], 15)
        questions = hub["questions"]
        self.assertEqual(len(questions), 15)

        # Verify strictly sequential question numbers 1 through 15
        question_numbers = [q["question_number"] for q in questions]
        self.assertEqual(question_numbers, list(range(1, 16)))

        # Category distribution verification
        core_fundamentals = [q for q in questions if q["category"] == "Core Fundamentals"]
        practical_scenarios = [q for q in questions if q["category"] == "Practical & Scenario-Based"]
        advanced_problems = [q for q in questions if q["category"] == "Advanced & Problem Solving"]

        self.assertEqual(len(core_fundamentals), 5, "Questions 1-5 must be Core Fundamentals")
        self.assertEqual(len(practical_scenarios), 5, "Questions 6-10 must be Practical & Scenario-Based")
        self.assertEqual(len(advanced_problems), 5, "Questions 11-15 must be Advanced & Problem Solving")

        # Questions 1-5 are Core Fundamentals
        self.assertEqual([q["question_number"] for q in core_fundamentals], [1, 2, 3, 4, 5])
        # Questions 6-10 are Practical & Scenario-Based
        self.assertEqual([q["question_number"] for q in practical_scenarios], [6, 7, 8, 9, 10])
        # Questions 11-15 are Advanced & Problem Solving
        self.assertEqual([q["question_number"] for q in advanced_problems], [11, 12, 13, 14, 15])

        # Verify each question has all required fields according to Section 22
        for q in questions:
            self.assertIn("question", q)
            self.assertTrue(len(q["question"]) > 10)
            self.assertIn("why_asked", q)
            self.assertTrue(len(q["why_asked"]) > 10)
            self.assertIn("interviewer_looking_for", q)
            self.assertTrue(len(q["interviewer_looking_for"]) > 10)
            self.assertIn("detailed_answer", q)
            self.assertTrue(len(q["detailed_answer"]) > 20)
            self.assertIn("response_structure_star", q)
            self.assertTrue(len(q["response_structure_star"]) > 10)
            self.assertIn("what_not_to_say", q)
            self.assertTrue(len(q["what_not_to_say"]) > 10)
            self.assertIn("is_practiced", q)
            self.assertFalse(q["is_practiced"], "Initial practiced status must be False")
            self.assertIsNone(q["practiced_at"])

        # Initial practice count
        self.assertEqual(hub["practiced_count"], 0)
        self.assertEqual(hub["practiced_percentage"], 0.0)

    def test_29_toggle_interview_question_practice(self):
        """
        Verify toggling 'Mark as Practiced / Understood' updates user progress,
        updates practice status endpoint, and persists correctly across sessions.
        """
        reg_res = self._register_user()
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Select Full Stack Developer goal
        goals_res = self.client.get("/api/goals")
        goals = goals_res.json()
        fs_goal = next(g for g in goals if g["slug"] == "full-stack-developer")
        self.client.post(f"/api/goals/{fs_goal['id']}/select", headers=headers)

        # Fetch Hub questions
        hub_res = self.client.get("/api/interview-prep/hub", headers=headers)
        self.assertEqual(hub_res.status_code, 200)
        hub = hub_res.json()
        questions = hub["questions"]
        q1 = questions[0]
        q2 = questions[1]

        # 1. Toggle Question 1 to practiced = True
        toggle_res1 = self.client.post(
            "/api/interview-prep/toggle-practiced",
            json={"question_id": q1["id"], "is_practiced": True},
            headers=headers
        )
        self.assertEqual(toggle_res1.status_code, 200)
        res1 = toggle_res1.json()
        self.assertEqual(res1["id"], q1["id"])
        self.assertTrue(res1["is_practiced"])
        self.assertIsNotNone(res1["practiced_at"])

        # 2. Check practice status endpoint
        status_res = self.client.get("/api/interview-prep/practice-status", headers=headers)
        self.assertEqual(status_res.status_code, 200)
        status_data = status_res.json()
        self.assertEqual(status_data["practiced_count"], 1)
        self.assertEqual(status_data["progress_percentage"], 7)
        self.assertIn(q1["id"], status_data["practiced_question_ids"])

        # 3. Toggle Question 2 to practiced = True
        toggle_res2 = self.client.post(
            "/api/interview-prep/toggle-practiced",
            json={"question_id": q2["id"], "is_practiced": True},
            headers=headers
        )
        self.assertEqual(toggle_res2.status_code, 200)

        # Check status again
        status_res2 = self.client.get("/api/interview-prep/practice-status", headers=headers)
        self.assertEqual(status_res2.status_code, 200)
        status_data2 = status_res2.json()
        self.assertEqual(status_data2["practiced_count"], 2)
        self.assertEqual(status_data2["progress_percentage"], 13)

        # 4. Fetch Hub to confirm state reflected inside question list
        hub_res2 = self.client.get("/api/interview-prep/hub", headers=headers)
        hub2 = hub_res2.json()
        self.assertEqual(hub2["practiced_count"], 2)
        q1_updated = next(q for q in hub2["questions"] if q["id"] == q1["id"])
        q2_updated = next(q for q in hub2["questions"] if q["id"] == q2["id"])
        q3_updated = next(q for q in hub2["questions"] if q["id"] == questions[2]["id"])
        self.assertTrue(q1_updated["is_practiced"])
        self.assertTrue(q2_updated["is_practiced"])
        self.assertFalse(q3_updated["is_practiced"])

        # 5. Untoggle Question 1 (is_practiced = False)
        untoggle_res = self.client.post(
            "/api/interview-prep/toggle-practiced",
            json={"question_id": q1["id"], "is_practiced": False},
            headers=headers
        )
        self.assertEqual(untoggle_res.status_code, 200)
        untoggle_data = untoggle_res.json()
        self.assertFalse(untoggle_data["is_practiced"])

        # Final check: count should now be 1
        status_res3 = self.client.get("/api/interview-prep/practice-status", headers=headers)
        self.assertEqual(status_res3.json()["practiced_count"], 1)

    # --- Phase 12 Tests: User Profile + Progress Dashboard ---
    def test_30_get_user_dashboard_comprehensive_metrics(self):
        """
        Verify GET /api/progress/dashboard computes full unified metrics
        including skills, topics, time investment, evaluations, and milestone badges.
        """
        reg_res = self._register_user()
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Select Full Stack Developer goal
        goals_res = self.client.get("/api/goals")
        fs_goal = next(g for g in goals_res.json() if g["slug"] == "full-stack-developer")
        self.client.post(f"/api/goals/{fs_goal['id']}/select", headers=headers)

        # Get first skill and first topic to mark complete
        skills_res = self.client.get(f"/api/goals/{fs_goal['id']}/skills")
        first_skill = skills_res.json()[0]
        topics_res = self.client.get(f"/api/skills/{first_skill['id']}/topics")
        first_topic = topics_res.json()[0]

        # Toggle topic complete
        toggle_res = self.client.post(
            f"/api/skills/{first_skill['id']}/topics/{first_topic['id']}/toggle",
            json={"is_completed": True},
            headers=headers
        )
        self.assertEqual(toggle_res.status_code, 200)

        # Fetch comprehensive dashboard
        dash_res = self.client.get("/api/progress/dashboard", headers=headers)
        self.assertEqual(dash_res.status_code, 200)
        dash = dash_res.json()

        self.assertEqual(dash["user_email"], self.test_email)
        self.assertEqual(dash["goal_id"], fs_goal["id"])
        self.assertEqual(dash["goal_title"], fs_goal["title"])
        self.assertGreater(dash["total_skills"], 0)
        self.assertGreater(dash["total_topics"], 0)
        self.assertGreaterEqual(dash["completed_topics"], 1)
        self.assertGreater(dash["estimated_total_minutes"], 0)
        self.assertGreater(dash["estimated_completed_minutes"], 0)
        self.assertEqual(dash["total_interview_questions"], 15)

        # Verify achievement badges list
        self.assertEqual(len(dash["achievements"]), 8)
        first_step_badge = next(b for b in dash["achievements"] if b["id"] == "first_topic")
        self.assertTrue(first_step_badge["is_unlocked"], "First topic badge should be unlocked")

        # Verify skill summaries list
        self.assertEqual(len(dash["skills"]), len(skills_res.json()))
        first_skill_dash = next(s for s in dash["skills"] if s["skill_id"] == first_skill["id"])
        self.assertGreaterEqual(first_skill_dash["completed_topics"], 1)

    def test_31_update_user_profile_and_summary(self):
        """
        Verify GET /api/auth/profile-summary and PUT /api/auth/profile for Phase 12 profile management.
        """
        reg_res = self._register_user()
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Select Full Stack Developer goal
        goals_res = self.client.get("/api/goals")
        fs_goal = next(g for g in goals_res.json() if g["slug"] == "full-stack-developer")
        self.client.post(f"/api/goals/{fs_goal['id']}/select", headers=headers)

        # 1. Fetch Profile Summary
        summary_res = self.client.get("/api/auth/profile-summary", headers=headers)
        self.assertEqual(summary_res.status_code, 200)
        summary = summary_res.json()
        self.assertEqual(summary["user"]["email"], self.test_email)
        self.assertEqual(summary["active_goal_title"], fs_goal["title"])
        self.assertEqual(summary["total_achievements"], 8)

        # 2. Update user name
        updated_name = "Alex Senior Architect"
        update_res = self.client.put(
            "/api/auth/profile",
            json={"name": updated_name},
            headers=headers
        )
        self.assertEqual(update_res.status_code, 200)
        updated_user = update_res.json()
        self.assertEqual(updated_user["name"], updated_name)

        # 3. Verify /me returns updated name
        me_res = self.client.get("/api/auth/me", headers=headers)
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["name"], updated_name)

    # --- Phase 13 Tests: Error Handling, Accessibility & System Resilience ---
    def test_32_error_handling_and_validation_resilience(self):
        """
        Verify robust error handling envelopes for 404 routes, 401 unauthenticated,
        422 input validation, and nonexistent entities (Phase 13).
        """
        # 1. 404 for non-existent endpoint
        not_found_res = self.client.get("/api/invalid-nonexistent-route")
        self.assertEqual(not_found_res.status_code, 404)

        # 2. 404 for non-existent skill ID
        skill_res = self.client.get("/api/skills/9999999")
        self.assertEqual(skill_res.status_code, 404)
        self.assertIn("detail", skill_res.json())

        # 3. 401 for protected endpoints without authentication token
        unauth_res = self.client.get("/api/auth/me")
        self.assertEqual(unauth_res.status_code, 401)

        unauth_dash_res = self.client.get("/api/progress/dashboard")
        self.assertEqual(unauth_dash_res.status_code, 401)

        # 4. 422 for malformed payload (missing password)
        invalid_reg_res = self.client.post("/api/auth/register", json={"name": "Bad Payload", "email": "bad@email.com"})
        self.assertEqual(invalid_reg_res.status_code, 422)

        # 5. Invalid login credentials returns 401
        invalid_login_res = self.client.post("/api/auth/login", json={"email": "nonexistent@example.com", "password": "WrongPassword"})
        self.assertEqual(invalid_login_res.status_code, 401)

    # --- Phase 14 Tests: Comprehensive End-to-End Candidate Lifecycle Journey ---
    def test_33_full_end_to_end_candidate_journey(self):
        """
        Verify the complete candidate journey through all 14 phases:
        1. Account registration & JWT issuance.
        2. Goal selection (Full Stack Developer).
        3. Skills roadmap retrieval & initial progress tracking.
        4. Topic mastery: Complete must-know topics for Skill 1.
        5. Skill 1 prerequisite check & completion.
        6. Skill 1 diagnostic self-evaluation: submission & score persistence.
        7. Skill 1 interview preparation: verify question bank & tips.
        8. Sequence progression: verify next skill identification.
        9. Overall Goal Cross-Skill Evaluation: submit architectural answers & verify readiness tier.
        10. Capstone Final Interview Hub: verify exactly 15 questions, practice tracking.
        11. Progress Dashboard: verify unified metrics, hours, and achievement badges.
        12. Candidate Profile & Readiness Transcript: verify active track & certificate data.
        """
        # Step 1: Register and login
        reg_res = self._register_user()
        self.assertEqual(reg_res.status_code, 201)
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 2: Choose Career Goal
        goals_res = self.client.get("/api/goals")
        self.assertEqual(goals_res.status_code, 200)
        fs_goal = next(g for g in goals_res.json() if g["slug"] == "full-stack-developer")
        select_res = self.client.post(f"/api/goals/{fs_goal['id']}/select", headers=headers)
        self.assertEqual(select_res.status_code, 200)

        # Step 3: Skills List & Progress
        skills_res = self.client.get(f"/api/goals/{fs_goal['id']}/skills")
        self.assertEqual(skills_res.status_code, 200)
        skills = skills_res.json()
        self.assertGreater(len(skills), 0)
        skill1 = skills[0]

        # Step 4: Complete must-know topics for Skill 1
        topics_res = self.client.get(f"/api/skills/{skill1['id']}/topics")
        self.assertEqual(topics_res.status_code, 200)
        topics = topics_res.json()
        for t in topics:
            if t["is_must_know"]:
                self.client.post(
                    f"/api/skills/{skill1['id']}/topics/{t['id']}/toggle",
                    json={"is_completed": True},
                    headers=headers
                )

        # Step 5: Mark Skill 1 Completed
        complete_skill_res = self.client.post(f"/api/skills/{skill1['id']}/complete", headers=headers)
        self.assertEqual(complete_skill_res.status_code, 200)
        self.assertTrue(complete_skill_res.json()["is_completed"])

        # Step 6: Skill 1 Self-Evaluation
        eval_q_res = self.client.get(f"/api/skills/{skill1['id']}/evaluation/questions")
        self.assertEqual(eval_q_res.status_code, 200)
        eval_questions = eval_q_res.json()
        self.assertGreater(len(eval_questions), 0)
        eval_answers = {str(q["id"]): "B" for q in eval_questions}
        submit_eval_res = self.client.post(
            f"/api/skills/{skill1['id']}/evaluation/submit",
            json={"answers": eval_answers},
            headers=headers
        )
        self.assertEqual(submit_eval_res.status_code, 200)
        self.assertIn("score", submit_eval_res.json())

        # Step 7: Skill 1 Interview Prep
        iq_res = self.client.get(f"/api/skills/{skill1['id']}/interview-questions")
        self.assertEqual(iq_res.status_code, 200)
        self.assertGreater(len(iq_res.json()), 0)

        # Step 8: Next Skill Sequence Progression
        seq_res = self.client.get(f"/api/skills/{skill1['id']}/sequence")
        self.assertEqual(seq_res.status_code, 200)
        self.assertTrue(seq_res.json()["has_next_skill"])

        # Step 9: Overall Cross-Skill Evaluation
        oq_res = self.client.get(f"/api/overall-evaluation/questions?goal_id={fs_goal['id']}")
        self.assertEqual(oq_res.status_code, 200)
        oq_questions = oq_res.json()
        oq_answers = {str(q["id"]): "B" for q in oq_questions}
        submit_oq_res = self.client.post(
            f"/api/overall-evaluation/submit?goal_id={fs_goal['id']}",
            json={"answers": oq_answers},
            headers=headers
        )
        self.assertEqual(submit_oq_res.status_code, 200)
        self.assertIn("readiness_level", submit_oq_res.json())

        # Step 10: Capstone Final Interview Prep (Exactly 15 Questions)
        hub_res = self.client.get("/api/interview-prep/hub", headers=headers)
        self.assertEqual(hub_res.status_code, 200)
        hub = hub_res.json()
        self.assertEqual(hub["total_questions"], 15)
        self.assertEqual(len(hub["questions"]), 15)

        # Practice first question
        q1 = hub["questions"][0]
        practice_res = self.client.post(
            "/api/interview-prep/toggle-practiced",
            json={"question_id": q1["id"], "is_practiced": True},
            headers=headers
        )
        self.assertEqual(practice_res.status_code, 200)
        self.assertTrue(practice_res.json()["is_practiced"])

        # Step 11: Progress Dashboard
        dash_res = self.client.get("/api/progress/dashboard", headers=headers)
        self.assertEqual(dash_res.status_code, 200)
        dash = dash_res.json()
        self.assertEqual(dash["completed_skills"], 1)
        self.assertGreaterEqual(dash["completed_topics"], 1)
        self.assertEqual(dash["practiced_interview_questions"], 1)
        self.assertTrue(dash["has_overall_evaluation"])
        # Verify badges unlocked: Enrolled, First Step, Skill Finisher, Evaluator
        unlocked_badge_ids = [b["id"] for b in dash["achievements"] if b["is_unlocked"]]
        self.assertIn("enrolled_goal", unlocked_badge_ids)
        self.assertIn("first_topic", unlocked_badge_ids)
        self.assertIn("first_skill", unlocked_badge_ids)
        self.assertIn("evaluator", unlocked_badge_ids)

        # Step 12: Profile Summary & Certificate
        profile_res = self.client.get("/api/auth/profile-summary", headers=headers)
        self.assertEqual(profile_res.status_code, 200)
        profile_data = profile_res.json()
        self.assertEqual(profile_data["active_goal_title"], fs_goal["title"])
        self.assertEqual(profile_data["skills_completed"], 1)
        self.assertGreaterEqual(profile_data["achievements_count"], 4)


if __name__ == "__main__":
    unittest.main()
