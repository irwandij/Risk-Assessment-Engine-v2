# Risk Assessment Engine

A Python-based merchant risk assessment framework for evaluating merchants applying for autodebit services.

## Features

- **9-Parameter Scoring System** (100 points total)
- **Merchant Type Classification** (Regular vs PJP/Aggregator)
- **BI License Verification** with registry check support
- **Auto-Reject Triggers** for regulatory non-compliance
- **Markdown Report Generation**
- **Web Wizard UI** for Merchant/Partner/Vendor/AI assessments

## Quick Start

```bash
# 1. Create and activate virtual environment (Python 3.10+)
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies and package
pip install -r requirements.txt
pip install -e .

# 3. Generate sample research data
python -m risk_assessment_engine sample -o my-merchant.json

# 4. Edit my-merchant.json with your research findings

# 5. Run assessment
python -m risk_assessment_engine assess my-merchant.json -o result.json -r report.md

# 6. Start local web UI (manual wizard)
python start_web.py
# open http://127.0.0.1:8080
```

## Installation

### Option 1: Direct Installation

```bash
cd risk_assessment_engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Option 2: Install as Package

```bash
cd risk_assessment_engine
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

### Generate Sample Research Data

```bash
python -m risk_assessment_engine sample -o new-merchant.json
```

### Validate Research Data

```bash
python -m risk_assessment_engine validate new-merchant.json
```

### Validate Partner/Vendor/AI Data

```bash
python -m risk_assessment_engine validate-partner partner_data.json
python -m risk_assessment_engine validate-vendor vendor_data.json
python -m risk_assessment_engine validate-ai ai_project_data.json
```

### Run Assessment

```bash
python -m risk_assessment_engine assess new-merchant.json -o result.json -r report.md
```

**Options:**
- `-o, --output` - Output JSON result file
- `-r, --report` - Output markdown report file

### Run Web Wizard (HTML)

```bash
cd risk_assessment_engine
source .venv/bin/activate
python start_web.py
```

Then open: `http://127.0.0.1:8080`

Web API endpoints:
- `GET /`
- `GET /api/health`
- `GET /api/form-config/{assessment_type}` where `{assessment_type}` is `merchant`, `partner`, `vendor`, or `ai`
- `POST /api/assess/{assessment_type}`

Web constraints (v1):
- Local-only runtime (`127.0.0.1`)
- No persistence
- Manual form entry only
- English UI

## Project Structure

```
risk_assessment_engine/
├── config.py              # Scoring thresholds, decision bands
├── main.py                # CLI entry point
├── models/
│   ├── research_data.py   # Input schema (research findings)
│   └── assessment_result.py
├── scorers/
│   ├── parameter_a.py     # Company Identity (15 pts)
│   ├── parameter_b.py     # Regulatory (25 pts)
│   ├── parameter_c.py     # Product Clarity (10 pts)
│   ├── parameter_d.py     # Payment Transparency (15/10 pts)
│   ├── parameter_e.py     # T&C Completeness (15/10 pts)
│   ├── parameter_f.py     # Consumer Protection (10 pts)
│   ├── parameter_g.py     # Privacy & PDP (10 pts)
│   ├── parameter_h.py     # Security (5 pts)
│   └── parameter_i.py     # Reputation (5 pts)
├── engine/
│   ├── classifier.py      # Merchant type classification
│   ├── assessor.py        # Main orchestration
│   └── decision.py        # Decision bands + auto-reject
├── generators/
│   └── report_generator.py
├── docs/
│   └── BI-LICENSE-VERIFICATION-GUIDE.md
└── tests/                 # Test cases and examples
```

## Scoring Framework

### Merchant Types

| Type | Description | Regulatory Requirement |
|------|-------------|----------------------|
| **Regular Merchant** | Receives payments for OWN products/services | N/A |
| **PJP / Aggregator** | Processes payments for OTHER merchants | BI PJP License REQUIRED |

### Parameter Weights

| # | Parameter | Regular | PJP |
|---|-----------|---------|-----|
| A | Company Identity | 15 pts | 15 pts |
| B | Regulatory | 25 pts (auto-pass) | 25 pts |
| C | Product Clarity | 10 pts | 10 pts |
| D | Payment Transparency | 15 pts | 10 pts |
| E | T&C Completeness | 15 pts | 10 pts |
| F | Consumer Protection | 10 pts | 10 pts |
| G | Privacy & PDP | 10 pts | 10 pts |
| H | Security | 5 pts | 5 pts |
| I | Reputation | 5 pts | 5 pts |
| **Total** | | **100 pts** | **100 pts** |

### Decision Bands

| Score | Decision |
|-------|----------|
| 80-100 | PROCEED |
| 60-79 | PROCEED WITH CONDITIONS |
| 40-59 | CONDITIONAL REJECT |
| 0-39 | REJECT |

### Auto-Reject Triggers

- **NO_BI_LICENSE**: PJP/Aggregator without verifiable BI license
- **NO_ONLINE_PRESENCE**: No functioning website and no social media
- **CONFIRMED_FRAUD**: Confirmed fraud/scam or regulatory enforcement
- **LOW_APP_RATING**: App rating <3.0 with serious negative news
- **NON_SUBSCRIPTION_MODEL**: Non-subscription model for autodebit
- **SCORE_TOO_LOW**: Total score below 40

## BI License Verification

For PJP/Aggregators, verify the BI license before assessment:

1. **BI Registry URL:** https://www.bi.go.id/id/layanan/informasi-perizinan/sistem-pembayaran/default.aspx
2. **Search** by company name
3. **Record** findings in research data (see `docs/BI-LICENSE-VERIFICATION-GUIDE.md`)

**Key fields to fill:**
```json
{
  "parameter_b": {
    "bi_registry_checked": true,
    "bi_registry_found": true/false,
    "bi_registry_category": "Penyedia Jasa Pembayaran - Kategori Izin 3",
    "bi_registry_license_number": "...",
    "bi_registry_status": "Berizin (Telah Operasional)",
    "bi_verification_notes": "..."
  }
}
```

## Research Data Template

See `templates/research_template.json` for a complete template.

### Required Fields

```json
{
  "merchant_info": {
    "name": "Merchant Name",
    "website": "https://example.com",
    "business_type": "Business Type",
    "processes_payments_for_others": false,
    "subscription_model": true
  },
  "parameter_a": { ... },
  "parameter_b": { ... },
  ...
}
```

## Test Cases

Run existing test cases:

```bash
# Tiga Pilar Media (Regular Merchant)
python -m risk_assessment_engine assess tests/tiga-pilar-media-research.json

# Koinworks (Regular Merchant - High Score)
python -m risk_assessment_engine assess tests/koinworks-research.json

# Saku Rupiah (PJP - REJECT)
python -m risk_assessment_engine assess tests/saku-rupiah-research.json

# Andapay (PJP - REJECT, license not verified)
python -m risk_assessment_engine assess tests/andapay-research.json
```

## Dependencies

- Python 3.10+
- pydantic >= 2.0.0

## Version

- Framework: v2.1
- Engine: v1.0.0

## License

Internal use - DANA Indonesia Risk Management Team
