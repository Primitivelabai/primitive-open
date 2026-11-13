---
name: retrieval-routing-patterns
description: Improve RAG, search, capability discovery, tool/skill selection, expert routing, retrieval quality, structured-output reliability, and semantic-cache decisions without creating duplicate runtime authority. Use when designing or reviewing retrieval pipelines, query rewriting/compression/expansion, semantic or hybrid search, reranking, progressive tool disclosure, capability search, specialist routing, evaluator loops, fact checking, schema repair, or cache policy.
---

# Retrieval Routing Patterns

Use retrieval as a composable pipeline, not a second agent runtime. Reuse the system's existing search, capability, routing, execution, approval, evidence, and memory components wherever they already exist.

## Workflow

1. **Run a reuse and authority preflight.**
   - Find what already owns search, routing, tools, approvals, evidence and memory in this system, from the live code rather than memory or old notes.
   - Check whether anyone else is already changing the same boundary.
   - Do not create a second search layer, router, agent runtime, tool runtime, approval path, evidence store, memory system, provider gateway, or job system when a canonical one exists.
2. **Classify the retrieval problem.**
   - Knowledge retrieval: find evidence or context.
   - Capability retrieval: find the smallest relevant tools, skills, agents, or methods.
   - Expert routing: select a specialist role or execution profile from an already-authorised candidate set.
   - Output reliability: validate structure, relevance, support, or cache reuse.
3. **Prepare the query only as much as needed.**
   - Compress conversational follow-ups into standalone queries when references such as "that one" or "the earlier fix" would hurt search.
   - Rewrite poorly formed queries for the target search system when necessary.
   - Translate only when the index or embedding substrate needs a target language.
   - Expand into several semantically distinct queries when recall matters more than a single precise hit.
   - Preserve the original query alongside expansions unless there is a strong reason not to.
4. **Retrieve with explicit controls.**
   - Prefer hybrid exact/lexical plus semantic retrieval when exact identifiers and fuzzy intent both matter.
   - Apply authorisation and scope filters before results are exposed.
   - Use metadata filters, top-K, and a similarity/relevance threshold deliberately rather than accepting every nearest neighbour.
   - Preserve source identity, score, scope, and provenance for every result.
5. **Join and post-process.**
   - Merge multi-query and multi-source results by canonical identity.
   - Deduplicate before generation.
   - Rerank against the original user intent when first-stage retrieval is noisy.
   - Remove irrelevant or redundant results.
   - Compress long documents only when the compression preserves citation/provenance anchors.
6. **Use progressive capability disclosure for large tool/skill catalogues.**
   - Index compact capability summaries rather than injecting every definition into model context.
   - Retrieve a small candidate set from the user's intent.
   - Then apply authority, capability, connection, approval, and availability checks.
   - Only after those checks expose executable definitions to the model.
   - **Discovery never grants authority.** Search can nominate a tool; the governed runtime decides whether it may execute.
7. **Route specialists through the existing router.**
   - Prefer stable role/capability classes before concrete model names.
   - Route simple, separable categories deterministically where possible.
   - Use an orchestrator only when decomposition cannot be known upfront.
   - Keep worker ownership and handoff contracts explicit.
   - Do not create a parallel "expert router" if the product already has a canonical router or role-routing layer.
8. **Define empty-context behaviour.**
   - Never let missing retrieval silently become invented context.
   - Choose one explicit mode: answer from general knowledge with a warning, ask for more information, run another retrieval path, or return insufficient evidence.
9. **Validate outputs with bounded repair.**
   - Validate structured outputs against the actual schema.
   - On validation failure, feed the validation error back for repair.
   - Hard-cap repair attempts. Default to no more than 3 model retries unless a stronger product constraint exists.
   - Evaluate RAG answers for relevance to the retrieved context.
   - For high-value factual claims, check whether the claim is supported by the supplied evidence.
   - Evaluators may reject or request repair; they do not silently promote authority, policy, or canonical knowledge.
10. **Use semantic caching only behind an authority-aware cache key.**
    - Cache only outputs that are safe to reuse across semantically similar requests.
    - Include relevant system/profile version, scope, model/policy version, source revision, and authorisation context in cache identity.
    - Use TTLs appropriate to source freshness.
    - Bypass semantic cache for current news, permissions, account-specific state, consequential decisions, external actions, rapidly changing data, or evidence-sensitive answers unless freshness and scope are proven.
11. **Return an integration recommendation, not framework enthusiasm.**
    - State the existing reuse surface first.
    - Name the smallest missing piece.
    - Classify donor patterns as COPY, ADAPT, REFERENCE, or BUILD.
    - Identify the canonical integration boundary.
    - Include tests for retrieval quality, authority filtering, stale context, duplicate results, empty context, retry limits, and evidence preservation.

## Pattern selection shortcuts

- Large tool/skill catalogue: progressive capability disclosure.
- Conversational follow-up search: query compression.
- Weak recall or vocabulary mismatch: multi-query expansion.
- Noisy vector results: metadata filtering plus reranking.
- Hallucination-prone RAG: relevancy and support evaluation.
- Fragile JSON/tool contracts: schema validation with bounded repair.
- Repeated stable Q&A: authority-aware semantic cache.
- Distinct specialist categories: canonical role routing.
- Unknown task decomposition: the existing orchestrator-workers mode, not a new orchestration system.

## References

- `references/spring-ai-patterns.md`: where each pattern appears in Spring AI, with the recommended reuse mode.
- `references/adoption-checklist.md`: read when turning a pattern into implementation work or a code-review recommendation.
