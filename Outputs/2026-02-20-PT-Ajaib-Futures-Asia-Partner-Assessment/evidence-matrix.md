# Evidence Matrix — PT Ajaib Futures Asia (Partner)

This matrix maps each **affirmative (true)** field in `partner_input.json` to a concrete evidence source.

## Partner profile

- `partner_info.name` → `[Confidential] DANA Business Partner Due Diligence Checklist.pdf` p.1 (Business Partner Name)
- `partner_info.website` → https://www.ajaibfuturesasia.co.id/ (captured 2026-02-26 09:04:59 UTC; snapshot `tmp/web-snapshots/20260226T090152Z/ajaibfuturesasia_home.html`)
- `partner_info.partnership_type` → `Inputs/Re_ [Request Review] Due Diligence Form by Ajaib (Offshore Stock).eml` (2026-02-20) states host-to-host integration initiative
- `partner_info.registration_number` → `[Confidential] ... Checklist.pdf` p.1 (NIB listed)
- `partner_info.address` → Bappebti list_pialang JSON row for “AJAIB FUTURES ASIA” (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`) and `[Confidential] ... Checklist.pdf` p.3 (registered address)

## Parameter A — Company Profile

- `parameter_a.has_legal_entity=true` → `[Confidential] ... Checklist.pdf` p.1 (legal docs marked available) + Bappebti list_pialang (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`)
- `parameter_a.registration_verified=true` → Bappebti list_pialang includes “AJAIB FUTURES ASIA” with SIUP (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`)
- `parameter_a.has_address=true` → `[Confidential] ... Checklist.pdf` p.3 + Bappebti list_pialang (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`)
- `parameter_a.ownership_structure_clear=true` → `[Confidential] ... Checklist.pdf` p.4 (ownership type marked privately owned; principal owner details provided)
- `parameter_a.beneficial_owners_identified=true` → `[Confidential] ... Checklist.pdf` p.4 (principal owner name provided)

## Parameter D — Operational Capability

- `parameter_d.has_track_record=true` → Bappebti listing as active Pialang Berjangka (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`)
- `parameter_d.has_expertise=true` → Bappebti listing as licensed Pialang Berjangka (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`)
- `parameter_d.has_adequate_resources=true` → `[DANA] Struktur Organisasi PT Ajaib Futures Asia.pdf` (multi-division org structure incl. operations/compliance/risk/IT)
- `parameter_d.operational_processes_documented=true` → `[Confidential] ... Checklist.pdf` p.2–3 (risk management function/policy/system; BCM/DR; fraud management marked “Yes”)

## Parameter E — Regulatory Compliance

- `parameter_e.has_required_licenses=true` → `[Confidential] ... Checklist.pdf` p.1 (license number listed) + Bappebti list_pialang (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`)
- `parameter_e.licenses_verified=true` → Bappebti list_pialang (snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang.json`)
- `parameter_e.no_regulatory_issues=true` → `[Confidential] ... Checklist.pdf` p.1 (no pending legal actions / non-compliance indicated) and p.8 (enforcement/investigation marked “No”) + negative check vs revoked list snapshot `tmp/web-snapshots/20260226T090152Z/bappebti_list_pialang_cabut.json`
- `parameter_e.compliance_program_exists=true` → `[Confidential] ... Checklist.pdf` p.5–8 (AML/CTF programme components marked “Yes”)
- `parameter_e.aml_kyc_compliant=true` → `[Confidential] ... Checklist.pdf` p.7–8 (KYC/CDD/EDD process questions marked “Yes”)
- `parameter_e.no_legal_issues=true` → `[Confidential] ... Checklist.pdf` p.1 (pending legal actions marked “No”) and p.8 (enforcement/investigation marked “No”)

