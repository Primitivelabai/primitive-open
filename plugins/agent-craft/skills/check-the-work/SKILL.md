---
name: check-the-work
description: Verify work that another agent, subagent, contractor or teammate reports as done, fixed, merged, deployed or live, using the primary record (git, CI, the running system) instead of their report. Use when accepting delegated work, before telling someone a job is finished, when a status update says "done" or "live", when an agent has gone quiet, or when deciding whether to merge. Do not use to re-review code quality in depth; use a code review or adversarial-verification for that.
---

# Check the Work

Agents are cheerful. They will tell you it is finished. Check the record, not the report.

## Core rules

- **The commit history does not exaggerate.** Read git, CI and the running system. A summary, acknowledgement or status message is a claim, not evidence.
- **A job that ran zero tests has failed**, whatever it says.
- **"Live" means a real person can complete the whole path** in production. A deployed screen with nothing behind it is not live.
- **Never repeat a claim you have not checked.** If you could not check it, say "reported, not verified".

## 1. Pin the claim

Write the exact claim being made, in one line each:

- what changed;
- where (repository, branch, commit, environment);
- what is now supposedly true for the user;
- what evidence was offered.

Vague claims ("all sorted", "should be working now") get pinned to something checkable first, or sent back.

## 2. Check the primary record

| Claim | Check |
| --- | --- |
| "Pushed" / "committed" | The branch exists on the remote; the commit is there; its time and author make sense; the diff touches what the job was about. |
| "Tests pass" | A CI run on **the exact head commit**, not an earlier one. Tests actually ran (count above zero), nothing was skipped or weakened to get green. |
| "Fixed" | The original failing case now passes, and it is in a test so it stays fixed. |
| "Merged" | The merge commit is on the target branch, and the merged tree was tested. A merge of two separately tested branches is a new tree. |
| "Deployed" | The running version or image matches the commit. Health checks pass. |
| "Live" | Walk the real end-to-end path a customer would take, or have it walked, in production. List every piece of that path and its state. |
| "Nothing else changed" | Compare the diff against the job's "must not change" list. |

Prefer looking yourself over asking the worker to look again.

## 3. Watch for the usual gaps

- Work on a local branch that was never pushed.
- CI green on an older commit, red or missing on the latest.
- Tests that pass because they no longer test anything (assertions removed, cases skipped, timeouts raised).
- Front end shipped, back end or integration missing.
- A "done" with no commit for hours, or a commit that touches unrelated files.
- Fixes that changed shared setup the job was told not to touch.
- Reports written before the work finished.

## 4. Quiet workers

If someone has reported progress but the record shows no new commits for a long stretch, ask one direct question about the specific missing piece, with the evidence: "No commits on `branch` since 10:40. Where is the change to X?" Not "how's it going?".

## 5. Report

```
CHECK: VERIFIED | PARTLY VERIFIED | NOT VERIFIED | CONTRADICTED

CLAIM        exactly what was claimed
RECORD       what git, CI and the running system show (links, commit ids, run ids)
MATCHES      parts of the claim the record supports
GAPS         parts unverified or contradicted, named piece by piece
NEXT         the one action that closes the biggest gap
```

When handing on a status, list unfinished pieces by name. "Mostly done" hides the piece that matters.
