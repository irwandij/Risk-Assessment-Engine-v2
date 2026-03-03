# QA Test Results - risk_assessment_engine

Date: 2026-02-22  
Project: `/Users/suryaf/projects/risk_assessment_engine`  
Tester: Codex QA run

## Scope
Performed integration QA across CLI flows and output artifacts:
- Merchant assessment (`validate`, `assess`) using existing fixture corpus
- Partner/Vendor/AI assessment commands using generated sample inputs
- Failure-path behavior checks (invalid path, wrong input shape)
- State-consistency check for repeated use of a single `Assessor` instance

## Environment
- Runtime used for test execution: `/Users/suryaf/projects/doc2md-lite/.venv/bin/python` (Python 3.11.14, pydantic 2.12.5)
- Note: system `python3` in this environment is missing `pydantic`, so CLI does not run there without dependency setup.

## Test Artifacts
- Merchant run summary: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/merchant_summary.json`
- Cross-type summary: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/cross_type_summary.json`
- Generated outputs: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/results`
- Generated reports: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/reports`
- Generated sample inputs: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/samples`

## Execution Summary
### Merchant fixtures (7/7 executed)
- Command status: `validate` and `assess` returned `0` for all 7 inputs.
- Functional status: **failed behaviorally**.
- Observed: all merchants scored `REJECT`, with total scores `25` or `0`, including previously strong fixtures (e.g. Koinworks).

### Non-merchant flows
- `sample --type merchant|partner|vendor|ai`: all passed.
- `assess-partner`: failed (validation error)
- `assess-vendor`: failed (validation error)
- `assess-ai`: failed (validation error)

### Negative-path checks
- `validate /tmp/does-not-exist.json` correctly returns non-zero.
- `assess-partner <merchant-json>` correctly returns schema validation error.

## Findings (Ordered by Severity)

### P0 - Merchant scoring is catastrophically incorrect (A/C/D/E/F/G/H/I effectively capped to 0)
- Impact: core merchant decisioning is invalid; high-quality merchants are forced to `REJECT`.
- Evidence:
  - `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/results/koinworks-result.json` shows strong evidence on many parameters but scores `0` for A/C/D/E/F/G/H/I and total score `25`.
  - `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/results/tiga-pilar-media-result.json` same pattern.
- Root cause:
  - Multiple scorers use `min(points, self.max_score)` while `self.max_score` remains default `0` (these classes define `max_score_regular` / `max_score_pjp`, not `max_score`).
  - Examples:
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_a.py:70`
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_c.py:53`
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_d.py:92`
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_e.py:94`
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_f.py:68`
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_g.py:59`
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_h.py:69`
    - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_i.py:82`

### P0 - `assess-partner` and `assess-vendor` are non-functional due schema mismatch
- Impact: Partner/Vendor assessment commands cannot complete.
- Evidence:
  - `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/cross_type_summary.json`
  - Error tail: `merchant_type` expects `regular_merchant|pjp_aggregator`, but receives `AssessmentType.PARTNER` / `AssessmentType.VENDOR`.
- Root cause:
  - `AssessmentResult.merchant_type` is typed as `MerchantType` only.
    - `/Users/suryaf/projects/risk_assessment_engine/models/assessment_result.py:86`
  - Partner/Vendor assessors pass `AssessmentType.*`.
    - `/Users/suryaf/projects/risk_assessment_engine/engine/partner_assessor.py:86`
    - `/Users/suryaf/projects/risk_assessment_engine/engine/vendor_assessor.py:87`

### P0 - `assess-ai` is non-functional due decision enum mismatch (and same merchant_type mismatch)
- Impact: AI assessment command cannot complete.
- Evidence:
  - `/Users/suryaf/projects/risk_assessment_engine/qa_runs/2026-02-22/cross_type_summary.json`
  - Error tail includes invalid decision input (`LOW`) for `Decision` enum.
- Root cause:
  - `DecisionResult.decision` expects `Decision` enum values.
    - `/Users/suryaf/projects/risk_assessment_engine/models/assessment_result.py:57`
  - AI assessor sets `decision` to risk labels (`LOW|MEDIUM|HIGH`) and `STOP` string.
    - `/Users/suryaf/projects/risk_assessment_engine/engine/ai_assessor.py:238`
    - `/Users/suryaf/projects/risk_assessment_engine/engine/ai_assessor.py:198`
  - AI assessor also sets `merchant_type=AssessmentType.AI_PROJECT` which conflicts with `MerchantType` schema.
    - `/Users/suryaf/projects/risk_assessment_engine/engine/ai_assessor.py:93`

### P1 - Merchant assessor leaks regulatory auto-reject state across repeated assessments
- Impact: if one `Assessor` instance is reused, later assessments may inherit stale `NO_BI_LICENSE` rejection.
- Evidence (reproduced):
  - Same `Assessor` object:
    - first assess `saku-rupiah` -> auto-reject `NO_BI_LICENSE`
    - second assess `koinworks` -> still auto-reject `NO_BI_LICENSE`
  - Fresh assessor on `koinworks` -> auto-reject reason becomes `SCORE_TOO_LOW` (different), proving stale state contamination.
- Root cause:
  - `_regulatory_auto_reject` and `_regulatory_auto_reject_reason` are set in `_score_all_parameters` when triggered, but never reset at start of `assess`.
  - `/Users/suryaf/projects/risk_assessment_engine/engine/assessor.py:42`
  - `/Users/suryaf/projects/risk_assessment_engine/engine/assessor.py:45`
  - `/Users/suryaf/projects/risk_assessment_engine/engine/assessor.py:109`

### P2 - Environment setup is brittle (dependency installation not isolated)
- Impact: easy to fail on clean systems; CLI did not run under system Python due missing `pydantic`.
- Evidence:
  - `ModuleNotFoundError: No module named 'pydantic'` when running module with system python.
- Context:
  - `setup.sh` installs to ambient Python via `pip install -r requirements.txt` without venv management.
  - `/Users/suryaf/projects/risk_assessment_engine/setup.sh:25`

## Recommendations (Builder Priority)
1. Fix scoring cap bug in merchant scorers:
   - Replace uses of `self.max_score` in score clamping with `self.max_score_for_type`.
   - Re-run all merchant fixtures and verify non-zero distributions for A/C/D/E/F/G/H/I.
2. Normalize result schema for multi-assessment support:
   - Update `AssessmentResult.merchant_type` to support `AssessmentType` (or split field into `assessment_type` + optional `merchant_type`).
   - Ensure partner/vendor/ai assessors emit schema-compatible values.
3. Correct AI decision typing:
   - Map AI outcomes to allowed `Decision` enum values OR extend enum/model intentionally for AI-specific decisions (including STOP).
   - Keep `risk_level` separate from `decision`.
4. Reset mutable assessor state at start of each merchant `assess` call:
   - Clear `_parameter_scores`, `_regulatory_auto_reject`, `_regulatory_auto_reject_reason` before scoring.
5. Add automated tests before next release:
   - Integration tests for all CLI commands (`assess`, `assess-partner`, `assess-vendor`, `assess-ai`).
   - Regression tests for merchant scoring (expected non-zero for known high-quality fixture).
   - Stateful reuse test for `Assessor` to guard against leak regressions.
6. Improve setup reliability:
   - Add documented venv flow (or `uv` workflow), and a `check` command that validates runtime dependencies.

## Suggested Acceptance Criteria for Fix Verification
- Merchant fixtures produce non-degenerate scores (not all `0` except B).
- `assess-partner`, `assess-vendor`, and `assess-ai` return code `0` with valid result/report files.
- Reusing one `Assessor` instance across mixed cases does not leak auto-reject reasons.
- QA regression suite passes in clean environment after documented setup.
