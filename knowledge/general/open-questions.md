# Preguntas pendientes y limites

| ID | Pregunta o evidencia que falta | Impacto |
| --- | --- | --- |
| OPEN-01 | Confirmar procedencia, version y correspondencia con master del asgard.sql local candidato, o suministrar el DDL efectivo | Sus 1,432 tablas y 13,149 columnas ya tienen catalogo separado; la coincidencia nominal con consultas no valida el despliegue |
| OPEN-02 | Rama/commit y version PHP realmente desplegados por pais y cliente | El Dockerfile PHP 5.4 y el codigo modernizado no prueban el runtime efectivo |
| OPEN-03 | Matriz de roles, empresas, tenants y excepciones autorizadas | Los tipos de proveedor del codigo no equivalen a autorizacion efectiva por entidad |
| OPEN-04 | Revision con responsables de negocio del glosario y las reglas | Las definiciones reconstruidas tienen evidencia de codigo, no aprobacion funcional |
| OPEN-05 | Implementaciones y contratos de los dos submodulos | Intercambio documental y notificaciones con cobertura parcial |
| OPEN-06 | Configuracion de servicios externos, errores y reintentos en despliegue | Contratos de ejecucion y efectos secundarios sin probar |
| OPEN-07 | Significado completo de codigos de estado y campos sin uso observado | Mantener los codigos sin descripcion funcional inventada |
| OPEN-08 | Validacion de candidatos SQL/API y controles compartidos en ejecucion | Senales estaticas no confirman por si solas exposicion o explotabilidad |
| OPEN-09 | Retencion documental, backups, recuperacion y operacion aprobada | Manuales de operacion limitados a evidencia versionada |
| OPEN-10 | Ejecucion nativa de ASGARD API Auditor | Lanzador bloqueado por Windows Application Control; se uso ampliacion estatica alternativa |

Cada respuesta nueva debe incluir procedencia, fecha, alcance de variante y
ubicacion de evidencia. Actualizar el glosario, procesos, contratos y pruebas
afectados conservando el historial previo. El estado global sigue `PARTIAL`
mientras las evidencias necesarias para esas dimensiones no esten disponibles.
