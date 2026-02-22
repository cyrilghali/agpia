# Copilot Code Review Instructions

## Comment classification

Every review comment must be prefixed with its type:

- **`[BLOCKING]`** — Must be fixed before merge. Correctness bugs, broken functionality, security issues, data loss risk.
- **`[NITPICK]`** — Minor style or consistency issue. Author may fix or ignore at their discretion; never blocks merge.
- **`[SUGGESTION]`** — Improvement worth considering (readability, performance, better API). Non-blocking; author decides.
- **`[QUESTION]`** — Seeking understanding, not requesting a change. Author should clarify or explain.
- **`[PRAISE]`** — Acknowledge good work explicitly. Helps authors know what to keep doing.

## Review philosophy (Google guidelines)

Follow [Google's code review guidelines](https://google.github.io/eng-practices/review/):

- **The primary goal is code health.** Approve changes that improve the codebase even if they are not perfect.
- **Do not request changes purely on personal preference.** Prefer established conventions in the codebase.
- **Be specific.** Point to the exact line, explain why it matters, and suggest a concrete fix.
- **Be kind.** Comment on code, not the author. Use "this function" not "you wrote this wrong".
- **Explain the why.** A comment without reasoning is harder to act on than one with context.
- **Distinguish facts from opinions.** Use "I think", "consider", "prefer" for subjective points.
- **Do not pile on.** If a pattern repeats, mention it once and note it applies elsewhere.

## What to look for

Review in this order of priority:

1. **Correctness** — Does the code do what it claims? Are edge cases handled?
2. **Security** — Any injection, XSS, or data exposure risk?
3. **Consistency** — Does it follow the conventions already in the codebase?
4. **Readability** — Is the intent clear without needing comments to explain it?
5. **Performance** — Any obvious inefficiency worth calling out?
6. **Style** — Naming, formatting, brevity. Only raise if it meaningfully affects readability.

## Project-specific conventions

This is a static HTML Coptic prayer app (Agpeya). Key conventions:

- All alleluia text uses `<span class="alleluia">ALLELUIA.</span>` — never `<em>` or plain text.
- Every psalm-ending ALLELUIA must be **inline** at the end of the last `<div class="psalm-verse">`, followed by a `<a class="jump-gospel-btn" href="#gospel">` button on the next line, before `</section>`.
- Standalone alleluia responses (between psalm verses, in `<div class="prayer-text">`) do **not** get a gospel button.
- The service worker cache name in `sw.js` is auto-updated by the pre-commit hook — do not change it manually.
- `en/` is the source of truth for HTML structure. Other locales (`fr-lsg/`, `ar/`, `fr-unofficial/`) mirror it.
- Shared logic goes in `agpeya.js`. No inline `<script>` tags in HTML files.
- Shared styles go in `agpeya-style.css`. No inline `style` attributes.
