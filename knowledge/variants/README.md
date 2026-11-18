# Variantes auditadas: master y Peru

Auditoria estatica del 2026-11-18 sobre `C:/repos/proveedores-github-review-20261118`. Los nombres de pais son etiquetas de navegacion; las diferencias se justifican con codigo, consultas y configuracion versionada.

| Identificador | Referencia comprobada | Commit inmutable |
| --- | --- | --- |
| M | `master` | `a8ce2c23dead8552d2c4699e4a9b9134f7a18707` |
| P | `origin/master_peru` | `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62` |

Las citas enlazan a `KPO-Group/proveedores`, remoto observado del checkout, con commit, ruta y lineas exactas. La fuente leida fue el objeto Git local mediante `git show <commit>:<ruta>`, no una rama remota mutable. Los numeros de linea cuentan separadores LF del blob, conservando las lineas de archivos CRLF. Una ausencia se fundamenta en el arbol completo, no en una busqueda parcial.

## Navegacion

- [Bolivia: comportamiento observado de master](bolivia.md).
- [Peru: cambios de comportamiento](peru.md).
- [Comparacion y mediciones reproducibles](comparison.md).
- [Arquitectura](../general/architecture.md), [modelo de datos y autoridad del esquema](../general/data-model.md) e [integraciones](../general/integrations.md).

## Medicion de arboles

| Medida | Resultado |
| --- | ---: |
| Entradas recursivas M | 10,629 |
| Entradas recursivas P | 10,685 |
| Misma ruta, modo, tipo y objeto | 10,466 |
| Misma ruta con entrada diferente | 159 |
| Solo M | 4 |
| Solo P | 60 |

Se incluyen dos gitlinks por arbol: M tiene 10,627 blobs y P 10,683. Los dos gitlinks cambian; por tanto las 159 entradas modificadas son 157 blobs y dos referencias a submodulos. El diff habitual informa **221 registros**: 159 modificaciones, 58 altas, dos bajas y dos renombrados. Con `--no-renames` son **223**: 159 modificaciones, 60 altas y cuatro bajas. No son resultados contradictorios. Detalle en [comparacion](comparison.md).

## Limites de confianza

- **Compartido** significa igualdad del objeto versionado en ambos pins, no equivalencia de bases de datos, permisos cargados, secretos, servicios o despliegues. `.env.php` y `index_archivos/vendor/` estan excluidos del repositorio ([M `.gitignore`, L1-L3](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/.gitignore#L1-L3)).
- **Cambio funcional observado** describe lo que implementa el codigo; no certifica que se ejecute correctamente. **Etiqueta/default de pais** describe presentacion, IDs o zona horaria; no demuestra requisitos legales ni aislamiento por pais.
- Ambos pins contienen un unico `.sql`: el demo `index_archivos/js/jqwidgetsVer/phpdemos/Northwind.MySQL5.sql`. No hay esquema SQL de la aplicacion versionado. El historico `asgardpe Base de Datos Peru.sql` del paquete anterior no es un modelo universal. El archivo actual `C:/repos/proveedores/asgard.sql` existe y figura como `?? asgard.sql`; su procedencia y autoridad siguen sin confirmar. Vease [modelo de datos](../general/data-model.md).
- Los submodulos estan sin poblar. Se compararon solo sus referencias y los puntos de inclusion; se excluyo su codigo y no se descargaron fuentes externas ([M `.gitmodules`, L1-L8](https://github.com/KPO-Group/proveedores/blob/a8ce2c23dead8552d2c4699e4a9b9134f7a18707/.gitmodules#L1-L8)).
- Los informes historicos de Graphify/Brownfield conservan su propia procedencia. Esta auditoria no los convierte en validacion del master actual ni eleva el glosario generico autogenerado a glosario de negocio terminado. Estado: **evidencia estatica, validacion de ejecucion pendiente**.

No se incluyen dumps de codigo, credenciales, valores de claves ni tokens. No se realizaron commits, pushes, consultas a bases de datos ni llamadas a servicios de negocio.
