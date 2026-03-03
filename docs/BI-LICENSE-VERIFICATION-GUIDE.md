# BI License Verification Guide

## Overview

This guide provides step-by-step instructions for verifying Bank Indonesia (BI) PJP licenses during the merchant risk assessment research phase.

## BI License Registry

**URL:** https://www.bi.go.id/id/layanan/informasi-perizinan/sistem-pembayaran/default.aspx

## License Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **PJP Kategori 1** | Principal License - Full payment services | E-wallet issuers, Payment gateways with own infrastructure |
| **PJP Kategori 2** | Limited License - Specific services | Money transfer, Virtual account providers |
| **PJP Kategori 3** | Narrow License - Single service | Remittance, Bill payment aggregators |
| **PTD** | Penyelenggara Transfer Dana | Domestic/international money transfer |
| **PVA** | Penukar Valuta Asing | Foreign exchange services |
| **QRIS** | QRIS Participants | QR payment acquirers |

## License Format Reference

### Current Format (Post-2016)
```
Format: XX/X/KEP.GBI/XXX/YYYY
Example: 28/2/KEP.GBI/Btm/2026
```

### Old Format (Pre-2016) - *May No Longer Be Valid*
```
Format: XX/XX/XXXX/XX
Example: 13/83/DASP/33
```

**Important:** Old format licenses should have been converted to new PJP categories after PBI 18/40/PBI/2016. If a merchant claims an old-format license, verify:
1. Has it been converted to new category?
2. Has it been revoked?
3. Has it expired?

## Verification Steps

### Step 1: Access BI Registry
1. Open: https://www.bi.go.id/id/layanan/informasi-perizinan/sistem-pembayaran/default.aspx
2. Wait for the page to fully load (JavaScript-heavy)

### Step 2: Search by Company Name
1. Use the **Pencarian** (Search) box
2. Enter the company name (e.g., "PT Andalusia Antar Benua")
3. Try variations: full name, short name, without "PT"

### Step 3: Filter by Category
If you know the merchant type:
- Payment Gateway/Aggregator → PJP Kategori 1, 2, or 3
- Money Transfer → PTD
- Foreign Exchange → PVA

### Step 4: Check All Status Filters
1. **Berizin (Telah Operasional)** - Licensed and operational
2. **Berizin (Belum Operasional)** - Licensed but not yet operational
3. **Terdaftar** - Registered (not full license)
4. **Izin Dicabut** - License revoked **(IMPORTANT TO CHECK!)**

### Step 5: Record Findings

If **FOUND**, record in `research_data.json`:

```json
"parameter_b": {
  "is_pjp_or_aggregator": true,
  "bi_license_verified": true,
  "bi_license_number": "XX/X/KEP.GBI/XXX/YYYY",
  "bi_registry_checked": true,
  "bi_registry_found": true,
  "bi_registry_category": "Penyedia Jasa Pembayaran - Kategori Izin 3",
  "bi_registry_license_number": "004.6796-001/79",
  "bi_registry_decision_number": "28/2/KEP.GBI/Btm/2026",
  "bi_registry_date": "15 Januari 2026",
  "bi_registry_status": "Berizin (Telah Operasional)",
  "bi_registry_url": "https://www.bi.go.id/id/qrcode/validate.aspx?tipe=PTD&id=004.6796-001/79",
  "bi_verification_notes": "License verified in BI registry. Active and operational."
}
```

If **NOT FOUND**, record:

```json
"parameter_b": {
  "is_pjp_or_aggregator": true,
  "bi_license_verified": false,
  "bi_license_number": "13/83/DASP/33",
  "bi_registry_checked": true,
  "bi_registry_found": false,
  "bi_registry_category": null,
  "bi_registry_license_number": null,
  "bi_registry_decision_number": null,
  "bi_registry_date": null,
  "bi_registry_status": null,
  "bi_registry_url": null,
  "bi_verification_notes": "BI Registry checked on [DATE]. License NOT FOUND. Old format license (13/83/DASP/33) from pre-2016 may have been revoked or expired."
}
```

## Scoring Impact

| Verification Status | Score (PJP) | Action |
|---------------------|-------------|--------|
| Registry VERIFIED + Operational | 23-25 pts | PROCEED |
| Registry VERIFIED + Not Operational | 20 pts | PROCEED WITH CONDITIONS |
| Registry VERIFIED + Revoked | 0 pts | AUTO-REJECT |
| Registry NOT FOUND | 0 pts | AUTO-REJECT |
| Registry NOT CHECKED + Claimed | 8-14 pts | PENDING VERIFICATION |
| Registry NOT CHECKED + No Claim | 0 pts | AUTO-REJECT |

## Common Issues

### Issue 1: Old Format License
**Problem:** Merchant claims license like "13/83/DASP/33"

**Solution:**
1. Search for company name (not license number)
2. Check if license was converted to new category
3. If not found, may be revoked/expired
4. Document in `bi_verification_notes`

### Issue 2: License Under Different Name
**Problem:** License exists but under parent company or different legal entity

**Solution:**
1. Search for parent company name
2. Verify relationship between companies
3. Document the connection

### Issue 3: Recently Issued License
**Problem:** License was just issued and not yet in registry

**Solution:**
1. Ask merchant for official BI decision letter
2. Set `bi_registry_checked: false`
3. Set `bi_license_number` from document
4. Flag for manual follow-up

## Verification Checklist

- [ ] Access BI registry URL
- [ ] Search by company name (all variations)
- [ ] Search by license number (if provided)
- [ ] Check all status filters including "Izin Dicabut"
- [ ] Click on company name to view details
- [ ] Record all findings in research_data.json
- [ ] Take screenshot as evidence
- [ ] Set `bi_registry_checked: true`

## Example: Andapay Verification

**Merchant:** Andapay (PT Andalusia Antar Benua)  
**Claimed License:** 13/83/DASP/33 (June 2011)

**Verification Process:**
1. Searched "Andalusia" in BI registry - NO RESULTS
2. Searched "Andapay" in BI registry - NO RESULTS
3. License format is OLD (pre-2016)
4. Checked "Izin Dicabut" filter - NOT FOUND

**Result:** NOT FOUND in registry

**Assessment Impact:**
- Score: 0/25 for Parameter B
- Auto-Reject triggered: `NO_BI_LICENSE_REGISTRY`
- Decision: REJECT

---

*Last Updated: February 2026*  
*Framework Version: 2.1*
