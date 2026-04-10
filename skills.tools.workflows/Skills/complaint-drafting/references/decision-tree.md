# Complaint Template Decision Tree

Use this to pick the right firm template from `Templates/`. The four available complaint templates are:

- `mva-complaint-basic.docx`
- `mva-complaint-standard.docx`
- `mva-complaint-um.docx`
- `premise-liability-complaint-template.docx`

## Flowchart

```
What's the case type?

├── Motor Vehicle Accident
│   │
│   ├── Is there a UM/UIM claim against client's own carrier?
│   │   ├── Yes → mva-complaint-um.docx
│   │   └── No → continue
│   │
│   ├── Any non-routine wrinkle?
│   │   (vicarious liability, negligent entrustment, punitive damages,
│   │    bad-faith count, government defendant, stolen vehicle, etc.)
│   │   ├── Yes → start from mva-complaint-standard.docx and add
│   │   │         extra counts from references/cause-action-templates.md.
│   │   │         Flag as non-standard in the activity log.
│   │   └── No → continue
│   │
│   └── Are liability facts simple and damages modest?
│       ├── Yes → mva-complaint-basic.docx
│       └── No  → mva-complaint-standard.docx
│
├── Premises Liability (slip/fall, dog bite, unsafe condition)
│   └── premise-liability-complaint-template.docx
│       (add premises-specific counts by hand if it's a dog bite
│        or has a government defendant)
│
└── Anything else (med mal, wrongful death standalone, product liability)
    → STOP. These don't have a firm template. Escalate to the attorney;
      this skill doesn't cover them.
```

## When to add counts by hand

The firm templates cover garden-variety negligence. If any of the following apply, add the matching count from [`cause-action-templates.md`](cause-action-templates.md):

| Fact pattern | Add this count |
|---|---|
| Defendant was on the job, employer should pay | Vicarious Liability / Respondeat Superior |
| Owner let an unfit driver use the vehicle | Negligent Entrustment |
| Conduct was reckless, want punitive damages | Gross Negligence |
| Carrier denied coverage in bad faith | Bad Faith (consult attorney — KRS 304.12-230) |
| Loss of consortium by spouse or parent | Loss of Consortium (separate plaintiff) |

## Notes

- Never edit the source template in `Templates/`. Copy to `cases/<slug>/documents/complaint-draft.docx` first.
- If no template fits at all, stop and flag it. Do not improvise a complaint from scratch without attorney direction.
- Premises cases against a government entity (city, county, housing authority) need notice-of-claim review before filing; surface this to the attorney.
