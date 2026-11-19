# Revisión iterativa de Perú HEAD — 19-11-2026

Esta revisión corrige la auditoría anterior de la variante Perú y fija `master_peru`
en `2a179e2e6472d5705d031665ecbc90c3d806edec`. La comparación histórica se
mantiene en P95 `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` y la referencia de
master en `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`. El nuevo master remoto
`a44f4ed69470f1bc00c800e592eadfce1bac6053` queda fuera de este alcance.

El resultado aceptado contiene **4 hallazgos** y **8 mejoras documentales**.
La revisión convergió después de dos pases consecutivos sin delta material: un
cierre SQL por AST/metamorfismos y un cierre inverso de procedencia sobre esta
publicación. La convergencia se limita al alcance revisado; el estado global
sigue **PARTIAL** y no certifica producción, base de datos, permisos efectivos
ni aprobación de negocio.

## Resultado aceptado

| ID | Tipo | Síntesis | Relación con P95 |
| --- | --- | --- | --- |
| PH-001 | Hallazgo | El ID genérico de proveedor se usa como transportista sin discriminar tipo 7. | Efecto cambiado en HEAD; condicionado a acceso y colisión de dominios. |
| PH-002 | Hallazgo | El filtro de fechas puede alterar el predicado que acota al proveedor. | Heredado de P95; se documenta la consecuencia sobre el nuevo límite de propietario. |
| PH-003 | Hallazgo | Las relaciones globales por chasis pueden atravesar el alcance de cabecera. | Heredado de P95; requiere multiplicidad o reutilización de VIN. |
| PH-004 | Hallazgo | Los `MAX` independientes pueden formar una relación de embarque/viaje que nunca existió. | Heredado de P95; condicionado a múltiples relaciones. |
| PH-IMP-001 | Mejora | Separar proveedor de cabecera y concesionario como dominios distintos. | Cambio explícito P95→HEAD. |
| PH-IMP-002 | Mejora | Precisar que estado y tipo filtran filas antes del pivote. | Contrato SQL heredado. |
| PH-IMP-003 | Mejora | “Realizado” demuestra presencia, no completitud de secciones. | Contrato SQL heredado. |
| PH-IMP-004 | Mejora | Distinguir constructor, includes, auxiliares y ejecutor del reporte. | Corrige una atribución demasiado amplia. |
| PH-IMP-005 | Mejora | `query.php` construye la consulta; `data.php` la ejecuta en el contexto del caller. | Corrige el candidato histórico. |
| PH-IMP-006 | Mejora | Cinco solicitudes de negocio conservan rangos exactos dentro del JS cambiado. | Carry-forward acotado, no cinco APIs nuevas verificadas. |
| PH-IMP-007 | Mejora | Una cita local idéntica no prueba equivalencia de una dependencia modificada. | Cuatro conceptos conservan frontera pendiente. |
| PH-IMP-008 | Mejora | La revalidación conserva la procedencia M/P95 sin inventar mappings M→P. | 80 conceptos con evidencia P95; uno solo M. |

El registro íntegro y reproducible está en [accepted-deltas.json](accepted-deltas.json).
Las versiones acumulativas, hashes semánticos y criterio de parada están en
[iterations.json](iterations.json). La vista funcional está en
[Perú HEAD](../../variants/peru-head-20261119.md).

## Evidencia y pruebas

- [Deltas del informe](report-deltas.md) y su [JSON](report-deltas.json).
- [Cierre SQL](closure-sql.md) y su [JSON](closure-sql.json).
- [Arrastre de evidencia](carryforward-deltas.md) y su [JSON](carryforward-deltas.json).
- [Cierre inverso de procedencia](closure-provenance.md) y su [JSON](closure-provenance.json).
- [Cinco solicitudes acotadas](../../variants/peru-api-head-20261119.md).
- [Overlay de glosario](../../glossary/peru-head-revalidation.json), sin modificar los 81 conceptos base.
- [Artefactos fuente](../../../source-audits/peru/2026-11-19/).

La captura contiene 10.685 entradas: 10.682 son idénticas a P95 por
`(ruta, modo, tipo, OID)` y tres rutas cambian. Graphify produjo 2.351 nodos y
2.694 aristas sobre 558 candidatos de código, mediante AST local y sin
extracción semántica. La identidad Git y el AST no prueban ejecución, política
de autorización, contratos externos ni despliegue.

## Límites

- No se ejecutó la aplicación, PHP de negocio, SQL, HTTP, navegador ni base de datos.
- No se usaron filas reales, secretos ni credenciales de producción.
- La auditoría nativa ASGARD no se reintentó tras el bloqueo previo de AppControl.
- La revisión rechazada de salidas/navegación/recarga no se cuenta como pase de cierre.
- El master remoto `a44f4ed…` y los submódulos quedan fuera del perfil.
- Los tres fallos de lint en PHP 8.4 describen compatibilidad del checkout, no el runtime desplegado.

## Reproducir y validar

```powershell
python -B scripts/audit/compile_peru_head_review.py
python -B scripts/audit/index_artifacts.py
python -B scripts/audit/validate_knowledge.py --source C:/ruta/master-a8c --peru-source C:/ruta/peru-p95 --peru-head-source C:/ruta/peru-head
python scripts/transfer/validate_transfer.py
```

Un `PASS` comprueba integridad, referencias y consistencia del expediente; no
cambia el estado global `PARTIAL` ni convierte los hallazgos en requisitos
canónicos aprobados.
