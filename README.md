# HXiao.ai
[![Live Site](https://img.shields.io/badge/Live-HXiao.ai-242424?style=flat&logo=githubpages&logoColor=white)](https://hy-x.github.io/HXiao.ai/)

HXiao.ai is a reading-first personal website by Hongyu Xiao.

It publishes long-form essays and research notes on:
- AI
- Agentic AI systems
- Seismology
- Research methods
- Science and reproducible workflows

The site follows an editorial minimal design system inspired by Medium-style clarity: serif body typography, restrained UI, and content-first layout.

## Live Site
- Website: https://hy-x.github.io/HXiao.ai/
- Sitemap: https://hy-x.github.io/HXiao.ai/sitemap.xml
- Robots: https://hy-x.github.io/HXiao.ai/robots.txt
- LLMs file: https://hy-x.github.io/HXiao.ai/llms.txt

## Website Pages
- Home feed: `index.html`
- About page: `about.html`
- Latest article alias: `article.html`
- Generated article pages: `article-<slug>.html`

## Core Topics (Search Intent)
- AI research and practical AI systems
- Agentic workflows and tool-using agents
- Seismology + AI applications
- Scientific reasoning, uncertainty, and evaluation
- Multi-agent systems and safety considerations

## Technical Stack
- Static HTML pages
- Custom CSS design system in `css/styles.css`
- GitHub Pages deployment via GitHub Actions
- Python content builder in `scripts/build_site.py`
- Article template in `templates/article-template.html`
- Article content source files in `content/articles/`
- Structured metadata for search and AI discovery (meta tags, Open Graph, JSON-LD, sitemap, robots, llms.txt)

## Publish a New Article (Automated)
1. Copy `content/articles/_example.json` to `content/articles/<slug>.json`.
2. Copy `content/articles/_example.body.html` to `content/articles/<slug>.body.html`.
3. Fill in title, subtitle, tags, dates, excerpt, and body content.
3. Run the builder locally:
	- `./.venv/bin/python scripts/build_site.py`
   - This now also runs `scripts/style_check.py` automatically after generating pages.
4. Commit and push to `main`.

What is generated automatically:
- Homepage feed cards in `index.html`
- New article page `article-<slug>.html`
- Latest alias page `article.html`
- URL entries in `sitemap.xml`

Quality checks:
- Build-time style conformance check against `design-rules.md` via `scripts/style_check.py`
- Optional standalone run: `./.venv/bin/python scripts/style_check.py`

## Auto-Generate Hero Images (Gemini)

You can generate article hero images automatically using the Google Gemini API.

1. Define global visual direction in `content/image-style.json`.
2. Keep per-article image brief fields in each `content/articles/<slug>.json`:
	- `hero_image_placeholder`
	- `hero_image_note`
3. Export your API key:
	- `export GEMINI_API_KEY="..."`
4. Generate hero images:
	- `./.venv/bin/python scripts/generate_images.py`
	- Optional force regenerate: `./.venv/bin/python scripts/generate_images.py --force`
5. Rebuild pages so generated images are embedded:
	- `./.venv/bin/python scripts/build_site.py`

Optional environment variables:
- `GEMINI_IMAGE_MODEL` (default: `gemini-2.5-flash-image`)
- `GEMINI_API_BASE` (default: `https://generativelanguage.googleapis.com/v1beta`)

Generated images are written to `assets/images/articles/`, and each article JSON gets `hero_image_file` set automatically.

### Secret Safety (Recommended)

- Never hardcode API keys in tracked files.
- Keep local secrets in `.env` (ignored by git) or shell environment variables.
- `.env.example` is provided as a safe template with placeholders only.

Local setup example:

```bash
cp .env.example .env
source .env
./.venv/bin/python scripts/generate_images.py
./.venv/bin/python scripts/build_site.py
```

The GitHub Pages workflow also runs the same builder step on every deploy.

Files beginning with `_` are treated as templates and ignored by the builder.

## SEO & AI Indexing Setup

### Google Search Console
1. Open https://search.google.com/search-console
2. Add property: `https://hy-x.github.io/HXiao.ai/`
3. Verify ownership (HTML tag method is easiest for GitHub Pages sites).
4. In **Sitemaps**, submit: `https://hy-x.github.io/HXiao.ai/sitemap.xml`
5. Use **URL Inspection** to request indexing for homepage and key pages.

### Bing Webmaster Tools
1. Open https://www.bing.com/webmasters
2. Add site: `https://hy-x.github.io/HXiao.ai/`
3. Verify ownership.
4. Submit sitemap: `https://hy-x.github.io/HXiao.ai/sitemap.xml`

### Notes
- Keep canonical URLs and sitemap domain aligned if switching to a custom domain.
- Re-submit sitemap after major content updates.
- Ensure GitHub Pages workflow stays green after every push to `main`.
- Keep page titles, descriptions, and article headings aligned with target topics (AI, Agentic AI, Seismology, Research, Science).

## Deployment
- Source branch: `main`
- Auto deploy: `.github/workflows/deploy-pages.yml`
- GitHub Pages URL: https://hy-x.github.io/HXiao.ai/
