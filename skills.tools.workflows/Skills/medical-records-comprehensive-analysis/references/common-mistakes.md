# Common Mistakes — Medical Records Comprehensive Analysis

The failures that recur when orchestrating this pipeline.

**Skipping fact investigation.** Jumping to medical organization without `case_facts.md` means causation analysis has no incident date or mechanism of injury to lean on. Always start with Phase 1.

**Starting Phase 3 before chronology synthesis finishes.** All four Phase 3 sub-agents read `chronology.md`. Wait for both extraction completion and chronology synthesis.

**No batching on extraction.** Spawning one sub-agent for fifty documents overruns the context budget. Spawn 3–4 extractors in parallel, each handling 1–2 files, then the next batch.

**Serializing what should be parallel.** Phase 2a organizer runs alongside Phase 2b extraction, not after it. Phase 3's four sub-agents run simultaneously, not sequentially.

**Starting Phase 4 before all four Phase 3 reports exist.** The summary writer needs all seven prior reports (`case_facts`, `inventory`, `chronology`, `inconsistencies`, `red_flags`, `causation`, `missing_records`).

**Forgetting to create `analysis/extractions/`.** Sub-agents fail silently when their output path doesn't exist. Create both directories in Phase 0.

**Reading every medical file in the organizer.** The organizer builds an inventory, not a deep read. It should read bills first, then a few key records for context, then stop.
