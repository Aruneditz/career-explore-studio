import sys
import os

# Add backend to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database.database import SessionLocal
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
from app.core.security import get_password_hash, create_access_token


def run_isolation_tests():
    client = TestClient(app)
    db: Session = SessionLocal()
    print("==================================================")
    print("PHASE 10: DATABASE RELATIONSHIPS & AUTHORIZATION AUDIT")
    print("==================================================")

    email_alice = "alice_iso_phase10@ces.internal"
    email_bob = "bob_iso_phase10@ces.internal"

    try:
        # 1. Cleanup any prior run
        for em in [email_alice, email_bob]:
            u = db.query(User).filter(User.email == em).first()
            if u:
                db.delete(u)
        db.commit()

        # 2. Create Alice and Bob
        alice = User(
            name="Alice Engineer",
            email=email_alice,
            hashed_password=get_password_hash("AlicePassword123!"),
            is_active=True
        )
        bob = User(
            name="Bob Designer",
            email=email_bob,
            hashed_password=get_password_hash("BobPassword123!"),
            is_active=True
        )
        db.add_all([alice, bob])
        db.commit()
        db.refresh(alice)
        db.refresh(bob)

        alice_id = alice.id
        bob_id = bob.id

        token_alice = create_access_token(subject=alice_id)
        token_bob = create_access_token(subject=bob_id)

        headers_alice = {"Authorization": f"Bearer {token_alice}"}
        headers_bob = {"Authorization": f"Bearer {token_bob}"}

        # Fetch base goal & skills
        goals = db.query(Goal).order_by(Goal.id.asc()).all()
        assert len(goals) >= 2, "Expected at least 2 goals for testing isolation!"
        goal_a = goals[0]
        goal_b = goals[1]

        skills_a = db.query(Skill).filter(Skill.goal_id == goal_a.id).order_by(Skill.order_index.asc()).all()
        assert len(skills_a) >= 2, "Expected at least 2 skills in goal_a!"
        skill_1 = skills_a[0]
        topics_s1 = db.query(Topic).filter(Topic.skill_id == skill_1.id).order_by(Topic.order_index.asc()).all()
        assert len(topics_s1) >= 2, "Expected at least 2 topics in skill_1!"

        # ----------------------------------------------------
        # TEST 1: GOAL SELECTION ISOLATION
        # ----------------------------------------------------
        # Alice selects Goal A
        res = client.post(f"/api/goals/{goal_a.id}/select", headers=headers_alice)
        assert res.status_code == 200, res.text

        # Bob selects Goal B
        res = client.post(f"/api/goals/{goal_b.id}/select", headers=headers_bob)
        assert res.status_code == 200, res.text

        # Verify Alice's active goal is Goal A
        res_a = client.get("/api/goals/current", headers=headers_alice)
        assert res_a.status_code == 200
        assert res_a.json()["goal_id"] == goal_a.id

        # Verify Bob's active goal is Goal B
        res_b = client.get("/api/goals/current", headers=headers_bob)
        assert res_b.status_code == 200
        assert res_b.json()["goal_id"] == goal_b.id
        print("  [PASS] Test 1: Goal selections strictly isolated per user.")

        # ----------------------------------------------------
        # TEST 2: TOPIC PROGRESS ISOLATION
        # ----------------------------------------------------
        # Alice marks topic 1 as completed
        topic_target = topics_s1[0]
        res_toggle = client.post(
            f"/api/skills/{skill_1.id}/topics/{topic_target.id}/toggle",
            json={"is_completed": True},
            headers=headers_alice
        )
        assert res_toggle.status_code == 200

        # Alice checks topics: topic 1 must be completed
        res_topics_a = client.get(f"/api/skills/{skill_1.id}/topics", headers=headers_alice)
        data_a = res_topics_a.json()
        assert any(t["id"] == topic_target.id and t["is_completed"] is True for t in data_a)

        # Bob checks topics: topic 1 must NOT be completed for Bob
        res_topics_b = client.get(f"/api/skills/{skill_1.id}/topics", headers=headers_bob)
        data_b = res_topics_b.json()
        assert all(t["is_completed"] is False for t in data_b)
        print("  [PASS] Test 2: Topic progress strictly isolated (Alice completed != Bob completed).")

        # ----------------------------------------------------
        # TEST 3: SKILL PROGRESS ISOLATION
        # ----------------------------------------------------
        # Alice gets skill progress
        res_prog_a = client.get(f"/api/skills/{skill_1.id}/progress", headers=headers_alice)
        assert res_prog_a.json()["completed_topics"] == 1

        # Bob gets skill progress
        res_prog_b = client.get(f"/api/skills/{skill_1.id}/progress", headers=headers_bob)
        assert res_prog_b.json()["completed_topics"] == 0
        print("  [PASS] Test 3: Skill progress percentages strictly isolated per user.")

        # ----------------------------------------------------
        # TEST 4: DIAGNOSTIC EVALUATION ISOLATION & ACCESS CONTROL
        # ----------------------------------------------------
        # Alice submits evaluation
        eval_q = db.query(EvaluationQuestion).filter(EvaluationQuestion.skill_id == skill_1.id).all()
        answers_payload = {str(q.id): q.correct_option for q in eval_q}
        res_submit_eval = client.post(
            f"/api/skills/{skill_1.id}/evaluation/submit",
            json={"answers": answers_payload},
            headers=headers_alice
        )
        assert res_submit_eval.status_code == 200
        alice_eval_id = res_submit_eval.json()["id"]

        # Bob checks latest evaluation for skill 1: should be None
        res_eval_b = client.get(f"/api/skills/{skill_1.id}/evaluation/latest", headers=headers_bob)
        assert res_eval_b.status_code == 200
        assert res_eval_b.json() is None

        # Alice accesses her evaluation by ID: 200 OK
        res_alice_lookup = client.get(f"/api/skills/evaluation/records/{alice_eval_id}", headers=headers_alice)
        assert res_alice_lookup.status_code == 200

        # Bob tries to access Alice's evaluation by ID: 403 FORBIDDEN
        res_bob_hack = client.get(f"/api/skills/evaluation/records/{alice_eval_id}", headers=headers_bob)
        assert res_bob_hack.status_code == 403, f"Expected 403 Forbidden, got: {res_bob_hack.status_code}"
        print("  [PASS] Test 4: Evaluation records isolated; cross-user ID access blocked with 403 Forbidden.")

        # ----------------------------------------------------
        # TEST 5: FINAL INTERVIEW PRACTICE ISOLATION
        # ----------------------------------------------------
        final_q = db.query(GoalFinalInterviewQuestion).filter(GoalFinalInterviewQuestion.goal_id == goal_a.id).first()
        if final_q:
            # Alice marks as practiced
            res_practice = client.post(
                "/api/interview-prep/toggle-practiced",
                json={"question_id": final_q.id, "is_practiced": True},
                headers=headers_alice
            )
            assert res_practice.status_code == 200, res_practice.text

            # Bob checks practice status for Goal A
            res_b_status = client.get(f"/api/interview-prep/practice-status?goal_id={goal_a.id}", headers=headers_bob)
            assert res_b_status.json()["practiced_count"] == 0
            print("  [PASS] Test 5: Final interview practice statuses strictly isolated per user.")

        # ----------------------------------------------------
        # TEST 6: CROSS-SKILL EVALUATION ISOLATION & ACCESS CONTROL
        # ----------------------------------------------------
        overall_q = db.query(OverallGoalEvaluationQuestion).filter(OverallGoalEvaluationQuestion.goal_id == goal_a.id).all()
        if overall_q:
            overall_ans = {str(q.id): q.correct_option for q in overall_q}
            res_overall = client.post(
                f"/api/overall-evaluation/submit?goal_id={goal_a.id}",
                json={"answers": overall_ans},
                headers=headers_alice
            )
            assert res_overall.status_code == 200
            alice_report_id = res_overall.json()["id"]

            # Bob checks latest overall evaluation
            res_b_overall = client.get(f"/api/overall-evaluation/latest?goal_id={goal_a.id}", headers=headers_bob)
            assert res_b_overall.json() is None

            # Bob tries to access Alice's report by ID: 403 FORBIDDEN
            res_b_hack_report = client.get(f"/api/overall-evaluation/reports/{alice_report_id}", headers=headers_bob)
            assert res_b_hack_report.status_code == 403
            print("  [PASS] Test 6: Cross-skill evaluation reports isolated; cross-user ID access blocked with 403 Forbidden.")

        # ----------------------------------------------------
        # TEST 7: CERTIFICATE GENERATION, OWNERSHIP & UNAUTHORIZED ACCESS
        # ----------------------------------------------------
        # Alice completes all must-know topics for skill 1
        for t in topics_s1:
            client.post(
                f"/api/skills/{skill_1.id}/topics/{t.id}/toggle",
                json={"is_completed": True},
                headers=headers_alice
            )
        client.post(f"/api/skills/{skill_1.id}/complete?force=true", headers=headers_alice)
        client.post(f"/api/skills/{skill_1.id}/record-stage", json={"stage": "practical"}, headers=headers_alice)
        client.post(f"/api/skills/{skill_1.id}/record-stage", json={"stage": "interview"}, headers=headers_alice)

        # Alice claims certificate
        res_claim_alice = client.post(f"/api/skills/{skill_1.id}/claim-certificate", headers=headers_alice)
        assert res_claim_alice.status_code == 200, res_claim_alice.text
        alice_cert_db_id = res_claim_alice.json()["id"]

        # Bob checks certificates: total_earned must be 0
        res_certs_bob = client.get("/api/certificates", headers=headers_bob)
        assert res_certs_bob.json()["total_earned"] == 0

        # Bob attempts to claim certificate for skill 1 without completing stages: 400 Bad Request
        res_bob_claim_fail = client.post(f"/api/skills/{skill_1.id}/claim-certificate", headers=headers_bob)
        assert res_bob_claim_fail.status_code == 400

        # Bob attempts to fetch Alice's certificate by database ID: 403 Forbidden
        res_bob_cert_hack = client.get(f"/api/certificates/{alice_cert_db_id}", headers=headers_bob)
        assert res_bob_cert_hack.status_code == 403, f"Expected 403, got: {res_bob_cert_hack.status_code}"
        print("  [PASS] Test 7: Certificate generation strictly enforced; unauthorized cross-user access returns 403 Forbidden.")

        # ----------------------------------------------------
        # TEST 8: AI CONTEXT & RECOMMENDATION ISOLATION
        # ----------------------------------------------------
        # Alice asks AI: "How is my progress?"
        res_ai_alice = client.post("/api/ai/ask", json={"prompt": "How is my progress?"}, headers=headers_alice)
        assert res_ai_alice.status_code == 200
        ai_data_alice = res_ai_alice.json()
        assert ai_data_alice["context_used"]["goal_title"] == goal_a.title

        # Bob asks AI: "How is my progress?"
        res_ai_bob = client.post("/api/ai/ask", json={"prompt": "How is my progress?"}, headers=headers_bob)
        assert res_ai_bob.status_code == 200
        ai_data_bob = res_ai_bob.json()
        assert ai_data_bob["context_used"]["goal_title"] == goal_b.title
        # Bob must have 0 completed skills
        assert len(ai_data_bob["context_used"]["completed_skills"]) == 0
        print("  [PASS] Test 8: AI Mentor learning context strictly isolated between Alice and Bob.")

        # ----------------------------------------------------
        # TEST 9: CASCADING DELETE INTEGRITY & CROSS-USER PRESERVATION
        # ----------------------------------------------------
        # Delete Alice from database
        db_alice = db.query(User).filter(User.id == alice_id).first()
        db.delete(db_alice)
        db.commit()

        # Verify all Alice's child records were deleted via cascade
        assert db.query(UserGoalSelection).filter(UserGoalSelection.user_id == alice_id).count() == 0
        assert db.query(UserTopicProgress).filter(UserTopicProgress.user_id == alice_id).count() == 0
        assert db.query(UserSkillProgress).filter(UserSkillProgress.user_id == alice_id).count() == 0
        assert db.query(UserSkillEvaluation).filter(UserSkillEvaluation.user_id == alice_id).count() == 0
        assert db.query(UserGoalEvaluation).filter(UserGoalEvaluation.user_id == alice_id).count() == 0
        assert db.query(UserInterviewPractice).filter(UserInterviewPractice.user_id == alice_id).count() == 0
        assert db.query(UserCertificate).filter(UserCertificate.user_id == alice_id).count() == 0

        # Verify Bob still exists and Bob's goal selection is 100% intact
        db_bob = db.query(User).filter(User.id == bob_id).first()
        assert db_bob is not None
        assert db.query(UserGoalSelection).filter(UserGoalSelection.user_id == bob_id).count() == 1
        print("  [PASS] Test 9: Cascade deletion cleanly removes user children while preserving other users.")

        print("\nALL 9 PHASE 10 USER ISOLATION & AUTHORIZATION TESTS PASSED SUCCESSFULLY!")

    finally:
        # Cleanup
        for em in [email_alice, email_bob]:
            u = db.query(User).filter(User.email == em).first()
            if u:
                db.delete(u)
        db.commit()
        db.close()


if __name__ == "__main__":
    run_isolation_tests()
