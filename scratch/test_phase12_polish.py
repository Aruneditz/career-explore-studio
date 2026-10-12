"""
Test script for Phase 12 Polish:
Verifies performance optimizations, client-side caching & deduplication,
accessible loading/empty states, localized error boundaries, modal keyboard/focus trapping,
and Section 13 UI string exact compliance.
"""
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
FRONTEND_SRC = WORKSPACE / "frontend" / "src"

def check(condition, message):
    if not condition:
        print(f"[FAIL] {message}")
        sys.exit(1)
    print(f"[PASS] {message}")

def test_api_client():
    api_file = FRONTEND_SRC / "services" / "api.js"
    content = api_file.read_text(encoding="utf-8")
    check("this.cache = new Map()" in content, "In-memory TTL request cache initialized in api.js")
    check("this.inFlight = new Map()" in content, "In-flight request deduplication map initialized in api.js")
    check("clearCache" in content, "clearCache method defined in api.js")
    check("invalidateCacheForMutation" in content, "Cache invalidation on mutations defined in api.js")
    check("this.defaultTtlMs = 30000" in content, "TTL expiration configured in api.js")

def test_loading_state():
    loading_file = FRONTEND_SRC / "components" / "Common" / "LoadingState.jsx"
    content = loading_file.read_text(encoding="utf-8")
    check('role="status"' in content, 'LoadingState contains role="status"')
    check('aria-live="polite"' in content, 'LoadingState contains aria-live="polite"')
    check('className="sr-only"' in content, 'LoadingState contains screen-reader only announcement')
    check('skeleton-bar' in content, 'LoadingState contains skeleton-bar class')
    check('memo(' in content, 'LoadingState is memoized with React.memo')

def test_empty_state():
    empty_file = FRONTEND_SRC / "components" / "Common" / "EmptyState.jsx"
    content = empty_file.read_text(encoding="utf-8")
    check('role="region"' in content, 'EmptyState contains role="region"')
    check('aria-label' in content, 'EmptyState contains aria-label attribute')
    check('memo(' in content, 'EmptyState is memoized with React.memo')

def test_memoization():
    logo_file = FRONTEND_SRC / "components" / "Common" / "BrandLogo.jsx"
    logo_content = logo_file.read_text(encoding="utf-8")
    check('memo(' in logo_content, 'BrandLogo is memoized with React.memo')

    wf_file = FRONTEND_SRC / "components" / "Navigation" / "WorkflowProgressIndicator.jsx"
    wf_content = wf_file.read_text(encoding="utf-8")
    check('memo(' in wf_content, 'WorkflowProgressIndicator is memoized with React.memo')
    check('<nav' in wf_content, 'WorkflowProgressIndicator uses semantic <nav> element')
    check('aria-current=' in wf_content, 'WorkflowProgressIndicator marks active step with aria-current')

def test_error_boundary():
    eb_file = FRONTEND_SRC / "components" / "Common" / "ErrorBoundary.jsx"
    eb_content = eb_file.read_text(encoding="utf-8")
    check('inline' in eb_content, 'ErrorBoundary supports inline rendering prop')
    check('role="alert"' in eb_content, 'ErrorBoundary uses role="alert"')
    check('Try Again' in eb_content, 'ErrorBoundary provides Try Again recovery action')

    layout_file = FRONTEND_SRC / "components" / "Layout" / "AppLayout.jsx"
    layout_content = layout_file.read_text(encoding="utf-8")
    check('<ErrorBoundary inline={true}>' in layout_content, 'AppLayout wraps main content in inline ErrorBoundary')

def test_modals_a11y():
    cert_modal = FRONTEND_SRC / "components" / "Certificate" / "CertificateModal.jsx"
    cert_content = cert_modal.read_text(encoding="utf-8")
    check('role="dialog"' in cert_content, 'CertificateModal has role="dialog"')
    check('aria-modal="true"' in cert_content, 'CertificateModal has aria-modal="true"')
    check('aria-labelledby=' in cert_content, 'CertificateModal has aria-labelledby')
    check("e.key === 'Escape'" in cert_content, 'CertificateModal listens to Escape key for dismissal')

    ai_modal = FRONTEND_SRC / "components" / "AI" / "AISearchAssistant.jsx"
    ai_content = ai_modal.read_text(encoding="utf-8")
    check('role="dialog"' in ai_content, 'AISearchAssistant has role="dialog"')
    check('aria-modal="true"' in ai_content, 'AISearchAssistant has aria-modal="true"')
    check("e.key === 'Escape'" in ai_content, 'AISearchAssistant listens to Escape key')

def test_section13_exact_strings():
    ai_file = FRONTEND_SRC / "components" / "AI" / "AISearchAssistant.jsx"
    ai_content = ai_file.read_text(encoding="utf-8")
    check('Thinking...' in ai_content, 'AISearchAssistant has exact string: Thinking...')
    check('Something went wrong. Please try again.' in ai_content, 'AISearchAssistant has exact string: Something went wrong. Please try again.')
    check('Ask a question to get started.' in ai_content, 'AISearchAssistant has exact string: Ask a question to get started.')

    cert_status = FRONTEND_SRC / "components" / "Certificate" / "CertificateStatusCard.jsx"
    cert_status_content = cert_status.read_text(encoding="utf-8")
    check('Congratulations! Your certificate is ready.' in cert_status_content, 'CertificateStatusCard has exact string: Congratulations! Your certificate is ready.')
    check('Complete all required stages to unlock your certificate.' in cert_status_content, 'CertificateStatusCard has exact string: Complete all required stages to unlock your certificate.')

    progress_page = FRONTEND_SRC / "pages" / "Progress" / "ProgressPage.jsx"
    prog_content = progress_page.read_text(encoding="utf-8")
    check('Complete all required stages to unlock your certificate.' in prog_content, 'ProgressPage has exact string: Complete all required stages to unlock your certificate.')

def test_css_styles():
    css_file = FRONTEND_SRC / "index.css"
    css_content = css_file.read_text(encoding="utf-8")
    check('focus-visible' in css_content, 'index.css defines universal focus-visible styles')
    check('.skeleton-bar' in css_content, 'index.css defines .skeleton-bar styling')
    check('skeletonShimmer' in css_content, 'index.css defines skeletonShimmer animation keyframes')

def main():
    print("=" * 60)
    print("RUNNING PHASE 12 AUDIT TESTS")
    print("=" * 60)
    test_api_client()
    test_loading_state()
    test_empty_state()
    test_memoization()
    test_error_boundary()
    test_modals_a11y()
    test_section13_exact_strings()
    test_css_styles()
    print("=" * 60)
    print("ALL PHASE 12 POLISH & A11Y TESTS PASSED!")
    print("=" * 60)

if __name__ == '__main__':
    main()
