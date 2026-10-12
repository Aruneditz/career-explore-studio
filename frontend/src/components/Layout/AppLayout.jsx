import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, Loader2, Sparkles } from 'lucide-react';
import Sidebar from '../Navigation/Sidebar';
import BrandLogo from '../Common/BrandLogo';
import AISearchTrigger from '../AI/AISearchTrigger';
import ErrorBoundary from '../Common/ErrorBoundary';
import { useAuth } from '../../context/AuthContext';

export default function AppLayout({ children, backendStatus }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user, isAuthenticated } = useAuth();
  const location = useLocation();

  // Extract contextual skillId and topicId from active route
  const matchSkill = location.pathname.match(/\/skills\/(\d+)/);
  const routeSkillId = matchSkill ? parseInt(matchSkill[1], 10) : null;
  const matchTopic = location.pathname.match(/\/topics\/(\d+)/);
  const routeTopicId = matchTopic ? parseInt(matchTopic[1], 10) : null;

  // Close mobile drawer on Escape key press
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  return (
    <div className="app-layout-wrapper">
      {/* Accessible Skip Link for Keyboard / Screen Reader Navigation */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      {/* Desktop Persistent Sidebar */}
      <aside className="desktop-sidebar" aria-label="Main Navigation">
        <Sidebar isMobile={false} />
      </aside>

      {/* Mobile Drawer Overlay */}
      {mobileMenuOpen && (
        <div 
          className="mobile-overlay" 
          onClick={() => setMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Mobile Sliding Drawer */}
      {mobileMenuOpen && (
        <div 
          className="mobile-sidebar-drawer"
          role="dialog"
          aria-modal="true"
          aria-label="Mobile Navigation Drawer"
        >
          <Sidebar isMobile={true} onClose={() => setMobileMenuOpen(false)} />
        </div>
      )}

      {/* Main Viewport Container */}
      <div className="app-main-viewport">
        {/* Top Navbar */}
        <header className="top-navbar" role="banner">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexShrink: 0 }}>
            {/* Mobile hamburger menu toggle - hidden on desktop, visible on mobile/tablet */}
            <button
              onClick={() => setMobileMenuOpen(true)}
              className="btn-icon mobile-menu-trigger"
              aria-label="Open navigation menu"
              aria-expanded={mobileMenuOpen}
            >
              <Menu size={20} />
            </button>

            <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center' }}>
              <BrandLogo size="sm" title="CAREER EXPLORE" subtitle="STUDIO" />
            </Link>
          </div>

          {/* Global Contextual AI Search Trigger */}
          <div style={{ display: 'flex', alignItems: 'center', flex: 1, justifyContent: 'center', maxWidth: '380px', margin: '0 0.5rem' }}>
            <AISearchTrigger skillId={routeSkillId} topicId={routeTopicId} />
          </div>

          {/* Right Header Status & Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexShrink: 0 }}>
            {backendStatus === 'healthy' && (
              <div className="badge badge-success top-navbar-status-badge" title="FastAPI Backend Live" role="status">
                <span className="status-dot active"></span>
                <span className="status-text">FastAPI Live</span>
              </div>
            )}

            {backendStatus === 'loading' && (
              <div className="badge badge-warning top-navbar-status-badge" title="Connecting to Backend API..." role="status">
                <Loader2 size={12} className="status-dot loading" />
                <span className="status-text">Connecting...</span>
              </div>
            )}

            {backendStatus === 'error' && (
              <div className="badge badge-warning top-navbar-status-badge" style={{ color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.3)' }} title="Backend Unreachable" role="status">
                <span className="status-dot error"></span>
                <span className="status-text">API Offline</span>
              </div>
            )}
          </div>
        </header>

        {/* Page Content Landmark with Localized Error Protection */}
        <main id="main-content" className="main-content" tabIndex="-1">
          <ErrorBoundary inline={true}>
            {children}
          </ErrorBoundary>
        </main>

        {/* Global Footer Landmark */}
        <footer role="contentinfo" style={{
          borderTop: '1px solid var(--border-subtle)',
          padding: '1.25rem 1.5rem',
          textAlign: 'center',
          color: 'var(--text-muted)',
          fontSize: '0.8125rem',
          backgroundColor: 'var(--bg-secondary)',
        }}>
          <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
            <div>
              <strong>CAREER EXPLORE STUDIO</strong> &bull; Personal Skill Learning, Roadmap & Interview Preparation
            </div>
            <div>
              FastAPI + SQLite/PostgreSQL Ready + React Router
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
