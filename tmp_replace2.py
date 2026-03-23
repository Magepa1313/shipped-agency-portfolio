import sys

file_path = r'c:\Users\maxim\OneDrive\Desktop\landscaping\portfolio\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Only replace in the project body of the Lead Gen card 
import re

pattern = re.compile(
    r'<div class="project-card__body">.*?</article>', 
    re.DOTALL
)

def replacer(match):
    block = match.group(0)
    if 'Local Business Redesign' in block:
        block = block.replace('<span class="stack-pill">Python</span>', '<span class="stack-pill">WordPress</span>')
        block = block.replace('<span class="stack-pill">Apify</span>', '<span class="stack-pill">SEO</span>')
        block = block.replace('<span class="stack-pill">Gemini API</span>', '<span class="stack-pill">Copywriting</span>')
        block = block.replace('<span class="stack-pill">HTML/CSS</span>', '<span class="stack-pill">Figma</span>')
    return block

text = pattern.sub(replacer, text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Done stack pills')
