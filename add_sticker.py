import sys
import re

file_path = r'c:\Users\maxim\OneDrive\Desktop\landscaping\portfolio\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# CSS to inject
css_to_add = '''
    /* ─────────────────────────────────────────
       CUTE TYPOGRAPHY
    ───────────────────────────────────────── */
    :root {
      --pink: rgba(255, 120, 200, 0.95);
      --blue: rgba(120, 210, 255, 0.95);
      --ink: rgba(255, 255, 255, 0.9);
    }

    .cute {
      position: relative;
      display: inline-block;
      margin: 0;
      font-weight: 900;
      letter-spacing: -0.04em;
      line-height: 0.92;
      font-size: clamp(2.2rem, 7.6vw, 5.6rem);
      color: rgba(255, 255, 255, 0.88);
      filter: drop-shadow(0 18px 54px rgba(0, 0, 0, 0.35));
    }

    .cute::before,
    .cute::after {
      content: attr(data-text);
      position: absolute;
      inset: 0;
      pointer-events: none;
      user-select: none;
    }

    @media (prefers-reduced-motion: reduce) {
      .cute::before,
      .cute::after {
        animation: none !important;
      }
    }

    .c-bubble { color: transparent; -webkit-text-stroke: 2px rgba(255, 255, 255, 0.35); }
    .c-bubble::before {
      color: transparent;
      background: radial-gradient(22px 14px at 22% 32%, rgba(255, 255, 255, 0.32) 0 60%, rgba(255, 255, 255, 0) 62%), radial-gradient(18px 12px at 62% 62%, rgba(255, 255, 255, 0.18) 0 60%, rgba(255, 255, 255, 0) 62%), radial-gradient(circle at 35% 35%, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0) 52%), linear-gradient(135deg, var(--pink), var(--blue));
      -webkit-background-clip: text; background-clip: text; filter: drop-shadow(0 0 18px rgba(255, 120, 200, 0.2));
    }
    .c-bubble::after {
      color: transparent;
      background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.7) 44%, rgba(255, 255, 255, 0) 58%);
      -webkit-background-clip: text; background-clip: text; mix-blend-mode: screen; opacity: 0.55; animation: sheen 1.9s ease-in-out infinite;
    }
    @keyframes sheen { 0%, 100% { transform: translateX(-12px) skewX(-8deg); opacity: 0.3; } 50% { transform: translateX(12px) skewX(-8deg); opacity: 0.7; } }

    .c-sprinkle { color: var(--ink); }
    .c-sprinkle::before {
      color: transparent;
      background: radial-gradient(120px 60px at 35% 45%, rgba(255, 120, 200, 0.55), rgba(255, 120, 200, 0) 70%), radial-gradient(120px 60px at 65% 55%, rgba(120, 210, 255, 0.55), rgba(120, 210, 255, 0) 70%);
      -webkit-background-clip: text; background-clip: text; filter: blur(10px); opacity: 0.75; transform: translate(0, 6px);
    }
    .c-sprinkle::after {
      color: transparent;
      background: radial-gradient(2px 2px at 12% 30%, rgba(255, 255, 255, 0.85) 0 60%, rgba(255, 255, 255, 0) 62%), radial-gradient(2px 2px at 22% 60%, rgba(255, 255, 255, 0.7) 0 60%, rgba(255, 255, 255, 0) 62%), radial-gradient(2px 2px at 38% 42%, rgba(255, 255, 255, 0.78) 0 60%, rgba(255, 255, 255, 0) 62%), radial-gradient(2px 2px at 58% 28%, rgba(255, 255, 255, 0.78) 0 60%, rgba(255, 255, 255, 0) 62%), radial-gradient(2px 2px at 74% 58%, rgba(255, 255, 255, 0.7) 0 60%, rgba(255, 255, 255, 0) 62%), radial-gradient(2px 2px at 86% 40%, rgba(255, 255, 255, 0.85) 0 60%, rgba(255, 255, 255, 0) 62%), linear-gradient(135deg, rgba(255, 120, 200, 0.75), rgba(120, 210, 255, 0.75));
      -webkit-background-clip: text; background-clip: text; opacity: 0.92; animation: sprMove 3.2s ease-in-out infinite;
    }
    @keyframes sprMove { 0%, 100% { background-position: 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; } 50% { background-position: 10px -6px, -10px 8px, 8px 10px, -8px -10px, 12px 6px, -12px -6px, 0 0; } }

    .c-sticker { color: rgba(255, 255, 255, 0.92); text-shadow: 0 10px 30px rgba(0, 0, 0, 0.35); }
    .c-sticker::before {
      color: transparent; background: linear-gradient(135deg, rgba(255, 120, 200, 0.55), rgba(120, 210, 255, 0.55));
      -webkit-background-clip: text; background-clip: text; transform: translate(10px, 10px); filter: blur(10px); opacity: 0.65;
    }
    .c-sticker::after {
      color: transparent; -webkit-text-stroke: 3px rgba(255, 255, 255, 0.7);
      text-shadow: 0 0 18px rgba(255, 255, 255, 0.14); filter: drop-shadow(0 0 10px rgba(255, 120, 200, 0.2)); opacity: 0.95;
    }

    .c-candy { color: transparent; -webkit-text-stroke: 2px rgba(255, 255, 255, 0.26); }
    .c-candy::before {
      color: transparent; background: linear-gradient(90deg, rgba(255, 120, 200, 0.95), rgba(255, 180, 230, 0.95), rgba(120, 210, 255, 0.95), rgba(170, 235, 255, 0.95), rgba(255, 120, 200, 0.95));
      background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; animation: candyFlow 2.6s linear infinite; filter: drop-shadow(0 0 20px rgba(120, 210, 255, 0.18));
    }
    @keyframes candyFlow { to { background-position: 220% 0; } }
    .c-candy::after {
      color: rgba(255, 255, 255, 0.85); clip-path: polygon(0 0, 100% 0, 100% 56%, 0 44%); filter: blur(0.25px); opacity: 0.35; transform: translate(0, -2px);
    }

    .c-heart { color: rgba(255, 255, 255, 0.9); }
    .c-heart::before {
      color: transparent; background: linear-gradient(90deg, var(--pink) 0 50%, var(--blue) 50% 100%);
      -webkit-background-clip: text; background-clip: text; mix-blend-mode: screen; opacity: 0.95; transform: translate(0, 1px);
    }
    .c-heart::after {
      color: transparent; background: radial-gradient(140px 70px at 35% 55%, rgba(255, 120, 200, 0.6), rgba(255, 120, 200, 0) 70%), radial-gradient(140px 70px at 65% 45%, rgba(120, 210, 255, 0.6), rgba(120, 210, 255, 0) 70%);
      -webkit-background-clip: text; background-clip: text; filter: blur(12px); opacity: 0.7; animation: pulse 1.8s ease-in-out infinite;
    }
    @keyframes pulse { 0%, 100% { transform: translate(0, 8px) scale(1); opacity: 0.55; } 50% { transform: translate(0, 8px) scale(1.06); opacity: 0.85; } }
'''

if 'CUTE TYPOGRAPHY' not in text:
    text = text.replace('</style>', f'{css_to_add}\n  </style>')

old_hero_pattern = re.compile(r'<h1 class="hero__title" id="hero-title">.*?</h1>', re.DOTALL)
new_hero = '''<h1 class="hero__title" id="hero-title" style="display:flex; flex-direction:column; align-items:center; gap:0.2em;">
        <span class="cute c-sticker" data-text="Ship premium websites">Ship premium websites</span>
        <span class="cute c-sticker" data-text="without the wait.">without the wait.</span>
      </h1>'''

text = old_hero_pattern.sub(new_hero, text, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Injected sticker aesthetics successfully.")
