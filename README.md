<<<<<<< HEAD
# CAREER EXPLORE STUDIO
**Personal Skill Learning, Roadmap & Interview Preparation Platform**

A production-ready, full-stack, data-driven web application to guide users through career goals, skill acquisition, interactive practical exercises, self-evaluation, and interview preparation for both technical and non-technical career paths.

---

## 🌟 Platform Highlights & Capabilities

- **Curated Multi-Domain Career Goals**: Full Stack Developer, Data Scientist, Cloud DevOps Engineer, Product Manager, UI/UX Designer, and Digital Marketing Specialist.
- **Guided Skill Roadmap**: Step-by-step skill mastery with strict prerequisite progression, must-know topic tags, and practical exercises.
- **Interactive Practical Learning Labs**: Code playgrounds with syntax highlighting, step-by-step guides, expected outcomes, tips, and common pitfalls.
- **Skill-Level Self-Evaluations**: Diagnostic multiple-choice evaluations with instant scoring, topic-level weakness analysis, and personalized improvement suggestions.
- **Targeted Skill Interview Prep**: Curated interview questions categorized by difficulty (Basic, Intermediate, Advanced) with structured STAR answers, tips, and common mistakes.
- **Overall Cross-Skill Readiness Diagnostic**: Comprehensive cross-domain assessments evaluating readiness across all skills within a career goal, identifying readiness tiers (Early Explorer, Competent Learner, Interview Ready, Master Candidate).
- **Capstone Final Interview Hub (15 Must-Know Questions)**: Exactly 15 high-impact questions per career path (5 Core/Fundamental, 5 Scenario/Practical, 5 Advanced/System Design) with active practice trackers and completion metrics.
- **Comprehensive Candidate Dashboard & Certificate**: Visual radar readiness charts, achievement badge unlocks, stats metrics, and exportable/printable **Certificate of Readiness**.
- **WCAG 2.1 AA Accessibility & Responsive Polish**: Skip-to-content links, ARIA live regions, focus-visible outlines, mobile navigation drawers, and robust error boundaries.

---

## 🛠️ Technology Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend** | React 18, Vite 5, React Router 6 | Component-driven SPA, fast HMR, responsive CSS design system |
| **Icons & UI** | Lucide React | Lightweight, accessible iconography |
| **Backend** | Python 3.14, FastAPI 0.142 | High-performance asynchronous REST API with automatic OpenAPI docs |
| **Database & ORM** | SQLite & SQLAlchemy 2.0 | Clean ORM design with auto-seeding, fully portable to PostgreSQL |
| **Security** | Direct `bcrypt` & PyJWT | Secure password hashing without legacy passlib dependencies |
| **Testing** | Python `unittest` & Starlette TestClient | 33 comprehensive automated end-to-end and regression tests |

---

## 📁 Project Structure

```
CAREER EXPLORE STUDIO/
├── backend/
│   ├── app/
│   │   ├── api/                     # Modular API routers
│   │   │   ├── auth.py              # Register, login, /me, profile summary
│   │   │   ├── goals.py             # Career goals list, detail, and selection
│   │   │   ├── skills.py            # Skills, topics, practical labs, evaluations, interview prep
│   │   │   ├── progress.py          # Topic toggling, skill completion, readiness dashboard
│   │   │   ├── overall_evaluation.py# Cross-skill evaluation questions & diagnostic scoring
│   │   │   ├── final_interview.py   # Capstone 15 must-know interview questions & practice tracker
│   │   │   ├── health.py            # Health diagnostics & system metrics
│   │   │   └── router.py            # Master router aggregator
│   │   ├── core/                    # Security, tokens, settings
│   │   │   ├── config.py            # App settings (CORS, JWT secret, DB URLs)
│   │   │   └── security.py          # Direct bcrypt hashing and JWT token handlers
│   │   ├── database/                # Database configuration
│   │   │   ├── database.py          # SQLAlchemy engine and session dependency
│   │   │   └── seed_data.py         # Complete initial database seeder
│   │   ├── models/                  # SQLAlchemy ORM models (User, Goal, Skill, Topic, etc.)
│   │   └── schemas/                 # Pydantic v2 validation schemas
│   ├── requirements.txt             # Python backend dependencies
│   ├── run.py                       # Development server runner (Uvicorn)
│   └── test_api.py                  # Master test suite (33 automated test cases)
│
└── frontend/
    ├── src/
    │   ├── components/              # Shared UI components
    │   │   ├── Common/              # ErrorBoundary, LoadingState, EmptyState, Modal
    │   │   ├── Evaluation/          # EvaluationQuestion, ScoreSummary
    │   │   ├── Interview/           # InterviewQuestionCard, CategoryFilter
    │   │   ├── Layout/              # AppLayout, Navbar, Sidebar, Footer, MobileNav
    │   │   └── Roadmap/             # WorkflowProgressIndicator, SkillRoadmapNode
    │   ├── context/                 # React Contexts (AuthContext, ToastContext)
    │   ├── pages/                   # Application Views
    │   │   ├── Auth/                # Login, Register, Profile
    │   │   ├── Dashboard/           # Comprehensive Progress Dashboard & Certificate
    │   │   ├── FinalInterview/      # Capstone 15 Must-Know Interview Prep Hub
    │   │   ├── Goals/               # Career Goal Selection Hub
    │   │   ├── Home/                # Interactive Splash & Feature Showcase
    │   │   ├── OverallEvaluation/   # Cross-Skill Diagnostic Evaluation
    │   │   └── Skills/              # Overview, Topics, Practical Lab, Skill Evaluation, Skill Interview
    │   ├── services/                # Axios API client with auth interceptors
    │   ├── App.jsx                  # Main router configuration and protected route guards
    │   ├── index.css                # Global responsive theme and accessibility styles
    │   └── main.jsx                 # Application entrypoint
    ├── package.json                 # Frontend dependencies and npm scripts
    └── vite.config.js               # Vite config with backend proxy
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+** (Python 3.14 supported)
- **Node.js 18+** & **npm**

### 2. Backend Setup & Startup
```bash
# From the project root:
# Windows (PowerShell/CMD):
backend\.venv\Scripts\python.exe backend\run.py

# Or with global Python:
python -m venv backend/.venv
backend/.venv/Scripts/pip install -r backend/requirements.txt
backend/.venv/Scripts/python backend/run.py
```
- **Backend API**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/api/docs`

### 3. Frontend Setup & Development Server
```bash
# In another terminal window:
cd frontend
npm install
npm run dev
```
- **Web Application**: `http://localhost:5173`

---

## 🧪 Testing & Verification

The project includes **110 passing automated tests** across 6 specialized audit suites covering the full application journey, database isolation, AI grounding, responsive design, accessibility, and production quality standards:

```bash
# 1. Master Phase 14 Production Readiness Audit (12 tests)
backend\.venv\Scripts\python.exe scratch\test_phase14_production_readiness.py

# 2. Master Phase 13 Integration & Security Suite (9 tests)
backend\.venv\Scripts\python.exe scratch\test_phase13_master_integration.py

# 3. Master Backend API Regression Suite (33 tests)
backend\.venv\Scripts\python.exe backend\test_api.py

# 4. Multi-Tenant Database Isolation Audit (9 tests)
backend\.venv\Scripts\python.exe scratch\test_user_isolation_phase10.py

# 5. AI Mentor Context Grounding Audit (11 tests)
backend\.venv\Scripts\python.exe scratch\test_ai_context.py

# 6. Responsive UI & CSS Breakpoint Audit (8 tests)
backend\.venv\Scripts\python.exe scratch\test_responsive_ui.py

# 7. Phase 12 Accessibility, Strings & Polish Audit (28 tests)
backend\.venv\Scripts\python.exe scratch\test_phase12_polish.py
```
**Expected Result**: All 110 tests pass with 0 errors.

### Frontend Production Build
```bash
cd frontend
npm run build
```
**Expected Result**:
```
✓ 1936 modules transformed.
dist/index.html                   1.22 kB │ gzip:   0.70 kB
dist/assets/index-DvlRRPlx.css   12.15 kB │ gzip:   3.39 kB
dist/assets/index-C2yibGC6.js   439.22 kB │ gzip: 105.15 kB
✓ built in ~25s (0 errors, 0 warnings)
```

---

## 📋 Comprehensive 14-Phase Implementation Summary

1. **Phase 1: Project Setup & Unified App Shell** — Virtual environment, FastAPI structure, database models, initial seed script, and `/api/health`.
2. **Phase 2: Streamlined Intro Flow & Core Authentication** — Smooth Splash screen without lag or duplicate renders, direct bcrypt hashing, JWT tokens, and protected routes.
3. **Phase 3: CES Brand Identity & Unified Logo System** — Unified white Compass badge logo across all headers, cards, and splash screens.
4. **Phase 4: 4-Part Interview Questions with Syntax & Practical Copy** — Curated question explanations, syntax structures, small practical examples, and scenario breakdowns.
5. **Phase 5: 4-Stage Skill Completion & Certificate Generation** — Strict prerequisite progression across Topics, Practical Labs, Diagnostic Evaluation, and Interview Prep.
6. **Phase 6: Official Certificate Verification & Modal Experience** — Secure server-side validation, `CES-SKILL-*` certificate generation, and public verification endpoints.
7. **Phase 7: CES AI Search Assistant Frontend** — Accessible search bar modal with prompt suggestions, loading states, and keyboard escape dismiss.
8. **Phase 8: FastAPI AI Backend Service & Provider Integration** — High-performance AI service supporting Gemini with structured technical and non-technical responses.
9. **Phase 9: Personalized AI Learning Context & SQLite Grounding** — Contextual AI prompt injection grounded in enrolled goal, active skill, completed topics, and quiz metrics.
10. **Phase 10: Database Integrity Audit & Multi-User Isolation** — Comprehensive tenant isolation across all tables; 403 Forbidden enforcement on unauthorized cross-user queries.
11. **Phase 11: Complete Responsive UI Improvement Across All Pages** — 7-tier breakpoint system (320px–1920px), 44px min-height touch targets, and `.stack-on-mobile` toolbars.
12. **Phase 12: Performance Optimization, Loading/Error States & Accessibility** — In-memory 30s TTL cache with request deduplication, memoization, localized error boundaries, and exact Section 13 strings.
13. **Phase 13: Complete Integration Testing & Full-Stack Regressions** — End-to-end candidate journey validation, negative path security, and 100% test pass rate across 98 tests.
14. **Phase 14: Final Production-Quality Review & Build Verification** — Complete 12-standard quality audit, verified production bundle, zero console errors, and production-ready state.

---

## 📄 License
MIT License. Built for career explorers, students, and aspiring software professionals.
=======
# career-explore-studio
3rd time
>>>>>>> 05848dcab42419ef1aa7f16ed7641e6d3c8fe1a0
