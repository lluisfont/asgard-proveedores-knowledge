# Analysis Completeness Report

Static analysis completed the deterministic seed only. The project is not ready as an OpenSpec baseline until the pending phases are reconstructed and verified.

- Pipeline phases: 16
- Minimum expected artifacts: 284
- Generated deterministic artifacts: 33
- Required release artifacts materialized: 323
- Seeded release artifacts copied from deterministic output: 38
- Deterministic coverage: 11.62%
- Status: INCOMPLETE_BASELINE

## Coverage By Group

| Family | Area | Status | Generated / Minimum | Next phase |
| --- | --- | --- | ---: | --- |
| engineering-analysis | baseline | PARTIAL_DETERMINISTIC_SEED | 2/15 | 05-architecture-reconstruct |
| engineering-analysis | architecture | INFERRED_DRAFT_REVIEW_REQUIRED | 0/16 | 05-architecture-reconstruct |
| engineering-analysis | data | PARTIAL_DETERMINISTIC_SEED | 10/24 | 04-data-semantics-reconstruct |
| engineering-analysis | interfaces | PARTIAL_DETERMINISTIC_SEED | 6/18 | 05-architecture-reconstruct |
| engineering-analysis | security | PARTIAL_DETERMINISTIC_SEED | 1/18 | 06-security-analyze |
| engineering-analysis | behavior | PARTIAL_DETERMINISTIC_SEED | 1/16 | 07-transaction-analyze |
| engineering-analysis | integrations | PARTIAL_DETERMINISTIC_SEED | 1/14 | 05-architecture-reconstruct |
| engineering-analysis | quality | INFERRED_DRAFT_REVIEW_REQUIRED | 0/15 | 13-characterization-tests-plan |
| engineering-analysis | tests | INFERRED_DRAFT_REVIEW_REQUIRED | 0/14 | 13-characterization-tests-plan |
| traceability | verification | PARTIAL_DETERMINISTIC_SEED | 1/15 | 14-verify-baseline |
| openspec | baseline | INFERRED_DRAFT_REVIEW_REQUIRED | 0/12 | 15-openspec-baseline |
| business-analysis | product-context | PARTIAL_DETERMINISTIC_SEED | 2/12 | 12-business-glossary-reconstruct |
| business-analysis | actors | INFERRED_DRAFT_REVIEW_REQUIRED | 0/8 | 09-business-reconstruct |
| business-analysis | processes | PARTIAL_DETERMINISTIC_SEED | 1/8 | 11-flow-usage-semantics-reconstruct |
| business-analysis | semantic-flow-analysis | GENERATED | 5/5 | 12-business-glossary-reconstruct |
| business-analysis | rules | INFERRED_DRAFT_REVIEW_REQUIRED | 0/12 | 10-business-rules-reconstruct |
| business-analysis | domain-model | PARTIAL_DETERMINISTIC_SEED | 3/9 | 04-data-semantics-reconstruct |
| business-analysis | use-cases | INFERRED_DRAFT_REVIEW_REQUIRED | 0/5 | 09-business-reconstruct |
| business-analysis | ui | INFERRED_DRAFT_REVIEW_REQUIRED | 0/9 | 09-business-reconstruct |
| business-analysis | reporting | INFERRED_DRAFT_REVIEW_REQUIRED | 0/8 | 10-business-rules-reconstruct |
| business-analysis | documents | INFERRED_DRAFT_REVIEW_REQUIRED | 0/8 | 09-business-reconstruct |
| business-analysis | exceptions | INFERRED_DRAFT_REVIEW_REQUIRED | 0/7 | 09-business-reconstruct |
| business-analysis | variants | INFERRED_DRAFT_REVIEW_REQUIRED | 0/7 | 10-business-rules-reconstruct |
| business-analysis | governance | INFERRED_DRAFT_REVIEW_REQUIRED | 0/9 | 14-verify-baseline |

## Required Pipeline

- 01-inventory
- 02-technical-evidence
- 03-data-archaeology
- 04-data-semantics-reconstruct
- 05-architecture-reconstruct
- 06-security-analyze
- 07-transaction-analyze
- 08-domain-discover
- 09-business-reconstruct
- 10-business-rules-reconstruct
- 11-flow-usage-semantics-reconstruct
- 12-business-glossary-reconstruct
- 13-characterization-tests-plan
- 14-verify-baseline
- 15-openspec-baseline
- 16-consolidate-release
