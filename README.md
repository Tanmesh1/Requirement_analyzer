# Requirement_analyzer
This is an AI-powered requirement analyzer which helps users understand and structure client requirements.

The system uses a **multi-stage reasoning framework** driven by a master prompt and domain-specific templates (software vs architecture).
The LLM pipeline performs:

1. Requirement clarification and intent inference
2. Decomposition into functional/non-functional items
3. Identification and severity classification of missing information
4. Risk analysis and structured JSON consolidation

The codebase provides:

* `app/services/ai_agent.py` – contains `LLMRequirementRefiner` with `analyze`, `rewrite`, and `answer_question` methods that build and invoke prompts. Master/domain prompts are defined as constants in the file.  
  The `analyze` method is resilient to non‑strict model responses; it will strip surrounding commentary, retry once if the output cannot initially be parsed as JSON, and raise a descriptive error if the model refuses to comply.  This helps avoid the common situation where the model returns human‑readable text instead of a pure JSON object.
* `DocumentAI` orchestrates analysis and prose rewriting.
* `app/services/pdf_generator.py` – builds a rich, multi-page PDF suitable for sharing with employees and stakeholders. The generator accepts cleaned requirements and optional structured analysis and renders cover page, executive summary, breakdowns, missing items and risk matrix followed by a refined-prose appendix.
* `RAGservice` performs retrieval-augmented QA using the same refiner.

Domain templates are selected by passing `domain="software"` or `"architecture"` when creating services.

See `test/test_ai_agent.py`, `test/test_rag_service.py`, and `test/test_embedding.py` for example usage and mocked tests.

Original rule-based extractor remains available as a legacy fallback.
