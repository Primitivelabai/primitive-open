# Spring AI donor patterns

Patterns observed in [Spring AI](https://github.com/spring-projects/spring-ai) (Apache-2.0) and [spring-ai-examples](https://github.com/spring-projects/spring-ai-examples), reviewed October 2026. Credit to the Spring AI team.

These are architecture patterns, not instructions to adopt Spring or Java, and this skill does not include Spring source code. If you copy or adapt Spring source, preserve its licence and notice files. Re-check upstream, as paths change.

## Recommended patterns

| Pattern | Where it appears in Spring AI | What to take | Default reuse mode |
| --- | --- | --- | --- |
| Progressive tool discovery | Dynamic tool search guide; `ToolIndex`, `VectorToolIndex` | Index tool summaries and disclose only relevant tool definitions per request/session | ADAPT |
| Query rewrite | `RewriteQueryTransformer` | Reformulate user text for the target search substrate | ADAPT |
| Conversation compression | `CompressionQueryTransformer` | Turn conversation history plus follow-up into a standalone search query | ADAPT |
| Query translation | `TranslationQueryTransformer` | Normalise query language when the index/embedding substrate requires it | REFERENCE / ADAPT when needed |
| Multi-query expansion | `MultiQueryExpander` | Generate several semantically distinct retrieval queries and preserve the original | ADAPT |
| Controlled vector retrieval | `VectorStoreDocumentRetriever` | Explicit metadata filters, similarity threshold, top-K | ADAPT to existing search authority |
| Multi-source join/dedupe | `ConcatenationDocumentJoiner` | Merge results by identity and keep first/canonical occurrence | ADAPT |
| Post-retrieval processing | `DocumentPostProcessor` | Stable seam for reranking, redundancy removal, and content compression | ADAPT |
| Context augmentation with empty-context policy | `ContextualQueryAugmenter` | Make missing-context behaviour explicit instead of silently hallucinating | ADAPT |
| Structured-output validation | `StructuredOutputValidationAdvisor` | Validate JSON against schema, feed validation errors back, cap retries, accumulate usage | ADAPT |
| RAG relevancy evaluation | Testing docs, `RelevancyEvaluator` | Score whether the answer is aligned with query plus retrieved context | ADAPT |
| Claim support checking | Testing docs, `FactCheckingEvaluator` | Check whether generated claims are logically supported by provided evidence | ADAPT |
| Semantic cache | Redis semantic cache module | Similarity-based response reuse with threshold and TTL | REFERENCE; adopt only with authority/freshness scoping |
| Tool-call limits and return-direct | Tools docs | Bound recursive tool loops; let terminal results skip another model round-trip when safe | REFERENCE; integrate only if your runtime lacks equivalent controls |

## Agentic workflow examples: reference only if you already have them

Spring's examples include routing, parallelisation, orchestrator-workers, chain workflow and evaluator-optimizer. They are useful architecture references. If your system already has a router, execution runtime and parallel/chain/multi-agent modes, use those rather than adding a second set.

The valuable distinction is:

- **Routing** when categories and specialists are known ahead of time.
- **Orchestrator-workers** when decomposition depends on the specific task.
- **Evaluator-optimizer** when explicit quality criteria justify bounded iterative repair.

## Skip unless a gap is proven

- A generic model/provider abstraction, if you already have a model gateway.
- A generic tool runtime, if you already have governed tools and an execution runtime.
- A generic ETL reader → transformer → writer pipeline, if you already have extraction, indexing, search and provenance.
- Framework-specific vector-store integrations: choose a backend only when your search layer needs one, and don't let it become a second retrieval authority.
