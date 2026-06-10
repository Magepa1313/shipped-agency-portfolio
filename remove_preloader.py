# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Preloader HTML
content = re.sub(r'<!-- PRELOADER -->.*?</div>\\s*</div>\\s*</div>', '', content, flags=re.DOTALL)

# 2. Update JS Logic to remove preloader logic and call initAnimations directly
js_logic_old = '''
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
'''

js_logic_new = '''
    // -- GSAP Animations
    gsap.registerPlugin(ScrollTrigger);
    
    document.addEventListener("DOMContentLoaded", () => {
      initAnimations();
    });

    function initAnimations() {
'''

content = content.replace(js_logic_old, js_logic_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
