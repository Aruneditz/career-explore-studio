import sys
import os
sys.path.insert(0, os.path.abspath("backend"))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import unittest
from starlette.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.models import (
    User, Goal, Skill, Topic, UserGoalSelection,
    UserSkillProgress, UserTopicProgress, UserSkillEvaluation,
    UserCertificate, GoalFinalInterviewQuestion, UserInterviewPractice
)

class TestMultiUserIsolation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

        # 1. Register Alice
        alice_resp = cls.client.post("/api/auth/register", json={
            "name": "Alice Candidate",
            "email": "alice.isolation@example.com",
            "password": "Password123!"
        })
        if alice_resp.status_code == 201:
            cls.alice_token = alice_resp.json()["access_token"]
        else:
            login_resp = cls.client.post("/api/auth/login", json={
                "email": "alice.isolation@example.com",
                "password": "Password123!"
            })
            cls.alice_token = login_resp.json()["access_token"]
        cls.alice_headers = {"Authorization": f"Bearer {cls.alice_token}"}

        # 2. Register Bob
        bob_resp = cls.client.post("/api/auth/register", json={
            "name": "Bob Candidate",
            "email": "bob.isolation@example.com",
            "password": "Password123!"
        })
        if bob_resp.status_code == 201:
            cls.bob_token = bob_resp.json()["access_token"]
        else:
            login_resp = cls.client.post("/api/auth/login", json={
                "email": "bob.isolation@example.com",
                "password": "Password123!"
            })
            cls.bob_token = login_resp.json()["access_token"]
        cls.bob_headers = {"Authorization": f"Bearer {cls.bob_token}"}

        db = SessionLocal()
        alice = db.query(User).filter(User.email == "alice.isolation@example.com").first()
        bob = db.query(User).filter(User.email == "bob.isolation@example.com").first()
        cls.alice_id = alice.id
        cls.bob_id = bob.id

        fullstack_goal = db.query(Goal).filter(Goal.slug == "full-stack-developer").first()
        if not fullstack_goal:
            fullstack_goal = db.query(Goal).first()
        cls.goal_id = fullstack_goal.id

        skill = db.query(Skill).filter(Skill.goal_id == fullstack_goal.id).first()
        cls.skill_id = skill.id

        # Clean up any existing records for both test users
        for uid in [cls.alice_id, cls.bob_id]:
            db.query(UserCertificate).filter(UserCertificate.user_id == uid).delete()
            db.query(UserInterviewPractice).filter(UserInterviewPractice.user_id == uid).delete()
            db.query(UserSkillEvaluation).filter(UserSkillEvaluation.user_id == uid).delete()
            db.query(UserSkillProgress).filter(UserSkillProgress.user_id == uid).delete()
            db.query(UserTopicProgress).filter(UserTopicProgress.user_id == uid).delete()
            db.query(UserGoalSelection).filter(UserGoalSelection.user_id == uid).delete()
        db.commit()
        db.close()

    def test_01_goal_selection_isolation(self):
        # Alice selects Full Stack Developer
        resp = self.client.post(f"/api/goals/{self.goal_id}/select", headers=self.alice_headers)
        self.assertEqual(resp.status_code, 200)

        # Alice's active goal is Full Stack Developer
        alice_goal = self.client.get("/api/goals/current", headers=self.alice_headers)
        self.assertEqual(alice_goal.status_code, 200)
        self.assertEqual(alice_goal.json()["goal_id"], self.goal_id)

        # Bob's active goal should be None (not yet selected)
        bob_goal = self.client.get("/api/goals/current", headers=self.bob_headers)
        self.assertEqual(bob_goal.status_code, 200)
        self.assertIsNone(bob_goal.json())
        print("\n[Isolation Test 1] Goal selection isolation verified: Alice enrolled, Bob not enrolled.")

    def test_02_topic_progress_isolation(self):
        db = SessionLocal()
        topics = db.query(Topic).filter(Topic.skill_id == self.skill_id).all()
        t0_id = topics[0].id
        db.close()

        # Alice completes topic 0
        resp = self.client.post(
            f"/api/skills/{self.skill_id}/topics/{t0_id}/toggle",
            json={"is_completed": True},
            headers=self.alice_headers
        )
        self.assertEqual(resp.status_code, 200)

        # Alice sees topic completed
        alice_topics = self.client.get(f"/api/skills/{self.skill_id}/topics", headers=self.alice_headers).json()
        alice_t0 = next(t for t in alice_topics if t["id"] == t0_id)
        self.assertTrue(alice_t0["is_completed"])

        # Bob queries topics: Bob's copy MUST NOT be completed!
        bob_topics = self.client.get(f"/api/skills/{self.skill_id}/topics", headers=self.bob_headers).json()
        bob_t0 = next(t for t in bob_topics if t["id"] == t0_id)
        self.assertFalse(bob_t0["is_completed"])
        print("[Isolation Test 2] Topic completion isolation verified: Alice completed, Bob incomplete.")

    def test_03_self_evaluation_isolation(self):
        # Alice submits evaluation
        db = SessionLocal()
        eval_record = UserSkillEvaluation(
            user_id=self.alice_id,
            skill_id=self.skill_id,
            score=5,
            total_questions=5,
            percentage=100,
            answers_json="{}",
            strong_areas_json="[]",
            weak_areas_json="[]",
            feedback_summary="Alice Excellent",
            improvement_suggestions_json="[]"
        )
        db.add(eval_record)
        db.commit()
        db.close()

        # Alice's latest evaluation exists
        alice_eval = self.client.get(f"/api/skills/{self.skill_id}/evaluation/latest", headers=self.alice_headers)
        self.assertEqual(alice_eval.status_code, 200)
        self.assertIsNotNone(alice_eval.json())
        self.assertEqual(alice_eval.json()["percentage"], 100)

        # Bob's latest evaluation MUST be None
        bob_eval = self.client.get(f"/api/skills/{self.skill_id}/evaluation/latest", headers=self.bob_headers)
        self.assertEqual(bob_eval.status_code, 200)
        self.assertIsNone(bob_eval.json())
        print("[Isolation Test 3] Evaluation isolation verified: Alice has 100% eval, Bob has None.")

    def test_04_certificate_isolation(self):
        # Alice finishes all stages to claim certificate
        db = SessionLocal()
        topics = db.query(Topic).filter(Topic.skill_id == self.skill_id).all()
        for t in topics:
            existing = db.query(UserTopicProgress).filter(
                UserTopicProgress.user_id == self.alice_id,
                UserTopicProgress.topic_id == t.id
            ).first()
            if not existing:
                db.add(UserTopicProgress(user_id=self.alice_id, topic_id=t.id, is_completed=True))
            else:
                existing.is_completed = True
        
        # Mark practical & interview for Alice
        prog = db.query(UserSkillProgress).filter(
            UserSkillProgress.user_id == self.alice_id,
            UserSkillProgress.skill_id == self.skill_id
        ).first()
        if not prog:
            prog = UserSkillProgress(
                user_id=self.alice_id,
                skill_id=self.skill_id,
                practical_reviewed=True,
                interview_reviewed=True,
                is_completed=True
            )
            db.add(prog)
        else:
            prog.practical_reviewed = True
            prog.interview_reviewed = True
            prog.is_completed = True
        db.commit()
        db.close()

        # Alice claims certificate
        alice_claim = self.client.post(f"/api/skills/{self.skill_id}/claim-certificate", headers=self.alice_headers)
        self.assertEqual(alice_claim.status_code, 200)
        alice_cert_id = alice_claim.json()["certificate_id"]

        # Alice's certificates list has 1 certificate
        alice_certs = self.client.get("/api/certificates", headers=self.alice_headers).json()["certificates"]
        self.assertEqual(len(alice_certs), 1)
        self.assertEqual(alice_certs[0]["certificate_id"], alice_cert_id)

        # Bob's certificates list MUST have 0 certificates!
        bob_certs = self.client.get("/api/certificates", headers=self.bob_headers).json()["certificates"]
        self.assertEqual(len(bob_certs), 0)

        # Bob's certificate status MUST be locked (not eligible)
        bob_status = self.client.get(f"/api/skills/{self.skill_id}/certificate", headers=self.bob_headers).json()
        self.assertFalse(bob_status["is_unlocked"])
        self.assertIsNone(bob_status["certificate"])

        # Bob attempting to claim certificate MUST fail with HTTP 400
        bob_claim_fail = self.client.post(f"/api/skills/{self.skill_id}/claim-certificate", headers=self.bob_headers)
        self.assertEqual(bob_claim_fail.status_code, 400)
        print(f"[Isolation Test 4] Certificate isolation verified: Alice claimed {alice_cert_id}, Bob has 0 certificates and is blocked from claiming.")

    def test_05_interview_practice_isolation(self):
        # Fetch question 1 ID
        db = SessionLocal()
        q1 = db.query(GoalFinalInterviewQuestion).filter(
            GoalFinalInterviewQuestion.goal_id == self.goal_id,
            GoalFinalInterviewQuestion.question_number == 1
        ).first()
        q1_id = q1.id if q1 else 1
        db.close()

        # Check capstone final interview practice isolation
        resp = self.client.post("/api/interview-prep/toggle-practiced", json={
            "question_id": q1_id,
            "is_practiced": True
        }, headers=self.alice_headers)
        self.assertEqual(resp.status_code, 200)

        # Alice status shows question 1 practiced
        alice_stat = self.client.get("/api/interview-prep/practice-status", headers=self.alice_headers).json()
        self.assertIn(q1_id, alice_stat["practiced_question_ids"])

        # Bob status MUST NOT show question 1 practiced
        bob_stat = self.client.get("/api/interview-prep/practice-status", headers=self.bob_headers).json()
        self.assertNotIn(q1_id, bob_stat["practiced_question_ids"])
        self.assertEqual(bob_stat["practiced_count"], 0)
        print("[Isolation Test 5] Final interview practice isolation verified: Alice practiced Q1, Bob has 0 practiced.")

    def test_06_dashboard_isolation(self):
        # Alice dashboard vs Bob dashboard
        alice_dash = self.client.get("/api/progress/dashboard", headers=self.alice_headers).json()
        bob_dash = self.client.get("/api/progress/dashboard", headers=self.bob_headers).json()

        self.assertTrue(alice_dash["completed_topics"] > 0)
        self.assertEqual(bob_dash["completed_topics"], 0)
        self.assertEqual(bob_dash["completed_skills"], 0)
        print(f"[Isolation Test 6] Dashboard isolation verified: Alice topics={alice_dash['completed_topics']}, Bob topics={bob_dash['completed_topics']}.")

if __name__ == "__main__":
    unittest.main()
