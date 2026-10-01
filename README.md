# ASGARD Proveedores Knowledge

Conocimiento tecnico y funcional de Proveedores, transferido con
[convertidor-knowledge](https://github.com/lluisfont/convertidor-knowledge)
el 2026-10-01. Incluye las auditorias originales, evidencia reproducible,
versiones historicas y herramientas para consultarlas sin el codigo fuente.

## Empezar

- [Alcance y procedencia](knowledge/transfer-scope.md).
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
| Graphify | Grafo completo de 48,495 nodos y 116,642 aristas, visualizacion, informe y cache |
| Brownfield | 4,471 evidencias, modelo de 1,055 tablas y 10,111 columnas, mapas de procesos y entregables |
| ASGARD API | Auditorias nativas, 246 candidatos PHP/AJAX, 23 candidatos de consumo y matrices de riesgos |
| Historia | Siete checkpoints Brownfield, recuperables desde manifiestos y objetos deduplicados |
| Checkout actual | Inventario de hashes y comparacion con la copia auditada |
| Material relacionado | Auditorias de la herramienta Graphify, identificadas separadamente |

Las auditorias de Proveedores proceden de `proveedores-master_peru`, fechadas
2026-09-15. La comparacion con `C:/repos/proveedores` encuentra 1,452 archivos
iguales, 48 diferentes y cinco ausentes del inventario historico.

El estado es **PARTIAL**: Brownfield mantiene `INCOMPLETE_BASELINE` y las APIs
son candidatas estaticas. No existe un commit auditado confirmado. Los dominios,
requisitos y secuencias de negocio inferidos requieren revision humana.
Las plantillas de release no equivalen a especificaciones validadas.

## Validar

```powershell
.\scripts\knowledge\validate.ps1 -Root .
python scripts/transfer/validate_transfer.py
```

La validacion comprueba estructura, integridad, formatos y contenido transferido.
Su `PASS` no implica que se hayan corregido los riesgos ni completado la auditoria.

## Recuperar artefactos

Los archivos grandes estan comprimidos sin perdida. Para recuperar `graph.json`:

```powershell
python scripts/transfer/restore_artifacts.py --file source-audits/graphify/graph.json.gz --destination C:/temp/proveedores-graph
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

