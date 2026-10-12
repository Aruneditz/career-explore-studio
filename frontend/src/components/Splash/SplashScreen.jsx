import React, { useEffect, useRef, useState } from 'react';
import { Sparkles, TrendingUp, Award, BookOpen, Layers } from 'lucide-react';
import BrandLogo from '../Common/BrandLogo';

export default function SplashScreen({ onFinish }) {
  const canvasRef = useRef(null);
  const [progress, setProgress] = useState(0);
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    // Canvas animation for career roadmap, skill nodes and growth pulses
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    // Career Roadmap Nodes
    const numNodes = Math.min(24, Math.floor((width * height) / 45000));
    const nodes = [];
    const skillTerms = ['Skills', 'Learn', 'Practical', 'Evaluation', 'Interview', 'Roadmap', 'Growth', 'Mastery'];

    for (let i = 0; i < numNodes; i++) {
      nodes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.7,
        vy: (Math.random() - 0.5) * 0.7,
        radius: Math.random() * 3 + 2,
        label: skillTerms[i % skillTerms.length],
        pulse: Math.random() * Math.PI,
      });
    }

    const pulses = [];
    let lastPulseTime = 0;

    const render = (time) => {
      ctx.clearRect(0, 0, width, height);

      // Background gradient
      const bgGrad = ctx.createRadialGradient(width / 2, height / 2, 50, width / 2, height / 2, width * 0.7);
      bgGrad.addColorStop(0, '#131b2e');
      bgGrad.addColorStop(1, '#070a12');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      // Update and connect nodes
      for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        node.x += node.vx;
        node.y += node.vy;
        node.pulse += 0.03;

        if (node.x < 0 || node.x > width) node.vx *= -1;
        if (node.y < 0 || node.y > height) node.vy *= -1;

        // Draw connections
        for (let j = i + 1; j < nodes.length; j++) {
          const other = nodes[j];
          const dx = other.x - node.x;
          const dy = other.y - node.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 180) {
            const alpha = (1 - dist / 180) * 0.25;
            ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(node.x, node.y);
            ctx.lineTo(other.x, other.y);
            ctx.stroke();

            // Spawn intermittent learning pulse traveling along roadmap
            if (time - lastPulseTime > 400 && pulses.length < 12 && Math.random() < 0.08) {
              pulses.push({
                fromX: node.x,
                fromY: node.y,
                toX: other.x,
                toY: other.y,
                progress: 0,
                speed: 0.02 + Math.random() * 0.02,
              });
              lastPulseTime = time;
            }
          }
        }

        // Draw node
        const glow = Math.sin(node.pulse) * 2 + 3;
        ctx.fillStyle = 'rgba(129, 140, 248, 0.85)';
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = 'rgba(99, 102, 241, 0.4)';
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + glow, 0, Math.PI * 2);
        ctx.stroke();

        // Node label
        ctx.font = '10px "Plus Jakarta Sans", sans-serif';
        ctx.fillStyle = 'rgba(148, 163, 184, 0.6)';
        ctx.fillText(node.label, node.x + 8, node.y + 3);
      }

      // Render pulses
      for (let k = pulses.length - 1; k >= 0; k--) {
        const p = pulses[k];
        p.progress += p.speed;
        if (p.progress >= 1) {
          pulses.splice(k, 1);
          continue;
        }

        const px = p.fromX + (p.toX - p.fromX) * p.progress;
        const py = p.fromY + (p.toY - p.fromY) * p.progress;

        ctx.fillStyle = '#38bdf8';
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(px, py, 2.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      animationFrameId = requestAnimationFrame(render);
    };

    // Draw first frame immediately
    render(performance.now());

    return () => {
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // Animated progress timer with robust cleanup and no updater side-effects
  const finishTriggeredRef = useRef(false);

  useEffect(() => {
    let finishTimeout = null;
    const duration = 2600; // ms
    const interval = 30; // ms
    const step = 100 / (duration / interval);

    const timer = setInterval(() => {
      setProgress((prev) => {
        const next = prev + step;
        if (next >= 100) {
          clearInterval(timer);
          if (!finishTriggeredRef.current) {
            finishTriggeredRef.current = true;
            setFadeOut(true);
            finishTimeout = setTimeout(() => {
              if (onFinish) onFinish();
            }, 350);
          }
          return 100;
        }
        return next;
      });
    }, interval);

    return () => {
      clearInterval(timer);
      if (finishTimeout) clearTimeout(finishTimeout);
    };
  }, [onFinish]);

  const skipTimeoutRef = useRef(null);

  const handleSkip = () => {
    if (finishTriggeredRef.current) return;
    finishTriggeredRef.current = true;
    setFadeOut(true);
    if (skipTimeoutRef.current) clearTimeout(skipTimeoutRef.current);
    skipTimeoutRef.current = setTimeout(() => {
      if (onFinish) onFinish();
    }, 200);
  };

  useEffect(() => {
    return () => {
      if (skipTimeoutRef.current) clearTimeout(skipTimeoutRef.current);
    };
  }, []);

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 99999,
        background: 'radial-gradient(circle at 50% 50%, #131b2e 0%, #070a12 100%)',
        backgroundColor: '#070a12',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity: fadeOut ? 0 : 1,
        transition: 'opacity 350ms cubic-bezier(0.16, 1, 0.3, 1)',
        userSelect: 'none',
        overflow: 'hidden',
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
        }}
      />

      {/* Center Branding Content */}
      <div
        style={{
          position: 'relative',
          zIndex: 10,
          textAlign: 'center',
          padding: '2rem',
          maxWidth: '640px',
          animation: 'fadeInUp 800ms cubic-bezier(0.16, 1, 0.3, 1)',
        }}
      >
        <BrandLogo size="xl" showText={false} style={{ margin: '0 auto 1.5rem' }} />

        <h1
          style={{
            fontSize: 'clamp(2rem, 5vw, 2.75rem)',
            fontWeight: 800,
            letterSpacing: '-0.03em',
            lineHeight: 1.15,
            marginBottom: '0.75rem',
            background: 'linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            textShadow: '0 4px 20px rgba(0, 0, 0, 0.4)',
          }}
        >
          CAREER EXPLORE STUDIO
        </h1>

        <div
          style={{
            fontSize: 'clamp(0.875rem, 2vw, 1.05rem)',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.22em',
            color: '#818cf8',
            marginBottom: '2rem',
          }}
        >
          CAREER SKILL GUIDANCE
        </div>

        {/* Progress Bar */}
        <div
          style={{
            width: '260px',
            height: '4px',
            background: 'rgba(255, 255, 255, 0.08)',
            borderRadius: '9999px',
            margin: '0 auto 1rem',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #6366f1, #38bdf8)',
              borderRadius: '9999px',
              transition: 'width 60ms linear',
              boxShadow: '0 0 10px #38bdf8',
            }}
          />
        </div>

        <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
          Preparing your personalized skill roadmap...
        </div>

        <button
          onClick={handleSkip}
          style={{
            marginTop: '1.25rem',
            background: 'transparent',
            border: 'none',
            color: '#94a3b8',
            fontSize: '0.75rem',
            cursor: 'pointer',
            padding: '0.4rem 0.8rem',
            borderRadius: '4px',
            transition: 'color 150ms',
          }}
          onMouseEnter={(e) => (e.target.style.color = '#ffffff')}
          onMouseLeave={(e) => (e.target.style.color = '#94a3b8')}
        >
          Skip Intro &rarr;
        </button>
      </div>
    </div>
  );
}
