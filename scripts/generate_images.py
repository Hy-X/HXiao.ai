from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "articles"
STYLE_CONFIG_PATH = ROOT / "content" / "image-style.json"
IMAGE_OUTPUT_DIR = ROOT / "assets" / "images" / "articles"
DEFAULT_MODEL = "gemini-2.5-flash-image"
DEFAULT_API_BASE = "https://generativelanguage.googleapis.com/v1beta"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_article_meta_files() -> list[Path]:
    return sorted(
        meta_file
        for meta_file in CONTENT_DIR.glob("*.json")
        if not meta_file.name.startswith("_")
    )


def build_prompt(style: dict, article: dict) -> str:
    title = article.get("title", "Untitled")
    subtitle = article.get("subtitle", "")
    placeholder = article.get("hero_image_placeholder", "1200x630 editorial cover image")
    note = article.get("hero_image_note", "")
    excerpt = article.get("excerpt", "")

    sections = [
        f"STYLE PRESET: {style.get('style_name', 'Custom style')}",
        f"GLOBAL STYLE: {style.get('global_style_prompt', '')}",
        f"ARTICLE TITLE: {title}",
        f"ARTICLE SUBTITLE: {subtitle}",
        f"IMAGE BRIEF: {placeholder}",
        f"ARTICLE NOTE: {note}",
        f"CONTEXT: {excerpt}",
        "OUTPUT: one horizontal hero image suitable for article cover.",
        f"NEGATIVE CONSTRAINTS: {style.get('negative_prompt', '')}",
    ]

    return "\n".join(item for item in sections if item.strip())


def call_gemini_image(api_key: str, model: str, prompt: str) -> tuple[bytes, str]:
    api_base = os.environ.get("GEMINI_API_BASE", DEFAULT_API_BASE).rstrip("/")
    normalized_model = model.removeprefix("models/")
    endpoint = f"{api_base}/models/{normalized_model}:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        },
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API request failed ({error.code}): {body}") from error

    for candidate in response_data.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            inline_data = part.get("inlineData") or part.get("inline_data")
            if not inline_data:
                continue
            b64 = inline_data.get("data")
            mime = inline_data.get("mimeType") or inline_data.get("mime_type") or "image/png"
            if b64:
                return base64.b64decode(b64), mime

    raise RuntimeError("Gemini response did not include inline image data")


def extension_for_mime(mime_type: str) -> str:
    if mime_type == "image/jpeg":
        return ".jpg"
    if mime_type == "image/webp":
        return ".webp"
    return ".png"


def generate_for_article(meta_path: Path, style: dict, api_key: str, model: str, force: bool) -> str:
    article = load_json(meta_path)
    slug = article["slug"]
    prompt = build_prompt(style, article)

    IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    existing = article.get("hero_image_file", "")
    if existing and (ROOT / existing).exists() and not force:
        return f"skip {slug}: image exists ({existing})"

    image_bytes, mime = call_gemini_image(api_key=api_key, model=model, prompt=prompt)
    ext = extension_for_mime(mime)
    image_rel = Path("assets") / "images" / "articles" / f"{slug}-hero{ext}"
    image_abs = ROOT / image_rel
    image_abs.write_bytes(image_bytes)

    article["hero_image_file"] = image_rel.as_posix()
    meta_path.write_text(json.dumps(article, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return f"ok {slug}: wrote {image_rel.as_posix()}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate article hero images with Gemini API")
    parser.add_argument("--force", action="store_true", help="Regenerate images even if hero_image_file already exists")
    parser.add_argument("--model", default=os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_MODEL), help="Gemini model name")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is required")

    if not STYLE_CONFIG_PATH.exists():
        raise SystemExit(f"Missing style config: {STYLE_CONFIG_PATH}")

    style = load_json(STYLE_CONFIG_PATH)

    results = []
    for meta_path in iter_article_meta_files():
        results.append(generate_for_article(meta_path, style, api_key, args.model, args.force))

    for line in results:
        print(line)


if __name__ == "__main__":
    main()
