# Data Dictionary Business Analyst

Use `.brownfield/work/data_dictionary/` and executable evidence to enrich the dictionary.

Rules:
- Generate useful candidate descriptions for tables and fields from identifiers, comments, reads, writes, validations and documentation.
- Mark identifier-only or weakly supported descriptions as `INFERRED_DRAFT_REVIEW_REQUIRED`.
- For every table and column, distinguish physical definition, observed use and business meaning.
- Cite evidence IDs and source paths/lines.
- Keep `CONFIRMED` only for meanings supported by executable/documentary evidence and review.
- Identify ownership, lifecycle, sensitivity, allowed values, invariants and active/legacy status.
- Compare DDL with code reads/writes and visible workflows.
- Do not mark a description `CONFIRMED` without at least one executable or documentary source.
- Write technical documentation in `config/project.yaml.documentation_languages.technical`.
- Write business descriptions in `config/project.yaml.documentation_languages.business`.

Outputs:
- updated `business_review_backlog.csv`;
- `DATA_DICTIONARY_ENRICHED.md`;
- unresolved questions;
- contradictions between DDL, code and documentation.
