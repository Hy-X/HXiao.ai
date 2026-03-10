from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH_ROOT = ROOT / "zh"
CONTENT_DIR = ZH_ROOT / "content" / "articles"
TEMPLATE_PATH = ZH_ROOT / "templates" / "article-template.html"
INDEX_PATH = ZH_ROOT / "index.html"
SITEMAP_PATH = ROOT / "sitemap.xml"
BASE_URL = "https://hy-x.github.io/HXiao.ai/zh"
EN_BASE_URL = "https://hy-x.github.io/HXiao.ai"
SITE_NAME = "HXiao.ai"
DEFAULT_AUTHOR = "肖鸿宇"

CARD_START = "<!-- AUTO:ARTICLE_CARDS:START -->"
CARD_END = "<!-- AUTO:ARTICLE_CARDS:END -->"
STAFF_START = "<!-- AUTO:STAFF_PICKS:START -->"
STAFF_END = "<!-- AUTO:STAFF_PICKS:END -->"


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
    hero_image_placeholder: str
    hero_image_note: str
    hero_image_file: str
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
            hero_caption=data.get("hero_caption", "本文的概念化视觉呈现。"),
            hero_aria=data.get("hero_aria", "文章抽象可视化"),
            hero_image_placeholder=data.get("hero_image_placeholder", "1200x630 封面图"),
            hero_image_note=data.get("hero_image_note", "请替换为最终文章头图。"),
            hero_image_file=data.get("hero_image_file", ""),
            body_html=body_file.read_text(encoding="utf-8").strip(),
            author=data.get("author", DEFAULT_AUTHOR),
        )
        articles.append(article)

    articles.sort(key=lambda item: item.published_date, reverse=True)
    return articles


def render_feed_card(article: Article) -> str:
    tags_html = "\n".join(f'              <span class="tag">{escape(tag)}</span>' for tag in article.tags[:2])
    all_tags = "|".join(article.tags)

    # Thumbnail: real image if available (shared from EN content), skeleton otherwise
    image_file = article.hero_image_file
    if image_file and (ROOT / image_file).exists():
        thumbnail_html = (
            f'              <img class="card-thumbnail" '
            f'src="../{escape(image_file)}" '
            f'alt="{escape(article.hero_aria)}" '
            f'loading="lazy" decoding="async" />\n'
        )
    else:
        thumbnail_html = '              <div class="card-thumbnail skeleton" role="img" aria-label="文章缩略图"></div>\n'

    return (
        f'          <a href="{escape(article.file_name)}" class="article-card" '
        f'data-topics="{escape(all_tags)}" '
        f'aria-label="阅读：{escape(article.title)}">\n'
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
        f'{thumbnail_html}'
        f'            </div>\n'
        f'            <div class="card-footer">\n'
        f'{tags_html}\n'
        f'              <span class="card-read-time">{escape(article.read_time)}</span>\n'
        f'              <div class="card-actions">\n'
        f'                <span aria-label="收藏" class="btn-icon" title="收藏"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg></span>\n'
        f'                <span aria-label="更多" class="btn-icon" title="更多选项"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg></span>\n'
        f'              </div>\n'
        f'            </div>\n'
        f'          </a>'
    )


def render_staff_pick(article: Article) -> str:
    return (
        f'            <div class="sidebar-pick">\n'
        f'              <div class="sidebar-pick-meta">\n'
        f'                <div class="sidebar-pick-avatar" role="img" aria-label="作者头像"></div>\n'
        f'                <span>{escape(article.author)}</span>\n'
        f'              </div>\n'
        f'              <a href="{escape(article.file_name)}" class="sidebar-pick-title">{escape(article.title)}</a>\n'
        f'            </div>'
    )


def update_index(articles: list[Article]) -> None:
    source = INDEX_PATH.read_text(encoding="utf-8")
    cards_html = "\n\n".join(render_feed_card(article) for article in articles)
    cards_replacement = f"{CARD_START}\n{cards_html}\n          {CARD_END}"

    staff_html = "\n\n".join(render_staff_pick(article) for article in articles[:3])
    staff_replacement = f"{STAFF_START}\n{staff_html}\n            {STAFF_END}"

    cards_pattern = re.compile(r"<!-- AUTO:ARTICLE_CARDS:START -->.*<!-- AUTO:ARTICLE_CARDS:END -->", re.S)
    if not cards_pattern.search(source):
        raise ValueError("zh/index.html missing AUTO article card markers")

    staff_pattern = re.compile(r"<!-- AUTO:STAFF_PICKS:START -->.*<!-- AUTO:STAFF_PICKS:END -->", re.S)
    if not staff_pattern.search(source):
        raise ValueError("zh/index.html missing AUTO staff picks markers")

    updated = cards_pattern.sub(cards_replacement, source)
    updated = staff_pattern.sub(staff_replacement, updated)
    INDEX_PATH.write_text(updated, encoding="utf-8")


def render_related_cards(current: Article, articles: list[Article]) -> str:
    related = [item for item in articles if item.slug != current.slug][:2]
    if not related:
        return ""

    blocks = []
    for article in related:
        image_file = article.hero_image_file
        if image_file and (ROOT / image_file).exists():
            thumb = (
                f'          <img class="card-thumbnail" '
                f'src="../{escape(image_file)}" '
                f'alt="{escape(article.hero_aria)}" loading="lazy" decoding="async" />\n'
            )
        else:
            thumb = '          <div class="card-thumbnail skeleton" role="img" aria-label="文章缩略图"></div>\n'

        blocks.append(
            f'        <a href="{escape(article.file_name)}" class="article-card">\n'
            f'          <div class="card-meta">\n'
            f'            <div class="card-avatar" role="img" aria-label="作者头像"></div>\n'
            f'            <span class="card-author">{escape(article.author)}</span>\n'
            f'          </div>\n'
            f'          <div class="card-body">\n'
            f'            <div class="card-text">\n'
            f'              <h3 class="card-title">{escape(article.title)}</h3>\n'
            f'              <p class="card-preview">{escape(article.excerpt)}</p>\n'
            f'            </div>\n'
            f'{thumb}'
            f'          </div>\n'
            f'          <div class="card-footer">\n'
            f'            <span class="tag">{escape(article.tags[0])}</span>\n'
            f'            <span class="card-read-time">{escape(article.read_time)}</span>\n'
            f'            <div class="card-actions">\n'
            f'              <span aria-label="收藏" class="btn-icon" title="收藏"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg></span>\n'
            f'              <span aria-label="更多" class="btn-icon" title="更多选项"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg></span>\n'
            f'            </div>\n'
            f'          </div>\n'
            f'        </a>'
        )

    return "\n\n".join(blocks)


def render_hero_media(article: Article) -> str:
    if article.hero_image_file:
        image_path = ROOT / article.hero_image_file
        if image_path.exists():
            return (
                f'      <img class="article-hero-image article-hero-image-full" '
                f'src="../{escape(article.hero_image_file)}" '
                f'alt="{escape(article.hero_aria)}" loading="eager" decoding="async" />'
            )

    return (
        f'      <div class="article-hero-image article-hero-image-full skeleton" role="img" '
        f'aria-label="{escape(article.hero_aria)}" '
        f'data-image-placeholder="{escape(article.hero_image_placeholder)}"></div>'
    )


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
        "keywords": ["AI", "智能体AI", "地震学", "研究", "科学"],
        "inLanguage": "zh-Hans",
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
        "{{HERO_IMAGE_PLACEHOLDER}}": article.hero_image_placeholder,
        "{{HERO_IMAGE_NOTE}}": article.hero_image_note,
        "{{HERO_MEDIA}}": render_hero_media(article),
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
        (ZH_ROOT / article.file_name).write_text(output, encoding="utf-8")

    latest = ZH_ROOT / articles[0].file_name
    (ZH_ROOT / "article.html").write_text(latest.read_text(encoding="utf-8"), encoding="utf-8")


def update_sitemap(articles: list[Article]) -> None:
    """Append Chinese URLs to the existing sitemap (or create from scratch with both EN + ZH)."""
    today = date.today().isoformat()

    # English base entries
    en_entries = [
        (f"{EN_BASE_URL}/", today, "weekly", "1.0"),
        (f"{EN_BASE_URL}/about.html", today, "monthly", "0.7"),
        (f"{EN_BASE_URL}/help.html", today, "monthly", "0.5"),
        (f"{EN_BASE_URL}/terms.html", today, "monthly", "0.4"),
        (f"{EN_BASE_URL}/privacy.html", today, "monthly", "0.4"),
        (f"{EN_BASE_URL}/article.html", today, "weekly", "0.9"),
    ]

    # Read existing English article URLs from the EN content dir
    en_content_dir = ROOT / "content" / "articles"
    en_articles = []
    for meta_file in sorted(en_content_dir.glob("*.json")):
        if meta_file.name.startswith("_"):
            continue
        data = json.loads(meta_file.read_text(encoding="utf-8"))
        en_articles.append((f"{EN_BASE_URL}/article-{data['slug']}.html", data["published_date"], "monthly", "0.8"))

    # Chinese entries
    zh_entries = [
        (f"{BASE_URL}/", today, "weekly", "0.9"),
        (f"{BASE_URL}/article.html", today, "weekly", "0.8"),
    ]
    zh_article_entries = [(article.canonical_url, article.published_date, "monthly", "0.7") for article in articles]

    all_entries = en_entries + en_articles + zh_entries + zh_article_entries

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, priority in all_entries:
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
    if not ZH_ROOT.exists():
        raise FileNotFoundError(f"zh/ directory not found at {ZH_ROOT}. Run setup first.")

    articles = load_articles()
    if not articles:
        raise ValueError("No Chinese articles found in zh/content/articles")

    update_index(articles)
    build_article_pages(articles)
    update_sitemap(articles)
    print(f"Built {len(articles)} Chinese article pages, updated zh/index.html and sitemap.xml.")


if __name__ == "__main__":
    main()
