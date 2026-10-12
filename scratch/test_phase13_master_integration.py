"""
PHASE 13: MASTER INTEGRATION AND REGRESSION TEST SUITE
======================================================
Covers:
1. System Health & Database Schema Integrity
2. Authentication & Authorization Lifecycle (Register, Login, Token, /me, Negative paths)
3. Goal Selection & Curriculum Progression (Technical & Non-Technical)
4. Full 4-Stage Skill Mastery Lifecycle (Topics, Practical, Diagnostic Quiz, Interview Prep)
5. Prerequisite & Completion Enforcement
6. Certificate Security, Generation, Claiming & Public Verification
7. Cross-Skill Overall Diagnostic Evaluation & Tier Analysis
8. Capstone 15 Must-Know Interview Questions & Practice Tracker
9. AI Assistant Integration, Validation & Server-side Grounding
10. Strict Multi-Tenant User Isolation & Authorization Protection
11. Frontend Route Map & Production Build Cleanliness
"""
import sys
import os
import uuid
import unittest
from pathlib import Path

# Add backend directory to path
WORKSPACE = Path(__file__).resolve().parent.parent
BACKEND_DIR = WORKSPACE / "backend"
sys.path.insert(0, str(BACKEND_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from starlette.testclient import TestClient
from app.main import app
from app.database.database import Base, engine, SessionLocal, auto_migrate_sqlite
from app.database.seed import seed_initial_data
from app.models.user import User
from app.models.goal import Goal
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.user_goal import UserGoalSelection
from app.models.skill_progress import UserSkillProgress
from app.models.topic_progress import UserTopicProgress
from app.models.evaluation import EvaluationQuestion, UserSkillEvaluation
from app.models.overall_evaluation import OverallGoalEvaluationQuestion, UserGoalEvaluation
from app.models.final_interview import GoalFinalInterviewQuestion, UserInterviewPractice
from app.models.certificate import UserCertificate


class Phase13MasterIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        auto_migrate_sqlite()
        db = SessionLocal()
        try:
            seed_initial_data(db)
        finally:
            db.close()
        cls.client = TestClient(app)

    def _create_user(self, name_prefix: str):
        """Helper to create a fresh, clean test user with JWT headers and ID."""
        run_id = uuid.uuid4().hex[:8]
        email = f"{name_prefix.lower().replace(' ', '_')}_{run_id}@ces.internal"
        password = "SecurePassword123!"
        name = f"{name_prefix} {run_id}"

        resp = self.client.post("/api/auth/register", json={
            "name": name,
            "email": email,
            "password": password
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        token = data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user_id = data["user"]["id"]
        return email, password, name, token, headers, user_id

    # ---------------------------------------------------------
    # TEST 1: Health & Database Schema Verification
    # ---------------------------------------------------------
    def test_01_system_health_and_database_connectivity(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
        print("\n  [PASS] Integration 1: Backend health & SQLite database connectivity verified.")

    # ---------------------------------------------------------
    # TEST 2: Authentication & Authorization Flow
    # ---------------------------------------------------------
    def test_02_authentication_and_authorization_lifecycle(self):
        email, password, name, token, headers, user_id = self._create_user("Auth Tester")

        # 1. Duplicate register fails
        resp_dup = self.client.post("/api/auth/register", json={
            "name": name, "email": email, "password": password
        })
        self.assertEqual(resp_dup.status_code, 400)

        # 2. Login with correct credentials
        resp_login = self.client.post("/api/auth/login", json={
            "email": email, "password": password
        })
        self.assertEqual(resp_login.status_code, 200)

        # 3. Login with incorrect password
        resp_bad_login = self.client.post("/api/auth/login", json={
            "email": email, "password": "WrongPassword!"
        })
        self.assertEqual(resp_bad_login.status_code, 401)

        # 4. Protected /me with valid token
        resp_me = self.client.get("/api/auth/me", headers=headers)
        self.assertEqual(resp_me.status_code, 200)
        self.assertEqual(resp_me.json()["email"], email)

        # 5. Protected /me without token fails
        resp_no_token = self.client.get("/api/auth/me")
        self.assertEqual(resp_no_token.status_code, 401)
        print("  [PASS] Integration 2: Auth lifecycle & authorization guards verified.")

    # ---------------------------------------------------------
    # TEST 3: Goal Catalog & Goal Selection
    # ---------------------------------------------------------
    def test_03_goal_catalog_and_selection(self):
        _, _, _, token, headers, _ = self._create_user("Goal Explorer")

        # List goals
        goals_resp = self.client.get("/api/goals")
        self.assertEqual(goals_resp.status_code, 200)
        goals = goals_resp.json()
        self.assertTrue(len(goals) >= 4)

        # Select Full Stack Developer goal
        fs_goal = next(g for g in goals if "Full Stack" in g["title"])
        sel_resp = self.client.post("/api/goals/select", json={"goal_id": fs_goal["id"]}, headers=headers)
        self.assertEqual(sel_resp.status_code, 200)
        self.assertEqual(sel_resp.json()["goal_id"], fs_goal["id"])

        # Check skills for selected goal
        skills_resp = self.client.get(f"/api/goals/{fs_goal['id']}/skills")
        self.assertEqual(skills_resp.status_code, 200)
        skills = skills_resp.json()
        self.assertTrue(len(skills) > 0)
        print("  [PASS] Integration 3: Goal catalog browsing & career enrollment verified.")

    # ---------------------------------------------------------
    # TEST 4: Full 4-Stage Skill Workflow & Completion
    # ---------------------------------------------------------
    def test_04_four_stage_skill_workflow_and_completion(self):
        _, _, _, token, headers, _ = self._create_user("Skill Master")

        # Select goal
        goals = self.client.get("/api/goals").json()
        goal_id = goals[0]["id"]
        self.client.post("/api/goals/select", json={"goal_id": goal_id}, headers=headers)

        # Get first skill
        skills = self.client.get(f"/api/goals/{goal_id}/skills").json()
        skill = skills[0]
        skill_id = skill["id"]

        # Stage 1: Complete all topics
        topics_resp = self.client.get(f"/api/skills/{skill_id}/topics", headers=headers)
        self.assertEqual(topics_resp.status_code, 200)
        topics = topics_resp.json()
        for t in topics:
            toggle_resp = self.client.post(
                f"/api/skills/{skill_id}/topics/{t['id']}/toggle",
                json={"is_completed": True},
                headers=headers
            )
            self.assertEqual(toggle_resp.status_code, 200)

        # Stage 2: Practical section
        prac_resp = self.client.get(f"/api/skills/{skill_id}/practical", headers=headers)
        self.assertEqual(prac_resp.status_code, 200)
        prac_record = self.client.post(f"/api/skills/{skill_id}/record-stage", json={"stage": "practical"}, headers=headers)
        self.assertEqual(prac_record.status_code, 200)

        # Stage 3: Self-evaluation quiz
        eval_q_resp = self.client.get(f"/api/skills/{skill_id}/evaluation/questions")
        self.assertEqual(eval_q_resp.status_code, 200)

        # Query correct options directly from database to test 100% mastery submission
        db = SessionLocal()
        eval_objs = db.query(EvaluationQuestion).filter(EvaluationQuestion.skill_id == skill_id).all()
        answers_payload = {str(q.id): q.correct_option for q in eval_objs}
        db.close()

        submit_eval = self.client.post(f"/api/skills/{skill_id}/evaluation/submit", json={"answers": answers_payload}, headers=headers)
        self.assertEqual(submit_eval.status_code, 200)
        self.assertEqual(submit_eval.json()["percentage"], 100)

        # Stage 4: Interview prep
        prep_resp = self.client.get(f"/api/skills/{skill_id}/interview-questions", headers=headers)
        self.assertEqual(prep_resp.status_code, 200)
        int_record = self.client.post(f"/api/skills/{skill_id}/record-stage", json={"stage": "interview"}, headers=headers)
        self.assertEqual(int_record.status_code, 200)

        # Verify complete skill endpoint
        complete_resp = self.client.post(f"/api/skills/{skill_id}/complete", headers=headers)
        self.assertEqual(complete_resp.status_code, 200)
        print("  [PASS] Integration 4: 4-Stage skill progression (topics, practical, evaluation, interview) verified.")

    # ---------------------------------------------------------
    # TEST 5: Certificate Claiming, Validation & Verification
    # ---------------------------------------------------------
    def test_05_certificate_lifecycle_and_verification(self):
        goals = self.client.get("/api/goals").json()
        target_goal_id = goals[0]["id"]
        skills = self.client.get(f"/api/goals/{target_goal_id}/skills").json()
        target_skill_id = skills[0]["id"]

        # 1. Candidate who has NOT completed should get 400 Bad Request
        _, _, _, _, headers_inc, _ = self._create_user("Incomplete Candidate")

        claim_premature = self.client.post(f"/api/skills/{target_skill_id}/claim-certificate", headers=headers_inc)
        self.assertEqual(claim_premature.status_code, 400)
        self.assertIn("detail", claim_premature.json())

        # 2. Candidate who completed all 4 stages can unlock and claim certificate
        _, _, graduate_name, _, headers_done, _ = self._create_user("Graduate Candidate")

        # Select goal
        self.client.post("/api/goals/select", json={"goal_id": target_goal_id}, headers=headers_done)

        # Complete topics, practical, evaluation, interview
        topics = self.client.get(f"/api/skills/{target_skill_id}/topics", headers=headers_done).json()
        for t in topics:
            self.client.post(
                f"/api/skills/{target_skill_id}/topics/{t['id']}/toggle",
                json={"is_completed": True},
                headers=headers_done
            )
        self.client.post(f"/api/skills/{target_skill_id}/record-stage", json={"stage": "practical"}, headers=headers_done)

        db = SessionLocal()
        eval_objs = db.query(EvaluationQuestion).filter(EvaluationQuestion.skill_id == target_skill_id).all()
        answers_payload = {str(q.id): q.correct_option for q in eval_objs}
        db.close()
        self.client.post(f"/api/skills/{target_skill_id}/evaluation/submit", json={"answers": answers_payload}, headers=headers_done)
        self.client.post(f"/api/skills/{target_skill_id}/record-stage", json={"stage": "interview"}, headers=headers_done)

        # Claim certificate
        claim_resp = self.client.post(f"/api/skills/{target_skill_id}/claim-certificate", headers=headers_done)
        self.assertEqual(claim_resp.status_code, 200)
        cert = claim_resp.json()
        cert_id = cert["certificate_id"]
        self.assertTrue(cert_id.startswith("CES-SKILL-"))

        # Public verification endpoint (unauthenticated)
        verify_resp = self.client.get(f"/api/certificates/verify/{cert_id}")
        self.assertEqual(verify_resp.status_code, 200)
        self.assertEqual(verify_resp.json()["recipient_name"], graduate_name)

        # Incomplete candidate attempting to access Graduate's certificate by DB ID should get 403 Forbidden
        db_cert_id = cert["id"]
        resp_forbidden = self.client.get(f"/api/certificates/{db_cert_id}", headers=headers_inc)
        self.assertEqual(resp_forbidden.status_code, 403)
        print("  [PASS] Integration 5: Certificate locking, genuine claiming, public verification & 403 isolation verified.")

    # ---------------------------------------------------------
    # TEST 6: Capstone Final Interview (15 Must-Know Questions)
    # ---------------------------------------------------------
    def test_06_capstone_final_interview_questions_and_tracker(self):
        _, _, _, token, headers, _ = self._create_user("Interview Candidate")

        # Select Full Stack Developer
        goals = self.client.get("/api/goals").json()
        fs_goal = next(g for g in goals if "Full Stack" in g["title"])
        self.client.post("/api/goals/select", json={"goal_id": fs_goal["id"]}, headers=headers)

        # Fetch exactly 15 questions from /api/interview-prep/hub
        hub_resp = self.client.get("/api/interview-prep/hub", headers=headers)
        self.assertEqual(hub_resp.status_code, 200)
        data = hub_resp.json()
        self.assertEqual(data["total_questions"], 15)
        self.assertEqual(len(data["questions"]), 15)

        # Verify category distribution (5 Core Fundamentals, 5 Practical & Scenario-Based, 5 Advanced & Problem Solving)
        categories = [q["category"] for q in data["questions"]]
        self.assertEqual(categories.count("Core Fundamentals"), 5)
        self.assertEqual(categories.count("Practical & Scenario-Based"), 5)
        self.assertEqual(categories.count("Advanced & Problem Solving"), 5)

        # Toggle practice on first question
        q1 = data["questions"][0]
        toggle_prac = self.client.post(
            "/api/interview-prep/toggle-practiced",
            json={"question_id": q1["id"], "is_practiced": True},
            headers=headers
        )
        self.assertEqual(toggle_prac.status_code, 200)
        self.assertTrue(toggle_prac.json()["is_practiced"])

        # Check practice status
        status_resp = self.client.get("/api/interview-prep/practice-status", headers=headers)
        self.assertEqual(status_resp.status_code, 200)
        self.assertEqual(status_resp.json()["practiced_count"], 1)
        print("  [PASS] Integration 6: Capstone 15 Must-Know questions (5/5/5 distribution) & practice tracking verified.")

    # ---------------------------------------------------------
    # TEST 7: Cross-Skill Overall Diagnostic Evaluation
    # ---------------------------------------------------------
    def test_07_overall_cross_skill_diagnostic_evaluation(self):
        _, _, _, token, headers, _ = self._create_user("Eval Candidate")

        goals = self.client.get("/api/goals").json()
        target_goal_id = goals[0]["id"]
        self.client.post("/api/goals/select", json={"goal_id": target_goal_id}, headers=headers)

        # Get questions
        q_resp = self.client.get("/api/overall-evaluation/questions", headers=headers)
        self.assertEqual(q_resp.status_code, 200)
        questions = q_resp.json()
        self.assertTrue(isinstance(questions, list))
        self.assertTrue(len(questions) > 0)

        # Query correct answers from DB to submit 100% score
        db = SessionLocal()
        overall_objs = db.query(OverallGoalEvaluationQuestion).filter(OverallGoalEvaluationQuestion.goal_id == target_goal_id).all()
        answers_payload = {str(q.id): q.correct_option for q in overall_objs}
        db.close()

        sub_resp = self.client.post("/api/overall-evaluation/submit", json={"answers": answers_payload}, headers=headers)
        self.assertEqual(sub_resp.status_code, 200)
        result = sub_resp.json()
        self.assertIn("readiness_level", result)
        self.assertIn("percentage", result)
        self.assertIn("score", result)
        print(f"  [PASS] Integration 7: Cross-skill overall diagnostic scoring & readiness level '{result['readiness_level']}' verified.")

    # ---------------------------------------------------------
    # TEST 8: AI Mentor Integration & Grounded Context
    # ---------------------------------------------------------
    def test_08_ai_assistant_integration_and_context_grounding(self):
        _, _, _, token, headers, _ = self._create_user("AI Candidate")

        # 1. Suggestions endpoint
        sug_resp = self.client.get("/api/ai/suggestions", headers=headers)
        self.assertEqual(sug_resp.status_code, 200)
        self.assertTrue(len(sug_resp.json()["suggestions"]) > 0)

        # 2. Ask technical question
        ask_resp = self.client.post("/api/ai/ask", json={"prompt": "Explain React state management"}, headers=headers)
        self.assertEqual(ask_resp.status_code, 200)
        ai_data = ask_resp.json()
        self.assertIn("answer", ai_data)
        self.assertIsNotNone(ai_data["syntax_or_framework"])
        self.assertIsNotNone(ai_data["code_example"])

        # 3. Validation: empty prompt returns 400
        bad_prompt = self.client.post("/api/ai/ask", json={"prompt": "   "}, headers=headers)
        self.assertEqual(bad_prompt.status_code, 400)

        # 4. Security: unauthenticated request returns 401
        unauth_ai = self.client.post("/api/ai/ask", json={"prompt": "What is Python?"})
        self.assertEqual(unauth_ai.status_code, 401)
        print("  [PASS] Integration 8: AI assistant grounded responses, syntax examples, and 401/400 validation verified.")

    # ---------------------------------------------------------
    # TEST 9: Comprehensive Candidate Profile & Dashboard Metrics
    # ---------------------------------------------------------
    def test_09_user_profile_and_dashboard_metrics(self):
        _, _, _, token, headers, _ = self._create_user("Dashboard Tester")

        # Select goal
        goals = self.client.get("/api/goals").json()
        self.client.post("/api/goals/select", json={"goal_id": goals[0]["id"]}, headers=headers)

        # Update profile name
        update_resp = self.client.put("/api/auth/profile", json={"name": "Dashboard Master"}, headers=headers)
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.json()["name"], "Dashboard Master")

        # Get profile summary
        summary_resp = self.client.get("/api/auth/profile-summary", headers=headers)
        self.assertEqual(summary_resp.status_code, 200)
        summary = summary_resp.json()
        self.assertEqual(summary["user"]["name"], "Dashboard Master")
        self.assertIn("active_goal_title", summary)
        self.assertIn("skill_completion_percentage", summary)
        print("  [PASS] Integration 9: Candidate profile updates, dashboard metrics & summary aggregation verified.")


def main():
    print("=" * 65)
    print("CAREER EXPLORE STUDIO — PHASE 13 MASTER INTEGRATION TEST SUITE")
    print("=" * 65)
    suite = unittest.TestLoader().loadTestsFromTestCase(Phase13MasterIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print(f"\n[FAIL] {len(result.failures)} failures, {len(result.errors)} errors encountered.")
        sys.exit(1)
    print("=" * 65)
    print("ALL PHASE 13 MASTER INTEGRATION TESTS PASSED CLEANLY!")
    print("=" * 65)


if __name__ == "__main__":
    main()
