# Brownfield Pipeline

Use these phase names when running or reviewing the analysis.

## Commands Available Now

1. `verify-config`
   Validate configuration, source/database scope, scoring policy, model policy and documentation languages.

2. `seed-baseline`
   Run the deterministic seed baseline. This creates inventory, evidence, physical data dictionary, process-map candidates, completeness report and `work/release/`.

3. `analyse-all`
   Deprecated alias for `seed-baseline`. Prefer `seed-baseline` in new runs.

4. `completeness-report`
   Rebuild deliverable coverage and the required release artifact tree.

5. `semantic-data`
   Generate semantic table/field catalogs and `SEMANTIC_DATA_DICTIONARY.*` from schema, constraints and observed usage.

6. `semantic-flows`
   Cross-check process candidates with table and field usage to produce flow/data matrices.

7. `semantic-glossary`
   Generate the business glossary from semantic data and flow evidence.

8. `semantic-reconstruct`
   Run semantic data, semantic flows, semantic glossary and refresh completeness.

9. `graphify-import`
   Import existing `graphify-out/` output as optional architecture evidence. Run Graphify separately first.

10. `package`
   Package a non-canonical checkpoint.

## Steps After `seed-baseline`

For ASGARD refactor programs, use `.brownfield/ASGARD_ANALYSIS_FRAMEWORK.md` as the common progress and closure checklist. `ASGARD-01` through `ASGARD-15` are the AS-IS closure scope; `ASGARD-16` and `ASGARD-17` are post-closure TO-BE and roadmap phases.

1. Review `.brownfield/work/completeness/ANALYSIS_COMPLETENESS_REPORT.md`.
2. Review `.brownfield/work/data_dictionary/business_review_backlog.csv`.
3. Review `.brownfield/work/process_maps/process_business_review.csv`.
4. Optionally run Graphify with `graphify .`.
5. Import Graphify output with `python .brownfield/bin/brownfield.py graphify-import`.
6. Run `python .brownfield/bin/brownfield.py semantic-reconstruct`.
7. Reconstruct business domains from evidence and mark unconfirmed claims as `INFERRED_DRAFT_REVIEW_REQUIRED`.
8. Generate OpenSpec AS-IS specs only after domain evidence is coherent.
9. Run independent verification before treating the baseline as formal.

## Future Phase Names

- `data-semantics-reconstruct`
- `architecture-reconstruct`
- `security-analyze`
- `transaction-analyze`
- `domain-discover`
- `business-reconstruct`
- `business-rules-reconstruct`
- `flow-usage-semantics-reconstruct`
- `business-glossary-reconstruct`
- `characterization-tests-plan`
- `verify-baseline`
- `openspec-baseline`
- `consolidate-release`

These names describe responsibilities that are not completed by `seed-baseline`.
