# AS-IS Business Process Mapper

Use `.brownfield/work/process_maps/` as technical evidence, not as a finished business process.

For each process reconstruct:
- business goal;
- trigger and termination;
- actors and permissions;
- preconditions;
- happy path;
- branches and exceptions;
- state transitions;
- data read/written;
- integrations and side effects;
- transaction boundaries;
- known defects and risks.

Every process must include a useful candidate business flow, even when it remains unvalidated.
Mark inferred goals, actors, steps, branch ordering, business rules and outputs as `INFERRED_DRAFT_REVIEW_REQUIRED`.
Every step must cite source/evidence.
Write technical documentation in `config/project.yaml.documentation_languages.technical`.
Write business process descriptions in `config/project.yaml.documentation_languages.business`.

Produce one Mermaid diagram per validated business process and a cross-process context map.
