# Technical component map: `index_archivos/controllers/GlobalClass.php`

Status: `CANDIDATE_AS_IS`

> Relationships are observed or candidate-level in the same component and are not yet a confirmed execution sequence.

```mermaid
flowchart LR
  Nf4525b5ab829["dav_cliente"]
  N96b3ab8d7c8d["dav_clientelineas"]
  Ncfbb8f884c4b["dav_clientereportescliente"]
  N3bdb417b6f2e["dav_clientetransportista"]
  N8b6f4abc9726["dav_localidad"]
  Nf838fcd7828f["dav_proveedor"]
  N7e75b82f1ff0["dav_usuario"]
  N847c8d025783["logis_embarques"]
  Nfdc9ccc828eb["logis_embarquesoperador"]
  N0863c2994040["prov_usuarioaccesoproveedor"]
  Nebbaaee950a4["index_archivos/controllers/GlobalClass.php"]
  Nbe23c82d2384["CLI_COMMAND: index_archivos/controllers/GlobalClass.php"]
  Nebbaaee950a4 -- "reads" --> Nf4525b5ab829
  Nebbaaee950a4 -- "reads" --> Nf4525b5ab829
  Nebbaaee950a4 -- "reads" --> Nf4525b5ab829
  Nebbaaee950a4 -- "reads" --> N96b3ab8d7c8d
  Nebbaaee950a4 -- "reads" --> Ncfbb8f884c4b
  Nebbaaee950a4 -- "reads" --> N3bdb417b6f2e
  Nebbaaee950a4 -- "reads" --> N8b6f4abc9726
  Nebbaaee950a4 -- "reads" --> Nf838fcd7828f
  Nebbaaee950a4 -- "reads" --> N7e75b82f1ff0
  Nebbaaee950a4 -- "reads" --> N847c8d025783
  Nebbaaee950a4 -- "reads" --> Nfdc9ccc828eb
  Nebbaaee950a4 -- "reads" --> N0863c2994040
  Nbe23c82d2384 -- "handled_by" --> Nebbaaee950a4
```
