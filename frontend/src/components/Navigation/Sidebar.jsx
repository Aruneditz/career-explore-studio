import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  Compass, 
  Home, 
  Target, 
  BookOpen, 
  TrendingUp, 
  HelpCircle, 
  User, 
  LogOut, 
  X, 
  Sparkles, 
  ChevronRight 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import BrandLogo from '../Common/BrandLogo';
import AISearchAssistant from '../AI/AISearchAssistant';

const NAV_ITEMS = [
  { path: '/', label: 'Home', icon: Home, exact: true },
  { path: '/goals', label: 'Goals', icon: Target },
  { path: '/skills', label: 'Skills', icon: BookOpen },
  { path: '/progress', label: 'Progress', icon: TrendingUp },
  { path: '/interview-prep', label: 'Interview Preparation', icon: HelpCircle },
  { path: '/profile', label: 'Profile', icon: User },
];

export default function Sidebar({ isMobile, onClose }) {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [aiAssistantOpen, setAiAssistantOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    if (onClose) onClose();
    navigate('/login');
  };

  const handleNavClick = () => {
    if (isMobile && onClose) {
      onClose();
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Sidebar Header */}
      <div className="sidebar-header">
        <NavLink to="/" onClick={handleNavClick} style={{ textDecoration: 'none' }}>
          <BrandLogo size="md" />
        </NavLink>

        {isMobile && (
          <button 
            onClick={onClose} 
            className="btn-icon" 
            title="Close navigation menu"
            aria-label="Close navigation menu"
            style={{ width: '32px', height: '32px' }}
          >
            <X size={18} />
          </button>
        )}
      </div>

      {/* Navigation Links */}
      <nav className="sidebar-nav">
        <div className="sidebar-nav-heading">Platform Workflow</div>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.exact}
              onClick={handleNavClick}
              className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}

        <div className="sidebar-nav-heading" style={{ marginTop: '1rem' }}>AI Mentorship</div>
        <button
          type="button"
          onClick={() => {
            setAiAssistantOpen(true);
            if (isMobile && onClose) onClose();
          }}
          className="sidebar-link"
          style={{
            width: '100%',
            textAlign: 'left',
            background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(168, 85, 247, 0.12) 100%)',
            border: '1px solid rgba(99, 102, 241, 0.3)',
            borderRadius: 'var(--radius-md)',
            cursor: 'pointer',
            color: '#c7d2fe',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            padding: '0.625rem 0.875rem',
          }}
          title="Open AI Career Mentor"
        >
          <Sparkles size={18} style={{ color: '#a5b4fc', flexShrink: 0 }} />
          <span>AI Career Mentor</span>
        </button>
      </nav>

      {/* User Section / Footer */}
      <div className="sidebar-footer">
        {isAuthenticated && user ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <NavLink
              to="/profile"
              onClick={handleNavClick}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                textDecoration: 'none',
                color: 'inherit',
                padding: '0.5rem',
                borderRadius: 'var(--radius-md)',
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
              }}
            >
              <div
                style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'var(--accent-light)',
                  color: '#a5b4fc',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                }}
              >
                <User size={16} />
              </div>
              <div style={{ minWidth: 0, flex: 1 }}>
                <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--text-main)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user.name}
                </div>
                <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user.email}
                </div>
              </div>
              <ChevronRight size={14} color="var(--text-muted)" />
            </NavLink>

            <button
              onClick={handleLogout}
              className="btn btn-outline"
              style={{ width: '100%', fontSize: '0.75rem', height: '34px', minHeight: '34px', gap: '0.5rem' }}
            >
              <LogOut size={14} />
              <span>Sign Out</span>
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <NavLink
              to="/login"
              onClick={handleNavClick}
              className="btn btn-secondary"
              style={{ width: '100%', fontSize: '0.8125rem', minHeight: '36px' }}
            >
              Sign In
            </NavLink>
            <NavLink
              to="/register"
              onClick={handleNavClick}
              className="btn btn-primary"
              style={{ width: '100%', fontSize: '0.8125rem', minHeight: '36px' }}
            >
              Get Started
            </NavLink>
          </div>
        )}
      </div>

      {aiAssistantOpen && (
        <AISearchAssistant
          isModal={true}
          isOpen={aiAssistantOpen}
          onClose={() => setAiAssistantOpen(false)}
        />
      )}
    </div>
  );
}
