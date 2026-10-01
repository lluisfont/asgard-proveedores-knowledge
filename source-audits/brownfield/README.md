# Installed Brownfield Refactor Kit

This directory isolates deterministic extraction, evidence, review backlogs, state, reports and checkpoint packages from the legacy source tree.

## First run

```bash
python .brownfield/bin/brownfield.py verify-config
python .brownfield/bin/brownfield.py seed-baseline
python .brownfield/bin/brownfield.py semantic-reconstruct
```

Then review:

- `.brownfield/work/data_dictionary/business_review_backlog.csv`;
- `.brownfield/work/process_maps/process_business_review.csv`;
- `.brownfield/work/data_dictionary/SEMANTIC_DATA_DICTIONARY.xlsx`;
- `.brownfield/work/semantic_flow_analysis/FLOW_USAGE_SEMANTIC_ANALYSIS.xlsx`;
- `.brownfield/work/business_glossary/BUSINESS_GLOSSARY.md`;
- `.brownfield/PROJECT_STATE.json`.
- `.brownfield/PIPELINE.md`.
- `.brownfield/ASGARD_ANALYSIS_FRAMEWORK.md` when the repository belongs to an ASGARD refactor program.

`analyse-all` is still available as a deprecated compatibility alias for `seed-baseline`.

Optional Graphify flow:

```bash
graphify .
python .brownfield/bin/brownfield.py graphify-import
```

Imported Graphify output is stored in `.brownfield/work/graphify/` and copied into architecture/traceability release artifacts. `graphify-out` is excluded from source inventory by default.

Semantic reconstruction flow:

```bash
python .brownfield/bin/brownfield.py semantic-data
python .brownfield/bin/brownfield.py semantic-flows
python .brownfield/bin/brownfield.py semantic-glossary
```

Use `semantic-reconstruct` to run those three steps together and refresh the completeness report.

## Trust boundary

Static output is not a validated business specification. DDL comments, route names and identifiers are documentary clues used to create `INFERRED_DRAFT_REVIEW_REQUIRED` candidates. Business meaning and process ordering remain unconfirmed until supported by evidence and independently verified.

Semantic outputs are useful hypotheses for review. They should explain fields, tables, flows, rules and glossary terms from crossed evidence, while keeping every unvalidated claim visibly provisional.

Documentation languages are configured in `config/project.yaml`:

- `documentation_languages.technical`
- `documentation_languages.business`

Checkpoint ZIPs are non-canonical working packages. Canonical promotion requires a valid verification report and human approval.
