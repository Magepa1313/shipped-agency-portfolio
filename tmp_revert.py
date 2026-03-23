import sys

file_path = r'c:\Users\maxim\OneDrive\Desktop\landscaping\portfolio\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

cursor_dom = '''
  <div class="cursor-dot" id="cursor-dot"></div>
  <div class="cursor-outline" id="cursor-outline"></div>
'''
text = text.replace(cursor_dom, '')

style_block = '''
    /* ─────────────────────────────────────────
       ADVANCED ANIMATIONS
    ───────────────────────────────────────── */
    @media (pointer: fine) {
      body, a, button, .project-card, .btn { cursor: none !important; }
      .cursor-dot {
        position: fixed; top: 0; left: 0; width: 8px; height: 8px;
        background: var(--acid); border-radius: 50%;
        pointer-events: none; z-index: 9999;
        transform: translate(-50%, -50%);
      }
      .cursor-outline {
        position: fixed; top: 0; left: 0; width: 40px; height: 40px;
        border: 1px solid rgba(202, 255, 0, 0.5); border-radius: 50%;
        pointer-events: none; z-index: 9998;
        transform: translate(-50%, -50%);
        transition: width 0.2s, height 0.2s, background 0.2s, border-color 0.2s;
      }
      .cursor-outline.hover {
        width: 80px; height: 80px; background: rgba(202, 255, 0, 0.1); border-color: transparent;
      }
    }

    .hero__badge { opacity: 0; transform: translateY(20px); animation: fadeUp 0.8s ease 0.2s forwards; }
    .hero__title .line { display: block; overflow: hidden; }
    .hero__title .line span { display: inline-block; transform: translateY(100%); opacity: 0; animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .hero__subtitle { opacity: 0; transform: translateY(20px); animation: fadeUp 1s ease 0.6s forwards; }
    .hero__actions { opacity: 0; transform: translateY(20px); animation: fadeUp 1s ease 0.8s forwards; }
    @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
    @keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }

    .project-card::before {
      content: ""; position: absolute; inset: -1px; border-radius: inherit;
      background: linear-gradient(45deg, transparent 40%, var(--acid) 50%, transparent 60%);
      background-size: 300% 300%;
      z-index: -1; opacity: 0; transition: opacity 0.3s;
    }
    .project-card:hover::before { opacity: 1; animation: shineBorder 2s infinite linear; }
    @keyframes shineBorder { 0% { background-position: 0% 50%; } 100% { background-position: 100% 50%; } }
'''
text = text.replace(style_block, '')

old_title = '''      <h1 class="hero__title" id="hero-title">
        Ship premium websites<br><span class="gradient-text">without the wait.</span>
      </h1>'''
new_title = '''      <h1 class="hero__title" id="hero-title">
        <span class="line"><span style="animation-delay: 0.3s">Ship premium websites</span></span>
        <span class="line"><span class="gradient-text" style="animation-delay: 0.4s">without the wait.</span></span>
      </h1>'''
text = text.replace(new_title, old_title)

js_block = '''
    // ── Custom Cursor & Hero Parallax
    (function() {
      const dot = document.getElementById('cursor-dot');
      const outline = document.getElementById('cursor-outline');
      const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      
      if (dot && outline && !prefersReducedMotion && window.matchMedia("(pointer: fine)").matches) {
        let mouseX = 0, mouseY = 0;
        let outlineX = 0, outlineY = 0;

        window.addEventListener('mousemove', e => {
          mouseX = e.clientX;
          mouseY = e.clientY;
          dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
        });

        function animateCursor() {
          outlineX += (mouseX - outlineX) * 0.15;
          outlineY += (mouseY - outlineY) * 0.15;
          outline.style.transform = `translate(${outlineX}px, ${outlineY}px) translate(-50%, -50%)`;
          requestAnimationFrame(animateCursor);
        }
        animateCursor();

        document.querySelectorAll('a, button, .project-card, .btn').forEach(el => {
          el.addEventListener('mouseenter', () => outline.classList.add('hover'));
          el.addEventListener('mouseleave', () => outline.classList.remove('hover'));
        });
      }

      // Parallax
      const heroGrid = document.querySelector('.hero__grid');
      const heroGlows = document.querySelectorAll('.hero .glow');
      if (!prefersReducedMotion) {
        window.addEventListener('mousemove', e => {
          const x = (e.clientX / window.innerWidth - 0.5) * 2;
          const y = (e.clientY / window.innerHeight - 0.5) * 2;
          if(heroGrid) heroGrid.style.transform = `translate(${x * -15}px, ${y * -15}px)`;
          heroGlows.forEach((glow, i) => {
            glow.style.transform = `translate(${x * (i%2===0 ? 30 : -30)}px, ${y * (i%2===0 ? 30 : -30)}px)`;
          });
        });
      }
    })();
'''
text = text.replace(js_block, '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Reverted successfully.")
