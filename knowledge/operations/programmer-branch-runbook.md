# Programmer Branch Runbook

## Primer Comando En Cada Rama

```powershell
.\scripts\knowledge\update.ps1
```

Revisar:

```text
knowledge/snapshots/current/github-local-diff.md
knowledge/snapshots/current/code-db-audit-coverage.md
knowledge/crosswalk/risks-unresolved.md
knowledge/openspec/guardrails.md
```

Si el gate de cobertura dice PARTIAL o FAIL, revisar la dimension pendiente.
El commit auditado actual pertenece a master de KPO-Group/proveedores, no al
historial Git del repositorio standalone de Knowledge. En un checkout de
aplicacion se comprueban tambien cambios funcionales sin commit; el esquema
SQL de master sigue pendiente de proporcionar y verificar.

