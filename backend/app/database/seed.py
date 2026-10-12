import json
from sqlalchemy.orm import Session
from app.models.goal import Goal
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.practical import PracticalContent
from app.models.evaluation import EvaluationQuestion
from app.models.skill_interview import SkillInterviewQuestion
from app.models.overall_evaluation import OverallGoalEvaluationQuestion
from app.models.final_interview import GoalFinalInterviewQuestion
from app.models.user import User
from app.core.security import get_password_hash
from app.database.seed_final_interview_data import INITIAL_FINAL_INTERVIEW_QUESTIONS_DATA

INITIAL_GOALS_DATA = [
    {
        "slug": "full-stack-developer",
        "title": "Full Stack Developer",
        "category": "Technical",
        "icon": "Code",
        "description": "Master complete modern web application development from interactive browser interfaces to scalable backend APIs and relational databases.",
        "career_relevance": "Full Stack Developers are among the highest-demand tech roles globally, capable of architecting and shipping end-to-end software products independently or within agile engineering teams.",
        "skills": [
            {
                "slug": "html-semantics",
                "name": "HTML & Semantic Web Structure",
                "category": "Frontend Core",
                "description": "Understand document structure, accessibility semantics, SEO tags, forms, and modern HTML5 elements.",
                "is_technical": True,
                "order_index": 1,
                "what_is_it": "HyperText Markup Language (HTML5) is the fundamental standard building block of the World Wide Web. It provides the structured skeleton for every webpage and web application.",
                "why_important": "Clean, semantic HTML ensures high search engine visibility (SEO), assists screen readers for accessibility (a11y), and establishes a resilient foundation for styling and scripting.",
                "where_used": "Used across all web browsers, hybrid mobile applications, progressive web apps, email templates, and web-based documentation.",
                "benefits": "Universal browser support, zero external build overhead, native accessibility support, and rapid rendering performance.",
                "challenges": "Browser inconsistencies in edge HTML features, maintaining strict accessibility standards (WCAG 2.1), and avoiding excessive div nesting ('div soup').",
                "prerequisites": "Basic computer literacy and understanding of how web browsers fetch and display text documents.",
                "career_relevance": "Every full-stack software engineer must be capable of architecting clean, standards-compliant, and accessible page templates.",
                "topics": [
                    {"title": "HTML5 Document Structure & DOCTYPE", "description": "Understanding html, head, body, meta charsets, viewport tags, and page metadata.", "is_must_know": True, "order_index": 1, "estimated_minutes": 15},
                    {"title": "Semantic Content Elements", "description": "Structuring layouts with header, nav, main, article, section, aside, and footer.", "is_must_know": True, "order_index": 2, "estimated_minutes": 20},
                    {"title": "Headings & Text Typography Elements", "description": "H1-H6 hierarchy, paragraphs, blockquotes, strong, em, and span elements.", "is_must_know": False, "order_index": 3, "estimated_minutes": 10},
                    {"title": "Lists, Tables & Structured Data", "description": "Ordered/unordered lists, description lists, and accessible data tables with thead/tbody.", "is_must_know": False, "order_index": 4, "estimated_minutes": 20},
                    {"title": "Hyperlinks & Document Navigation", "description": "Absolute vs relative URLs, target attributes, download attribute, and anchor bookmark links.", "is_must_know": True, "order_index": 5, "estimated_minutes": 15},
                    {"title": "Images & Responsive Media", "description": "Img element, alt descriptions, picture tag, srcset, svg icons, and modern lazy loading.", "is_must_know": True, "order_index": 6, "estimated_minutes": 25},
                    {"title": "Forms & Modern Input Controls", "description": "Form elements, input types (text, email, password, number), textarea, select, and datalists.", "is_must_know": True, "order_index": 7, "estimated_minutes": 30},
                    {"title": "Form Validation & Native Attributes", "description": "Required, pattern, min/max, step, maxlength, and custom validity styling with :user-valid.", "is_must_know": True, "order_index": 8, "estimated_minutes": 20},
                    {"title": "Web Accessibility & ARIA Essentials", "description": "ARIA roles, aria-labels, aria-expanded, keyboard focusability, and screen reader friendliness.", "is_must_know": True, "order_index": 9, "estimated_minutes": 35},
                    {"title": "Audio, Video & Embedded Content", "description": "Native HTML5 audio/video players, iframe sandboxing, and web component slots.", "is_must_know": False, "order_index": 10, "estimated_minutes": 20},
                ],
                "practical": [
                    {
                        "title": "Accessible Semantic Document Structure",
                        "content_type": "code_syntax",
                        "language": "html",
                        "code_snippet": "<!-- Semantic Web Page Layout -->\n<header role=\"banner\" class=\"site-header\">\n  <nav aria-label=\"Primary Navigation\">\n    <ul>\n      <li><a href=\"#dashboard\">Dashboard</a></li>\n      <li><a href=\"#reports\">Reports</a></li>\n      <li><a href=\"#settings\">Settings</a></li>\n    </ul>\n  </nav>\n</header>\n\n<main id=\"main-content\" role=\"main\">\n  <article aria-labelledby=\"article-heading\">\n    <h1 id=\"article-heading\">Semantic HTML5 Architecture</h1>\n    <p>Using semantic elements ensures screen readers and crawlers parse document hierarchy cleanly.</p>\n    <section aria-labelledby=\"section-heading\">\n      <h2 id=\"section-heading\">Why Semantic Structure Matters</h2>\n      <p>Semantic tags improve SEO, WCAG compliance, and developer maintainability.</p>\n    </section>\n  </article>\n</main>\n\n<footer role=\"contentinfo\">\n  <p>&copy; 2026 Career Explore Studio. All rights reserved.</p>\n</footer>",
                        "explanation": "Semantic tags like <header>, <nav>, <main>, <article>, and <footer> convey explicit layout hierarchy to screen readers and search crawlers without relying on arbitrary <div> soup.",
                        "real_world_context": "High-traffic web platforms (GitHub, Stripe, MDN) structure pages strictly with semantic landmarks to satisfy WCAG 2.1 AA accessibility and reliable keyboard navigation.",
                        "activity_prompt": "Refactor a legacy page full of <div class='header'>, <div class='nav-bar'>, and <div class='content-card'> into semantic HTML5 landmark tags with proper aria-labelledby attributes.",
                        "solution_or_guide": "Replace outer <div class='header'> with <header>, wrapper <div class='nav-bar'> with <nav aria-label='Main'>, and card container <div class='content-card'> with <article aria-labelledby='card-title'>. Add <a href='#main-content' class='skip-link'>Skip to Content</a> at the top of the body for keyboard users.",
                        "order_index": 1
                    },
                    {
                        "title": "Accessible Form Validation with ARIA Live Announcements",
                        "content_type": "exercise",
                        "language": "html",
                        "code_snippet": "<!-- Accessible Form Validation Example -->\n<form id=\"profile-form\" novalidate>\n  <div class=\"form-group\">\n    <label for=\"work-email\">Work Email <span aria-hidden=\"true\">*</span></label>\n    <input \n      type=\"email\" \n      id=\"work-email\" \n      name=\"email\" \n      required \n      aria-describedby=\"email-hint email-error\"\n      placeholder=\"engineer@company.com\"\n      autocomplete=\"email\"\n    />\n    <small id=\"email-hint\" class=\"hint\">Use your verified corporate domain.</small>\n    <span id=\"email-error\" class=\"error-msg\" role=\"alert\" aria-live=\"assertive\"></span>\n  </div>\n  <button type=\"submit\">Save Changes</button>\n</form>",
                        "explanation": "Using aria-describedby links both the informational hint and live error region to the input element so assistive devices read validation states automatically.",
                        "real_world_context": "Used in enterprise authentication, billing, and checkout forms where screen readers must immediately alert users if an input fails validation.",
                        "activity_prompt": "Write client-side validation logic that toggles aria-invalid='true' and injects an accessible error message into the role='alert' element when an invalid email is submitted.",
                        "solution_or_guide": "Listen to the form submit event: if (!input.value.includes('@')) { input.setAttribute('aria-invalid', 'true'); errorSpan.textContent = 'Please enter a valid work email address.'; input.focus(); } else { input.removeAttribute('aria-invalid'); errorSpan.textContent = ''; }",
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "css-responsive-design",
                "name": "CSS3 & Modern Responsive Design",
                "category": "Frontend Core",
                "description": "Master CSS Grid, Flexbox, media queries, CSS variables, transitions, and responsive mobile-first layouts.",
                "is_technical": True,
                "order_index": 2,
                "what_is_it": "Cascading Style Sheets (CSS3) controls the visual presentation, formatting, spatial layout, typography, and responsive adaptability of web applications across all screen sizes.",
                "why_important": "Modern users expect responsive, polished, and intuitive digital interfaces on everything from mobile phones to high-resolution desktop monitors.",
                "where_used": "Every web application, component library, responsive marketing site, design system, and modern frontend framework.",
                "benefits": "Declarative presentation, GPU-accelerated smooth animations, theme switching via CSS custom properties, and fluid responsive adaptability without JavaScript.",
                "challenges": "Managing cascade specificity, avoiding layout shifts (CLS), container vs viewport sizing, and cross-browser quirks.",
                "prerequisites": "HTML5 semantic structure.",
                "career_relevance": "Crucial for delivering professional, pixel-perfect user experiences that prevent visual regressions and optimize Core Web Vitals.",
                "topics": [
                    {"title": "The Box Model & Box Sizing", "description": "Content, padding, border, margin, and box-sizing: border-box fundamentals.", "is_must_know": True, "order_index": 1, "estimated_minutes": 15},
                    {"title": "CSS Selectors & Specificity Hierarchy", "description": "Class, ID, attribute selectors, pseudo-classes (:hover, :focus-visible), and cascade rules.", "is_must_know": True, "order_index": 2, "estimated_minutes": 25},
                    {"title": "CSS Custom Properties (Variables)", "description": "Declaring --color variables, dynamic theming, dark mode overrides, and inheritance.", "is_must_know": True, "order_index": 3, "estimated_minutes": 20},
                    {"title": "Modern Flexbox Layouts", "description": "Flex direction, justify-content, align-items, flex-grow/shrink, and responsive wrapping.", "is_must_know": True, "order_index": 4, "estimated_minutes": 30},
                    {"title": "CSS Grid Systems", "description": "Grid template columns, repeat(), minmax(), grid-gap, auto-fit/fill, and area templates.", "is_must_know": True, "order_index": 5, "estimated_minutes": 35},
                    {"title": "Responsive Media Queries & Breakpoints", "description": "Mobile-first approach, min-width queries, fluid clamp() typography, and orientation.", "is_must_know": True, "order_index": 6, "estimated_minutes": 25},
                    {"title": "Positioning Models (Sticky, Absolute, Fixed)", "description": "Static, relative, absolute, fixed, and sticky positioning contexts with z-index stacking.", "is_must_know": True, "order_index": 7, "estimated_minutes": 20},
                    {"title": "Transitions & Keyframe Animations", "description": "CSS transitions, easing functions, keyframe animations, and will-change optimizations.", "is_must_know": False, "order_index": 8, "estimated_minutes": 25},
                    {"title": "Modern Glassmorphism & Backdrop Filters", "description": "Translucent card styling, backdrop-filter: blur(), and border-highlight techniques.", "is_must_know": False, "order_index": 9, "estimated_minutes": 15},
                    {"title": "Container Queries & Size-Aware Styling", "description": "Styling components based on their parent container width rather than viewport.", "is_must_know": False, "order_index": 10, "estimated_minutes": 30},
                ],
                "practical": [
                    {
                        "title": "Modern Fluid Grid with auto-fit, minmax, and Clamp Typography",
                        "content_type": "code_syntax",
                        "language": "css",
                        "code_snippet": ".metrics-grid {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));\n  gap: 1.5rem;\n  padding: 1.5rem;\n}\n\n.metric-card {\n  background: rgba(255, 255, 255, 0.9);\n  backdrop-filter: blur(12px);\n  border: 1px solid rgba(226, 232, 240, 0.8);\n  border-radius: 12px;\n  padding: 1.5rem;\n  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);\n}\n\n.metric-card h3 {\n  font-size: clamp(1.1rem, 2vw, 1.5rem);\n  font-weight: 700;\n  color: #0f172a;\n  margin-bottom: 0.5rem;\n}",
                        "explanation": "repeat(auto-fit, minmax(280px, 1fr)) computes column counts dynamically based on parent container width, eliminating the need for rigid media query breakpoints.",
                        "real_world_context": "SaaS analytics portals (Datadog, Stripe Dashboard) use this pattern to display analytical widgets that gracefully adapt between smartphones, tablets, and 4K displays.",
                        "activity_prompt": "Create a 3-column pricing card layout that automatically wraps to a single column on mobile viewports while ensuring all cards maintain equal height.",
                        "solution_or_guide": "Use display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); align-items: stretch;. Inside each card use flexbox: display: flex; flex-direction: column; justify-content: space-between; so the CTA button stays pinned to the bottom.",
                        "order_index": 1
                    },
                    {
                        "title": "Sticky Header with Glassmorphism Backdrop Blur",
                        "content_type": "exercise",
                        "language": "css",
                        "code_snippet": ".app-header {\n  position: sticky;\n  top: 0;\n  z-index: 50;\n  background: rgba(255, 255, 255, 0.8);\n  backdrop-filter: blur(16px);\n  -webkit-backdrop-filter: blur(16px);\n  border-bottom: 1px solid rgba(226, 232, 240, 0.6);\n  padding: 0.75rem 1.5rem;\n  transition: box-shadow 0.2s ease, background 0.2s ease;\n}\n\n.app-header.scrolled {\n  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);\n}",
                        "explanation": "Combining position: sticky with backdrop-filter: blur() creates the frosted-glass aesthetic popularized by macOS and modern web design systems.",
                        "real_world_context": "Apple, Linear, and Vercel sites use blurred sticky headers to preserve scroll context while maintaining clear separation between navigation and content.",
                        "activity_prompt": "Implement a sticky navigation header that remains pinned during vertical scrolling, blurring the underlying content without obscuring it.",
                        "solution_or_guide": "Assign position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px); background-color: rgba(255, 255, 255, 0.85);. Ensure no ancestor element has overflow: hidden, which breaks sticky positioning.",
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "javascript-es6",
                "name": "JavaScript ES6+ & Async Programming",
                "category": "Frontend Core",
                "description": "Learn closures, modern arrow functions, array operations, Promises, async/await, and Fetch API.",
                "is_technical": True,
                "order_index": 3,
                "what_is_it": "JavaScript is the universal programming language of the web. It powers dynamic client-side interactivity, state management, asynchronous data fetching, and application logic.",
                "why_important": "Modern web development is impossible without deep JavaScript proficiency. It is the language behind modern frontend frameworks (React, Vue) and runs backend runtimes like Node.js.",
                "where_used": "Interactive frontend web apps, full-stack Node.js servers, mobile React Native apps, Electron desktop apps, and serverless edge functions.",
                "benefits": "Dynamic execution, non-blocking asynchronous event loop, massive global open-source package ecosystem (npm), and cross-platform flexibility.",
                "challenges": "Asynchronous concurrency pitfalls, loose typing edge cases, memory leaks in uncleaned event listeners, and scope closures.",
                "prerequisites": "Basic understanding of variables, conditional logic, and HTML/CSS fundamentals.",
                "career_relevance": "The indispensable cornerstone of frontend and full-stack software development interviews and daily engineering work.",
                "topics": [
                    {"title": "Variables & Scope (let, const, var)", "description": "Block scope, function scope, hoisting, temporal dead zone, and best practices.", "is_must_know": True, "order_index": 1, "estimated_minutes": 15},
                    {"title": "Primitive & Reference Data Types", "description": "Strings, numbers, booleans, null, undefined, symbols, and mutable objects/arrays.", "is_must_know": True, "order_index": 2, "estimated_minutes": 20},
                    {"title": "Operators & Expressions", "description": "Strict equality (=== vs ==), arithmetic, logical operators (&&, ||, ??), and optional chaining (?.).", "is_must_know": True, "order_index": 3, "estimated_minutes": 15},
                    {"title": "Conditional Statements & Switch", "description": "if/else branching, ternary operators (? :), and pattern matching with switch statements.", "is_must_know": False, "order_index": 4, "estimated_minutes": 15},
                    {"title": "Loops & Iteration (for, while, for...of)", "description": "Standard loops, for...of for iterables, for...in for object keys, break, and continue.", "is_must_know": False, "order_index": 5, "estimated_minutes": 20},
                    {"title": "Functions & Arrow Functions", "description": "Function declarations, expressions, arrow syntax, default parameters, rest parameters, and this binding.", "is_must_know": True, "order_index": 6, "estimated_minutes": 25},
                    {"title": "Arrays & High-Order Array Methods", "description": "map, filter, reduce, find, some, every, forEach, slice, splice, and array destructuring.", "is_must_know": True, "order_index": 7, "estimated_minutes": 35},
                    {"title": "Objects, Methods & Destructuring", "description": "Key-value pairs, object methods, computed property names, Object.entries/keys/values, and spread operator.", "is_must_know": True, "order_index": 8, "estimated_minutes": 30},
                    {"title": "The DOM & Element Selection", "description": "querySelector, querySelectorAll, getElementById, traversing parent/child nodes, and manipulating classes.", "is_must_know": True, "order_index": 9, "estimated_minutes": 25},
                    {"title": "Event Handling & Event Delegation", "description": "addEventListener, event object, event bubbling, event capturing, preventDefault, and stopPropagation.", "is_must_know": True, "order_index": 10, "estimated_minutes": 30},
                    {"title": "ES6 Modules (import & export)", "description": "Named exports, default exports, module bundling concepts, and code splitting.", "is_must_know": False, "order_index": 11, "estimated_minutes": 20},
                    {"title": "Asynchronous JavaScript & The Event Loop", "description": "Call stack, Web APIs, task queue, microtask queue, callbacks, and non-blocking execution.", "is_must_know": True, "order_index": 12, "estimated_minutes": 35},
                    {"title": "Promises (resolve, reject, chaining)", "description": "Creating promises, .then(), .catch(), .finally(), Promise.all, Promise.race, and Promise.allSettled.", "is_must_know": True, "order_index": 13, "estimated_minutes": 30},
                    {"title": "Async / Await Syntax & Error Handling", "description": "Writing clean async functions, awaiting promises, and handling exceptions with try/catch/finally blocks.", "is_must_know": True, "order_index": 14, "estimated_minutes": 25},
                    {"title": "Fetch API & Network HTTP Requests", "description": "Sending GET and POST requests, handling JSON payloads, HTTP headers, status codes, and error parsing.", "is_must_know": True, "order_index": 15, "estimated_minutes": 35},
                ],
                "practical": [
                    {
                        "title": "Resilient Async API Client with AbortController Timeout",
                        "content_type": "code_syntax",
                        "language": "javascript",
                        "code_snippet": "async function fetchJsonWithTimeout(endpoint, timeoutMs = 8000) {\n  const controller = new AbortController();\n  const timer = setTimeout(() => controller.abort(), timeoutMs);\n\n  try {\n    const response = await fetch(endpoint, {\n      signal: controller.signal,\n      headers: {\n        'Accept': 'application/json',\n        'Content-Type': 'application/json'\n      }\n    });\n\n    if (!response.ok) {\n      throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);\n    }\n\n    const payload = await response.json();\n    return { data: payload, error: null };\n  } catch (err) {\n    if (err.name === 'AbortError') {\n      return { data: null, error: `Request timed out after ${timeoutMs}ms` };\n    }\n    return { data: null, error: err.message };\n  } finally {\n    clearTimeout(timer);\n  }\n}",
                        "explanation": "Using AbortController alongside setTimeout ensures in-flight network requests terminate cleanly if the backend or network latency spikes.",
                        "real_world_context": "Production applications cannot afford frozen UI loading spinners when a third-party microservice or gateway times out.",
                        "activity_prompt": "Write a function fetchMultipleEndpoints(urls) that triggers concurrent requests with Promise.allSettled() and collects only successful responses into an array.",
                        "solution_or_guide": "Use: const responses = await Promise.allSettled(urls.map(u => fetch(u).then(r => r.json()))); return responses.filter(r => r.status === 'fulfilled').map(r => r.value);",
                        "order_index": 1
                    },
                    {
                        "title": "Immutable Array Data Transformations with Map, Filter & Reduce",
                        "content_type": "exercise",
                        "language": "javascript",
                        "code_snippet": "// Sample candidate interview evaluations\nconst candidateEvaluations = [\n  { candidate: \"Alex\", skill: \"React\", score: 88, passed: true },\n  { candidate: \"Jordan\", skill: \"FastAPI\", score: 62, passed: false },\n  { candidate: \"Alex\", skill: \"FastAPI\", score: 91, passed: true },\n  { candidate: \"Taylor\", skill: \"React\", score: 79, passed: true },\n  { candidate: \"Jordan\", skill: \"React\", score: 85, passed: true }\n];\n\n// Calculate average passing score per candidate using reduce\nconst candidateSummaries = candidateEvaluations\n  .filter(record => record.passed)\n  .reduce((acc, curr) => {\n    if (!acc[curr.candidate]) {\n      acc[curr.candidate] = { total: 0, count: 0 };\n    }\n    acc[curr.candidate].total += curr.score;\n    acc[curr.candidate].count += 1;\n    return acc;\n  }, {});\n\nconst averages = Object.entries(candidateSummaries).map(([candidate, stats]) => ({\n  candidate,\n  averagePassingScore: Math.round(stats.total / stats.count)\n}));\n\nconsole.log(averages);",
                        "explanation": "Higher-order functional methods (filter, reduce, map) enable expressive, declarative data processing pipelines without mutating original datasets.",
                        "real_world_context": "Client-side dashboards frequently process raw REST JSON payloads to calculate analytics, group metric cards, and prepare chart series.",
                        "activity_prompt": "Given an array of transactions with amounts and categories, write a reduce function that computes total spend per category.",
                        "solution_or_guide": "Use transactions.reduce((acc, t) => { acc[t.category] = (acc[t.category] || 0) + t.amount; return acc; }, {});",
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "react-architecture",
                "name": "React Architecture & State Management",
                "category": "Frontend Framework",
                "description": "Build single-page web applications using functional components, hooks, custom state, and client routing.",
                "is_technical": True,
                "order_index": 4,
                "what_is_it": "React is an industry-standard declarative, component-based JavaScript library for building user interfaces with virtual DOM reconciliation.",
                "why_important": "Powers the vast majority of modern enterprise web applications, enabling modular, reusable component architectures and clean reactive state management.",
                "where_used": "Enterprise dashboards, social platforms, SaaS applications, and interactive web tools.",
                "benefits": "Component reusability, unidirectional data flow, vast ecosystem of tools and libraries, and strong developer ergonomics.",
                "challenges": "Managing re-renders, state synchronization, deep prop drilling, and choosing the right state management approach.",
                "prerequisites": "JavaScript ES6+ fundamentals, destructuring, arrow functions, and Promise handling.",
                "career_relevance": "The most widely requested frontend library across engineering hiring roadmaps and technical interviews.",
                "topics": [
                    {"title": "JSX Syntax & Component Composition", "description": "Embedding JavaScript expressions in JSX, fragment containers, and nesting components.", "is_must_know": True, "order_index": 1, "estimated_minutes": 20},
                    {"title": "Props & Component Communication", "description": "Passing data downward, prop destructuring, default props, and children prop composition.", "is_must_know": True, "order_index": 2, "estimated_minutes": 20},
                    {"title": "useState Hook & Local State", "description": "Declaring reactive state variables, functional updates, and immutability rules.", "is_must_know": True, "order_index": 3, "estimated_minutes": 25},
                    {"title": "useEffect Hook & Lifecycle Synchronization", "description": "Dependency arrays, side effects (API calls, event listeners), and cleanup functions.", "is_must_know": True, "order_index": 4, "estimated_minutes": 35},
                    {"title": "Conditional Rendering & List Rendering", "description": "Ternary operators, logical AND shortcuts, mapping arrays to JSX, and the key prop rule.", "is_must_know": True, "order_index": 5, "estimated_minutes": 20},
                    {"title": "Controlled Forms & Input Handling", "description": "Binding inputs to component state, form submission handlers, and multi-input state patterns.", "is_must_know": True, "order_index": 6, "estimated_minutes": 25},
                    {"title": "useRef & DOM Element References", "description": "Accessing native DOM elements, storing mutable values without triggering re-renders.", "is_must_know": False, "order_index": 7, "estimated_minutes": 20},
                    {"title": "useContext Hook & Global State", "description": "Creating context providers, avoiding prop drilling, and sharing auth/theme state globally.", "is_must_know": True, "order_index": 8, "estimated_minutes": 30},
                    {"title": "Custom React Hooks", "description": "Extracting reusable stateful logic into custom hook functions (e.g. useFetch, useLocalStorage).", "is_must_know": False, "order_index": 9, "estimated_minutes": 30},
                    {"title": "React Router 6 Client-Side Routing", "description": "BrowserRouter, Routes, Route, Link, NavLink, useNavigate, and protected route wrappers.", "is_must_know": True, "order_index": 10, "estimated_minutes": 35},
                ],
                "practical": [
                    {
                        "title": "Custom Data Hook with Lifecycle Cleanup & Cache",
                        "content_type": "code_syntax",
                        "language": "javascript",
                        "code_snippet": "import { useState, useEffect } from 'react';\n\nexport function useApiResource(endpoint) {\n  const [data, setData] = useState(null);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState(null);\n\n  useEffect(() => {\n    let isSubscribed = true;\n    const controller = new AbortController();\n\n    async function fetchData() {\n      setLoading(true);\n      setError(null);\n      try {\n        const response = await fetch(endpoint, { signal: controller.signal });\n        if (!response.ok) throw new Error(`HTTP Error ${response.status}`);\n        const result = await response.json();\n        if (isSubscribed) setData(result);\n      } catch (err) {\n        if (err.name !== 'AbortError' && isSubscribed) {\n          setError(err.message);\n        }\n      } finally {\n        if (isSubscribed) setLoading(false);\n      }\n    }\n\n    fetchData();\n\n    return () => {\n      isSubscribed = false;\n      controller.abort();\n    };\n  }, [endpoint]);\n\n  return { data, loading, error };\n}",
                        "explanation": "Encapsulating API data fetching inside a reusable custom hook abstracts away boilerplate. The abort cleanup prevents memory leak warnings when a user navigates away mid-request.",
                        "real_world_context": "Every major React team uses custom hooks (useUser, useProjects, useTheme) to decouple backend communication from UI presentation.",
                        "activity_prompt": "Build a useLocalStorage(key, initialValue) hook that synchronizes a React state variable with window.localStorage.",
                        "solution_or_guide": "Initialize state with localStorage.getItem(key) fallback. In a setter function or useEffect, call localStorage.setItem(key, JSON.stringify(value)) whenever value changes.",
                        "order_index": 1
                    },
                    {
                        "title": "Optimized Context Provider with Action Dispatching",
                        "content_type": "exercise",
                        "language": "javascript",
                        "code_snippet": "import React, { createContext, useContext, useState, useMemo } from 'react';\n\nconst CareerContext = createContext(null);\n\nexport function CareerProvider({ children }) {\n  const [activeGoal, setActiveGoal] = useState(null);\n  const [activeSkill, setActiveSkill] = useState(null);\n\n  const contextValue = useMemo(() => ({\n    activeGoal,\n    activeSkill,\n    selectGoal: (goal) => setActiveGoal(goal),\n    selectSkill: (skill) => setActiveSkill(skill),\n    resetSelection: () => {\n      setActiveGoal(null);\n      setActiveSkill(null);\n    }\n  }), [activeGoal, activeSkill]);\n\n  return (\n    <CareerContext.Provider value={contextValue}>\n      {children}\n    </CareerContext.Provider>\n  );\n}\n\nexport function useCareer() {\n  const ctx = useContext(CareerContext);\n  if (!ctx) throw new Error(\"useCareer must be used within a CareerProvider\");\n  return ctx;\n}",
                        "explanation": "Wrapping the context value in useMemo prevents unnecessary re-renders of consuming components unless activeGoal or activeSkill actually changes.",
                        "real_world_context": "Critical for global state like authentication, active user preferences, and theme providers to prevent whole-tree render thrashing.",
                        "activity_prompt": "Add a toast notification queue system into this context provider with showToast(message, type) and dismissToast(id) actions.",
                        "solution_or_guide": "Add const [toasts, setToasts] = useState([]). Define showToast(msg, type) to append { id: Date.now(), msg, type } and auto-remove after 4 seconds with setTimeout. Include toasts and methods in the context memo.",
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "python-fastapi",
                "name": "Python & FastAPI REST APIs",
                "category": "Backend Core",
                "description": "Develop high-performance RESTful APIs, dependency injection, and Pydantic data validation.",
                "is_technical": True,
                "order_index": 5,
                "what_is_it": "FastAPI is a modern, high-performance Python web framework for building RESTful APIs, leveraging Python type hints, Starlette, and Pydantic validation.",
                "why_important": "One of the fastest-growing backend frameworks in tech, offering asynchronous concurrency, automated interactive OpenAPI documentation, and minimal boilerplate.",
                "where_used": "High-throughput microservices, machine learning model APIs, SaaS backend services, and scalable web applications.",
                "benefits": "Asynchronous ASGI performance on par with NodeJS/Go, automatic interactive Swagger docs, type safety, and clean dependency injection.",
                "challenges": "Understanding async/await concurrency, managing thread pools for blocking operations, and configuring CORS properly.",
                "prerequisites": "Python core language syntax and HTTP fundamentals.",
                "career_relevance": "Key requirement for modern Python backend, full-stack, and AI engineering roles.",
                "topics": [
                    {"title": "FastAPI Application Setup & ASGI Servers", "description": "FastAPI app instance, running with Uvicorn, reload mode, and server lifespan events.", "is_must_know": True, "order_index": 1, "estimated_minutes": 20},
                    {"title": "Route Handlers & HTTP Methods", "description": "GET, POST, PUT, DELETE, and PATCH decorators with path parameters and query parameters.", "is_must_know": True, "order_index": 2, "estimated_minutes": 25},
                    {"title": "Pydantic Schemas & Request Validation", "description": "Defining request/response models, field constraints, type hints, and automated 422 errors.", "is_must_know": True, "order_index": 3, "estimated_minutes": 30},
                    {"title": "FastAPI Dependency Injection (Depends)", "description": "Creating reusable dependencies, database session injection, and authentication guards.", "is_must_know": True, "order_index": 4, "estimated_minutes": 35},
                    {"title": "CORS Middleware & Security Headers", "description": "Configuring CORSMiddleware, allowed origins, HTTP methods, and cookie credentials.", "is_must_know": True, "order_index": 5, "estimated_minutes": 20},
                    {"title": "Error Handling & HTTPExceptions", "description": "Raising structured HTTPExceptions, custom error response schemas, and exception handlers.", "is_must_know": True, "order_index": 6, "estimated_minutes": 20},
                    {"title": "Modular Routing with APIRouter", "description": "Splitting endpoints across feature modules and mounting into a central API router.", "is_must_know": True, "order_index": 7, "estimated_minutes": 25},
                    {"title": "Background Tasks & Asynchronous Operations", "description": "Running background execution tasks and async async def vs sync def functions.", "is_must_know": False, "order_index": 8, "estimated_minutes": 25},
                ],
                "practical": [
                    {
                        "title": "Dependency Injection with Authentication Guard & Pydantic Validation",
                        "content_type": "code_syntax",
                        "language": "python",
                        "code_snippet": "from fastapi import APIRouter, Depends, HTTPException, status\nfrom pydantic import BaseModel, Field, EmailStr\nfrom sqlalchemy.orm import Session\nfrom app.database.database import get_db\nfrom app.api.deps import get_current_user\nfrom app.models.user import User\n\nrouter = APIRouter(prefix=\"/projects\", tags=[\"projects\"])\n\nclass ProjectCreateRequest(BaseModel):\n    title: str = Field(..., min_length=3, max_length=120)\n    description: str = Field(..., min_length=10)\n    tags: list[str] = Field(default_factory=list)\n\n@router.post(\"/\", status_code=status.HTTP_201_CREATED)\ndef create_user_project(\n    payload: ProjectCreateRequest,\n    current_user: User = Depends(get_current_user),\n    db: Session = Depends(get_db)\n):\n    project = Project(\n        user_id=current_user.id,\n        title=payload.title,\n        description=payload.description,\n        tags=\",\".join(payload.tags)\n    )\n    db.add(project)\n    db.commit()\n    db.refresh(project)\n    return {\"message\": \"Project created successfully\", \"project_id\": project.id}",
                        "explanation": "FastAPI automatically validates JSON payloads against ProjectCreateRequest. Depends(get_current_user) validates JWT auth tokens, while Depends(get_db) injects and tears down DB sessions cleanly.",
                        "real_world_context": "Used across modern production Python microservices to decouple auth validation, database session lifecycles, and request deserialization.",
                        "activity_prompt": "Write a dependency verify_role(required_role: str) that inspects current_user.role and raises an HTTP 403 Forbidden exception if the user does not possess the required permission.",
                        "solution_or_guide": "Define a closure: def require_role(role: str): def dependency(current_user: User = Depends(get_current_user)): if current_user.role != role: raise HTTPException(status_code=403, detail='Insufficient permissions') return current_user; return dependency. Use it via Depends(require_role('admin')).",
                        "order_index": 1
                    },
                    {
                        "title": "Automated Error Handling & Custom HTTPException Handler",
                        "content_type": "exercise",
                        "language": "python",
                        "code_snippet": "from fastapi import FastAPI, Request, status\nfrom fastapi.responses import JSONResponse\n\nclass BusinessRuleViolation(Exception):\n    def __init__(self, message: str, code: str):\n        self.message = message\n        self.code = code\n\napp = FastAPI()\n\n@app.exception_handler(BusinessRuleViolation)\nasync def business_rule_exception_handler(request: Request, exc: BusinessRuleViolation):\n    return JSONResponse(\n        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,\n        content={\n            \"success\": False,\n            \"error_code\": exc.code,\n            \"detail\": exc.message,\n            \"path\": str(request.url)\n        }\n    )",
                        "explanation": "FastAPI exception handlers catch domain-specific exceptions raised anywhere in route handlers or service layers and serialize them into predictable, standardized JSON error responses.",
                        "real_world_context": "Fintech and SaaS companies rely on standardized error schemas so mobile apps and frontend clients can display user-friendly error dialogs.",
                        "activity_prompt": "Create a custom exception EntityNotFoundException(entity_name, entity_id) and an exception handler that returns a 404 response with a helpful diagnostic payload.",
                        "solution_or_guide": "Subclass Exception with entity_name and entity_id. Register @app.exception_handler(EntityNotFoundException) to return JSONResponse status 404 with {'error': f'{exc.entity_name} with ID {exc.entity_id} was not found'}.",
                        "order_index": 2
                    }
                ]
            },
        ],
    },
    {
        "slug": "business-administration",
        "title": "Business Administration",
        "category": "Business",
        "icon": "Briefcase",
        "description": "Gain holistic business acumen across corporate management, financial budgeting, marketing, operations, and organizational leadership.",
        "career_relevance": "Equips professionals for executive, operational, and management leadership roles across startups, corporations, and non-profit enterprises.",
        "skills": [
            {
                "slug": "business-management",
                "name": "Business Management & Strategy",
                "category": "Management",
                "description": "Analyze business environments, organizational structures, strategic planning, and competitive positioning.",
                "is_technical": False,
                "order_index": 1,
                "what_is_it": "Business management is the art and science of coordinating, directing, and optimizing an organization's resources, people, and strategy to achieve commercial success.",
                "why_important": "Effective management determines whether a business flourishes, adapts to competitive market shifts, or fails due to operational inefficiency.",
                "where_used": "Across corporate departments, executive teams, consulting firms, venture-backed startups, and growing small businesses.",
                "benefits": "Strategic clarity, enhanced operational efficiency, streamlined decision making, and measurable team accountability.",
                "challenges": "Managing uncertainty, balancing short-term quarterly revenue with long-term research, and mitigating organizational friction.",
                "prerequisites": "Interest in commerce, critical reasoning, and team collaboration.",
                "career_relevance": "Foundational competence for general managers, project directors, startup founders, and management consultants.",
                "topics": [
                    {"title": "Organizational Structures & Governance", "description": "Functional, divisional, flat, and matrix organizational hierarchies and accountability lines.", "is_must_know": True, "order_index": 1, "estimated_minutes": 25},
                    {"title": "SWOT Analysis & Environmental Scanning", "description": "Strengths, Weaknesses, Opportunities, and Threats assessment in commercial markets.", "is_must_know": True, "order_index": 2, "estimated_minutes": 30},
                    {"title": "Porter's Five Forces & Industry Competition", "description": "Assessing supplier power, buyer leverage, competitive rivalry, and threats of substitution.", "is_must_know": True, "order_index": 3, "estimated_minutes": 35},
                    {"title": "Goal Setting with OKRs & KPIs", "description": "Crafting Objectives and Key Results, performance metrics, and alignment with corporate strategy.", "is_must_know": True, "order_index": 4, "estimated_minutes": 25},
                    {"title": "Change Management Frameworks", "description": "Kotter's 8-step model, ADKAR methodology, overcoming organizational inertia and resistance.", "is_must_know": False, "order_index": 5, "estimated_minutes": 30},
                    {"title": "Corporate Ethics, Compliance & Governance", "description": "Fiduciary duties, ESG guidelines, ethical dilemmas, and corporate transparency.", "is_must_know": True, "order_index": 6, "estimated_minutes": 20},
                ],
                "practical": [
                    {
                        "title": "Corporate Turnaround: Managing Disruptive Market Entry",
                        "content_type": "scenario",
                        "language": None,
                        "code_snippet": None,
                        "explanation": "When an established business faces a sudden decline in market share due to an aggressive tech disruptor, management must immediately stabilize runway cashflow, protect core high-margin accounts, and reallocate capital toward digital transformation.",
                        "real_world_context": "A regional logistics company with $15M annual revenue experienced a 22% client churn in two quarters after an automated freight aggregator entered the market. The executive team initiated an urgent 90-day turnaround strategy.",
                        "activity_prompt": "Formulate a 3-phase strategic response: 1) Immediate cash preservation & top-tier client retention, 2) Operational streamlining, and 3) A clear internal communication framework to prevent staff panic.",
                        "solution_or_guide": "1. Phase 1 (Days 1-30): Conduct executive triage on the top 20% accounts that generate 80% of revenue, offering customized SLA guarantees and loyalty rebates. Pause discretionary capital expenditures to extend runway. 2. Phase 2 (Days 31-60): Consolidate underutilized warehouse routes and partner with a digital dispatch API provider to match competitor booking speeds. 3. Phase 3 (Days 61-90): Host weekly transparent company-wide town halls, establish measurable team OKRs, and celebrate early client win-backs to bolster morale.",
                        "order_index": 1
                    },
                    {
                        "title": "Cascading Corporate Strategy into Measurable Departmental OKRs",
                        "content_type": "case_study",
                        "language": None,
                        "code_snippet": None,
                        "explanation": "Objectives and Key Results (OKRs) ensure company-wide alignment by connecting executive vision to frontline team deliverables. An Objective defines a qualitative aspirational ambition; Key Results define verifiable, numeric milestones.",
                        "real_world_context": "Scaling companies frequently suffer from organizational drift where engineering builds features that sales cannot monetize. OKRs align disparate departments toward cohesive commercial outcomes.",
                        "activity_prompt": "Draft an OKR set for a retail banking institution transitioning to a digital-first mobile banking experience, targeting 100,000 active digital banking users within two quarters.",
                        "solution_or_guide": "Objective: Establish the bank as the premier mobile banking choice for digital-native customers. Key Result 1: Launch mobile onboarding with biometric KYC, reducing account creation time under 4 minutes. Key Result 2: Acquire 100,000 verified active accounts by Q4 with a Day-30 retention rate above 60%. Key Result 3: Maintain App Store and Google Play customer satisfaction ratings above 4.7 stars across at least 10,000 user reviews.",
                        "order_index": 2
                    }
                ]
            },
            {
                "slug": "marketing-fundamentals",
                "name": "Marketing & Customer Acquisition",
                "category": "Marketing",
                "description": "Understand target audiences, value propositions, market segmentation, and modern campaign design.",
                "is_technical": False,
                "order_index": 2,
                "what_is_it": "Marketing is the systematic process of discovering, creating, and delivering value to meet the needs of a target market at a profit.",
                "why_important": "Even the best product fails without a clear marketing narrative, customer acquisition strategy, and brand resonance.",
                "where_used": "Product launches, consumer brands, B2B enterprise sales, e-commerce, and growth engineering.",
                "benefits": "Predictable customer acquisition funnels, higher customer lifetime value (LTV), and brand loyalty.",
                "challenges": "High advertising acquisition costs, customer fatigue, saturated channels, and measuring true marketing attribution.",
                "prerequisites": "Understanding basic consumer behavior and business value propositions.",
                "career_relevance": "Crucial for commercial leaders, marketing directors, brand managers, and business operators.",
                "topics": [
                    {"title": "Market Segmentation & Target Audience Identification", "description": "Demographic, psychographic, behavioral, and geographic segmentation principles.", "is_must_know": True, "order_index": 1, "estimated_minutes": 25},
                    {"title": "Crafting a Compelling Value Proposition", "description": "Positioning statements, unique selling points (USP), and solving customer pain points.", "is_must_know": True, "order_index": 2, "estimated_minutes": 25},
                    {"title": "The Marketing Funnel Architecture", "description": "Top of Funnel (Awareness), Middle (Consideration), and Bottom (Conversion/Retention).", "is_must_know": True, "order_index": 3, "estimated_minutes": 30},
                    {"title": "The 4 Ps Marketing Mix (Product, Price, Place, Promotion)", "description": "Designing integrated go-to-market strategies using the marketing mix framework.", "is_must_know": True, "order_index": 4, "estimated_minutes": 25},
                    {"title": "Customer Acquisition Cost (CAC) vs Lifetime Value (LTV)", "description": "Financial unit economics of marketing, payback periods, and ROI calculations.", "is_must_know": True, "order_index": 5, "estimated_minutes": 30},
                    {"title": "Digital Distribution Channels & Content Strategy", "description": "Evaluating search, social, paid, email, and partner channels for maximum conversion.", "is_must_know": False, "order_index": 6, "estimated_minutes": 25},
                ],
                "practical": [
                    {
                        "title": "Customer Acquisition Funnel Diagnostics & CAC/LTV Realignment",
                        "content_type": "case_study",
                        "language": None,
                        "code_snippet": None,
                        "explanation": "A healthy acquisition funnel balances top-of-funnel brand discovery with high-converting bottom-of-funnel triggers. When Customer Acquisition Cost (CAC) approaches Customer Lifetime Value (LTV), unit economics deteriorate and marketing burns capital without creating enterprise value.",
                        "real_world_context": "A B2B SaaS startup spending $40,000/month on search ads discovered their blended CAC was $210, while average 6-month customer churn capped LTV at $180. The marketing leadership had to overhaul the channel mix.",
                        "activity_prompt": "Design an integrated marketing strategy to lower CAC by 40% and increase 12-month customer LTV to $350 through content marketing, partner referral programs, and email onboarding sequences.",
                        "solution_or_guide": "1. Channel Shift: Reallocate 35% of paid PPC budget to high-intent SEO content hubs and free interactive ROI calculator tools that attract organic leads with compounding lifetime value. 2. Conversion Optimization: Deploy an automated 7-step behavior-triggered email onboarding sequence showcasing product value moments to double trial-to-paid conversion from 4% to 8%. 3. Expansion & Retention: Implement an in-app customer referral program giving both parties a free month, and introduce an annual billing discount (yielding immediate cash flow and locking in 12-month retention).",
                        "order_index": 1
                    },
                    {
                        "title": "Go-to-Market Positioning & Unique Value Proposition Formulation",
                        "content_type": "scenario",
                        "language": None,
                        "code_snippet": None,
                        "explanation": "A compelling Value Proposition explicitly identifies the target buyer, names the urgent problem they face, explains the unique solution, and demonstrates quantifiable differentiation compared to existing market alternatives.",
                        "real_world_context": "An AI-powered document review startup was struggling to sell to legal firms because their messaging was overly technical ('Neural Transformer Parsing') rather than client-benefit oriented.",
                        "activity_prompt": "Rewrite the company's positioning statement and create a concise pitch matrix addressing the needs of three distinct buyer personas: Managing Partners (Cost/Risk), Associates (Hours Saved), and IT Directors (Data Security).",
                        "solution_or_guide": "Core Value Proposition: 'Cut contract turnaround time by 70% with enterprise-grade legal AI that never trains on client data.' 1. Managing Partner Pitch: Focus on firm billable efficiency and zero breach liability with SOC2 Type II compliance. 2. Associate Pitch: Eliminate tedious 2 AM manual clause redlining so attorneys can focus on strategic client counsel. 3. IT Director Pitch: Highlight on-premises deployment options, end-to-end encryption, and role-based access control.",
                        "order_index": 2
                    }
                ]
            },
        ],
    },
]

INITIAL_EVALUATIONS_DATA = {
    "html-semantics": [
        {
            "question_text": "Which HTML5 landmark element should encapsulate the central content unique to the document, excluding repeating headers, sidebars, or footers?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "<section>"},
                {"id": "B", "text": "<main>"},
                {"id": "C", "text": "<article>"},
                {"id": "D", "text": "<content>"}
            ],
            "correct_option": "B",
            "explanation": "<main> represents the dominant content of the <body>. Each document must contain only one visible <main> landmark, directly conveying page purpose to assistive technologies.",
            "topic_area": "Semantic Elements",
            "order_index": 1
        },
        {
            "question_text": "To ensure an image is accessible to users navigating with screen readers without causing broken speech flow, what attribute is strictly required?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "title"},
                {"id": "B", "text": "name"},
                {"id": "C", "text": "alt"},
                {"id": "D", "text": "aria-hidden=\"false\""}
            ],
            "correct_option": "C",
            "explanation": "The alt attribute provides alternative text description. For purely decorative graphics, alt=\"\" allows screen readers to safely bypass the element without reading raw image file URLs.",
            "topic_area": "Accessibility & ARIA",
            "order_index": 2
        },
        {
            "question_text": "A user complains that pressing the Tab key bypasses an interactive custom dropdown component. How should this be resolved semantically?",
            "question_type": "problem_solving",
            "options": [
                {"id": "A", "text": "Add CSS cursor: pointer to the container div"},
                {"id": "B", "text": "Wrap the div in an anchor without an href attribute"},
                {"id": "C", "text": "Use a native <button> or attach tabindex=\"0\" and handle keyboard Enter/Space keydown events"},
                {"id": "D", "text": "Add an inline onclick attribute directly to the div"}
            ],
            "correct_option": "C",
            "explanation": "Native buttons have built-in keyboard focus and click synthesis. If implementing a custom widget, tabindex=\"0\" coupled with keyboard event handlers is required for WCAG compliance.",
            "topic_area": "Keyboard Navigation & Focus",
            "order_index": 3
        },
        {
            "question_text": "Which combination of attributes ensures an email form field cannot be submitted blank and alerts users with modern browser constraint validation?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "validate=\"true\" pattern=\"email\""},
                {"id": "B", "text": "type=\"email\" required aria-required=\"true\""},
                {"id": "C", "text": "strict=\"on\" check=\"email\""},
                {"id": "D", "text": "data-required=\"yes\""}
            ],
            "correct_option": "B",
            "explanation": "type=\"email\" validates proper syntax, required blocks empty form submission natively, and aria-required=\"true\" communicates the requirement clearly to screen readers.",
            "topic_area": "Form Validation",
            "order_index": 4
        }
    ],
    "css-responsive-design": [
        {
            "question_text": "In modern CSS layouts, what is the primary architectural difference between CSS Grid and Flexbox?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "Flexbox is only for mobile screens; Grid is only for desktop monitors"},
                {"id": "B", "text": "Flexbox is one-dimensional (row OR column), while Grid is two-dimensional (rows AND columns simultaneously)"},
                {"id": "C", "text": "CSS Grid is deprecated in favor of CSS Subgrid and Flexbox"},
                {"id": "D", "text": "Flexbox cannot handle wrapping items onto multiple lines"}
            ],
            "correct_option": "B",
            "explanation": "Flexbox coordinates alignment along a single axis (row or column), whereas CSS Grid establishes full two-dimensional layout systems with explicit row and column tracks.",
            "topic_area": "Grid & Flexbox Architecture",
            "order_index": 1
        },
        {
            "question_text": "Which CSS rule prevents elements with fixed widths and padding from accidentally causing horizontal scrollbars on mobile devices?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "* { box-sizing: border-box; }"},
                {"id": "B", "text": "* { display: inline-block; }"},
                {"id": "C", "text": "* { overflow: scroll; }"},
                {"id": "D", "text": "* { float: left; }"}
            ],
            "correct_option": "A",
            "explanation": "box-sizing: border-box ensures padding and borders are absorbed within the defined width and height rather than expanding outwards, preventing unexpected horizontal page overflow.",
            "topic_area": "Box Model & Sizing",
            "order_index": 2
        },
        {
            "question_text": "A stylesheet uses min-width media queries starting from default mobile styles and progressively adding desktop enhancements. What approach does this represent?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "Desktop-first graceful degradation"},
                {"id": "B", "text": "Mobile-first progressive enhancement"},
                {"id": "C", "text": "Adaptive viewport emulation"},
                {"id": "D", "text": "Subgrid isolation"}
            ],
            "correct_option": "B",
            "explanation": "Mobile-first architecture defines clean baseline styles for compact screens, then utilizes @media (min-width: ...) to progressively layer complex multi-column structures as screen real estate increases.",
            "topic_area": "Media Queries & Mobile-First",
            "order_index": 3
        },
        {
            "question_text": "When styling a reusable widget whose layout needs to respond based on its parent container's width rather than the overall browser viewport, what modern CSS feature should you use?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "@media (max-width: ...)"},
                {"id": "B", "text": "@container (min-width: ...)"},
                {"id": "C", "text": "window.addEventListener('resize')"},
                {"id": "D", "text": "z-index coordinate stacking"}
            ],
            "correct_option": "B",
            "explanation": "CSS Container Queries (@container) allow components to query their parent container's dimensions, making components truly self-contained and context-independent across any layout slot.",
            "topic_area": "Modern Responsive Features",
            "order_index": 4
        }
    ],
    "javascript-es6": [
        {
            "question_text": "What distinguishes `let` and `const` declarations from legacy `var` in modern JavaScript?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "`let` and `const` attach automatically to the global window object"},
                {"id": "B", "text": "`let` and `const` have block scope and temporal dead zone (TDZ) protection, whereas `var` is function-scoped and hoisted with undefined"},
                {"id": "C", "text": "`var` executes faster in V8 engine than block-scoped bindings"},
                {"id": "D", "text": "`const` makes all object keys deeply immutable"}
            ],
            "correct_option": "B",
            "explanation": "let and const are block-scoped ({ ... }) and throw a ReferenceError if accessed before declaration due to the Temporal Dead Zone (TDZ). var leaks outside blocks and hoists as undefined.",
            "topic_area": "Scope & Variable Declarations",
            "order_index": 1
        },
        {
            "question_text": "What happens when an unhandled Promise rejection occurs inside an `async` function that lacks a `try/catch` block?",
            "question_type": "problem_solving",
            "options": [
                {"id": "A", "text": "The browser execution freezes completely"},
                {"id": "B", "text": "The function automatically retries three times"},
                {"id": "C", "text": "The returned Promise rejects and bubbles up, potentially triggering an 'UnhandledPromiseRejection' event"},
                {"id": "D", "text": "The execution silently converts into synchronous execution"}
            ],
            "correct_option": "C",
            "explanation": "Async functions always return a Promise. Any uncaught error or rejected await inside rejects that returned Promise, requiring caller handling via .catch() or outer try/catch.",
            "topic_area": "Promises & Async/Await",
            "order_index": 2
        },
        {
            "question_text": "Which array method transforms an array of numbers `[1, 2, 3, 4]` into a single accumulated total without mutating the source array?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "numbers.forEach()"},
                {"id": "B", "text": "numbers.filter()"},
                {"id": "C", "text": "numbers.reduce()"},
                {"id": "D", "text": "numbers.splice()"}
            ],
            "correct_option": "C",
            "explanation": "Array.prototype.reduce() executes a reducer callback over all elements, returning a single accumulated result while keeping the original array purely intact.",
            "topic_area": "Array Methods & Immutability",
            "order_index": 3
        },
        {
            "question_text": "Why is the object spread operator (`const clone = { ...original }`) classified as a shallow clone rather than a deep clone?",
            "question_type": "understanding",
            "options": [
                {"id": "A", "text": "It only copies primitive string values and ignores integers"},
                {"id": "B", "text": "Nested objects or arrays are copied by reference, so mutating `clone.details.city` will also mutate `original.details.city`"},
                {"id": "C", "text": "It converts all method functions to null"},
                {"id": "D", "text": "It is restricted to objects with fewer than 10 keys"}
            ],
            "correct_option": "B",
            "explanation": "Spread copies only top-level enumerable properties. Any nested arrays or objects are copied by pointer reference, requiring structuredClone() or deep-copy utilities for full data isolation.",
            "topic_area": "Object References & Memory",
            "order_index": 4
        }
    ],
    "react-architecture": [
        {
            "question_text": "Why must React Hook calls (such as `useState` or `useEffect`) never be placed inside conditionals, loops, or nested functions?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "Conditions degrade rendering performance in the V8 compiler"},
                {"id": "B", "text": "React relies on the exact identical order of Hook invocations across renders to preserve component state"},
                {"id": "C", "text": "JavaScript forbids function calls within if statements"},
                {"id": "D", "text": "Hooks can only be registered on DOM window mount"}
            ],
            "correct_option": "B",
            "explanation": "React tracks Hook state using an internal array indexed by the order in which Hooks are invoked during each render. Changing the call order corrupts component state alignment.",
            "topic_area": "Hooks & Component Lifecycle",
            "order_index": 1
        },
        {
            "question_text": "What is the primary risk of omitting variables from the dependency array of a `useEffect` hook?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "Immediate JSX compilation crash"},
                {"id": "B", "text": "Stale closures where the effect callback captures outdated prop or state snapshots"},
                {"id": "C", "text": "CSS animation frame drops"},
                {"id": "D", "text": "Automatic unmounting of the parent route"}
            ],
            "correct_option": "B",
            "explanation": "JavaScript closures preserve variables from the render cycle in which they were created. Omitting dependencies prevents the effect from refreshing when those variables change, creating stale state bugs.",
            "topic_area": "Stale Closures & Effects",
            "order_index": 2
        },
        {
            "question_text": "A large data dashboard experiences typing lag because an entire data grid re-renders on every keystroke. What is the most targeted optimization?",
            "question_type": "problem_solving",
            "options": [
                {"id": "A", "text": "Migrate the entire application to Vanilla JS"},
                {"id": "B", "text": "Lift state up to the root App component"},
                {"id": "C", "text": "Isolate the input state into its own local component and wrap heavy data grid components with React.memo"},
                {"id": "D", "text": "Disable all CSS transitions"}
            ],
            "correct_option": "C",
            "explanation": "State colocation prevents parent re-renders when the input changes. React.memo prevents the heavy data grid from re-rendering as long as its incoming props remain unchanged.",
            "topic_area": "Performance Optimization",
            "order_index": 3
        },
        {
            "question_text": "Why should stable, unique entity IDs be used for React `key` props instead of array indices when rendering dynamic lists?",
            "question_type": "understanding",
            "options": [
                {"id": "A", "text": "Array indices are invalid syntax in JSX elements"},
                {"id": "B", "text": "Using array indices causes DOM reconciliation bugs, lost input focus, and mismatched state when items are inserted, deleted, or reordered"},
                {"id": "C", "text": "Keys are solely used by CSS pseudo-selectors"},
                {"id": "D", "text": "Indices are stripped out during the build step"}
            ],
            "correct_option": "B",
            "explanation": "React uses keys to track identity across renders. When items are inserted or removed, array indices shift, causing React to mismatch component instances with their corresponding DOM nodes.",
            "topic_area": "Reconciliation & Keys",
            "order_index": 4
        }
    ],
    "python-fastapi": [
        {
            "question_text": "How does FastAPI achieve high concurrent throughput compared to traditional synchronous WSGI frameworks like Flask or Django?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "FastAPI compiles Python code directly into native C++ binaries"},
                {"id": "B", "text": "FastAPI is built on Starlette and ASGI, leveraging Python's native `asyncio` event loop for non-blocking I/O"},
                {"id": "C", "text": "FastAPI disables database transactions"},
                {"id": "D", "text": "FastAPI only supports GET HTTP requests"}
            ],
            "correct_option": "B",
            "explanation": "FastAPI runs on ASGI servers (like Uvicorn) and Starlette. When handling network, database, or disk I/O with `await`, Python's asyncio event loop pauses that coroutine and processes other concurrent requests.",
            "topic_area": "ASGI & Concurrency",
            "order_index": 1
        },
        {
            "question_text": "In FastAPI, what primary role do Pydantic schemas fulfill in API route definitions?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "Direct execution of SQL table migrations"},
                {"id": "B", "text": "Request body validation, type coercion, JSON response serialization, and automatic OpenAPI documentation generation"},
                {"id": "C", "text": "Transport layer TLS certificate encryption"},
                {"id": "D", "text": "Managing thread pools in the OS kernel"}
            ],
            "correct_option": "B",
            "explanation": "Pydantic models declare data structure contracts. FastAPI validates incoming payloads, automatically formats error responses (422), serializes outgoing data, and publishes Swagger/OpenAPI docs.",
            "topic_area": "Pydantic & Request Validation",
            "order_index": 2
        },
        {
            "question_text": "Why should you use `Depends(get_db)` rather than importing a global SQLAlchemy session object directly in route handlers?",
            "question_type": "problem_solving",
            "options": [
                {"id": "A", "text": "Global sessions cannot execute SELECT queries"},
                {"id": "B", "text": "FastAPI dependency injection guarantees each HTTP request receives its own isolated database session that is safely closed in a `finally` block when the request completes"},
                {"id": "C", "text": "Depends() increases raw CPU clock speed"},
                {"id": "D", "text": "Global sessions are forbidden by the Python language specification"}
            ],
            "correct_option": "B",
            "explanation": "Yielding a session in a dependency creates an isolated request scope. It prevents cross-request session leakage, race conditions across threads, and guarantees connection pooling cleanup on errors.",
            "topic_area": "Dependency Injection & DB Sessions",
            "order_index": 3
        },
        {
            "question_text": "How should a route handler properly reject an unauthenticated request with an informative standard status code?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "return {'error': 'unauthorized'}"},
                {"id": "B", "text": "raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Invalid token\", headers={\"WWW-Authenticate\": \"Bearer\"})"},
                {"id": "C", "text": "sys.exit(1)"},
                {"id": "D", "text": "print('User not logged in')"}
            ],
            "correct_option": "B",
            "explanation": "Raising HTTPException returns an RFC-compliant HTTP 401 response with WWW-Authenticate header, stopping execution cleanly without requiring cumbersome manual JSON response formatting.",
            "topic_area": "Error Handling & Status Codes",
            "order_index": 4
        }
    ],
    "business-management": [
        {
            "question_text": "In strategic management, what four dimensions are analyzed within a classic SWOT analysis framework?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "Sales, Workforce, Operations, Targets"},
                {"id": "B", "text": "Strengths, Weaknesses, Opportunities, and Threats"},
                {"id": "C", "text": "Strategy, Workflow, Output, Timeline"},
                {"id": "D", "text": "Suppliers, Warehousing, Orders, Transportation"}
            ],
            "correct_option": "B",
            "explanation": "SWOT categorizes internal capabilities (Strengths & Weaknesses) alongside external market forces (Opportunities & Threats) to formulate resilient, high-impact business strategies.",
            "topic_area": "Strategic Frameworks",
            "order_index": 1
        },
        {
            "question_text": "What is the primary formula used to evaluate Return on Investment (ROI) for a strategic business project?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "(Net Profit / Cost of Investment) * 100"},
                {"id": "B", "text": "(Total Revenue - Taxes) / Headcount"},
                {"id": "C", "text": "Gross Margin * Operating Expenses"},
                {"id": "D", "text": "Asset Value - Current Liabilities"}
            ],
            "correct_option": "A",
            "explanation": "ROI evaluates project financial efficiency: Net Profit (Gain from Investment - Cost of Investment) divided by Cost of Investment, expressed as a percentage.",
            "topic_area": "Financial Analysis",
            "order_index": 2
        },
        {
            "question_text": "A company experiences recurring cross-departmental deadline bottlenecks between marketing and product engineering. Which managerial intervention is most effective?",
            "question_type": "problem_solving",
            "options": [
                {"id": "A", "text": "Immediately terminate the lowest-performing team members"},
                {"id": "B", "text": "Implement a RACI matrix (Responsible, Accountable, Consulted, Informed) and established weekly sprint synchronization checkpoints"},
                {"id": "C", "text": "Cancel all joint planning meetings"},
                {"id": "D", "text": "Double the marketing budget without product consultation"}
            ],
            "correct_option": "B",
            "explanation": "A RACI matrix clarifies exact decision ownership and execution roles across cross-functional teams, eliminating ambiguity, finger-pointing, and communication silos.",
            "topic_area": "Operations & Governance",
            "order_index": 3
        },
        {
            "question_text": "When managing cash flow during an unforeseen seasonal revenue drop, which action best protects business solvency without sacrificing core long-term capabilities?",
            "question_type": "understanding",
            "options": [
                {"id": "A", "text": "Default on supplier contracts without notice"},
                {"id": "B", "text": "Audit variable vs fixed costs, defer discretionary capital expenditures, and negotiate short-term vendor payment terms"},
                {"id": "C", "text": "Liquidate core production equipment"},
                {"id": "D", "text": "Ignore financial statements until next quarter"}
            ],
            "correct_option": "B",
            "explanation": "Controlling variable spending, managing accounts payable timing, and safeguarding cash preserves solvency during market downturns without impairing organizational capacity.",
            "topic_area": "Cash Flow & Risk Management",
            "order_index": 4
        }
    ],
    "marketing-fundamentals": [
        {
            "question_text": "What is Customer Acquisition Cost (CAC) and how is it accurately calculated?",
            "question_type": "conceptual",
            "options": [
                {"id": "A", "text": "Total annual revenue divided by average product price"},
                {"id": "B", "text": "Total sales and marketing expenses divided by the number of new customers acquired during that period"},
                {"id": "C", "text": "Customer lifetime value minus annual churn rate"},
                {"id": "D", "text": "Average order value multiplied by total website impressions"}
            ],
            "correct_option": "B",
            "explanation": "CAC quantifies the total capital required to win a customer: (Marketing & Advertising Spend + Sales Overhead) / Number of New Customers Acquired.",
            "topic_area": "Marketing Metrics & CAC",
            "order_index": 1
        },
        {
            "question_text": "In a standard marketing funnel (TOFU -> MOFU -> BOFU), what category of content is most effective at the Top of the Funnel (TOFU)?",
            "question_type": "practical",
            "options": [
                {"id": "A", "text": "Urgent checkout discount codes and aggressive sales pitches"},
                {"id": "B", "text": "Educational blog posts, infographics, and awareness videos addressing broader audience pain points"},
                {"id": "C", "text": "Multi-year enterprise contract signing requests"},
                {"id": "D", "text": "Technical API reference manuals"}
            ],
            "correct_option": "B",
            "explanation": "Top of Funnel (TOFU) builds broad awareness and trust. High-value educational resources solve audience pain points before introducing commercial product solutions.",
            "topic_area": "Funnel Strategy",
            "order_index": 2
        },
        {
            "question_text": "An e-commerce business attracts high traffic and strong product views, but experiences a 92% cart abandonment rate. What is the most targeted diagnostic step?",
            "question_type": "problem_solving",
            "options": [
                {"id": "A", "text": "Double spending on Google Ads search campaigns"},
                {"id": "B", "text": "Audit the checkout flow for unexpected shipping costs, forced account creation friction, and test simplified guest checkout"},
                {"id": "C", "text": "Redesign the brand logo"},
                {"id": "D", "text": "Remove product return warranties"}
            ],
            "correct_option": "B",
            "explanation": "High cart abandonment directly signals checkout friction: unexpected delivery fees, cumbersome form requirements, or missing payment options. Optimizing the checkout funnel restores conversion rates.",
            "topic_area": "Conversion Rate Optimization",
            "order_index": 3
        },
        {
            "question_text": "A startup with a minimal marketing budget needs to launch a new product. Which approach delivers the highest early customer discovery and ROI?",
            "question_type": "understanding",
            "options": [
                {"id": "A", "text": "Purchase expensive prime-time television advertising slots"},
                {"id": "B", "text": "Target a specific niche community, leverage organic founder storytelling, and build personal relationships with early adopters"},
                {"id": "C", "text": "Retain multiple enterprise advertising agencies simultaneously"},
                {"id": "D", "text": "Broadcast unsolicited promotional emails to unverified scraped contact lists"}
            ],
            "correct_option": "B",
            "explanation": "Focusing on a hyper-specific niche enables high-converting word-of-mouth distribution and deep customer feedback loops at zero initial advertising cost.",
            "topic_area": "Budget Allocation & Strategy",
            "order_index": 4
        }
    ]
}

INITIAL_INTERVIEW_QUESTIONS_DATA = {
    "html-semantics": [
        {
            "question": "Why is semantic HTML critical for modern production web development, and how does it impact SEO and accessibility?",
            "difficulty": "Basic",
            "category": "Conceptual",
            "expected_answer": "Semantic HTML uses elements that clearly describe their meaning and purpose (such as <header>, <main>, <nav>, <article>, and <footer>) rather than generic <div> containers. It enables search engines to accurately index content hierarchy and allows assistive screen readers to navigate web pages without requiring cumbersome custom code.",
            "simple_syntax": "<header>\n  <nav><!-- navigation links --></nav>\n</header>\n<main>\n  <article><!-- primary content --></article>\n</main>\n<footer><!-- site info --></footer>",
            "small_example": "<header>\n  <h1>Career Explore Studio</h1>\n  <nav><a href=\"#dashboard\">Dashboard</a></nav>\n</header>\n<main>\n  <article><h2>Web Foundations</h2></article>\n</main>",
            "explanation": "When an engineer builds with semantic landmarks, the browser accessibility tree (AOM) automatically inherits standard roles and keyboard interactions. In addition, search engines prioritize content in <article> and <main> over peripheral boilerplate.",
            "practical_scenario": "An audit discovers that blind users cannot navigate your e-commerce checkout because the entire form is composed of nested <div> tags with custom onClick handlers. How would you remediate this?",
            "tips_for_answering": "Structure your answer around three pillars: Accessibility (WCAG compliance), Search Engine Optimization (SEO rankings), and Maintainability. Mention the First Rule of ARIA.",
            "common_mistakes": "Saying semantic HTML is only about 'clean code' or 'readability' without explaining screen reader accessibility trees or search crawlers.",
            "order_index": 1
        },
        {
            "question": "What are ARIA landmarks and live regions, and when should you use them alongside native HTML5 elements?",
            "difficulty": "Intermediate",
            "category": "Practical Scenario",
            "expected_answer": "ARIA attributes supply assistive technology with extra context when standard HTML elements cannot convey dynamic state alone. The First Rule of ARIA is: always prefer native HTML elements first. Only use ARIA (such as aria-live or role='alert') for custom widgets or dynamic live updates that native tags cannot communicate.",
            "simple_syntax": "<!-- Live Region Syntax -->\n<div role=\"status\" aria-live=\"polite\">\n  <!-- Dynamic announcement text -->\n</div>",
            "small_example": "<!-- Live notification banner -->\n<div role=\"status\" aria-live=\"polite\" class=\"toast\">\n  Profile saved successfully.\n</div>",
            "explanation": "Native elements like <button> have built-in keyboard tab focus and click synthesis. Custom widgets need ARIA roles (aria-expanded, aria-controls) and JavaScript event listeners to bridge accessibility gaps.",
            "practical_scenario": "A single-page application fetches real-time notifications via WebSockets without triggering a page reload. How do you alert screen reader users immediately without interrupting their current reading flow?",
            "tips_for_answering": "Explain the difference between aria-live='polite' (waits for a speech pause) and aria-live='assertive' (interrupts immediately). Emphasize using polite for background toasts.",
            "common_mistakes": "Recommending putting role='button' on a <div> when a native <button> is completely available.",
            "order_index": 2
        },
        {
            "question": "How does the browser construct the DOM and Accessibility Tree (AOM), and what causes layout thrashing during dynamic DOM updates?",
            "difficulty": "Advanced",
            "category": "Architecture",
            "expected_answer": "The browser tokenizes raw HTML bytes into character streams, builds the DOM tree, combines it with the CSSOM to form the Render Tree, and generates the Accessibility Tree. Layout thrashing occurs when JavaScript repeatedly alternates between reading layout geometry and modifying DOM styles, forcing synchronous layout recalculations.",
            "simple_syntax": "// Bad: Interleaved read/write\n// const h = el.offsetHeight; el.style.height = h + 10 + 'px';\n\n// Good: Batch reads first, then batch writes\nconst height = el.offsetHeight;\nel.style.height = `${height + 10}px`;",
            "small_example": "// Clean batching example\nconst currentHeight = panel.offsetHeight;\n// Write after read\npanel.style.height = `${currentHeight + 20}px`;",
            "explanation": "Batching DOM mutations (using DocumentFragment, Virtual DOM batching, or requestAnimationFrame) preserves smooth 60fps rendering and avoids flooding the AOM with continuous mutation events.",
            "practical_scenario": "A real-time financial ticker updates 50 rows per second, causing extreme UI stutter and assistive technology freezes. How would you re-architect the rendering pipeline?",
            "tips_for_answering": "Walk the interviewer through the critical rendering path steps in order: Bytes -> Characters -> Tokens -> Nodes -> DOM + CSSOM -> Render Tree -> Layout -> Paint.",
            "common_mistakes": "Failing to explain how rapid DOM mutations negatively impact assistive technology performance alongside visual frame drops.",
            "order_index": 3
        }
    ],
    "css-responsive-design": [
        {
            "question": "Explain the CSS Box Model and why setting `box-sizing: border-box` is an essential production best practice.",
            "difficulty": "Basic",
            "category": "Conceptual",
            "expected_answer": "The CSS box model defines four concentric layers: Content, Padding, Border, and Margin. Under default 'content-box', declared width applies only to content, meaning padding and border inflate the rendered size. 'box-sizing: border-box' forces padding and borders inside the declared width, preventing layout overflow.",
            "simple_syntax": "*,\n*::before,\n*::after {\n  box-sizing: border-box;\n}",
            "small_example": ".column {\n  box-sizing: border-box;\n  width: 50%;\n  padding: 16px;\n  border: 1px solid #e2e8f0;\n}",
            "explanation": "With border-box, two columns styled with width: 50% and 16px padding will remain exactly 50% wide and sit side-by-side cleanly without dropping onto a new line.",
            "practical_scenario": "Two 50% width columns inside a 100% width row drop onto separate lines unexpectedly when 10px padding is added. Why did this happen and how do you fix it?",
            "tips_for_answering": "List the four layers from inside out: Content -> Padding -> Border -> Margin. Clarify that margins are never absorbed inside border-box.",
            "common_mistakes": "Assuming margins are included inside the border-box calculation (margins are always outside).",
            "order_index": 1
        },
        {
            "question": "When should you choose CSS Grid versus Flexbox, and how do they complement each other in production applications?",
            "difficulty": "Intermediate",
            "category": "Practical Scenario",
            "expected_answer": "Flexbox is designed for one-dimensional layouts along a single axis (either row or column), making it ideal for toolbars, navbars, and item alignment within components. CSS Grid is designed for two-dimensional layouts where items must align across both rows and columns simultaneously (like page templates and dashboard grids).",
            "simple_syntax": "/* Flexbox: 1-Dimensional */\n.navbar { display: flex; justify-content: space-between; }\n\n/* Grid: 2-Dimensional */\n.dashboard { display: grid; grid-template-columns: repeat(3, 1fr); }",
            "small_example": ".card-grid {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));\n  gap: 1rem;\n}",
            "explanation": "In production, Grid is commonly used for page-level structural matrices, while Flexbox handles micro-layouts inside individual cards or header sections.",
            "practical_scenario": "You are building a responsive dashboard where widgets must span multiple columns and rows while maintaining strict vertical and horizontal alignment. Which system do you deploy?",
            "tips_for_answering": "Use the terms 'content-first' (Flexbox adapts to item sizes) vs 'layout-first' (Grid sets the blueprint). Mention CSS Subgrid.",
            "common_mistakes": "Claiming that CSS Grid replaces Flexbox entirely or that Flexbox is only for mobile screens.",
            "order_index": 2
        },
        {
            "question": "What are CSS Container Queries and how do they improve modular design compared to viewport Media Queries?",
            "difficulty": "Advanced",
            "category": "Architecture",
            "expected_answer": "Viewport media queries (@media) evaluate the entire browser window dimensions, forcing components to know global screen breakpoints. Container queries (@container) allow a component to query the dimensions of its immediate parent container, enabling the exact same component to render compactly in a sidebar and expanded in a hero section.",
            "simple_syntax": ".card-wrapper {\n  container-type: inline-size;\n}\n\n@container (min-width: 450px) {\n  .card { display: flex; }\n}",
            "small_example": ".profile-container {\n  container-type: inline-size;\n}\n\n@container (min-width: 400px) {\n  .profile-layout {\n    flex-direction: row;\n  }\n}",
            "explanation": "Container queries decouple components from page context, dramatically enhancing design system reusability without requiring repetitive modifier classes or JS ResizeObservers.",
            "practical_scenario": "A design system team creates a reusable <UserCard> component that looks broken when placed inside a narrow sidebar on a high-resolution 4K monitor. How do container queries solve this?",
            "tips_for_answering": "Mention container-type: inline-size and container-name. Explain how container queries eliminate brittle JavaScript ResizeObserver hacks.",
            "common_mistakes": "Suggesting viewport @media queries for component-level styling when parent container width varies independently of the viewport.",
            "order_index": 3
        }
    ],
    "javascript-es6": [
        {
            "question": "What are the core differences between `var`, `let`, and `const`, and what is the Temporal Dead Zone (TDZ)?",
            "difficulty": "Basic",
            "category": "Conceptual",
            "expected_answer": "`var` is function-scoped and hoisted with undefined, allowing accidental re-declarations and global variable leakage. `let` and `const` are block-scoped ({}) and hoisted into the Temporal Dead Zone (TDZ), meaning accessing them before declaration throws a ReferenceError. `const` prevents re-assignment of the variable identifier.",
            "simple_syntax": "const constantValue = \"immutable_identifier\";\nlet mutableValue = 100;\n// Avoid 'var'",
            "small_example": "const maxAttempts = 3;\nlet currentAttempt = 1;\n\ncurrentAttempt += 1; // Valid\n// maxAttempts = 4;  // TypeError: Assignment to constant variable",
            "explanation": "Block scoping prevents variable leakage outside of loops and conditionals, eliminating closure bugs commonly seen with var in asynchronous callbacks.",
            "practical_scenario": "Explain why `for (var i = 0; i < 3; i++) { setTimeout(() => console.log(i), 100); }` prints '3 3 3', and how changing `var` to `let` produces '0 1 2'.",
            "tips_for_answering": "Explain both scope differences and hoisting behavior. Clarify that const does NOT make objects deeply immutable (use Object.freeze() or deep freeze).",
            "common_mistakes": "Claiming that `let` and `const` are not hoisted at all (they are hoisted into the TDZ).",
            "order_index": 1
        },
        {
            "question": "How does the JavaScript Event Loop coordinate the Call Stack, Microtask Queue, and Macrotask Queue?",
            "difficulty": "Intermediate",
            "category": "Architecture",
            "expected_answer": "Synchronous code executes sequentially on the Call Stack. When asynchronous operations finish, callbacks are queued: Microtasks (Promises, queueMicrotask) have top priority and are completely drained after each synchronous tick before the Event Loop executes a single Macrotask (setTimeout, setInterval).",
            "simple_syntax": "// Synchronous -> Microtasks -> Macrotasks\nPromise.resolve().then(microtaskCallback);\nsetTimeout(macrotaskCallback, 0);",
            "small_example": "console.log('1: Sync');\nsetTimeout(() => console.log('2: Macrotask'), 0);\nPromise.resolve().then(() => console.log('3: Microtask'));\nconsole.log('4: Sync');\n// Output: 1 -> 4 -> 3 -> 2",
            "explanation": "If a microtask continuously schedules another microtask recursively, it will starve the macrotask queue and completely block browser rendering.",
            "practical_scenario": "Predict the exact console output of: `console.log('1'); setTimeout(() => console.log('2'), 0); Promise.resolve().then(() => console.log('3')); console.log('4');`",
            "tips_for_answering": "State the output immediately: 1, 4, 3, 2. Walk step-by-step through Call Stack -> Microtask Queue -> Macrotask Queue.",
            "common_mistakes": "Believing that `setTimeout(..., 0)` runs immediately before pending resolved Promise callbacks.",
            "order_index": 2
        },
        {
            "question": "What are JavaScript Closures, how do memory leaks occur through retained closures, and how do you diagnose them?",
            "difficulty": "Advanced",
            "category": "Problem Solving",
            "expected_answer": "A closure is the combination of a function bundled together with references to its surrounding lexical environment. A memory leak occurs when a long-lived object (such as a global event listener or detached DOM node) retains a reference to an inner function that encloses large variables, preventing garbage collection.",
            "simple_syntax": "function outer(outerValue) {\n  return function inner(innerValue) {\n    return outerValue + innerValue;\n  };\n}",
            "small_example": "function makeCounter() {\n  let count = 0;\n  return () => ++count;\n}\n\nconst counter = makeCounter();\nconsole.log(counter()); // 1\nconsole.log(counter()); // 2",
            "explanation": "V8's Mark-and-Sweep garbage collector cannot reclaim memory that is reachable through active root references. Cleaning up event listeners on unmount breaks the retention chain.",
            "practical_scenario": "A Single Page App memory footprint climbs by 50MB every time a user opens and closes a modal. How do you trace and eliminate the leak using Chrome DevTools?",
            "tips_for_answering": "Reference Chrome DevTools Memory tab: Take heap snapshots, compare deltas, look for 'Detached HTMLDivElement' and closures retained by event listeners.",
            "common_mistakes": "Claiming that closures are an anti-pattern or that all closures cause memory leaks. Leaks only occur when references are unintentionally retained.",
            "order_index": 3
        }
    ],
    "react-architecture": [
        {
            "question": "What are the core Rules of Hooks in React, and why does React mandate them?",
            "difficulty": "Basic",
            "category": "Conceptual",
            "expected_answer": "Hooks must only be called at the top level of React function components or custom Hooks (never inside loops, conditions, or nested functions), and only from React functions. React mandates this because it tracks Hook state internally using ordered linked arrays based strictly on invocation sequence across renders.",
            "simple_syntax": "function MyComponent() {\n  // 1. Call hooks at the top level only\n  const [state, setState] = useState(initial);\n  useEffect(() => { /* effect */ }, []);\n  return <div>{state}</div>;\n}",
            "small_example": "function UserStatus({ user }) {\n  const [online, setOnline] = useState(false);\n\n  // Place condition INSIDE the hook, not wrapping it\n  useEffect(() => {\n    if (user?.id) {\n      setOnline(true);\n    }\n  }, [user]);\n\n  return <span>{online ? 'Online' : 'Offline'}</span>;\n}",
            "explanation": "If a hook call is skipped inside an `if` block, all subsequent hook calls shift index positions, causing state variables and effect cleanups to associate with the wrong variables.",
            "practical_scenario": "A developer attempts: `if (user.isAdmin) { useEffect(...) }`. What bug will happen in production and how should it be rewritten?",
            "tips_for_answering": "Emphasize that the condition belongs INSIDE the hook, not wrapping the hook call: `useEffect(() => { if (!user.isAdmin) return; ... }, [user.isAdmin])`.",
            "common_mistakes": "Believing hooks are stored by variable name rather than execution order index.",
            "order_index": 1
        },
        {
            "question": "Explain React's Reconciliation process, Virtual DOM diffing algorithm, and the role of the `key` prop in dynamic lists.",
            "difficulty": "Intermediate",
            "category": "Architecture",
            "expected_answer": "Reconciliation compares the new Virtual DOM tree against the previous one using an O(n) heuristic algorithm. React assumes elements of different types generate different trees. The `key` prop provides stable identity across renders, allowing React to match items when elements are inserted, deleted, or reordered.",
            "simple_syntax": "{items.map((item) => (\n  <ListItem key={item.id} data={item} />\n))}",
            "small_example": "const todos = [\n  { id: 'item-1', text: 'Master React' },\n  { id: 'item-2', text: 'Build Studio' },\n];\n\nfunction TodoList() {\n  return (\n    <ul>\n      {todos.map(todo => <li key={todo.id}>{todo.text}</li>)}\n    </ul>\n  );\n}",
            "explanation": "Using array indices as keys breaks when items are sorted or filtered, causing child input components to retain obsolete internal state and trigger unnecessary DOM thrashing.",
            "practical_scenario": "A list of todo items has editable text fields. When a user deletes the first item, the third item's input text mysteriously replaces the second item. What caused this?",
            "tips_for_answering": "Mention that keys must be stable, unique, and predictable. Emphasize never using Math.random() as a key as it destroys and re-mounts nodes on every render.",
            "common_mistakes": "Using array index as a key for dynamic lists, or explaining Virtual DOM without mentioning reconciliation heuristics.",
            "order_index": 2
        },
        {
            "question": "How do you identify and resolve unnecessary component re-renders in a complex React application without over-optimizing?",
            "difficulty": "Advanced",
            "category": "Performance",
            "expected_answer": "First, measure before optimizing using React DevTools Profiler ('Highlight updates when components render'). Apply State Colocation (keep state close to where it is used) and component composition (passing heavy children as props). If parent re-renders still cause expensive leaf re-renders, wrap children in React.memo and memoize unstable object props with useMemo and callback references with useCallback.",
            "simple_syntax": "const MemoizedChild = React.memo(ChildComponent);\nconst memoizedFn = useCallback(() => { /* handler */ }, [dependency]);",
            "small_example": "import React, { useState, useCallback } from 'react';\n\nconst ActionBtn = React.memo(({ onClick, label }) => (\n  <button onClick={onClick}>{label}</button>\n));\n\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  const handleIncrement = useCallback(() => setCount(c => c + 1), []);\n  return <ActionBtn onClick={handleIncrement} label=\"Count + 1\" />;\n}",
            "explanation": "useCallback and useMemo carry memory and execution overhead. Using them everywhere indiscriminately adds cognitive load without measurable gain if components are already cheap to render.",
            "practical_scenario": "A parent component hosts a timer that ticks every second, causing an expensive 5,000-row data grid to re-render every second. What is your optimization order?",
            "tips_for_answering": "Order of optimization: 1. Push state down / lift content up (composition), 2. Profiler measurement, 3. React.memo + useCallback/useMemo.",
            "common_mistakes": "Suggesting useCallback without wrapping the child in React.memo (the child will still re-render when the parent renders).",
            "order_index": 3
        }
    ],
    "python-fastapi": [
        {
            "question": "What makes FastAPI exceptionally performant compared to traditional Python frameworks like Flask and Django?",
            "difficulty": "Basic",
            "category": "Conceptual",
            "expected_answer": "FastAPI is built on Starlette and Uvicorn utilizing the ASGI (Asynchronous Server Gateway Interface) standard. It runs on Python's native asyncio event loop, enabling non-blocking asynchronous I/O. Furthermore, it leverages Pydantic for high-performance data parsing and automatic OpenAPI generation.",
            "simple_syntax": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/endpoint\")\nasync def handler():\n    return {\"status\": \"success\"}",
            "small_example": "from fastapi import FastAPI\nimport asyncio\n\napp = FastAPI()\n\n@app.get(\"/ping\")\nasync def ping():\n    # Non-blocking async operation\n    await asyncio.sleep(0.01)\n    return {\"message\": \"pong\"}",
            "explanation": "In Flask/WSGI, a slow database query or third-party HTTP call blocks the entire OS worker thread. In FastAPI, `await db.fetch()` yields control to the event loop to service thousands of other concurrent requests.",
            "practical_scenario": "An API needs to call 5 external credit check services simultaneously. How does FastAPI execute this efficiently without spawning 5 heavy OS threads?",
            "tips_for_answering": "Mention asyncio.gather() for parallel async I/O. Clarify that synchronous CPU-bound operations should be offloaded to thread pools via `def` endpoints or run_in_threadpool.",
            "common_mistakes": "Assuming all endpoints must be `async def`. Calling blocking sync libraries (like requests or sync DB drivers) inside `async def` blocks the event loop.",
            "order_index": 1
        },
        {
            "question": "How does FastAPI's Dependency Injection (`Depends`) system work, and how does it manage database session lifecycles?",
            "difficulty": "Intermediate",
            "category": "Architecture",
            "expected_answer": "`Depends` evaluates hierarchical dependency trees per request. For database connections, a generator function (`get_db`) yields a SQLAlchemy session and uses a `finally` block to guarantee `db.close()` runs when the response completes, even if an uncaught exception occurred.",
            "simple_syntax": "def get_db():\n    db = SessionLocal()\n    try:\n        yield db\n    finally:\n        db.close()\n\n# In route:\n@app.get(\"/items\")\ndef read_items(db: Session = Depends(get_db)): ...",
            "small_example": "from fastapi import FastAPI, Depends\nfrom sqlalchemy.orm import Session\n\n@app.get(\"/profile\")\ndef get_profile(db: Session = Depends(get_db)):\n    user = db.query(User).first()\n    return {\"username\": user.username}",
            "explanation": "This isolates database sessions per HTTP request, prevents connection pooling leaks, and simplifies testing by allowing mock overrides (`app.dependency_overrides`).",
            "practical_scenario": "A junior developer uses a single global `db = SessionLocal()` at module level. What disasters occur under high concurrency?",
            "tips_for_answering": "Highlight thread safety, race conditions, dirty reads, and transaction isolation when explaining why global sessions fail in multi-threaded web servers.",
            "common_mistakes": "Failing to mention the `finally` block for resource cleanup, or not knowing about app.dependency_overrides for automated testing.",
            "order_index": 2
        },
        {
            "question": "How do you implement secure JWT authentication, password hashing, and token revocation in a production FastAPI architecture?",
            "difficulty": "Advanced",
            "category": "Security",
            "expected_answer": "Passwords must be hashed using robust adaptive algorithms (bcrypt, Argon2) with cryptographic salts before storage. Upon login, the server issues an expiring JSON Web Token (JWT) signed with a secret key using HS256/RS256. Routes are protected via OAuth2PasswordBearer and Depends(get_current_user). Revocation is handled via short token lifespans coupled with refresh token rotation stored in a Redis blocklist.",
            "simple_syntax": "oauth2_scheme = OAuth2PasswordBearer(tokenUrl=\"/api/auth/login\")\n\nasync def get_current_user(token: str = Depends(oauth2_scheme)): ...",
            "small_example": "from fastapi import APIRouter, Depends, HTTPException, status\nfrom fastapi.security import OAuth2PasswordBearer\n\noauth2_scheme = OAuth2PasswordBearer(tokenUrl=\"/token\")\n\n@router.get(\"/secure-data\")\nasync def get_data(token: str = Depends(oauth2_scheme)):\n    if not token:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)\n    return {\"authorized\": True}",
            "explanation": "Stateless JWTs cannot be revoked natively before expiry without maintaining a distributed token blacklist (e.g. Redis) or tracking user credential version numbers (token_version).",
            "practical_scenario": "A user reports their laptop stolen. How does your authentication architecture immediately revoke their active JWT tokens?",
            "tips_for_answering": "Mention the trade-offs of stateless vs stateful revocation. Emphasize storing refresh tokens in HttpOnly, Secure, SameSite cookies.",
            "common_mistakes": "Storing plain text passwords, or using eval() or unverified JWT payload decoding.",
            "order_index": 3
        }
    ],
    "business-management": [
        {
            "question": "How do you conduct an effective SWOT analysis, and how do you translate the matrix into an actionable business strategy?",
            "difficulty": "Basic",
            "category": "Conceptual",
            "expected_answer": "SWOT categorizes internal factors (Strengths & Weaknesses) and external market environmental factors (Opportunities & Threats). To make it actionable, use the TOWS Matrix: match Strengths to Opportunities (Growth), use Strengths to counter Threats (Defense), and address Weaknesses to capture Opportunities (Turnaround).",
            "simple_syntax": "SWOT Framework:\n- Strengths (Internal): Unique assets & core advantages\n- Weaknesses (Internal): Capability gaps & resource limitations\n- Opportunities (External): Market trends & emerging niches\n- Threats (External): Competitor moves & regulatory risks",
            "small_example": "Retail Business Case:\n- Strength: 95% local customer loyalty.\n- Opportunity: High demand for home grocery delivery.\n- Strategic Action: Launch pilot same-day delivery service for existing loyalty members.",
            "explanation": "Without cross-matching internal capabilities to external realities, a SWOT remains a passive brainstorm rather than an execution blueprint.",
            "practical_scenario": "A legacy retail brand has strong customer trust (Strength) but outdated digital technology (Weakness), while e-commerce adoption is surging (Opportunity). What is the strategic priority?",
            "tips_for_answering": "Emphasize that Strengths/Weaknesses are internal and controllable, while Opportunities/Threats are external market forces. Propose concrete milestones.",
            "common_mistakes": "Treating SWOT as a static list of bullet points without prioritizing or pairing factors into execution actions.",
            "order_index": 1
        },
        {
            "question": "What is a RACI Matrix, and how does it prevent accountability failures across cross-functional product and operations teams?",
            "difficulty": "Intermediate",
            "category": "Operations",
            "expected_answer": "RACI defines four roles for project tasks: Responsible (does the work), Accountable (owns the outcome; strictly ONE person), Consulted (provides two-way expert input), and Informed (kept updated one-way). It eliminates bystander apathy and communication bottlenecks.",
            "simple_syntax": "RACI Matrix Roles:\n- R (Responsible): Completes the deliverable\n- A (Accountable): Single owner who makes final decision\n- C (Consulted): Subject-matter advisor (two-way)\n- I (Informed): Kept updated on progress (one-way)",
            "small_example": "Feature Launch Roles:\n- Design & Implementation: Engineering Team (Responsible)\n- Release Approval: Product Manager (Single Accountable)\n- Security Review: InfoSec Lead (Consulted)\n- Sales Team: Support & Marketing (Informed)",
            "explanation": "Having more than one 'Accountable' owner means no one is truly accountable. RACI clarifies decision rights and prevents duplicate efforts.",
            "practical_scenario": "A software launch misses its release date because engineering believed marketing signed off on QA, while marketing assumed engineering had final authority. How does RACI fix this?",
            "tips_for_answering": "Remember the golden rule: Exactly ONE 'A' (Accountable) per decision or deliverable. Walk through how to facilitate alignment workshops.",
            "common_mistakes": "Assigning multiple people as 'Accountable' for the same deliverable, creating confusion.",
            "order_index": 2
        },
        {
            "question": "How do you evaluate and optimize working capital and cash conversion cycles during macroeconomic downturns?",
            "difficulty": "Advanced",
            "category": "Financial Strategy",
            "expected_answer": "The Cash Conversion Cycle (CCC = DIO + DSO - DPO) measures the days required to convert inventory and resources into cash flows. During downturns, optimize by reducing Days Sales Outstanding (faster receivables, early-payment discounts), managing Days Inventory Outstanding (lean inventory, just-in-time), and extending Days Payable Outstanding with suppliers without damaging vendor goodwill.",
            "simple_syntax": "Working Capital = Current Assets - Current Liabilities\nCash Conversion Cycle (CCC) = Days Inventory + Days Receivables - Days Payables",
            "small_example": "Working Capital Optimization:\n- Standard terms: 60-day customer payment window.\n- Action: Offer 2% discount for payment within 10 days.\n- Result: Average receivables collection accelerates from 60 days to 14 days, infusing immediate liquid cash.",
            "explanation": "Profitable companies frequently go bankrupt during downturns due to liquidity crises rather than lack of demand. Cash flow preservation ensures survival.",
            "practical_scenario": "A B2B enterprise is generating 20% net margin on paper but cannot meet payroll this Friday due to 90-day invoice delays. What immediate and structural interventions do you deploy?",
            "tips_for_answering": "Distinguish clearly between Net Profit on an accrual basis and Operating Cash Flow. Mention invoice factoring and variable cost restructuring.",
            "common_mistakes": "Confusing paper profitability with real cash liquidity.",
            "order_index": 3
        }
    ],
    "marketing-fundamentals": [
        {
            "question": "Explain the classic Marketing Funnel (TOFU, MOFU, BOFU) and what types of content and metrics apply at each stage.",
            "difficulty": "Basic",
            "category": "Conceptual",
            "expected_answer": "Top of Funnel (TOFU: Awareness) attracts wide audiences using educational blogs, viral video, and PR (measured by impressions, reach, traffic). Middle of Funnel (MOFU: Consideration) nurtures prospects with webinars, case studies, and email drip sequences (measured by MQLs, engagement). Bottom of Funnel (BOFU: Conversion) drives purchase decisions with demos, trials, and customer testimonials (measured by CAC, conversion rate, revenue).",
            "simple_syntax": "Funnel Flow:\n1. TOFU (Top of Funnel): Brand Awareness & Discovery\n2. MOFU (Middle of Funnel): Trust Building & Problem Evaluation\n3. BOFU (Bottom of Funnel): Purchase Decision & Conversion",
            "small_example": "Solar Energy Provider Funnel:\n- TOFU: Blog post '5 Ways Homeowners Cut Electric Bills by 40%'.\n- MOFU: Interactive 'Roof Solar Potential Calculator'.\n- BOFU: Free in-home engineering quote with 10% seasonal discount.",
            "explanation": "Prospects rarely purchase on first touch. Respecting funnel stages prevents aggressive premature sales pitches from alienating high-intent prospects.",
            "practical_scenario": "A startup sends direct 'Buy Now' discount ads to cold traffic with zero prior brand awareness, resulting in 0.05% conversion. How do you restructure the funnel?",
            "tips_for_answering": "Describe the transition triggers between stages (e.g. Lead Magnet download -> MQL -> Product Demo -> SQL).",
            "common_mistakes": "Treating all audience segments identically or applying bottom-of-funnel conversion metrics to brand awareness campaigns.",
            "order_index": 1
        },
        {
            "question": "What is the relationship between Customer Acquisition Cost (CAC) and Customer Lifetime Value (LTV), and what is an ideal LTV:CAC ratio?",
            "difficulty": "Intermediate",
            "category": "Metrics & Growth",
            "expected_answer": "CAC measures the total sales and marketing cost to acquire a single customer. LTV measures the projected gross profit generated from that customer over their entire relationship. An ideal LTV:CAC ratio for sustainable growth is 3:1. Below 1:1 loses money on every customer; above 5:1 typically indicates under-investing in marketing growth opportunities.",
            "simple_syntax": "CAC = Total Sales & Marketing Spend / New Customers Acquired\nLTV = Average Revenue Per User * Gross Margin * Average Lifespan\nHealthy Benchmark: LTV : CAC >= 3 : 1",
            "small_example": "SaaS Subscription Example:\n- Ad spend: $1,000 acquiring 10 customers -> CAC = $100.\n- Average subscription: $30/month across 12 months with 85% gross margin -> LTV = $306.\n- Ratio: $306 / $100 = 3.06x (Sustainable & scalable).",
            "explanation": "In addition to ratio, CAC Payback Period (ideally under 12 months) dictates cash flow sustainability and capital runway.",
            "practical_scenario": "A SaaS company has an LTV of $1,500 and a CAC of $1,200. The CEO wants to double marketing spend. What is your strategic recommendation?",
            "tips_for_answering": "Do not just state the formula; explain unit economics, churn rate impact on LTV, and CAC payback timeline.",
            "common_mistakes": "Ignoring customer churn rate when calculating LTV, or calculating CAC without factoring in sales team salaries and software overhead.",
            "order_index": 2
        },
        {
            "question": "How do you design and execute a rigorous Conversion Rate Optimization (CRO) experiment on a high-dropoff checkout page?",
            "difficulty": "Advanced",
            "category": "Problem Solving",
            "expected_answer": "Start with quantitative data (funnel drop-off analytics in GA4/Mixpanel) and qualitative data (session recordings in Hotjar, user surveys). Formulate a falsifiable hypothesis (e.g., 'Removing mandatory account registration will decrease cart abandonment by 15%'). Run a statistically significant A/B test with isolated variables, ensuring sufficient sample size and statistical power before declaring a winner.",
            "simple_syntax": "CRO Experiment Lifecycle:\n1. Analytics Audit (Identify Drop-off)\n2. Falsifiable Hypothesis Formulation\n3. Controlled A/B Split Test\n4. Statistical Significance Validation (p < 0.05)\n5. Full Production Rollout",
            "small_example": "Checkout Experiment:\n- Problem: 65% drop-off at billing address screen.\n- Hypothesis: Offering One-Click Apple/Google Pay will reduce friction.\n- Test: 50% traffic receives One-Click Pay.\n- Result: Checkout completion lifts by 22% with 99% statistical confidence.",
            "explanation": "Prematurely stopping A/B tests or testing multiple simultaneous design changes produces false positives (p-hacking) and unreliable business conclusions.",
            "practical_scenario": "A high-ticket eCommerce cart has an 88% abandonment rate at step 2 of checkout. Walk me through your diagnostic and experimentation roadmap.",
            "tips_for_answering": "Mention calculating sample size beforehand, minimum detectable effect (MDE), and guarding against seasonal biases.",
            "common_mistakes": "Changing multiple variables at once in an A/B test, or declaring a winner after 24 hours without statistical confidence.",
            "order_index": 3
        }
    ]
}

INITIAL_OVERALL_EVALUATION_DATA = {
    "full-stack-developer": [
        {
            "question_text": "Trace the end-to-end data lifecycle: A user submits a new profile bio in a React textarea. What sequence of operations occurs across the full stack?",
            "question_type": "data_flow_integration",
            "integrated_skills": "React, FastAPI, Database, Authentication",
            "options": [
                {"id": "A", "text": "React writes directly to SQLite file on the user's hard drive."},
                {"id": "B", "text": "React handles form state -> dispatches JSON fetch with JWT Bearer header -> FastAPI route parses & validates via Pydantic -> SQLAlchemy session commits changes -> response serializes to JSON -> React updates UI state."},
                {"id": "C", "text": "FastAPI automatically generates HTML and replaces the entire browser DOM."},
                {"id": "D", "text": "The database triggers a WebSocket callback before FastAPI processes the request."}
            ],
            "correct_option": "B",
            "explanation": "Modern full-stack data flow cleanly separates client-side reactive state management, network transport serialization, backend validation & authorization, and ORM transactional persistence.",
            "scenario_context": "User profile editing form with live feedback.",
            "order_index": 1
        },
        {
            "question_text": "A React frontend receives `TypeError: Failed to fetch (NetworkError)` while the FastAPI backend logs report zero incoming HTTP requests. What is the most probable architectural culprit?",
            "question_type": "end_to_end_debugging",
            "integrated_skills": "React, FastAPI, REST API",
            "options": [
                {"id": "A", "text": "SQLAlchemy foreign key constraint violation in the database."},
                {"id": "B", "text": "Browser Preflight OPTIONS request failed due to missing CORS (Cross-Origin Resource Sharing) headers or port mismatch."},
                {"id": "C", "text": "React state hook memory leak."},
                {"id": "D", "text": "CSS z-index conflict blocking user clicks."}
            ],
            "correct_option": "B",
            "explanation": "When client and server run on different origins/ports, the browser fires an automated OPTIONS preflight request. If CORS middleware is misconfigured or blocked by a firewall, the browser aborts the request before the server's endpoint handler is ever reached.",
            "scenario_context": "Connecting a Vite frontend on port 5173 to a FastAPI backend on port 8000.",
            "order_index": 2
        },
        {
            "question_text": "A database migration alters a `users` table column from `name` to `full_name`. To maintain system integrity and avoid downtime, what coordinated changes must be executed?",
            "question_type": "cross_skill_architecture",
            "integrated_skills": "Database, FastAPI, React",
            "options": [
                {"id": "A", "text": "Only update the HTML <label> tag in React."},
                {"id": "B", "text": "Update the SQLAlchemy model, run the DB migration, update the Pydantic request/response schemas, and synchronize the frontend React API client and interfaces."},
                {"id": "C", "text": "Restart the Uvicorn server without altering code."},
                {"id": "D", "text": "Drop all database tables completely in production."}
            ],
            "correct_option": "B",
            "explanation": "Relational schema modifications cascade through the ORM definition, API validation contracts, serialization layers, and frontend consuming client states.",
            "scenario_context": "Production schema refactoring and contract synchronization.",
            "order_index": 3
        },
        {
            "question_text": "A user logs in, but every subsequent protected API request returns HTTP 401 Unauthorized. How would you systematically diagnose this issue across the full stack?",
            "question_type": "end_to_end_debugging",
            "integrated_skills": "Authentication, React, FastAPI",
            "options": [
                {"id": "A", "text": "Check browser localStorage/cookies for token existence -> inspect Network tab for Authorization: Bearer <token> header -> verify backend JWT secret key, algorithm, and token expiration logic."},
                {"id": "B", "text": "Reinstall the Python virtual environment on the server."},
                {"id": "C", "text": "Change the database from SQLite to CSV files."},
                {"id": "D", "text": "Disable all authentication logic permanently."}
            ],
            "correct_option": "A",
            "explanation": "Full-stack authentication debugging isolates client token storage, transport layer header injection, and server-side signature verification.",
            "scenario_context": "Session persistence and route protection debugging.",
            "order_index": 4
        }
    ],
    "business-administration": [
        {
            "question_text": "A software business achieves rapid top-of-funnel user acquisition, but operational customer support tickets spike by 400% and cash reserves drop significantly. How should the executive leadership team respond?",
            "question_type": "strategic_decision_making",
            "integrated_skills": "Marketing, Operations Management, Financial Management",
            "options": [
                {"id": "A", "text": "Triple the marketing ad budget to compensate for churn."},
                {"id": "B", "text": "Convene cross-functional alignment: adjust marketing spend, audit customer onboarding bottlenecks in operations, and analyze working capital runway in finance."},
                {"id": "C", "text": "Immediately shut down customer support channels."},
                {"id": "D", "text": "Double product prices without informing existing customers."}
            ],
            "correct_option": "B",
            "explanation": "Business management requires balancing demand generation with delivery capacity and financial solvency. Scaling sales without operational capacity destroys unit economics.",
            "scenario_context": "Rapid scaling causing operational strain and cash flow contraction.",
            "order_index": 1
        },
        {
            "question_text": "A business has a high Customer Acquisition Cost (CAC) and a long Cash Conversion Cycle (CCC). Which integrated strategy best improves solvency without sacrificing brand equity?",
            "question_type": "cross_skill_integration",
            "integrated_skills": "Marketing, Financial Management, Strategic Management",
            "options": [
                {"id": "A", "text": "Optimize marketing channels toward high-retention organic referrals while negotiating shorter payment terms with B2B accounts receivable."},
                {"id": "B", "text": "Stop paying all vendors indefinitely."},
                {"id": "C", "text": "Fire the entire executive team."},
                {"id": "D", "text": "Rely solely on high-interest short-term debt."}
            ],
            "correct_option": "A",
            "explanation": "Pairing CAC reduction (organic retention loops) with accelerated accounts receivable shortens the CCC, preserving liquidity without damaging brand reputation.",
            "scenario_context": "Managing cash flow cycles during marketing expansion.",
            "order_index": 2
        },
        {
            "question_text": "When executing a strategic pivot in response to a new aggressive competitor, how should leadership coordinate organizational governance?",
            "question_type": "strategic_decision_making",
            "integrated_skills": "Leadership, Operations Management, Strategic Management",
            "options": [
                {"id": "A", "text": "Issue a new RACI matrix, communicate strategic realignment via structured all-hands meetings, and set measurable OKRs across marketing, operations, and finance."},
                {"id": "B", "text": "Keep the pivot secret from all department heads."},
                {"id": "C", "text": "Eliminate all performance metrics."},
                {"id": "D", "text": "Wait for the competitor to fail."}
            ],
            "correct_option": "A",
            "explanation": "Effective leadership operationalizes strategic change by establishing clear ownership (RACI), transparent vision, and quantitative cross-functional objectives (OKRs).",
            "scenario_context": "Organizational realignment during competitive threats.",
            "order_index": 3
        }
    ]
}


def seed_initial_data(db: Session):
    """
    Seed or upgrade initial career goals, skills, topic hierarchies, practical content,
    self-evaluation questions, interview preparation questions, and overall cross-skill evaluation questions.
    """
    for goal_data in INITIAL_GOALS_DATA:
        goal_attrs = {k: v for k, v in goal_data.items() if k != "skills"}
        skills_data = goal_data.get("skills", [])
        
        # Check if goal exists by slug
        existing_goal = db.query(Goal).filter(Goal.slug == goal_attrs["slug"]).first()
        if not existing_goal:
            goal = Goal(**goal_attrs)
            db.add(goal)
            db.flush()
        else:
            goal = existing_goal
            # Update attributes
            for k, v in goal_attrs.items():
                setattr(goal, k, v)
            db.flush()

        # Seed overall cross-skill evaluation questions (Section 20)
        overall_questions = INITIAL_OVERALL_EVALUATION_DATA.get(goal.slug, [])
        for oq_data in overall_questions:
            existing_oq = db.query(OverallGoalEvaluationQuestion).filter(
                OverallGoalEvaluationQuestion.goal_id == goal.id,
                OverallGoalEvaluationQuestion.question_text == oq_data["question_text"]
            ).first()
            options_str = json.dumps(oq_data["options"])
            if not existing_oq:
                oq = OverallGoalEvaluationQuestion(
                    goal_id=goal.id,
                    question_text=oq_data["question_text"],
                    question_type=oq_data.get("question_type", "cross_skill_integration"),
                    integrated_skills=oq_data["integrated_skills"],
                    options_json=options_str,
                    correct_option=oq_data["correct_option"],
                    explanation=oq_data["explanation"],
                    scenario_context=oq_data.get("scenario_context"),
                    order_index=oq_data.get("order_index", 0)
                )
                db.add(oq)
            else:
                existing_oq.question_type = oq_data.get("question_type", "cross_skill_integration")
                existing_oq.integrated_skills = oq_data["integrated_skills"]
                existing_oq.options_json = options_str
                existing_oq.correct_option = oq_data["correct_option"]
                existing_oq.explanation = oq_data["explanation"]
                existing_oq.scenario_context = oq_data.get("scenario_context")
                existing_oq.order_index = oq_data.get("order_index", 0)

        # Seed Capstone Final Interview Questions (Sections 21-23, Exactly 15 questions per goal)
        final_interview_questions = INITIAL_FINAL_INTERVIEW_QUESTIONS_DATA.get(goal.slug, [])
        for fiq_data in final_interview_questions:
            existing_fiq = db.query(GoalFinalInterviewQuestion).filter(
                GoalFinalInterviewQuestion.goal_id == goal.id,
                GoalFinalInterviewQuestion.question_number == fiq_data["question_number"]
            ).first()
            if not existing_fiq:
                fiq = GoalFinalInterviewQuestion(
                    goal_id=goal.id,
                    **fiq_data
                )
                db.add(fiq)
            else:
                for k, v in fiq_data.items():
                    setattr(existing_fiq, k, v)

        # Seed skills
        for s_data in skills_data:
            skill_attrs = {k: v for k, v in s_data.items() if k not in ("topics", "practical")}
            topics_data = s_data.get("topics", [])
            practical_data = s_data.get("practical", [])

            existing_skill = db.query(Skill).filter(Skill.goal_id == goal.id, Skill.slug == skill_attrs["slug"]).first()
            if not existing_skill:
                skill = Skill(goal_id=goal.id, **skill_attrs)
                db.add(skill)
                db.flush()
            else:
                skill = existing_skill
                for k, v in skill_attrs.items():
                    setattr(skill, k, v)
                db.flush()

            # Seed topics
            for t_data in topics_data:
                existing_topic = db.query(Topic).filter(Topic.skill_id == skill.id, Topic.title == t_data["title"]).first()
                if not existing_topic:
                    topic = Topic(skill_id=skill.id, **t_data)
                    db.add(topic)
                else:
                    for k, v in t_data.items():
                        setattr(existing_topic, k, v)

            # Seed practical content
            for p_data in practical_data:
                existing_practical = db.query(PracticalContent).filter(
                    PracticalContent.skill_id == skill.id,
                    PracticalContent.title == p_data["title"]
                ).first()
                if not existing_practical:
                    practical = PracticalContent(skill_id=skill.id, **p_data)
                    db.add(practical)
                else:
                    for k, v in p_data.items():
                        setattr(existing_practical, k, v)

            # Seed evaluation questions
            eval_questions = INITIAL_EVALUATIONS_DATA.get(skill.slug, [])
            for eq_data in eval_questions:
                existing_q = db.query(EvaluationQuestion).filter(
                    EvaluationQuestion.skill_id == skill.id,
                    EvaluationQuestion.question_text == eq_data["question_text"]
                ).first()
                
                options_str = json.dumps(eq_data["options"])
                if not existing_q:
                    question = EvaluationQuestion(
                        skill_id=skill.id,
                        question_text=eq_data["question_text"],
                        question_type=eq_data.get("question_type", "conceptual"),
                        options_json=options_str,
                        correct_option=eq_data["correct_option"],
                        explanation=eq_data["explanation"],
                        topic_area=eq_data.get("topic_area"),
                        order_index=eq_data.get("order_index", 0)
                    )
                    db.add(question)
                else:
                    existing_q.question_type = eq_data.get("question_type", "conceptual")
                    existing_q.options_json = options_str
                    existing_q.correct_option = eq_data["correct_option"]
                    existing_q.explanation = eq_data["explanation"]
                    existing_q.topic_area = eq_data.get("topic_area")
                    existing_q.order_index = eq_data.get("order_index", 0)

            # Seed interview questions
            interview_questions = INITIAL_INTERVIEW_QUESTIONS_DATA.get(skill.slug, [])
            for iq_data in interview_questions:
                existing_iq = db.query(SkillInterviewQuestion).filter(
                    SkillInterviewQuestion.skill_id == skill.id,
                    SkillInterviewQuestion.question == iq_data["question"]
                ).first()
                if not existing_iq:
                    iq = SkillInterviewQuestion(
                        skill_id=skill.id,
                        question=iq_data["question"],
                        difficulty=iq_data.get("difficulty", "Basic"),
                        category=iq_data.get("category", "Conceptual"),
                        expected_answer=iq_data["expected_answer"],
                        simple_syntax=iq_data.get("simple_syntax"),
                        small_example=iq_data.get("small_example"),
                        explanation=iq_data["explanation"],
                        practical_scenario=iq_data.get("practical_scenario"),
                        tips_for_answering=iq_data["tips_for_answering"],
                        common_mistakes=iq_data["common_mistakes"],
                        order_index=iq_data.get("order_index", 0)
                    )
                    db.add(iq)
                else:
                    existing_iq.difficulty = iq_data.get("difficulty", "Basic")
                    existing_iq.category = iq_data.get("category", "Conceptual")
                    existing_iq.expected_answer = iq_data["expected_answer"]
                    existing_iq.simple_syntax = iq_data.get("simple_syntax")
                    existing_iq.small_example = iq_data.get("small_example")
                    existing_iq.explanation = iq_data["explanation"]
                    existing_iq.practical_scenario = iq_data.get("practical_scenario")
                    existing_iq.tips_for_answering = iq_data["tips_for_answering"]
                    existing_iq.common_mistakes = iq_data["common_mistakes"]
                    existing_iq.order_index = iq_data.get("order_index", 0)

    # Seed default demo user if not present (for one-click demo login in UI)
    demo_user = db.query(User).filter(User.email == "alex@careerexplore.com").first()
    if not demo_user:
        demo_user = User(
            name="Alex Careerist",
            email="alex@careerexplore.com",
            hashed_password=get_password_hash("Explore2026!"),
            is_active=True
        )
        db.add(demo_user)

    db.commit()
    print("[Seed] Initial goals, skills, topics, practical content, evaluations, overall cross-skill, and capstone interview questions populated successfully.")



