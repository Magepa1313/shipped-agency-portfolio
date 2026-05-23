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

# ─── Pick next topic ──────────────────────────────────────────────────────────
def pick_topic():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    queue = [t for t in data["queue"] if t["slug"] not in data["used"]]
    if not queue:
        print("All topics used — resetting queue.")
        data["used"] = []
        queue = data["queue"]

    topic = queue[0]
    data["used"].append(topic["slug"])

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
Du schreibst Blog-Posts für lokale österreichische Unternehmen die eine bessere Website wollen.

STIMME & STIL:
- Direkt, kein Bullshit, kein Corporate-Speak
- Du-Form durchgehend
- Kurze Sätze und Absätze (max 3 Sätze pro Absatz)
- Sprichst als Gleichgestellter, nicht als Experte der herabblickt
- Konkret: Zahlen, Beispiele, österreichischer Kontext wo sinnvoll
- Klingt wie ein smarter Freund der sich auskennt

INHALT-FRAMEWORK (Alex Hormozi / PAS):
1. Hook: Eröffne mit dem Problem/Schmerz den der Leser bereits fühlt
2. Agitate: Mach die Konsequenz greifbar — was kostet das Nichts-Tun konkret?
3. Lösung: Klar und spezifisch — was ändert sich?
4. Beweis/Logik: Erkläre warum das funktioniert (keine erfundenen Testimonials)
5. CTA: Direkt und konkret — ein klarer nächster Schritt

SEO-REGELN:
- Ziel-Keyword natürlich im ersten Absatz und in mindestens 2 Überschriften
- 750-950 Wörter gesamt
- H2-Überschriften alle 200-250 Wörter
- Eine highlight-Box (wichtigste Erkenntnis des Posts)
- Keine Keyword-Stuffing — natürlicher Lesefluss hat Vorrang

FORMATIERUNG (gibt HTML-Blöcke zurück):
Gib NUR den Artikel-Inhalt zurück — keine HTML-Shell, kein head/body.
Nur diese Tags: <p>, <h2>, <h3>, <ul>, <li>, <strong>, <div class="highlight"><p>...</p></div>
Keine anderen Tags, keine Klassen außer highlight."""

    user = f"""Schreib einen Blog-Post mit folgenden Parametern:

Titel/Hook: {topic['hook']}
Ziel-Keyword: {topic['keyword']}
Kategorie: {topic['tag']}
Hormozi-Winkel: {topic['hormozi_angle']}
Datum: {today}

Am Ende soll ein CTA-Block stehen der auf ein kostenloses Gespräch hinweist.
Gib nur den Inhalt zwischen den INHALT-Kommentaren zurück — reines HTML wie beschrieben."""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": user}]
    )

    return message.content[0].text.strip()

# ─── Build HTML file ──────────────────────────────────────────────────────────
def build_post_html(topic, content, date_str, date_iso):
    slug = topic["slug"]
    title = topic["hook"]
    tag = topic["tag"]
    keyword = topic["keyword"]
    url = f"{BASE_URL}/posts/{slug}.html"

    # Estimate read time
    word_count = len(re.sub(r'<[^>]+>', '', content).split())
    read_time = max(2, round(word_count / 200))

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Maximilian Kürner</title>
  <meta name="description" content="{title}. Von Maximilian Kürner, Webdesign Freelance aus Wels, Österreich." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{title}" />
  <meta property="og:url" content="{url}" />
  <meta property="article:published_time" content="{date_iso}" />
  <meta property="article:author" content="Maximilian Kürner" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "author": {{"@type": "Person", "name": "Maximilian Kürner"}},
    "datePublished": "{date_iso}",
    "description": "{title}",
    "url": "{url}"
  }}
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
    .btn {{ display: inline-flex; align-items: center; gap: 8px; padding: 13px 26px; border-radius: 100px; font-family: var(--font); font-size: .9rem; font-weight: 700; cursor: pointer; transition: transform var(--tr), box-shadow var(--tr); }}
    .btn-acid {{ background: var(--acid); color: #06070c; border: 1px solid rgba(200,255,0,.6); box-shadow: 0 4px 22px rgba(200,255,0,.32); }}
    .btn-acid:hover {{ transform: translateY(-2px); box-shadow: 0 8px 32px rgba(200,255,0,.48); }}
    .btn-glass {{ background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.13); backdrop-filter: blur(12px); }}
    .btn-glass:hover {{ background: rgba(255,255,255,.11); transform: translateY(-2px); }}
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
    .post-title {{ font-size: clamp(2rem,5vw,4rem); font-weight: 800; letter-spacing: -.04em; line-height: 1.08; max-width: 800px; margin: 0 auto 20px; }}
    .post-meta {{ display: flex; align-items: center; justify-content: center; gap: 16px; font-size: .82rem; color: var(--muted); }}
    .post-body {{ padding: 60px 0 100px; }}
    .post-body p {{ font-size: 1.05rem; color: rgba(240,240,240,.82); line-height: 1.8; margin-bottom: 24px; }}
    .post-body h2 {{ font-size: 1.5rem; font-weight: 800; letter-spacing: -.03em; margin: 48px 0 16px; }}
    .post-body h3 {{ font-size: 1.15rem; font-weight: 800; letter-spacing: -.02em; margin: 32px 0 12px; color: var(--acid); }}
    .post-body ul {{ padding-left: 20px; margin-bottom: 24px; }}
    .post-body li {{ font-size: 1.05rem; color: rgba(240,240,240,.82); line-height: 1.8; margin-bottom: 8px; list-style: disc; }}
    .post-body strong {{ color: var(--text); font-weight: 800; }}
    .post-body .highlight {{ background: rgba(200,255,0,.07); border-left: 3px solid var(--acid); padding: 20px 24px; border-radius: 0 12px 12px 0; margin: 32px 0; }}
    .post-body .highlight p {{ margin-bottom: 0; color: var(--text); }}
    .post-cta {{ border-radius: 20px; border: 1px solid rgba(200,255,0,.2); background: rgba(200,255,0,.04); padding: 40px; text-align: center; margin: 60px 0; }}
    .post-cta h3 {{ font-size: 1.5rem; font-weight: 800; letter-spacing: -.03em; margin-bottom: 12px; }}
    .post-cta p {{ color: var(--muted); margin-bottom: 28px; }}
    .back-link {{ display: inline-flex; align-items: center; gap: 8px; font-size: .875rem; font-weight: 700; color: var(--muted); transition: color var(--tr); margin-bottom: 60px; }}
    .back-link:hover {{ color: var(--text); }}
    footer {{ border-top: 1px solid var(--bord); padding: 28px 0; }}
    .ft {{ display: flex; align-items: center; justify-content: space-between; font-size: .82rem; color: var(--muted); }}
    @media (max-width: 600px) {{ .nav-links {{ display: none; }} }}
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

      {content}

      <div class="post-cta">
        <h3>Deine Website hat dieses Problem?</h3>
        <p>Ich schau sie mir kostenlos an und sag dir direkt was nicht stimmt — in 15 Minuten.</p>
        <a class="btn btn-acid" href="../index.html#contact">Kostenloses Gespräch →</a>
      </div>

      <a class="back-link" href="../blog.html">← Zurück zum Blog</a>
    </div>
  </div>

  <footer>
    <div class="wrap ft">
      <div>Shipped. — Maximilian Kürner</div>
      <div>© {datetime.now().year} Maximilian Kürner</div>
    </div>
  </footer>
</body>
</html>"""

# ─── Update blog.html ─────────────────────────────────────────────────────────
def update_blog_html(topic, date_str):
    with open(BLOG_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Estimate read time from topic hook length
    read_time = 3

    new_card = f"""
      <a class="blog-card" href="posts/{topic['slug']}.html">
        <div class="blog-tag">{topic['tag']}</div>
        <h2 class="blog-title">{topic['hook']}</h2>
        <p class="blog-excerpt">{topic['hook']}. Ein direkter Post über {topic['keyword'].lower()}.</p>
        <div class="blog-foot">
          <span class="blog-date">{date_str}</span>
          <span class="blog-read">{read_time} min →</span>
        </div>
      </a>
"""

    # Insert after opening blog-grid div
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

    print("Picking topic...")
    topic = pick_topic()
    print(f"Topic: {topic['hook']}")

    print("Generating content...")
    content = generate_post(topic)

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
