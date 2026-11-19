# ASGARD Proveedores Knowledge

Conocimiento tecnico y de negocio de Proveedores, actualizado el 2026-11-19
desde [KPO-Group/proveedores](https://github.com/KPO-Group/proveedores).
La base general de contenido es `master` en `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`;
el HEAD `a44f4ed69470f1bc00c800e592eadfce1bac6053` está revisado por delta y no
cambia ningún archivo del repositorio padre. La comparación histórica usa
`master_peru` en `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` y Perú HEAD está revalidado
en `2a179e2e6472d5705d031665ecbc90c3d806edec`.
Las particularidades de Bolivia y Peru se documentan por separado.
La transferencia original realizada con convertidor-knowledge queda conservada
como evidencia historica de Peru.

## Empezar

- [Indice completo](knowledge/INDEX.md).
- [Alcance actual y procedencia](knowledge/audit-scope.md).
- [Diccionario de negocio](knowledge/glossary/business-glossary.md), tambien en [JSON](knowledge/glossary/business-glossary.json) y [CSV](knowledge/glossary/business-glossary.csv).
- [Variantes Bolivia y Peru](knowledge/variants/README.md).
- [Manual de usuario](knowledge/general/user-manual.md).
- [Procesos](knowledge/general/workflows.md) y [reglas de negocio](knowledge/general/business-rules.md).
- [Arquitectura](knowledge/general/architecture.md) y [referencia API](knowledge/general/api-reference.md).
- [Auditoria de seguridad](knowledge/general/security-audit.md).
- [Revisión iterativa y cambios respecto a la auditoría anterior](knowledge/reviews/iterative-20261118/README.md).
- [Auditoría corregida de Perú HEAD](knowledge/reviews/peru-head-20261119/README.md).
- [Revisión incremental de master HEAD](knowledge/reviews/master-head-20261119/README.md).
- [Defectos operativos y pruebas de invariantes](knowledge/general/operational-findings.md).
- [Mapa de evidencias](knowledge/evidence-map.md).
- [Manifiesto del paquete](knowledge/manifest.json).
- [Inventario de transferencia y hashes](knowledge/transfer-artifacts.json).
- [Dominios y superficie candidata](knowledge/product/business-domains.md).
- [Guia del modelo de datos](knowledge/product/data-model-guide.md).
- [Pantallas, endpoints y tablas](knowledge/crosswalk/screens-endpoints-tables.md).
- [Endpoints, servicios y SQL](knowledge/crosswalk/endpoints-services-sql.md).
- [Permisos observados](knowledge/crosswalk/modules-permissions-clients.md).
- [Riesgos y decisiones pendientes](knowledge/crosswalk/risks-unresolved.md).

## Evidencia conservada

| Area | Contenido |
| --- | --- |
| Graphify master | AST local: 2,173 nodos y 2,711 aristas; cobertura complementada con scripts PHP directos |
| Brownfield master | 1,091 evidencias; esquema SQL de master ausente |
| API master | 241 candidatos PHP/AJAX y 20 candidatos de consumo; revision estatica aumentada |
| Variantes | Comparacion de archivos y revision funcional de master/Bolivia frente a master_peru |
| SQL local candidato | 1,432 tablas y 13,149 columnas extraidas por separado de asgard.sql; pais y correspondencia con master sin confirmar |
| Historia Peru | Grafo original, diccionario fisico de Peru y siete checkpoints recuperables |
| Inventario actual | 10,629 entradas versionadas; 545 archivos de codigo seleccionados y 279 PHP comprobados |
| Material relacionado | Auditorias de la herramienta Graphify, identificadas separadamente |

La auditoria actual esta fijada a commits concretos de GitHub. Las fuentes del
2026-09-15 y la comparacion de la transferencia del 2026-10-01 permanecen como
historial, sin convertir el dump de Peru en esquema general.

El estado global sigue **PARTIAL**: falta el esquema SQL de master, el entorno
real de ejecucion, la auditoria interna de los submodulos y la aprobacion de negocio.
Las definiciones y procesos se han reconstruido con evidencia de codigo y un
registro explicito de inferencias y preguntas pendientes. La auditoria nativa
ASGARD no pudo ejecutarse por bloqueo de Windows Application Control; se uso
ampliacion estatica. Ninguna plantilla historica se presenta como validacion.

El [diccionario SQL local candidato](knowledge/general/local-schema-candidate.md)
conserva estructura adicional encontrada en el workspace. Su existencia no
acredita que sea la base usada por master ni sustituye la confirmacion pendiente.

## Validar

```powershell
.\scripts\knowledge\validate.ps1 -Root .
python scripts/transfer/validate_transfer.py
python scripts/audit/validate_knowledge.py
```

La validacion comprueba estructura, integridad, formatos y contenido transferido.
Su `PASS` no implica que se hayan corregido los riesgos ni completado la auditoria.

## Recuperar artefactos

Los archivos grandes estan comprimidos sin perdida. Para recuperar `graph.json`:

```powershell
python scripts/transfer/restore_artifacts.py --file source-audits/master/2026-11-18/graphify/graph.json.gz --destination C:/temp/proveedores-master-graph
```

Para reconstruir un checkpoint:

```powershell
python scripts/transfer/restore_artifacts.py --checkpoint source-audits/history/brownfield_checkpoint_20260915_172701_112419Z.json --destination C:/temp/proveedores-checkpoint
```

El restaurador verifica hashes, limita las rutas al destino elegido y evita
sobrescribir archivos existentes.

## Instalar en un checkout

```powershell
.\install-knowledge-pack.ps1 -TargetRepo C:/ruta/al/checkout
```

Revisar [QUICK_START.md](QUICK_START.md) y el estado de cobertura antes de usar
el paquete para cambios. Los valores `unknown`, `partial` e `inferred` conservan
su significado original.
