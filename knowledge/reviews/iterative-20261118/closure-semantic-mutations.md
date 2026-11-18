# Mutaciones semánticas de afirmaciones documentales

**21 registros revisados después de aceptar BR-IMP-001..004: 9 OPS, 8 mejoras operativas y 4 BR externas. Sin nuevos hallazgos o mejoras en este alcance; no convergencia global.**

Se conserva [el abstracto anterior](closure-abstract-contracts.json) como auxiliar sin delta anterior a BR4. No se incorporan las cuatro BR al registro operativo: su integración de variantes pertenece al otro agente. Esta pasada usa las cuatro mejoras aceptadas del [sidecar BR](closure-branch-obligations.json), como autorizó el usuario; el registro de variantes no existía todavía al ejecutar.

Pins: M `a8ce2c23dead8552d2c4699e4a9b9134f7a18707`; P95 histórica `95fe9a4c3b3cddd84be922cc0e1eb9c88603df62`. No se audita el nuevo head Perú ni se cambian refs.

## Técnica y resultados

Se extraen propiedades concretas de la fuente fijada y se representan afirmaciones con país, valor semántico, caller o condición, y calificadores requeridos. Cada registro tiene un control positivo. Se muta el valor/caller, se elimina un calificador y se intercambia el país; los BR añaden mutaciones de timestamp o fallback. No se repiten fallos inyectados ni la fórmula de estados abstractos.

| Resultado | Mutaciones | Significado |
|---|---:|---|
| SOURCE_CONTRADICTED | 30 | La afirmación alterada difiere de la propiedad extraída. |
| NOT_ENTAILED_WITHOUT_QUALIFIER | 23 | Al retirar la condición, la fuente deja de sustentar la afirmación más amplia. No prueba su contrario en producción. |
| SUPPORTED_WITHIN_PIN_AND_SCOPE | 17 | Controles de país legítimamente equivalentes en esa propiedad; no acreditan equivalencia global de runtime. |

En total, 70 mutaciones y 21 checks `completed`. Los resultados y el código reproducible figuran en [closure-semantic-mutations.json](closure-semantic-mutations.json). Se leen objetos Git; no se ejecuta código de aplicación.

```powershell
python -X utf8 -B -c "import json; from pathlib import Path; d=json.loads(Path('knowledge/reviews/iterative-20261118/closure-semantic-mutations.json').read_text(encoding='utf-8')); exec(compile(d['reproduction_code'], '<semantic-mutation-review>', 'exec'))"
```

## Checks por registro

| ID | Propiedad de fuente contrastada | Calificadores preservados |
|---|---|---|
| OPS-001 | `cost_master_identity` = `"shipment_creator_max_id"` | concurrent_visible_other_insert, source_not_production |
| OPS-002 | `location_return` = `"overwritten_status_of_last_successful_location"` | ordinary_returns_no_exception, multiple_required_locations |
| OPS-003 | `load_replace` = `"DELETE_then_call_four_for_five_required"` | call_reached_after_DELETE_true, loss_requires_matching_committed_rows, PHP8_not54 |
| OPS-004 | `batch_mark` = `"batch_and_user_without_group"` | multiple_groups_snapshot, update_confirmed_no_external_correction |
| OPS-005 | `event_merge` = `"positional_overwrite"` | nonempty_remote, history_not_unique_prefix, representation_not_SQL_mutation |
| OPS-006 | `event_guard` = `"truthiness_of_first_array_search_index"` | first_matching_index0, no_business_meaning_for26 |
| OPS-007 | `cost_total` = `"client_totalCategory"` | header_total_differs_from_detail, no_DB_constraint_claim, monetary_policy_unapproved |
| OPS-008 | `edit_chassis` = `"header_success_then_truthy_new_chassis_child_without_return"` | edit_not_create_route, PHP_truthy_not_every_nonempty, no_upstream_policy_claim |
| OPS-009 | `mostrartabla_arity` = `[1,2]` | mostrartabla_not_main_AJAX, PHP8_not54, JS_reachability_unverified |
| IMP-T008 | `save_optional_results` = `"unchecked_routes_relay_locations"` | optional_false_can_be_no_request, only_observed_helper_chain |
| IMP-T009 | `status_time` = `"updated_at_alias_and_separate_interruption_time"` | DDL_trigger_unknown, UI_filter_not_server_state_machine |
| IMP-T010 | `cast_date` = `"slash_reorder_or1900_without_calendar_check"` | format_absence_policy_unapproved, SQL_acceptance_unknown |
| CLR-IMP-001 | `deletion_evidence` = `"statement_bool_without_affected_count"` | zero_rows_is_possible, commit_required_for_loss |
| CLR-IMP-002 | `guard_repetitions` = `"first_match_index0_remains_falsy"` | first_match_not_any_later_index, event26_meaning_unverified |
| CLR-IMP-003 | `child_return` = `"implicit_NULL_even_if_queries_succeed"` | child_not_parent_return, queries_not_executed |
| RPR-IMP-001 | `count_partition` = `"proposed_only_not_implemented_in_helper"` | TO_BE_not_AS_IS, no_op_policy_conditional, count_client_config_unknown |
| RPR-IMP-002 | `id_normalization` = `"proposed_only_not_before_current_search"` | TO_BE_not_AS_IS, documented_int_digit_string_only, runtime_type_unknown |
| BR-IMP-001 | `bulk_edp_call` = `true` | bulk_route_not_all_routes, attempt_not_persistence |
| BR-IMP-002 | `event_order` = `"fecharegistro"` | producer_order_pin_specific, same_order_possible_no_universal_divergence |
| BR-IMP-003 | `reference_in_resolver_SQL` = `true` | nonempty_reference, SQL_interpolation_not_only_variable_construction, LIMIT1_not_uniqueness |
| BR-IMP-004 | `temporary_dates` = `"input_if_not_empty_else_current"` | not_empty_input_else_fallback, temporary_expression_not_full_trip_schedule, no_calendar_timezone_claim |

## Mutaciones BR y sus controles

- **BR-IMP-001:** atribuir a P95 el intento EDP de carga masiva M contradice la cadena. Cambiar el caller VIN a save ordinario también. El helper y save ordinario P95 sí pueden intentar EDP: se rechaza afirmar que todo Perú carece de esa vía.
- **BR-IMP-002:** M ordena por fecharegistro y P95 por tck_registrareventos.created_at. Intercambiarlos contradice el productor. Si ambas fechas dan el mismo orden, no se infiere divergencia.
- **BR-IMP-003:** M construye una condición pero no la interpola en ese SELECT; P95 sí la incorpora cuando la referencia no está vacía. LIMIT1 no prueba unicidad o geografía. El predicado de segmentos es >2, no exactamente3; cuatro segmentos siguen usando los primeros tres.
- **BR-IMP-004:** M usa fecha/hora actuales en el temporal. P95 usa entrada no vacía y actuales como fallback. Quitar esa condición o afirmar siempre entrada pierde el contrato. Esto no valida calendario, zona horaria ni programación completa del viaje.

## Deduplicación y límites

Mutations expose already accepted OPS/operational/BR distinctions; no additional independent omission found. Equivalent country mutations survive only where pinned source facts match, without inferring runtime equality.

Las diferencias y precisiones expuestas por las mutaciones ya pertenecen a los registros aceptados. No se vuelve a contar el error de aridad existente, la mezcla posicional o los fallos parciales genéricos. Las reglas TO-BE no se promocionan a comportamiento actual.

- 21registros aceptados:9OPS+8mejoras operativas propias+4BRaceptadas externas. No global convergence or absence-of-defects claim.
- País significa pin inmutable M/P95, no despliegue. P95es comparación histórica, no último Perú.2a179e2no auditado; no refs cambiadas.
- Una mutación SOURCE_CONTRADICTED difiere del valor extraído. NOT_ENTAILED_WITHOUT_QUALIFIER significa que la fuente no sustenta la afirmación ampliada, no prueba el contrario en producción.
- Las17mutaciones equivalentes legítimas no son fallos del test ni igualdad funcional global: conservan solo la propiedad leída en los dos pins.
- Se usan BR4aceptadas del sidecar por autorización del usuario; al ejecutar, el registro externo de variantes aún no existía. No se edita ni se espera aprobación adicional.
- No PHP/motorSQL ni agendas de fallo, BD/red, sesiones o salidas de navegador/navegación. No se ejecutan rutas.
- No se inventa timezone, calendario válido, unicidad, geografía correcta, EDPpersistido ni significado empresarial de26.
- Reparaciones siguen TO-BE. Fuente AS-IS, riesgo condicionado y propuesta se separan. Sin ledger, main ajeno, commits o push.

No se compila ledger ni se editan las variantes del otro agente o archivos ajenos del main. El log de integración conserva la secuencia y el fingerprint final.
