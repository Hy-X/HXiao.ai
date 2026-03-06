# Design System
> A comprehensive reference to compose and understand web aesthetic.

---

## 1. Design Philosophy

This Website's design is **editorial minimalism** — a reading-first experience that gets out of its own way. Every decision serves the written word.

**Core Principles:**
- **Typography is the UI.** Fonts carry visual weight; chrome is stripped to near-nothing.
- **Whitespace is content.** Generous padding signals quality and calm.
- **No decoration for its own sake.** If an element doesn't aid reading or navigation, it doesn't exist.
- **Progressive disclosure.** Menus, bylines, and secondary actions appear only when needed.
- **Trust through restraint.** The minimal aesthetic signals that the platform is serious about ideas.

---

## 2. Color Palette

### Light Mode (Default)

| Role               | Value       | Usage                                      |
|--------------------|-------------|--------------------------------------------|
| Background         | `#FFFFFF`   | Page background, card surfaces             |
| Surface Elevated   | `#F9F9F9`   | Sidebar panels, hover states               |
| Border Subtle      | `#E6E6E6`   | Dividers, card outlines                    |
| Text Primary       | `#242424`   | Body copy, headings                        |
| Text Secondary     | `#6B6B6B`   | Bylines, metadata, captions                |
| Text Muted         | `#B3B3B3`   | Placeholders, disabled states              |
| Accent / Brand     | `#1A8917`   | Follow buttons (green), publication tags   |
| Link / Action      | `#1565C0`   | In-text links (sparingly used)             |
| Highlight          | `#FFF176`   | Text highlight (annotation feature)        |
| Tag Background     | `#F2F2F2`   | Topic pill backgrounds                     |
| Tag Text           | `#242424`   | Topic pill labels                          |

### Dark Mode

| Role               | Value       |
|--------------------|-------------|
| Background         | `#191919`   |
| Surface Elevated   | `#242424`   |
| Border Subtle      | `#2E2E2E`   |
| Text Primary       | `#E6E6E6`   |
| Text Secondary     | `#999999`   |
| Accent / Brand     | `#1A8917`   |

**Color Rule:** This website almost never uses color. When it does appear (green Follow, highlight yellow), it carries maximum weight precisely because it's rare.

---

## 3. Typography

### Font Families

| Role            | Font                        | Fallback                          |
|-----------------|-----------------------------|-----------------------------------|
| **Display / Hero** | `gt-super`, `Georgia`    | `"Times New Roman", serif`        |
| **Body / Article** | `charter`, `Georgia`     | `"Times New Roman", serif`        |
| **UI / Sans**      | `sohne`, `Helvetica Neue` | `Arial, sans-serif`               |
| **Code**           | `source-code-pro`         | `"Courier New", monospace`        |

> This website could uses fons such as **Playfair Display** (display), **Lora** (body serif), **DM Sans** (UI).

### Type Scale

| Name             | Size      | Weight    | Line Height | Usage                            |
|------------------|-----------|-----------|-------------|----------------------------------|
| `hero-title`     | `46px`    | `700`     | `1.18`      | Homepage hero heading            |
| `hero-subtitle`  | `28px`    | `400`     | `1.4`       | Homepage tagline                 |
| `article-title`  | `32px`    | `700`     | `1.2`       | Story page H1                    |
| `article-h2`     | `24px`    | `700`     | `1.3`       | In-article subheadings           |
| `article-body`   | `20px`    | `400`     | `1.8`       | Long-form article body           |
| `feed-title`     | `18px`    | `700`     | `1.3`       | Card headline in feed            |
| `feed-preview`   | `14px`    | `400`     | `1.5`       | Card excerpt in feed             |
| `ui-label`       | `14px`    | `400`     | `1.4`       | Navigation, metadata, bylines    |
| `ui-small`       | `12px`    | `400`     | `1.4`       | Tags, timestamps, read time      |
| `caption`        | `14px`    | `400`     | `1.5`       | Image captions (italic)          |

### Typography Rules
- Body text is always **serif** for long-form articles — never sans-serif.
- Headings inside articles use the same serif as body, bold weight.
- Navigation and metadata use a **neutral sans-serif** (Sohne/DM Sans).
- Letter-spacing is never manipulated on body text.
- Max body column width: **680px** (desktop), **full width minus 24px padding** (mobile).

---

## 4. Layout & Grid

### Page Structure

```
[Navbar — full width, 65px height]
[Content Area — centered, max-width varies by page]
[Footer — full width, minimal]
```

### Content Max-Widths

| Context             | Max Width  |
|---------------------|------------|
| Homepage / Feed     | `1192px`   |
| Article body        | `680px`    |
| Article with sidebar| `1032px` (body 680 + sidebar 320 + gap) |
| Navbar inner        | `1192px`   |

### Spacing Scale (8px base unit)

| Token   | Value  | Usage                              |
|---------|--------|------------------------------------|
| `4px`   | xs     | Internal padding in tags, icons    |
| `8px`   | sm     | Gap between inline elements        |
| `16px`  | md     | Card internal padding              |
| `24px`  | lg     | Section gaps, page side padding    |
| `32px`  | xl     | Between cards in feed              |
| `48px`  | 2xl    | Major section separation           |
| `64px`  | 3xl    | Hero top padding                   |
| `80px`  | 4xl    | Article content top margin         |

### Column Patterns

**Homepage Feed (desktop):**
```
[Left Nav — 240px] | [Main Feed — auto] | [Right Sidebar — 300px]
```

**Article Page (desktop):**
```
[Centered column — 680px max, auto margins]
Sticky right sidebar appears at ≥1080px: position:absolute, right: -280px
```

---

## 5. Components

### 5.1 Navigation Bar

```
[M logo]   [Topics dropdown]   [Search icon]   [Write]   [Sign In]   [Get Started (CTA)]
```

- Height: `65px`
- Background: `#FFFFFF` with `1px` border-bottom `#E6E6E6`
- Logo: SVG wordmark "M", black, `~28px` tall
- Links: `14px` sohne, `#242424`, no underline, hover: underline
- **"Get Started" CTA**: Black background `#242424`, white text, `border-radius: 99px`, `padding: 8px 20px`, `font-size: 14px`
- On scroll past 65px: navbar gains `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`

### 5.2 Article Card (Feed)

Layout: Image right (optional), text left
```
[Author avatar 20px] [Author name] · [Publication] · [Follow button]
[Card Title — 18px bold serif]
[Preview text — 14px sans, 2 lines max, color #6B6B6B]
[Tag pill] [Read time] [Bookmark icon] [More icon]
```

- Card: No border, no shadow by default
- Hover state: Background `#F9F9F9`, smooth `200ms ease` transition
- Thumbnail: `112px × 112px`, `border-radius: 4px`, `object-fit: cover`, right-aligned
- Title max-lines: 3, `-webkit-line-clamp: 3`
- Border between cards: `1px solid #E6E6E6`

### 5.3 Topic / Tag Pills

```css
.tag {
  display: inline-block;
  background: #F2F2F2;
  color: #242424;
  font-size: 13px;
  font-family: sohne, sans-serif;
  padding: 6px 12px;
  border-radius: 99px;
  cursor: pointer;
  transition: background 150ms ease;
}
.tag:hover {
  background: #E6E6E6;
}
```

### 5.4 Follow Button

Two states:

**Unfollow state:**
```css
.follow-btn {
  background: #1A8917;
  color: #FFFFFF;
  border: none;
  border-radius: 99px;
  font-size: 14px;
  padding: 7px 16px;
  cursor: pointer;
}
```

**Following state:**
```css
.following-btn {
  background: transparent;
  color: #242424;
  border: 1px solid #242424;
  border-radius: 99px;
}
```

### 5.5 Primary CTA Button

Used for "Get Started", "Start reading":
```css
.cta-primary {
  background: #242424;
  color: #FFFFFF;
  border-radius: 99px;
  padding: 12px 28px;
  font-size: 15px;
  font-family: sohne, sans-serif;
  font-weight: 500;
  letter-spacing: 0.01em;
  border: none;
  cursor: pointer;
  transition: opacity 150ms ease;
}
.cta-primary:hover {
  opacity: 0.85;
}
```

### 5.6 Article Body Styles

```css
.article-body {
  font-family: charter, Georgia, serif;
  font-size: 20px;
  line-height: 1.8;
  color: #242424;
  max-width: 680px;
  margin: 0 auto;
}

.article-body p { margin-bottom: 2em; }

.article-body h2 {
  font-size: 24px;
  font-weight: 700;
  margin: 2.5em 0 0.5em;
}

.article-body blockquote {
  border-left: 3px solid #242424;
  padding-left: 24px;
  font-style: italic;
  color: #6B6B6B;
  margin: 2em 0;
}

.article-body img {
  width: 100%;
  margin: 2em 0;
}

.article-body figcaption {
  text-align: center;
  font-size: 14px;
  color: #6B6B6B;
  font-style: italic;
  margin-top: -1.5em;
}

.article-body code {
  font-family: source-code-pro, monospace;
  background: #F2F2F2;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.85em;
}

.article-body pre {
  background: #F2F2F2;
  padding: 24px;
  overflow-x: auto;
  border-radius: 4px;
}
```

### 5.7 Clap Button (Article Engagement)

- Icon: Hand-clap SVG, `24px`
- Count text: `14px` sans, `#6B6B6B`
- On click: bouncy scale animation (`transform: scale(1.3)` then back)
- Held click animates count incrementally
- Positioned: Sticky left sidebar on desktop, inline below article on mobile

### 5.8 Author Byline (Article Header)

```
[Avatar 48px circle] [Author Name bold 15px] [Follow button sm]
                     [Publication · Date · Read time  — 13px #6B6B6B]
```

### 5.9 Divider

```css
.divider {
  border: none;
  border-top: 1px solid #E6E6E6;
  margin: 32px 0;
}
```

---

## 6. Imagery

- **Hero image**: Full-width, max-height `525px`, `object-fit: cover`, no border-radius on full-bleed
- **Card thumbnails**: `112×112px` square, `border-radius: 4px`
- **Author avatars**: Circular, `20px` (card) / `48px` (article header) / `32px` (nav dropdown)
- **Publication logos**: Circular or square, `24px` in feed, `64px` on publication page
- Image captions: Always centered, italic, `14px`, `#6B6B6B`
- No image borders or shadows
- Lazy-load all images below the fold

---

## 7. Iconography

- Style: **Thin stroke** SVG icons, `1.5px` stroke, rounded caps
- Size: `20px × 20px` standard; `24px` for primary actions
- Color: `#6B6B6B` default; `#242424` on active/hover
- Icon set feel: Custom, not Heroicons or FontAwesome — subdued and editorial
- Key icons used: Bookmark, More (···), Share, Clap/Applause, Search, Write (pencil), Arrow (→)

---

## 8. Motion & Interaction

This website uses **almost no animation** — interactions feel instant and confident.

| Interaction               | Animation                                     |
|---------------------------|-----------------------------------------------|
| Button hover              | `opacity` or `background` 150ms ease          |
| Card hover                | Background color swap, 200ms ease             |
| Navbar on scroll          | `box-shadow` fade-in, 200ms ease              |
| Follow button state change| Color swap, 150ms ease                        |
| Clap button               | `scale(1.3)` spring bounce on click           |
| Page transitions           | None (hard navigation)                        |
| Skeleton loaders          | Subtle shimmer (`opacity 0.4 → 1`, 1.2s loop) |

**Rules:**
- `transition-duration` never exceeds `300ms`
- No parallax
- No entrance animations on scroll
- No looping background animations

---

## 9. Responsive Behavior

| Breakpoint   | Width       | Changes                                               |
|--------------|-------------|-------------------------------------------------------|
| Mobile       | `< 728px`   | Single column, no sidebar, 24px side padding          |
| Tablet       | `728–1080px`| Single column feed, sidebar hidden                    |
| Desktop SM   | `1080–1280px`| Two-column feed, sidebar appears                     |
| Desktop LG   | `> 1280px`  | Full three-zone layout                                |

**Mobile specifics:**
- Navbar collapses to: `[M logo]` left, `[Sign In] [Get Started]` right
- Card images move above text (stacked layout)
- Article font-size drops to `18px`
- Sticky article actions (clap, bookmark) move to bottom bar

---

## 10. Accessibility

- Minimum contrast ratio: **4.5:1** for body text (WCAG AA)
- Focus states: `outline: 2px solid #242424; outline-offset: 2px` — never suppressed with `outline: none` without replacement
- All images have meaningful `alt` text
- Interactive elements: minimum tap target `44×44px`
- Font size never below `12px`
- `prefers-reduced-motion`: disable all transitions and animations

---

## 11. Do's and Don'ts

### ✅ Do
- Use a single serif for all long-form body text
- Let whitespace breathe — resist filling every gap
- Keep the navbar minimal; hide secondary links
- Use black CTAs with rounded corners
- Keep color usage to a strict minimum (green for follow/action only)
- Right-align thumbnails in feed cards
- Italicize blockquotes and captions

### ❌ Don't
- Use gradients, drop shadows, or decorative backgrounds
- Mix multiple typefaces in the article body
- Use colored backgrounds on cards or sections
- Animate page transitions or scroll events
- Use icon-heavy navigation
- Place ads or widgets inside the article column
- Underline links inside body text (rely on color + hover)
- Use `border-radius` > `4px` except on pills/avatars/buttons

---

## 12. Page Templates

### Homepage (Logged Out)
```
Navbar
─────────────────────────────────────────
  [Hero — centered, large serif headline]
  ["Human stories & ideas"]
  [Tagline — sans, muted]
  [Start reading — black CTA button]
─────────────────────────────────────────
Footer (About · Help · Terms · Privacy)
```

### Feed (Logged In)
```
Navbar
─────────────────────────────────────────
[Left Nav 240px]  [Feed — auto]  [Sidebar 300px]
  - Topics          - Story cards   - Staff picks
  - Following       - Pagination    - Recommended
  - Saved                           - Who to follow
─────────────────────────────────────────
```

### Article Page
```
Navbar
─────────────────────────────────────────
  [Article header — title, subtitle]
  [Author byline]
  [Hero image full-width]
  [Body — 680px centered serif]
  [Clap + share bar — sticky left on desktop]
─────────────────────────────────────────
  [Author bio section]
  [More from this author]
  [Recommended stories]
─────────────────────────────────────────
Footer
```

---

## 13. CSS Variables Reference

```css
:root {
  /* Colors */
  --color-bg: #FFFFFF;
  --color-surface: #F9F9F9;
  --color-border: #E6E6E6;
  --color-text-primary: #242424;
  --color-text-secondary: #6B6B6B;
  --color-text-muted: #B3B3B3;
  --color-accent: #1A8917;
  --color-tag-bg: #F2F2F2;

  /* Typography */
  --font-serif: charter, Georgia, "Times New Roman", serif;
  --font-display: gt-super, Georgia, serif;
  --font-sans: sohne, "Helvetica Neue", Arial, sans-serif;
  --font-mono: source-code-pro, "Courier New", monospace;

  --text-hero: 46px;
  --text-article: 20px;
  --text-feed-title: 18px;
  --text-ui: 14px;
  --text-small: 12px;

  --leading-body: 1.8;
  --leading-heading: 1.2;
  --leading-ui: 1.4;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* Layout */
  --max-article: 680px;
  --max-feed: 1192px;
  --navbar-height: 65px;

  /* Radius */
  --radius-sm: 4px;
  --radius-pill: 99px;

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
}
```

---

*Design system extracted from and try to follow the syle of Medium.com. Intended for AI reference to reproduce its editorial aesthetic accurately.*
