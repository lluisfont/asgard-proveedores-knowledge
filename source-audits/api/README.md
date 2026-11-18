# API Knowledge historico de Peru

La referencia actual de master esta en
`knowledge/general/api-reference.md` y los artefactos nuevos en
`source-audits/master/2026-11-18/brownfield/custom/`.
Las cifras y resultados de este documento describen exclusivamente la
auditoria historica de Peru, no la ejecucion actual sobre master.

Version del auditor nativo: `asgard-api-auditor 0.8.0`.
Fecha de las auditorias originales: 2026-09-15.
Estado: `partial_with_static_augmentation`.

La ejecucion nativa se realizo sobre una copia temporal Git de
`proveedores-master_peru`, con commit temporal
`f4f6d607c39d5b911b2f6e1dbf98c9658d5b3f4a`. Ese identificador no es un commit
confirmado del repositorio GitLab actual.

- `asgard-api-audit/`: primera ejecucion nativa.
- `asgard-api-audit-v2/`: ejecucion nativa con exclusiones de dependencias.
- `asgard-api-audit-augmented/`: catalogo PHP/AJAX, OpenAPI provisional,
  llamadas externas y matriz endpoint-seguridad-base de datos.
- `api-deep-iterative/`: riesgos por endpoint y consumidor, y registro iterativo.

El detector nativo encontro cero endpoints expuestos y dos consumidos, con
cobertura parcial. La ampliacion estatica identifico 246 candidatos expuestos
y 23 candidatos de consumo. Esas cifras describen tecnicas distintas y no deben
interpretarse como inventario runtime confirmado.

Los scripts de ampliacion y scanner profundo se conservan en
`../brownfield/verification/custom_tools/`. El informe iterativo completo esta
en `../brownfield/reports/iterative/AUDITORIA_ASGARD_API_ITERATIVA.md`.
