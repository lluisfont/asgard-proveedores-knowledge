# Comparacion master / Peru

M = `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; P = `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. Fuente leida: objetos Git de `C:/repos/proveedores-github-review-20261118`, el 2026-11-18. Los enlaces contienen el pin completo, ruta y lineas; no apuntan al HEAD cambiante.

## Medidas y semantica del diff

| Medida de `git ls-tree -r` | M | P |
| --- | ---: | ---: |
| Entradas totales | 10,629 | 10,685 |
| Blobs | 10,627 | 10,683 |
| Gitlinks | 2 | 2 |
| Solo en ese arbol | 4 | 60 |

Hay **10,466 entradas identicas** en la misma ruta y **159 entradas cambiadas** en rutas compartidas, comparando `(modo, tipo, objeto)`. Las identicas son blobs; ambos gitlinks cambian. Comprobacion aritmetica: `10466 + 159 + 4 = 10629`; `10466 + 159 + 60 = 10685`.

| Presentacion Git | Modificadas | Altas | Bajas | Renombradas | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Diff con deteccion de renombrados | 159 | 58 | 2 | 2 | 221 |
| Diff con `--no-renames` | 159 | 60 | 4 | 0 | 223 |

Los dos pares detectados como renombrados son `reportetrackingnacionallocal.php` → `reporteviajescargamasiva.php` (R080) y sus archivos `query.php` (R060), todos en `index_archivos/reportes/`. Git reconoce similitud, no identidad; cambian contenido y finalidad aparente del informe. Las otras dos rutas exclusivas M son las guardas de descarga e imagen.

Las 60 rutas exclusivas P incluyen codigo de aplicacion, assets/jquery-ui, propuestas OpenSpec y un test. No son 60 funciones nuevas. Las mediciones incluyen bibliotecas de terceros; no constituyen un porcentaje de equivalencia funcional ni cobertura de auditoria.

## Componentes comunes comprobados

Se compararon los IDs de blob en los dos pins. Ejemplos de igualdad exacta:

| Ruta | Blob compartido | Que demuestra |
| --- | --- | --- |
| `.env-example.php` | `8226c56b7b9b86d32e7d021e85b1ee4efa3b06f6` | Mismo ejemplo de configuracion; no mismo `.env.php` desplegado. |
| `Dockerfile` | `1809ef64124c79d50557492ca9884293acfa0b6c` | Misma definicion PHP 5.4/La Paz, incluso en P. |
| `package.json` | `936d198888e5c20a3e1d3fdc0de7717dab1628d4` | Mismos comandos Docker y test de npm sin prueba implementada. |
| `index_archivos/composer.json` | `390c7f15d42d3e9a00a16c8549a73399daf0aa4a` | Mismas declaraciones Pusher/Carbon/Guzzle; no mismo vendor instalado. |
| `index_archivos/MailClass.php` | `259021860e416d356b028b8494928f725cc2d9e8` | Mismo cliente de correo SendGrid. |
| `index_archivos/embarques/embarquesController.php` | `94dec7d667025de14cee0a1dfb174ee242cd9722` | Mismo script orquestador; sus clases incluidas si cambian. |
| `src/core/users/config.php` | `b1e1ff9828626fcb8649c65bb14d2bbefb200bad` | Misma configuracion secundaria; no prueba de uso en todas las rutas. |

Evidencia legible de esas funciones: [M Docker, L1-L6](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/Dockerfile#L1-L6), [P Docker, L1-L6](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/Dockerfile#L1-L6), [M Composer, L1-L12](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/composer.json#L1-L12), [P Composer, L1-L12](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/composer.json#L1-L12), [M controlador, L9-L20](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/embarquesController.php#L9-L20), [P controlador, L9-L20](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/embarquesController.php#L9-L20), [M correo, L11-L14](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/MailClass.php#L11-L14) y [P correo, L80-L86](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/MailClass.php#L80-L86). No se reproducen valores secretos del ejemplo ni del codigo.

## Cambios sustantivos y defaults de pais

| Area / clasificacion | M | P | Evidencia primaria |
| --- | --- | --- | --- |
| Zona horaria / default | La Paz en bootstrap. | Lima y zona SQL -05:00; quedan defaults compartidos La Paz. | [M bootstrap L11-L25](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/cnfdb105.php#L11-L25); [P L11-L24](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/cnfdb105.php#L11-L24). |
| Geografia / default y etiqueta | Creacion con pais 31; formularios nacionales agregan BOLIVIA. | Creacion con 179; quita el sufijo; listado aun usa 31. | [M creacion L30-L33](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/embarquecrear.php#L30-L33); [P L30-L34](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/embarquecrear.php#L30-L34); [M etiqueta L19-L24](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/componentes/cotizaciones/nacional/aereo.php#L19-L24); [P listado L14-L23](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/index.php#L14-L23). |
| Clientes / consulta | Selector general sin filtro 417. | Selector limitado a 417. | [M L252-L262](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/CotizacionClass.php#L252-L262); [P L252-L262](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/CotizacionClass.php#L252-L262). |
| Tipo 7 / comportamiento | Adaptador de usuario sin caso concesionario. | JOIN a concesionario y mapeo CONCESIONARIO; filtro de embarques por concesionario. | [M adaptador L25-L61](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/src/core/users/application/Find/UserFind.php#L25-L61); [P L25-L63](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/src/core/users/application/Find/UserFind.php#L25-L63); [P filtro L368-L382](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/EmbarqueClass.php#L368-L382). |
| Columnas nacionales / comportamiento | Lista fija con factura. | Operador para tipo 7; sin factura para tipo 1; filtros/columnas coordinados. | [M L97-L132](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/index.php#L97-L132); [P L20-L61](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/EmbarqueClass.php#L20-L61). |
| Pedidos / flujo ampliado | Ya existe creacion local para 417 y detalle API. | Pantalla de gestion, carga Excel, agrupacion/clonado, conversion y refresco independiente. | [M creacion L680-L689](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/CotizacionClass.php#L680-L689); [P API de agrupacion L426-L446](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/js/datosPedidos.js#L426-L446); [P conversion L582-L654](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/js/datosPedidos.js#L582-L654). |
| Preembarques / nuevas vistas y contratos | Sin directorio `preembarques/` en arbol M. | Lista, detalle e inventarios 1/2/3 mediante API. | Ausencia: inventario `git ls-tree -r M`; [P lista L25-L44](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/preembarques/js/datosPreembarques.js#L25-L44); [P inventarios L351-L399](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/preembarques/js/datosPreembarques.js#L351-L399). |
| Inventario / contrato cambiado | Lista local recibe embarque/chasis/partida en cuerpo. | Embarque en URL, `busqueda`, filtros nacionales, fotos 360/ZIP y kilometraje. | [M llamada L86-L109](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js#L86-L109); [P L150-L188](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js#L150-L188); [P kilometraje L45-L62](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/componentes/inventario-local/kilometraje.js#L45-L62). |
| Viajes / nueva orquestacion | Ya tiene carga masiva y seguimiento. | VIN seleccionados → validacion → filas de carga masiva → crear viaje; filtra soft deletes y viajes existentes. | [M carga masiva L19-L30](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/tracking/controllers/CargaMasiva.php#L19-L30); [P endpoint L51-L99](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/ajax/crear-viaje-desde-items.php#L51-L99), [L256-L283](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/embarques/ajax/crear-viaje-desde-items.php#L256-L283). |
| Video / nuevo proxy | Sin `getVideo.php` en arbol M. | Formularios con video, comprobacion de proveedor, cache y rangos HTTP; requiere servicio blob y campos DB. | [P acceso L473-L493](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/tracking/ListaViajesClass.php#L473-L493); [P proxy L133-L204](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/tracking/getVideo.php#L133-L204). |
| PHP/DB / divergencia tecnica | Puente `conexionMysqli()` y clases migradas a mysqli. | Bootstrap y clases comparadas conservan mysql; usa etiquetas cortas. | [M bootstrap L13-L49](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/cnfdb105.php#L13-L49); [P L13-L24](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/cnfdb105.php#L13-L24); [M menu L19-L40](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/MenuClass.php#L19-L40); [P L19-L40](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/MenuClass.php#L19-L40). |
| Sesion/enlaces / divergencia tecnica | Entrada frameset a login; cifrado OpenSSL con manejo de fallo. | Entrada reconoce sesion, rechaza POST y difiere carga del frame; mantiene mcrypt en enlaces externos. | [M entrada L57-L82](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index.php#L57-L82); [M cifrado L11-L54](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index.php#L11-L54); [P sesion L1-L23](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index.php#L1-L23), [P cifrado/frame L59-L93](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index.php#L59-L93). |
| Descargas/imagenes / control diferente | Guardas locales de sesion y ruta. | Elimina guardas y sus inclusiones; no asumir controles equivalentes. | [M descarga L1-L10](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/download.php#L1-L10); [P L1-L9](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/download.php#L1-L9); [M imagen L1-L6](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/index_archivos/tracking/getImage.php#L1-L6); [P L1-L5](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/index_archivos/tracking/getImage.php#L1-L5). |

## Obligaciones por ruta — BR-IMP-001..004

La igualdad de una operación concreta no equivale a igualdad de sus productores, entradas o efectos posteriores. Estas cuatro precisiones aceptadas se acotan a M/P95; el head remoto2a queda fuera de la revisión semántica.

| ID / contrato | M | P95 | Límite que se conserva |
| --- | --- | --- | --- |
| [BR-IMP-001](peru.md#br-imp-001), intento EDP de carga masiva | Tras WhatsApp llama `registrarEdp`. | La ruta masiva retorna sin esa llamada; el helper y el `save` ordinario sí existen. | No inferir ausencia global de EDP ni inserción efectiva desde una llamada. |
| [BR-IMP-002](peru.md#br-imp-002), orden del historial | `ORDER BY fecharegistro ASC`. | `ORDER BY tck_registrareventos.created_at ASC`. | Mismas filas pueden cambiar la posición de26; no determina la fecha correcta del negocio. |
| [BR-IMP-003](peru.md#br-imp-003), referencia de lugar | La condición calculada no entra en el SELECT. | Filtro por referencia nombre/dirección o primeros tres segmentos nombre/latitud/longitud. | Restricción de candidatos y `LIMIT 1` no prueban unicidad, autorización o elección correcta. |
| [BR-IMP-004](peru.md#br-imp-004), fecha/hora del temporal | Expresiones actuales aun con O/P recibidas. | Entrada con `!empty`; fallback actual si no se cumple. | Usar entrada no valida calendario/SQL/timezone ni acredita persistencia o programación completa. |

Evidencia de código con pin completo, controles negativos y relación con OPS-004/005/006 están en [las cuatro entradas aceptadas](../reviews/iterative-20261118/branch-obligations.md). La [documentación de Perú](peru.md#br-imp-001) incluye los enlaces primarios por rango. Las precisiones CLR/RPR de pérdida, primera coincidencia y retorno explícito siguen vigentes; estas diferencias no las sustituyen ni añaden nuevos OPS.

## Submodulos fuera de alcance

| Ruta | Gitlink M | Gitlink P |
| --- | --- | --- |
| `index_archivos/intercambioDocumental` | `dc840f9dd80d5d0bda0f31c343a0f9f877519327` | `bcae698d28704445169ce3641ea7477de04666bc` |
| `index_archivos/servicioNotificaciones` | `71e3097542750058b4880f3595cd2ed3b1a89fc6` | `9473651c4052376406747ad0715940000d2c5f59` |

`git submodule status` del checkout M muestra ambos con prefijo `-` (sin inicializar). Los pins se extrajeron con `git ls-tree -r` de cada commit. No se inspecciono su implementacion ni se ejecuto `submodule update`/fetch. Las inclusiones del llamador solo demuestran dependencias ([M definiciones, L1-L8](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/.gitmodules#L1-L8); [P inclusiones de usuario, L3-L5](https://github.com/KPO-Group/proveedores/blob/95fe9a4c3b3cddd84be922cc0e1eb9c88603df62/src/core/users/application/Find/UserFind.php#L3-L5)).

## Reproducir sin cambiar el checkout

```powershell
$sourceRepo = 'C:/repos/proveedores-github-review-20261118'
$masterPin = 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707'
$peruPin = '95fe9a4c3b3cddd84be922cc0e1eb9c88603df62'
git -C $sourceRepo rev-parse master origin/master_peru
git -C $sourceRepo ls-tree -r $masterPin
git -C $sourceRepo ls-tree -r $peruPin
git -C $sourceRepo diff --name-status --find-renames=50% $masterPin $peruPin
git -C $sourceRepo diff --no-renames --name-status $masterPin $peruPin
git -C $sourceRepo diff --unified=4 $masterPin $peruPin -- index_archivos/embarques/EmbarqueClass.php
```

Comparar los dos mapas por ruta y tupla `(modo,tipo,objeto)` reproduce los conteos sin semantica de renombrados. Para revisar una cita, leer el blob del pin indicado y contar sus lineas LF. Los archivos de configuracion contienen literales sensibles: no volcar su contenido en documentacion ni logs compartidos.
