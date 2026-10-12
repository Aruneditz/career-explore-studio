import React, { useState, useEffect } from 'react';
import { 
  X, 
  Printer, 
  Copy, 
  Check, 
  Award, 
  ShieldCheck, 
  Compass, 
  Calendar, 
  CheckCircle2, 
  ExternalLink,
  Sparkles
} from 'lucide-react';
import BrandLogo from '../Common/BrandLogo';

export default function CertificateModal({ certificate, onClose }) {
  const [copiedId, setCopiedId] = useState(false);

  // Keyboard accessibility: Close on Escape key
  useEffect(() => {
    if (!certificate || !onClose) return;
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [certificate, onClose]);

  if (!certificate) return null;

  let metadata = {};
  try {
    if (certificate.metadata_json) {
      metadata = JSON.parse(certificate.metadata_json);
    }
  } catch (e) {
    console.error('Failed to parse certificate metadata', e);
  }

  const handleCopyId = async () => {
    try {
      await navigator.clipboard.writeText(certificate.certificate_id);
      setCopiedId(true);
      setTimeout(() => setCopiedId(false), 2000);
    } catch (e) {
      console.error('Failed to copy certificate ID', e);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const issueDateFormatted = certificate.issued_at
    ? new Date(certificate.issued_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });

  return (
    <div 
      className="certificate-modal-overlay"
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        backgroundColor: 'rgba(5, 8, 16, 0.88)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 'clamp(0.5rem, 2.5vw, 1.5rem)',
        overflowY: 'auto',
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div 
        className="certificate-modal-content"
        role="dialog"
        aria-modal="true"
        aria-labelledby="certificate-modal-title"
        style={{
          width: '100%',
          maxWidth: '920px',
          background: 'var(--bg-card)',
          borderRadius: '16px',
          border: '1px solid var(--border-medium)',
          boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 40px rgba(99, 102, 241, 0.2)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          animation: 'fadeInUp 250ms ease-out forwards',
        }}
      >
        {/* Modal Top Control Bar */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '0.875rem 1.25rem',
            background: 'var(--bg-secondary)',
            borderBottom: '1px solid var(--border-subtle)',
            flexWrap: 'wrap',
            gap: '0.75rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
            <Award size={20} color="#818cf8" aria-hidden="true" />
            <span id="certificate-modal-title" style={{ fontSize: '0.875rem', fontWeight: 700, color: '#f8fafc', letterSpacing: '0.02em' }}>
              Official Verified Credential
            </span>
            <span className="badge badge-success" style={{ fontSize: '0.6875rem' }}>
              Authenticated
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={handleCopyId}
              className="btn btn-secondary"
              style={{ fontSize: '0.8125rem', padding: '0.4rem 0.75rem', gap: '0.375rem' }}
              title="Copy Certificate ID"
              aria-label="Copy Certificate ID to clipboard"
            >
              {copiedId ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
              <span>{copiedId ? 'Copied' : 'Copy ID'}</span>
            </button>

            <button
              type="button"
              onClick={handlePrint}
              className="btn btn-primary"
              style={{ fontSize: '0.8125rem', padding: '0.4rem 0.85rem', gap: '0.375rem' }}
              aria-label="Print or save certificate as PDF"
            >
              <Printer size={14} />
              <span>Print / Save PDF</span>
            </button>

            <button
              type="button"
              onClick={onClose}
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
              }}
              aria-label="Close certificate modal"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Printable Certificate Frame */}
        <div style={{ padding: 'clamp(0.75rem, 2.5vw, 2rem)', overflowX: 'auto' }}>
          <div
            id="ces-certificate-frame"
            className="ces-certificate-frame"
          >
            {/* Inner Decorative Corner Border Accents */}
            <div style={{ position: 'absolute', top: '10px', left: '10px', width: '24px', height: '24px', borderTop: '2px solid #a5b4fc', borderLeft: '2px solid #a5b4fc' }} />
            <div style={{ position: 'absolute', top: '10px', right: '10px', width: '24px', height: '24px', borderTop: '2px solid #a5b4fc', borderRight: '2px solid #a5b4fc' }} />
            <div style={{ position: 'absolute', bottom: '10px', left: '10px', width: '24px', height: '24px', borderBottom: '2px solid #a5b4fc', borderLeft: '2px solid #a5b4fc' }} />
            <div style={{ position: 'absolute', bottom: '10px', right: '10px', width: '24px', height: '24px', borderBottom: '2px solid #a5b4fc', borderRight: '2px solid #a5b4fc' }} />

            {/* Certificate Header: Brand Logo & Title */}
            <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
              <div style={{ display: 'inline-flex', justifyContent: 'center', marginBottom: '0.875rem' }}>
                <BrandLogo size="md" />
              </div>

              <div style={{ fontSize: 'clamp(0.6875rem, 2vw, 0.8125rem)', letterSpacing: '0.25em', textTransform: 'uppercase', color: '#a5b4fc', fontWeight: 700, marginBottom: '0.5rem' }}>
                Skill Guidance & Vocational Excellence Council
              </div>

              <h1
                style={{
                  fontSize: 'clamp(1.35rem, 4vw, 2rem)',
                  fontWeight: 900,
                  letterSpacing: '0.04em',
                  textTransform: 'uppercase',
                  color: '#ffffff',
                  margin: '0 0 0.5rem',
                  background: 'linear-gradient(135deg, #ffffff 30%, #c7d2fe 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Certificate of Mastery
              </h1>

              <div style={{ width: '120px', height: '3px', background: 'linear-gradient(90deg, transparent, #6366f1, transparent)', margin: '0.75rem auto 0' }} />
            </div>

            {/* Recipient Text */}
            <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
              <p style={{ fontSize: '0.875rem', color: '#94a3b8', fontStyle: 'italic', margin: '0 0 0.5rem' }}>
                This is proudly presented and certified to
              </p>

              <h2
                style={{
                  fontSize: 'clamp(1.3rem, 4.5vw, 2.125rem)',
                  fontWeight: 800,
                  color: '#38bdf8',
                  letterSpacing: '-0.01em',
                  margin: '0 0 0.5rem',
                  textShadow: '0 2px 10px rgba(56, 189, 248, 0.25)',
                }}
              >
                {certificate.recipient_name}
              </h2>

              <p style={{ fontSize: 'clamp(0.8125rem, 2vw, 0.9rem)', color: '#cbd5e1', maxWidth: '600px', margin: '0 auto', lineHeight: 1.6 }}>
                for successfully completing all required coursework topics, hands-on practical labs, 
                diagnostic self-evaluations, and technical interview preparation in:
              </p>
            </div>

            {/* Subject / Skill Awarded Box */}
            <div
              style={{
                textAlign: 'center',
                padding: '1rem 1.5rem',
                background: 'rgba(99, 102, 241, 0.08)',
                borderRadius: '10px',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                maxWidth: '560px',
                margin: '0 auto 1.75rem',
              }}
            >
              <h3 style={{ fontSize: 'clamp(1.1rem, 3.5vw, 1.4rem)', fontWeight: 800, color: '#f8fafc', margin: '0 0 0.375rem' }}>
                {certificate.title.replace('Certificate of Mastery: ', '')}
              </h3>
              {metadata.goal_title && (
                <div style={{ fontSize: '0.8125rem', color: '#a5b4fc', fontWeight: 600 }}>
                  Career Track: {metadata.goal_title}
                </div>
              )}
            </div>

            {/* Certificate Footer: Details & Signatures */}
            <div
              className="certificate-footer-grid"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-end',
                flexWrap: 'wrap',
                gap: '1.5rem',
                borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                paddingTop: '1.5rem',
              }}
            >
              {/* Left: Credential Verification Block */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', color: '#10b981', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  <ShieldCheck size={15} />
                  <span>Verified Credential</span>
                </div>
                <div style={{ fontSize: '0.8125rem', fontFamily: 'monospace', color: '#94a3b8' }}>
                  ID: <span style={{ color: '#f8fafc', fontWeight: 700 }}>{certificate.certificate_id}</span>
                </div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                  Issued: {issueDateFormatted}
                </div>
              </div>

              {/* Middle: Digital Seal */}
              <div
                style={{
                  width: '74px',
                  height: '74px',
                  borderRadius: '50%',
                  background: 'radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%)',
                  border: '2px dashed #818cf8',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#a5b4fc',
                  margin: '0 auto',
                }}
              >
                <Sparkles size={18} color="#a5b4fc" />
                <span style={{ fontSize: '0.55rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em', marginTop: '2px' }}>
                  CES SEAL
                </span>
              </div>

              {/* Right: Official Signatures */}
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontFamily: 'cursive', fontSize: '1.25rem', color: '#e2e8f0', marginBottom: '0.25rem' }}>
                  Academic Board of CES
                </div>
                <div style={{ width: '160px', height: '1px', background: 'rgba(255, 255, 255, 0.3)', marginLeft: 'auto', marginBottom: '0.375rem' }} />
                <div style={{ fontSize: '0.6875rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#94a3b8', fontWeight: 600 }}>
                  Curriculum & Evaluation Director
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Modal Bottom Bar */}
        <div
          style={{
            padding: '1rem 1.5rem',
            background: 'var(--bg-secondary)',
            borderTop: '1px solid var(--border-subtle)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '1rem',
          }}
        >
          <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
            This official credential can be verified at any time using your Certificate ID.
          </div>

          <button onClick={onClose} className="btn btn-secondary" style={{ fontSize: '0.8125rem' }}>
            Close Preview
          </button>
        </div>
      </div>
    </div>
  );
}
