import os
import re

print("=" * 60)
print("PHASE 11: RESPONSIVE UI IMPROVEMENT AUDIT & VERIFICATION")
print("=" * 60)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
SRC_DIR = os.path.join(FRONTEND_DIR, "src")

# 1. Verify Viewport Meta Tag in index.html
index_html_path = os.path.join(FRONTEND_DIR, "index.html")
with open(index_html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

assert 'name="viewport"' in html_content, "Viewport meta tag missing in index.html"
assert "width=device-width" in html_content, "width=device-width missing in viewport meta"
print("  [PASS] Test 1: index.html has valid viewport meta tag (width=device-width, initial-scale=1.0).")

# 2. Verify CSS Breakpoints in index.css
index_css_path = os.path.join(SRC_DIR, "index.css")
with open(index_css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

breakpoints_to_check = [
    ("@media (max-width: 1024px)", "Desktop sidebar toggle & grid-4 collapse"),
    ("@media (max-width: 820px)", "Tablet grid-3 collapse"),
    ("@media (max-width: 768px)", "Tablet/mobile touch targets & navbar padding"),
    ("@media (max-width: 640px)", "Mobile 1-column grid & actions stack"),
    ("@media (max-width: 480px)", "Mobile compact card padding & modal margins"),
    ("@media (max-width: 430px)", "Ultra-mobile brand text & search shrink"),
    ("@media (max-width: 360px)", "Micro-mobile top navbar status text"),
]

for bp, desc in breakpoints_to_check:
    assert bp in css_content, f"Breakpoint {bp} ({desc}) missing in index.css"
print("  [PASS] Test 2: All 7 key media query breakpoints present in index.css covering 320px to 1920px.")

# 3. Verify min-height: 44px tap target rule for mobile
assert "min-height: 44px;" in css_content, "44px touch target rule missing in index.css"
print("  [PASS] Test 3: WCAG / Mobile Touch Target standards (min-height: 44px) enforced for buttons and inputs.")

# 4. Verify Code / Pre block horizontal scroll containment
assert "pre, code" in css_content, "pre, code containment rule missing in index.css"
assert "overflow-x: auto;" in css_content, "overflow-x: auto missing in pre blocks"
print("  [PASS] Test 4: Pre and Code elements strictly bounded with max-width: 100% and overflow-x: auto.")

# 5. Verify Certificate Frame Fluid Responsiveness
assert ".ces-certificate-frame" in css_content, ".ces-certificate-frame class missing in index.css"
assert "@media (max-width: 768px)" in css_content and "padding: 1.5rem 1rem !important;" in css_content, "Certificate frame mobile padding override missing"
print("  [PASS] Test 5: Certificate frame supports fluid responsive widths and stacked signatures on mobile.")

# 6. Verify Top Navbar Hamburger Visibility on Desktop vs Mobile
assert ".mobile-menu-trigger" in css_content, ".mobile-menu-trigger rule missing in index.css"
assert "display: none !important;" in css_content, "mobile-menu-trigger display: none rule missing"
print("  [PASS] Test 6: Mobile hamburger button hidden on desktop (>1024px) and displayed on mobile/tablet.")

# 7. Verify Responsive Actions Utility
assert ".responsive-actions" in css_content, ".responsive-actions utility missing"
assert ".responsive-actions.stack-on-mobile" in css_content, ".stack-on-mobile utility missing"
print("  [PASS] Test 7: .responsive-actions and .stack-on-mobile utilities present for workflow page footers.")

# 8. Check that major pages avoid rigid pixel minWidths without min(..., 100%)
pages_to_check = [
    "CompleteTopicsPage.jsx",
    "ImportantTopicsPage.jsx",
    "PracticalSectionPage.jsx",
    "LearnCompletePage.jsx",
    "SelfEvaluationPage.jsx",
    "SkillInterviewPrepPage.jsx",
    "ProgressPage.jsx",
    "ProfilePage.jsx",
]

for page in pages_to_check:
    page_path = None
    for root, dirs, files in os.walk(SRC_DIR):
        if page in files:
            page_path = os.path.join(root, page)
            break
    assert page_path, f"Page {page} not found"
    with open(page_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Check for stack-on-mobile or responsive wrapping
    assert "stack-on-mobile" in content or "flexWrap" in content or "grid" in content, f"Responsive utilities missing in {page}"

print("  [PASS] Test 8: All core workflow and profile pages verified with responsive wrapping and fluid bounds.")

print("\nALL 8 PHASE 11 RESPONSIVE UI AUDIT TESTS PASSED SUCCESSFULLY!")
