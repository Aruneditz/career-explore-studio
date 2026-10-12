import sys
import os
sys.path.insert(0, os.path.abspath("backend"))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import unittest
from starlette.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.models.user import User

class TestAIAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        email = "ai_test_user@careerexplore.com"
        password = "Password123!"
        resp = cls.client.post("/api/auth/register", json={
            "name": "AI Test Candidate",
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

    def test_01_get_suggestions(self):
        resp = self.client.get("/api/ai/suggestions", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("suggestions", data)
        self.assertTrue(len(data["suggestions"]) > 0)
        print(f"\n[AI Test] Dynamic suggestions: {data['suggestions']}")

    def test_02_ask_technical_question(self):
        resp = self.client.post("/api/ai/ask", json={
            "prompt": "Explain React useState simply"
        }, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("useState", data["answer"])
        self.assertIsNotNone(data["syntax_or_framework"])
        self.assertIsNotNone(data["code_example"])
        self.assertIsNotNone(data["practical_explanation"])
        self.assertIsNotNone(data["ces_recommendation"])
        print(f"[AI Test] Technical Q Answer: {data['answer']}")
        print(f"[AI Test] Syntax: {data['syntax_or_framework']}")

    def test_03_ask_next_skill_guidance(self):
        resp = self.client.post("/api/ai/ask", json={
            "prompt": "What should I learn next?"
        }, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsNotNone(data["answer"])
        self.assertIsNotNone(data["ces_recommendation"])
        print(f"[AI Test] Next Skill Answer: {data['answer']}")
        print(f"[AI Test] CES Recommendation: {data['ces_recommendation']}")

    def test_04_ask_non_technical_question(self):
        resp = self.client.post("/api/ai/ask", json={
            "prompt": "Explain marketing in simple words"
        }, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsNotNone(data["answer"])
        self.assertIsNotNone(data["syntax_or_framework"])
        self.assertIsNotNone(data["code_example"])
        print(f"[AI Test] Non-tech Q Answer: {data['answer']}")
        print(f"[AI Test] Framework: {data['syntax_or_framework']}")

    def test_05_empty_prompt_validation(self):
        resp = self.client.post("/api/ai/ask", json={
            "prompt": "   "
        }, headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        print(f"[AI Test] Empty prompt correctly rejected with HTTP 400: {resp.json()['detail']}")

    def test_06_unauthenticated_ask_fails(self):
        resp = self.client.post("/api/ai/ask", json={
            "prompt": "Explain Python"
        })
        self.assertEqual(resp.status_code, 401)
        print("[AI Test] Unauthenticated /api/ai/ask correctly rejected with HTTP 401 Unauthorized.")

    def test_07_unauthenticated_suggestions_fails(self):
        resp = self.client.get("/api/ai/suggestions")
        self.assertEqual(resp.status_code, 401)
        print("[AI Test] Unauthenticated /api/ai/suggestions correctly rejected with HTTP 401 Unauthorized.")

    def test_08_no_secret_keys_in_response(self):
        resp = self.client.post("/api/ai/ask", json={
            "prompt": "How does CES authenticate users?"
        }, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        resp_text = resp.text.lower()
        self.assertNotIn("secret_key", resp_text)
        self.assertNotIn("super-secret-key", resp_text)
        self.assertNotIn("ai_api_key", resp_text)
        self.assertNotIn("gemini_api_key", resp_text)
        print("[AI Test] Verified zero secret keys or private tokens leaked in AI response.")

if __name__ == "__main__":
    unittest.main()
