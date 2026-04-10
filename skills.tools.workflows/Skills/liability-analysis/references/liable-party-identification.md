# Liable Party Identification

Framework for identifying every potentially liable party on a new matter so the insurance and claim setup captures them all. Use alongside the main `liability-analysis` skill when a case has more than one obvious defendant.

## When this applies

- New case setup where liability is complex (multi-vehicle, commercial defendant, premises, product)
- Government entity involvement (notice-of-claim deadlines apply)
- Any scenario where vicarious or joint liability may bring in an employer, owner, contractor, or manufacturer

## Analytical steps

1. **Review incident facts.** Incident type (MVA, premises, product, med-mal), location, parties present, property ownership, employment relationships. Read `cases/<slug>/<slug>.md` and any police report or intake notes.
2. **Direct tortfeasors.** Every party whose act or omission directly caused injury: drivers, property owners, manufacturers, providers, employers.
3. **Vicarious liability.** Employer (respondeat superior), vehicle owner, franchisor, joint venture, agency. Each creates a separate potential defendant with its own insurance.
4. **Additional parties.** Government entities (notice requirements), contractors vs employees, parent/subsidiary companies, direct-action states.
5. **Insurance for each.** For every potential defendant, request carrier, verify coverage active, capture limits, note any excess or umbrella.
6. **Document.** For each defendant, create a `cases/<slug>/contacts/<slug>.md` stub with `role: defendant` and note the basis for liability, known insurance, SOL, and any notice requirement in the body.

## Scenario quick reference

| Incident type | Typical defendant set |
|---|---|
| MVA | Driver, titled owner, employer, lessor |
| Premises | Owner, tenant, property manager, maintenance contractor |
| Product | Manufacturer, distributor, retailer |
| Med-mal | Provider, practice group, hospital, employer |

## Output

- New defendant contact stubs under `cases/<slug>/contacts/`
- Updated `## Insurance Claims` section in `cases/<slug>/<slug>.md` with one bullet per known carrier/defendant pair
- SOL and notice-of-claim deadlines tracked in a body note on each defendant contact stub, so the materializer can surface them
