import json
import logging
from typing import Optional, Dict, Any, List
import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.goal import Goal
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.user_goal import UserGoalSelection
from app.models.skill_progress import UserSkillProgress
from app.models.topic_progress import UserTopicProgress
from app.models.evaluation import EvaluationQuestion, UserSkillEvaluation
from app.models.skill_interview import SkillInterviewQuestion
from app.models.final_interview import GoalFinalInterviewQuestion
from app.models.certificate import UserCertificate
from app.schemas.ai import AIAskRequest, AIAskResponse

logger = logging.getLogger("ces_ai")


def get_user_ces_context(
    db: Session,
    user_id: int,
    skill_id: Optional[int] = None,
    topic_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Extract sanitized learning context for the user from the CES SQLite database.
    Grounded in:
    - Active enrolled goal
    - Completed skills and in-progress skills
    - Current active skill and next upcoming skill
    - Completed topics count and first pending topic
    - Diagnostic quiz / evaluation score
    - Interview prep status & certificate status
    Private personal data (passwords, emails, secret keys) is strictly omitted.
    """
    context: Dict[str, Any] = {
        "has_goal": False,
        "goal_id": None,
        "goal_title": None,
        "career_track": None,
        "total_skills": 0,
        "completed_skills": [],
        "in_progress_skills": [],
        "current_skill": None,
        "next_skill": None,
        "current_topic": None,
        "pending_topic": None,
        "skill_topics_completed": 0,
        "skill_topics_total": 0,
        "goal_topics_completed": 0,
        "goal_topics_total": 0,
        "latest_evaluation": None,
        "certificate_earned": False,
    }

    # 1. Fetch user's active career goal
    active_selection = db.query(UserGoalSelection).filter(
        UserGoalSelection.user_id == user_id,
        UserGoalSelection.is_active == True
    ).first()

    if not active_selection:
        # Fallback: check most recently selected goal
        active_selection = db.query(UserGoalSelection).filter(
            UserGoalSelection.user_id == user_id
        ).order_by(UserGoalSelection.selected_at.desc()).first()

    if not active_selection:
        return context

    goal = db.query(Goal).filter(Goal.id == active_selection.goal_id).first()
    if not goal:
        return context

    context["has_goal"] = True
    context["goal_id"] = goal.id
    context["goal_title"] = goal.title
    context["career_track"] = goal.category

    # 2. Fetch skills in curriculum order
    skills = db.query(Skill).filter(Skill.goal_id == goal.id).order_by(Skill.order_index.asc()).all()
    context["total_skills"] = len(skills)
    skill_ids = [s.id for s in skills]

    skill_progress_records = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id.in_(skill_ids)
    ).all() if skill_ids else []
    progress_map = {p.skill_id: p for p in skill_progress_records}

    completed_names = []
    in_progress_names = []
    first_incomplete_skill = None

    for s in skills:
        p = progress_map.get(s.id)
        if p and p.is_completed:
            completed_names.append(s.name)
        else:
            if not first_incomplete_skill:
                first_incomplete_skill = s
            in_progress_names.append(s.name)

    context["completed_skills"] = completed_names
    context["in_progress_skills"] = in_progress_names

    # 3. Resolve active and next skill
    resolved_current_skill = None
    if skill_id:
        resolved_current_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not resolved_current_skill:
        if first_incomplete_skill:
            resolved_current_skill = first_incomplete_skill
        elif skills:
            resolved_current_skill = skills[-1]

    if resolved_current_skill:
        curr_p = progress_map.get(resolved_current_skill.id)
        context["current_skill"] = {
            "id": resolved_current_skill.id,
            "name": resolved_current_skill.name,
            "category": resolved_current_skill.category,
            "order_index": resolved_current_skill.order_index,
            "practical_reviewed": curr_p.practical_reviewed if curr_p else False,
            "interview_reviewed": curr_p.interview_reviewed if curr_p else False,
            "is_completed": curr_p.is_completed if curr_p else False,
        }

        # Find next sequential skill
        next_s = db.query(Skill).filter(
            Skill.goal_id == goal.id,
            Skill.order_index > resolved_current_skill.order_index
        ).order_by(Skill.order_index.asc()).first()
        if next_s:
            context["next_skill"] = next_s.name

        # Check certificate for current skill
        cert = db.query(UserCertificate).filter(
            UserCertificate.user_id == user_id,
            UserCertificate.skill_id == resolved_current_skill.id
        ).first()
        context["certificate_earned"] = cert is not None

        # 4. Fetch topics for current skill and identify completed & pending
        skill_topics = db.query(Topic).filter(
            Topic.skill_id == resolved_current_skill.id
        ).order_by(Topic.order_index.asc()).all()
        context["skill_topics_total"] = len(skill_topics)
        skill_topic_ids = [t.id for t in skill_topics]

        user_tp = db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.topic_id.in_(skill_topic_ids),
            UserTopicProgress.is_completed == True
        ).all() if skill_topic_ids else []
        completed_topic_ids = {utp.topic_id for utp in user_tp}
        context["skill_topics_completed"] = len(completed_topic_ids)

        pending_topics = [t for t in skill_topics if t.id not in completed_topic_ids]
        if pending_topics:
            context["pending_topic"] = {
                "id": pending_topics[0].id,
                "title": pending_topics[0].title,
                "description": pending_topics[0].description,
                "is_must_know": pending_topics[0].is_must_know,
            }

        # Resolve current topic
        resolved_topic = None
        if topic_id:
            resolved_topic = db.query(Topic).filter(Topic.id == topic_id).first()
        elif pending_topics:
            resolved_topic = pending_topics[0]
        elif skill_topics:
            resolved_topic = skill_topics[0]

        if resolved_topic:
            context["current_topic"] = {
                "id": resolved_topic.id,
                "title": resolved_topic.title,
                "description": resolved_topic.description,
                "is_must_know": resolved_topic.is_must_know,
            }

        # Latest diagnostic evaluation score
        latest_eval = db.query(UserSkillEvaluation).filter(
            UserSkillEvaluation.user_id == user_id,
            UserSkillEvaluation.skill_id == resolved_current_skill.id
        ).order_by(UserSkillEvaluation.completed_at.desc()).first()
        if latest_eval:
            context["latest_evaluation"] = {
                "score": latest_eval.score,
                "total_questions": latest_eval.total_questions,
                "percentage": latest_eval.percentage,
                "passed": latest_eval.percentage >= 70,
                "feedback": latest_eval.feedback_summary
            }

    # 5. Goal-level topics count
    if skill_ids:
        all_goal_topics = db.query(Topic.id).filter(Topic.skill_id.in_(skill_ids)).all()
        all_goal_topic_ids = [t[0] for t in all_goal_topics]
        context["goal_topics_total"] = len(all_goal_topic_ids)
        if all_goal_topic_ids:
            goal_completed_count = db.query(UserTopicProgress).filter(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.topic_id.in_(all_goal_topic_ids),
                UserTopicProgress.is_completed == True
            ).count()
            context["goal_topics_completed"] = goal_completed_count

    return context


def get_suggested_prompts(db: Session, user_id: int) -> List[str]:
    """
    Generate dynamic prompt chips tailored to the candidate's active goal and progress.
    """
    context = get_user_ces_context(db, user_id)
    if not context["has_goal"]:
        return [
            "What career goals are available in CES?",
            "What skills do I need for Full Stack Development?",
            "Explain React useState simply",
            "Give me Python interview questions",
            "Explain marketing in simple words",
        ]

    goal_title = context["goal_title"]
    completed = context["completed_skills"]
    curr_skill = context.get("current_skill")
    curr_name = curr_skill["name"] if curr_skill else None
    pending_topic = context.get("pending_topic")

    prompts = []
    # 1. Progression check
    if completed:
        prompts.append(f"I completed {completed[-1]}. What should I learn next?")
    else:
        prompts.append("What should I learn next?")

    # 2. Topic explanation
    if pending_topic:
        prompts.append(f"Explain {pending_topic['title']} in simple words")
    elif curr_name:
        prompts.append("Explain the topic I am currently learning")

    # 3. Overall progress
    prompts.append("How is my progress?")

    # 4. Interview questions for current skill
    if curr_name:
        prompts.append(f"Give me interview questions for {curr_name}")

    # 5. Milestone completion
    prompts.append(f"How do I complete my {goal_title} curriculum?")

    return prompts[:5]


def _call_gemini_api(api_key: str, prompt: str, ces_context: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Calls Google Gemini REST API if a key is configured in backend environment.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    curr_skill_name = ces_context.get("current_skill", {}).get("name") if ces_context.get("current_skill") else "None"
    pending_topic_name = ces_context.get("pending_topic", {}).get("title") if ces_context.get("pending_topic") else "None"
    
    system_instruction = (
        "You are the Career Explore Studio (CES) AI Mentor. CES is a structured skill learning, "
        "roadmap, and interview preparation platform supporting technical and non-technical career tracks. "
        "User context in CES:\n"
        f"- Enrolled Goal: {ces_context.get('goal_title', 'None')}\n"
        f"- Completed Skills: {', '.join(ces_context.get('completed_skills', [])) or 'None'}\n"
        f"- Current Active Skill: {curr_skill_name}\n"
        f"- First Pending Topic: {pending_topic_name}\n"
        f"- Next Recommended Skill: {ces_context.get('next_skill', 'None')}\n"
        f"- Topics Mastered in Current Skill: {ces_context.get('skill_topics_completed', 0)}/{ces_context.get('skill_topics_total', 0)}\n\n"
        "Format requirements:\n"
        "Always respond in valid JSON with these exact string keys:\n"
        "- answer: Simple, beginner-friendly direct explanation (2-3 sentences).\n"
        "- syntax_or_framework: Simple syntax or structural steps (short, concise).\n"
        "- code_example: Small practical example (code snippet for technical skills, real-world case study for non-technical).\n"
        "- practical_explanation: Practical explanation of why and how this works in real projects.\n"
        "- ces_recommendation: Clear next step recommendation specifically within Career Explore Studio.\n"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_instruction},
                    {"text": f"User Question: {prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.4,
            "maxOutputTokens": 800
        }
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text_part = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text_part)
                return parsed
    except Exception as e:
        logger.warning(f"External AI call failed or timed out: {e}. Falling back to CES Knowledge Engine.")
        return None

    return None


def _built_in_ces_reasoner(
    db: Session,
    prompt: str,
    context: Dict[str, Any]
) -> Dict[str, str]:
    """
    Built-in, high-accuracy CES Knowledge Engine.
    Guarantees instant, beginner-friendly, structured answers grounded in CES database:
    1. 'I completed HTML and CSS. What should I learn next?' / Progression queries
    2. 'Explain the topic I am currently learning'
    3. 'How is my progress?'
    4. 'Give me interview questions for my current skill'
    5. Concept lookups (React useState, JavaScript, Python, FastAPI, etc.)
    """
    p_lower = prompt.lower().strip()
    goal_title = context.get("goal_title") or "Career Track"
    completed = context.get("completed_skills") or []
    current_skill_data = context.get("current_skill") or {}
    current_skill_name = current_skill_data.get("name", "HTML")
    current_skill_id = current_skill_data.get("id")
    next_skill_name = context.get("next_skill")
    pending_topic = context.get("pending_topic")
    current_topic = context.get("current_topic") or pending_topic

    # ---------------------------------------------------------
    # 1. 'Explain the topic I am currently learning'
    # ---------------------------------------------------------
    if any(k in p_lower for k in [
        "topic i am currently learning",
        "topic i'm currently learning",
        "topic am i currently learning",
        "explain my current topic",
        "explain current topic",
        "current topic",
        "explain the topic",
        "what topic am i",
    ]):
        topic_to_explain = current_topic or pending_topic
        if topic_to_explain:
            t_title = topic_to_explain.get("title", "Foundational Concepts")
            t_desc = topic_to_explain.get("description", "Core principles and syntax patterns.")
            is_must_know = topic_to_explain.get("is_must_know", False)
            must_know_tag = " [Must-Know Essential]" if is_must_know else ""

            # Check if this topic has technical or non-technical nature
            is_tech = any(s in current_skill_name.lower() for s in ["html", "css", "javascript", "react", "python", "fastapi", "sql", "git"])

            if "semantic" in t_title.lower() or "html" in current_skill_name.lower():
                syntax_box = "<header>\n  <nav>Navigation Links</nav>\n</header>\n<main>\n  <article>Content</article>\n</main>"
                code_box = "<article class='lesson-card'>\n  <h2>Semantic Structure</h2>\n  <p>Improves accessibility and search indexing.</p>\n</article>"
                prac_exp = "Semantic elements clearly convey their purpose to both browsers and assistive screen readers, making pages easier to navigate and maintain."
            elif "box model" in t_title.lower() or "flexbox" in t_title.lower() or "css" in current_skill_name.lower():
                syntax_box = ".container {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n}"
                code_box = ".card {\n  display: flex;\n  padding: 1.5rem;\n  margin: 0.5rem;\n  box-sizing: border-box;\n}"
                prac_exp = "Flexbox and the CSS box model let you align interface components smoothly across varying screen dimensions without floats or absolute positioning hacks."
            elif "react" in current_skill_name.lower():
                syntax_box = "const [state, setState] = useState(initialValue);"
                code_box = "const [activeTab, setActiveTab] = useState('overview');\nfunction handleTabChange(tab) { setActiveTab(tab); }"
                prac_exp = "Managing state via React hooks allows modular components to react immediately to user clicks, keyboard inputs, and data fetching."
            elif "fastapi" in current_skill_name.lower():
                syntax_box = "@router.get('/items/{item_id}', response_model=ItemSchema)\ndef get_item(item_id: int): return item"
                code_box = "@app.get('/api/skills')\ndef list_skills():\n    return {'status': 'success', 'data': ['HTML', 'CSS', 'JS']}"
                prac_exp = "FastAPI endpoints leverage Python type hints to serialize responses cleanly and auto-generate interactive Swagger docs at /docs."
            elif is_tech:
                syntax_box = f"// Syntax pattern for {t_title}\nfunction executeTask(params) {{\n  return performAction(params);\n}}"
                code_box = f"// Practical Example of {t_title}\nconst config = {{ topic: '{t_title}' }};\nconsole.log(`Mastering ${{config.topic}} in CES!`);"
                prac_exp = f"{t_title} is a fundamental pillar of {current_skill_name} that appears consistently in production codebases and technical interviews."
            else:
                syntax_box = f"3-Step Structure: 1. Objective Alignment → 2. Execution Plan → 3. Outcome Verification"
                code_box = f"Case Scenario for {t_title}:\n- Challenge: Align team deliverables\n- Action: Applied {t_title} workflow\n- Result: 25% faster milestone completion"
                prac_exp = f"Mastering {t_title} equips professionals with structured frameworks to make reliable strategic decisions."

            return {
                "answer": f"You are currently learning **{t_title}**{must_know_tag} in **{current_skill_name}**. {t_desc}",
                "syntax_or_framework": syntax_box,
                "code_example": code_box,
                "practical_explanation": prac_exp,
                "ces_recommendation": f"Review this topic thoroughly and mark **{t_title}** complete in your CES Must-Know Topics checklist to boost your skill progress percentage!"
            }
        else:
            return {
                "answer": f"You are currently focused on **{current_skill_name}** in the **{goal_title}** curriculum.",
                "syntax_or_framework": "CES Learning Workflow: Topic Checklist → Must-Know Topics → Practical Labs → Self-Evaluation",
                "code_example": f"// Current Learning Focus\nconst currentSkill = '{current_skill_name}';\nopenSkillCurriculum(currentSkill);",
                "practical_explanation": "Completing all topics sequentially ensures you build strong foundations before moving into practical code labs and evaluation quizzes.",
                "ces_recommendation": f"Open the {current_skill_name} topics list to select and start your first topic."
            }

    # ---------------------------------------------------------
    # 2. 'How is my progress?' / Status & Metrics
    # ---------------------------------------------------------
    if any(k in p_lower for k in [
        "how is my progress",
        "what is my progress",
        "my progress",
        "my learning status",
        "show my progress",
        "am i ready",
        "my status",
        "check my progress",
    ]):
        completed_count = len(completed)
        total_skills = context.get("total_skills", 1)
        skill_t_comp = context.get("skill_topics_completed", 0)
        skill_t_tot = context.get("skill_topics_total", 0)
        goal_t_comp = context.get("goal_topics_completed", 0)
        goal_t_tot = context.get("goal_topics_total", 0)
        latest_eval = context.get("latest_evaluation")
        cert_earned = context.get("certificate_earned", False)

        eval_str = f"{latest_eval['score']}/{latest_eval['total_questions']} ({latest_eval['percentage']}%)" if latest_eval else "Pending"
        cert_status_str = "Earned & Unlocked" if cert_earned else "In Progress"

        summary_answer = (
            f"In your **{goal_title}** path, you have completed **{completed_count} of {total_skills} skills** "
            f"with **{goal_t_comp}/{goal_t_tot} total curriculum topics mastered**. "
            f"You are actively working on **{current_skill_name}** ({skill_t_comp}/{skill_t_tot} topics completed)."
        )

        code_box = (
            f"// CES Candidate Progress Metrics\n"
            f"const userProgress = {{\n"
            f"  goal: \"{goal_title}\",\n"
            f"  skillsCompleted: \"{completed_count}/{total_skills}\",\n"
            f"  activeSkill: \"{current_skill_name}\",\n"
            f"  skillTopics: \"{skill_t_comp}/{skill_t_tot}\",\n"
            f"  diagnosticQuiz: \"{eval_str}\",\n"
            f"  certificateStatus: \"{cert_status_str}\"\n"
            f"}};\n"
            f"console.table(userProgress);"
        )

        if pending_topic:
            rec = f"Next Action: Complete your pending topic **'{pending_topic['title']}'** in the {current_skill_name} Must-Know checklist."
        elif not latest_eval:
            rec = f"Next Action: Take the {current_skill_name} Diagnostic Self-Evaluation quiz to test your mastery."
        elif not current_skill_data.get("interview_reviewed"):
            rec = f"Next Action: Review the {current_skill_name} Interview Preparation questions to finalize this skill."
        elif next_skill_name:
            rec = f"Next Action: Advance to your next skill: **{next_skill_name}**."
        else:
            rec = "Next Action: Proceed to the Capstone Final Interview & Overall Evaluation Hub to test overall readiness."

        return {
            "answer": summary_answer,
            "syntax_or_framework": "CES 4-Stage Completion Formula: Topics Checklist (100%) → Practical Labs → Evaluation Quiz (≥70%) → Interview Prep → Verified Certificate",
            "code_example": code_box,
            "practical_explanation": (
                f"To complete {current_skill_name} and unlock its official verified certificate, "
                f"you must complete all must-know topics, review practical labs, achieve 70%+ on the evaluation quiz, and review interview questions."
            ),
            "ces_recommendation": rec
        }

    # ---------------------------------------------------------
    # 3. Next Skill / Progression Questions
    # Handles: 'I completed HTML and CSS. What should I learn next?'
    # ---------------------------------------------------------
    if any(k in p_lower for k in [
        "what should i learn next",
        "what to learn next",
        "which skill next",
        "what next",
        "learn after",
        "next step",
        "what to learn",
        "i completed",
        "i finished",
        "completed html",
        "after css",
        "after javascript",
        "after react",
        "after python",
    ]):
        # Check if user mentioned specific skills in the prompt
        mentions_html = "html" in p_lower
        mentions_css = "css" in p_lower
        mentions_js = "javascript" in p_lower or "js" in p_lower
        mentions_react = "react" in p_lower
        mentions_python = "python" in p_lower
        mentions_fastapi = "fastapi" in p_lower

        # Sequence for Full Stack: HTML (0) -> CSS (1) -> JavaScript (2) -> React (3) -> Python (4) -> FastAPI (5)
        if mentions_fastapi:
            target_next = "Capstone Final Interview & Overall Evaluation"
        elif mentions_python:
            target_next = "FastAPI"
        elif mentions_react:
            target_next = "Python"
        elif mentions_js:
            target_next = "React"
        elif (mentions_html and mentions_css) or mentions_css:
            target_next = "JavaScript"
        elif mentions_html:
            target_next = "CSS"
        elif next_skill_name:
            target_next = next_skill_name
        elif completed and len(completed) >= context.get("total_skills", 1) and context.get("total_skills", 0) > 0:
            target_next = "Capstone Final Interview & Overall Evaluation"
        else:
            target_next = current_skill_name

        # Produce tailored response for target_next
        if target_next == "JavaScript":
            return {
                "answer": f"Having completed HTML and CSS, your immediate next milestone in the **{goal_title}** roadmap is **JavaScript**.",
                "syntax_or_framework": "Learning Progression: HTML (Structure) → CSS (Styling) → JavaScript (Interactivity) → React (Component Architecture)",
                "code_example": (
                    "// Dynamic Event Handling in JavaScript\n"
                    "const enrollBtn = document.querySelector('#enroll-btn');\n"
                    "enrollBtn.addEventListener('click', () => {\n"
                    "  console.log('Advancing to interactive web development in CES!');\n"
                    "});"
                ),
                "practical_explanation": (
                    "JavaScript connects your semantic HTML markup and CSS styling to real business logic. "
                    "It powers dynamic DOM updates, asynchronous data fetching with fetch/async-await, and responsive client-side event handling."
                ),
                "ces_recommendation": "Navigate to the JavaScript module in Career Explore Studio to begin its Must-Know topics, starting with ES6 variables, arrow functions, and DOM manipulation."
            }
        elif target_next == "React":
            return {
                "answer": f"Having completed JavaScript, your next milestone in the **{goal_title}** curriculum is **React**.",
                "syntax_or_framework": "Progression: JavaScript (ES6+ / Async) → React (Components, Hooks, State) → Python / Backend",
                "code_example": (
                    "import React, { useState } from 'react';\n\n"
                    "export default function SkillProgress({ name }) {\n"
                    "  const [done, setDone] = useState(false);\n"
                    "  return (\n"
                    "    <button onClick={() => setDone(!done)}>\n"
                    "      {name}: {done ? 'Mastered' : 'In Progress'}\n"
                    "    </button>\n"
                    "  );\n"
                    "}"
                ),
                "practical_explanation": (
                    "React abstracts imperative DOM queries into declarative component hierarchies. "
                    "You will manage state re-renders using hooks like useState and useEffect with fast virtual DOM reconciliation."
                ),
                "ces_recommendation": "Head to the React module in CES to practice component architecture, props, and useState in practical labs."
            }
        elif target_next == "Python":
            return {
                "answer": f"Having completed frontend foundations, your next milestone in the **{goal_title}** curriculum is **Python** for backend development.",
                "syntax_or_framework": "Progression: Frontend UI → Python Backend → FastAPI REST APIs → Full Stack Integration",
                "code_example": (
                    "def calculate_readiness(topics_done: int, total_topics: int) -> dict:\n"
                    "    pct = round((topics_done / total_topics) * 100, 1) if total_topics else 0.0\n"
                    "    return {'percentage': pct, 'ready_for_eval': pct >= 100.0}\n\n"
                    "print(calculate_readiness(6, 6))  # {'percentage': 100.0, 'ready_for_eval': True}"
                ),
                "practical_explanation": (
                    "Python gives you clean, expressive syntax to build backend business logic, database queries, and data processing routines. "
                    "Its standard library and typing support prepare you for building scalable APIs."
                ),
                "ces_recommendation": "Open the Python module in CES to cover Python data structures, functions, OOP, and unit testing."
            }
        elif target_next == "FastAPI":
            return {
                "answer": f"With Python mastered, your next milestone is **FastAPI** to build high-performance production REST APIs.",
                "syntax_or_framework": "FastAPI Workflow: Pydantic Schema Validation → Async Route Handlers → SQLAlchemy ORM → JSON Response",
                "code_example": (
                    "from fastapi import FastAPI\n"
                    "from pydantic import BaseModel\n\n"
                    "app = FastAPI()\n\n"
                    "class TopicStatus(BaseModel):\n"
                    "    topic_id: int\n"
                    "    is_completed: bool\n\n"
                    "@app.post('/api/topics/status')\n"
                    "def update_status(payload: TopicStatus):\n"
                    "    return {'status': 'saved', 'topic': payload.topic_id}"
                ),
                "practical_explanation": (
                    "FastAPI uses modern Python type hints to automatically validate HTTP payloads and generate interactive Swagger OpenAPI documentation at /docs."
                ),
                "ces_recommendation": "Open the FastAPI module in CES to build REST endpoints and connect them to SQLite database models."
            }
        elif target_next == "Capstone Final Interview & Overall Evaluation":
            return {
                "answer": f"Congratulations! You have completed all curriculum skills for **{goal_title}**. Your final step is the **Capstone Final Interview & Overall Evaluation**.",
                "syntax_or_framework": "Final Stage: Overall Cross-Skill Evaluation (≥75%) → Capstone 15 Must-Know Questions → Goal Certificate",
                "code_example": (
                    "// Capstone Readiness Verification\n"
                    "const readiness = {\n"
                    "  skillsCompleted: '100%',\n"
                    "  evaluationPassed: true,\n"
                    "  readyForCapstone: true\n"
                    "};\n"
                    "console.log('Ready for Capstone Final Interview Hub!');"
                ),
                "practical_explanation": (
                    "The Capstone interview tests cross-cutting architectural knowledge, debugging strategies, and full-stack integration under realistic interview conditions."
                ),
                "ces_recommendation": "Proceed to the Capstone Final Interview Prep Hub in CES to practice all 15 comprehensive cross-skill questions."
            }
        else:
            return {
                "answer": f"Based on your current progression in **{goal_title}**, continue directly with **{target_next}**.",
                "syntax_or_framework": "Curriculum Sequence: Must-Know Topics → Practical Labs → Self-Evaluation → Interview Prep",
                "code_example": f"// Next Step\nconst currentStep = '{target_next}';\nstartModule(currentStep);",
                "practical_explanation": f"Mastering {target_next} provides the requisite knowledge for upcoming roadmap milestones and unlocks your verified certificate.",
                "ces_recommendation": f"Open the {target_next} module in your CES roadmap to begin its structured learning stages."
            }

    # ---------------------------------------------------------
    # 4. 'Give me interview questions for my current skill'
    # ---------------------------------------------------------
    if "interview" in p_lower and any(k in p_lower for k in ["question", "prep", "practice", "my current skill", "current skill", "ask me", "give me"]):
        # Check questions in database for current skill
        questions = []
        if current_skill_id:
            questions = db.query(SkillInterviewQuestion).filter(
                SkillInterviewQuestion.skill_id == current_skill_id
            ).order_by(SkillInterviewQuestion.order_index.asc()).limit(2).all()

        if not questions:
            # Fallback query for any skill questions
            questions = db.query(SkillInterviewQuestion).limit(2).all()

        if questions:
            q_snippets = []
            for idx, q in enumerate(questions, 1):
                ans_preview = q.expected_answer[:130] + "..." if len(q.expected_answer) > 130 else q.expected_answer
                ex_preview = q.small_example or q.simple_syntax or "See full example in interview hub"
                q_snippets.append(
                    f"{idx}. {q.question}\n"
                    f"   Answer: {ans_preview}\n"
                    f"   Example / Syntax:\n"
                    f"   {ex_preview}"
                )
            code_block = "\n\n".join(q_snippets)

            return {
                "answer": f"Here are curated interview questions for **{current_skill_name}** from the CES question bank:",
                "syntax_or_framework": "Interview Formula: Direct Definition → Simple Syntax/Structure → Small Practical Example → Production Considerations",
                "code_example": code_block,
                "practical_explanation": (
                    questions[0].explanation if getattr(questions[0], "explanation", None) else
                    "Interviewers look for concise definitions followed immediately by real-world coding examples and awareness of common edge cases."
                ),
                "ces_recommendation": f"Open the Interview Preparation section for {current_skill_name} in CES to practice all questions with STAR-format model answers."
            }

    # ---------------------------------------------------------
    # 5. Technical Concept Lookups
    # ---------------------------------------------------------
    if "usestate" in p_lower:
        return {
            "answer": "useState is a core React Hook used to store and update reactive state data inside a functional component.",
            "syntax_or_framework": "const [state, setState] = useState(initialValue);",
            "code_example": (
                "import React, { useState } from 'react';\n\n"
                "export default function Counter() {\n"
                "  const [count, setCount] = useState(0);\n"
                "  return (\n"
                "    <button onClick={() => setCount(count + 1)}>\n"
                "      Count: {count}\n"
                "    </button>\n"
                "  );\n"
                "}"
            ),
            "practical_explanation": "Whenever `setCount` is called, React schedules a component re-render so the DOM reflects the updated value cleanly.",
            "ces_recommendation": "Review the React Practical Labs section in CES to build hands-on stateful widgets."
        }

    if "react" in p_lower:
        return {
            "answer": "React is an open-source JavaScript library for building fast, declarative, component-based user interfaces. It lets you construct complex web applications from modular, isolated pieces of code called components.",
            "syntax_or_framework": "function MyComponent({ title }) {\n  return <div><h1>{title}</h1></div>;\n}",
            "code_example": (
                "import React, { useState } from 'react';\n\n"
                "export default function SkillProgress() {\n"
                "  const [mastered, setMastered] = useState(false);\n"
                "  return (\n"
                "    <div className='card'>\n"
                "      <h3>React Fundamentals</h3>\n"
                "      <button onClick={() => setMastered(true)}>\n"
                "        {mastered ? 'Status: Mastered!' : 'Mark Completed'}\n"
                "      </button>\n"
                "    </div>\n"
                "  );\n"
                "}"
            ),
            "practical_explanation": "React uses a Virtual DOM and declarative state management to update only the specific UI nodes that change, avoiding expensive direct browser DOM recalculations.",
            "ces_recommendation": "Advance to the React module in Career Explore Studio to practice component composition, props, hooks, and responsive web apps."
        }

    if "javascript" in p_lower or "js" in p_lower:
        return {
            "answer": "JavaScript is the programming language that powers dynamic interactions, event handling, and data fetching in modern web applications.",
            "syntax_or_framework": "document.querySelector(selector).addEventListener('event', handler);",
            "code_example": (
                "const btn = document.querySelector('#explore-btn');\n"
                "btn.addEventListener('click', () => {\n"
                "  console.log('Starting learning journey in CES!');\n"
                "});"
            ),
            "practical_explanation": "JavaScript binds user interactions directly to DOM updates and handles asynchronous communication with backend APIs.",
            "ces_recommendation": "Check out the JavaScript Must-Know topics in your CES curriculum for ES6+, async/await, and DOM events."
        }

    if "python" in p_lower:
        return {
            "answer": "Python is a versatile, high-level programming language known for its clear readability, robust standard library, and powerful backend frameworks.",
            "syntax_or_framework": "def function_name(param: type) -> return_type:\n    return result",
            "code_example": (
                "def calculate_progress(completed: int, total: int) -> float:\n"
                "    if total == 0:\n"
                "        return 0.0\n"
                "    return round((completed / total) * 100, 1)\n\n"
                "print(calculate_progress(4, 5))  # Output: 80.0"
            ),
            "practical_explanation": "Type hints (`int`, `float`) and clean syntax make Python ideal for backend API services, data transformations, and automated testing.",
            "ces_recommendation": "Practice Python functions and data structures in the Python Practical Section of CES."
        }

    if "fastapi" in p_lower or "api" in p_lower or "backend" in p_lower:
        return {
            "answer": "FastAPI is a modern, high-performance Python web framework designed for building REST APIs with automatic Swagger documentation and Pydantic validation.",
            "syntax_or_framework": "@router.get('/endpoint', response_model=Schema)\ndef handler():\n    return data",
            "code_example": (
                "from fastapi import FastAPI\n\n"
                "app = FastAPI()\n\n"
                "@app.get('/api/skills')\n"
                "def list_skills():\n"
                "    return {'status': 'active', 'total': 6}"
            ),
            "practical_explanation": "FastAPI automatically validates incoming JSON schemas and generates interactive OpenAPI documentation at `/docs`.",
            "ces_recommendation": "Explore the FastAPI and API Integration modules in CES to inspect live backend endpoints."
        }

    if "html" in p_lower or "css" in p_lower:
        return {
            "answer": "HTML structures content semantically on the web, while CSS provides visual styling, layouts, responsive design, and animations.",
            "syntax_or_framework": "Selector { property: value; }",
            "code_example": (
                ".ces-badge {\n"
                "  display: inline-flex;\n"
                "  align-items: center;\n"
                "  padding: 0.5rem 1rem;\n"
                "  border-radius: 9999px;\n"
                "  background: #6366f1;\n"
                "  color: #ffffff;\n"
                "}"
            ),
            "practical_explanation": "Semantic markup and CSS variables create consistent design systems that adapt across mobile, tablet, and desktop screens.",
            "ces_recommendation": "Complete the HTML/CSS topic checklist in CES to unlock your frontend foundation certificate."
        }

    if any(k in p_lower for k in ["marketing", "leadership", "business", "communication", "project"]):
        return {
            "answer": "In professional environments, effective execution relies on clear value proposition, audience alignment, and structured communication frameworks.",
            "syntax_or_framework": "STAR Framework: Situation → Task → Action → Result",
            "code_example": (
                "Case Scenario:\n"
                "- Situation: Team faced duplicate roadmap priorities.\n"
                "- Action: Instituted weekly sprint alignment & clear ownership.\n"
                "- Result: Increased on-time delivery by 35%."
            ),
            "practical_explanation": "Structured communication ensures both technical and business stakeholders stay synchronized on project milestones and deliverables.",
            "ces_recommendation": "Review the non-technical case studies and leadership interview questions in CES to prepare for behavioral rounds."
        }

    # ---------------------------------------------------------
    # 6. Generic Fallback
    # ---------------------------------------------------------
    return {
        "answer": f"In Career Explore Studio, every concept is taught through direct explanation, practical examples, and interview readiness.",
        "syntax_or_framework": "Learn Topics → Practical Labs → Self-Evaluation → Interview Preparation",
        "code_example": (
            "// CES Structured Learning Flow\n"
            "const workflow = ['Learn Topics', 'Code Labs', 'Evaluation Quiz', 'Interview Prep'];\n"
            "workflow.forEach(stage => console.log(`Mastering ${stage}`));"
        ),
        "practical_explanation": "Following structured learning stages ensures durable retention and prepares you for real technical and behavioral interviews.",
        "ces_recommendation": f"Continue advancing in your enrolled {goal_title} roadmap in CES to unlock your official verified certificate."
    }


def ask_ai_mentor(
    db: Session,
    user_id: int,
    request: AIAskRequest
) -> AIAskResponse:
    """
    Master entrypoint for AI Assistant:
    1. Extracts sanitized CES user context.
    2. Attempts external Gemini call if API key is present.
    3. Seamlessly falls back to built-in CES Knowledge Engine if external key is not present or offline.
    4. Enforces the strict 4-part + recommendation response format.
    """
    ces_context = get_user_ces_context(db, user_id, request.skill_id, request.topic_id)
    prompt = request.prompt.strip()

    result_data = None

    # Check for configured backend API key
    api_key = settings.GEMINI_API_KEY or settings.AI_API_KEY
    if api_key:
        result_data = _call_gemini_api(api_key, prompt, ces_context)

    # If external API is not configured or failed, use built-in engine
    if not result_data:
        result_data = _built_in_ces_reasoner(db, prompt, ces_context)

    suggestions = get_suggested_prompts(db, user_id)

    # Build context_used for response metadata
    eval_data = ces_context.get("latest_evaluation")
    eval_status = "Passed" if (eval_data and eval_data.get("passed")) else ("Taken" if eval_data else "Pending")

    return AIAskResponse(
        query=prompt,
        answer=result_data.get("answer", "Here is the guidance for your question."),
        syntax_or_framework=result_data.get("syntax_or_framework"),
        code_example=result_data.get("code_example"),
        practical_explanation=result_data.get("practical_explanation"),
        ces_recommendation=result_data.get("ces_recommendation"),
        context_used={
            "goal_title": ces_context.get("goal_title"),
            "current_skill": ces_context.get("current_skill", {}).get("name") if ces_context.get("current_skill") else None,
            "current_topic": ces_context.get("current_topic", {}).get("title") if ces_context.get("current_topic") else None,
            "pending_topic": ces_context.get("pending_topic", {}).get("title") if ces_context.get("pending_topic") else None,
            "next_skill": ces_context.get("next_skill"),
            "completed_skills": ces_context.get("completed_skills", []),
            "topics_progress": f"{ces_context.get('skill_topics_completed', 0)}/{ces_context.get('skill_topics_total', 0)}",
            "evaluation_status": eval_status,
            "certificate_earned": ces_context.get("certificate_earned", False),
        },
        suggestions=suggestions
    )
