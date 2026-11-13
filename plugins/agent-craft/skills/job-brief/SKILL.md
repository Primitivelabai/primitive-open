---
name: job-brief
description: Turn a request into a job brief another agent can build from without guessing, and have the builder answer with a plan grounded in the actual code before it starts. Use when delegating coding work to an agent or subagent, writing a ticket or issue for a builder, packing work for a parallel worker, or when a builder is about to start without a clear definition of done. Do not use for one-line fixes you will do yourself.
---

# Job Brief

Most failed agent jobs fail in the brief: a missing "don't touch this", a definition of done nobody can check, or a builder that planned from memory instead of the code.

## Part 1: Write the brief

Keep it to one screen. Every line should be checkable.

```
JOB        <short id>: <one-line outcome>
WHY        the user or business reason, one or two sentences
DONE WHEN  what is true when finished, as observable facts
           (a user can…, the test X passes, the endpoint returns…)
MUST NOT   what must not change: files, shared setup, public APIs,
           data, behaviour other features rely on
SCOPE      repository, branch to start from, area of the code
TESTS      which tests must pass, and which new tests are expected
LIMITS     authority: may push to a branch / open a PR / never merge,
           never deploy, never touch production data or secrets
RISK       normal | serious (security, money, accounts, data, hosting)
HANDBACK   what to return: branch, commit, CI run, notes on anything unfinished
```

Rules for a good brief:

- **Name the shared setup the builder may not change.** Test helpers, routing, global config, and shared fixtures are where "my fix" quietly breaks someone else's feature.
- **Write "done" as evidence, not effort.** "Refactored X" is not done; "X's tests pass and the page loads in under 1s" is.
- **One job, one outcome.** If the brief needs an "and also", it is two jobs.
- **Give absolute paths and exact names.** Relative paths and "the usual place" get lost between agents.
- **Say what risk tier it is.** Serious work gets a cross-check from a different reviewer before merge; experiments and unreleased work do not need the ceremony.

### Check the brief before sending

Read it as the builder will, or have a second agent do so read-only. Look for:

- contradictions between DONE WHEN and MUST NOT;
- a test that cannot pass without breaking a MUST NOT;
- missing authority (who can merge? may it add dependencies?);
- assumptions about files or APIs that do not exist.

Fix the brief, not the build. A contradiction found now costs a minute; found in review it costs a round.

## Part 2: Builder plans from the code

Before writing any code, the builder replies with a plan grounded in the repository as it is:

```
PLAN for <job id>
FILES      exact files to change, found by searching the repo (not from memory)
CALLERS    other code that uses what changes, and how it stays working
TESTS      existing tests to run, new tests to add, and how each fails today
MUST NOT   how the plan avoids each MUST NOT item
UNKNOWNS   anything in the brief that does not match the code
```

- The file list comes from a repo-wide search (`grep`, `rg`, symbol search), so callers in other packages are not missed.
- New tests should fail first for the right reason (an assertion, not a typo or a broken harness).
- If the code contradicts the brief, the builder stops and asks. It does not quietly pick one.

The person who wrote the brief reads the plan and says go, or fixes the brief.

## Part 3: Build and hand back

- Run the tests for what changed locally before pushing; let CI run the rest.
- Push to a branch, never straight to the main branch.
- Hand back exactly what HANDBACK asked for, and list anything unfinished by name.

Then verify the handback against the record, not the message (see `check-the-work`).
