---
audit_id: "audit-a2f71c47153e0503"
auditor_version: "0.8.0"
repository: "graphify-v0.9.61"
source_ref: "HEAD"
source_commit: "fe66389083369c3159aa391117185c8f58b4d07c"
---

# API Knowledge

Knowledge schema: `1.0`

This document is generated from source evidence. Unknown request/response/authentication details are not inferred.

## Summary

- HTTP exposed: **0**
- HTTP consumed: **0**
- Integration findings: **0**
- Discovery complete: **false**
- Contract enrichment unresolved: **0**
- Semantic complete: **0/0**
- Semantic unresolved: **0**

## Exposed HTTP

No exposed HTTP endpoints were proven.
## Consumed HTTP

No consumed HTTP endpoints were proven.
## Integration surfaces

No non-HTTP integration operations were proven.
## Unresolved

- **unsupported_server_framework** — Server framework 'aspnet-core' has no v0.4 exposed-endpoint detector.
- **unsupported_server_framework** — Server framework 'django' has no v0.4 exposed-endpoint detector.
- **unsupported_server_framework** — Server framework 'nestjs' has no v0.4 exposed-endpoint detector.
- **http_client_detected_no_calls** — HTTP client 'angular-httpclient' was detected by inventory but no supported direct calls were proven. Wrapper or dynamic usage may exist.
- **unsupported_http_client** — HTTP client 'dotnet-httpclient' is detected but has no v0.4 endpoint detector.
- **fetch_dynamic_or_complex_call_unresolved** — fetch() call could not be resolved as a supported literal URL/options form.
- **http_client_detected_no_calls** — HTTP client 'fetch' was detected by inventory but no supported direct calls were proven. Wrapper or dynamic usage may exist.
- **non_http_integration_requires_dedicated_detector** — Non-HTTP/OpenAPI integration surfaces detected (sse); v0.4 endpoint discovery does not audit those contracts yet.

## Contract Enrichment Coverage

- Total exposed endpoints: **0**
- Request enrichment: **0/0**
- Response enrichment: **0/0**
- Security enrichment: **0/0**

## Semantic Enrichment Coverage

- Analysis attempted: **0/0**
- Complete: **0**
- Partial: **0**
- Unresolved endpoints: **0**
- Operations with data access facts: **0**
- Operations with auth-context facts: **0**
- Operations with conditional/outcome facts: **0**
- Operations with outbound integration facts: **0**
- Semantic unresolved findings: **0**
