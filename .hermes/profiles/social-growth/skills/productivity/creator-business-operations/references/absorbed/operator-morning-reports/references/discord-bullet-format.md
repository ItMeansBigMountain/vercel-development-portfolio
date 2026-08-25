# Discord-readable morning report formatting

Session lesson: Markdown tables rendered poorly in Discord and looked like code. The user explicitly asked to either make tables presentable in Discord or switch to simplified bullets.

Use this instead of Markdown tables:

```md
**Search + Social Pulse**
- **Signal name** — Where: Google/X/TikTok/etc. | Why: short reason | Move/Ignore: short action

**AI + Coding News**
- **News item** — Impact: short practical implication | Leverage move: one action

**Trend Radar**
- **Trend** — Velocity: High/Med/Low | Spread: platforms | Money: High/Med/Low | Saturation: High/Med/Low | Capability: what to strengthen | Kill/Scale: condition
```

Rules:
- Optimize for Discord on iPhone: short sections, visible bold labels, bullets separated by blank lines, and minimal nesting.
- No Markdown tables.
- No code blocks in the delivered report; the code block above is only an internal example.
- Avoid long paragraphs; keep most bullets under ~120 characters where possible.
- Use **bold section headers**, `-` bullets, and occasional emoji only when it improves scanning; do not over-decorate.
- Put the most important noun first in each bullet so mobile notification/preview text is useful.
- Prefer “what changed / why it matters / what to do” in one compact line over explanatory paragraphs.
- If a section has many items, show only the top signals and hide/suppress low-signal routine items instead of making the user scroll.
- Keep each bullet to one line when possible.
- Prefer 3–5 high-signal items over comprehensive coverage.
- If source data is unavailable, say `not verified` briefly rather than expanding into caveats.
