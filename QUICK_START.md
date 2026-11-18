# Quick Start

## 1. Validar

```powershell
.\scripts\knowledge\validate.ps1 -Root .
python scripts/audit/validate_knowledge.py
```

Debe responder:

```text
Knowledge Pack validation PASS
```

## 2. Usar Sin Codigo

Abrir:

```text
knowledge/README.md
knowledge/INDEX.md
knowledge/glossary/business-glossary.md
knowledge/general/user-manual.md
knowledge/variants/README.md
source-audits/
```

## 3. Instalar En Checkout De Programador

```powershell
.\install-knowledge-pack.ps1 -TargetRepo "C:\repos\dev\asgard-proveedores"
```

Dentro del checkout:

```powershell
.\scripts\knowledge\update.ps1
```

Si `knowledge/snapshots/current/code-db-audit-coverage.md` dice `PARTIAL` o
`FAIL`, revisar la accion indicada. Un repositorio standalone documenta una
instantanea; no es un checkout de aplicacion ni demuestra el esquema SQL o
el despliegue real. El glosario y la documentacion pueden consultarse con sus
limites de evidencia explicitos.

