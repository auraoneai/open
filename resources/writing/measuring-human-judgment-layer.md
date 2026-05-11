# Measuring The Human Judgment Layer

Owner: AuraOne open-source working group
Status: external thesis draft for PRD 14
Audience: AI lab leaders, eval engineers, research engineers, and data/eval operations leads
Publication target: auraone.ai/writing, auraone.ai/open excerpt, and outbound-friendly summary

The best evals will stay private. The standards for building trustworthy evals should not.

That is the core bet behind AuraOne EvalKit: the industry does not need another unsupported public leaderboard dressed up as methodology. It needs inspectable standards for the part of AI evaluation that has become hardest to reason about: the human judgment layer.

This post is the external thesis memo. The implementation details live separately in the [EvalKit technical methodology](../evalkit/evalkit-technical-methodology.md). EvalKit is a standalone open-source package concept with the `evalkit` CLI namespace; it is separate from the hosted AuraOne SDKs and the hosted `aura` CLI. The tutorial examples described here are synthetic. They are not expert-authored, not human-validated, and not benchmarks.

Related links: [EvalKit docs index](../evalkit/README.md), [open-source strategy](../../../opensource.md), [auraone.ai/open](https://auraone.ai/open), and [auraone.ai/resources](https://auraone.ai/resources).

## The Problem

Frontier teams have become good at producing model outputs. They have become less comfortable with the question that follows: who decides whether those outputs are good, how consistent is that decision, and can the result be trusted across releases?

Benchmarks answer one version of the question. They compress a task distribution, a scoring method, and a result into something comparable. That is useful, but it is not enough for private model development. The most valuable evals inside labs are often private because they encode product risk, unreleased capabilities, customer workflows, internal policy, or domain-specific failure cases.

So the practical question is not whether all evals should be public. They will not be. The practical question is whether the standards around private evals can be public.

## Evals Are Becoming Release Infrastructure

The old mental model was simple: run a benchmark, compare a score, publish a chart.

The newer operating model is messier:

- Rubrics change.
- Model judges need calibration.
- Human reviewers disagree.
- Reviewer pools drift.
- Task mixes shift between releases.
- Public prompts can leak.
- Reports need to say what the run can and cannot prove.

That is EvalOps. It treats evals as release infrastructure rather than one-off research artifacts.

A private eval program needs the same hygiene software teams expect elsewhere: schemas, linting, versioning, reproducible commands, review checklists, and run reports that disclose limitations. Rubrics are not prose decoration. Rubrics are part of the system.

## Benchmark, EvalOps, Rubric Engineering, JudgeOps

These terms are related but not interchangeable.

| Term | What it answers | Common failure |
| --- | --- | --- |
| Benchmark | "How did this model score on this public task set?" | Treating one score as complete evidence. |
| EvalOps | "Can this eval be run, compared, audited, and reported across releases?" | Missing versioning, drift checks, and disclosure. |
| Rubric engineering | "Are the criteria scorable, atomic, weighted, and disagreement-aware?" | Vague criteria that reviewers cannot apply consistently. |
| JudgeOps | "Can an LLM judge be trusted for this rubric and domain?" | Using judge scores without reference-label calibration. |
| Human judgment observability | "Can we measure the quality and stability of human or judge decisions?" | Hiding disagreement behind aggregate scores. |

AuraOne's open-source posture starts with the tooling layer. Not a claim that we have a public expert benchmark on day one. Not a synthetic safety benchmark. A set of public standards and local tools for teams building their own evals.

## Why Private Evals Need Public Standards

Private evals are often private for good reasons. They may include unreleased product behavior, confidential customer workflows, sensitive domain criteria, or proprietary failure cases. Publishing the data can be impossible or irresponsible.

But teams can still publish and share the standards around the work:

- What does a rubric criterion need before it is scorable?
- What should a dataset card disclose?
- How should reviewer agreement be reported?
- How should judge calibration be summarized?
- What should a run report say before anyone uses it in a release decision?
- Which limitations should block a leaderboard-style claim?

This is where public tooling helps. The artifact is not the private eval itself. The artifact is the method a serious team can inspect before trusting the private eval.

## A Concrete EvalKit Shape

A local EvalKit workflow should look boring in the best way:

```bash
evalkit validate-rubric examples/tutorial/rubric.yaml
evalkit score \
  --rubric examples/tutorial/rubric.yaml \
  --responses examples/tutorial/model_outputs.jsonl \
  --out reports/tutorial-run.json
evalkit report --input reports/tutorial-run.json --out reports/tutorial-run.md
```

The command is not the point. The contract is the point:

- The rubric has a version.
- The dataset has a data-status disclosure.
- The scoring policy is explicit.
- Agreement and judge calibration are reported when available.
- The report says what the run cannot prove.

For v0.1 tutorial material, the disclosure matters as much as the demo: synthetic examples make the workflow runnable, but they are not expert-authored data, human-validated data, safety benchmarks, or model leaderboards.

## The Human Judgment Layer

The human judgment layer includes everything between raw model output and a trusted decision:

- rubric authorship
- task design
- reviewer qualification
- reviewer calibration
- LLM judge calibration
- disagreement handling
- drift monitoring
- report interpretation

This layer is becoming part of the model stack. If it is weak, model teams get noisy signals. If it is unobservable, leaders get confident-looking reports that do not survive scrutiny.

The better question is not "human or judge?" It is "how is judgment measured, versioned, calibrated, and reported?"

## What To Use Now

Start with the public standards:

- [EvalKit Technical Methodology](../evalkit/evalkit-technical-methodology.md)
- [Criterion Quality Checklist](../evalkit/criterion-quality-checklist.md)
- [Eval Dataset Card Template](../evalkit/eval-dataset-card-template.md)
- [Human Data Failure Modes Catalog](../evalkit/human-data-failure-modes.md)
- [Red-Team Prompt Taxonomy](../evalkit/red-team-prompt-taxonomy.md)
- [Multi-Turn Eval Template Pack](../evalkit/multi-turn-eval-template-pack.md)
- [Eval Run Report Template](../evalkit/eval-run-report-template.md)

For buying and implementation resources, use [auraone.ai/resources](https://auraone.ai/resources) and [auraone.ai/open/private-evals](https://auraone.ai/open/private-evals).

## Decision Checklist

Before using any eval result in a release conversation, ask:

- [ ] Is the task data status explicit?
- [ ] Is the rubric version pinned?
- [ ] Are criteria scorable, atomic, and evidence-backed?
- [ ] Are aggregate scores backed by per-criterion results?
- [ ] Is reviewer agreement reported or explicitly unavailable?
- [ ] Is judge calibration reported before judge scores are trusted?
- [ ] Are drift and task mix changes separated from model changes?
- [ ] Does the report state what the run cannot prove?
- [ ] Are customer, reviewer, and proprietary details protected?

## Excerpt For auraone.ai/open

Private evals do not have to become public benchmarks to be trustworthy. The data, prompts, and customer-specific criteria may need to stay private. The standards around them should not. AuraOne EvalKit focuses on the open tooling layer for rubric quality, scoring reproducibility, reviewer agreement, judge calibration, drift, and eval reports, with synthetic tutorial data used only to make the workflow runnable.

## Outbound-Friendly Summary

We are open-sourcing the standards layer around private evals: rubric linting, scoring contracts, agreement checks, judge calibration, drift, dataset cards, and eval run reports. The first release is intentionally not an expert-authored benchmark. It is infrastructure for teams that already know their most important evals will remain private, but still want the methodology to be inspectable.

## Social Launch Snippets

1. The best evals will stay private. The standards for building trustworthy evals should not. AuraOne EvalKit is our open-source push toward rubric quality, judge calibration, reviewer agreement, drift checks, and reproducible eval reports.
2. Benchmarks tell you how a model scored once. EvalOps asks whether that score is stable, reproducible, versioned, and safe to interpret for a release decision.
3. Rubrics are part of the model stack now. They need linting, versioning, examples, disagreement checks, and reports, not just prose in a spreadsheet.

## Caveats And Public References

This memo makes a methodology argument, not a benchmark claim. It does not claim AuraOne has released expert-authored benchmark data, validated model-safety data, or customer eval results. The following public references are useful category context, but they should not be read as endorsement of AuraOne or evidence for any private AuraOne result:

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework): public risk-management context for AI systems.
- [Stanford HELM paper](https://arxiv.org/abs/2211.09110): public work on holistic model evaluation and transparency.
- [OpenAI Evals](https://github.com/openai/evals): open-source framework for evaluating LLMs and LLM systems.
- [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness): open-source language-model evaluation harness.
- [UK AI Safety Institute Inspect announcement](https://www.gov.uk/government/news/ai-safety-institute-releases-new-ai-safety-evaluations-platform): public announcement of the Inspect evaluations platform.

## Limitations

Open standards do not replace expert review, representative data, privacy review, or release governance. They make it easier to see whether those things exist. EvalKit can make an eval workflow inspectable; it cannot make unsupported data representative or turn synthetic tutorials into a benchmark.
