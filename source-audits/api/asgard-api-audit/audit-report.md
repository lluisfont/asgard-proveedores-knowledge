---
audit_id: "audit-ccb4411d42a22cd0"
auditor_version: "0.8.0"
repository: "asgard-api-audit-target-20260915"
source_ref: "HEAD"
source_commit: "f4f6d607c39d5b911b2f6e1dbf98c9658d5b3f4a"
---

# API Audit Report

## Verdict

**PARTIAL** — at least one applicable completion gate remains unresolved; unknown behavior is not inferred.

## Proven surface

- Exposed HTTP endpoints: **0**
- Consumed HTTP endpoints: **2**
- Integration findings: **0**
- Discovery complete: **false**
- Contract enrichment scope: **not_applicable**
- Correlation scope: **out_of_scope**
- Semantic complete: **0/0**
- Semantic unresolved findings: **0**

## Contract enrichment coverage

- Total exposed endpoints: **0**
- Path parameters enriched: **0/0**
- Request enrichment: **0/0**
- Response enrichment: **0/0**
- Security enrichment: **0/0**
- Unresolved contract enrichment: **0**

## Semantic enrichment coverage

- Analysis attempted: **0/0**
- Complete: **0**
- Partial: **0**
- Unresolved endpoints: **0**
- Operations with non-generic descriptions: **0**
- Operations with data access facts: **0**
- Operations with auth-context facts: **0**
- Operations with conditional/outcome facts: **0**
- Operations with outbound integration facts: **0**

## Blocking work before full audit completion

- Resolve discovery-level blocking findings listed below.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `http_client_detected_no_calls`: HTTP client 'guzzle' was detected by inventory but no supported direct calls were proven. Wrapper or dynamic usage may exist.

## OpenAPI semantics

The generated OpenAPI describes only proven exposed HTTP paths/methods. Equivalent templates that differ only by source parameter names are canonicalized without discarding their original source paths.
