# Endpoint Findings - augmented pass

Status: REVIEW_REQUIRED

New findings produced after correcting Brownfield's zero-route blind spot:

- Direct PHP/AJAX endpoint candidates found: 241
- Strong AJAX endpoint candidates: 96
- Strong direct endpoint candidates: 65
- Public PHP logic candidates exposed under webroot: 8
- Likely third-party/test candidates to exclude or block at web server: 5
- Endpoint candidates referenced by frontend/PHP callers: 55
- PHP caller references not matched to scanned endpoint candidates: 15
- POST/REQUEST endpoints without local CSRF signal: 73
- DB-writing endpoints without local CSRF signal: 7
- Upload/import endpoints requiring file validation review: 47
- JSON endpoints: 127
- Endpoints without local auth/session evidence: 71

Top corrective action: use this catalog instead of Brownfield's native zero-route output when auditing HTTP exposure.
