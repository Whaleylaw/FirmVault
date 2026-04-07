# Technology-Assisted Review (TAR) Protocol

When a case has a large document production on either side, both parties can stipulate to a TAR protocol to control cost. Use this reference when the volume justifies it (tens of thousands of documents or more) or when opposing counsel proposes one.

## What TAR is

Technology-Assisted Review — also called predictive coding or computer-assisted review — trains a machine-learning classifier on human-coded seed documents, then scores the rest of the collection for relevance. A well-run TAR workflow cuts review cost 70–90% versus linear review and produces defensible results under Rio Tinto / Da Silva Moore.

## When to propose one

- Large document production expected from either side
- Meaningful e-discovery (email corpora, chat archives, document management systems)
- Cost of linear review would be disproportionate to the matter
- Opposing counsel has proposed TAR and we need to respond

## Protocol components to negotiate

1. **Scope.** Data sources, custodians, date range, file types, de-duplication rules.
2. **Culling.** Optional keyword culling before TAR; the keyword list itself.
3. **Training workflow.** Seed set selection (random vs. judgmental), human review rounds, stability criteria.
4. **Validation.** Statistical sampling, recall and precision targets, elusion testing of the discard pile.
5. **Transparency.** Whether seed sets are shared, methodology disclosure, access to validation stats.
6. **Privilege review.** Always done post-TAR on the responsive set.

## Sample workflow language

```
1. Collection. Collect from agreed custodians and apply date filters.
   De-duplicate at the family level.

2. Optional keyword culling. Apply the keyword list at Exhibit A to
   reduce the review population.

3. TAR training. Draw a random seed sample, human-review for
   relevance, train the classifier, iterate until stability metrics
   are met.

4. Validation. Draw a statistical sample from the discards; calculate
   elusion and recall. Document the results.

5. Production. Human privilege review of the responsive set, then
   produce with Bates numbering and agreed metadata fields.
```

## Target metrics

| Metric | Meaning | Typical target |
|---|---|---|
| Recall | Share of truly-relevant documents the model surfaced | 70–80%+ |
| Precision | Share of surfaced documents that are actually relevant | 50%+ |
| Elusion | Share of discarded documents that were relevant | <10% |

## Meet-and-confer checklist

- [ ] Agreement to use TAR in the first place
- [ ] Transparency level (share seeds? share methodology?)
- [ ] Seed set composition rules
- [ ] Number of training iterations / stability criteria
- [ ] Validation methodology and recall target
- [ ] Documentation each side will keep
- [ ] Cost allocation, if any

## Deliverables

- TAR protocol draft (joint stipulation, filed with the court if requested)
- Meet-and-confer talking points
- Short cost-benefit memo for the attorney
