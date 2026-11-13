# primitive-open

Agent skills and small tools from Primitive Labs, an Australian startup. Open source under the Apache License 2.0.

## What's here

| Plugin | What it does |
| --- | --- |
| [agent craft](plugins/agent-craft) | Eight skills for agents that do serious work: job briefs, runtime pacing, adversarial verification, UI adversarial testing, an expert council review, retrieval routing patterns, checking reported work, and an open-source scrub. |

## Install

Claude Code:

```
/plugin marketplace add Primitivelabai/primitive-open
/plugin install agent-craft@primitive-open
```

Other agents: every skill is a plain folder with a `SKILL.md`. Copy the ones you want into your agent's skills directory.

## Licence

Apache License 2.0. See `LICENSE`.
