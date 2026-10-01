# Auditoria iterativa de APIs con Asgard - Pass 2

Fecha: 2026-09-15  
Repositorio auditado: `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61`  
Informe base comparado: `C:\repos\proveedores\graphify-asgard-audit\ASGARD_API_ITERATIVE_AUDIT_2026-09-15.md`  
Auditor instalado: `asgard-api-auditor 0.8.0` desde `C:\repos\proveedores\asgard-api-auditor`

## Criterio de esta pasada

Esta pasada continuo el bucle anterior pero cambio tecnicas:

- consultas Graphify BFS/DFS centradas en API, callbacks y recursos;
- extractor AST propio sobre Python, primero con scope contaminado y luego depurado;
- pruebas dinamicas MCP para `resources/list`, `resources/read` y query logging;
- auditoria de proveedores LLM y endpoints configurables;
- tests selectivos de contrato HTTP, proveedores, query logging y backends;
- cierre con Asgard product-only y busqueda de superficies no REST.

El bucle se detuvo cuando las dos pasadas finales no anadieron hallazgos nuevos: Asgard siguio reportando el mismo bloqueo de detector y los tests solo confirmaron el contrato ya inventariado.

## Nuevos hallazgos frente al informe anterior

### 1. La API MCP no solo expone herramientas: tambien expone recursos

El informe anterior enumero las 10 herramientas MCP. Esta pasada encontro y probo 6 recursos MCP adicionales:

- `graphify://report`
- `graphify://stats`
- `graphify://god-nodes`
- `graphify://surprises`
- `graphify://audit`
- `graphify://questions`

Evidencia:

- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2199`
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2203`
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\graphify\serve.py:2211`
- `C:\repos\proveedores\graphify-asgard-audit\resource-smoke-results.json`

Prueba dinamica:

- `resources/list` devolvio las 6 URIs.
- `resources/read` sobre `graphify://audit` devolvio el resumen de confianza del grafo.

Impacto:

- El contrato API real es mayor que el listado de herramientas. Cualquier catalogo API de Graphify debe modelar herramientas MCP y recursos MCP.
- Asgard/OpenAPI no representan esta parte del contrato.

### 2. Existe un selector multi-proyecto por `project_path` en todas las herramientas

El AST y los tests confirman que cada tool acepta un `project_path` opcional. Si se envia, el servidor carga `<project_path>/<GRAPHIFY_OUT>/graph.json` y ejecuta la herramienta sobre ese grafo.

Evidencia:

- `serve.py:1769` resuelve `project_path`.
- `serve.py:1792` cambia el grafo activo por request.
- `serve.py:1937` inyecta `project_path` en todos los esquemas de herramientas.
- `serve.py:2264` extrae `project_path` de los argumentos del tool call.
- `tests\test_serve_http.py:203`, `:217`, `:280`, `:292`.

Validacion:

- `test_project_context_cache_is_lru_and_pins_default_graph`
- `test_bad_project_path_errors_without_killing_server`
- `test_corrupt_project_graph_is_a_tool_error_without_killing_server`

Impacto:

- En un servidor compartido, cualquier cliente con acceso al MCP puede pedir consultas sobre otros grafos accesibles por el proceso si conoce o adivina el path.
- No aparece un allowlist de proyectos en el contrato actual; el control principal es la autenticacion general del servidor y los permisos del proceso.
- Esto no es necesariamente un bug, pero si es un requisito operativo/documental: `project_path` debe tratarse como capacidad sensible.

### 3. La cache de contexto MCP es LRU y configurable

El servidor mantiene un grafo por defecto pinneado y una cache LRU de grafos de proyecto.

Evidencia:

- `serve.py:104` define `_max_server_contexts`.
- `serve.py:121` define `_GraphContextCache`.
- `serve.py:1757` crea `_GraphContextCache(_max_server_contexts())`.
- `README.md:557` documenta `GRAPHIFY_MAX_CONTEXTS`.

Validacion:

- `tests\test_serve_http.py:234`
- `tests\test_serve_http.py:242`

Impacto:

- `GRAPHIFY_MAX_CONTEXTS` forma parte del contrato operativo del API MCP, porque afecta memoria, aislamiento entre proyectos y comportamiento bajo uso concurrente.
- Asgard no lo detecta porque no es una ruta HTTP literal ni un cliente HTTP convencional.

### 4. `build/lib` duplica el paquete y puede contaminar auditorias estaticas

La primera variante AST encontro 20 herramientas y 12 recursos. Al revisar el detalle, la mitad venia de `build/lib/graphify/serve.py`, una copia byte-a-byte de `graphify/serve.py`.

Evidencia:

- `C:\repos\proveedores\graphify-asgard-audit\api-v9-ast-inventory.json`
- `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61\build\lib\graphify\serve.py` existe.
- Hash SHA256 de `graphify/serve.py` y `build/lib/graphify/serve.py`: `5182792A2C0F227665CBFCA42F6DCD152B349832238B003E43DDDD589F62A926`.

Impacto:

- Ademas de `tests` y `worked`, el directorio `build` debe excluirse de auditorias API para evitar duplicados exactos.
- Asgard ya excluye `build` en su catalogo por defecto; el hallazgo importa para herramientas complementarias que no hereden esas exclusiones.

### 5. Hay un endpoint/canal de recursos MCP que siempre lee el grafo por defecto

Las herramientas aceptan `project_path`, pero `read_resource()` llama `_select_graph(None)`, por lo que los recursos leen el grafo por defecto del servidor.

Evidencia:

- `serve.py:2211` define `read_resource`.
- `serve.py:2212` fuerza `_select_graph(None)`.
- `serve.py:2307` registra `_on_read_resource`.

Impacto:

- El contrato no es simetrico: tools pueden operar sobre proyectos alternativos, resources no.
- Esto puede sorprender a clientes MCP que esperan que recursos y herramientas compartan el mismo contexto de proyecto.
- No es necesariamente fallo de seguridad, pero si un matiz contractual que faltaba en la version anterior.

### 6. Graphify tiene una matriz de APIs LLM salientes mas amplia que la inventariada inicialmente

El informe anterior menciono APIs salientes de forma general. Esta pasada preciso los backends y endpoints por defecto:

- Anthropic: `https://api.anthropic.com`
- Kimi/Moonshot: `https://api.moonshot.ai/v1`
- Ollama/OpenAI-compatible local: `http://localhost:11434/v1`
- Gemini OpenAI-compatible: `https://generativelanguage.googleapis.com/v1beta/openai/`
- OpenAI/OpenAI-compatible: `https://api.openai.com/v1`
- DeepSeek: `https://api.deepseek.com`
- Azure OpenAI: endpoint obligatorio via `AZURE_OPENAI_ENDPOINT`
- Bedrock: `bedrock-runtime` via `boto3`
- Claude CLI: subprocess `claude`

Evidencia:

- `llm.py:103-203` define `BACKENDS`.
- `llm.py:1353` define `_call_openai_compat`.
- `llm.py:1495` define `_call_claude`.
- `llm.py:1821` define `_azure_client`.
- `llm.py:1878` define `_call_bedrock`.
- `llm.py:2870` define `_call_llm`.
- `C:\repos\proveedores\graphify-asgard-audit\api-v11-ast-inventory-product.json`

Validacion:

- Tests LLM seleccionados: `10 passed`.

Impacto:

- El mapa API de Graphify debe separar APIs de producto MCP de APIs de extraccion/LLM.
- Muchas rutas salen por SDKs OpenAI-compatible o proveedores cloud, no por `requests/httpx/aiohttp`; Asgard no las modela.

### 7. Los endpoints LLM son configurables y los custom providers son una superficie sensible

Graphify carga proveedores custom desde `~/.graphify/providers.json`. Los providers locales de proyecto `./.graphify/providers.json` se ignoran salvo opt-in con `GRAPHIFY_ALLOW_LOCAL_PROVIDERS=1`.

Evidencia:

- `llm.py:227` selecciona `~/.graphify/providers.json`.
- `llm.py:228` define el path local `./.graphify/providers.json`.
- `llm.py:231` define `provider_base_url_ok`.
- `llm.py:269-279` bloquea providers locales salvo opt-in.
- `tests\test_provider_registry.py:72`, `:94`, `:112`, `:128`, `:141`.

Validacion:

- `tests\test_provider_registry.py`: incluido en tanda de `31 passed` y luego en `68 passed`.

Impacto:

- `base_url` de provider controla donde se envia corpus + API key; el propio codigo lo describe como canal de exfiltracion.
- Los esquemas no HTTP se rechazan.
- HTTP plaintext hacia host no-loopback se permite con warning, no se bloquea; esto debe figurar en la auditoria de uso seguro.

### 8. Query logging MCP puede registrar respuestas completas del grafo

`query_graph` llama a `querylog.log_query`. Por defecto el logging esta apagado, pero si se activa puede escribir preguntas, path del corpus y, con `GRAPHIFY_QUERY_LOG_RESPONSES=1`, respuestas completas.

Evidencia:

- `serve.py:1957` define `_tool_query_graph`.
- `serve.py:1975` llama `querylog.log_query`.
- `querylog.py:15` resuelve el path del log.
- `querylog.py:35` habilita respuestas completas.
- `querylog.py:43` escribe JSONL.
- `README.md:552-555`, `README.md:569`.
- `C:\repos\proveedores\graphify-asgard-audit\mcp-querylog-smoke.jsonl`

Prueba dinamica:

- Con `GRAPHIFY_QUERY_LOG` y `GRAPHIFY_QUERY_LOG_RESPONSES=1`, un `tools/call` a `query_graph` escribio una linea JSONL que incluye `question`, `corpus`, `nodes_returned`, `result_chars`, parametros de traversal y `response`.

Impacto:

- En entornos compartidos, el log puede contener informacion sensible del grafo y de las preguntas del usuario.
- La mitigacion principal es que el logging esta opt-in y `GRAPHIFY_QUERY_LOG_DISABLE=1` fuerza apagado.

### 9. Google Workspace no envia `resourceKey` como query param al CLI

El informe anterior solo identifico `gws` como integracion saliente. Esta pasada encontro una decision de contrato concreta: `resource_key` se lee del shortcut, pero no se pasa como query param porque el CLI `gws export` no tiene flag de header personalizado.

Evidencia:

- `google_workspace.py:95` resuelve `gws`.
- `google_workspace.py:104-107` documenta que no se pasa `resourceKey`.
- `google_workspace.py:110` ejecuta `gws drive files export`.
- `tests\test_google_workspace.py:102` cubre que no se envia `resource_key` como query param.

Impacto:

- Algunos documentos de Drive protegidos por resource key pueden no exportarse aunque el shortcut tenga el dato.
- Es una limitacion funcional/contractual del canal API indirecto.

### 10. PostgreSQL se introspecta en transaccion read-only serializable

El informe anterior marco PostgreSQL como integracion. Esta pasada preciso el contrato:

- `psycopg.connect(dsn or "")`, por tanto puede usar DSN explicito o variables `PG*`.
- Ejecuta `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE`.
- Lee `information_schema` y `pg_catalog`.
- Sanitiza errores para no exponer DSN/credenciales completas.

Evidencia:

- `pg_introspect.py:11` define `introspect_postgres`.
- `pg_introspect.py:14` importa `psycopg`.
- `pg_introspect.py:20-25` conecta y sanea errores.
- `pg_introspect.py:28` configura transaccion read-only.

Impacto:

- PostgreSQL es una API/base de datos saliente con contrato de permisos read-only.
- La auditoria API debe tratarla separadamente de HTTP/OpenAPI.

### 11. No se encontraron GraphQL/gRPC/WebSocket/SOAP/Webhook reales en producto

La busqueda especifica en `graphify`, `README.md` y `pyproject.toml` no encontro superficies reales de GraphQL, gRPC, WebSocket, SOAP o webhooks. Lo unico relacionado fue SSE, que pertenece al transporte MCP Streamable HTTP.

Impacto:

- La matriz de APIs no REST queda acotada: MCP Streamable HTTP/SSE, recursos MCP, CLI/API indirectas, LLM SDKs y bases de datos.

## Artefactos nuevos

- `C:\repos\proveedores\graphify-asgard-audit\tools\api_ast_inventory.py`
- `C:\repos\proveedores\graphify-asgard-audit\api-v9-ast-inventory.json`
- `C:\repos\proveedores\graphify-asgard-audit\api-v10-ast-inventory-clean.json`
- `C:\repos\proveedores\graphify-asgard-audit\api-v11-ast-inventory-product.json`
- `C:\repos\proveedores\graphify-asgard-audit\resource-smoke-results.json`
- `C:\repos\proveedores\graphify-asgard-audit\mcp-querylog-smoke.jsonl`
- `C:\repos\proveedores\graphify-asgard-audit\api-v12-final-product-inventory.json`
- `C:\repos\proveedores\graphify-asgard-audit\api-v13-final-product-discovery.json`

## Validacion ejecutada

- `tests\test_provider_registry.py`, `tests\test_querylog.py` y tests HTTP multi-proyecto: `31 passed`.
- Tests LLM/backend seleccionados: `10 passed`.
- Tanda final combinada de HTTP, providers, querylog y LLM: `68 passed`.
- Smoke MCP resources: `resources/list` y `resources/read` correctos.
- Smoke MCP querylog: escritura JSONL confirmada con respuestas completas cuando se activa.

## Estado de estabilizacion

Versiones con hallazgos nuevos:

- V9: AST amplio encontro duplicacion `build/lib`.
- V10/V11: AST depurado encontro recursos MCP, callbacks, scripts y conteo de superficies producto.
- V12: recursos MCP probados dinamicamente.
- V13: proveedor LLM/custom endpoints y controles de `base_url`.
- V14: multi-proyecto `project_path` y cache LRU.
- V15: query logging MCP con respuestas completas.
- V16: Google Workspace y PostgreSQL precisados como contratos salientes.

Pasadas sin hallazgos nuevos:

- V17: busqueda no REST clasica solo confirmo SSE/MCP ya conocido.
- V18: Asgard product-only final repitio `no_supported_api_detector_selected`.
- V19: tanda final de tests confirmo comportamiento, sin nuevas superficies.

Conclusiones nuevas mas importantes:

1. El contrato MCP incluye herramientas y recursos.
2. `project_path` amplia el alcance del servidor compartido y debe tratarse como capacidad sensible.
3. Query logging puede registrar respuestas completas si se habilita.
4. Los providers LLM configurables son una superficie saliente critica.
5. `build/lib` debe excluirse para no duplicar falsamente el inventario API.
