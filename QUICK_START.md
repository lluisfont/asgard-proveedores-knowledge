# Quick Start

## 1. Validar

```powershell
.\scripts\knowledge\validate.ps1 -Root .
```

Debe responder:

```text
Knowledge Pack validation PASS
```

## 2. Usar Sin Codigo

Abrir:

```text
knowledge/README.md
knowledge/product/requirements-analysis-guide.md
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

Si `knowledge/snapshots/current/code-db-audit-coverage.md` dice `FAIL`, no tratar la auditoria como vigente.

