# Quick Start Guide

## Installation

1. **Extract** the `risk_assessment_engine` folder
2. **Open terminal** and navigate to the folder:
   ```bash
   cd risk_assessment_engine
   ```
3. **Run setup**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   source .venv/bin/activate
   ```

## Conducting an Assessment

### Step 1: Research the Merchant

Gather information from:
- Website
- Play Store / App Store
- Google Search
- BI Registry (for PJP/Aggregators): https://www.bi.go.id/id/layanan/informasi-perizinan/sistem-pembayaran/default.aspx

### Step 2: Fill in Research Data

1. Copy the template:
   ```bash
   cp templates/research_template.json my-merchant.json
   ```

2. Edit `my-merchant.json` and fill in all fields

### Step 3: Run Assessment

```bash
python -m risk_assessment_engine assess my-merchant.json -o result.json -r report.md
```

### Optional: Validate Partner/Vendor/AI Inputs

```bash
python -m risk_assessment_engine validate-partner partner_data.json
python -m risk_assessment_engine validate-vendor vendor_data.json
python -m risk_assessment_engine validate-ai ai_project_data.json
```

### Step 4: Review Report

Open `report.md` to see the full assessment report.

## Key Classification

| Type | Definition | Regulatory Requirement |
|------|------------|----------------------|
| **Regular Merchant** | Receives payments for OWN products/services | N/A - Auto-pass on Parameter B |
| **PJP / Aggregator** | Processes payments for OTHER merchants | **BI PJP License REQUIRED** |

## BI License Verification (for PJP/Aggregators)

1. Go to: https://www.bi.go.id/id/layanan/informasi-perizinan/sistem-pembayaran/default.aspx
2. Search by company name
3. Fill in the `parameter_b` section with:
   - `bi_registry_checked`: true
   - `bi_registry_found`: true/false
   - Other registry details

See `docs/BI-LICENSE-VERIFICATION-GUIDE.md` for detailed instructions.

## Test Cases

Run these to verify the engine is working:

```bash
# Regular Merchant - PROCEED WITH CONDITIONS
python -m risk_assessment_engine assess tests/tiga-pilar-media-research.json

# PJP without license - REJECT
python -m risk_assessment_engine assess tests/saku-rupiah-research.json

# PJP with old license not found - REJECT
python -m risk_assessment_engine assess tests/andapay-research.json
```

## Decision Bands

| Score | Decision | Action |
|-------|----------|--------|
| 80-100 | PROCEED | Standard onboarding |
| 60-79 | PROCEED WITH CONDITIONS | Address conditions within timeline |
| 40-59 | CONDITIONAL REJECT | Risk Committee review required |
| 0-39 | REJECT | Not suitable for onboarding |

## Support

- Documentation: `README.md`, `docs/`
- Test cases: `tests/`
- Template: `templates/research_template.json`
