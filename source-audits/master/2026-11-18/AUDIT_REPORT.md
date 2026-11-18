# Auditoria de Proveedores master

Fecha: 2026-11-18. Fuente: KPO-Group/proveedores.
Master: `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`.
Peru comparado: `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`.

## Resultado

El conocimiento principal ahora se reconstruye desde master. Las particularidades
observadas de Bolivia y las adiciones/diferencias de Peru se documentan en
perfiles separados. El esquema historico de Peru y el grafo antiguo se conservan
sin atribuirlos a master.

Ademas se analizo el asgard.sql local como candidato independiente: 1,432
tablas, 13,149 columnas, 62 relaciones y 158 objetos SQL, sin ejecutar el dump
ni publicar datos. Su correspondencia con master y su pais no estan confirmados.

Se documentan 81 conceptos de negocio, 51 reglas, actores y permisos, procesos,
manual de usuario, arquitectura, integraciones, referencia de API, modelo de datos
con sus limites, operacion y pruebas. Los 891 candidatos del extractor historico
tienen disposicion individual: 122 con referencias candidatas en master y 769
sin referencia actual verificada. Ninguno recibe aprobacion de negocio por esa
clasificacion automatica.

## Verificaciones realizadas

| Tecnica | Resultado |
| --- | --- |
| Inventario Git | 10,629 entradas versionadas de master |
| Comparacion de arboles | 10,466 entradas iguales; 157 blobs distintos; 2 gitlinks distintos; 4 entradas solo master y 60 solo Peru |
| Brownfield | 1,091 evidencias; 762 SQL, 112 transiciones, 35 transacciones, 7 marcas heuristicas de permiso en dependencias y 175 candidatos sensibles redactados |
| Graphify AST | 545 archivos seleccionados; 2,173 nodos y 2,711 aristas; 319 archivos sin simbolos mas alla del nodo de fichero |
| PHP/AJAX | 241 candidatos de endpoints, 87 referencias de callers y 20 candidatos de consumo externo |
| Referencias de entrada/datos | 1,222 accesos a campos; 942 tokens SQL y 134 nombres de tabla candidatos, sin DDL master |
| Sintaxis PHP | 279 archivos con PHP 8.4.25, 276 pasan y 3 fallan por ternarios anidados; no demuestra runtime de produccion |
| Guardas aisladas | 8/8 casos CLI, sin handlers de negocio, base de datos ni red |
| Pruebas independientes de seguridad | 12/12 casos controlados, sin sesiones persistentes, base de datos ni red |
| Instalacion | Paquete instalado en checkout aislado; codigos de snapshot coincidentes y cambios locales distinguidos de cobertura SQL pendiente |

La revision cruzo inventario y AST con scripts PHP directos, includes, consultas,
pantallas y reglas. Se verificaron referencias de fuente y limites de lineas,
formatos, hashes, navegacion y preservacion del historial. Los resultados
completos estan en `knowledge/snapshots/current/knowledge-validation.json`.

## Riesgos priorizados

La revision de seguridad recoge 14 hallazgos: siete P1 y siete P2. Incluyen
autorizacion insuficiente en el flujo final de recuperacion de clave, SQL sin
parametrizar en handlers seleccionados, identidad suministrada por el cliente
en la autenticacion de segundo factor, aceptacion de clave maestra, problemas
de terminacion del control compartido en el camino legacy, credenciales en
codigo y otros riesgos de archivos, transporte, diagnostico y logging.

Cada hallazgo conserva precondiciones y salvedades: no se afirma explotacion
de produccion. PHP 5.4 declarado y PHP 8.4 probado no se confunden. Los controles
de guarda existentes se reconocen; superar una prueba aislada no demuestra
autorizacion de propietario o tenant en el handler completo.

Ver `knowledge/general/security-audit.md` y `security-findings.json` para
ubicaciones, trazas, prioridad, recomendaciones y pruebas de cada hallazgo.
No se modifico el codigo de aplicacion para corregirlos.

## Limites pendientes

Falta DDL de aplicacion para master, entorno real de ejecucion, revision de
los dos submodulos, contratos efectivos de servicios y matriz de permisos por
cliente. El lanzador nativo ASGARD API Auditor fue bloqueado por Windows
Application Control; se realizaron analisis alternativos, sin presentar esa
ejecucion como completada ni sus resultados como cero APIs.

El baseline Brownfield sigue `INCOMPLETE_BASELINE`; la documentacion basada
en fuente no equivale a especificacion canonica aprobada. La cobertura global
permanece PARTIAL y las preguntas pendientes se mantienen accionables.
