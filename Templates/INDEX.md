# Template Index

Authoritative list of every form template in `Templates/`. This file is the contract between skills and the firm template library — when a skill needs to fill a form, it should look here first to find the right template slug.

**Conventions.** Templates are stored at the vault root in `Templates/<slug>.{docx,pdf}`. Slug filenames follow the rules in `skills.tools.workflows/DATA_CONTRACT.md` §4. A few templates have a companion `<slug>.yaml` describing the placeholder fields and where their values come from. Most do not yet — adding placeholder mappings is a Week-2 follow-up.

> ⚠️ The 17 existing `.yaml` mappings reference Cypher queries against a deleted FalkorDB graph. Their declared field sources are stale; treat the `.yaml` files as documentation of *what* the template needs, not *how* to get it. The vault is the source of truth (see `skills.tools.workflows/DATA_CONTRACT.md`); placeholder resolution will be rewritten to read frontmatter and wikilinks instead of Cypher.

---

## Quick stats

- **73** total templates
- **19** with placeholder mapping (`.yaml` companion)
- **17** mappings using stale graph queries (need rewrite)

## Intake
_Client intake forms, fee agreements, authorizations gathered at the start of a matter._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `authorization-of-digitally-signature-replication` | `Templates/authorization-of-digitally-signature-replication.pdf` (PDF) | Authorization of Digitally Signature Replication |  |
| `cms-medicare-verification-form` | `Templates/cms-medicare-verification-form.pdf` (PDF) | Cms Medicare Verification Form |  |
| `employment-information-authorization` | `Templates/employment-information-authorization.pdf` (PDF) | Employment Information Authorization |  |
| `medical-authorization-hipaa` | `Templates/medical-authorization-hipaa.pdf` (PDF) | Medical Authorization Hipaa |  |
| `medical-treatment-questionnaire` | `Templates/medical-treatment-questionnaire.pdf` (PDF) | Medical Treatment Questionnaire |  |
| `mva-accident-detail-information-sheet` | `Templates/mva-accident-detail-information-sheet.pdf` (PDF) | Mva Accident Detail Information Sheet |  |
| `mva-client-intake-packet-adult` | `Templates/mva-client-intake-packet-adult.pdf` (PDF) | Mva Client Intake Packet Adult |  |
| `mva-client-intake-packet-minor` | `Templates/mva-client-intake-packet-minor.pdf` (PDF) | Mva Client Intake Packet Minor |  |
| `mva-fee-agreement` | `Templates/mva-fee-agreement.pdf` (PDF) | Mva Fee Agreement |  |
| `new-client-information-sheet` | `Templates/new-client-information-sheet.pdf` (PDF) | New Client Information Sheet |  |
| `non-solicitation-affidavit` | `Templates/non-solicitation-affidavit.pdf` (PDF) | Non Solicitation Affidavit |  |
| `preliminary-lost-wage-application` | `Templates/preliminary-lost-wage-application.pdf` (PDF) | Preliminary Lost Wage Application |  |
| `sandf-accident-detail-information-sheet` | `Templates/sandf-accident-detail-information-sheet.pdf` (PDF) | Sandf Accident Detail Information Sheet |  |
| `sandf-client-intake-packet-adult` | `Templates/sandf-client-intake-packet-adult.pdf` (PDF) | Sandf Client Intake Packet Adult |  |
| `sandf-fee-agreement` | `Templates/sandf-fee-agreement.pdf` (PDF) | Sandf Fee Agreement |  |
| `wage-and-salary-verification` | `Templates/wage-and-salary-verification.pdf` (PDF) | Wage and Salary Verification |  |
| `wc-client-intake-packet-adult` | `Templates/wc-client-intake-packet-adult.pdf` (PDF) | Wc Client Intake Packet Adult |  |
| `wc-fee-agreement-final` | `Templates/wc-fee-agreement-final.pdf` (PDF) | Wc Fee Agreement Final |  |

## Correspondence
_Letters sent to insurance adjusters and other parties._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `attorney-lien-notice` | `Templates/attorney-lien-notice.docx` (DOCX) | Notice of attorney lien to BI adjuster and new counsel when client changes representation, asserting lien pursuant to KR | ⚠ stale yaml |
| `blank-letter-bi-adjuster` | `Templates/blank-letter-bi-adjuster.docx` (DOCX) | General-purpose blank letter template for correspondence to bodily injury insurance adjuster with pre-filled case detail | ⚠ stale yaml |
| `blank-letter-pip-adjuster` | `Templates/blank-letter-pip-adjuster.docx` (DOCX) | General-purpose correspondence to PIP insurance adjuster for client matters | ✓ yaml |
| `blank-letter-to-pip-adjuster` | `Templates/blank-letter-to-pip-adjuster.docx` (DOCX) | Blank Letter to Pip Adjuster |  |
| `blank-ltr-to-bi-adjuster` | `Templates/blank-ltr-to-bi-adjuster.docx` (DOCX) | Blank Ltr to Bi Adjuster |  |
| `coots-letter` | `Templates/coots-letter.docx` (DOCX) | Coots Letter |  |
| `coots-letter-to-uim-adjuster` | `Templates/coots-letter-to-uim-adjuster.docx` (DOCX) | Coots Letter to Uim Adjuster |  |
| `coots-letter-uim` | `Templates/coots-letter-uim.docx` (DOCX) | Certificate of Other Coverage (COOTs) letter to UIM adjuster notifying them of settlement offer from at-fault driver's i | ⚠ stale yaml |
| `coots-ltr` | `Templates/coots-ltr.docx` (DOCX) | Coots Ltr |  |
| `initial-lien-request` | `Templates/initial-lien-request.docx` (DOCX) | Initial request for lien amount from medical provider before settlement | ⚠ stale yaml |
| `letter-of-rep-bi-adjuster` | `Templates/letter-of-rep-bi-adjuster.docx` (DOCX) | Initial letter of representation sent to bodily injury insurance adjuster to formally notify them of client representati | ⚠ stale yaml |
| `letter-of-rep-pip-adjuster` | `Templates/letter-of-rep-pip-adjuster.docx` (DOCX) | Initial letter of representation sent to PIP insurance adjuster to formally notify them of client representation and res | ⚠ stale yaml |
| `lor-prior-attorney-file-request` | `Templates/lor-prior-attorney-file-request.docx` (DOCX) | Notifies prior attorney of new representation and requests case file transfer | ⚠ stale yaml |
| `lor-to-bi-adjuster` | `Templates/lor-to-bi-adjuster.docx` (DOCX) | Lor to Bi Adjuster |  |
| `lor-to-pip-adjuster` | `Templates/lor-to-pip-adjuster.docx` (DOCX) | Lor to Pip Adjuster |  |
| `lor-to-prior-attorney-wfile-request-language` | `Templates/lor-to-prior-attorney-wfile-request-language.docx` (DOCX) | Lor to Prior Attorney Wfile Request Language |  |
| `medical-billing-request` | `Templates/medical-billing-request.docx` (DOCX) | Request for itemized medical billing records from healthcare provider for workers compensation or personal injury case | ⚠ stale yaml |
| `medical-record-request` | `Templates/medical-record-request.docx` (DOCX) | Formal request for complete medical records from healthcare provider for personal injury case | ⚠ stale yaml |
| `pip-direction-letter` | `Templates/pip-direction-letter.docx` (DOCX) | Letter directing PIP adjuster on benefit handling and payment instructions after lifting reservation | ⚠ stale yaml |
| `request-declaration-page-bi` | `Templates/request-declaration-page-bi.docx` (DOCX) | Request letter for insurance policy declaration page from bodily injury adjuster (follow-up to initial letter of represe | ⚠ stale yaml |
| `request-pip-ledger` | `Templates/request-pip-ledger.docx` (DOCX) | Request letter for updated PIP benefits ledger from PIP adjuster | ⚠ stale yaml |

## Medical Records
_Forms for requesting medical bills and records from providers._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `initial-medical-billing-request-to-provider-mbr` | `Templates/initial-medical-billing-request-to-provider-mbr.pdf` (PDF) | Initial Medical Billing Request to Provider Mbr |  |
| `initial-wc-medical-billing-request-to-provider-mbr` | `Templates/initial-wc-medical-billing-request-to-provider-mbr.docx` (DOCX) | Initial Wc Medical Billing Request to Provider Mbr |  |
| `law-firm-medical-request-template` | `Templates/law-firm-medical-request-template.pdf` (PDF) | Law Firm Medical Request Template |  |
| `medical-bill` | `Templates/medical-bill.docx` (DOCX) | Medical Bill |  |
| `medical-record-request-urr` | `Templates/medical-record-request-urr.docx` (DOCX) | Medical Record Request Urr |  |
| `wc-medical-record-request-irr` | `Templates/wc-medical-record-request-irr.docx` (DOCX) | Wc Medical Record Request Irr |  |

## Insurance
_PIP application, declarations-page requests, and other carrier-facing forms._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `fillable-pip-application` | `Templates/fillable-pip-application.pdf` (PDF) | Fillable Pip Application |  |
| `jefferson-county-clerk-insurance-request-form` | `Templates/jefferson-county-clerk-insurance-request-form.docx` (DOCX) | Jefferson County Clerk Insurance Request Form |  |
| `kacp-application-03-2021` | `Templates/kacp-application-03-2021.pdf` (PDF) | Kacp Application 03 2021 |  |
| `pip-direction-letter-2` | `Templates/pip-direction-letter-2.docx` (DOCX) | Pip Direction Letter 2 |  |
| `request-for-declaration-page-to-bi-adjuster` | `Templates/request-for-declaration-page-to-bi-adjuster.docx` (DOCX) | Request for Declaration Page to Bi Adjuster |  |
| `request-for-updated-pip-ledger` | `Templates/request-for-updated-pip-ledger.docx` (DOCX) | Request for Updated Pip Ledger |  |
| `state-of-ky-vehicle-information-request-tc-96-16a` | `Templates/state-of-ky-vehicle-information-request-tc-96-16a.pdf` (PDF) | State of Ky Vehicle Information Request Tc 96 16a |  |

## Lien Management
_Lien identification, initial request, negotiation, and final payoff letters._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `1st-bi-offer-to-client` | `Templates/1st-bi-offer-to-client.docx` (DOCX) | 1st Bi Offer to Client |  |
| `attorney-lien-notice-to-bi-and-new-counsel` | `Templates/attorney-lien-notice-to-bi-and-new-counsel.docx` (DOCX) | Attorney Lien Notice to Bi and New Counsel |  |
| `declined-rep-notice-to-client` | `Templates/declined-rep-notice-to-client.docx` (DOCX) | Declined Rep Notice to Client |  |
| `final-lien-request` | `Templates/final-lien-request.docx` (DOCX) | Final/urgent follow-up request for lien amount from medical provider. Used when initial requests have not received a res | ✓ yaml |
| `final-lien-request-2` | `Templates/final-lien-request-2.docx` (DOCX) | Final Lien Request 2 |  |
| `initial-lien-request-2` | `Templates/initial-lien-request-2.docx` (DOCX) | Initial Lien Request 2 |  |
| `notice-of-deposition-to-client` | `Templates/notice-of-deposition-to-client.docx` (DOCX) | Notice of Deposition to Client |  |
| `notice-of-dme-to-client` | `Templates/notice-of-dme-to-client.docx` (DOCX) | Notice of Dme to Client |  |
| `thank-you-ltr-to-client-case-manager-assigned` | `Templates/thank-you-ltr-to-client-case-manager-assigned.docx` (DOCX) | Thank You Ltr to Client Case Manager Assigned |  |

## Litigation
_Complaints, civil cover sheets, and litigation-phase notices._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `deposition-notice-client` | `Templates/deposition-notice-client.docx` (DOCX) | Letter notifying client of their scheduled deposition with preparation instructions | ⚠ stale yaml |
| `dme-notice-client` | `Templates/dme-notice-client.docx` (DOCX) | Letter notifying client of scheduled Independent Medical Examination (Defense Medical Exam) | ⚠ stale yaml |
| `mva-complaint-basic` | `Templates/mva-complaint-basic.docx` (DOCX) | Mva Complaint Basic |  |
| `mva-complaint-standard` | `Templates/mva-complaint-standard.docx` (DOCX) | Mva Complaint Standard |  |
| `mva-complaint-um` | `Templates/mva-complaint-um.docx` (DOCX) | Mva Complaint Um |  |
| `mva-litigation-ky-aoc-104-civil-case-cover-sheet` | `Templates/mva-litigation-ky-aoc-104-civil-case-cover-sheet.pdf` (PDF) | Mva Litigation Ky Aoc 104 Civil Case Cover Sheet |  |
| `premise-liability-complaint-template` | `Templates/premise-liability-complaint-template.docx` (DOCX) | Premise Liability Complaint Template |  |

## Client Communication
_Letters and notices sent directly to the client._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `declined-representation` | `Templates/declined-representation.docx` (DOCX) | Letter to client declining or withdrawing representation | ⚠ stale yaml |
| `settlement-offer-client` | `Templates/settlement-offer-client.docx` (DOCX) | Letter to client presenting first settlement offer from insurance company | ⚠ stale yaml |
| `thank-you-client` | `Templates/thank-you-client.docx` (DOCX) | Thank you letter sent to client after case manager is assigned to their case | ⚠ stale yaml |

## Investigation
_Open records requests and other discovery of fact._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `orr-to-public-works` | `Templates/orr-to-public-works.docx` (DOCX) | Orr to Public Works |  |

## System
_Boilerplate and shared assets used across templates._

| Slug | File | Purpose | Placeholders |
|------|------|---------|--------------|
| `letterhead` | `Templates/letterhead.docx` (DOCX) | Letterhead |  |

## How skills should reference templates

```yaml
# In a workflow.md or SKILL.md frontmatter:
templates:
  - Templates/letter-of-rep-bi-adjuster.docx
  - Templates/kacp-application-03-2021.pdf
```

In skill prose, refer to a template by its slug (without extension) and link it as a standard markdown link or vault wikilink:

```markdown
Use the [letter of representation to BI adjuster](../../Templates/letter-of-rep-bi-adjuster.docx) template, fill the placeholder fields from the case file, and write the output to `cases/<slug>/documents/`.
```

**Never** copy templates into a skill, workflow, or case folder. Read them in place. Outputs go to `cases/<slug>/documents/`.

## Open work

1. **Rewrite the 17 stale `.yaml` mappings** to source field values from the vault (frontmatter + linked contact files) instead of Cypher graph queries.
2. **Add `.yaml` mappings** for the templates that don't yet have them (mostly intake/litigation forms).
3. **Decide intake-packet handling** — the multi-page intake packets are PDFs that get printed and signed; they don't need placeholder filling but skills should still be able to discover and send them.