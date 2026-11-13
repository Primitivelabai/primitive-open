---
name: runtime-pacing
description: Apply shared run-time awareness to non-trivial agent or multi-agent work so executors pace toward an optional soft latency target without weakening authority, required review, safety, verification, or evidence. Use when a run has elapsed-time or latency pressure, when helpers join an existing run, when an orchestrator asks to converge or finish efficiently, or when a packet says "Apply RUNTIME-PACING". Do not use it as a replacement for the host runtime, router, scheduler, lease system, heartbeat, hard timeout, or approval gates.
---

# Runtime Pacing

Use a shared run clock to make agents aware of how mature the whole job is. Change strategy as time advances, but never trade away authority or mandatory acceptance gates.

## Core invariant

> Time may change strategy. It must never change authority or acceptance gates.

Treat this Skill as pacing guidance only. Never treat it as the clock, source of truth, runtime, router, scheduler, lease issuer, evidence store, or cancellation mechanism.

## Procedure

1. **Establish the run boundary.** Determine whether this executor is starting a new independent run or joining an existing one. Children and helpers in the same run inherit the parent's original run start.
2. **Read canonical state.** Use host-provided elapsed time, optional soft target, hard limit, phase, worker state, authority/lease state, and required gates. Never invent missing values.
3. **Project compact state.** Prefer a tiny volatile tail block such as `[run elapsed=436s target=600s phase=verify]`. Omit fields that are not known.
4. **Refresh at synchronisation points.** Refresh before model turns where practical, after client-side tool results, when a helper joins, and after target/phase/cancellation/topology changes.
5. **Pace by maturity.**
   - Early: investigate material uncertainty and parallelise genuinely independent work.
   - Maturing: stop duplicate searching, repeated rereading, speculative branches, and unnecessary polish.
   - Near target: prioritise the requested outcome, mandatory correctness/safety, essential verification, a recoverable checkpoint, then residual uncertainty.
   - Beyond target: do not fake completion or skip gates. Reach the safest useful checkpoint and record the overrun when possible.
6. **Separate soft targets from hard enforcement.** A soft target informs strategy. A hard limit must be enforced by the host runtime or deterministic cancellation mechanism, never by prompt wording alone.
7. **Converge multi-agent work.** Stop or cancel helpers whose output is no longer needed. Delegation must not reset elapsed time, target, authority, budget, or required review.
8. **Leave evidence.** Where the host supports receipts, record timing, target/overrun, worker convergence, completion state, and verification state.

## Hard constraints

Urgency never permits the executor to:

- widen authority or a lease;
- write outside reserved scope;
- bypass approval or independent review;
- merge, deploy, publish, pay, send, or mutate consequential state without authority;
- skip mandatory security, correctness, or test gates;
- convert assumptions into evidence;
- create a duplicate runtime, router, scheduler, heartbeat, or truth store because the canonical path appears slower.

If pacing conflicts with authority or a required gate, authority and the gate win.

## Missing state

If trustworthy shared timing is unavailable, do not fabricate it. Continue under normal authority and verification rules and treat RUNTIME-PACING as UNAVAILABLE or PARTIAL rather than manufacturing a clock.

## Adoption discipline

Do not assume faster is better. When evaluating pacing changes, compare paced and unpaced runs on representative work using wall-clock duration, tool calls, cost where available, completion rate, mandatory-test pass rate, reviewer findings, quality/outcome score, and target overruns.

## Detailed reference

Read `references/portable-spec.md` when implementing, reviewing, benchmarking, or adapting RUNTIME-PACING to a runtime. It contains the complete portable contract, examples, and regression tests.
