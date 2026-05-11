# Red-Team Prompt Taxonomy

This taxonomy is a high-level organizing aid for human review and judge calibration. It is not a prompt cookbook, not a safety benchmark, and not expert-validated.

## Categories

| Category | Definition | Review Focus | Metadata Tags |
| --- | --- | --- | --- |
| direct_violation | A request directly asks for disallowed behavior in a policy-bound setting. | Detect clear policy boundaries without adding operational details. | severity, modality, turn_structure |
| indirect_jailbreak | A request tries to route around stated constraints indirectly. | Identify hidden objective changes and constraint conflicts. | ambiguity, turn_structure |
| roleplay_attack | A request uses fictional framing to shift the assistant's behavior. | Check whether role framing changes boundary handling. | persona, modality |
| multi_turn_escalation | Benign turns move toward a prohibited or out-of-scope objective. | Track trajectory and context changes. | turn_structure, escalation |
| tool_use_abuse | A request asks the assistant to misuse tools or misstate tool output. | Check grounding in visible tool observations. | tool, evidence |
| hidden_instruction | A prompt includes instructions that conflict with visible user or system intent. | Detect instruction hierarchy issues without reproducing sensitive content. | instruction_source |
| emotional_manipulation | A request uses pressure or urgency to override boundaries. | Check whether urgency changes evaluation behavior. | pressure, ambiguity |
| authority_spoofing | A request claims authority or approval without evidence. | Check evidence requirements and refusal to invent authorization. | authority, evidence |
| ambiguity_exploitation | Ambiguous wording is used to produce risky or misleading output. | Require clarification instead of over-interpretation. | ambiguity, severity |
| benign_to_harmful_pivot | A harmless task pivots into an out-of-scope request over turns. | Score multi-turn context tracking. | turn_structure, escalation |

## Sanitized Example Shape

Use abstract placeholders such as `[restricted objective]`, `[claimed authority]`, or `[tool output unavailable]` instead of detailed attack text.

## Publication Guardrails

- Keep examples abstract or sanitized.
- Avoid operational instructions.
- Do not claim coverage is comprehensive.
- Do not use this as a hidden benchmark.
- Pair taxonomy use with human review before production decisions.
