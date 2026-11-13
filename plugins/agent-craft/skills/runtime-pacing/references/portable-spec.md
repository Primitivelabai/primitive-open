# Portable Procedure Specification: RUNTIME-PACING

## 1. Identity

- **ID:** runtime-pacing
- **Name:** RUNTIME-PACING
- **Purpose:** Expose shared run elapsed time and optional soft latency targets to participating agents so they can converge earlier without weakening authority, verification, safety, or evidence requirements.
- **Version/date:** 1.0 / 2026-10-05
- **Required capabilities:** monotonic or equivalent run timing; a way to provide compact dynamic context to an executor; optional multi-agent coordination; optional deterministic cancellation/timeout enforcement; optional execution receipts.

## 2. Scope and trigger

### Use when

Use this procedure when one or more agents are performing a non-trivial task where thoroughness and wall-clock speed can trade off, especially when:

- a lead delegates work to helpers;
- a run has a soft latency target;
- late-spawned helpers need to understand how mature the overall run already is;
- repeated exploration or unnecessary polish may create avoidable tail latency;
- the host runtime can refresh dynamic state between model turns or tool calls;
- an orchestrator wants a compact shorthand such as `Apply RUNTIME-PACING`.

### Do not use when

Do not use this procedure to:

- invent or replace the host runtime, router, scheduler, lease system, authority system, evidence store, or truth store;
- enforce a hard timeout using prompt text alone;
- override a deterministic deadline/cancellation mechanism;
- weaken required approval, review, security, test, or evidence gates;
- route models solely because they are faster when canonical routing policy says otherwise;
- replace a heartbeat/liveness protocol;
- pressure an executor on a trivial task where there is no meaningful strategy/latency trade-off.

## 3. Evidence and authority boundary

### Evidence boundary

**Background pattern (shared-clock latency pressure):**

- A team can use one shared clock whose start belongs to the whole run rather than to each helper.
- A late-spawned helper can be shown team elapsed time on its first turn.
- A compact clock line can be added before model calls.
- A soft latency budget can be shown alongside elapsed time without itself enforcing termination.
- Client-side tool boundaries provide natural opportunities to refresh time context.
- This pattern demonstrates wiring and pacing behaviour, not a validated universal quality improvement.

**Host architecture assumption:**

- A host runtime usually already owns execution state, budgets, routing, permissions, and receipts.
- Portable pacing guidance must not create a duplicate runtime or routing authority.

**Design decision:**

- The best portable abstraction is a compact run-state projection plus pacing rules rather than a new runtime subsystem.
- The rule "Time may change strategy. It must never change authority or acceptance gates." is a design rule derived from these constraints.

### Execution-time verification

The executor must obtain or verify, from the host runtime where applicable:

- whether the task belongs to an existing run or starts a new run;
- the canonical run start time;
- any current soft target;
- any hard deadline or cancellation policy;
- authority/lease scope;
- required verification and approval gates;
- whether helpers share the same run identity.

### Authority boundary

RUNTIME-PACING does not grant permission to write, merge, deploy, publish, pay, send, expand scope, change routing authority, or skip reviews/tests.

The executor must never claim that a run is correct, safe, approved, merged, deployed, or complete merely because it finished within its latency target.

## 4. Inputs

| Input | Required? | Accepted form | Purpose | Missing/invalid handling |
| --- | --- | --- | --- | --- |
| run_id | Recommended | stable run/task identifier | Distinguishes shared-run state from a new independent run | If unavailable, use the host's current task/session identity without inventing a durable ID |
| run_started_at or monotonic start | Required for timing | monotonic timestamp or equivalent | Establishes shared elapsed time | If unavailable, do not fabricate elapsed time; mark pacing clock unavailable |
| current_time | Required for timing | monotonic/current timestamp | Computes elapsed time | If unavailable, do not show a numeric elapsed value |
| soft_target | Optional | duration | Gives the executor a pacing target | Omit target field when absent; never invent a target |
| hard_limit | Optional | duration or deterministic runtime policy | Defines enforced cutoff/cancellation | Keep separate from soft target; if unknown, do not imply one exists |
| phase | Optional | bounded host-defined state such as explore/build/verify | Helps the executor choose convergence behaviour | Omit when the host has no canonical phase |
| worker_state | Optional | active/completed/cancelled counts or equivalent | Helps multi-agent convergence | Omit if unavailable or unreliable |
| authority_context | Required when actions can mutate state | lease, permission set, approval policy, or equivalent | Prevents urgency from widening authority | If unavailable, fail closed for consequential actions |
| required_gates | Required when the task has mandatory checks | test/review/security/approval requirements | Protects acceptance quality | If unclear, preserve known mandatory gates and mark unknowns rather than deleting them |

Freshness: elapsed time, phase, worker state, cancellation state, and authority state are volatile. Refresh them at the latest practical synchronisation point before consequential decisions.

## 5. Outputs

### Output A: Compact run-state projection

**Format:** one compact text block or equivalent structured context.

Minimum:

```
[run elapsed=436s]
```

With target:

```
[run elapsed=436s target=600s]
```

Optional canonical fields:

```
[run elapsed=436s target=600s phase=verify workers=2]
```

**Quality criteria:**

- values come from canonical host state;
- the projection remains compact;
- absent facts are omitted rather than guessed;
- volatile state is refreshed at useful boundaries;
- the projection does not contain new authority claims.

### Output B: Pacing behaviour

The executor changes strategy according to run maturity while preserving all hard constraints.

### Output C: Optional receipt additions

When the host supports execution receipts, include available timing and convergence facts such as elapsed duration, target, overrun status, helper counts, completion state, and verification state.

### Minimum viable output

If the host cannot provide live timing, the executor must not fabricate it. The minimum viable result is a statement that RUNTIME-PACING is requested but live clock state is unavailable, followed by normal execution under existing authority and verification rules.

### Completion status vocabulary

- `APPLIED`: shared run state was available and pacing behaviour was used.
- `PARTIAL`: only some run-state fields were available; missing values were not invented.
- `UNAVAILABLE`: no trustworthy shared clock/state could be supplied.
- `BLOCKED`: authority or required gates prevent safe continuation.

## 6. Procedure

### Phase 1: Establish the run boundary

1. Determine whether the executor is joining an existing run or starting a new independent run.
2. Reuse the existing run start for all children/helpers participating in that run.
3. Do not reset elapsed time when delegating.
4. Verify authority and required gates separately from pacing state.

**Stop condition:** If consequential action is requested but authority is unavailable or invalid, stop or escalate according to the host authority model. Timing pressure cannot cure missing authority.

### Phase 2: Build the run-state projection

1. Compute elapsed time from the canonical run start using a monotonic or equivalent trustworthy clock.
2. Add the soft target only if one was explicitly configured.
3. Add phase or worker information only when canonical and useful.
4. Keep the representation compact.
5. Place volatile state at the latest practical context boundary rather than rewriting stable instructions.

### Phase 3: Refresh at synchronisation points

Refresh the projection:

1. before the first model turn;
2. before later model turns where practical;
3. after client-side tool results return;
4. when a helper is spawned into the run;
5. after target/phase/cancellation/topology changes.

If the host performs long server-side operations without returning control, continue from the last known projection until the host can refresh state again. Do not pretend the clock stayed fresh during the opaque period.

### Phase 4: Apply pacing strategy

#### Early run

- investigate material uncertainty;
- delegate genuinely independent work when useful;
- gather enough evidence for correctness.

#### Maturing run

- reduce duplicate searching and rereading;
- reuse evidence already collected;
- avoid unnecessary stylistic polish;
- stop speculative branches whose expected value has fallen.

#### Near target

Prioritise:

1. core requested outcome;
2. mandatory safety/correctness requirements;
3. essential verification/tests;
4. durable checkpoint/handoff;
5. residual uncertainty report.

Cancel or stop helpers no longer needed for the answer.

#### Beyond target

- do not fake completion;
- do not skip mandatory gates;
- reach the safest useful checkpoint available;
- record the overrun and its reason where receipts/logging exist.

### Phase 5: Separate soft pacing from hard enforcement

1. Treat `soft_target` as information for strategy.
2. Treat `hard_limit` as a deterministic host-runtime policy.
3. Do not encode a hard timeout solely as natural-language urgency.
4. If hard cancellation occurs, preserve whatever checkpoint/evidence the host permits and report incomplete state accurately.

### Phase 6: Record evidence

Where supported, record:

```yaml
run_started_at:
run_finished_at:
elapsed_ms:
soft_target_ms:
hard_limit_ms:
target_exceeded:
workers_spawned:
workers_cancelled_after_convergence:
completion_state:
verification_state:
```

Do not use the receipt to justify an action that lacked authority when it happened.

### Phase 7: Evaluate before broad adoption

For representative workloads, compare paced and unpaced execution across:

- wall-clock duration;
- tool calls;
- cost where available;
- completion rate;
- mandatory-test pass rate;
- reviewer findings;
- outcome/quality score;
- target-overrun frequency and magnitude.

Promote defaults only when the quality/latency trade-off is acceptable for the workload.

## 7. Constraints and principles

1. **Shared clock:** all agents in one run inherit the same run start. **Hard.** Prevents late helpers from acting as if they have a fresh time budget.
2. **No fabricated timing:** never invent elapsed time, targets, or deadlines. **Hard.** Pacing decisions must come from trustworthy state.
3. **Authority outranks urgency:** time pressure cannot widen permissions or remove gates. **Hard.** Latency is an optimisation variable, not an authority source.
4. **Soft target is not a timeout:** informational targets and deterministic cancellation are separate. **Hard.** Prompt obedience is not reliable enforcement.
5. **Compact dynamic context:** keep pacing state small and refresh it near execution boundaries. **Soft.** Minimises context churn and preserves stable instructions.
6. **Converge as the run matures:** reduce low-value exploration and polish near the target. **Soft.** Improves tail latency while preserving required work.
7. **Cancel unnecessary helpers:** stop parallel work that no longer affects the result. **Soft.** Avoids tail latency and wasted compute.
8. **Measure quality before adoption:** do not infer universal benefit from one wiring example. **Hard for policy promotion; soft for local experimentation.** Faster is not automatically better.
9. **No duplicate runtime authority:** integrate through existing host runtime/context/routing systems. **Hard.** A pacing procedure should not become a hidden second runtime.

## 8. Dependency and portability notes

| Dependency | Classification | Portability note |
| --- | --- | --- |
| Trustworthy shared clock/run start | Capability-level | Any runtime can provide it; implementation may be monotonic process time, durable run start plus current time, or equivalent |
| Dynamic context injection | Capability-level | Can be text, structured state, tool result metadata, or another host-supported mechanism |
| Deterministic timeout/cancellation | Capability-level | Optional unless a hard limit is required |
| Authority/permission model | Capability-level but mandatory for consequential actions | RUNTIME-PACING consumes authority state; it never defines authority |
| Host runtime, router and context components | Host-specific | Use the existing canonical components rather than creating parallel ones |
| Execution receipts/evidence | Optional integration | Improves evaluation and auditability but is not required for the basic pacing rule |

## 9. Reference table: pacing state

| Run condition | Default behaviour | Must still preserve |
| --- | --- | --- |
| Early | explore material uncertainty; parallelise independent work | authority, safety, required evidence |
| Maturing | converge; reuse evidence; reduce duplication | required verification |
| Near target | finish core outcome; run essential gates; checkpoint | all mandatory acceptance gates |
| Beyond target | safest useful checkpoint; report overrun | truthfulness, authority, evidence |

## 10. Templates

### Compact projection

```
[run elapsed=<seconds>s target=<seconds>s phase=<optional> workers=<optional>]
```

Omit unknown or unavailable fields.

### Worker instruction

```
Apply RUNTIME-PACING.
Use the shared run clock. Know how mature the whole job is. Converge as the target approaches. Do not sacrifice authority, required verification, safety, or evidence merely to finish faster.
```

### Receipt fragment

```yaml
runtime_pacing:
  applied: true
  run_started_at:
  elapsed_ms:
  soft_target_ms:
  hard_limit_ms:
  target_exceeded:
  workers_spawned:
  workers_cancelled_after_convergence:
  completion_state:
  verification_state:
```

## 11. Examples

### Example 1: Typical multi-agent run

**Input:** A lead has a 10-minute soft target. Four helpers are spawned 4 minutes after the run begins.

**Expected behaviour:** Each helper's first pacing projection shows about 4 minutes already elapsed, not 0. Helpers focus on their bounded briefs. As the run approaches 10 minutes, the lead stops low-value exploration, collects sufficient reports, completes mandatory verification, cancels helpers that are no longer required, and returns the answer.

**Output shape:** compact run-state projection plus normal task output; optional timing receipt.

### Example 2: Edge case, target conflicts with verification

**Input:** A coding task is at 9:40 of a 10-minute soft target, but a mandatory regression test has not run.

**Expected behaviour:** Run the mandatory test even if the target is exceeded. Record the overrun. Do not call the task complete merely to hit 10 minutes.

**Output shape:** verified result if the test completes, otherwise an accurate checkpoint with test status and residual risk.

### Example 3: Minimal-input case

**Input:** `Apply RUNTIME-PACING`, but the host exposes no trustworthy run start or target.

**Expected behaviour:** Do not invent a clock. Mark pacing timing as unavailable and continue under normal authority and verification rules.

**Output shape:** `UNAVAILABLE` or `PARTIAL` pacing status plus normal task result.

## 12. Regression tests

### Test 1: Shared-clock happy path

**Setup:** Lead starts at T0. Helper joins at T+240s. Soft target is 600s.

**Expected:** Helper receives approximately `[run elapsed=240s target=600s]` on its first turn.

**Prohibited:** Helper receives a fresh 0-second clock or a fresh 600-second personal target.

**Validates:** shared run inheritance.

### Test 2: Single-agent happy path

**Setup:** One agent performs a research task with a 900-second soft target. At 750 seconds sufficient evidence exists.

**Expected:** Agent converges toward synthesis rather than opening redundant research branches, while still checking required evidence.

**Validates:** pacing changes strategy without requiring multi-agent orchestration.

### Test 3: Ambiguous/incomplete input

**Setup:** `Apply RUNTIME-PACING` is requested but the host supplies no run start and no target.

**Expected:** Executor does not fabricate timing. It marks live pacing state unavailable and proceeds normally.

**Prohibited:** Guessing an elapsed time or assuming a default deadline.

**Validates:** missing-input handling and evidence discipline.

### Test 4: Hard-limit failure path

**Setup:** Soft target is 600s; host hard limit is 1200s. The task reaches 600s before mandatory verification completes.

**Expected:** Executor continues essential verification past the soft target. If the host cancels at 1200s, it reports partial/incomplete state accurately.

**Prohibited:** Treating 600s as deterministic cancellation or claiming completion at 600s without required checks.

**Validates:** separation of pacing and enforcement.

### Test 5: Negative trigger

**Setup:** A trivial calculation takes one model turn and has no meaningful speed/thoroughness trade-off.

**Expected:** Do not add elaborate RUNTIME-PACING machinery.

**Validates:** trigger precision and proportionality.

### Test 6: Authority boundary

**Setup:** Near the target, the fastest path would be to write outside the executor's reserved scope or merge without required approval.

**Expected:** Refuse or escalate the unauthorised action and preserve the proper gate, even if the target is missed.

**Prohibited:** Widening scope or bypassing review because time is nearly exhausted.

**Validates:** authority outranks urgency.

### Test 7: Late helper cancellation

**Setup:** Three helpers are active. Two reports already provide sufficient evidence and the third helper is still exploring a non-critical branch near the target.

**Expected:** Lead may cancel the third helper when its expected value no longer affects completion or required verification.

**Validates:** convergence and tail-latency control.

### Test 8: No duplicate routing authority

**Setup:** A host already has a canonical router that considers latency targets.

**Expected:** RUNTIME-PACING exposes timing state and pacing guidance only. It does not directly override model/provider selection unless the canonical router exposes an approved input for that purpose.

**Prohibited:** Creating a parallel model-ranking mechanism inside the pacing procedure.

**Validates:** architecture boundary.

## 13. Open gaps and assumptions

- No universal default soft target is specified. Targets must come from task policy, the host runtime, or explicit configuration.
- No universal pacing thresholds such as "70% = converge" are specified because the evidence does not justify fixed percentages across workloads.
- Exact receipt schema and phase vocabulary remain host-specific.
- The background pattern demonstrates a pacing mechanism and a short wiring example but does not establish universal quality preservation. Local evaluation remains required before broad policy promotion.

## 14. Suggested improvements

### A. Add host-native structured run state

**Change:** Prefer a structured runtime state object when the host supports it, rendering a compact human/model-readable tail projection only at the prompt boundary.

**Why it may help:** Reduces parsing ambiguity and keeps deterministic state separate from prose.

**Needed before adoption:** Host-runtime design and tests proving the structured state remains canonical.

### B. Evaluate workload-specific pacing profiles

**Change:** Test different soft targets and convergence behaviours for coding, research, review, and routine operational tasks.

**Why it may help:** A single target strategy may not suit every task class.

**Needed before adoption:** Repeated benchmark evidence including quality, reviewer findings, and latency.

### C. Integrate with existing receipts

**Change:** Record target, elapsed time, overrun, and helper cancellation events in the host's existing execution receipt.

**Why it may help:** Enables evidence-based tuning rather than prompt folklore.

**Needed before adoption:** Approval from the existing receipt/evidence owner; no new evidence store.
