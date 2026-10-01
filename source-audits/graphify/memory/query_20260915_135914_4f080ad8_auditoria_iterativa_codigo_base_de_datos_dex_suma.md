---
type: "query"
date: "2026-09-15T13:59:14.955164+00:00"
question: "Auditoria iterativa codigo base de datos dex_suma SQLi IDOR Graphify"
contributor: "graphify"
outcome: "useful"
source_nodes: ["dex_suma", "permisos.php", "TrackingNewClass"]
---

# Q: Auditoria iterativa codigo base de datos dex_suma SQLi IDOR Graphify

## Answer

Expanded from original query via graph vocab: dex,suma,items,mysql,query,post,get,embarques,tracking,permisos. Traversed Graphify and confirmed relationships among dex_suma, permisos.php, TrackingNewClass and embarques/tracking/exportaciones communities; line-level audit then identified ActualizarMICs.php raw POST item IDs flowing into INSERT/UPDATE dex_suma SQL.

## Outcome

- Signal: useful

## Source Nodes

- dex_suma
- permisos.php
- TrackingNewClass