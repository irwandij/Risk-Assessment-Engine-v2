# Post-Fix QA Test Results - risk_assessment_engine

Date: 2026-02-22  
Project: `/Users/suryaf/projects/risk_assessment_engine`  
Post-fix result folder: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22`

## Implemented Fixes
1. Merchant scorer cap bug fixed (A/C/D/E/F/G/H/I):
- Replaced score clamp from `self.max_score` to `self.max_score_for_type` in:
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_a.py`
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_c.py`
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_d.py`
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_e.py`
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_f.py`
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_g.py`
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_h.py`
  - `/Users/suryaf/projects/risk_assessment_engine/scorers/parameter_i.py`

2. Schema compatibility fixed for multi-assessment flows:
- `AssessmentResult.merchant_type` now accepts both merchant and assessment enums.
  - `/Users/suryaf/projects/risk_assessment_engine/models/assessment_result.py`

3. Decision enum expanded for vendor/AI outcomes:
- Added `ESCALATE`, `LOW`, `MEDIUM`, `HIGH`, `STOP`.
  - `/Users/suryaf/projects/risk_assessment_engine/config.py`

4. Merchant assessor state leak fixed:
- Reset mutable state at start of each `assess()` call.
  - `/Users/suryaf/projects/risk_assessment_engine/engine/assessor.py`

5. Report type handling and decision display polish:
- Corrected assessment type detection precedence for enums.
- Decision threshold table now displays enum values cleanly (e.g., `PROCEED`, not `Decision.PROCEED`).
  - `/Users/suryaf/projects/risk_assessment_engine/generators/report_generator.py`

## Retest Scope
- Re-ran all merchant fixtures from original test corpus (`tests/*-research.json`, 7 files).
- Re-ran cross-type commands using generated samples:
  - `sample --type merchant|partner|vendor|ai`
  - `assess`, `assess-partner`, `assess-vendor`, `assess-ai`
- Re-ran negative-path checks.
- Re-ran state-reuse check for merchant assessor.

## Merchant Retest (All Existing Test Cases)
Source summary: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/merchant_summary.json`

| Fixture | Pre-fix | Post-fix |
|---|---|---|
| `tiga-pilar-media-research.json` | 25, REJECT | 67, PROCEED WITH CONDITIONS |
| `koinworks-research.json` | 25, REJECT | 100, PROCEED |
| `danarapay-research.json` | 0, REJECT | 4, REJECT |
| `singapay-research.json` | 0, REJECT | 36, REJECT |
| `hss-sumber-remitan-research.json` | 0, REJECT | 4, REJECT |
| `saku-rupiah-research.json` | 0, REJECT | 47, REJECT |
| `andapay-research.json` | 0, REJECT | 28, REJECT |

Interpretation:
- High-quality regular merchants now score correctly and are no longer false-rejected.
- PJP/aggregator rejection cases remain rejected for expected regulatory triggers (e.g., `NO_BI_LICENSE`, `NO_BI_LICENSE_REGISTRY`).

## Cross-Type Retest
Source summary: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/cross_type_summary.json`

| Case | Result |
|---|---|
| `sample_merchant` | PASS |
| `sample_partner` | PASS |
| `sample_vendor` | PASS |
| `sample_ai` | PASS |
| `assess sample_merchant` | PASS (`100`, `PROCEED`) |
| `assess-partner sample_partner` | PASS (`99`, `PROCEED`) |
| `assess-vendor sample_vendor` | PASS (`96`, `APPROVED`) |
| `assess-ai sample_ai` | PASS (`16`, `LOW`) |
| `negative_1` missing file validate | PASS (fails as expected) |
| `negative_2` wrong schema for assess-partner | PASS (fails as expected) |

## State-Reuse Regression Check
Source: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/state_reuse_check.json`

- Same `Assessor` instance:
  - First: `saku-rupiah` -> `REJECT`, trigger `NO_BI_LICENSE`
  - Second: `koinworks` -> `PROCEED`, triggers `[]`

Result: state contamination issue is resolved.

## Output Locations (Post-Fix)
- Results JSON: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/results`
- Reports MD: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/reports`
- Generated samples: `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/samples`
- Summaries:
  - `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/merchant_summary.json`
  - `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/cross_type_summary.json`
  - `/Users/suryaf/projects/risk_assessment_engine/qa_runs/postfix-2026-02-22/state_reuse_check.json`

## Final Status
- All requested fixes implemented.
- Merchant scoring regression resolved.
- Partner/Vendor/AI command failures resolved.
- Assessor state-leak resolved.
- Post-fix retest completed and saved in separate folder.
