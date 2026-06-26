# Hacker News Digest

A GitHub Pages static site that publishes a daily, AI-generated digest of the hottest
Hacker News tech / computer-science stories, tools, and discussions. It mirrors the
layout of the reference site (calendar sidebar plus Markdown-rendered digest pane) and
is themed with the Clawpilot design tokens.

## How it works

The site is fully static. There is no build step and no backend:

- **`index.html`** - single-page app. Renders a month calendar, highlights days that have
  a digest, and loads the selected day's Markdown with [marked](https://github.com/markedjs/marked).
  Colors come entirely from Clawpilot `--cp-*` CSS variables, with light/dark detection via
  the `scoutTheme` query param or `prefers-color-scheme`.
- **`digests/manifest.json`** - a JSON array of available digest dates (`YYYY-MM-DD`).
  The calendar reads this to know which days are clickable.
- **`digests/YYYY-MM-DD.md`** - one Markdown file per day. The app fetches and renders it.
- **`.nojekyll`** - disables Jekyll so the raw `.md` files are served verbatim.

## Digest format

Each digest is Markdown with a stable shape (sections are optional and counts vary per day):

```
# Hacker News Digest -- YYYY-MM-DD
---
## Top Stories          (3–5 items: ### [Title](hn-link) + 1 short summary paragraph)
## Projects & Tools     (bulleted: **[Name](hn-link)** -- one-liner, optional (repo) link)
## Worth Reading        (bulleted links + one-liners)
## Community Pulse       (optional: Ask HN / discussion highlights)
---
*Generated from [Hacker News](https://news.ycombinator.com) top stories and discussions.*
```

## Adding a new digest

1. Write `digests/YYYY-MM-DD.md` following the format above.
2. Append the date to `digests/manifest.json` (keep it sorted).

## Automation

The scheduled generator lives in `.github/workflows/hacker-news-digest.md` and is
compiled to `.github/workflows/hacker-news-digest.lock.yml`. It runs every day at
08:13 Europe/Paris during daylight saving time and can also be triggered manually with:

```bash
gh aw run hacker-news-digest
```

The agent fetches Hacker News front-page and Show HN stories, summarizes the technical
topics into the Markdown format above, updates the manifest, and opens an auto-mergeable
pull request scoped to `digests/**`.
