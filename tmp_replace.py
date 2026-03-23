import sys

file_path = r'c:\Users\maxim\OneDrive\Desktop\landscaping\portfolio\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    ("<h3>Backend & APIs</h3>", "<h3>CMS & Integrations</h3>"),
    ("<h3>Backend &amp; APIs</h3>", "<h3>CMS & Integrations</h3>"),
    ("Node.js, Python, REST, GraphQL. I design and build robust backend systems and integrations from scratch.", "WordPress, Webflow, Shopify. I connect your website to your favorite tools and CRMs effortlessly."),
    ("I translate product requirements into clean systems with obsessive visual hierarchy.", "I translate brand requirements into clean web systems with obsessive visual hierarchy."),
    ("<h3>AI & Automation</h3>", "<h3>SEO & Speed</h3>"),
    ("<h3>AI &amp; Automation</h3>", "<h3>SEO & Speed</h3>"),
    ("LLM integrations, workflow automation, data pipelines. I leverage AI to dramatically accelerate delivery.", "Technical SEO, Core Web Vitals, dynamic caching. I make your website rank higher and load instantly."),
    ("Lead Gen & Mutation Engine", "Local Business Redesign"),
    ("Lead Gen &amp; Mutation Engine", "Local Business Redesign"),
    ("Automated pipeline that scrapes local business leads, analyses brand feel, and generates custom demo websites for cold outreach.", "A complete visual and technical overhaul for a local brand, drastically improving local SEO and organic lead generation."),
    ("Discovery & Scoping", "Discovery & Strategy"),
    ("Discovery &amp; Scoping", "Discovery & Strategy"),
    ("I start by deeply understanding your users, goals, and constraints. A shared, precise spec saves weeks downstream.", "I start by deeply understanding your business, target audience, and goals. A shared, precise strategy saves weeks downstream."),
    ("Design & Architecture", "Design & Layouts"),
    ("Design &amp; Architecture", "Design & Layouts"),
    ("System design and UI wireframes come together in Figma. Fast iteration cycles, low-fidelity to high-fidelity, sign-off before a line of code is written.", "Layouts and UI wireframes come together in Figma. Fast iteration cycles and sign-off before a line of code is written."),
    ("Build & Ship", "Build & Launch"),
    ("Build &amp; Ship", "Build & Launch"),
    ("Rapid, clean development with CI/CD from day one. You see real progress in weekly demos, not presentations.", "Rapid, semantic web development optimized for search engines. You see real design progress in staging, not presentations."),
    ("Launch & Iterate", "Monitor & Refine"),
    ("Launch &amp; Iterate", "Monitor & Refine"),
    ("I stay involved post-launch. Real user feedback drives the next sprint — I ship until the product feels right.", "I stay involved post-launch. Real user analytics drive the next phase — I refine until the website performs perfectly.")
]

for old, new in replacements:
    text = text.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Done')
