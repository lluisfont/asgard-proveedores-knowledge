# Guardrails

1. No asumir cobertura si un gate indica FAIL.
2. No convertir `unknown`, `partial`, `ambiguous` o `inferred` en requisito confirmado.
3. Revisar impacto antes de tocar API, SQL, permisos, autenticacion o integraciones.
4. Si hay cambios funcionales desde el commit auditado, refrescar auditorias afectadas o marcar el pack como partial.

