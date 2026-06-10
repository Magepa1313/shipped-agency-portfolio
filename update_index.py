# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Title and Meta
content = re.sub(r'<title>.*?</title>', '<title>Maximilian Kürner — Antigravity Optimierung</title>', content)
content = re.sub(r'<meta name="description".*?/>', '<meta name="description" content="Website-Verbesserung und Optimierung mit Antigravity." />', content)
content = re.sub(r'<meta property="og:title".*?/>', '<meta property="og:title" content="Maximilian Kürner — Antigravity Optimierung" />', content)
content = re.sub(r'<meta property="og:description".*?/>', '<meta property="og:description" content="Website-Verbesserung und Optimierung mit Antigravity." />', content)

# 2. Nav
content = content.replace('Shipped.', 'M. Kürner')
content = content.replace('>Home<', '>Start<')
content = content.replace('>About<', '>Antigravity<')
content = content.replace('>Projects<', '>Prozess<')
content = content.replace('>Contact<', '>Kontakt<')
content = content.replace("Let's Talk", "Kostenlose Analyse")
content = content.replace("Let's Work Together →", "Jetzt Starten →")

# 3. Hero
content = content.replace('<canvas id="particle-canvas" aria-hidden="true"></canvas>', '<canvas id="spectra-canvas" aria-hidden="true" style="position:absolute; inset:0; z-index:0; width:100%; height:100%;"></canvas>')
content = content.replace('Available for new projects', 'Kapazitäten für Website-Analysen verfügbar')
content = content.replace('Ship premium websites<br><span class="gradient-text">without the wait.</span>', 'Ihre Website.<br><span class="gradient-text">Nur messbar besser.</span>')
content = content.replace('I turn your brand into a high-converting, blazing-fast website instantly, saving you thousands in lost revenue.', 'Ich bin Maximilian Kürner. Mit der Antigravity-Methode analysiere, optimiere und skaliere ich Ihre digitale Präsenz — für mehr Speed und maximale Conversion.')
content = content.replace('See My Work', 'Kostenlose Analyse anfordern')
content = content.replace('Get in Touch', 'Wie es funktioniert')

# 4. Impact Scene
content = content.replace('Stop wasting money<br><span class="gradient-text">on bad websites.</span>', 'Heben Sie die Schwerkraft<br><span class="gradient-text">Ihrer Website auf.</span>')
content = content.replace("A pretty design doesn't matter if it's slow and doesn't convert. We build high-performance, premium websites that turn your traffic into revenue.", 'Ein hübsches Design bringt nichts, wenn es langsam lädt und keine Anfragen generiert. Mit Antigravity lösen wir diese Bremsen – datenbasiert und extrem performant.')

# 5. Ticker
content = re.sub(r'<div class="ticker__track">.*?</div>', '''<div class="ticker__track">
        <span class="ticker__item"><span class="dot">✦</span> Antigravity Performance</span>
        <span class="ticker__item"><span class="dot">✦</span> Conversion Boost</span>
        <span class="ticker__item"><span class="dot">✦</span> Ladezeit Minimierung</span>
        <span class="ticker__item"><span class="dot">✦</span> UI / UX Audit</span>
        <span class="ticker__item"><span class="dot">✦</span> Messbare Resultate</span>
        <span class="ticker__item"><span class="dot">✦</span> SEO Optimierung</span>
        <span class="ticker__item"><span class="dot">✦</span> Lead Generation</span>
        <span class="ticker__item"><span class="dot">✦</span> Antigravity Performance</span>
        <span class="ticker__item"><span class="dot">✦</span> Conversion Boost</span>
        <span class="ticker__item"><span class="dot">✦</span> Ladezeit Minimierung</span>
        <span class="ticker__item"><span class="dot">✦</span> UI / UX Audit</span>
        <span class="ticker__item"><span class="dot">✦</span> Messbare Resultate</span>
        <span class="ticker__item"><span class="dot">✦</span> SEO Optimierung</span>
        <span class="ticker__item"><span class="dot">✦</span> Lead Generation</span>
      </div>''', content, flags=re.DOTALL)

# 6. About
content = content.replace('Open to<br>Remote Work 🌍', 'Fokus auf<br>Messergebnisse 📊')
content = content.replace('// About Me', '// Die Methode')
content = content.replace('Launch your website in<br>1/5th the time.', 'Optimierung statt<br>Neuerfindung.')
content = content.replace('Stop waiting months. Your vision turns into a clean, professional, and lightning-fast website in days, not weeks.', 'Eine komplett neue Website dauert Monate. Eine intelligente Optimierung bringt Resultate in Tagen.')
content = content.replace('With a background spanning web development and UI/UX magic, I bring websites from concept to launch with uncompromising speed and precision. No bloated templates—just pure performance.', 'Mit der Antigravity-Methode analysiere ich bestehende Engpässe in Ihrem Code und Design. Statt pauschaler Templates implementiere ich zielgenaue Hebel, die Ihre Performance und Conversion-Rate drastisch erhöhen.')

# 7. Stats
content = content.replace('40+', '100')
content = content.replace('Websites Launched', 'PageSpeed Fokus')
content = content.replace('3+', '0')
content = content.replace('Years Designing', 'Kompromisse')
content = content.replace('100%', '100')
content = content.replace('Client Satisfaction', 'Datenbasiert')
content = content.replace('Turnaround', 'Erstanalyse')

# 8. Impact / Results text
content = content.replace('// The Impact', '// Der Vorher-Nachher Effekt')
content = content.replace('Stop losing leads to<br>ugly, slow websites.', 'Warum Performance<br>Umsatz bedeutet.')
content = content.replace("A pretty website doesn't matter if it doesn't load fast or convert. We transform outdated platforms into high-speed lead generation engines.", 'Sekundenbruchteile entscheiden über Absprung oder Anfrage. Durch technische Exzellenz machen wir Ihre Website zum stärksten Vertriebler.')
content = content.replace('Before Shipped.', 'Vor der Optimierung')
content = content.replace('After Shipped.', 'Nach Antigravity')

# 9. Skills / What I Bring -> Expertise
content = content.replace('// What I Bring', '// Meine Expertise')
content = content.replace('A performance mindset<br>meets sharp web design.', 'Technische Exzellenz<br>für messbaren Erfolg.')
content = content.replace('I cover the entire website surface — from technical SEO to pixel-perfect UI — so nothing gets lost in translation.', 'Der Antigravity-Ansatz ist ganzheitlich: Vom technischen Fundament bis zur Nutzerpsychologie wird alles auf Performance getrimmt.')

content = content.replace('Frontend Engineering', 'Performance Audits')
content = content.replace('React, Next.js, TypeScript — performant, accessible, and maintainable UIs that users actually enjoy.', 'Tiefgehende Analyse von Ladezeiten, Core Web Vitals und Code-Qualität. Identifikation aller technischen Bremsen.')
content = content.replace('↑ Core Strength', '↑ Priorität 1')

content = content.replace('CMS & Integrations', 'Conversion-Optimierung')
content = content.replace('WordPress, Webflow, Shopify. I connect your website to your favorite tools and CRMs effortlessly.', 'Datengetriebene UX-Anpassungen, die Besucher in qualifizierte Leads verwandeln. Kein Raten, nur Testen.')

content = content.replace('UI / UX Design', 'Technisches SEO')
content = content.replace('Figma-native. I translate brand requirements into clean web systems with obsessive visual hierarchy.', 'Sichtbarkeit ist alles. Ich optimiere Ihre Struktur, damit Google Ihre Seite liebt und besser rankt.')

content = content.replace('SEO & Speed', 'Code-Refactoring')
content = content.replace('Technical SEO, Core Web Vitals, dynamic caching. I make your website rank higher and load instantly.', 'Befreiung von altem, langsamem Code. Implementierung moderner Web-Technologien für blitzschnelles Laden.')

# 10. Projects -> Prozess (Bypassing PoC)
content = content.replace('// Selected Work', '// Der Antigravity-Prozess')
content = content.replace('Websites that<br>convert and grow.', 'In 4 Schritten<br>zur maximalen Performance.')
content = content.replace("A curated selection of websites I've designed and built — each one solving a real business problem with clean execution.", 'Ein klar strukturierter Ablauf, der sicherstellt, dass wir genau die Hebel finden, die Ihre Website zurückhalten.')

process_html = '''
          <article class="project-card reveal" tabindex="0">
            <div class="project-card__body" style="padding-top: 40px;">
              <span class="project-card__thumb-tag" style="position:relative; top:0; right:0; margin-bottom:20px; display:inline-block; background:var(--acid-dim); border:1px solid var(--acid);">Schritt 1</span>
              <h3 class="project-card__title">Die kostenlose Erstanalyse</h3>
              <p class="project-card__desc">In einem ersten Audit prüfe ich Ihre aktuelle Website auf die offensichtlichsten Performance- und Conversion-Killer. Kostenlos und unverbindlich.</p>
            </div>
          </article>
          <article class="project-card reveal" tabindex="0">
            <div class="project-card__body" style="padding-top: 40px;">
              <span class="project-card__thumb-tag" style="position:relative; top:0; right:0; margin-bottom:20px; display:inline-block; background:var(--acid-dim); border:1px solid var(--acid);">Schritt 2</span>
              <h3 class="project-card__title">Der Antigravity-Plan</h3>
              <p class="project-card__desc">Sie erhalten eine präzise Roadmap. Keine Pauschallösungen, sondern exakt die Maßnahmen, die den größten Impact auf Ihren Umsatz haben.</p>
            </div>
          </article>
          <article class="project-card reveal" tabindex="0">
            <div class="project-card__body" style="padding-top: 40px;">
              <span class="project-card__thumb-tag" style="position:relative; top:0; right:0; margin-bottom:20px; display:inline-block; background:var(--acid-dim); border:1px solid var(--acid);">Schritt 3</span>
              <h3 class="project-card__title">Technische Umsetzung</h3>
              <p class="project-card__desc">Ich setze die Optimierungen chirurgisch um. Besserer Code, schnellere Ladezeiten, überzeugendes UX-Design. Ohne dass Ihre Seite offline geht.</p>
            </div>
          </article>
'''
content = re.sub(r'<div class="projects-grid">.*?</div>\s*</section>', f'<div class="projects-grid">{process_html}</div>\n    </section>', content, flags=re.DOTALL)

# 11. Process -> Remove
content = re.sub(r'<!-- ═══════════════════════════════════════ PROCESS -->.*?</section>', '', content, flags=re.DOTALL)

# 12. CTA
content = content.replace('Ready to start<br><span>building?</span>', 'Bereit für den<br><span>nächsten Level?</span>')
content = content.replace("I currently have availability for Q3. Let's discuss your project and see if we're a good fit.", 'Lassen Sie uns herausfinden, wie viel Potenzial in Ihrer Website schlummert. Fordern Sie jetzt Ihre kostenlose Erstanalyse an.')
content = content.replace('Book a Discovery Call', 'Analyse anfordern')

# 13. Footer
content = content.replace('Shipped. is an independent web agency focused on high-performance digital products that scale.', 'Antigravity Optimierung. Unabhängige Beratung für messbar bessere Performance und Conversion.')
content = content.replace('Social', 'Kontakt')
content = content.replace('E-Commerce Store', 'Performance Audit')
content = content.replace('Local Business Site', 'UX/UI Check')
content = content.replace('Corporate Vision', 'SEO Optimierung')

# Fix double 100% bug from stats replacement
content = content.replace('id="stat-sat">100', 'id="stat-sat">100%')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
