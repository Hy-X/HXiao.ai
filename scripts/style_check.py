from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "css" / "styles.css"
DESIGN_RULES_PATH = ROOT / "design-rules.md"

REQUIRED_ROOT_VARS = {
    "--color-bg": "#FFFFFF",
    "--color-surface": "#F9F9F9",
    "--color-border": "#E6E6E6",
    "--color-text-primary": "#242424",
    "--color-text-secondary": "#6B6B6B",
    "--color-text-muted": "#B3B3B3",
    "--color-accent": "#1A8917",
    "--color-tag-bg": "#F2F2F2",
    "--max-article": "680px",
    "--max-feed": "1192px",
    "--navbar-height": "65px",
    "--radius-sm": "4px",
    "--radius-pill": "99px",
    "--transition-fast": "150ms ease",
    "--transition-base": "200ms ease",
}

REQUIRED_DARK_MODE_VARS = {
    "--color-bg": "#191919",
    "--color-surface": "#242424",
    "--color-border": "#2E2E2E",
    "--color-text-primary": "#E6E6E6",
    "--color-text-secondary": "#999999",
}

MAX_TRANSITION_MS = 300


def extract_block(css: str, marker: str) -> str:
    start = css.find(marker)
    if start == -1:
        return ""

    brace_start = css.find("{", start)
    if brace_start == -1:
        return ""

    depth = 0
    for index in range(brace_start, len(css)):
        char = css[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return css[brace_start + 1 : index]

    return ""


def parse_vars(block: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", block, flags=re.I):
        values[name.strip()] = value.strip()
    return values


def check_required_vars(css: str, errors: list[str]) -> None:
    root_block = extract_block(css, ":root")
    if not root_block:
        errors.append("Missing ':root' CSS variable block")
        return

    root_vars = parse_vars(root_block)
    for var_name, expected in REQUIRED_ROOT_VARS.items():
        actual = root_vars.get(var_name)
        if actual != expected:
            errors.append(
                f"CSS variable {var_name} expected '{expected}' but found '{actual or 'missing'}'"
            )

    dark_block = extract_block(css, "@media (prefers-color-scheme: dark)")
    if not dark_block:
        errors.append("Missing dark mode block '@media (prefers-color-scheme: dark)'")
        return

    dark_root_block = extract_block(dark_block, ":root")
    if not dark_root_block:
        errors.append("Missing ':root' block inside dark mode media query")
        return

    dark_vars = parse_vars(dark_root_block)
    for var_name, expected in REQUIRED_DARK_MODE_VARS.items():
        actual = dark_vars.get(var_name)
        if actual != expected:
            errors.append(
                f"Dark mode variable {var_name} expected '{expected}' but found '{actual or 'missing'}'"
            )


def check_reduced_motion(css: str, errors: list[str]) -> None:
    reduced_motion_block = extract_block(css, "@media (prefers-reduced-motion: reduce)")
    if not reduced_motion_block:
        errors.append("Missing reduced-motion media query")
        return

    if "transition: none !important;" not in reduced_motion_block:
        errors.append("Reduced-motion block must disable transitions")

    if "animation: none !important;" not in reduced_motion_block:
        errors.append("Reduced-motion block must disable animations")


def duration_to_ms(value: str, unit: str) -> float:
    amount = float(value)
    if unit == "s":
        return amount * 1000
    return amount


def check_transition_durations(css: str, errors: list[str]) -> None:
    # Enforce design-rules.md §8: transition-duration never exceeds 300ms.
    for match in re.finditer(r"transition(?:-duration)?\s*:\s*([^;]+);", css):
        declaration = match.group(1)
        for duration, unit in re.findall(r"(\d*\.?\d+)\s*(ms|s)", declaration):
            duration_ms = duration_to_ms(duration, unit)
            if duration_ms > MAX_TRANSITION_MS:
                errors.append(
                    "Transition duration exceeds 300ms: "
                    f"'{match.group(0).strip()}'"
                )


def check_article_body_typography(css: str, errors: list[str]) -> None:
    article_body_match = re.search(r"\.article-body\s*\{([^}]+)\}", css, flags=re.S)
    if not article_body_match:
        errors.append("Missing '.article-body' style block")
        return

    article_body = article_body_match.group(1)
    required_declarations = [
        "font-family: var(--font-serif);",
        "font-size: var(--text-article);",
        "line-height: var(--leading-body);",
        "max-width: var(--max-article);",
    ]

    for declaration in required_declarations:
        if declaration not in article_body:
            errors.append(f".article-body missing declaration: {declaration}")

    mobile_block = extract_block(css, "@media (max-width: 728px)")
    if not mobile_block or ".article-body" not in mobile_block or "font-size: 18px;" not in mobile_block:
        errors.append("Mobile rule must set '.article-body' font-size to 18px")


def check_html_basics(errors: list[str]) -> None:
    html_files = sorted(ROOT.glob("*.html"))
    if not html_files:
        errors.append("No root-level HTML files found")
        return

    required_snippets = [
        '<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
        '<link rel="stylesheet" href="css/styles.css" />',
    ]

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        for snippet in required_snippets:
            if snippet not in content:
                errors.append(f"{html_file.name} missing required tag: {snippet}")


def run() -> int:
    errors: list[str] = []

    if not DESIGN_RULES_PATH.exists():
        errors.append(f"Missing design rules file: {DESIGN_RULES_PATH}")

    if not CSS_PATH.exists():
        errors.append(f"Missing stylesheet: {CSS_PATH}")
    else:
        css = CSS_PATH.read_text(encoding="utf-8")
        check_required_vars(css, errors)
        check_reduced_motion(css, errors)
        check_transition_durations(css, errors)
        check_article_body_typography(css, errors)

    check_html_basics(errors)

    if errors:
        print("Style check failed against design-rules.md:\n")
        for index, item in enumerate(errors, start=1):
            print(f"{index}. {item}")
        return 1

    print("Style check passed (design-rules.md baseline).")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
