# Modulos, permisos y clientes

El extractor solo identifico las siguientes senales de permisos. No constituyen una matriz completa de roles, tenants o clientes. Fuente: `source-audits/brownfield/reports/evidence/evidence.jsonl`.

| Evidencia ID | Fuente | Linea | Observacion | Confianza |
| --- | --- | --- | --- | --- |
| EV-PERMISSION-33124F22EE4B1B | index_archivos/libs/fileinput/CHANGE.md | 191 | - (enh #1249, #290): Add capability for resumable and chunk uploads. | observed |
| EV-PERMISSION-F08494FCB483AD | index_archivos/libs/fileinput/CHANGE.md | 409 | - (enh #977): Add RTL capability (new property `rtl` to be set) - includes new `fileinput-rtl.css` (to be loaded after `fileinput.css` for RTL styling). | observed |
| EV-PERMISSION-6AAA5589A741DA | index_archivos/libs/fileinput/CHANGE.md | 748 | - (enh #427): Add image resizing capability before upload. | observed |
| EV-PERMISSION-3CDC2AD4B92EDE | index_archivos/libs/fileinput/LICENSE.md | 17 | this software without specific prior written permission. | observed |
| EV-PERMISSION-C11A37741E4AE9 | index_archivos/resetpassword/js/vue.js | 696 | var isAllowed = allowedGlobals_1(key) \|\| | observed |
| EV-PERMISSION-D1F4AB413023F4 | index_archivos/resetpassword/js/vue.js | 700 | if (!has && !isAllowed) { | observed |
| EV-PERMISSION-3F7F0DB43627FD | index_archivos/resetpassword/js/vue.js | 706 | return has \|\| !isAllowed; | observed |

La asignacion real rol-cliente-modulo queda `unknown` hasta revisar las reglas de acceso y el contexto de despliegue. Los candidatos de endpoint se encuentran en `screens-endpoints-tables.md`.
