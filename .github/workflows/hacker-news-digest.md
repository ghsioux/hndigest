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

## Section Definitions

Place each story in the right section. These definitions match the reference site's historical conventions:

- **Top Stories** -- the day's lead, highest-salience HN front-page news: major releases, security incidents, business shocks, infrastructure events, and significant breakthroughs. Major applied-science or research breakthroughs with a computing/ML/engineering core belong here (e.g. an ML-decoded ancient scroll, an AI-assisted math proof, a notable medical-AI result), not in Worth Reading. Use a `###` heading plus one paragraph.
- **Projects & Tools** -- concrete things to use or inspect: Show HN launches, OSS releases, libraries, developer tools, ports, and demos. Bulleted; append a `([repo](https://...))` or `([domain.com](https://...))` secondary link when that source was fetched or present in the HN result.
- **Worth Reading** -- secondary but intellectually rich items: essays, explainers, deep-dives, post-mortems, opinion, and technical curiosities that are worth time but are not the day's lead news. Bulleted; use only the HN item link (no secondary links).
- **Community Pulse** -- discussion-centric threads: Ask HN, Tell HN, debates, sentiment shifts, and recurring community themes. Each item MUST be a bullet linking to a specific HN discussion thread, exactly like the other bulleted sections: `- **[Title](https://news.ycombinator.com/item?id=...)** -- summary`. Never write link-less thematic bullets.

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

- **[Project name](https://news.ycombinator.com/item?id=...)** -- One concise sentence. Add `([repo](https://...))` or `([domain.com](https://...))` only when that source was fetched or present in the HN result.

---

## Worth Reading

- **[Article title](https://news.ycombinator.com/item?id=...)** -- One concise sentence. Use only the HN item link.

---

## Community Pulse

- **[Discussion thread title](https://news.ycombinator.com/item?id=...)** -- One concise sentence summarizing the discussion and community reaction.

---

*Generated from [Hacker News](https://news.ycombinator.com) top stories and discussions.*
```

Use 3 to 5 Top Stories, 2 to 4 Projects & Tools, 2 to 3 Worth Reading items, and 0 to 2 Community Pulse items. Include Community Pulse only when one or two genuine discussion threads stand out (it is present in roughly half of the reference digests); omit the whole section otherwise rather than inventing a theme. Keep the tone compact, editorial, and similar to the existing files in `digests/`.

## Safe Output

After editing the digest and manifest files, use the configured `create-pull-request` safe output. Use `noop` only if no qualifying Hacker News stories are available for the evaluated date or if the digest already exists with equivalent content.
