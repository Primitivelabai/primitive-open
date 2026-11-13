---
name: adversarial-verification
description: Use when a consequential, surprising, high-stakes, novel, safety-relevant, research, proof, benchmark, or "verified" claim needs stronger checking than ordinary review, especially when one passing test or one evaluator could create false confidence.
---

# Adversarial Verification

## Core rule

Do not ask "can I confirm this?" Ask **"what would make this false, and can I make that happen?"**

Agreement is not verification. A passing test is evidence about the tested case, not proof of the wider claim.

## When to use

Use this for:

- surprising or unusually strong research claims;
- mathematical/proof arguments;
- security, safety, protocol or architecture guarantees;
- benchmark, eval or simulation conclusions;
- important code claims such as "fixed", "safe", "correct", "no regression" or "production-ready";
- any result where the author, test, checker and evidence may share the same blind spot.

For ordinary UI edge-case testing, use the narrower `ui-adversarial-testing` skill instead.

## Verification contract

Before checking, write:

1. **Claim:** the smallest precise statement being asserted.
2. **Scope:** what is and is not covered.
3. **Dependencies:** assumptions, data, prior results, environment and external guarantees.
4. **Kill conditions:** observations that would falsify, weaken or reclassify the claim.
5. **Evidence needed:** what would count as strong enough support.
6. **Promotion rule:** what must be complete before the claim can be upgraded.

Never strengthen the claim after seeing favourable results.

## Independent lanes

Use genuinely different attack paths where practical. Keep them blind to one another until they report.

Assign narrow joints, not "review everything":

- **Counterexample hunter:** construct valid-looking cases where the claim should fail.
- **Assumption auditor:** find circular, hidden, unrealistic or conclusion-bearing assumptions.
- **Re-deriver:** reproduce the result independently from the underlying sources/data/code.
- **Oracle/test auditor:** ask whether the checker could pass while the system is wrong.
- **Boundary reviewer:** identify exactly what the result does *not* establish.
- **Source/literature verifier:** confirm that cited external inputs say what the argument requires.

The original author must not be the sole judge of their own result.

## Adversarial checks

Choose checks that can actually kill the claim:

- known-false or opposite-world controls;
- edge and boundary cases;
- valid-looking but wrong inputs;
- omitted-transition or missing-state probes;
- stale, reordered, duplicated or partial inputs;
- independent implementation or calculation;
- ablation of each load-bearing assumption;
- "proves too much" test: does the method also certify a case known to be false?;
- coverage audit: what states or cases were never explored?;
- implementation-correspondence check: does the executable system match the model/spec that was verified?;
- replay: can a reported failure or success be reproduced exactly?

If a checker trusts mutable state that it is supposed to verify, treat that as an oracle defect.

## Evidence discipline

Keep these separate:

- **Observed:** directly reproduced or inspected.
- **Supported:** multiple independent checks agree.
- **Formally verified:** machine-checked within explicitly stated assumptions.
- **Not independently verified:** reported by another source only.
- **Unknown:** not checked or evidence unavailable.

Do not turn "no failure found" into "safe".
Do not turn "tests pass" into "correct".
Do not turn "formal proof passes" into "production implementation is correct" without a correspondence argument.

## Failure classification

When something breaks, classify it before fixing it:

- claim/theory counterexample;
- implementation bug;
- verifier/oracle blind spot;
- coverage gap;
- invalid-input probe;
- unrealistic or unstated assumption;
- source/citation error;
- environment/tooling limitation.

A repair is not evidence until the original failing case becomes a regression and the affected verification is rerun.

## Stop and promotion rules

Do **not** promote while an assigned verification lane is still outstanding merely because earlier lanes passed.

A claim may be promoted only when:

- all required lanes have reported;
- no unresolved valid counterexample remains;
- assumptions are explicit and acceptable;
- the strongest relevant negative controls fail as expected;
- the claimed scope matches the evidence;
- repairs have permanent regression coverage;
- independent reproduction is possible from the saved evidence.

If a small principled repair fixes the issue, repair, add the regression and rerun the affected checks.
If safety/correctness requires circular or unrealistic assumptions, or repeated patching reveals a structural failure, return **REDESIGN / REJECT**, not another patch.

## Output contract

Return:

```
VERDICT: PASS | PASS WITH LIMITS | REPAIR | REJECT | NOT VERIFIED

CLAIM
Exact claim checked

SCOPE / NON-CLAIMS
What this does not establish

ATTACKS RUN
Independent lanes, controls, reproductions and coverage

FINDINGS
Each finding with evidence and classification

ASSUMPTIONS
Explicit, tested where possible

EVIDENCE STATUS
Observed / supported / formally verified / unverified / unknown

REMAINING GAPS
Anything not checked or still ambiguous

NEXT ACTION
Exact repair, rerun or promotion step
```

Preserve failed ideas and disproved routes as a **do-not-repeat ledger** with the honest statement of what actually stood.

See `TESTS.md` for pressure scenarios that this skill should handle.
