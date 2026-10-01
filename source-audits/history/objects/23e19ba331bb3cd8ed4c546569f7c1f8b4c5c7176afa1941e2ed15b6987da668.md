---
audit_id: "audit-6e48abdfb91166ed"
auditor_version: "0.8.0"
repository: "asgard-api-audit-target-20260915"
source_ref: "HEAD"
source_commit: "f4f6d607c39d5b911b2f6e1dbf98c9658d5b3f4a"
---

# API Knowledge

Knowledge schema: `1.0`

This document is generated from source evidence. Unknown request/response/authentication details are not inferred.

## Summary

- HTTP exposed: **0**
- HTTP consumed: **2**
- Integration findings: **0**
- Discovery complete: **false**
- Contract enrichment unresolved: **0**
- Semantic complete: **0/0**
- Semantic unresolved: **0**

## Exposed HTTP

No exposed HTTP endpoints were proven.
## Consumed HTTP

### `GET https://maps.googleapis.com/maps/api/geocode/json`

- Endpoint ID: `ep_74dc3d085e619b689e51`
- Confidence: `confirmed`
- Evidence: index_archivos/tracking/vue/components/location.component.js:104

### `POST https://api.sendgrid.com/v3/mail/send`

- Endpoint ID: `ep_12a92dbed8ff00fb6f9e`
- Confidence: `confirmed`
- Evidence: index_archivos/embarques/EmbarqueClass.php:558

## Integration surfaces

No non-HTTP integration operations were proven.
## Unresolved

- **http_client_detected_no_calls** — HTTP client 'guzzle' was detected by inventory but no supported direct calls were proven. Wrapper or dynamic usage may exist.

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
