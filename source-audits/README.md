# Auditorias originales y procedencia

| Carpeta | Proyecto auditado | Papel |
| --- | --- | --- |
| `graphify/` | Proveedores, copia `proveedores-master_peru` | Grafo historico completo y artefactos de extraccion |
| `brownfield/` | Proveedores, copia `proveedores-master_peru` | Baseline determinista, evidencias, reconstruccion y borradores |
| `api/` | Proveedores, copia `proveedores-master_peru` | Auditoria API nativa y aumentada, con estados parciales |
| `history/` | Proveedores, copia `proveedores-master_peru` | Todos los checkpoints Brownfield en forma reconstruible |
| `related-graphify-audits/` | Graphify v0.9.61 y sus interfaces | Auditorias de una herramienta, conservadas como contexto historico |

Los hallazgos de `related-graphify-audits/` no describen vulnerabilidades ni APIs
de Proveedores. Se conserva su texto original y sus evidencias para evitar
perder el contexto del trabajo anterior.

Los informes iterativos de Proveedores estan en `brownfield/reports/iterative/`.
Los informes de seguridad, integridad SQL y ampliacion de endpoints estan en
`brownfield/reports/custom/`. La configuracion y los scanners se conservan en
`brownfield/verification/`.

Consultar `knowledge/transfer-artifacts.json` para localizar cada entrada original
y verificar sus hashes. El contenido de los checkpoints esta deduplicado: los
manifiestos enumeran todas las entradas y sus objetos correspondientes.
