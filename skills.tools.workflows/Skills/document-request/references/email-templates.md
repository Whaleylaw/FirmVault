# Document Request Email Templates

Skeletons for the initial intake request and for follow-up reminders. Treat these as starting points — hand-tune tone and the attachment list for the actual case.

## Initial request

```
Subject: Documents Needed — Your Personal Injury Case

Dear {client_first_name},

Thank you for choosing the firm to represent you. To move forward with your
case, please complete and return the forms attached to this email.

Required (please return as soon as possible):
  - New Client Information Sheet
  - Fee Agreement ({mva|sandf|wc})
  - Medical Authorization (HIPAA)

Additional:
  - Medical Treatment Questionnaire
  - Authorization of Digital Signature Replication
  - {mva|sandf} Accident Detail Information Sheet
  - Wage & Salary Verification (if claiming lost wages)
  - CMS Medicare Verification (if Medicare-eligible)

You can complete the fillable PDFs electronically and reply with the
attachments, or print, sign, and return by mail or fax.

  Email: reply to this message
  Fax: (XXX) XXX-XXXX
  Mail: [Office address]

Please let us know if you have any questions.

{sender_name}
```

## Follow-up reminder

```
Subject: Reminder — Documents Still Needed for {client_name}

Dear {client_first_name},

We are still waiting on the following forms to move your case forward:

  - {list the specific missing documents}

Your case cannot progress until we receive these. I've re-attached the forms
for convenience. Please let me know if anything is unclear or if you'd like
to switch to electronic signature via DocuSign instead.

{sender_name}
```

## Selecting attachments

Read template paths from `Templates/` — never copy them into the case folder. The attachment list is just a manifest for the email; the actual files stay in place in the firm template library per `DATA_CONTRACT.md` §6.

For a typical MVA packet:

```
Templates/new-client-information-sheet.pdf
Templates/mva-fee-agreement.pdf
Templates/medical-authorization-hipaa.pdf
Templates/medical-treatment-questionnaire.pdf
Templates/authorization-of-digitally-signature-replication.pdf
Templates/mva-accident-detail-information-sheet.pdf
```

Swap the fee agreement and accident detail sheet for the S&F or WC variants per the table in `SKILL.md`.
