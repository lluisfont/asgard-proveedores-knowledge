# Reproducir la auditoria fijada

Esta receta reproduce el perfil del 2026-11-18; los scripts rechazan commits
distintos. Para una revision nueva se debe crear un perfil fechado y actualizar
sus fuentes, no sobrescribir silenciosamente esta instantanea.

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
