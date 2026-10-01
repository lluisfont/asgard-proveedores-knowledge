# Verificacion de la transferencia

Fecha: 2026-10-01.

| Comprobacion | Resultado |
| --- | --- |
| Validador original de convertidor-knowledge | PASS |
| Hashes y formatos de 1,741 artefactos | PASS |
| Hashes de 3,313 entradas de siete checkpoints | PASS |
| Payloads distintos verificados | 2,197 |
| Graphify completo | 48,495 nodos y 116,642 aristas |
| Sintaxis de scripts PowerShell y Python de transferencia | PASS |
| Restauracion real de graph.json | PASS, con verificacion de hash |
| Restauracion real del checkpoint final | PASS, 487 entradas con hashes verificados |
| Codigo de aplicacion, dump SQL y archivos de entorno en source-audits | No exportados |
| Tokens con formatos conocidos en evidencias, comprimidos y XLSX | Sin coincidencias pendientes |
| Cobertura funcional actual de la auditoria | PARTIAL; no demostrada para todo el checkout |

El resultado verificable en formato JSON se conserva en
`transfer-validation.json`. La comparacion de archivos con el inventario
auditado esta en `audited-source-comparison.json`.

Esta verificacion confirma el transporte de evidencia y la capacidad de
reconstruirla. Las observaciones de riesgo originales conservan su nivel de
confianza; la transferencia no valida reglas de negocio ni corrige defectos.
