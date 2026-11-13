# agent craft

Seven skills for agents that do serious work. From **punnet**, primitive's open-source lab.

Works with Claude Code as a plugin, and with any agent that reads `SKILL.md` folders, including Codex and ChatGPT.

## Skills

**job-brief** turns a request into a brief an agent can build from without guessing: what's true when done, what must not change, which shared setup is off limits. The builder answers with a plan from the actual code before writing any.

**check-the-work** verifies "done", "fixed" and "live" against git, CI and the running system, never against the report. A job that ran zero tests has failed, and live means a real person can complete the whole path.

**runtime-pacing** gives every agent in a run the same clock, so a helper that joins at minute 4 knows it's minute 4. Agents explore early, converge as the target nears, and stop helpers they no longer need.
The one rule: *time may change strategy. It must never change authority or acceptance gates.* Includes a portable spec with regression tests (`references/portable-spec.md`).

**adversarial-verification** is for claims that matter: "fixed", "safe", "proved", "beats the benchmark". Instead of asking "can I confirm this?", it asks "what would make this false, and can I make that happen?" Blind reviewers each attack one weak joint, and nothing gets promoted while a lane is still out. Includes pressure scenarios (`TESTS.md`).

**ui-adversarial-testing** tries to break a changed web UI the way real people do: double-submits, Escape mid-flow, narrow screens, slow networks, empty states. Every check ends as PASS, FAIL or SKIP with evidence, and a skip is never a pass.

**expert-council** puts your work in front of five critics (Strategist, Analyst, Challenger, Builder, Audience Advocate), runs a short focused debate, and ends with one recommendation each critic signs off on, or an honest record of who didn't.

**retrieval-routing-patterns** is a checklist for AI search done properly: RAG, tool search across big catalogues, reranking, schema repair and caching. Its rules: discovery never grants authority, an empty search never becomes made-up context, repair loops are capped, and caches respect permissions. Comes with 14 acceptance tests and a map of the patterns in Spring AI (credited, Apache-2.0).

## Use

Ask your agent things like:
- "Write a job brief for adding CSV export."
- "Check the work: the agent says the login fix is live."
- "Apply runtime pacing, 10 minute target."
- "Adversarially verify this fix before we ship."
- "Try to break the new checkout form."
- "Run Expert Council on this plan."
- "Review our RAG pipeline with retrieval routing patterns."

## Install

Claude Code:

```
/plugin marketplace add Primitivelabai/primitive-open
/plugin install agent-craft@punnet
```

Anything else: copy a folder from `skills/` into your agent's skills directory.

## Licence

[Apache-2.0](../../LICENSE). Made in Perth by [primitive](https://primitiveai.com.au). https://punnet.dev
