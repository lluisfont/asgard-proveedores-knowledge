# Auditoria iterativa de APIs con Asgard - Graphify v0.9.61

Fecha: 2026-09-15  
Repositorio auditado: `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61`  
Auditor instalado: `asgard-api-auditor 0.8.0` desde `C:\repos\proveedores\asgard-api-auditor`  
Commit fuente reportado por Asgard: `fe66389083369c3159aa391117185c8f58b4d07c`  
Estado del arbol auditado: dirty antes y despues de esta auditoria, con cambios previos no tocados por esta pasada.

## Criterio aplicado

Se ejecuto un bucle de mejora iterativa. Cada version tenia que aportar hallazgos o precision que no estuviera en la anterior. Se detuvo cuando dos pasadas consecutivas de cierre no anadieron hallazgos nuevos y solo confirmaron el mismo estado: Asgard no dispone de detector para la API real de Graphify.

## Resumen ejecutivo

Asgard quedo instalado y ejecutado correctamente, pero su salida oficial para el codigo de producto queda en estado `partial` y con OpenAPI vacio. Esto no significa que Graphify no tenga API: significa que Asgard 0.8.0 no selecciona ningun detector compatible para la superficie real de Graphify, que es un servidor MCP sobre Streamable HTTP montado en Starlette como ASGI crudo.

La API expuesta real esta en `graphify\serve.py`: `serve_http()` construye un `Starlette` app con un unico mount configurable, por defecto `/mcp`, y lo sirve con `uvicorn`. La autenticacion HTTP es opcional y se activa con `--api-key` o `GRAPHIFY_API_KEY`; acepta `Authorization: Bearer <key>` o `X-API-Key`. El contrato no es REST clasico: es JSON-RPC/MCP sobre Streamable HTTP.

Las APIs consumidas tampoco quedan cubiertas por Asgard: Graphify usa `urllib` encapsulado en `safe_fetch`/`safe_fetch_text`, `yt-dlp`, `gh`, `gws`, drivers de Neo4j/FalkorDB y DSN PostgreSQL, todos fuera del conjunto de detectores efectivos usados en esta ejecucion.

## Versiones de la auditoria

### V1 - Asgard sobre repo completo

Artefactos:

- `C:\repos\proveedores\graphify-asgard-audit\api-v1-inventory.json`
- `C:\repos\proveedores\graphify-asgard-audit\api-v1-discovery.json`
- `C:\repos\proveedores\graphify-asgard-audit\api-v1-audit`

Resultado: `partial`, 0 endpoints, 0 integraciones probadas.

Hallazgo nuevo:

- La pasada completa queda contaminada por `tests/fixtures` y codigo de test. Asgard detecta frameworks/clientes como `aspnet-core`, `django`, `nestjs`, `angular-httpclient`, `dotnet-httpclient`, `fetch` y `sse`, pero la evidencia pertenece a fixtures/tests, no al producto. Esta pasada no sirve como inventario API de producto sin exclusiones.

### V2 - Asgard limitado a codigo de producto

Artefactos:

- `C:\repos\proveedores\graphify-asgard-audit\api-v2-product-inventory.json`
- `C:\repos\proveedores\graphify-asgard-audit\api-v2-product-discovery.json`
- `C:\repos\proveedores\graphify-asgard-audit\api-v2-product-audit`
- `C:\repos\proveedores\graphify-asgard-audit\api-v2-product-audit\api-catalog.json`

Exclusiones principales: `tests`, `worked`, `graphify-out`, `.brownfield`, `dist_audit*`, artefactos de auditorias previas.

Resultado: `partial`, 496 ficheros escaneados, lenguaje `python`, 0 endpoints, 0 integraciones, sin detectores seleccionados.

Hallazgo nuevo:

- Asgard informa `no_supported_api_detector_selected`. La propia salida dice que la ausencia de hallazgos no prueba ausencia de integraciones. En Graphify esto es un falso negativo practico, porque la API MCP HTTP existe pero no encaja en los detectores de Asgard 0.8.0.

### V3 - Inspeccion de contrato expuesto real

Evidencia principal:

- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2350` define `_MCPASGIApp`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2366` define `_ApiKeyMiddleware`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2407` define `_build_http_app`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2483` monta `Route(path, endpoint=_MCPASGIApp(manager))`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2489` define `serve_http`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\README.md:491` documenta clientes apuntando a `http://<host>:8080/mcp`.

Hallazgos nuevos:

- API expuesta real: MCP Streamable HTTP en path configurable, por defecto `/mcp`.
- Transporte alternativo: stdio por defecto; HTTP solo si se usa `--transport http`.
- Metodo/forma: no es REST/OpenAPI convencional; las operaciones relevantes viajan como JSON-RPC MCP (`initialize`, `tools/list`, `tools/call`, notificaciones y manejo de sesion).
- Seguridad: si `api_key` esta configurada, faltante o incorrecta devuelve 401; si se pasa clave vacia, se normaliza a "sin auth".
- Riesgo operativo documentado por el propio codigo: al bindear `0.0.0.0`, `::` o host vacio sin clave, el servidor queda expuesto sin autenticacion y solo emite warning.

Herramientas MCP expuestas:

- `query_graph` en `serve.py:1805`
- `get_node` en `serve.py:1825`
- `get_neighbors` en `serve.py:1834`
- `get_community` en `serve.py:1847`
- `god_nodes` en `serve.py:1859`
- `graph_stats` en `serve.py:1868`
- `shortest_path` en `serve.py:1873`
- `list_prs` en `serve.py:1891`
- `get_pr_impact` en `serve.py:1906`
- `triage_prs` en `serve.py:1922`

### V4 - Smoke test dinamico del ASGI

Artefacto: `C:\repos\proveedores\graphify-asgard-audit\asgi-smoke-results.json`

Resultado observado:

- `missing_key`: 401
- `bad_key`: 401
- `good_key`: 200
- `session_header_present`: true
- `tools_list_status`: 200
- `unknown_path`: 404
- `get_mcp_no_session`: 400
- `delete_mcp_no_session`: 400

Hallazgo nuevo:

- El endpoint `/mcp` no es teorico ni solo documentacion. Se inicializa correctamente, crea sesion, lista herramientas MCP y aplica autenticacion. GET/DELETE alcanzan el gestor MCP y devuelven 400 sin sesion valida, lo que confirma que el mount maneja varios metodos aunque el contrato funcional sea MCP.

### V5 - APIs consumidas e integraciones salientes

Evidencia:

- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\security.py:103` define `validate_url`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\security.py:258` define `safe_fetch`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\security.py:302` define `safe_fetch_text`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\ingest.py:108` llama a `https://publish.twitter.com/oembed`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\ingest.py:171` llama a `https://export.arxiv.org/abs/{id}`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\transcribe.py:50` define `download_audio`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\transcribe.py:83` ejecuta descarga via `yt_dlp.YoutubeDL`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\prs.py:141` encapsula llamadas a GitHub mediante CLI `gh`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\google_workspace.py:110` usa subprocess para `gws`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\exporters\graphdb.py:40` conecta a Neo4j con `GraphDatabase.driver`.
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\exporters\graphdb.py:134` conecta a FalkorDB.

Hallazgos nuevos:

- Graphify consume URLs arbitrarias suministradas por usuario a traves de `safe_fetch`/`safe_fetch_text`; existe defensa SSRF centralizada con validacion de esquema, DNS/IP y redirects.
- Existen integraciones HTTP concretas con Twitter/X oEmbed y arXiv.
- La descarga de video/audio delega en `yt-dlp` despues de `validate_url`, por lo que hay una integracion de red indirecta no visible para Asgard.
- Las herramientas MCP `list_prs`, `get_pr_impact` y `triage_prs` consumen GitHub a traves de `gh`, no por una libreria HTTP detectable por Asgard.
- Google Workspace se consume mediante `gws`, tambien por CLI externa.
- Neo4j, FalkorDB y PostgreSQL son integraciones de red/base de datos fuera de OpenAPI y fuera de la salida de Asgard.

### V6 - Revision del alcance de Asgard

Evidencia:

- `C:\repos\proveedores\asgard-api-auditor\src\asgard_api_auditor\inventory_catalog.py` cataloga frameworks Python `fastapi`, `flask`, `django`.
- El mismo catalogo cataloga clientes Python `requests`, `httpx`, `aiohttp`.
- No aparecen `starlette`, `mcp`, `urllib`, `yt-dlp`, `neo4j`, `falkordb`, `psycopg`, `gh` ni `gws` como detectores API equivalentes.

Hallazgo nuevo:

- La limitacion no esta solo en la ejecucion sobre Graphify; esta en la matriz de cobertura efectiva del auditor instalado. Para este repositorio, Asgard aporta valor como evidencia negativa controlada: avisa que no puede seleccionar detector, pero no sustituye una auditoria manual/semantica de API.

### V7 - Cierre 1: correlacion estricta

Artefacto: `C:\repos\proveedores\graphify-asgard-audit\api-v4-closure-require-correlation`

Resultado: `partial`, 0 endpoints, mismo bloqueo `no_supported_api_detector_selected`.

Nuevos hallazgos: ninguno.

### V8 - Cierre 2: tests HTTP del contrato MCP

Comando ejecutado:

`python -m pytest C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\tests\test_serve_http.py -q`

Resultado: `30 passed, 1 warning`.

Nuevos hallazgos: ninguno. Esta pasada confirma que el contrato HTTP observado en V3/V4 esta cubierto por tests y que no aparecio una superficie adicional nueva.

## Inventario API consolidado

### Expuesta

| Tipo | Ruta / interfaz | Estado | Evidencia |
| --- | --- | --- | --- |
| MCP Streamable HTTP | `/mcp` por defecto, configurable con `--path` | Real, probado dinamicamente | `serve.py:2407`, `serve.py:2483`, `serve.py:2489`, `asgi-smoke-results.json` |
| MCP stdio | `python -m graphify.serve graphify-out/graph.json` | Real, no HTTP | `serve.py:2331`, README `:475-480` |
| Herramientas MCP | 10 herramientas listadas arriba | Real, probado con `tools/list` | `serve.py:1805-1922`, `asgi-smoke-results.json` |

### Consumida / saliente

| Tipo | Destino | Mecanismo | Evidencia |
| --- | --- | --- | --- |
| Web fetch generico | URLs usuario `http/https` | `safe_fetch`, `safe_fetch_text` | `security.py:258`, `security.py:302` |
| Twitter/X oEmbed | `https://publish.twitter.com/oembed` | `safe_fetch_text` | `ingest.py:108` |
| arXiv | `https://export.arxiv.org/abs/{id}` | `safe_fetch_text` | `ingest.py:171` |
| Video/audio remoto | URL soportada por `yt-dlp` | `yt_dlp.YoutubeDL` | `transcribe.py:50`, `transcribe.py:83` |
| GitHub PRs | GitHub API via CLI | `gh` subprocess | `prs.py:141-144` |
| Google Workspace | Drive/Docs/Sheets/Slides via CLI | `gws` subprocess | `google_workspace.py:110` |
| Neo4j | Bolt URI | Python driver | `graphdb.py:40` |
| FalkorDB | Redis/Falkor URI | FalkorDB SDK | `graphdb.py:134` |
| PostgreSQL | DSN | `psycopg` extra | `pyproject.toml:75` |

## Riesgos y recomendaciones API

1. No usar el OpenAPI vacio generado por Asgard como prueba de ausencia de API. Para Graphify es una salida parcial por falta de detector.
2. Si se expone HTTP fuera de localhost, exigir `--api-key`/`GRAPHIFY_API_KEY` y documentarlo como requisito operativo, no solo warning.
3. Mantener la cobertura SSRF centralizada en `safe_fetch` y asegurar que nuevas integraciones URL pasen por `validate_url`.
4. Considerar un detector Asgard especifico para `Starlette` + MCP Streamable HTTP: deteccion de `_build_http_app`, `StreamableHTTPSessionManager`, `Route(path, endpoint=...)` y listado de `types.Tool`.
5. Considerar detectores de consumidores indirectos para Python: `urllib` wrappers, `yt-dlp`, `gh`, `gws`, drivers de graph DB y DSN PostgreSQL.
6. Mantener los tests de `tests\test_serve_http.py` como contrato vivo del API MCP; ahora mismo son la mejor fuente ejecutable del comportamiento HTTP.

## Estado final del bucle

Las versiones V1-V6 agregaron informacion nueva o corrigieron falsos positivos/falsos negativos. V7 y V8 no agregaron hallazgos nuevos: ambas confirmaron el mismo mapa de API y el mismo limite de Asgard. Por tanto, el bucle se detiene conforme al criterio solicitado.
