# Verificacion del paquete actualizado

Fecha: 2026-11-18. Perfil principal master
`a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; comparacion Peru
`95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`.

| Comprobacion | Resultado |
| --- | --- |
| Glosario, esquema JSON e indices | PASS; 81 conceptos con evidencia y confianza explicitas |
| Candidatos historicos | PASS; 891 entradas contabilizadas y clasificadas individualmente |
| Referencias de fuente | PASS; commits, rutas y limites de linea comprobados en ambos checkouts |
| Navegacion y formatos actuales | PASS; enlaces locales, JSON/CSV, XML de XLSX y hashes |
| Hallazgos de seguridad | 15 revisados; ocho P1 y siete P2 con precondiciones y límites; SEC-015 nuevo |
| Revisión iterativa | Véase [delta y criterio de cierre](../../reviews/iterative-20261118/README.md), con defectos operativos, mejoras y registros de pasadas |
| Guardas aisladas | 8/8 casos correctos |
| Pruebas independientes de seguridad | 12/12 casos reproducibles correctos, sin DB/red/sesion persistente |
| Lint de aplicacion | 276/279 pasan bajo PHP 8.4.25; tres fallos documentados, sin afirmar compatibilidad de produccion |
| Scripts de soporte | Sintaxis PowerShell y Python comprobada |
| Instalacion aislada | PASS; se incluyen validadores y helpers de restauracion |
| Gate de cobertura | Detecta codigo coincidente y cambio funcional local; mantiene separada la validacion SQL pendiente |
| Recuperacion del grafo actual | PASS; contenido y hash verificados |
| Historia original de Peru | PASS; 1,741 artefactos y 3,313 entradas de siete checkpoints preservados |
| SQL local candidato | Estructura extraida por separado, sin ejecutar SQL ni publicar registros; correspondencia con master pendiente |

Los resultados exactos del perfil actual se guardan en
`knowledge-validation.json`. Los del transporte historico estan en
`transfer-validation.json`. La validacion confirma integridad y referencias,
no cierre de vulnerabilidades ni aprobacion funcional de negocio.

El codigo de la aplicacion permanece intacto; solo se generaron metadatos de
auditoria en el checkout aislado. La cobertura global sigue PARTIAL por esquema
efectivo, despliegue, submodulos, contratos externos y aprobacion pendientes.
