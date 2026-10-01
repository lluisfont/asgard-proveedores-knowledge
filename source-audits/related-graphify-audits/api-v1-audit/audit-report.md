---
audit_id: "audit-948c4f9ecafa27fb"
auditor_version: "0.8.0"
repository: "graphify-v0.9.61"
source_ref: "HEAD"
source_commit: "fe66389083369c3159aa391117185c8f58b4d07c"
---

# API Audit Report

## Verdict

**PARTIAL** — at least one applicable completion gate remains unresolved; unknown behavior is not inferred.

## Proven surface

- Exposed HTTP endpoints: **0**
- Consumed HTTP endpoints: **0**
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
  - `unsupported_server_framework`: Server framework 'aspnet-core' has no v0.4 exposed-endpoint detector.
  - `unsupported_server_framework`: Server framework 'django' has no v0.4 exposed-endpoint detector.
  - `unsupported_server_framework`: Server framework 'nestjs' has no v0.4 exposed-endpoint detector.
  - `http_client_detected_no_calls`: HTTP client 'angular-httpclient' was detected by inventory but no supported direct calls were proven. Wrapper or dynamic usage may exist.
  - `unsupported_http_client`: HTTP client 'dotnet-httpclient' is detected but has no v0.4 endpoint detector.
  - `fetch_dynamic_or_complex_call_unresolved`: fetch() call could not be resolved as a supported literal URL/options form.
  - `http_client_detected_no_calls`: HTTP client 'fetch' was detected by inventory but no supported direct calls were proven. Wrapper or dynamic usage may exist.
  - `non_http_integration_requires_dedicated_detector`: Non-HTTP/OpenAPI integration surfaces detected (sse); v0.4 endpoint discovery does not audit those contracts yet.

## OpenAPI semantics

The generated OpenAPI describes only proven exposed HTTP paths/methods. Equivalent templates that differ only by source parameter names are canonicalized without discarding their original source paths.
