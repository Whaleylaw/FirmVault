# Trust Account Reconciliation

**Client:** {{client_name}}
**Case:** [[cases/{{case_slug}}/{{case_slug}}|{{client_name}} — {{case_type}} {{date_of_incident}}]]
**Account:** Firm IOLTA — Client Trust
**Period:** {{settlement_date}} through {{today}}

---

## Ledger

| Date | Description | Debit | Credit | Balance |
|---|---|---:|---:|---:|
| {{settlement_date}} | Settlement received, {{carrier_name}} | | ${{gross}} | ${{gross}} |
| {{settlement_date}} | Attorney fee → operating | ${{fee}} | | |
| {{settlement_date}} | Case cost reimbursement → operating | ${{costs_total}} | | |
| {{settlement_date}} | Initial distribution to client | ${{initial_net}} | | ${{original_holdback}} |
| {{paid_date_1}} | {{lien_holder_1}} payoff | ${{paid_1}} | | |
| {{paid_date_2}} | {{lien_holder_2}} payoff | ${{paid_2}} | | |
| {{today}} | Supplemental distribution to client | ${{total_surplus}} | | **$0.00** |

## Summary

- Opening balance (settlement deposit): **${{gross}}**
- Total disbursed: **${{gross}}**
- **Closing balance: $0.00**
- Account status for this client: **CLOSED**

---

Reconciled by: ____________________________________    Date: ________
