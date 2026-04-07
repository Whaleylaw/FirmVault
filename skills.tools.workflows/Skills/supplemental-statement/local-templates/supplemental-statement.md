# Supplemental Settlement Statement

**Client:** {{client_name}}
**Case:** [[cases/{{case_slug}}/{{case_slug}}|{{client_name}} — {{case_type}} {{date_of_incident}}]]
**Date of Incident:** {{date_of_incident}}
**Original Settlement Date:** {{settlement_date}}
**Supplemental Statement Date:** {{today}}

---

## Reference — Original Settlement

| Item | Amount |
|---|---:|
| Gross Settlement | ${{gross}} |
| Attorney Fee ({{fee_rate}}%) | −${{fee}} |
| Case Costs | −${{costs_total}} |
| Lien Holdback (held in trust) | −${{original_holdback}} |
| **Initial Net to Client** | **${{initial_net}}** |

## Lien Resolution

| Lien Holder | Type | Held | Paid | Surplus |
|---|---|---:|---:|---:|
| {{holder}} | {{type}} | ${{held}} | ${{paid}} | ${{surplus}} |
| **Totals** | | **${{original_holdback}}** | **${{total_paid}}** | **${{total_surplus}}** |

## Additional Distribution

| Item | Amount |
|---|---:|
| Original holdback | ${{original_holdback}} |
| Liens actually paid | −${{total_paid}} |
| **Additional to Client** | **${{total_surplus}}** |

## Total Net to Client

| | Amount |
|---|---:|
| Initial distribution ({{settlement_date}}) | ${{initial_net}} |
| Additional distribution ({{today}}) | +${{total_surplus}} |
| **Total Net to Client** | **${{total_net}}** |

Trust balance after this distribution: **$0.00**. See the companion
`trust-reconciliation-{{today}}.md` for full ledger.

---

**Client Acknowledgment:**

____________________________________________    ________________
{{client_name}}                                 Date

**Attorney:**

____________________________________________    ________________
{{attorney_name}}                               Date
