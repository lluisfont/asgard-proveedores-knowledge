# Dominios y modulos de Proveedores

AS-IS estatico del commit `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, rama `master`. Los candidatos requieren verificar configuracion y despliegue.

Entradas principales: [procesos](../general/workflows.md), [actores](../general/actors-and-permissions.md), [reglas](../general/business-rules.md), [glosario de negocio](../glossary/business-glossary.md).

| Grupo de handlers | Candidatos |
| --- | --- |
| embarques | 81 |
| tracking | 75 |
| (raiz) | 24 |
| parametros | 15 |
| reportes | 15 |
| js | 7 |
| libs | 6 |
| resetpassword | 4 |
| 2fa | 3 |
| rating | 3 |
| logistica | 2 |
| reporteexcel | 2 |
| usuario | 2 |
| ajax | 1 |
| php-jwt-5.2.0 | 1 |

Estas agrupaciones son tecnicas; no equivalen a bounded contexts confirmados. Las diferencias por pais estan en [variantes](../variants/README.md). Las pantallas dedicadas de pedidos y preembarques de Peru no se incorporan como funciones universales de master; master ya contiene operaciones relacionadas con pedidos.
