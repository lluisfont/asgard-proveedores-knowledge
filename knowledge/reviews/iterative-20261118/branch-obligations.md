# Obligaciones de variante aceptadas

M `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; P `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. **Cuatro mejoras materiales aceptadas; cero nuevos OPS.** La pasada9 es positiva y no cuenta como cierre sin delta.

## BR-IMP-001 — Distinguir el intento automático de EDP de carga masiva M y P95

Al alcanzar el final favorable de CargaMasiva::crearViaje, M intenta registrarEdp después de WhatsApp y antes de responder. P95 no llama a ese helper en la ruta masiva. El helper existe en ambos pins y TrackingNewClass::save ordinario lo llama bajo condición de asignación. Por tanto, la ausencia de esa llamada se limita a la cadena masiva P95, incluida su reutilización desde VIN; no demuestra ausencia global de EDP, ni inserción efectiva en M. Otras rutas, triggers, datos y fallos previos no se comprobaron.

Control negativo: Helper disponible ysaveordinario enPimpiden concluir que todoPerú carece de registro automático.

Evidencia fijada:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L574-L588`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L590-L603`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/TrackingNewClass.php:L222-L224`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/TrackingNewClass.php:L222-L224`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/TrackingNewClass.php:L1635-L1648`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/TrackingNewClass.php:L1635-L1648`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L256-L283`

## BR-IMP-002 — Fecharegistro frente a created_at puede cambiar la guardia26 con las mismas filas

El historial M se ordena por fecharegistro; P95 usa tck_registrareventos.created_at. El consumidor posicional y la guardia de primera coincidencia26 se conservan, pero el mismo conjunto de filas puede llegar en un orden distinto. Con catálogo remoto no vacío, eso puede cambiar qué rama activa la guardia. La evidencia no decide qué fecha debe gobernar el orden de negocio ni cómo tratar empates. Corregir la presencia o los tipos no establece esa política temporal.

Control negativo: Si ambos timestamps inducen el mismo orden, no cambia la secuencia por este motivo. No se probaron empates ni datos reales.

Evidencia fijada:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/ListaViajesClass.php:L387-L409`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/ListaViajesClass.php:L386-L408`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/ListaViajesClass.php:L157-L190`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/ListaViajesClass.php:L157-L190`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/viajedetalle.php:L89-L90`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/viajedetalle.php:L89-L90`

## BR-IMP-003 — La referencia de lugar restringe la resolución en P95 pero no en M

P95 pasa la referencia a los callers de validación/carga y su resolver interpola un filtro de nombre/dirección; con al menos tres segmentos toma los tres primeros como nombre/latitud/longitud. M calcula una condición pero no la incorpora al SELECT y varios callers pasan solo código/cuenta. El filtro adicional cambia el conjunto candidato, sin demostrar unicidad, autorización, coordenadas válidas ni elección correcta. Ambos mantienen LIMIT1 sin ORDER BY; no se predice una fila concreta.

Control negativo: SinreferenciaPno agrega esa restricción. El ejemplo compara conjuntos candidatos, no filas realmente seleccionadas enSQL.

Evidencia fijada:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L132-L161`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L134-L178`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L438-L439`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L454-L455`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L518-L518`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L534-L534`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L632-L632`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L647-L647`

## BR-IMP-004 — Acotar a M la sustitución incondicional de fecha/hora en el temporal masivo

La sustitución incondicional por fecha/hora actuales del temporal corresponde a M. P95 usa fechacarguio/horacarguio recibidos cuando cumplen !empty de PHP, y CURRENT_DATE/TIME como fallback. El lector Excel y la ruta VIN suministran esos campos. La diferencia describe expresiones preparadas para el temporal; no acredita calendario válido, formato SQL aceptado, timezone, persistencia ni conservación de toda la programación del viaje.

Control negativo: Concampos vacíosPtambién usa actuales. No se declara reparadocastDate ni persistencia de fechas.

Evidencia fijada:

- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/controllers/CargaMasiva.php:L64-L80`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L47-L48`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/controllers/CargaMasiva.php:L64-L82`
- `a8ce2c23dead8552d2c4699e4a9b9134f7a18707:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L61-L73`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/tracking/ajax/uploadExcelCargaMasiva.php:L61-L73`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L124-L138`
- `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62:index_archivos/embarques/ajax/crear-viaje-desde-items.php:L256-L258`

## Alcance

- Comparación fijada a M/P95; no revisión semántica del nuevo head2a.
- AS-IS de código y precisión documental; no contrato empresarial aprobado ni prueba de BD o aplicación.
- No modifica el registro operativo, el ledger ni la fuente.
- Los intentos y expresiones de consulta no prueban efectos persistidos ni ausencia global de efectos.

La incorporación documental no repara la aplicación ni acredita ejecución. La revisión positiva original se conserva en [closure-branch-obligations.json](closure-branch-obligations.json).
