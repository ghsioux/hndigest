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

Editorial scope: "HN technical-interest", not narrow academic computer science. Prioritize AI/ML, software engineering, developer tools, programming languages, security, privacy, infrastructure, databases, operating systems, hardware, semiconductors, technical business shifts, and applied science when the HN discussion has a concrete computing, engineering, or research-method angle. Skip pure obituaries, generic politics, finance, culture, celebrity, and human-interest stories unless there is a direct technical angle in the story or HN discussion.

Do not invent stories, IDs, titles, repository links, source links, quotes, or metrics. Every `news.ycombinator.com/item?id=...` link and title must be copied from a fetched Algolia or Hacker News result. Prefer stories whose HN item page was fetched when the selection is ambiguous. If there are not enough qualifying stories, write fewer items or use `noop`.

## Section Definitions

Place each story in the right section:

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

Per-digest item counts, matching the observed distribution of the corpus: 3 to 5 Top Stories (usually 3 to 4), 1 to 4 Projects & Tools (usually 2), 1 to 3 Worth Reading items (usually 2), and 0 to 2 Community Pulse items. Community Pulse appears on only about half of the days: include it only when one or two genuine discussion threads stand out, and omit the whole section otherwise rather than inventing a theme. A whole digest runs roughly 340 to 610 words. Keep the tone compact, editorial, and consistent with the existing files in `digests/`.

## Writing Style

Write in the established voice of this digest. The rules below describe it; the example phrasings are illustrative only and you must never restrict yourself to them. Vary wording naturally and invent your own phrasings as each story dictates.

- **Lead with the fact, not the forum.** Every Top Stories paragraph must open with an objective summary of what actually happened (the release, incident, result, or announcement). Never open with a forum-first phrase such as "The HN thread...", "The HN discussion...", "On Hacker News...", or "Users discussed...".
- **Carry the community angle in most, but not all, Top Stories.** About two out of three Top Stories should fold in what readers actually argued; roughly one in three is a clean factual and technical summary with no community mention at all. Do not force a reaction onto every story. When you do include it, surface the substance: the specific technical objection, the tension readers fixated on, the trade-off, the correction, or the comparison to prior work, not the bare fact that people commented. A colon is often a natural way to introduce that substance (for example, "...: many engineers see X, while others argue Y").
- **Vary how the community angle is expressed.** Do not introduce the reaction the same way twice in a row. Vary the verb, the placement (sentence two, sentence three, or woven into the explanation), and the frame (skepticism, trade-off, feasibility, precedent, security, economics, usability). Recurring frames like "The HN thread...", "The HN discussion...", "Commenters note...", "The community is split...", "The consensus is..." are part of this voice and may be reused across the digest; they are normal, not banned. The goal is natural variety, not avoidance of any particular phrase. These examples are illustrative; do not limit yourself to them.
- **Use the "two camps" framing sometimes, not always.** When a thread is genuinely divided, "some... others..." or "while... others..." is a signature move, but it should appear in only a minority of stories, not most.
- **Name the collective tenor with a precise, reason-bearing word** (skeptical, impressed, outraged, unconvinced, frustrated) rather than a vague "people reacted", and back it with the reason. When one short comment captures the mood, you may quote it briefly, or name a notable person who appeared in the thread.
- **Do not invent consensus.** If the reaction is fragmented, present it as a debate or a set of open questions, never as a fabricated unanimous verdict.
- **Attribute opinions to the crowd**, do not editorialize in your own voice.
- **Length:** Top Stories are one tight paragraph of roughly 40 to 70 words (2 to 4 sentences). No filler.
- **Minor sections are pure curation.** Projects & Tools and Worth Reading items are single noun-phrase fragments of roughly 25 to 45 words (vary the openings freely). They must NOT mention Hacker News, the thread, commenters, or community reaction at all.
- **Community Pulse** is the one bulleted section where the social split or memorable argument is the point; summarize the debate, not just the topic.
- **No em dashes.** Never output the em dash character (U+2014, the long dash) anywhere in the digest, including summaries, headings, and copied titles. Use commas, colons, parentheses, semicolons, or separate sentences instead. Plain hyphens, numeric ranges like "40 to 70", and the required `--` bullet separator (`- **[Title](url)** -- summary`) are allowed and must be kept. Before finalizing, scan the whole digest and replace every em dash; there must be zero em dash characters in the output.
- Editorial, technically literate, lightly sardonic when earned; never a joke per line.

## Safe Output

After editing the digest and manifest files, use the configured `create-pull-request` safe output. Use `noop` only if no qualifying Hacker News stories are available for the evaluated date or if the digest already exists with equivalent content.
