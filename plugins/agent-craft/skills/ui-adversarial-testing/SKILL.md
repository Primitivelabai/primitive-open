---
name: ui-adversarial-testing
description: Use when QA needs to actively try to break a changed web UI, explore edge cases around a pull request, or test user flows beyond the happy path with browser evidence.
---

# UI Adversarial Testing

## Goal

Find failures the implementation author did not plan for. This complements ordinary browser testing; it is not a replacement for unit, integration or accessibility-specific tests.

## Plan before clicking

Build one compact test list from three passes:

1. **Functional:** What must work for the intended user?
2. **Adversarial:** What breaks if the user is fast, confused, interrupted or supplies hostile/edge input?
3. **Coverage gaps:** What changes with keyboard-only use, small viewport, slow/erroring network, empty data, different roles, console errors or broken media?

Deduplicate the list and prioritise the changed surface. Parallelise independent groups only when the environment supports it; do not invent subagents as a requirement.

## High-value adversarial checks

Use only those relevant to the feature:

- empty, whitespace-only, huge and special-character input;
- rapid double-click/double-submit;
- repeated open/close and Escape/back navigation;
- refresh or route change mid-flow;
- loading, empty, error and recovery states;
- slow/failed request and retry behaviour;
- mobile/narrow viewport overflow;
- keyboard-only navigation and focus order;
- stale data or duplicate actions;
- broken images/media;
- console errors and failed network requests;
- role/permission boundaries when test identities are available.

## Evidence loop

For each test:

1. capture the before state;
2. perform the exact action;
3. capture the after state;
4. mark **PASS**, **FAIL** or **SKIP** with concrete evidence.

A failure report includes: test id, reproduction steps, expected result, actual result and a screenshot for visual failures where possible.

## Scope discipline

- Start from the git diff or named feature when one exists.
- Do not turn a one-component change into an unbounded whole-product audit.
- Do not call skipped checks passes.
- Do not infer "no bugs" from limited coverage.
- Reproduce a failure before suggesting a fix.

## Relationship to other skills

Use ordinary web-app testing for routine browser verification and a dedicated accessibility test for accessibility claims. This skill adds adversarial planning and edge-case pressure. For high-stakes claims beyond the UI, use `adversarial-verification`.
