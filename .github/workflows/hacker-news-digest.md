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

- **Top Stories** -- the day's lead, highest-salience HN front-page news, such as major releases, security incidents, business shocks, infrastructure events, and significant breakthroughs (these categories are illustrative, not exhaustive). Major applied-science or research breakthroughs with a computing/ML/engineering core belong here (e.g. an ML-decoded ancient scroll, an AI-assisted math proof, a notable medical-AI result), not in Worth Reading. Use a `###` heading plus one paragraph.
- **Projects & Tools** -- concrete things to use or inspect, such as Show HN launches, OSS releases, libraries, developer tools, ports, and demos. Bulleted; append a `([repo](https://...))` or `([domain.com](https://...))` secondary link when that source was fetched or present in the HN result.
- **Worth Reading** -- secondary but intellectually rich items, such as essays, explainers, deep-dives, post-mortems, opinion, and technical curiosities that are worth time but are not the day's lead news. Bulleted; use only the HN item link (no secondary links).
- **Community Pulse** -- discussion-centric threads, such as Ask HN, Tell HN, debates, sentiment shifts, and recurring community themes. Each item MUST be a bullet linking to a specific HN discussion thread, exactly like the other bulleted sections: `- **[Title](https://news.ycombinator.com/item?id=...)** -- summary`. Never write link-less thematic bullets.

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

## Writing Style

The reference site has a distinctive voice. Follow these rules so the prose reads like it and never feels formulaic:

- **Lead with the fact, not the forum.** Every Top Stories paragraph MUST open with an objective summary of what actually happened (the release, incident, result, or announcement). Never open with a forum-first phrase — examples to avoid include "The HN thread...", "The HN discussion...", "On Hacker News...", "Users discussed..." and any similar variant.
- **Fold the reaction in later.** When you mention the community response, do it in the second or third sentence, after the facts are established.
- **Kill the "HN thread" monoculture.** Within a single digest, do not introduce the community reaction the same way twice; vary the wording naturally. Examples of varied forms (illustrative, not an exhaustive or required list — invent your own as the story dictates): "Commenters note...", "The community is split...", "Critics argue...", "Skeptics point out...", "Engineers in the thread...", "The consensus is...", "Users report...", "The comments highlight...". Do not limit yourself to these phrasings. The exact phrase "The HN thread" or "The HN discussion" may appear at most once per digest, if at all.
- **Roughly one Top Story in four should mention no community meta at all** — just summarize the news and the substance of the technical debate as fact.
- **Attribute opinions to the crowd**, do not editorialize in your own voice (report what commenters debate, not your own verdict).
- **Capture the angle HN fixated on** — the pragmatic catch, the trade-off, the edge case — not a generic "people reacted".
- **Length:** Top Stories are one tight paragraph of 40-70 words (2-4 sentences). No filler.
- **Minor sections are pure curation.** Projects & Tools and Worth Reading items are single noun-phrase fragments of roughly 20-40 words (e.g. openings like "A tiny...", "An open-source...", "A technical breakdown of..." — illustrative only, vary them freely). They must NOT mention Hacker News, the thread, commenters, or community reaction at all.
- **Community Pulse** is the one bulleted section where the social split or memorable argument is the point; summarize the debate, not just the topic.
- Editorial, technically literate, lightly sardonic when earned — never a joke per line.

## Safe Output

After editing the digest and manifest files, use the configured `create-pull-request` safe output. Use `noop` only if no qualifying Hacker News stories are available for the evaluated date or if the digest already exists with equivalent content.
