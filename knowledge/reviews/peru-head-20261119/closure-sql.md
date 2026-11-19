# Cierre acotado por AST MySQL y metamorfismos benignos

19 de noviembre de 2026 · Europe/Madrid · fecha del usuario · no canónico.

SQLglot **30.33.0**, dialecto MySQL, instalación aislada `C:\repos\audit-tools-proveedores-sqlglot-20261118`. **25/25 checks completed/pass**: cuatro hallazgos aceptados y cinco mejoras de reportes revalidados. No hay novedades materiales adicionales: `new_findings=[]`, `improvements=[]`. No se reclama cierre global.

Pins: HEAD `2a179e2e6472d5705d031665ecbc90c3d806edec`, P95 `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`, M histórico `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, KB `0c4bb99f076d6a8c18ae98375d6e154da6319922`. La única comparación de SQL es HEAD/P95; M no se audita de nuevo.

Técnica diferente de los 36 probes de fase1: extracción del constructor sin ejecutar PHP; parsing MySQL, 11 CTE, 29 ámbitos; resolución de aliases, claves ON, conjunciones WHERE, GROUP BY y linaje de MAX; evaluación parcial de nodos AST sobre dominios sintéticos. Se prueban inserción de filtros benignos, dominios de identidad, mutación de claves, permutación/duplicación/dominación de filas y filtrado antes/después del pivote. No se construye ningún payload adversarial ni consulta de ataque.

La consulta benigna conserva el scope como conjunción obligatoria. Eso no demuestra que el constructor PHP parametrice sus fragmentos: el testigo AND/OR usa únicamente símbolos abstractos, sin entradas adversariales. Las uniones por VIN no añaden pertenencia; el control con claves compuestas sí distingue dominios. Los MAX de varias columnas preservan sus máximos, pero pueden perder una fila origen coherente; cambiar una clave GROUP BY separa esos grupos.

## Cobertura de lo aceptado

| Registro | Origen fase1 | Checks | Resultado |
| --- | --- | --- | --- |
| PH-001 | TEMP-PH002 | CS-02, CS-07, CS-08 | completed/pass |
| PH-002 | TEMP-PH003 | CS-04, CS-05, CS-06 | completed/pass |
| PH-003 | TEMP-PH004 | CS-09, CS-10, CS-11, CS-12, CS-24 | completed/pass |
| PH-004 | TEMP-PH005 | CS-13, CS-14, CS-15, CS-24 | completed/pass |
| PH-IMP001 | TEMP-PH001 | CS-02, CS-03, CS-04, CS-22, CS-25 | completed/pass |
| PH-IMP002 | TEMP-PH006 | CS-04, CS-16, CS-17, CS-18, CS-19 | completed/pass |
| PH-IMP003 | TEMP-PH007 | CS-11, CS-19, CS-20, CS-21 | completed/pass |
| PH-IMP004 | TEMP-PH008 | CS-22, CS-23 | completed/pass |
| PH-IMP005 | TEMP-PH010 | CS-01, CS-23, CS-24 | completed/pass |

## Checks y controles negativos

### CS-01 — Consulta única y resolución local de aliases

Estado: completed/pass. Registros: PH-IMP005.

Control negativo/límite de inferencia: No se infiere que la existencia del alias pruebe columnas físicas o que query.php ejecute SQL.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L52-L432`.

### CS-02 — Predicado HEAD y predicado P95 pertenecen a dominios distintos

Estado: completed/pass. Registros: PH-001, PH-IMP001.

Control negativo/límite de inferencia: El predicado de concesionario no aparece como obligación adicional en HEAD.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L391`; `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L390`.

### CS-03 — Igualdad AST fuera del cambio de WHERE

Estado: completed/pass. Registros: PH-IMP001.

Control negativo/límite de inferencia: No extiende igualdad a runtime, datos ni al tercer JS cambiado.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L52-L432`; `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/reportes/reportepreembarquenacionalquery.php:L52-L431`.

### CS-04 — Filtros benignos conservan la conjunción obligatoria de proveedor

Estado: completed/pass. Registros: PH-002, PH-IMP001, PH-IMP002.

Control negativo/límite de inferencia: No se genera ninguna entrada adversarial: la prueba no afirma que entradas arbitrarias mantengan esta propiedad.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L391`.

### CS-05 — El operador raíz determina si un scope sigue siendo obligatorio

Estado: completed/pass. Registros: PH-002.

Control negativo/límite de inferencia: Control abstracto AND frente a OR; no consulta de ataque, concatenación maliciosa ni replay de RP-09.

Límite: No acredita que un servidor acepte un texto de ataque; el riesgo de composición conserva la evidencia de PHP de fase1.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L45-L50`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L391`.

### CS-06 — La variante de fecha benigna no prueba parametrización del constructor

Estado: completed/pass. Registros: PH-002.

Control negativo/límite de inferencia: SQLglot recibe la instanciación segura, no ejecuta PHP ni demuestra validación de entradas no instanciadas.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L45-L50`.

### CS-07 — Igualdad numérica no equivale a identidad con dominio

Estado: completed/pass. Registros: PH-001.

Control negativo/límite de inferencia: Al igualar dominios desaparece la discrepancia. No se presume acceso efectivo de tipo7 ni una política de admisión aprobada.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/veriflogin.php:L85-L91`; `2a179e2e6472d5705d031665ecbc90c3d806edec:src/core/users/application/Find/UserFind.php:L19-L35`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L382`.

### CS-08 — El WHERE no incorpora discriminador de rol

Estado: completed/pass. Registros: PH-001.

Control negativo/límite de inferencia: La presencia de ambos IDs en PHP no transforma el ID genérico en un ID tipado en SQL.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue. La admisión PHP/ruta no se prueba con AST SQL.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L391`.

### CS-09 — Las tres uniones débiles tienen solo clave chasis

Estado: completed/pass. Registros: PH-003.

Control negativo/límite de inferencia: m, mtres e ip no se incluyen en esta generalización.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L370-L377`.

### CS-10 — Mutar pertenencia no afecta una unión que solo mira chasis

Estado: completed/pass. Registros: PH-003.

Control negativo/límite de inferencia: Cambiar VIN elimina el match; una clave compuesta abstracta también lo elimina. No se propone una columna física inexistente como reparación.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L370-L382`.

### CS-11 — El control correlacionado rechaza otro preembarque o tipo

Estado: completed/pass. Registros: PH-003, PH-IMP003.

Control negativo/límite de inferencia: Evita afirmar que todas las CTE cruzan por VIN sin más claves.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L354-L362`.

### CS-12 — El MAX de pedidos opera con agrupación global de chasis

Estado: completed/pass. Registros: PH-003.

Control negativo/límite de inferencia: No se deriva aislamiento por proveedor de un GROUP BY sin tal clave; constraints reales desconocidos.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L210-L220`.

### CS-13 — Agregar una fila incomparable puede producir una tupla sin fila origen

Estado: completed/pass. Registros: PH-004.

Control negativo/límite de inferencia: Una sola fila mantiene coherencia. No se usa MAX textual de app_tracking ni se presupone collation.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L393-L428`.

### CS-14 — Permutación, duplicación y dominación no reparan la agregación

Estado: completed/pass. Registros: PH-004.

Control negativo/límite de inferencia: El último control selecciona una fila completa como ejemplo abstracto de coherencia, no como política aprobada de cuál fila usar.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L393-L413`.

### CS-15 — Cambiar una clave GROUP BY separa las poblaciones

Estado: completed/pass. Registros: PH-004.

Control negativo/límite de inferencia: La mezcla requiere al menos dos relaciones dentro del mismo grupo; no se afirma para grupos distintos.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L416-L428`.

### CS-16 — Dominio de CROSS JOIN solo1/2 frente al estado3 derivado

Estado: completed/pass. Registros: PH-IMP002.

Control negativo/límite de inferencia: El filtro3 tiene dominio vacío; no selecciona inventario_3_concesionario.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L53-L57`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L337-L337`.

### CS-17 — Filtrar antes de pivotar no equivale a seleccionar vehículo después

Estado: completed/pass. Registros: PH-IMP002.

Control negativo/límite de inferencia: Sin filtro ambas rutas coinciden; no se declara cuál política debe adoptar negocio.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L38-L43`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L386-L387`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L411-L413`.

### CS-18 — Pivote vacío y tipo único conservan NULL de SQL MAX

Estado: completed/pass. Registros: PH-IMP002.

Control negativo/límite de inferencia: No se transforma NULL en Pendiente ni se atribuye comportamiento al navegador.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L411-L412`.

### CS-19 — Los dominios local2 y preembarque3 permanecen separados

Estado: completed/pass. Registros: PH-IMP002, PH-IMP003.

Control negativo/límite de inferencia: Los números de dos campos distintos no se convierten en un único catálogo.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L158-L207`.

### CS-20 — CASE de estado3 es disyunción de presencia, no completitud

Estado: completed/pass. Registros: PH-IMP003.

Control negativo/límite de inferencia: Solo el caso sin ambos registros queda Pendiente; no se valida la inspección física ni todas sus secciones.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L299-L305`.

### CS-21 — Existencia UNION de cuatro fuentes y flags sin consumo exterior

Estado: completed/pass. Registros: PH-IMP003.

Control negativo/límite de inferencia: No se interpreta presencia de una fuente como defecto de completitud; tampoco se audita presentación de resultados.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L115-L156`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L288-L308`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L393-L413`.

### CS-22 — Los SELECT auxiliares no comparten el mismo scope de proveedor

Estado: completed/pass. Registros: PH-IMP001, PH-IMP004.

Control negativo/límite de inferencia: Consulta global no equivale a divulgación: no se inspecciona su salida al navegador.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L52-L76`.

### CS-23 — Dependencia constructor→data no equivale a ejecución del constructor

Estado: completed/pass. Registros: PH-IMP004, PH-IMP005.

Control negativo/límite de inferencia: Un AST SQL válido no demuestra éxito de PHP/mysql_query ni captura fallos de include/conexión. No se ejecuta data.php.

Límite: Lectura estática del puente PHP; los controles de fallo de fase1 se conservan, sin emulación de despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacional.php:L85-L87`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L52-L52`; `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/data.php:L6-L14`.

### CS-24 — Round-trip AST sin cambiar cláusulas ni claves

Estado: completed/pass. Registros: PH-003, PH-004, PH-IMP005.

Control negativo/límite de inferencia: SQL emitido solo se vuelve a parsear en memoria; no se guarda ni se envía a un motor.

Límite: AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L52-L432`.

### CS-25 — NULL no satisface igualdad de scope

Estado: completed/pass. Registros: PH-IMP001.

Control negativo/límite de inferencia: WHERE admite solo True; Unknown no se convierte en True por coerción Python.

Límite: Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.

Evidencia: `2a179e2e6472d5705d031665ecbc90c3d806edec:index_archivos/reportes/reportepreembarquenacionalquery.php:L381-L382`.

## Limitaciones

- AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue.
- Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales.
- La extracción sustituye el ID por placeholder y nueve fragmentos por constantes benignas; no interpreta PHP ni prueba toda entrada dinámica.
- No se vuelve a probar explotación de fechas; solo su frontera de composición y la diferencia entre AST instanciado y constructor de PHP.
- Sin DDL autorizado: resolución de aliases no demuestra columnas físicas, unicidad, tipos efectivos, FK ni aislamiento entre tenants.
- La obligación de rol de PH-001 mantiene acceso efectivo y dominios reales como precondiciones; no se decide política de tipo7.
- No se valida SQL_MODE, versión del servidor, collation, plan de ejecución, privilegios, PHP/extensiones, includes ni despliegue.
- No revisión de navegación/salidas al navegador, exportador, master a44, código JS ni CF/PH-IMP006..008 en esta fase acotada.
- Checks completed significa pruebas aisladas terminadas, no cierre global, aprobación de TOBE ni certificación productiva.

Solo se escriben los sidecars de cierre. Fase1, registro aceptado, documentos finales y manifest permanecen fuera de la escritura de este script. CF/PH-IMP006..008 quedan en la integración del padre; no se usa una comprobación local para afirmar composición o vigencia de M-only en Perú.

[Evidencia y resultados](../../../source-audits/peru/2026-11-19/closure-sql.json) · [Registro JSON](closure-sql.json) · [Script](../../../scripts/audit/peru_head_closure_sql.py).

Reproducción: `python -B scripts/audit/peru_head_closure_sql.py --source C:/repos/proveedores-peru-head-review-20261119 --knowledge C:/repos/asgard-proveedores-knowledge --sqlglot C:/repos/audit-tools-proveedores-sqlglot-20261118`.
