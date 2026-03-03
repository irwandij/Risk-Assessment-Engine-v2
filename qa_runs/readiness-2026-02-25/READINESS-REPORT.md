# Readiness Report - Risk Assessment Engine

## Status
- READY for assessments with `.venv` Python 3.14 environment.
- All requested checks completed: dependency/import, CLI, web endpoints, automated tests.

## Installed Versions
- python: Python 3.14.3
- pip: pip 26.0.1 from /Users/suryaf/projects/risk_assessment_engine/.venv/lib/python3.14/site-packages/pip (python 3.14)
- pydantic: 2.12.5
- fastapi: 0.133.0
- uvicorn: 0.41.0
- jinja2: 3.1.6
- multipart: 0.0.22
- pytest: 9.0.2
- httpx: 0.28.1

## Verification Summary
- Runtime import checks: PASS (`pydantic`, `fastapi`, `uvicorn`, `jinja2`, `multipart`, `pytest`, `httpx`).
- CLI sample generation: PASS (`merchant`, `partner`, `vendor`, `ai`).
- CLI validate: PASS (`tests/tiga-pilar-media-research.json`).
- Web API health: PASS (`/api/health` => `status=ok`).
- Web API form config: PASS (all types).
- Web API assess: PASS (all types; expected payload fields returned).
- Web API negative tests: PASS (`unknown` => 404, invalid merchant payload => 422).
- Automated tests: PASS (`11 passed, 1 warning`).

## CLI Assessment Outputs (Sample)
- koinworks-result.json: Koinworks | score=100 | risk=LOW | decision=PROCEED | triggers=-
- tiga-pilar-media-result.json: PT Tiga Pilar Media | score=67 | risk=MEDIUM | decision=PROCEED WITH CONDITIONS | triggers=-
- saku-rupiah-result.json: Saku Rupiah | score=47 | risk=VERY HIGH | decision=REJECT | triggers=NO_BI_LICENSE
- andapay-result.json: Andapay | score=28 | risk=VERY HIGH | decision=REJECT | triggers=NO_BI_LICENSE_REGISTRY
- sample_partner_result.json: PT Sample Partner | score=99 | risk=LOW | decision=PROCEED | triggers=-
- sample_vendor_result.json: PT Sample Vendor | score=96 | risk=LOW | decision=APPROVED | triggers=-
- sample_ai_result.json: Sample AI Project | score=16 | risk=LOW | decision=LOW | triggers=-

## Findings and Remediation
- Python 3.9 is not compatible with this codebase due to Python 3.10+ type-union syntax (`|`) used in models.
- Remediation applied: standardized runtime to Python 3.14 in `.venv`; documentation updated to Python 3.10+ minimum.
- Missing test dependency (`httpx`) caused initial pytest collection failure; added to `requirements.txt`.

## Canonical Operator Commands
```bash
cd /Users/suryaf/projects/risk_assessment_engine
source .venv/bin/activate
python -m risk_assessment_engine assess tests/koinworks-research.json -o result.json -r report.md
python start_web.py  # http://127.0.0.1:8080
pytest -q
```
