/*
 * SexyScroll (Vanilla JS Port)
 * Ported from: https://framer.com/m/SexyScroll-PPLp.js@7igGURKkQfQxK8ucTl83
 */

(function() {
  // A11y: respect prefers-reduced-motion
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  // Disable smooth scroll on mobile and touch devices to prevent conflicts with native momentum scrolling
  if (window.matchMedia('(max-width: 768px)').matches || window.matchMedia('(hover: none)').matches) {
    return;
  }

  // Remove CSS smooth scroll behavior to prevent physics conflicts
  const style = document.createElement('style');
  style.textContent = 'html { scroll-behavior: auto !important; }';
  document.head.appendChild(style);

  // Configuration (Portfolio Preset)
  const smoothTime = 0.6;
  const maxSpeed = 4500;
  const keyboardLines = 1.0;
  const pageJumpRatio = 0.9;
  const touchEnabled = false; // default is false in Framer
  const showBadge = false;    // disabled by default for cleaner production look (can be toggled)

  let currentY = window.scrollY;
  let targetY = window.scrollY;
  let velocityY = 0;
  let rafId = null;
  let lastTimestamp = null;

  // Unity-like SmoothDamp algorithm
  function smoothDamp(current, target, currentVelocity, smoothTime, maxSpeed, deltaTime) {
    const EPS = 1e-4;
    smoothTime = Math.max(EPS, smoothTime);
    const maxChange = maxSpeed * smoothTime;
    let delta = target - current;
    const originalTarget = target;
    
    if (Math.abs(delta) > maxChange) {
      target = current + Math.sign(delta) * maxChange;
    }
    
    const omega = 2 / smoothTime;
    const x = omega * deltaTime;
    const exp = 1 / (1 + x + 0.48 * x * x + 0.235 * x * x * x);
    const change = current - target;
    const temp = (currentVelocity + omega * change) * deltaTime;
    
    let newVelocity = (currentVelocity - omega * temp) * exp;
    let newValue = target + (change + temp) * exp;
    
    const origToCurrent = originalTarget - current;
    const newToOrig = newValue - originalTarget;
    
    if (origToCurrent > 0 === newToOrig > 0) {
      newValue = originalTarget;
      newVelocity = 0;
    }
    
    return [newValue, newVelocity];
  }

  function clamp(y) {
    const max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    return Math.max(0, Math.min(y, max));
  }

  function loop(timestamp) {
    if (lastTimestamp === null) {
      lastTimestamp = timestamp;
    }
    
    const dt = Math.max(0.001, Math.min(0.033, (timestamp - lastTimestamp) / 1000));
    lastTimestamp = timestamp;

    const clampedTarget = clamp(targetY);
    const [nextY, nextVel] = smoothDamp(currentY, clampedTarget, velocityY, smoothTime, maxSpeed, dt);
    
    currentY = nextY;
    velocityY = nextVel;
    window.scrollTo(0, currentY);

    // Stop the RAF loop when we are very close to the target
    if (Math.abs(currentY - clampedTarget) < 0.2 && Math.abs(velocityY) < 2) {
      currentY = clampedTarget;
      velocityY = 0;
      window.scrollTo(0, clampedTarget);
      rafId = null;
      lastTimestamp = null;
    } else {
      rafId = requestAnimationFrame(loop);
    }
  }

  function startLoop() {
    if (rafId === null) {
      lastTimestamp = null;
      rafId = requestAnimationFrame(loop);
    }
  }

  function scrollToTarget(y) {
    targetY = clamp(y);
    startLoop();
  }

  function nudge(dy) {
    targetY = clamp(targetY + dy);
    startLoop();
  }

  // Mouse Wheel scrolling
  window.addEventListener('wheel', function(e) {
    if (e.ctrlKey || e.shiftKey || e.altKey) return;
    
    e.preventDefault();
    const factor = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? window.innerHeight : 1;
    const dy = e.deltaY * factor;
    nudge(dy);
  }, { passive: false });

  // Keyboard scrolling
  window.addEventListener('keydown', function(e) {
    const el = e.target;
    if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable)) {
      return;
    }

    const line = 48 * keyboardLines;
    const h = window.innerHeight * pageJumpRatio;

    switch (e.code) {
      case 'ArrowDown':
        e.preventDefault();
        nudge(line);
        break;
      case 'ArrowUp':
        e.preventDefault();
        nudge(-line);
        break;
      case 'PageDown':
        e.preventDefault();
        nudge(h);
        break;
      case 'PageUp':
        e.preventDefault();
        nudge(-h);
        break;
      case 'Space':
        e.preventDefault();
        nudge(e.shiftKey ? -h : h);
        break;
      case 'Home':
        e.preventDefault();
        scrollToTarget(0);
        break;
      case 'End':
        e.preventDefault();
        scrollToTarget(document.documentElement.scrollHeight);
        break;
    }
  }, { passive: false });

  // Touch scrolling (if enabled)
  if (touchEnabled) {
    let lastY = 0;
    window.addEventListener('touchmove', function(e) {
      if (e.touches.length !== 1) return;
      const y = e.touches[0].clientY;
      const dy = lastY ? lastY - y : 0;
      lastY = y;
      if (Math.abs(dy) > 0) {
        e.preventDefault();
        nudge(dy);
      }
    }, { passive: false });
    
    window.addEventListener('touchend', function() {
      lastY = 0;
    }, { passive: true });
  }

  // Sync scroll positions when scrolling externally (e.g. dragging scrollbar or clicking anchor links)
  window.addEventListener('scroll', function() {
    if (rafId === null) {
      currentY = window.scrollY;
      targetY = window.scrollY;
    }
  }, { passive: true });

  // Optional Visual Badge
  if (showBadge) {
    const badge = document.createElement('div');
    badge.style.cssText = 'position:fixed;top:12px;left:12px;z-index:99999;pointer-events:none;user-select:none;font-family:Inter,system-ui,sans-serif;font-size:12px;padding:6px 8px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.12);background:rgba(20,20,20,0.85);color:#fff;';
    badge.textContent = 'Sexy Scroll (by Baco): Portfolio';
    document.body.appendChild(badge);
  }
})();
