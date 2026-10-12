import sys
import os
sys.path.insert(0, os.path.abspath("backend"))

import unittest
from starlette.testclient import TestClient
from app.main import app
from app.database.database import get_db, SessionLocal
from app.models.user import User
from app.models import (
    User, Goal, Skill, Topic, UserSkillProgress,
    UserTopicProgress, UserSkillEvaluation, UserCertificate
)

class TestCertificateWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        # Register a unique test user
        email = "cert_test_user@example.com"
        password = "Password123!"
        resp = cls.client.post("/api/auth/register", json={
            "name": "Certificate Test User",
            "email": email,
            "password": password
        })
        if resp.status_code == 201:
            cls.token = resp.json()["access_token"]
        else:
            login_resp = cls.client.post("/api/auth/login", json={
                "email": email,
                "password": password
            })
            cls.token = login_resp.json()["access_token"]
            
        cls.headers = {"Authorization": f"Bearer {cls.token}"}
        
        # Get user ID and an active skill
        db = SessionLocal()
        cls.user = db.query(User).filter(User.email == email).first()
        cls.skill = db.query(Skill).first()
        db.close()

    def test_01_locked_status_when_incomplete(self):
        # Clean any existing certificates for this skill for this user
        db = SessionLocal()
        db.query(UserCertificate).filter(
            UserCertificate.user_id == self.user.id,
            UserCertificate.skill_id == self.skill.id
        ).delete()
        db.query(UserSkillProgress).filter(
            UserSkillProgress.user_id == self.user.id,
            UserSkillProgress.skill_id == self.skill.id
        ).delete()
        db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == self.user.id
        ).delete()
        db.query(UserSkillEvaluation).filter(
            UserSkillEvaluation.user_id == self.user.id,
            UserSkillEvaluation.skill_id == self.skill.id
        ).delete()
        db.commit()
        db.close()

        # Check status
        resp = self.client.get(f"/api/skills/{self.skill.id}/certificate", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertFalse(data["is_unlocked"])
        self.assertIsNone(data["certificate"])
        self.assertIn("checklist", data)
        print(f"\n[Test] Checklist before completion: {data['checklist']}")

    def test_02_claim_fails_when_incomplete(self):
        resp = self.client.post(f"/api/skills/{self.skill.id}/claim-certificate", headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("detail", resp.json())
        print(f"[Test] Correctly rejected claim when incomplete: {resp.json()['detail']}")

    def test_03_record_stages_and_complete_topics_eval(self):
        # 1. Mark practical reviewed
        resp_prac = self.client.post(
            f"/api/skills/{self.skill.id}/record-stage",
            json={"stage": "practical"},
            headers=self.headers
        )
        self.assertEqual(resp_prac.status_code, 200)

        # 2. Mark interview reviewed
        resp_int = self.client.post(
            f"/api/skills/{self.skill.id}/record-stage",
            json={"stage": "interview"},
            headers=self.headers
        )
        self.assertEqual(resp_int.status_code, 200)

        # 3. Complete all topics for this skill
        db = SessionLocal()
        topics = db.query(Topic).filter(Topic.skill_id == self.skill.id).all()
        for t in topics:
            existing = db.query(UserTopicProgress).filter(
                UserTopicProgress.user_id == self.user.id,
                UserTopicProgress.topic_id == t.id
            ).first()
            if not existing:
                tp = UserTopicProgress(user_id=self.user.id, topic_id=t.id, is_completed=True)
                db.add(tp)
            else:
                existing.is_completed = True
        
        # 4. Add evaluation pass
        eval_record = db.query(UserSkillEvaluation).filter(
            UserSkillEvaluation.user_id == self.user.id,
            UserSkillEvaluation.skill_id == self.skill.id
        ).first()
        if not eval_record:
            eval_record = UserSkillEvaluation(
                user_id=self.user.id,
                skill_id=self.skill.id,
                score=5,
                total_questions=5,
                percentage=100,
                answers_json="{}",
                strong_areas_json="[]",
                weak_areas_json="[]",
                feedback_summary="Excellent mastery",
                improvement_suggestions_json="[]"
            )
            db.add(eval_record)
        else:
            eval_record.percentage = 100

        db.commit()
        db.close()

        # Check status again -> should be unlocked!
        resp = self.client.get(f"/api/skills/{self.skill.id}/certificate", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        print(f"[Test] Checklist after 100% completion: {data['checklist']}")
        self.assertTrue(data["is_unlocked"])
        self.assertTrue(data["checklist"]["overall_completed"])
        self.assertEqual(data["checklist"]["progress_percentage"], 100)

    def test_04_claim_and_verify_certificate(self):
        # Claim certificate
        resp = self.client.post(f"/api/skills/{self.skill.id}/claim-certificate", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        cert = resp.json()
        cert_id = cert["certificate_id"]
        self.assertTrue(cert_id.startswith("CES-SKILL-"))
        self.assertEqual(cert["recipient_name"], "Certificate Test User")
        print(f"[Test] Successfully claimed Certificate: {cert_id}")

        # Verify certificate publicly
        resp_verify = self.client.get(f"/api/certificates/verify/{cert_id}")
        self.assertEqual(resp_verify.status_code, 200)
        verify_data = resp_verify.json()
        self.assertEqual(verify_data["certificate_id"], cert_id)
        self.assertEqual(verify_data["recipient_name"], "Certificate Test User")
        self.assertEqual(verify_data["status"], "issued")
        print(f"[Test] Verified public certificate ID {cert_id}: status={verify_data['status']}")

        # List user certificates
        resp_list = self.client.get("/api/certificates", headers=self.headers)
        self.assertEqual(resp_list.status_code, 200)
        certs = resp_list.json()["certificates"]
        self.assertTrue(any(c["certificate_id"] == cert_id for c in certs))
        print(f"[Test] User certificates count: {len(certs)}")

if __name__ == "__main__":
    unittest.main()
