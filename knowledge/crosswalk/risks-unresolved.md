# Riesgos y pendientes actuales

La [ampliación iterativa](../reviews/iterative-20261118/README.md) añade [defectos operativos](../general/operational-findings.md), una variante de inventario Perú y SEC-015. Los controles de la auditoría validan evidencia y reproducen contratos aislados; los hallazgos documentados siguen pendientes de corrección y verificación en aplicación.

AS-IS estatico del commit `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`, rama `master`. Los candidatos requieren verificar configuracion y despliegue.

Consultar la [auditoria de seguridad](../general/security-audit.md), los [hallazgos estructurados](../general/security-findings.json), las [preguntas pendientes](../general/open-questions.md) y el [plan de pruebas](../general/testing.md).

El resultado global sigue PARTIAL: falta el esquema SQL de master, no se verifico el despliegue, los submodulos ni la matriz de autorizacion efectiva. La auditoria nativa ASGARD esta bloqueada por Application Control; sus resultados no se sustituyen por una falsa ausencia de APIs. Las senales de escaner se separan de hallazgos revisados y no equivalen automaticamente a vulnerabilidades confirmadas.
