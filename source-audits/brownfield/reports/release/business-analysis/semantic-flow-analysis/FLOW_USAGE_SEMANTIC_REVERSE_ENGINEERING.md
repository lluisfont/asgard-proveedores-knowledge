# Flow Usage Semantic Reverse Engineering

Status: INFERRED_DRAFT_REVIEW_REQUIRED

This pass cross-checks process candidates with observed data reads/writes and semantic field candidates. It is intended to separate operational business flows from simple reporting or isolated technical endpoints.

- Domains: 3
- Flow/table crossings: 595
- Flow/field crossings: 10463

| Domain | Processes | Tables | Fields | Reads | Writes |
| --- | ---: | ---: | ---: | ---: | ---: |
| general-business-data | 42 | 370 | 4348 | 571 | 199 |
| identity-access | 1 | 2 | 25 | 2 | 2 |
| operations-workflow | 5 | 0 | 0 | 0 | 0 |
