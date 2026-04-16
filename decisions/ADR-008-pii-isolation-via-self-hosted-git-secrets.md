# ADR-008: PII Isolation via Self-Hosted Git Secrets

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Proposed       |
| **Date**          | 2026-04-16     |
| **Author**        | Aaron / Roscoe |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

FirmVault's core principle is "the firm as a code repo" — law firm work modeled
as git primitives (commits, PRs, branches, diffs). CLAUDE.md already states:

> **PHI never lives in the vault.** Placeholders like `{{client_ssn}}` and
> `{{dob}}` reference secrets held in the user's own infrastructure. At render
> time, deterministic code (not the model) substitutes real values. The model
> never sees raw PII.

This principle exists but has no implementation spec. Today FirmVault is a single
GitHub repo. The real deployment vision is multi-office, multi-machine, with
actual client data flowing through the system. The question is: **where does PII
live, and how do agents access it without seeing it?**

Personal injury cases contain significant PII:

- Client: full name, DOB, SSN, address, phone, email, employer
- Medical: provider names, account numbers, treatment dates, diagnosis codes
- Insurance: policy numbers, claim numbers, adjuster contacts
- Financial: settlement amounts, lien amounts, fee calculations
- Opposing parties: names, contact info, policy details

This data must be:
1. **Accessible to agents** for document generation (demands, letters, filings)
2. **Invisible to agents** during reasoning (case strategy, phase transitions)
3. **Auditable** — who accessed what, when
4. **Recoverable** — if a value changes, the old value isn't lost
5. **Secure in transit** — multi-office sync can't expose PII
6. **Compliant** — bar association and HIPAA requirements for data handling

The existing placeholder pattern (`{{client_ssn}}`) solves #2 but doesn't
address where the actual values live or how they get injected.

**Relevant FirmVault principles** (from CLAUDE.md):
- "The vault is a shadow, not the source of truth"
- "Git is the deliberate interface"
- "Markdown, not a graph DB"
- "The vault is the only state store for this layer"

---

## Decision

Use **self-hosted Git platform secrets** (Forgejo, Gitea, or GitLab CE) as the
PII vault for each case repository. Every case is a repository. Every piece of
PII is a repository-level secret or variable on the hosting platform.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Self-Hosted Git Platform (Forgejo / Gitea / GitLab CE)     │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Case: smith-v-   │  │ Case: jones-v-  │  ... per case    │
│  │ state-farm-2026  │  │ geico-2026      │                  │
│  │                  │  │                  │                  │
│  │  Git Repo:       │  │  Git Repo:       │                  │
│  │  ├── case.md     │  │  ├── case.md     │                  │
│  │  ├── timeline/   │  │  ├── timeline/   │                  │
│  │  ├── issues/     │  │  ├── issues/     │                  │
│  │  ├── templates/  │  │  ├── templates/  │                  │
│  │  └── ...         │  │  └── ...         │                  │
│  │                  │  │                  │                  │
│  │  Secrets:        │  │  Secrets:        │                  │
│  │  PII_CLIENT_NAME │  │  PII_CLIENT_NAME │                  │
│  │  PII_CLIENT_DOB  │  │  PII_CLIENT_DOB  │                  │
│  │  PII_CLIENT_SSN  │  │  PII_CLIENT_SSN  │                  │
│  │  PII_INSURER_... │  │  PII_INSURER_... │                  │
│  │  ...             │  │  ...             │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  Organization-level secrets (shared across cases):          │
│  ORG_FIRM_NAME, ORG_FIRM_ADDRESS, ORG_BAR_NUMBER, ...      │
│                                                             │
│  Environment scoping:                                       │
│  "intake" → PII_CLIENT_NAME, PII_CLIENT_PHONE only         │
│  "demand" → all PII fields                                  │
│  "readonly" → no PII injection (agent reasoning only)       │
└─────────────────────────────────────────────────────────────┘
```

### One Case = One Repository

Each case gets its own repository on the self-hosted platform. This maps
naturally to the existing FirmVault structure (`cases/<slug>/` becomes its own
repo). Benefits:

- **Access control per case** — repo-level permissions
- **Independent secret stores** — each case's PII is isolated
- **Git history per case** — cleaner diffs, no cross-case noise
- **Archive/delete per case** — close a case, archive the repo
- **Size stays manageable** — no mono-repo scaling issues

The platform acts as a "case server" — each office has a Forgejo instance
(or shares one) and cases sync via git remote operations. Shared templates,
skills, and workflows live in a separate "firm-infrastructure" repo that all
case repos reference.

### PII Naming Convention

All PII is stored as repository secrets with a structured naming scheme:

```
PII_CLIENT_FIRST_NAME
PII_CLIENT_LAST_NAME
PII_CLIENT_FULL_NAME
PII_CLIENT_DOB
PII_CLIENT_SSN
PII_CLIENT_ADDRESS_STREET
PII_CLIENT_ADDRESS_CITY
PII_CLIENT_ADDRESS_STATE
PII_CLIENT_ADDRESS_ZIP
PII_CLIENT_PHONE
PII_CLIENT_EMAIL
PII_CLIENT_EMPLOYER

PII_INSURER_NAME
PII_INSURER_POLICY_NUMBER
PII_INSURER_CLAIM_NUMBER
PII_ADJUSTER_NAME
PII_ADJUSTER_PHONE
PII_ADJUSTER_EMAIL

PII_PROVIDER_1_NAME             # indexed for multiple providers
PII_PROVIDER_1_ACCOUNT_NUMBER
PII_PROVIDER_1_PHONE
PII_PROVIDER_2_NAME
PII_PROVIDER_2_ACCOUNT_NUMBER
...

PII_OPPOSING_PARTY_NAME
PII_OPPOSING_COUNSEL_NAME
PII_OPPOSING_COUNSEL_FIRM
PII_OPPOSING_COUNSEL_PHONE
```

"Variables" (non-secret, visible in logs) for non-sensitive case metadata:

```
CASE_TYPE                       # auto, premises, dog-bite, etc
CASE_JURISDICTION               # county/state
CASE_ACCIDENT_DATE
CASE_FILE_OPEN_DATE
CASE_STATUS                     # mirrors phase_dag status
```

### Injection Model

PII is injected ONLY during **materialization** — the step where a template
becomes a real document:

```
1. Agent works on case reasoning using placeholders:
   "Client {{PII_CLIENT_FULL_NAME}} was injured on {{CASE_ACCIDENT_DATE}}..."

2. Agent decides a demand letter should be generated.
   Creates a PR: "Generate demand letter from template demand-standard"

3. CI/CD workflow triggers on PR merge (or on specific label):
   - Workflow runs in Forgejo Actions / Gitea Actions / GitLab CI
   - Secrets are injected as environment variables
   - Deterministic template engine (envsubst, jinja2, or similar)
     substitutes {{PII_*}} placeholders with real values
   - Output PDF/docx is saved to an encrypted artifact store
     (NOT committed to the repo)

4. The materialized document with real PII lives OUTSIDE git:
   - Encrypted artifact attached to the workflow run
   - Or pushed to the firm's file storage (Drive, Dropbox, local NAS)
   - A reference (path/URL, not content) is committed to the repo
```

This means:
- **Git history never contains PII** — only placeholders
- **Agents never see PII in their context** — only placeholders
- **Real documents are produced by deterministic code** — not the model
- **The CI/CD runner is the only process that touches both** secrets and templates

### Environment Scoping for Agent Access Control

Different agent roles get different secret scopes:

| Environment    | Secrets Available           | Use Case                     |
|---------------|-----------------------------|------------------------------|
| `readonly`    | None                        | Case reasoning, strategy     |
| `intake`      | PII_CLIENT_NAME, PHONE, EMAIL | Initial contact, scheduling |
| `treatment`   | + PII_PROVIDER_*            | Medical coordination         |
| `demand`      | All PII_*                   | Document generation          |
| `litigation`  | All PII_* + court info      | Filing, discovery            |
| `admin`       | All secrets + ORG_*         | Firm administration          |

An agent running in the `treatment` environment literally cannot access
`PII_CLIENT_SSN` — the platform doesn't inject it. This is infrastructure-level
access control, not prompt-level trust.

### Multi-Office Sync

```
Office A (Forgejo instance)          Office B (Forgejo instance)
┌──────────────────────┐             ┌──────────────────────┐
│ Case repo: smith-v-  │  git push   │ Case repo: smith-v-  │
│ state-farm-2026      │ ──────────> │ state-farm-2026      │
│                      │  git pull   │                      │
│ Secrets: (local)     │ <────────── │ Secrets: (local)     │
│ PII_CLIENT_NAME=...  │             │ PII_CLIENT_NAME=...  │
└──────────────────────┘             └──────────────────────┘
         │                                     │
         │  Secrets sync via separate           │
         │  encrypted channel (NOT git)         │
         └─────────────────────────────────────┘
```

Git push/pull syncs the case work (documents, timeline, issues, agent logs).
PII secrets are synced separately via:
- Platform API (Forgejo/Gitea REST API for secrets management)
- Encrypted backup/restore
- Manual entry (small firms)

This separation means if git traffic is intercepted, no PII is exposed.

### Platform Recommendation: Forgejo

Forgejo is the recommended platform because:

1. **Forgejo Actions** — GitHub Actions-compatible CI/CD with secret injection
2. **Lightweight** — runs on a single machine, minimal resources
3. **Repository secrets and variables** — same UX as GitHub
4. **Active development** — community-driven fork of Gitea with strong governance
5. **Federation roadmap** — ActivityPub support maps to multi-office federation
6. **Self-hosted** — all data stays on firm infrastructure
7. **SQLite mode** — zero external dependencies for small deployments
8. **Familiar to agents** — API is GitHub-compatible, so existing tooling works

GitLab CE is a viable alternative for larger firms wanting more mature CI/CD
variable scoping and built-in secret management features.

---

## Alternatives Considered

### A1: Encrypt PII in the git repo itself (git-crypt, SOPS)

PII lives in the repo as encrypted files, decrypted at checkout by authorized
users/agents.

Rejected because:
- Key management is complex, especially multi-office
- Decrypted PII appears in working directory and agent context
- Git diffs on encrypted blobs are useless
- Doesn't solve the "agent shouldn't see PII during reasoning" requirement
- One leaked key exposes all PII in history

### A2: External secret manager (HashiCorp Vault, Doppler)

PII stored in a dedicated secret management service, referenced by the git
platform at runtime.

Deferred. This is the enterprise-grade version of the same architecture. A
Forgejo instance with built-in secrets is simpler to operate for a small firm.
If the system scales to 50+ simultaneous offices, migrating the secret store
to HashiCorp Vault or similar while keeping the same injection interface is
straightforward — just change the CI/CD secret source.

### A3: Database with row-level encryption (Postgres + pgcrypto)

Traditional approach: PII in a database, application logic handles encryption
and access control.

Rejected because:
- Violates "markdown, not a graph DB" principle
- Adds a database dependency that must be separately backed up, secured, HA'd
- Doesn't integrate with git-native workflows
- Agents would need database access, adding attack surface
- No natural mapping to PR-based approval gates

### A4: Keep using GitHub with placeholder convention only

Continue with the current FirmVault approach: placeholders in markdown, PII
managed "somewhere else" without specifying where.

Rejected because:
- "Somewhere else" is doing a lot of work in that sentence
- No actual implementation of PII storage, injection, or access control
- Can't deploy to real firms without answering where PII actually lives
- Multi-office coordination is impossible without a concrete mechanism

---

## Consequences

### Positive

- **PII isolation is infrastructure, not convention** — enforced by the platform,
  not by hoping agents follow rules
- **Git audit trail has zero PII exposure** — safe to back up, replicate, analyze
- **Multi-office sync is just git** — familiar tooling, well-understood security model
- **Agent access control via environment scoping** — intake agent literally can't
  access SSNs, not just told not to
- **Materialization is deterministic** — document generation is template + secrets,
  no model hallucination of PII
- **Case isolation** — one repo per case means a breach of one case doesn't expose
  all cases
- **Familiar to lawyers** — "the case file is a folder, the secrets are in a vault"
  maps to how they already think
- **Scales from solo to multi-office** — same architecture, just add Forgejo instances
  or use federation

### Negative

- **Repo proliferation** — a firm with 500 active cases has 500 repos
- **Secret management overhead** — someone (or something) must enter PII into the
  platform's secret store during intake
- **Secrets aren't versioned** — if a client's address changes, the old address
  is gone from the platform (though it may exist in a materialized document)
- **Backup complexity** — need to back up both the git repos AND the secret store
- **Platform dependency** — switching from Forgejo to another platform means
  migrating the secret store, not just the git repos

### Mitigations

- **Repo proliferation**: Forgejo handles thousands of repos well. Org-level
  grouping and archival policies keep it manageable. Closed cases get archived.
- **Secret entry overhead**: Build an intake workflow that collects PII via a
  secure form and programmatically stores it via the Forgejo API. The intake
  agent collects placeholders; a separate secure process stores the real values.
- **Secret versioning**: Maintain a `pii-changelog.md` (itself using placeholders
  referencing dated secret versions: `PII_CLIENT_ADDRESS_V1`, `PII_CLIENT_ADDRESS_V2`)
  or use the platform's audit log if available.
- **Backup**: Script that exports secrets via API into an encrypted file alongside
  the git bundle. One backup artifact per case, encrypted at rest.

---

## Failure Criteria

1. **Platform secret limits hit**: If Forgejo/Gitea imposes a per-repo secret
   count limit below ~60 (a complex case with multiple providers/parties), the
   naming convention breaks down. → Mitigation: switch to a single encrypted
   JSON secret containing all PII, parsed at runtime.

2. **Materialization latency unacceptable**: If CI/CD-based document generation
   is too slow for real-time agent workflows (e.g., agent needs to reference
   client name in a phone call script RIGHT NOW). → Mitigation: add a "hot
   path" secure API that agents can call for single-value lookups with audit
   logging, bypassing CI/CD.

3. **Multi-office secret sync fails**: If keeping PII secrets synchronized across
   Forgejo instances proves unreliable or insecure. → Mitigation: centralize
   to a single Forgejo instance with VPN access, or adopt HashiCorp Vault (A2).

4. **Lawyers won't adopt it**: If the workflow of "work with placeholders, get
   real documents from CI/CD" is too alien for attorneys. → Mitigation: build a
   thin UI layer that abstracts the git/CI plumbing into familiar "case file"
   and "generate document" buttons.

5. **Agents can't reason effectively with only placeholders**: If placeholder-only
   context degrades agent performance on tasks that genuinely need PII awareness
   (e.g., searching for similar cases by injury type + location). → Mitigation:
   create anonymized/hashed derivative fields that allow pattern matching without
   exposing raw PII.

---

## Definition of Done

- [ ] Wiki evidence reviewed (this ADR extends existing principles, no wiki
      articles directly cited — grounded in CLAUDE.md architectural principles)
- [ ] Forgejo (or chosen platform) proof-of-concept deployed with one test case
- [ ] PII naming convention documented in DATA_CONTRACT.md
- [ ] Intake workflow stores PII via platform API
- [ ] Materialization workflow produces a real document from template + secrets
- [ ] Environment scoping tested (intake agent cannot access demand-phase secrets)
- [ ] Multi-office sync tested (two instances, one case, git + secret sync)
- [ ] Aaron approved
- [ ] Committed to FirmVault
