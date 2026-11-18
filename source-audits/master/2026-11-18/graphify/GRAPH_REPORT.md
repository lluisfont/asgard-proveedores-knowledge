# Graphify master: AST local

Fuente: master a8ce2c23dead8552d2c4699e4a9b9134f7a18707.

2173 nodos; 2711 aristas; 620 comunidades.

Se seleccionaron 545 archivos de codigo tras exclusiones de dependencias conocidas. La extraccion advirtio que 319 solo generan un nodo de fichero sin simbolos. Consultar tambien los catalogos PHP/AJAX, campos y referencias SQL.

Coste de extraccion semantica: 0 tokens de entrada y 0 de salida. No se ejecuto una API de lenguaje para construir este grafo. La revision funcional y el glosario se documentan aparte con referencias de fuente.

## Nodos conectados

| Etiqueta | Grado | Fuente |
| --- | ---: | --- |
| conexionMysqli() | 324 | index_archivos/cnfdb105.php |
| CotizacionClass | 65 | index_archivos/embarques/CotizacionClass.php |
| TrackingNewClass | 62 | index_archivos/tracking/TrackingNewClass.php |
| TrackingClass | 42 | index_archivos/tracking/TrackingClass.php |
| L() | 33 | index_archivos/js/scripts/knockout-2.2.1.js |
| CostosClass | 27 | index_archivos/embarques/CostosClass.php |
| SolicitudesClass | 27 | index_archivos/embarques/SolicitudesClass.php |
| toDate() | 26 | index_archivos/resetpassword/js/vee-validate.js |
| EmbarqueClass | 24 | index_archivos/embarques/EmbarqueClass.php |
| ListaViajesClass | 21 | index_archivos/tracking/ListaViajesClass.php |
| DB | 20 | index_archivos/libs/modulos/libs/PDO.class.php |
| DB | 19 | index_archivos/libs/pdo/PDO.class.php |

## Uso y limites

La visualizacion es `graph.html`; los datos completos son `graph.json.gz`. Una conexion AST no valida ejecucion, autorizacion ni equivalencia de negocio entre paises. La configuracion y los submodulos externos siguen fuera de la comprobacion de despliegue.

Para consultar con Graphify, restaurar primero graph.json usando el helper del paquete y pasar la ruta con --graph. Los simbolos seleccionados deben corresponder a archivos del alcance; las comunidades no son requisitos ni dominios de negocio confirmados.
