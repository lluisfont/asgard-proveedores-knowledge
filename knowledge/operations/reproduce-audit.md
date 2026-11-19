# Reproducir la auditoria fijada

Esta receta reproduce la base completa del 2026-11-18; los scripts rechazan
commits distintos. El perfil incremental del 2026-11-19 conserva esa base porque
las 10.628 entradas del padre ajenas al gitlink son idénticas por objeto Git.

## Entradas

- Checkout autorizado de KPO-Group/proveedores con master fijado a
  `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`.
- Referencia origin/master_peru fijada a
  `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`.
- Worktree opcional de Peru para verificar las lineas de ambas ramas.
- Python 3.12, graphifyy 0.9.108, brownfield-refactor-kit 0.2.3 y sus
  dependencias; PHP 8.4.25 CLI para lint y pruebas aisladas.

El codigo privado se mantiene en un checkout separado del repositorio de
conocimiento. Las credenciales y dumps operativos no se publican.

## Extraccion y ampliacion

Instalar Brownfield en el checkout aislado con sus instrucciones de instalacion,
usar `project.yaml` exportado como configuracion de exclusiones y ejecutar
verify-config, seed-baseline y semantic-reconstruct. El esquema SQL de master
no fue suministrado: una reproduccion no debe sustituirlo por el dump de Peru.

Desde el repositorio de conocimiento, con la ruta del checkout de master:

```powershell
python scripts/audit/collect_master.py collect --source C:/ruta/master
python scripts/audit/collect_master.py graph --source C:/ruta/master
python scripts/audit/legacy/php_endpoint_scanner.py --root C:/ruta/master
python scripts/audit/legacy/deep_security_scanner.py --root C:/ruta/master
python scripts/audit/legacy/asgard_api_augmentation.py --root C:/ruta/master
```

El scanner profundo adicional `api_iterative_deep_audit.py` usa como directorio
actual el checkout de master. Ejecutarlo alli una vez generados los catalogos.
El resultado nativo ASGARD falta por bloqueo de Application Control y se
registra separadamente; no se reinterpreta como ausencia de endpoints.

## Exportar y verificar

```powershell
python scripts/audit/export_master.py --source C:/ruta/master
python scripts/audit/render_graph.py
python scripts/audit/probe_guards.py --source C:/ruta/master
python scripts/audit/security_probes.py --source C:/ruta/master
python scripts/audit/build_knowledge.py
python scripts/audit/index_artifacts.py
python scripts/audit/validate_knowledge.py --source C:/ruta/master --peru-source C:/ruta/peru
python scripts/transfer/validate_transfer.py
```

La reconstruccion funcional, las 51 reglas y las definiciones del glosario
incluyen lectura y revision de evidencia; no se regeneran por expansion de
nombres SQL. Los scripts producen inventarios y vistas y validan referencias;
no sustituyen esa revision ni la aprobacion por negocio.

El perfil SQL local candidato requiere el asgard.sql original con huella
`a0833cde6629ac2d458dad6faaa17df4c61af19401eacad59e4bc4400aa5d1e5`.
Se analiza con data-dictionary en un directorio aislado y se exporta con
`scripts/audit/export_local_schema.py --parsed-root RUTA --original RUTA_SQL`.
Repetir despues index_artifacts y validate_knowledge. El dump original no se
incluye en el repositorio de conocimiento y la exportacion no confirma su
correspondencia con master.

La receta no inicia servicios de aplicacion, no construye Docker, no conecta a
base de datos ni ejecuta mutaciones por HTTP. Las pruebas de seguridad usan
guardas o metodos aislados con sustitutos controlados y registran sus limites.

## Revisión incremental de master HEAD

Comparar la base y el HEAD, y verificar que el único delta sea el gitlink:

```powershell
git diff-tree --no-commit-id --raw -r a8ce2c23dead8552d2c4699e4a9b9134f7a18707 a44f4ed69470f1bc00c800e592eadfce1bac6053
git ls-tree a8ce2c23dead8552d2c4699e4a9b9134f7a18707 index_archivos/intercambioDocumental
git ls-tree a44f4ed69470f1bc00c800e592eadfce1bac6053 index_archivos/intercambioDocumental
python -B scripts/audit/validate_knowledge.py --source C:/ruta/master-a8c --master-head-source C:/ruta/master-a44
```

Para auditar el contenido interno debe estar disponible el objeto
`88e6d6a58ef54662eaa604aa060adbeba96098ff` del GitLab configurado en
`.gitmodules`. Sin él solo se reproduce el cierre del repositorio padre.

## Ampliación iterativa

La [revisión iterativa](../reviews/iterative-20261118/README.md) conserva por separado las propuestas iniciales, su aceptación/deduplicación y los cierres. Para reproducir sus pruebas desde la raíz del paquete:

```powershell
python -B scripts/audit/report_contract_probes.py --source C:/ruta/master --output source-audits/master/2026-11-18/iterative/report-contract-probes.json
python -B scripts/audit/transaction_probes.py --source C:/ruta/master --output source-audits/master/2026-11-18/iterative/transaction-probes.json
python -B scripts/audit/contract_consistency_probes.py --source-repo C:/ruta/master
python -B scripts/audit/static_arity_review.py --source C:/ruta/master
python -B scripts/audit/arity_contract_probes.py --source C:/ruta/master
python -B scripts/audit/sql_ast_crosscheck.py --source C:/ruta/master --parser-path C:/ruta/sqlglot-30.33.0
python -B scripts/audit/integrate_iterative_core.py
python -B scripts/audit/build_knowledge.py --view api-reference
python -B scripts/audit/build_knowledge.py --view glossary-csv
python -B scripts/audit/compile_iterative_review.py --close
python -B scripts/audit/index_artifacts.py
python -B scripts/audit/validate_knowledge.py --source C:/ruta/master --peru-source C:/ruta/peru
```

El parser SQLglot requiere su versión fijada y Brownfield instalado. El censo usa solo tokenización; las pruebas de aridad sustituyen el cuerpo por un centinela, hecho registrado en su JSON. No se reproduce la revisión rechazada de salidas al navegador/navegación ni se usa para el criterio de convergencia. La auditoría nativa ASGARD continúa bloqueada por AppControl y no se intenta eludir ese bloqueo.
