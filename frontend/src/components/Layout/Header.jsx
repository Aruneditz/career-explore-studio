import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, LogOut, LogIn, UserPlus, Loader2 } from 'lucide-react';
import BrandLogo from '../Common/BrandLogo';
import { useAuth } from '../../context/AuthContext';

export default function Header({ backendStatus }) {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="header-glass">
      <div className="header-inner">
        {/* Brand identity */}
        <Link to="/" style={{ textDecoration: 'none' }}>
          <BrandLogo size="md" />
        </Link>

        {/* Right Nav: Status & Authentication Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          {/* Backend Status Badge */}
          <div className="status-container" style={{ display: 'flex', alignItems: 'center' }}>
            {backendStatus === 'healthy' && (
              <div className="badge badge-success" title="FastAPI Backend Connected">
                <span className="status-dot active"></span>
                <span>FastAPI Live</span>
              </div>
            )}

            {backendStatus === 'loading' && (
              <div className="badge badge-warning" title="Connecting to Backend API...">
                <Loader2 size={12} className="status-dot loading" />
                <span>Connecting...</span>
              </div>
            )}

            {backendStatus === 'error' && (
              <div className="badge badge-warning" style={{ color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.3)' }} title="Backend Unreachable">
                <span className="status-dot error"></span>
                <span>API Offline</span>
              </div>
            )}
          </div>

          {/* User Profile or Auth Buttons */}
          {isAuthenticated && user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.35rem 0.75rem',
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border-medium)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.8125rem',
                }}
              >
                <div
                  style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '50%',
                    background: 'var(--accent-light)',
                    color: '#a5b4fc',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <User size={14} />
                </div>
                <span style={{ fontWeight: 600, color: 'var(--text-main)', maxWidth: '140px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {user.name}
                </span>
              </div>

              <button
                onClick={handleLogout}
                className="btn btn-outline"
                style={{ padding: '0.4rem 0.75rem', minHeight: '34px', height: '34px', fontSize: '0.75rem' }}
                title="Sign out of your account"
              >
                <LogOut size={14} />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Link
                to="/login"
                className="btn btn-secondary"
                style={{ padding: '0.4rem 0.85rem', minHeight: '34px', height: '34px', fontSize: '0.8125rem' }}
              >
                <LogIn size={14} />
                <span>Sign In</span>
              </Link>
              <Link
                to="/register"
                className="btn btn-primary"
                style={{ padding: '0.4rem 0.85rem', minHeight: '34px', height: '34px', fontSize: '0.8125rem' }}
              >
                <UserPlus size={14} />
                <span>Sign Up</span>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
