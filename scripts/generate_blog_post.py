#!/usr/bin/env python3
"""
Auto Blog Post Generator for maximiliankuerner.at
Generates SEO-optimized blog posts in Maxi's voice using Claude API.
Runs weekly via GitHub Actions.
"""

import os
import json
import re
from datetime import datetime
import anthropic

# ─── Paths ────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_FILE = os.path.join(ROOT, "scripts", "topics.json")
POSTS_DIR = os.path.join(ROOT, "posts")
BLOG_HTML = os.path.join(ROOT, "blog.html")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
BASE_URL = "https://portfolio-silk-rho-95.vercel.app"
AUTHOR = "Maximilian Kürner"

# ─── Pick topic via angle system ──────────────────────────────────────────────
def pick_topic():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    angle = data["angles"][data["angle_index"] % len(data["angles"])]
    category = data["categories"][data["category_index"] % len(data["categories"])]
    used = data["used_topics"]

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""Du generierst einen Blog-Post-Topic für maximiliankuerner.at.
Zielgruppe: lokale österreichische Unternehmen (KMU) die eine bessere Website wollen.
Autor: Maximilian Kürner, 17 Jahre, Webdesign Freelancer, Wels Oberösterreich.

Winkel: {angle['name']}
Winkel-Anweisung: {angle['instruction']}
Kategorie: {category}
Bereits verwendete Slugs — NICHT wiederholen: {json.dumps(used, ensure_ascii=False)}

Gib exakt dieses JSON zurück — kein anderer Text, kein Markdown, keine Erklärung:
{{
  "hook": "Prägnanter Titel (7-12 Wörter, Deutsch, Du-Form, konkret — enthält eine Zahl oder spezifisches Versprechen)",
  "slug": "url-slug-auf-deutsch-mit-bindestrichen-maximal-6-woerter",
  "keyword": "Haupt-SEO-Keyword Österreich (2-4 Wörter, lokaler Bezug wenn möglich)",
  "meta_description": "150-160 Zeichen: Problem + Lösungshinweis + Nutzen. Österreichischer Kontext. Keine Anführungszeichen.",
  "excerpt": "1 Satz Teaser für die Blog-Übersicht, max 120 Zeichen, enthält eine konkrete Zahl oder Überraschung",
  "toc_headings": ["H2 Überschrift 1", "H2 Überschrift 2", "H2 Überschrift 3", "H2 Überschrift 4"]
}}"""

    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = msg.content[0].text.strip()
    raw = re.sub(r'^```[a-z]*\n?', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'\n?```$', '', raw, flags=re.MULTILINE)
    topic = json.loads(raw.strip())

    topic["tag"] = category
    topic["angle_instruction"] = angle["instruction"]
    topic["angle_name"] = angle["name"]

    data["angle_index"] += 1
    data["category_index"] += 1
    data["used_topics"].append(topic["slug"])

    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return topic

# ─── Generate post content ────────────────────────────────────────────────────
def generate_post(topic):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    today = datetime.now().strftime("%d. %B %Y").replace(
        "January","Jänner").replace("February","Februar").replace(
        "March","März").replace("April","April").replace(
        "May","Mai").replace("June","Juni").replace(
        "July","Juli").replace("August","August").replace(
        "September","September").replace("October","Oktober").replace(
        "November","November").replace("December","Dezember")

    system = """Du bist Maximilian Kürner — 17 Jahre alt, Webdesign Freelancer aus Wels, Österreich.
Du schreibst Blog-Posts für lokale österreichische KMU die eine bessere Website wollen.

STIMME & STIL:
- Direkt, kein Bullshit, kein Corporate-Speak
- Du-Form (informell) durchgehend
- Kurze Sätze und Absätze (max 3 Sätze pro Absatz)
- Konkret: echte Zahlen, österreichischer Kontext (Wien, Graz, Linz, Wels wo passend)
- Klingt wie ein smarter Freund der sich auskennt — nicht wie ein Unternehmensberater
- Kein Keyword-Stuffing — natürlicher Lesefluss hat immer Vorrang

INHALT-FRAMEWORK (Alex Hormozi / PAS):
1. HOOK (erster Absatz): Öffne mit einem spezifischen Schmerz oder einer überraschenden Zahl
2. AGITATE: Mach die Konsequenz des Nichts-Tuns in Euro oder konkreten Verlusten greifbar
3. [INLINE_CTA_1] — nach etwa 35% des Artikels
4. LÖSUNG: Klar und spezifisch — was ändert sich und warum funktioniert das?
5. BEWEIS/LOGIK: Erkläre warum — Mechanismus, Logik, keine erfundenen Testimonials
6. [INLINE_CTA_2] — nach etwa 65% des Artikels
7. TAKEAWAY: Konkrete nächste Schritte für den Leser

LÄNGE & STRUKTUR:
- Ziel: 1.500-2.000 Wörter (nicht weniger — kurze Posts ranken nicht)
- Genau ein H1 (der Titel — nicht im Inhalt wiederholen)
- 4-5 H2-Überschriften, ungefähr alle 250-300 Wörter eine neue
- H3-Überschriften für Unterpunkte wenn sinnvoll
- Ziel-Keyword natürlich im ersten Absatz, in mind. 2 H2-Überschriften, und 0.5-1.5% Dichte gesamt
- Keyword-Dichte: ~1% — bei 1.500 Wörtern also ~15 Mal das Keyword oder enge Varianten
- Eine highlight-Box mit der zentralen Erkenntnis des Posts

INLINE CTAs:
Platziere an den markierten Stellen [INLINE_CTA_1] und [INLINE_CTA_2] exakt diesen HTML-Block:
<div class="inline-cta">
  <p>Kurzer überzeugender Satz der zum CTA passt (1 Satz, bezieht sich auf aktuellen Abschnitt).</p>
  <a class="btn btn-acid" href="../index.html#contact">Kostenlos anfragen →</a>
</div>

FORMATIERUNG — gibt NUR reinen Artikel-Inhalt zurück:
Erlaubte Tags: <p>, <h2>, <h3>, <ul>, <li>, <strong>, <div class="highlight"><p>...</p></div>, <div class="inline-cta">...</div>
KEINE anderen Tags. KEINE Klassen außer highlight und inline-cta.
KEIN h1-Tag im Inhalt — der Titel wird separat gerendert."""

    user = f"""Schreib den vollständigen Blog-Post:

Titel: {topic['hook']}
Ziel-Keyword: {topic['keyword']}
Kategorie: {topic['tag']}
Hormozi-Winkel: {topic['angle_name']}
Winkel-Anweisung: {topic['angle_instruction']}
H2-Struktur (verwende diese oder ähnliche): {', '.join(topic.get('toc_headings', []))}
Datum: {today}

Platziere [INLINE_CTA_1] nach dem zweiten H2 und [INLINE_CTA_2] nach dem vierten H2.
Gib NUR den Artikel-Inhalt zurück — reines HTML wie beschrieben. Mindestens 1.500 Wörter."""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4000,
        system=system,
        messages=[{"role": "user", "content": user}]
    )

    return message.content[0].text.strip()

# ─── Build table of contents HTML ────────────────────────────────────────────
def build_toc(headings):
    if not headings:
        return ""
    items = "".join(
        f'<li><a href="#{re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-")}">{h}</a></li>'
        for h in headings
    )
    return f'<nav class="toc"><p class="toc-label">Inhalt</p><ul>{items}</ul></nav>'

# ─── Add id anchors to H2 tags in content ─────────────────────────────────────
def add_heading_ids(content):
    def replace_h2(m):
        text = re.sub(r'<[^>]+>', '', m.group(1))
        anchor = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
        return f'<h2 id="{anchor}">{m.group(1)}</h2>'
    return re.sub(r'<h2>(.*?)</h2>', replace_h2, content)

# ─── Build HTML file ──────────────────────────────────────────────────────────
def build_post_html(topic, content, date_str, date_iso):
    slug = topic["slug"]
    title = topic["hook"]
    tag = topic["tag"]
    keyword = topic["keyword"]
    meta_desc = topic.get("meta_description", f"{title}. Von Maximilian Kürner, Webdesign Freelancer aus Wels, Österreich.")
    url = f"{BASE_URL}/posts/{slug}.html"

    content = add_heading_ids(content)
    toc_html = build_toc(topic.get("toc_headings", []))

    word_count = len(re.sub(r'<[^>]+>', '', content).split())
    read_time = max(3, round(word_count / 200))

    # Escape quotes in meta fields for JSON-LD
    title_esc = title.replace('"', '\\"')
    meta_esc = meta_desc.replace('"', '\\"')

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — {AUTHOR}</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="article:published_time" content="{date_iso}" />
  <meta property="article:author" content="{AUTHOR}" />
  <script type="application/ld+json">
  [
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{title_esc}",
      "description": "{meta_esc}",
      "author": {{
        "@type": "Person",
        "name": "{AUTHOR}",
        "url": "{BASE_URL}"
      }},
      "publisher": {{
        "@type": "Person",
        "name": "{AUTHOR}",
        "url": "{BASE_URL}"
      }},
      "datePublished": "{date_iso}",
      "dateModified": "{date_iso}",
      "url": "{url}",
      "inLanguage": "de-AT",
      "keywords": "{keyword}"
    }},
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE_URL}/index.html"}},
        {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "{BASE_URL}/blog.html"}},
        {{"@type": "ListItem", "position": 3, "name": "{title_esc}", "item": "{url}"}}
      ]
    }}
  ]
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;700;800&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #06070c; --acid: #c8ff00; --text: #f0f0f0;
      --muted: rgba(240,240,240,.42); --bord: rgba(255,255,255,.08);
      --surf: rgba(255,255,255,.04); --font: 'Bricolage Grotesque', system-ui, sans-serif;
      --tr: 0.22s cubic-bezier(.4,0,.2,1);
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{ background: var(--bg); color: var(--text); font-family: var(--font); line-height: 1.65; overflow-x: hidden; -webkit-font-smoothing: antialiased; }}
    a {{ color: inherit; text-decoration: none; }}
    ul {{ list-style: none; }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 24px; }}
    .wrap-narrow {{ max-width: 700px; margin: 0 auto; padding: 0 24px; }}
    .btn {{ display: inline-flex; align-items: center; gap: 8px; padding: 13px 26px; border-radius: 100px; font-family: var(--font); font-size: .9rem; font-weight: 700; cursor: pointer; transition: transform var(--tr), box-shadow var(--tr); border: none; }}
    .btn-acid {{ background: var(--acid); color: #06070c; border: 1px solid rgba(200,255,0,.6); box-shadow: 0 4px 22px rgba(200,255,0,.32); }}
    .btn-acid:hover {{ transform: translateY(-2px); box-shadow: 0 8px 32px rgba(200,255,0,.48); }}
    .nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 100; padding: 20px 0; background: rgba(6,7,12,.82); backdrop-filter: blur(24px); border-bottom: 1px solid var(--bord); }}
    .nav-inner {{ display: flex; align-items: center; justify-content: space-between; }}
    .nav-logo {{ display: flex; align-items: center; gap: 11px; }}
    .nav-logo-name {{ display: flex; flex-direction: column; line-height: 1.15; }}
    .nav-logo-name .ln1 {{ font-size: .7rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }}
    .nav-logo-name .ln2 {{ font-size: 1rem; font-weight: 800; letter-spacing: -.02em; }}
    .nav-mark {{ width: 40px; height: 40px; background: var(--acid); border-radius: 10px; display: grid; place-items: center; flex-shrink: 0; }}
    .nav-mark svg {{ width: 22px; height: 15px; }}
    .nav-links {{ display: flex; gap: 28px; }}
    .nav-link {{ font-size: .875rem; font-weight: 600; color: var(--muted); transition: color var(--tr); }}
    .nav-link:hover {{ color: var(--text); }}
    .post-header {{ padding: 140px 24px 60px; text-align: center; }}
    .post-tag {{ display: inline-block; font-size: .72rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--acid); margin-bottom: 20px; }}
    .post-title {{ font-size: clamp(1.9rem,5vw,3.6rem); font-weight: 800; letter-spacing: -.04em; line-height: 1.08; max-width: 800px; margin: 0 auto 20px; }}
    .post-meta {{ display: flex; align-items: center; justify-content: center; gap: 16px; font-size: .82rem; color: var(--muted); }}
    .toc {{ background: rgba(255,255,255,.03); border: 1px solid var(--bord); border-radius: 14px; padding: 22px 26px; margin-bottom: 48px; }}
    .toc-label {{ font-size: .72rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--acid); margin-bottom: 12px; }}
    .toc ul {{ padding-left: 0; display: flex; flex-direction: column; gap: 8px; }}
    .toc li {{ list-style: none; }}
    .toc a {{ font-size: .92rem; color: var(--muted); transition: color var(--tr); }}
    .toc a:hover {{ color: var(--text); }}
    .post-body {{ padding: 60px 0 100px; }}
    .post-body p {{ font-size: 1.05rem; color: rgba(240,240,240,.82); line-height: 1.8; margin-bottom: 24px; }}
    .post-body h2 {{ font-size: 1.5rem; font-weight: 800; letter-spacing: -.03em; margin: 52px 0 16px; }}
    .post-body h3 {{ font-size: 1.15rem; font-weight: 800; letter-spacing: -.02em; margin: 32px 0 12px; color: var(--acid); }}
    .post-body ul {{ padding-left: 20px; margin-bottom: 24px; }}
    .post-body li {{ font-size: 1.05rem; color: rgba(240,240,240,.82); line-height: 1.8; margin-bottom: 8px; list-style: disc; }}
    .post-body strong {{ color: var(--text); font-weight: 800; }}
    .post-body .highlight {{ background: rgba(200,255,0,.07); border-left: 3px solid var(--acid); padding: 20px 24px; border-radius: 0 12px 12px 0; margin: 32px 0; }}
    .post-body .highlight p {{ margin-bottom: 0; color: var(--text); }}
    .inline-cta {{ border-radius: 16px; border: 1px solid rgba(200,255,0,.18); background: rgba(200,255,0,.04); padding: 24px 28px; display: flex; align-items: center; justify-content: space-between; gap: 20px; margin: 40px 0; flex-wrap: wrap; }}
    .inline-cta p {{ margin: 0; font-size: 1rem; color: var(--text); font-weight: 600; flex: 1; }}
    .post-cta {{ border-radius: 20px; border: 1px solid rgba(200,255,0,.2); background: rgba(200,255,0,.04); padding: 48px 40px; text-align: center; margin: 60px 0; }}
    .post-cta h3 {{ font-size: 1.6rem; font-weight: 800; letter-spacing: -.03em; margin-bottom: 12px; }}
    .post-cta p {{ color: var(--muted); margin-bottom: 28px; font-size: 1.05rem; }}
    .back-link {{ display: inline-flex; align-items: center; gap: 8px; font-size: .875rem; font-weight: 700; color: var(--muted); transition: color var(--tr); margin-bottom: 60px; }}
    .back-link:hover {{ color: var(--text); }}
    footer {{ border-top: 1px solid var(--bord); padding: 28px 0; }}
    .ft {{ display: flex; align-items: center; justify-content: space-between; font-size: .82rem; color: var(--muted); }}
    @media (max-width: 600px) {{
      .nav-links {{ display: none; }}
      .inline-cta {{ flex-direction: column; text-align: center; }}
    }}
  </style>
</head>
<body>
  <nav class="nav">
    <div class="wrap">
      <div class="nav-inner">
        <a class="nav-logo" href="../index.html">
          <div class="nav-mark">
            <svg viewBox="0 0 22 15" fill="none" stroke="#06070c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1,14 1,1 5.5,8 10,1 10,14" />
              <line x1="13" y1="1" x2="13" y2="14" />
              <line x1="13" y1="7.5" x2="21" y2="1" />
              <line x1="13" y1="7.5" x2="21" y2="14" />
            </svg>
          </div>
          <div class="nav-logo-name">
            <span class="ln1">Webdesign Freelance</span>
            <span class="ln2">Maximilian Kürner</span>
          </div>
        </a>
        <ul class="nav-links">
          <li><a class="nav-link" href="../index.html#results">Ergebnisse</a></li>
          <li><a class="nav-link" href="../index.html#about">Über mich</a></li>
          <li><a class="nav-link" href="../blog.html">Blog</a></li>
          <li><a class="nav-link" href="../index.html#contact">Kontakt</a></li>
        </ul>
        <a class="btn btn-acid" href="../index.html#contact" style="padding:10px 20px;font-size:.82rem;">Projekt starten →</a>
      </div>
    </div>
  </nav>

  <div class="post-header">
    <div class="post-tag">{tag}</div>
    <h1 class="post-title">{title}</h1>
    <div class="post-meta">
      <span>{date_str}</span>
      <span>·</span>
      <span>{read_time} min Lesezeit</span>
    </div>
  </div>

  <div class="post-body">
    <div class="wrap-narrow">
      <a class="back-link" href="../blog.html">← Zurück zum Blog</a>

      {toc_html}

      {content}

      <div class="post-cta">
        <h3>Deine Website hat dieses Problem?</h3>
        <p>Ich schau sie mir kostenlos an und sag dir direkt was nicht stimmt — in 15 Minuten. Kein Pitch, kein Bullshit.</p>
        <a class="btn btn-acid" href="../index.html#contact">Kostenloses Gespräch →</a>
      </div>

      <a class="back-link" href="../blog.html">← Zurück zum Blog</a>
    </div>
  </div>

  <footer>
    <div class="wrap ft">
      <div>Shipped. — {AUTHOR}</div>
      <div>© {datetime.now().year} {AUTHOR}</div>
    </div>
  </footer>
</body>
</html>"""

# ─── Update blog.html ─────────────────────────────────────────────────────────
def update_blog_html(topic, date_str):
    with open(BLOG_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    excerpt = topic.get("excerpt", topic["hook"])
    word_count_estimate = 1700
    read_time = max(3, round(word_count_estimate / 200))

    new_card = f"""
      <a class="blog-card" href="posts/{topic['slug']}.html">
        <div class="blog-tag">{topic['tag']}</div>
        <h2 class="blog-title">{topic['hook']}</h2>
        <p class="blog-excerpt">{excerpt}</p>
        <div class="blog-foot">
          <span class="blog-date">{date_str}</span>
          <span class="blog-read">{read_time} min →</span>
        </div>
      </a>
"""

    html = html.replace(
        '<div class="blog-grid">',
        f'<div class="blog-grid">{new_card}',
        1
    )

    with open(BLOG_HTML, "w", encoding="utf-8") as f:
        f.write(html)

# ─── Update sitemap.xml ───────────────────────────────────────────────────────
def update_sitemap(topic, date_iso):
    with open(SITEMAP, "r", encoding="utf-8") as f:
        xml = f.read()

    new_entry = f"""  <url>
    <loc>{BASE_URL}/posts/{topic['slug']}.html</loc>
    <lastmod>{date_iso}</lastmod>
    <priority>0.7</priority>
  </url>
</urlset>"""

    xml = xml.replace("</urlset>", new_entry)

    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(xml)

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    now = datetime.now()
    date_iso = now.strftime("%Y-%m-%d")
    months = ["Jänner","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
    date_str = f"{now.day}. {months[now.month - 1]} {now.year}"

    print("Generating topic from angle system...")
    topic = pick_topic()
    print(f"Angle: {topic['angle_name']} | Category: {topic['tag']}")
    print(f"Topic: {topic['hook']}")
    print(f"Keyword: {topic['keyword']}")

    print("Generating content (~1500-2000 words)...")
    content = generate_post(topic)

    word_count = len(re.sub(r'<[^>]+>', '', content).split())
    print(f"Word count: {word_count}")

    print("Building HTML...")
    post_html = build_post_html(topic, content, date_str, date_iso)

    post_path = os.path.join(POSTS_DIR, f"{topic['slug']}.html")
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(post_html)
    print(f"Written: {post_path}")

    print("Updating blog.html...")
    update_blog_html(topic, date_str)

    print("Updating sitemap.xml...")
    update_sitemap(topic, date_iso)

    print(f"Done. Post: {topic['slug']}")

if __name__ == "__main__":
    main()
