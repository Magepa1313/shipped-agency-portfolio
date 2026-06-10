# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\\n  <script src="spectra.js"></script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
