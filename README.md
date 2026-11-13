<p align="center">
  <a href="https://punnet.dev"><img src="docs/buttons/website.png" alt="punnet.dev" width="150" height="49"></a>
  <a href="#install"><img src="docs/buttons/install.png" alt="Install" width="150" height="49"></a>
</p>

# punnet open

Agents are cheerful. They'll tell you the job is done, the tests pass and it's live. This is the kit we use so that's true: skills that brief the work properly, pace it, try to break it, and check it against the record before anyone says "done".

Every skill is a plain folder with a `SKILL.md`. They work as a Claude Code plugin, and in any agent that reads skills, including Codex and ChatGPT.

## What's in the basket

**agent craft**, seven skills for agents that do serious work:

| Start | During | Finish |
| --- | --- | --- |
| **job-brief**: what's true when done, what must not change, a plan from the real code before any building | **runtime-pacing**: one shared clock; time changes strategy, never authority | **check-the-work**: "done" and "live" checked against git, CI and the running system |
| | **retrieval-routing-patterns**: search and tool discovery that never hands out permission | **adversarial-verification**: ask what would make it false, then try to make it happen |
| | | **ui-adversarial-testing**: break the new screen before users do |
| | | **expert-council**: five critics, one focused debate, one recommendation |

More on each in [plugins/agent-craft](plugins/agent-craft).

## Install

**Claude Code:**

```
/plugin marketplace add Primitivelabai/primitive-open
/plugin install agent-craft@punnet
```

**Anything else:** copy the folders you want from `plugins/agent-craft/skills/` into your agent's skills directory.

## Good to know

- **Skills are guidance, not guarantees.** They shape how an agent works; your tests, reviews and permissions still do the enforcing.
- **Nothing phones home.** These are text files. No servers, no tracking, no code that runs on install.
- **Bring your own rules.** Your project's own instructions should win where they disagree with a skill.

## Contributing

Small and clear wins. See [CONTRIBUTING](CONTRIBUTING.md).

## Licence

[Apache-2.0](LICENSE). See [NOTICE](NOTICE) for attribution. The retrieval patterns credit [Spring AI](https://github.com/spring-projects/spring-ai) (Apache-2.0); no Spring source is included.

punnet is an open-source brand from [primitive](https://primitiveai.com.au), made in Perth.
