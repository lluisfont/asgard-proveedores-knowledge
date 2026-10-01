# Technical component map: `index_archivos/embarques/ajax/listaLineasFiltro.php`

Status: `CANDIDATE_AS_IS`

> Relationships are observed or candidate-level in the same component and are not yet a confirmed execution sequence.

```mermaid
flowchart LR
  N96b3ab8d7c8d["dav_clientelineas"]
  N847c8d025783["logis_embarques"]
  Ne70cfdc3cc76["index_archivos/embarques/ajax/listaLineasFiltro.php"]
  Nbabd78d00f25["CLI_COMMAND: index_archivos/embarques/ajax/listaLineasFiltro.php"]
  Ne70cfdc3cc76 -- "reads" --> N96b3ab8d7c8d
  Ne70cfdc3cc76 -- "reads" --> N96b3ab8d7c8d
  Ne70cfdc3cc76 -- "reads" --> N96b3ab8d7c8d
  Ne70cfdc3cc76 -- "reads" --> N96b3ab8d7c8d
  Ne70cfdc3cc76 -- "reads" --> N96b3ab8d7c8d
  Ne70cfdc3cc76 -- "reads" --> N96b3ab8d7c8d
  Ne70cfdc3cc76 -- "reads" --> N96b3ab8d7c8d
  Ne70cfdc3cc76 -- "reads" --> N847c8d025783
  Ne70cfdc3cc76 -- "reads" --> N847c8d025783
  Ne70cfdc3cc76 -- "reads" --> N847c8d025783
  Ne70cfdc3cc76 -- "reads" --> N847c8d025783
  Ne70cfdc3cc76 -- "reads" --> N847c8d025783
  Ne70cfdc3cc76 -- "reads" --> N847c8d025783
  Nbabd78d00f25 -- "handled_by" --> Ne70cfdc3cc76
```
