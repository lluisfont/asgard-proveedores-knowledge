# Alcance y procedencia de la transferencia

Fecha de transferencia: 2026-10-01.

El paquete se genera con `lluisfont/convertidor-knowledge`, commit
`80735144d6609ee2dd8035ec9388510c229d03b9`. La adaptacion reproducible de las
rutas de auditoria se conserva en `scripts/transfer/export_knowledge.py`.

## Fuentes

| Fuente | Papel | Estado |
| --- | --- | --- |
| `C:/repos/proveedores` | Checkout actual del proyecto, remoto GitLab `kpo-group/asgard-project/proveedores` | Incluye modificaciones locales anteriores a esta transferencia |
| `C:/repos/proveedores-master_peru` | Copia historica auditada con Graphify, Brownfield y ASGARD API Auditor el 2026-09-15 | No contiene `.git`; no se ha demostrado equivalencia completa con el checkout actual |
| `C:/repos/proveedores/graphify-asgard-audit` | Auditorias historicas realizadas a la herramienta Graphify | Archivadas como material relacionado; sus hallazgos no describen Proveedores |

## Evidencia transferida

- Grafo completo, informe, visualizacion, cache de extraccion, manifiestos,
  memoria y reflexiones de Graphify.
- Estado, configuracion, esquemas, instrucciones, prompts y scanners personalizados
  de Brownfield; inventarios, evidencia, diccionarios, mapas, glosario,
  reconstruccion semantica, entregables y resultados de completitud.
- Auditorias nativas ASGARD, catalogo aumentado PHP/AJAX, OpenAPI provisional,
  llamadas consumidas, matrices de seguridad y resultados de las pasadas profundas.
- Informes iterativos originales y todos los checkpoints historicos Brownfield.
- Comparacion SHA256 del inventario auditado con los archivos del checkout actual.

El indice completo esta en `transfer-artifacts.json`. Cada artefacto conserva
procedencia, ruta original, hash original y hash de la copia exportada.
Los checkpoints se almacenan como manifiestos y objetos deduplicados; todas sus
entradas se pueden reconstruir con `scripts/transfer/restore_artifacts.py`.

No se publica el codigo de la aplicacion, el dump SQL, `.env.php`, los entornos
Python ni los ejecutables. Los scripts de extraccion y los fragmentos necesarios
para interpretar evidencias se conservan con redaccion de credenciales detectadas.
Los hashes originales permiten verificar la procedencia sin publicar sus valores.

## Limites de confianza

Brownfield declara `INCOMPLETE_BASELINE`, con baseline sin confirmar, cobertura
determinista del 11.62% y sin dominios canonicos. Las plantillas materializadas
siguen siendo borradores; su existencia no demuestra validacion funcional.

ASGARD API Auditor devuelve `partial`. Su detector nativo no reconoce la
superficie principal PHP/AJAX: sus cero endpoints expuestos no prueban ausencia
de APIs. El catalogo aumentado contiene candidatos estaticos y necesita
verificacion de despliegue, autenticacion y comportamiento en ejecucion.

Graphify incluye codigo de terceros. Sus enlaces `INFERRED` y sus comunidades
no son requisitos de negocio confirmados. Algunas consultas generales seleccionan
simbolos de librerias externas; hay que comprobar `source_file` y `source_location`.

La coincidencia de archivos individuales con el inventario historico no convierte
el checkout actual en una version totalmente auditada. El estado del paquete es
`PARTIAL`. Un `PASS` del validador confirma integridad y estructura del transporte.

## Reproducibilidad

```powershell
python scripts/transfer/validate_transfer.py
.\scripts\knowledge\validate.ps1 -Root .
```

Para abrir el grafo completo en herramientas que requieren `graph.json`:

```powershell
python scripts/transfer/restore_artifacts.py --file source-audits/graphify/graph.json.gz --destination C:/temp/proveedores-graph
```

Para restaurar un checkpoint se usa `--checkpoint` con uno de los manifiestos
de `source-audits/history/` y un directorio de destino nuevo. Los antiguos
`MANIFEST.json` y `SHA256SUMS.txt` describen los archivos originales. Para la
copia exportada y redactada se verifican los campos `export_sha256` del manifiesto
de transferencia.
