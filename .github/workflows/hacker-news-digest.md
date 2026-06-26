---
emoji: 📰
name: Hacker News Digest
description: Generate the daily Hacker News tech digest for GitHub Pages.
on:
  workflow_dispatch:
  schedule:
    - cron: "13 6 * * *"
permissions:
  contents: read
strict: true
network:
  allowed:
    - defaults
    - github
    - node-cdns
    - news.ycombinator.com
    - hn.algolia.com
tools:
  web-fetch: {}
  bash: true
  edit: true
safe-outputs:
  create-pull-request:
    title-prefix: "Hacker News Digest:"
    branch-prefix: "hndigest/"
    labels: [automation]
    draft: false
    auto-merge: true
    if-no-changes: ignore
    protected-files: allowed
    allowed-files:
      - "digests/manifest.json"
      - "digests/*.md"
---

# Hacker News Digest

## Task

Generate the daily Hacker News digest content for this repository's static GitHub Pages site.

Use the workflow start date in Europe/Paris as the digest date and write `digests/YYYY-MM-DD.md`. Update `digests/manifest.json` so it remains a sorted ascending JSON array of every date with a digest.

Gather candidate stories from:

- `https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=40`
- `https://hn.algolia.com/api/v1/search?tags=show_hn&hitsPerPage=30`
- relevant `https://news.ycombinator.com/item?id=<id>` discussion pages when needed

Mimic the editorial scope of the reference site: "HN technical-interest", not narrow academic computer science. Prioritize AI/ML, software engineering, developer tools, programming languages, security, privacy, infrastructure, databases, operating systems, hardware, semiconductors, technical business shifts, and applied science when the HN discussion has a concrete computing, engineering, or research-method angle. Skip pure obituaries, generic politics, finance, culture, celebrity, and human-interest stories unless there is a direct technical angle in the story or HN discussion.

Do not invent stories, IDs, titles, repository links, source links, quotes, or metrics. Every `news.ycombinator.com/item?id=...` link and title must be copied from a fetched Algolia or Hacker News result. Prefer stories whose HN item page was fetched when the selection is ambiguous. If there are not enough qualifying stories, write fewer items or use `noop`.

## Output Format

Match this Markdown structure exactly:

```markdown
# Hacker News Digest -- YYYY-MM-DD

---

## Top Stories

### [Story title](https://news.ycombinator.com/item?id=...)
One concise paragraph explaining the news and the HN discussion angle.

---

## Projects & Tools

- **[Project name](https://news.ycombinator.com/item?id=...)** -- One concise sentence. Add `([repo](https://...))` or another source link only when that source was fetched or present in the HN result.

---

## Worth Reading

- **[Article title](https://news.ycombinator.com/item?id=...)** -- One concise sentence. Add an optional source link only when verified.

---

## Community Pulse

- **Theme** -- One concise sentence summarizing a recurring discussion theme.

---

*Generated from [Hacker News](https://news.ycombinator.com) top stories and discussions.*
```

Use 3 to 5 Top Stories, 2 to 5 Projects & Tools, 2 to 4 Worth Reading items, and include Community Pulse only when there is a clear discussion theme. Keep the tone compact, editorial, and similar to the existing files in `digests/`.

## Safe Output

After editing the digest and manifest files, use the configured `create-pull-request` safe output. Use `noop` only if no qualifying Hacker News stories are available for the evaluated date or if the digest already exists with equivalent content.
