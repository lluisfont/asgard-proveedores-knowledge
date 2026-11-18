# Diccionario estructural SQL local candidato

Estado: LOCAL_SCHEMA_CANDIDATE_UNVERIFIED.

Fuente local: asgard.sql, dump etiquetado Asgard_dev/asgard con fecha 2026-07-23. No esta versionado en los commits auditados. Pais y correspondencia con master/Peru sin confirmar.

Extraccion Brownfield: 1432 tablas, 13149 columnas, 62 relaciones declaradas, 1717 indices y 158 objetos SQL.

121 de 134 nombres candidatos usados por master aparecen en este DDL. Eso demuestra coincidencia nominal, no compatibilidad completa ni autoridad del esquema.

## Catalogos

- [Tablas](../../source-audits/local-schema-candidate/2026-11-18/tables.csv).
- [Columnas y tipos](../../source-audits/local-schema-candidate/2026-11-18/columns.csv).
- [Relaciones declaradas](../../source-audits/local-schema-candidate/2026-11-18/relations.csv).
- [Indices](../../source-audits/local-schema-candidate/2026-11-18/indexes.csv).
- [Constraints](../../source-audits/local-schema-candidate/2026-11-18/constraints.csv).
- [Funciones/procedimientos](../../source-audits/local-schema-candidate/2026-11-18/database_objects.csv).
- [Estructura JSON comprimida](../../source-audits/local-schema-candidate/2026-11-18/structure.json.gz).
- [Procedencia y hash](../../source-audits/local-schema-candidate/2026-11-18/summary.json).

Se conservan lineas e IDs de evidencia del archivo local para revisar cada declaracion. No se publican registros INSERT, valores por defecto, direcciones de servidor ni cuerpos de rutinas. Las definiciones de negocio revisadas estan en el glosario; los nombres SQL no se convierten automaticamente en terminos validados.

## Pendiente de confirmar

Confirmar propietario, entorno y version de este dump y contrastar columnas, indices, rutinas y catalogos contra la base usada por cada commit desplegado. Hasta entonces este perfil se mantiene separado tanto del esquema historico de Peru como del modelo general basado en consultas de master.
