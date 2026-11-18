# Alcance de la auditoria actual

Fecha: 2026-11-18. Repositorio: `https://github.com/KPO-Group/proveedores`.

| Perfil | Fuente fijada | Uso |
| --- | --- | --- |
| Principal | master a8ce2c23dead8552d2c4699e4a9b9134f7a18707 | Codigo general observado; particularidades Bolivia separadas |
| Comparacion Peru | master_peru 95fe9a4c3b3cddd84be922cc0e1eb9c88603df62 | Diferencias funcionales, codigo y conceptos de variante |
| Historia Peru | Auditoria local 2026-09-15 sin commit Git confirmado | Evidencia del dump y artefactos historicos, no esquema universal |

## Tecnicas ejecutadas

Se inventariaron 10,629 entradas versionadas de master y se compararon los blobs
de ambas ramas. Se seleccionaron 545 archivos de codigo para extraccion AST
local Graphify y 279 PHP para chequeo sintactico con PHP 8.4.25 y short_open_tag
activado. Los tres fallos detectados describen esa version local; el Dockerfile
declara PHP 5.4 y no demuestra el runtime desplegado.

Brownfield genero 1,091 evidencias, incluidas 762 referencias SQL y 112 marcas
de transicion de estado. La ausencia de DDL de master se registra como tal.
Como fuente adicional separada, se analizo el asgard.sql local no versionado
y se exportaron solo sus estructuras: 1,432 tablas, 13,149 columnas, 62 relaciones
y 158 objetos SQL. Su cabecera de desarrollo no acredita pais ni correspondencia
con los commits desplegados. Ver `general/local-schema-candidate.md`.

El mapa tecnico identifica 59 componentes, 258 nodos y 857 aristas; no acredita
por si solo la secuencia real de cada proceso.

Graphify genero 2,173 nodos y 2,711 aristas mediante AST, sin llamadas LLM ni
extraccion semantica facturada. Emitio advertencia para 319 scripts sin simbolos
mas alla del nodo de archivo. Esa limitacion se complementa con catalogos de
superglobales, callers, scripts PHP y referencias SQL.

Los escaneres de ampliacion generaron 241 candidatos PHP/AJAX y 20 candidatos
de consumo externo. La ejecucion nativa de ASGARD API Auditor quedo bloqueada
por Windows Application Control; no se presenta como realizada ni como cero
APIs. Los metodos, parametros y rutas efectivos requieren comprobacion HTTP.

Se cruzaron las evidencias con lectura directa de clases, pantallas, menus,
controles y reglas. Se ejecutaron ocho casos CLI aislados sobre guardas de
descarga, sin handlers de negocio, base de datos ni llamadas externas.

## Separacion de fuentes

Los artefactos actuales estan en `source-audits/master/2026-11-18/`.
El grafo y modelo fisico antiguos de `source-audits/graphify/` y
`source-audits/brownfield/` proceden de Peru. Los hallazgos de
`source-audits/related-graphify-audits/` describen la herramienta Graphify,
no vulnerabilidades de Proveedores.

Los perfiles Bolivia y Peru se apoyan en diferencias observadas, no solo en
los nombres de las ramas. Una funcion de Peru no se promociona a comportamiento
comun por tener un nombre parecido. Una tabla usada por ambas ramas no demuestra
que compartan el mismo DDL, poblacion, constraints o reglas de despliegue.

## Limites

No se recibio el esquema SQL de master ni un entorno de despliegue verificable.
Los dos submodulos externos se inventariaron, pero no se descargaron ni auditaron.
No se comprobaron servicios externos, autorizacion por tenant ni todos los
flujos con datos reales. Los significados reconstruidos conservan su evidencia,
confianza e inferencias; la aprobacion de responsables de negocio queda pendiente.

La auditoria actualiza el conocimiento y registra riesgos. No modifica ni corrige
el codigo de la aplicacion. El baseline Brownfield sigue no canonico e
INCOMPLETE_BASELINE; el estado agregado del conocimiento sigue PARTIAL.
