import sys
import re

file_path = r'c:\Users\maxim\OneDrive\Desktop\landscaping\portfolio\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the CSS block appended at the end of <style>
if 'CUTE TYPOGRAPHY' in text:
    parts = text.split('/* ─────────────────────────────────────────\n       CUTE TYPOGRAPHY')
    rest = parts[1].split('</style>', 1)
    text = parts[0] + '\n  </style>' + rest[1]

# Revert the hero title
hero_pattern = re.compile(r'<h1 class="hero__title" id="hero-title".*?</h1>', re.DOTALL)
new_hero = '''<h1 class="hero__title" id="hero-title">
        Ship premium websites<br><span class="gradient-text">without the wait.</span>
      </h1>'''

text = hero_pattern.sub(new_hero, text, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed cute typography successfully.")
