from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "articles"
TEMPLATE_PATH = ROOT / "templates" / "article-template.html"
INDEX_PATH = ROOT / "index.html"
SITEMAP_PATH = ROOT / "sitemap.xml"
BASE_URL = "https://hy-x.github.io/HXiao.ai"
SITE_NAME = "HXiao.ai"
DEFAULT_AUTHOR = "Hongyu Xiao"

CARD_START = "<!-- AUTO:ARTICLE_CARDS:START -->"
CARD_END = "<!-- AUTO:ARTICLE_CARDS:END -->"


@dataclass
class Article:
    slug: str
    title: str
    subtitle: str
    description: str
    excerpt: str
    tags: list[str]
    published_date: str
    published_display: str
    read_time: str
    hero_caption: str
    hero_aria: str
    body_html: str
    author: str = DEFAULT_AUTHOR

    @property
    def file_name(self) -> str:
        return f"article-{self.slug}.html"

    @property
    def canonical_url(self) -> str:
        return f"{BASE_URL}/{self.file_name}"


def load_articles() -> list[Article]:
    articles: list[Article] = []
    for meta_file in sorted(CONTENT_DIR.glob("*.json")):
        if meta_file.name.startswith("_"):
            continue

        data = json.loads(meta_file.read_text(encoding="utf-8"))
        body_file_name = data.get("body_file", f"{data['slug']}.body.html")
        body_file = meta_file.with_name(body_file_name)
        if not body_file.exists():
            raise FileNotFoundError(f"Missing article body file: {body_file}")

        article = Article(
            slug=data["slug"],
            title=data["title"],
            subtitle=data["subtitle"],
            description=data["description"],
            excerpt=data["excerpt"],
            tags=data["tags"],
            published_date=data["published_date"],
            published_display=data["published_display"],
            read_time=data["read_time"],
            hero_caption=data.get("hero_caption", "A conceptual visualization for this essay."),
            hero_aria=data.get("hero_aria", "Abstract visualization for article"),
            body_html=body_file.read_text(encoding="utf-8").strip(),
            author=data.get("author", DEFAULT_AUTHOR),
        )
        articles.append(article)

    articles.sort(key=lambda item: item.published_date, reverse=True)
    return articles


def render_feed_card(article: Article) -> str:
    tags_html = "\n".join(f'              <span class="tag">{escape(tag)}</span>' for tag in article.tags[:2])
    all_tags = "|".join(article.tags)
    return (
        f'          <a href="{escape(article.file_name)}" class="article-card" '
        f'data-topics="{escape(all_tags)}" '
        f'aria-label="Read: {escape(article.title)}">\n'
        f'            <div class="card-meta">\n'
        f'              <span class="card-author">{escape(article.author)}</span>\n'
        f'              <span class="card-meta-sep" aria-hidden="true">·</span>\n'
        f'              <time class="card-date" datetime="{escape(article.published_date)}">{escape(article.published_display)}</time>\n'
        f'            </div>\n'
        f'            <div class="card-body">\n'
        f'              <div class="card-text">\n'
        f'                <h2 class="card-title">{escape(article.title)}</h2>\n'
        f'                <p class="card-preview">{escape(article.excerpt)}</p>\n'
        f'              </div>\n'
        f'              <div class="card-thumbnail skeleton" role="img" aria-label="Article thumbnail"></div>\n'
        f'            </div>\n'
        f'            <div class="card-footer">\n'
        f'{tags_html}\n'
        f'              <span class="card-read-time">{escape(article.read_time)}</span>\n'
        f'            </div>\n'
        f'          </a>'
    )


def update_index(articles: list[Article]) -> None:
    source = INDEX_PATH.read_text(encoding="utf-8")
    cards_html = "\n\n".join(render_feed_card(article) for article in articles)
    replacement = f"{CARD_START}\n{cards_html}\n          {CARD_END}"

    pattern = re.compile(r"<!-- AUTO:ARTICLE_CARDS:START -->.*<!-- AUTO:ARTICLE_CARDS:END -->", re.S)
    if not pattern.search(source):
        raise ValueError("index.html missing AUTO article card markers")

    INDEX_PATH.write_text(pattern.sub(replacement, source), encoding="utf-8")


def render_related_cards(current: Article, articles: list[Article]) -> str:
    related = [item for item in articles if item.slug != current.slug][:2]
    if not related:
        return ""

    blocks = []
    for article in related:
        blocks.append(
            f'        <a href="{escape(article.file_name)}" class="article-card">\n'
            f'          <div class="card-meta">\n'
            f'            <div class="card-avatar" role="img" aria-label="Author avatar"></div>\n'
            f'            <span class="card-author">{escape(article.author)}</span>\n'
            f'          </div>\n'
            f'          <div class="card-body">\n'
            f'            <div class="card-text">\n'
            f'              <h3 class="card-title">{escape(article.title)}</h3>\n'
            f'              <p class="card-preview">{escape(article.excerpt)}</p>\n'
            f'            </div>\n'
            f'          </div>\n'
            f'          <div class="card-footer">\n'
            f'            <span class="tag">{escape(article.tags[0])}</span>\n'
            f'            <span class="card-read-time">{escape(article.read_time)}</span>\n'
            f'          </div>\n'
            f'        </a>'
        )

    return "\n\n".join(blocks)


def render_article_page(article: Article, articles: list[Article], template: str) -> str:
    json_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article.title,
        "description": article.description,
        "author": {"@type": "Person", "name": article.author},
        "publisher": {"@type": "Organization", "name": SITE_NAME},
        "datePublished": article.published_date,
        "dateModified": article.published_date,
        "mainEntityOfPage": article.canonical_url,
        "keywords": ["AI", "Agentic AI", "Seismology", "Research", "Science"],
    }

    replacements = {
        "{{PAGE_TITLE}}": f"{article.title} — {SITE_NAME}",
        "{{META_DESCRIPTION}}": article.description,
        "{{AUTHOR_NAME}}": article.author,
        "{{CANONICAL_URL}}": article.canonical_url,
        "{{OG_TITLE}}": f"{article.title} — {SITE_NAME}",
        "{{OG_DESCRIPTION}}": article.description,
        "{{OG_URL}}": article.canonical_url,
        "{{TWITTER_TITLE}}": f"{article.title} — {SITE_NAME}",
        "{{TWITTER_DESCRIPTION}}": article.description,
        "{{JSON_LD}}": json.dumps(json_ld, ensure_ascii=False),
        "{{ARTICLE_TITLE}}": article.title,
        "{{ARTICLE_SUBTITLE}}": article.subtitle,
        "{{PUBLISHED_DISPLAY}}": article.published_display,
        "{{READ_TIME}}": article.read_time,
        "{{HERO_ARIA}}": article.hero_aria,
        "{{HERO_CAPTION}}": article.hero_caption,
        "{{BODY_HTML}}": article.body_html,
        "{{RELATED_ARTICLES}}": render_related_cards(article, articles),
    }

    output = template
    for key, value in replacements.items():
        output = output.replace(key, value)

    return output


def build_article_pages(articles: list[Article]) -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    for article in articles:
        output = render_article_page(article, articles, template)
        (ROOT / article.file_name).write_text(output, encoding="utf-8")

    latest = ROOT / articles[0].file_name
    (ROOT / "article.html").write_text(latest.read_text(encoding="utf-8"), encoding="utf-8")


def update_sitemap(articles: list[Article]) -> None:
    today = date.today().isoformat()

    entries = [
        (f"{BASE_URL}/", today, "weekly", "1.0"),
        (f"{BASE_URL}/about.html", today, "monthly", "0.7"),
        (f"{BASE_URL}/help.html", today, "monthly", "0.5"),
        (f"{BASE_URL}/terms.html", today, "monthly", "0.4"),
        (f"{BASE_URL}/privacy.html", today, "monthly", "0.4"),
        (f"{BASE_URL}/article.html", today, "weekly", "0.9"),
    ]

    for article in articles:
        entries.append((article.canonical_url, article.published_date, "monthly", "0.8"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, priority in entries:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{loc}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                f"    <changefreq>{changefreq}</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    lines.append("")

    SITEMAP_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    articles = load_articles()
    if not articles:
        raise ValueError("No articles found in content/articles")

    update_index(articles)
    build_article_pages(articles)
    update_sitemap(articles)
    print(f"Built {len(articles)} article pages and updated index/sitemap.")


if __name__ == "__main__":
    main()
