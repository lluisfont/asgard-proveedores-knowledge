# Operacion y configuracion

AS-IS del commit `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, rama `master`.

## Despliegue observado

`Dockerfile:1-6` declara Apache con PHP 5.4, puerto 80, extensiones mysql,
mysqli, PDO y pdo_mysql, y zona horaria America/La_Paz. El codigo contiene
migraciones parciales a mysqli y dependencias Composer. Este archivo expresa
una receta versionada, no demuestra la imagen ni la configuracion desplegadas.

Antes de reproducir un entorno hay que confirmar la version de PHP efectiva,
extensiones, configuracion de Apache, short_open_tag, zonas horarias, permisos
de ficheros y compatibilidad de las dependencias. La sintaxis se comprobo con
PHP 8.4.25 local: tres archivos no superan ese chequeo; ver
`source-audits/master/2026-11-18/php-lint.json`. No se ejecuto la imagen de
produccion ni se actualizaron dependencias durante esta auditoria.

## Configuracion requerida

`index_archivos/cnfdb105.php:2-3` carga `.env.php` y el autoload Composer.
Las familias de configuracion observadas incluyen conexion de base de datos,
HOME, rutas de archivos e integraciones de notificacion y servicios externos.
Consultar los simbolos usados en el [catalogo de integraciones](integrations.md).
Los nombres de variables y referencias se conservan; las credenciales no se
publican en el Knowledge Pack. La existencia de `.env-example.php` no acredita
que cubra todas las variables usadas por cada entorno.

La seleccion de pais depende tambien de rama, datos y configuracion, no solo
del nombre del repositorio. Las rutas nacionales de master muestran Bolivia;
la variante de Peru se documenta separadamente en `knowledge/variants/peru.md`.

## Submodulos

`.gitmodules:1-8` declara intercambio documental y servicio de notificaciones,
ambos sobre ramas develop de repositorios externos GitLab. Se inventariaron
sus gitlinks, pero no se descargaron ni auditaron sus implementaciones. Sus
contratos efectivos, autenticacion y despliegue siguen pendientes.

## Procedimiento para cambios

1. Identificar rama y commit exactos y leer el alcance de su variante.
2. Consultar procesos, reglas, glosario y contratos afectados.
3. Comparar el cambio con la matriz de archivos entre master y master_peru.
4. Actualizar evidencias, escenarios de regresion y riesgos antes de publicar
   comportamiento nuevo como documentado.
5. Ejecutar los validadores del paquete; registrar tambien los limites de
   pruebas de aplicacion, esquema SQL y despliegue.

## Operacion pendiente de acreditar

No se recibieron configuraciones reales de produccion, esquemas de master,
inventarios de roles efectivos, cron, backups, retencion, recuperacion ante
fallos, monitorizacion ni procedimientos operativos aprobados. Estos puntos
permanecen `unknown`; no deben rellenarse con valores del dump de Peru.

## Referencias de compatibilidad

El manual oficial documenta que el
[operador ternario](https://www.php.net/manual/en/language.operators.comparison.php#language.operators.comparison.ternary)
dejo de ser asociativo en PHP 8.0. Las
[constantes no definidas](https://www.php.net/manual/en/language.constants.syntax.php)
tienen comportamiento distinto antes y despues de PHP 8.0, relevante para la
guardia legacy. La funcion
[password_verify](https://www.php.net/manual/en/function.password-verify.php)
existe de forma nativa desde PHP 5.5; su uso no acredita por si solo una ruta
de acceso operativa sobre la imagen PHP 5.4 declarada.
