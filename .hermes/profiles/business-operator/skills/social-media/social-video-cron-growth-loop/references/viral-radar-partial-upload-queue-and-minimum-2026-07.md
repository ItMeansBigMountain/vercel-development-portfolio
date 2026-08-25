# Viral Radar partial uploads, queue semantics, and 5-clip minimum (2026-07)

Session learning from a user correction: Viral Radar should not treat `1/10`, `1/5`, or any partial source as success. The current user priority is **at least 5 public clips per selected/source video** when the source supports distinct clips, plus immediate blocker notification when it cannot.

## Correct interpretation

- A public report of `uploaded 1/N` is **PARTIAL/BLOCKED**, not OK.
- The upload queue is only for **rendered clips that failed at upload time**.
- An empty queue does **not** mean the source/video is complete.
- If the queue is empty after a partial result, identify why the missing clips were never queued:
  - source video was a YouTube Short / too short for 5 distinct clips;
  - source file was missing or download was blocked;
  - manifest planned only 1 clip;
  - render failed before upload;
  - duplicate guard skipped clips;
  - auth/quota prevented upload before rendered artifacts existed.

## Required future report shape

For Viral Radar cron/manual recovery reports, include concise bullets:

- uploaded URLs;
- per-source `uploaded_count/5`;
- `queue_count`;
- exact blocker(s);
- next action.

Final status rules:

- `OK` only when the selected/source video reached >=5 public uploads, or the task explicitly asked for fewer.
- `PARTIAL/BLOCKED` when any selected/source video is below 5 and the deficit is not resolved.
- If rendered uploads fail, verify the rendered MP4 + `.upload.json` metadata remain in `UPLOAD_QUEUE`; if not, fix queue preservation before claiming recovery.
- If no queue items exist because clips were never rendered/planned, say that explicitly instead of saying the queue is drained.

## Script/config expectation

The durable default minimum should be 5, not 10, unless the user explicitly requests 10+ for that run. Seed/planning, rendering, cron prompts, and final report logic should use the same minimum so the agent does not publish/report `1/10` or `1/5` as success.
