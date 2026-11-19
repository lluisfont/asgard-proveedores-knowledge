# asgard-proveedores Knowledge Pack

Este paquete documenta la rama master de Proveedores y separa las variantes de
Bolivia y Peru. Empezar por [INDEX.md](INDEX.md), [alcance](audit-scope.md) y
[glosario de negocio](glossary/business-glossary.md). Las auditorias antiguas
de Peru se conservan como historial.

## Punto De Entrada

Para agentes y OpenSpec:

- `openspec/context.md`
- `openspec/guardrails.md`
- `openspec/impact-rules.md`
- `crosswalk/risks-unresolved.md`

Para producto:

- `product/requirements-analysis-guide.md`
- `product/business-domains.md`
- `product/user-manual-source.md`

## Estado

Ver `manifest.json`.

La fuente general auditada está fijada al commit master
`a8ce2c23dead8552d2c4699e4a9b9134f7a18707`. La comparación histórica usa
master_peru `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` y la auditoría corregida de
Perú HEAD fija `2a179e2e6472d5705d031665ecbc90c3d806edec`. El master HEAD
`a44f4ed69470f1bc00c800e592eadfce1bac6053` está revisado por delta: el padre
no cambia y solo avanza un gitlink cuyo contenido interno no está auditado. Falta acreditar
el esquema físico de master, la ejecución real y la aprobación de negocio.

## Regla

UNKNOWN > GUESS. No convertir inferencias en requisitos confirmados sin revision humana.

