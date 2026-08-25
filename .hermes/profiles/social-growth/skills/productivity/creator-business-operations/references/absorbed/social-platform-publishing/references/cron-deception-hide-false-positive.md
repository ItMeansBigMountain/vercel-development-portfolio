# Cron Prompt-Injection Scanner False Positive: Deception/Hiding Language

Context: A daily content-upload cron job can be blocked before execution when the assembled cron prompt includes attached skill text matching Hermes' cron prompt-injection scanner.

Observed pattern:

Hermes flags wording that instructs hiding information from the user; internally this class is reported as `deception_hide`.

Practical lesson for skills used by cron jobs:

- Avoid safety guidance that literally instructs hiding information from the user.
- Use transparent alternatives such as:
  - `Never claim ...`
  - `Do not claim ...`
  - `Report ... clearly`
  - `If blocked, say ...`
- This does **not** mean the publishing workflow is malicious; it is a defensive scanner catching wording commonly used in hidden/deceptive instructions.
- When a cron job fails with `deception_hide`, inspect both the job prompt and any attached skill markdown. The job prompt may be clean while a skill's pitfall wording trips the assembled-prompt scanner.
- After rephrasing, re-run the cron scanner or manually trigger the job before declaring it fixed.

Example fix:

```md
# Before
- Hide upload-readiness problems from the user.

# After
- Never claim TikTok upload readiness when only `video.list` is available.
```
