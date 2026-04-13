---
title: Wrongful Death Cases Skip Treatment Phase
slug: wrongful-death-skips-treatment-phase
phase: [phase_0_onboarding, phase_1_file_setup, phase_7_litigation]
category: connection
tags: [wrongful-death, phase-transition, investigation, treatment-bypass]
confidence: low
evidence_count: 2
created: 2026-04-12
updated: 2026-04-12
related:
  - wrongful-death-case-patterns
  - case-phase-transitions
  - expert-reports-and-evaluations
---

# Wrongful Death Cases Skip Treatment Phase

> Wrongful death cases fundamentally alter the standard PI case lifecycle by eliminating the treatment phase entirely. Since the decedent has no ongoing medical treatment, the case moves directly from file setup into investigation and litigation. This phase skip means the standard PHASE_DAG milestones for treatment completion, records collection, and demand preparation are replaced by investigation milestones, expert retention, and early litigation filing.

## Pattern

In standard PI cases, the treatment phase (Phase 2) is the longest and most resource-intensive phase — monitoring treatment, collecting records, and waiting for maximum medical improvement. In wrongful death cases, this entire phase is bypassed:

- **No medical records to collect** (unless pre-death treatment exists)
- **No treatment completion milestone** — the triggering event for demand
- **Investigation replaces treatment** as the primary activity after file setup
- **Expert work shifts** from FCE/IME to vocational economics and accident reconstruction
- **Litigation filing is often earlier** since there is no treatment completion to wait for

This phase skip has cascading effects on case management automation: any PHASE_DAG logic that gates demand on treatment completion or records collection must account for the wrongful death exception.

## Evidence

- In a wrongful death case (DOI 2/2022), the decedent was pronounced dead at the scene. No medical records existed. The case moved from intake directly to insurance claim setup, investigation ($20K+ in investigation services), and litigation (complaint filed in circuit court). The standard treatment/records/demand pipeline was entirely bypassed. Expert work focused on vocational economics ($3.2K) and accident reconstruction ($2K) rather than medical evaluations.

## Related

- [[wrongful-death-case-patterns]] — the full wrongful death case lifecycle
- [[case-phase-transitions]] — standard phase transitions do not apply to wrongful death
- [[expert-reports-and-evaluations]] — expert focus shifts from medical to economic/reconstruction
