import React, { memo } from 'react';
import { Compass } from 'lucide-react';

/**
 * Reusable CES Brand Logo Component
 * Renders the modern white compass icon inside a purple/indigo rounded container
 * with aligned "CAREER EXPLORE" and "SKILL GUIDANCE STUDIO" typography.
 * Memoized in Phase 12 for high rendering performance.
 *
 * @param {'sm' | 'md' | 'lg' | 'xl'} size - Container and icon size
 * @param {boolean} showText - Whether to render brand title and subtitle text
 * @param {string} title - Primary brand title (defaults to "CAREER EXPLORE")
 * @param {string} subtitle - Secondary brand subtitle (defaults to "SKILL GUIDANCE STUDIO")
 * @param {string} className - Additional CSS class names
 * @param {object} style - Additional inline styles
 * @param {number} iconSize - Optional custom icon pixel size override
 */
function BrandLogoComponent({
  size = 'md',
  showText = true,
  title = 'CAREER EXPLORE',
  subtitle = 'SKILL GUIDANCE STUDIO',
  className = '',
  style = {},
  iconSize
}) {
  const sizeMap = {
    sm: { containerClass: 'sm', iconPx: 16 },
    md: { containerClass: '', iconPx: 20 },
    lg: { containerClass: 'lg', iconPx: 26 },
    xl: { containerClass: 'xl', iconPx: 36 }
  };

  const selectedSize = sizeMap[size] || sizeMap.md;
  const computedIconSize = iconSize || selectedSize.iconPx;

  return (
    <div 
      className={`brand-wrapper ${className}`} 
      style={{ userSelect: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.75rem', ...style }}
    >
      <div
        className={`brand-logo-badge ${selectedSize.containerClass}`}
        aria-hidden="true"
      >
        <Compass size={computedIconSize} color="#ffffff" strokeWidth={2.2} />
      </div>

      {showText && (
        <div className="brand-text-container" style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.2 }}>
          <div className="brand-title">{title}</div>
          {subtitle && <div className="brand-subtitle">{subtitle}</div>}
        </div>
      )}
    </div>
  );
}

export const BrandLogo = memo(BrandLogoComponent);
export default BrandLogo;
