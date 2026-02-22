# Copilot Code Review Instructions

## Comment classification

Every review comment must be prefixed with its type:

- **`[BLOCKING]`** — Must be fixed before merge. Correctness bugs, broken functionality, security issues, data loss risk.
- **`[NITPICK]`** — Minor style or consistency issue. Author may fix or ignore at their discretion; never blocks merge.
- **`[SUGGESTION]`** — Improvement worth considering (readability, performance, better API). Non-blocking; author decides.
- **`[QUESTION]`** — Seeking understanding, not requesting a change. Author should clarify or explain.
- **`[PRAISE]`** — Acknowledge good work explicitly. Helps authors know what to keep doing.

Review in this order of priority:

1. **Correctness** — Does the code do what it claims? Are edge cases handled?
2. **Security** — Any injection, XSS, or data exposure risk?
3. **Consistency** — Does it follow the conventions already in the codebase?
4. **Readability** — Is the intent clear without needing comments to explain it?
5. **Performance** — Any obvious inefficiency worth calling out?
6. **Style** — Naming, formatting, brevity. Only raise if it meaningfully affects readability.
