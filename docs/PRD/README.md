# AuraOne Open Source PRD Index

This directory contains one PRD per build/public-asset item from `opensource.md` phases 1-4. Phase 5 expert-authored benchmarks are intentionally excluded because that phase is paused until paid customer work unlocks permissioned data and public expert authorship.

## Package Naming Rules

- Existing hosted TypeScript SDK: `@auraone/sdk`.
- Existing hosted Python SDK: `auraone-sdk`.
- Existing hosted API CLI: `aura`.
- New standalone OSS package: `auraone-evalkit`.
- New standalone OSS CLI: `evalkit`.

## PRD Files

- [01 - AuraOne Eval SDK](./01-auraone-eval-sdk.md) - Phase 1 - EvalKit Launch
- [02 - AuraOne Rubric Schema](./02-auraone-rubric-schema.md) - Phase 1 - EvalKit Launch
- [03 - Scoring CLI](./03-scoring-cli.md) - Phase 1 - EvalKit Launch
- [04 - Rubric Linter](./04-rubric-linter.md) - Phase 1 - EvalKit Launch
- [05 - LLM Judge Calibration Toolkit](./05-llm-judge-calibration-toolkit.md) - Phase 1 - EvalKit Launch
- [06 - Reviewer Agreement Library](./06-reviewer-agreement-library.md) - Phase 1 - EvalKit Launch
- [07 - Reviewer Drift Detector](./07-reviewer-drift-detector.md) - Phase 1 - EvalKit Launch
- [08 - Synthetic Multi-Turn Eval Dataset](./08-synthetic-multi-turn-eval-dataset.md) - Phase 1 - EvalKit Launch
- [09 - Inspect AI Adapter](./09-inspect-ai-adapter.md) - Phase 1 - EvalKit Launch
- [10 - LM Eval Harness Adapter](./10-lm-eval-harness-adapter.md) - Phase 1 - EvalKit Launch
- [11 - Eval Report Generator](./11-eval-report-generator.md) - Phase 1 - EvalKit Launch
- [12 - Dataset Card Generator](./12-dataset-card-generator.md) - Phase 1 - EvalKit Launch
- [13 - Methodology Paper / Technical Memo](./13-methodology-paper-technical-memo.md) - Phase 1 - EvalKit Launch
- [14 - Benchmark Saturation / Eval Quality Memo](./14-benchmark-saturation-eval-quality-memo.md) - Phase 1 - EvalKit Launch
- [15 - Rubric Tutorial Dataset](./15-rubric-tutorial-dataset.md) - Phase 1 - EvalKit Launch
- [16 - Rubric Versioning Tool](./16-rubric-versioning-tool.md) - Phase 2 - AI Eval Depth
- [17 - Eval Leakage Audit Tool](./17-eval-leakage-audit-tool.md) - Phase 2 - AI Eval Depth
- [18 - Model Output Sampling Tool](./18-model-output-sampling-tool.md) - Phase 2 - AI Eval Depth
- [19 - Rubric Weight Calibration Notebook](./19-rubric-weight-calibration-notebook.md) - Phase 2 - AI Eval Depth
- [20 - Criterion Quality Checklist](./20-criterion-quality-checklist.md) - Phase 2 - AI Eval Depth
- [21 - Dataset Card Template For Eval Data](./21-dataset-card-template-for-eval-data.md) - Phase 2 - AI Eval Depth
- [22 - Human Data Failure Modes Catalog](./22-human-data-failure-modes-catalog.md) - Phase 2 - AI Eval Depth
- [23 - Red-Team Prompt Taxonomy](./23-red-team-prompt-taxonomy.md) - Phase 2 - AI Eval Depth
- [24 - Multi-Turn Eval Template Pack](./24-multi-turn-eval-template-pack.md) - Phase 2 - AI Eval Depth
- [25 - Eval Run Report Template](./25-eval-run-report-template.md) - Phase 2 - AI Eval Depth
- [26 - Human-Data Program Playbook](./26-human-data-program-playbook.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [27 - Eval Data Readiness Checklist](./27-eval-data-readiness-checklist.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [28 - Pilot Design Templates](./28-pilot-design-templates.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [29 - Data Quality SLA Template](./29-data-quality-sla-template.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [30 - Expert Reviewer Certification Template](./30-expert-reviewer-certification-template.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [31 - Human Data SOW Template](./31-human-data-sow-template.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [32 - Vendor Comparison Checklist](./32-vendor-comparison-checklist.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [33 - AI Data Vendor RFP Template](./33-ai-data-vendor-rfp-template.md) - Phase 3 - Buying Toolkit / Customer Conversion Resources
- [34 - Robotics Failure Taxonomy](./34-robotics-failure-taxonomy.md) - Phase 4 - Robotics ReviewKit
- [35 - Teleop Review Schema](./35-teleop-review-schema.md) - Phase 4 - Robotics ReviewKit
- [36 - Robotics Dataset Card Template](./36-robotics-dataset-card-template.md) - Phase 4 - Robotics ReviewKit
- [37 - Sensor QA Checklist](./37-sensor-qa-checklist.md) - Phase 4 - Robotics ReviewKit
- [38 - Robotics Failure Viewer with sample/mock data](./38-robotics-failure-viewer-with-sample-mock-data.md) - Phase 4 - Robotics ReviewKit
- [39 - Intervention Ontology For Humanoid Data](./39-intervention-ontology-for-humanoid-data.md) - Phase 4 - Robotics ReviewKit
- [40 - Teleop Task Library](./40-teleop-task-library.md) - Phase 4 - Robotics ReviewKit
- [41 - Robotics Data Failure Modes Catalog](./41-robotics-data-failure-modes-catalog.md) - Phase 4 - Robotics ReviewKit
- [42 - LeRobot Dataset Adapter](./42-lerobot-dataset-adapter.md) - Phase 4 - Robotics ReviewKit
- [43 - RLDS / OpenX Export Tool](./43-rlds-openx-export-tool.md) - Phase 4 - Robotics ReviewKit

## Completion Rule

The numbered PRD files are immutable requirements for the current repair run. Their unchecked boxes describe required work and should not be edited merely to show progress.

`COMPLETION_AUDIT.md` is the Completion Ledger. It contains the checkbox-level Traceability rows, extracted checkbox counts, Status model, known blockers, and orchestrator evidence fields used to prove completion. A PRD is complete only when every checkbox-level row for that PRD is marked `complete` in the ledger with satisfying artifacts, validation commands, and reviewer evidence.

## Implementation Progress

The current status is pending hardening and evidence collection. Do not treat the PRD checkboxes or prior summary claims as completion evidence; use `COMPLETION_AUDIT.md` as the authoritative ledger.
