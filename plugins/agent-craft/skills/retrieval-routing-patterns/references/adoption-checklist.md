# Adoption checklist

Use this before turning any donor pattern into production work.

## Existing authority

- What canonical component already owns this responsibility?
- Is the proposed change an extension point or a duplicate authority?
- Is another worker or job already touching this boundary?

## Retrieval contract

- Original query preserved?
- Rewrite/compression output inspectable?
- Multi-query expansion bounded?
- Authorisation and scope applied before exposure?
- Metadata filters explicit?
- Top-K and thresholds measured rather than guessed?
- Duplicate identity semantics defined?
- Reranking preserves source IDs and provenance?
- Empty-context behaviour explicit?

## Capability discovery contract

- Index only compact capability metadata, not secrets or credentials.
- Search candidates before exposing full definitions.
- Apply authority, connection, policy, and approval gates after discovery.
- Prevent search result ranking from bypassing deterministic admissibility.
- Record which candidates were considered and why the winner was admitted.

## Validation and repair

- Schema or acceptance criteria machine-checkable where possible?
- Retry count hard-capped?
- Usage/cost accumulated across retries?
- Failed repair leaves inspectable evidence rather than silently falling through?
- Relevancy/support evaluator separated from the generator where practical?
- Evaluator cannot mutate canonical authority or policy by itself?

## Semantic cache

- Query similarity threshold justified?
- Cache key includes relevant scope/actor, system/policy version, source revision, and model/profile version?
- TTL matches source volatility?
- Dynamic/account-specific/consequential/current-state requests bypass cache?
- Cache hit retains original provenance and age?
- Permission revocation invalidates or prevents reuse?

## Acceptance tests

Cover at least:

1. exact identifier query;
2. fuzzy natural-language query;
3. conversational follow-up requiring compression;
4. multi-query duplicate collapse;
5. unauthorised but semantically relevant result;
6. low-similarity/no-result case;
7. stale source versus fresh source;
8. reranker ordering regression;
9. malformed structured output then bounded repair;
10. retry exhaustion;
11. relevant-looking but unsupported generated claim;
12. semantic cache collision across scopes or policy versions;
13. capability search returns a forbidden tool;
14. discovered capability loses authority before execution.
