# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add GSAP and SplitType CDNs at the bottom of the body
scripts = '''
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
  <script src="https://unpkg.com/split-type"></script>
'''
content = content.replace('<!-- --------------------------------------- JS -->', '<!-- --------------------------------------- JS -->\\n' + scripts)

# 2. Preloader HTML & CSS
preloader_html = '''
  <!-- PRELOADER -->
  <div id="preloader" style="position:fixed; inset:0; z-index:99999; background:var(--bg); display:flex; flex-direction:column; align-items:center; justify-content:center; color:var(--acid); font-family:var(--font-alt);">
    <div style="font-size:3rem; font-weight:800; letter-spacing:-0.05em; text-transform:uppercase;" class="glitch" data-text="ANTIGRAVITY">ANTIGRAVITY</div>
    <div style="font-size:0.8rem; letter-spacing:0.3em; margin-top:10px; color:var(--text);">ENGINE INITIALIZING... <span id="load-pct">0</span>%</div>
    <div style="width:200px; height:2px; background:var(--surface); margin-top:20px; overflow:hidden; border-radius:2px;">
      <div id="load-bar" style="width:0%; height:100%; background:var(--acid);"></div>
    </div>
  </div>
'''
content = content.replace('<div class="noise" aria-hidden="true"></div>', '<div class="noise" aria-hidden="true"></div>\\n' + preloader_html)

# 3. New CSS for Animations
extra_css = '''
    /* ANTIGRAVITY FLOATING */
    .float { animation: antigrav 6s ease-in-out infinite; }
    .float-delay-1 { animation-delay: -1.5s; }
    .float-delay-2 { animation-delay: -3s; }
    .float-delay-3 { animation-delay: -4.5s; }
    @keyframes antigrav {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-15px); }
    }
    
    /* SPLIT TEXT STYLES */
    .char { transform: translateY(115%); opacity:0; transition: transform .5s cubic-bezier(.3,0,0,1), opacity .5s; }
    .word { overflow: hidden; display: inline-flex; padding-bottom: 0.1em; margin-bottom: -0.1em; }
    
    /* RGB GLITCH HOVER */
    .btn:hover {
      text-shadow: 2px 0 var(--pink), -2px 0 var(--teal);
      animation: button-shake 0.2s infinite;
    }
    @keyframes button-shake {
      0% { transform: translate(1px, 1px) rotate(0deg); }
      20% { transform: translate(-1px, 0px) rotate(0.5deg); }
      40% { transform: translate(1px, -1px) rotate(-0.5deg); }
      60% { transform: translate(-1px, 1px) rotate(0deg); }
      80% { transform: translate(1px, -1px) rotate(0.5deg); }
      100% { transform: translate(1px, 1px) rotate(0deg); }
    }
    
    /* SHIMMER BORDER ENHANCEMENT */
    .project-card, .skill-card, .ba-card { position: relative; }
    .project-card::before, .skill-card::before, .ba-card::before {
      content: ''; position: absolute; inset: -2px; border-radius: inherit;
      background: conic-gradient(from var(--angle), transparent 70%, var(--acid) 85%, var(--purple) 100%);
      z-index: -1; opacity: 0; transition: opacity 0.3s; animation: spin-angle 4s linear infinite;
    }
    .project-card:hover::before, .skill-card:hover::before, .ba-card:hover::before { opacity: 1; }
    
    /* MOUSE TRAIL */
    .trail { position: fixed; width: 10px; height: 10px; border-radius: 50%; background: var(--acid); pointer-events: none; z-index: 9998; mix-blend-mode: screen; opacity: 0; }
'''
content = content.replace('</style>', extra_css + '\\n  </style>')

# 4. Add floating classes to elements
content = content.replace('class="project-card reveal"', 'class="project-card reveal float"')
content = content.replace('class="skill-card skill-card--accent reveal"', 'class="skill-card skill-card--accent reveal float"')
content = content.replace('class="skill-card reveal"', 'class="skill-card reveal float float-delay-1"')
content = content.replace('class="ba-card ba-card--before"', 'class="ba-card ba-card--before float float-delay-2"')
content = content.replace('class="ba-card ba-card--after shimmer-card"', 'class="ba-card ba-card--after shimmer-card float float-delay-3"')
content = content.replace('class="stat"', 'class="stat float"')

# 5. Add custom JS script block for GSAP animations
js_logic = '''
    // -- Preloader & GSAP
    gsap.registerPlugin(ScrollTrigger);
    
    let loadPct = 0;
    const pctEl = document.getElementById('load-pct');
    const barEl = document.getElementById('load-bar');
    const interval = setInterval(() => {
      loadPct += Math.floor(Math.random() * 15) + 5;
      if(loadPct >= 100) {
        loadPct = 100;
        clearInterval(interval);
        setTimeout(() => {
          gsap.to('#preloader', { yPercent: -100, duration: 1, ease: 'power4.inOut', onComplete: initAnimations });
        }, 300);
      }
      pctEl.textContent = loadPct;
      barEl.style.width = loadPct + '%';
    }, 100);

    function initAnimations() {
      // Split Texts
      const titles = new SplitType('.hero__title, .section__title', { types: 'words, chars' });
      
      // Animate Hero
      gsap.to('#hero-title .char', { y: 0, opacity: 1, stagger: 0.02, duration: 1, ease: 'back.out(1.5)' });
      gsap.fromTo('.hero__subtitle', {y: 30, opacity: 0}, {y: 0, opacity: 1, duration: 1, delay: 0.5, ease: 'power3.out'});
      gsap.fromTo('.hero__actions', {scale: 0.8, opacity: 0}, {scale: 1, opacity: 1, duration: 0.8, delay: 0.8, ease: 'back.out(2)'});
      
      // Scroll Trigger Titles
      document.querySelectorAll('.section__title').forEach(title => {
        gsap.to(title.querySelectorAll('.char'), {
          scrollTrigger: { trigger: title, start: 'top 85%' },
          y: 0, opacity: 1, stagger: 0.01, duration: 0.8, ease: 'back.out(1.5)'
        });
      });
      
      // Parallax Images
      gsap.utils.toArray('.about-img__inner img, .ba-visual img').forEach(img => {
        gsap.to(img, {
          yPercent: 20, ease: 'none',
          scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true }
        });
      });
      
      // Glitch text effect randomly on titles
      setInterval(() => {
        const chars = document.querySelectorAll('.hero__title .char');
        if(chars.length) {
          const rand = chars[Math.floor(Math.random() * chars.length)];
          gsap.to(rand, { y: -10, color: 'var(--acid)', duration: 0.1, yoyo: true, repeat: 1, onComplete: () => gsap.to(rand, {color: 'var(--text)', duration:0.1})});
        }
      }, 2000);
    }
    
    // -- Mouse Trails
    const trails = [];
    for(let i=0; i<5; i++) {
      let d = document.createElement('div');
      d.className = 'trail';
      document.body.appendChild(d);
      trails.push({ el: d, x: 0, y: 0 });
    }
    let mx=0, my=0;
    window.addEventListener('mousemove', e => { mx=e.clientX; my=e.clientY; });
    gsap.ticker.add(() => {
      trails.forEach((t, i) => {
        const next = i === 0 ? {x: mx, y: my} : trails[i-1];
        t.x += (next.x - t.x) * (0.3 - i*0.04);
        t.y += (next.y - t.y) * (0.3 - i*0.04);
        gsap.set(t.el, { x: t.x, y: t.y, opacity: 1 - i*0.15, scale: 1 - i*0.15 });
      });
    });
'''
content = content.replace('lucide.createIcons();', 'lucide.createIcons();\\n' + js_logic)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
