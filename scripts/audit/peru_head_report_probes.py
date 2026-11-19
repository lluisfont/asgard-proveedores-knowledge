"""Pinned Peru report review: text extraction and synthetic predicate/relational probes.

No PHP interpreter, handlers, includes, SQL engine, database, network, deployment,
browser, or real application rows. Only git read commands and the three sidecar
outputs below are used. Run from any directory with Python 3.10+ (stdlib only).
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess


HEAD = "2a179e2e6472d5705d031665ecbc90c3d806edec"
P95 = "95fe9a4c3b3cddd84be922cc0e1eb9c88603df62"
M = "a8ce2c23dead8552d2c4699e4a9b9134f7a18707"
KB = "0c4bb99f076d6a8c18ae98375d6e154da6319922"
PAGE = "index_archivos/reportes/reportepreembarquenacional.php"
QUERY = "index_archivos/reportes/reportepreembarquenacionalquery.php"
READ_PATHS = [PAGE, QUERY, "index_archivos/permisos.php", "index_archivos/data.php",
              "index_archivos/cnfdb105.php", "index_archivos/veriflogin.php",
              "src/core/users/application/Find/UserFind.php", "index_archivos/MenuClass.php",
              "index_archivos/menu.php", "index_archivos/menu_b4.php",
              "index_archivos/libs/reportelibs_bs2.php", "index_archivos/boton.php",
              "index_archivos/reportes/filtros/fechas.php"]
PROBES = "source-audits/peru/2026-11-19/report-probes.json"
DELTAS = "knowledge/reviews/peru-head-20261119/report-deltas.json"
MARKDOWN = "knowledge/reviews/peru-head-20261119/report-deltas.md"


def git(root, *args):
    # All callers below use read-only commands and immutable local object IDs.
    return subprocess.check_output(["git", "-C", str(root), *args])


def text_blob(root, commit, path):
    return git(root, "show", f"{commit}:{path}").decode("utf-8-sig").replace("\r\n", "\n")


def evidence(path, start, end=None, commit=HEAD):
    return {"commit": commit, "path": path, "line_start": start, "line_end": end or start}


def date_fragment(mode, first, last):
    """Literal translation of QUERY:45-50 for nonempty slash-separated strings only."""
    if mode != "1" or not first or not last:
        return ""
    a, b = first.split("/"), last.split("/")
    return " AND DATE(p.created_at) BETWEEN '" + a[2] + "-" + a[1] + "-" + a[0] + "' AND '" + b[2] + "-" + b[1] + "-" + b[0] + "'"


def unquoted_sql(fragment):
    """Small lexical witness only; does not parse or execute SQL."""
    out, quoted, i = [], False, 0
    while i < len(fragment):
        if not quoted and fragment[i:i + 3] == "-- ":
            break
        if fragment[i] == "'":
            quoted = not quoted
            out.append(" ")
        elif not quoted:
            out.append(fragment[i])
        i += 1
    return "".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="C:/repos/proveedores-peru-head-review-20261119")
    parser.add_argument("--knowledge", default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args()
    source, knowledge = Path(args.source).resolve(), Path(args.knowledge).resolve()
    if source == knowledge or source in knowledge.parents or knowledge in source.parents:
        raise ValueError("Source and knowledge must be separate repositories")
    for root, expected in [(source, HEAD), (knowledge, KB)]:
        if git(root, "rev-parse", "HEAD").decode().strip() != expected:
            raise ValueError("Unexpected repository pin")
    blobs = {p: text_blob(source, HEAD, p) for p in READ_PATHS}
    old = {p: text_blob(source, P95, p) for p in [PAGE, QUERY]}
    for p, body in blobs.items():
        disk = (source / p).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        if disk != body:
            raise ValueError(f"Worktree differs from pinned source: {p}")
    page, query = blobs[PAGE], blobs[QUERY]
    cases = []

    def check(case_id, kind, observed, expected, basis, limit):
        cases.append({"id": case_id, "kind": kind, "status": "pass" if observed == expected else "fail",
                      "observed": observed, "expected": expected, "basis": basis, "limits": limit})

    source_limit = "Comprobación textual del blob fijado; no acredita ejecución ni accesibilidad."
    model_limit = "Modelo Python con filas sintéticas; sin motor SQL, collation, constraints ni datos reales."
    # No browser-output blocks are evaluated or tested. Only admission/SQL contracts.
    old_pred = "WHERE p.deleted_at IS NULL AND tc.idconcesionario = \".$_SESSION['idtransportista'].\""
    new_pred = "WHERE p.deleted_at IS NULL\n    AND p.proveedor_id = \".$idTransportistaSesion.\""
    check("RP-01", "source_delta", old[QUERY].replace(old_pred, new_pred) == query, True,
          [evidence(QUERY, 381, 391), evidence(QUERY, 381, 390, P95)], source_limit)
    absent_m = [p for p in [PAGE, QUERY] if not git(source, "ls-tree", M, "--", p).strip()]
    check("RP-02", "negative_control", absent_m, [PAGE, QUERY], [], "Ausencia en árbol M; no comparación con otro master.")
    check("RP-03", "source_contract", all(s in page for s in ["(int) $_SESSION['idtransportista']", ": 0;",
          'AND p.proveedor_id = ".$idTransportistaSesion."']), True, [evidence(PAGE, 6, 9), evidence(PAGE, 52, 59)], source_limit)

    # Complete truth table over small domains: SQL equality to NULL never passes WHERE.
    table = []
    for provider, dealer in itertools.product([41, 82], [None, 41, 82]):
        table.append({"provider": provider, "dealer": dealer, "P95": dealer == 41, "HEAD": provider == 41})
    check("RP-04", "predicate_matrix", [(r["P95"], r["HEAD"]) for r in table],
          [(False, True), (True, True), (False, True), (False, False), (True, False), (False, False)],
          [evidence(QUERY, 381, 382), evidence(QUERY, 381, 381, P95)], model_limit)
    # idtransportista is a generic provider ID in login, not a transportista-only identity.
    login = blobs["index_archivos/veriflogin.php"]
    finder = blobs["src/core/users/application/Find/UserFind.php"]
    check("RP-05", "identity_trace", all(s in login for s in [
          '$_SESSION["idtransportista"] = $row[\'idproveedor\'];',
          '$_SESSION["idtipoproveedor"] = $row[\'idtipoproveedor\'];']) and
          "WHEN 7 THEN cn_concesionario.nombre" in finder and "idtipoproveedor" not in page + query,
          True, [evidence("index_archivos/veriflogin.php", 85, 91),
                 evidence("src/core/users/application/Find/UserFind.php", 19, 35), evidence(PAGE, 6, 9)], source_limit)
    check("RP-06", "role_collision_and_negative", {
          "type7_provider82_dealer41": {"P95": 41 == 41, "HEAD": 82 == 41},
          "type7_provider41_dealer82": {"P95": 82 == 41, "HEAD": 41 == 41},
          "type1_owned_no_dealer": {"P95": None == 41, "HEAD": 41 == 41}},
          {"type7_provider82_dealer41": {"P95": True, "HEAD": False},
           "type7_provider41_dealer82": {"P95": False, "HEAD": True},
           "type1_owned_no_dealer": {"P95": False, "HEAD": True}}, [evidence(QUERY, 381, 382)],
          model_limit + " No se declara autorizado al tipo7 para este reporte ni colisiones existentes.")
    # A zero fallback is an equality, not an unconditional deny. No PHP cast emulation.
    check("RP-07", "negative_control", [p for p in [0, 41, 82] if p == 0], [0],
          [evidence(PAGE, 7, 9), evidence(QUERY, 381, 382)], model_limit + " Solo IDs enteros; no reproduce conversiones PHP generales.")

    # Date construction is isolated from PHP; demonstrate unquoted predicate tokens, not exploitation.
    date_basis = [evidence(PAGE, 38, 40), evidence(QUERY, 45, 50), evidence(QUERY, 381, 391)]
    normal = date_fragment("1", "01/11/2026", "19/11/2026")
    altered = date_fragment("1", "01/11/2026", "19/11/2026-11-19' OR 1=1 -- ")
    check("RP-08", "literal_extraction", normal,
          " AND DATE(p.created_at) BETWEEN '2026-11-01' AND '2026-11-19'", date_basis, source_limit)
    check("RP-09", "predicate_counterexample", bool(re.search(r"\bOR 1=1\b", unquoted_sql(altered))),
          True, date_basis, "Solo construcción y testigo léxico de OR fuera del literal; no se envía ni ejecuta SQL.")
    check("RP-10", "negative_control", [date_fragment("", "01/11/2026", "19/11/2026'"),
          date_fragment("1", "", "19/11/2026'"), bool(re.search(r"\bOR\b", unquoted_sql(normal)))],
          ["", "", False], date_basis, source_limit)
    check("RP-11", "boolean_predicate", {"owner_false_AND_date_false": False and False,
          "owner_false_AND_date_false_OR_true": (False and False) or True},
          {"owner_false_AND_date_false": False, "owner_false_AND_date_false_OR_true": True},
          date_basis, "Álgebra booleana de predicados; no validación del parser/runtime MySQL ni explotación.")
    check("RP-12", "negative_control", all(f"mysql_real_escape_string(${x})" in query for x in
          ["transportista", "concesionario", "marca", "vin"]), True, [evidence(QUERY, 3, 21)],
          "No se traslada el defecto de fechas a estos cuatro filtros; charset/conexión no comprobados.")
    # Alias checks are intentionally scoped to injected filter fragments in base.
    filter_block = query[:query.index('$query[0]')]
    aliases = sorted(set(re.findall(r"\b([a-z]+)\.[a-z_]+", filter_block)))
    check("RP-13", "negative_control", aliases, ["d", "m", "mdos", "p", "t", "tc", "te", "tra"],
          [evidence(QUERY, 3, 50), evidence(QUERY, 328, 391)], "Aliases declarados en base; no es compilación SQL.")
    check("RP-14", "negative_control", "ctype_digit(trim((string)$pre_embarque))" in query and
          "ctype_digit(trim((string)$embarque))" in query, True, [evidence(QUERY, 23, 31)], source_limit)

    # Source contracts for relational witnesses, including deletion scopes.
    te_block = query[query.index("tmp_embarques AS ("):query.index("tmp_concesionario AS (")]
    tc_block = query[query.index("tmp_concesionario AS ("):query.index("tmp_viaje AS (")]
    mdos_block = query[query.index("tmp_movimientosdos AS ("):query.index("tmp_embarques AS (")]
    check("RP-15", "join_contract", ["deleted_at" in te_block, "proveedor_id" in te_block + tc_block + mdos_block,
          "ON mdos.chasis = d.chasis" in query, "ON te.chasis = d.chasis" in query,
          "ON tc.chasis = d.chasis" in query], [False, False, True, True, True],
          [evidence(QUERY, 166, 261), evidence(QUERY, 370, 382)], source_limit)
    # Global MAX ignores tenant/preembarque and missing order/detail soft-delete filters.
    orders = [{"vin": "SYN-VIN", "shipment": 100, "owner": 41, "deleted": False},
              {"vin": "SYN-VIN", "shipment": 200, "owner": 82, "deleted": True}]
    selected = max(x["shipment"] for x in orders if x["vin"] == "SYN-VIN")
    isolated = max(x["shipment"] for x in orders if x["owner"] == 41 and not x["deleted"])
    check("RP-16", "relational_counterexample", {"global": selected, "scoped_control": isolated},
          {"global": 200, "scoped_control": 100}, [evidence(QUERY, 210, 220), evidence(QUERY, 370, 380)], model_limit)
    local_movements = [{"vin": "SYN-VIN", "shipment": 200, "owner": 82, "local_type": 2}]
    joined = [x for x in local_movements if x["vin"] == "SYN-VIN" and x["local_type"] == 2]
    check("RP-17", "relational_counterexample", {"base_owner": 41, "foreign_local_type2_matches": len(joined),
          "estadodos": "Realizado" if joined else "Pendiente"},
          {"base_owner": 41, "foreign_local_type2_matches": 1, "estadodos": "Realizado"},
          [evidence(QUERY, 166, 207), evidence(QUERY, 299, 305), evidence(QUERY, 370, 382)], model_limit)
    check("RP-18", "negative_control", [x for x in local_movements if x["vin"] == "OTHER-SYN-VIN"], [],
          [evidence(QUERY, 370, 374)], model_limit + " Sin coincidencia de chasis, el contraejemplo desaparece.")
    # Correlated movement CTEs preserve a composite key. No universal foreign-tenant claim.
    movement_keys = {(10, "SYN-VIN", 1)}
    check("RP-19", "negative_control", [(10, "SYN-VIN", 1) in movement_keys,
          (11, "SYN-VIN", 1) in movement_keys, (10, "SYN-VIN", 2) in movement_keys],
          [True, False, False], [evidence(QUERY, 339, 362)], model_limit)
    # With te/tc shipment NULL and two mdos shipments, the outer maxima can mix rows.
    base_rows = [{"embarque_id": 100, "numero_viaje": 900, "fecha": "2026-11-19"},
                 {"embarque_id": 200, "numero_viaje": 800, "fecha": "2026-11-18"}]
    aggregate = {k: max(r[k] for r in base_rows) for k in base_rows[0]}
    check("RP-20", "aggregate_counterexample", {"aggregate": aggregate, "is_original_row": aggregate in base_rows},
          {"aggregate": {"embarque_id": 200, "numero_viaje": 900, "fecha": "2026-11-19"}, "is_original_row": False},
          [evidence(QUERY, 310, 320), evidence(QUERY, 370, 380), evidence(QUERY, 393, 413)], model_limit)
    check("RP-21", "negative_control", {k: max(r[k] for r in base_rows[:1]) for k in base_rows[0]} == base_rows[0],
          True, [evidence(QUERY, 393, 413)], model_limit + " Una sola relación coherente no produce mezcla.")
    # Pre-pivot filtering changes both the vehicle population and inventory columns.
    inventories = [{"type": 1, "movement": False}, {"type": 2, "movement": True}]
    pivot = lambda rows: {str(t): next(("Realizado" if r["movement"] else "Pendiente" for r in rows if r["type"] == t), None)
                         for t in [1, 2]}
    check("RP-22", "population_contract", {"all": pivot(inventories),
          "estado1": pivot([r for r in inventories if not r["movement"]]),
          "tipo3_rows": len([r for r in inventories if r["type"] == 3])},
          {"all": {"1": "Pendiente", "2": "Realizado"}, "estado1": {"1": "Pendiente", "2": None}, "tipo3_rows": 0},
          [evidence(QUERY, 33, 43), evidence(QUERY, 53, 57), evidence(QUERY, 386, 387), evidence(QUERY, 411, 413)], model_limit)
    check("RP-23", "negative_control", pivot([r for r in inventories if r["type"] == 2]),
          {"1": None, "2": "Realizado"}, [evidence(QUERY, 33, 35), evidence(QUERY, 411, 412)], model_limit)
    # Existence semantics: a single active record is sufficient, not full inspection.
    check("RP-24", "existence_contract", [{"active_records": n, "estado": "Realizado" if n else "Pendiente"} for n in [0, 1]],
          [{"active_records": 0, "estado": "Pendiente"}, {"active_records": 1, "estado": "Realizado"}],
          [evidence(QUERY, 115, 164), evidence(QUERY, 292, 305)], model_limit)
    aux = page[page.index('$queryConcesionario ='):page.index('$resConcesionario =')]
    check("RP-25", "auxiliary_scope", ["proveedor_id" in aux, page.index('$resConcesionario =') < page.index('include("reportepreembarquenacionalquery.php")')],
          [False, True], [evidence(PAGE, 65, 86)], source_limit + " No se afirma divulgación al navegador.")
    data = blobs["index_archivos/data.php"]
    check("RP-26", "failure_control", '$result = mysql_query($query[0]);\nwhile($row = mysql_fetch_array($result))' in data,
          True, [evidence("index_archivos/data.php", 6, 14)], "False se entrega a fetch en fuente; warning/Error depende de runtime, no modelado.")
    missing_include = not git(source, "ls-tree", HEAD, "--", "index_archivos/contador.php").strip()
    check("RP-27", "include_boundary", missing_include and 'include("../contador.php");' in page, True,
          [evidence(PAGE, 29, 48)], "Ausente del árbol fijado; no afirma ausencia en despliegue ni que include continúe bajo todo error handler.")
    check("RP-28", "builder_execution_negative", [bool(re.search(r'\b(?:mysql_query|mysqli_query|session_start|include|require)\s*\(', query)),
          query.count('$query[0] ='), bool(re.search(r'\$query\[[1-9]', query))], [False, 1, False],
          [evidence(QUERY, 1, 52), evidence(QUERY, 430, 438), evidence(PAGE, 85, 87)], source_limit)
    check("RP-29", "guard_dedup", 'isset($_SESSION[\'idtransportista\'])' in blobs["index_archivos/permisos.php"] and
          not re.search(r'\b(?:exit|die)\b', blobs["index_archivos/permisos.php"]), True,
          [evidence("index_archivos/permisos.php", 1, 27)], "SEC-005 previo; no se ejecuta la rama ni se analiza su salida al navegador.")
    check("RP-30", "menu_access_contract", 'getPermisos($_SESSION["idusuarioaccesoproveedor"],8)' in blobs["index_archivos/menu.php"] and
          "getPermisos" not in page + query and page.index('include("../menu.php")') > page.index('include("../data.php")'), True,
          [evidence("index_archivos/menu.php", 60, 67), evidence("index_archivos/MenuClass.php", 25, 42), evidence(PAGE, 85, 87), evidence(PAGE, 221, 222)],
          "Solo contrato de acceso: permisos cargados/ruta real desconocidos; no navegación ni visibilidad auditadas.")
    check("RP-31", "timezone_contract", "date_default_timezone_set('America/La_Paz')" in page and
          "date_default_timezone_set('America/Lima')" in blobs["index_archivos/cnfdb105.php"], True,
          [evidence(PAGE, 4), evidence("index_archivos/cnfdb105.php", 11)],
          "Herencia P95; no decide política horaria ni datos en el cambio de día.")
    # Bind each Python witness to exact source operations, not just similar names.
    date_assignment = next(l.strip() for l in query.splitlines() if l.strip().startswith('$fechafiltro_sql = " AND DATE'))
    expected_date_assignment = '''$fechafiltro_sql = " AND DATE(p.created_at) BETWEEN '".$fecha1a[2]."-".$fecha1a[1]."-".$fecha1a[0]."' AND '".$fecha2a[2]."-".$fecha2a[1]."-".$fecha2a[0]."'";'''
    check("RP-32", "witness_source_binding", date_assignment, expected_date_assignment,
          [evidence(QUERY, 45, 50)], "La traducción del testigo corresponde literalmente a los operandos/orden de la concatenación PHP; no evalúa PHP.")
    check("RP-33", "witness_source_binding", all(s in query for s in [
          "MAX(lp.embarque_id) AS embarque_id", "MAX(embarque_id) AS embarque_id",
          "DATE_FORMAT(MAX(embarque_fecha_creacion), '%d/%m/%Y')", "MAX(numero_viaje) AS numero_viaje",
          "MAX(app_tracking) AS app_tracking", "MAX(CASE WHEN tipo_inventario_id = 1 THEN estado END)",
          "MAX(CASE WHEN tipo_inventario_id = 2 THEN estado END)", "MAX(estadodos)",
          "COALESCE(te.embarque_id, mdos.embarque_id, tc.embarque_id)",
          "IF(m.chasis IS NULL, 1, 0) AS pendiente"]), True,
          [evidence(QUERY, 210, 220), evidence(QUERY, 292, 310), evidence(QUERY, 393, 413)], source_limit)
    check("RP-34", "deletion_negative_control", [
          "p.deleted_at IS NULL" in query, "AND d.deleted_at IS NULL" in query,
          "WHERE tav.deleted_at IS NULL" in query,
          "AND ip.deleted_at IS NULL" in query,
          "AND le.deleted_at IS NULL" in query[query.index("  LEFT JOIN logis_embarques le ON le.id ="):]],
          [True, True, True, True, False], [evidence(QUERY, 262, 269), evidence(QUERY, 328, 382)],
          "No se atribuye ausencia universal de soft-delete: p/d/ip/viaje sí tienen controles; el le externo no.")
    def id_filter(value):
        # Model only ASCII strings used by these fixtures, matching trim+ctype_digit.
        stripped = value.strip(" \t\n\r\0\x0b")
        return int(stripped) if re.fullmatch(r"[0-9]+", stripped) else None
    check("RP-35", "id_filter_negative_controls", [id_filter(v) for v in ["17", " 17 ", "", "-1", "17x", "17 OR 1=1"]],
          [17, 17, None, None, None, None], [evidence(QUERY, 23, 31)],
          "Modelo solo ASCII dentro del rango entero; inválido omite filtro, no significa rechazo de petición ni ampliación fuera del proveedor.")
    check("RP-36", "provider_and_optional_filter_matrix", [
          {"requested_name": name, "ids": [r["id"] for r in [
              {"id": 1, "owner": 41, "name": "SYN-A"},
              {"id": 2, "owner": 82, "name": "SYN-B"}]
              if r["owner"] == 41 and (name == "" or r["name"] == name)]}
          for name in ["", "SYN-A", "SYN-B"]],
          [{"requested_name": "", "ids": [1]}, {"requested_name": "SYN-A", "ids": [1]},
           {"requested_name": "SYN-B", "ids": []}], [evidence(QUERY, 3, 6), evidence(QUERY, 381, 383)],
          model_limit + " Con sintaxis no alterada, el filtro transportista se añade con AND y no reemplaza la identidad de sesión.")

    by_id = {c["id"]: c for c in cases}
    items = []

    def item(number, classification, title, statement, status, risk, tobe, ev, tests, limits, dedup, change):
        items.append({"id": f"TEMP-PH{number:03}", "classification": classification, "title": title,
                      "statement": statement, "source_status": status, "risk": risk, "tobe": tobe,
                      "evidence": ev, "tests": [{"id": t, "status": by_id[t]["status"]} for t in tests],
                      "limits": limits, "dedup": dedup, "change_vs_P95": change,
                      "production_status": "UNVERIFIED", "canonical": False})

    item(1, "improvement", "HEAD sustituye ámbito de concesionario por proveedor de cabecera",
         "P95 exige tc.idconcesionario igual al ID de sesión; HEAD exige p.proveedor_id igual a un entero obtenido en el caller. No son predicados equivalentes: HEAD admite cabeceras propias sin concesionario y excluye cabeceras de otros proveedores aunque su concesionario coincida. El SELECT auxiliar de transportistas adopta el mismo proveedor. Los demás bloques del query son idénticos tras esa sustitución exacta.",
         "SOURCE", "La mejora de aislamiento de cabecera no acredita autorización de todos los roles ni de las relaciones anexas.",
         "Documentar separadamente identidad de proveedor y concesionario y su población autorizada antes de integrar el delta.",
         [evidence(PAGE, 6, 9), evidence(PAGE, 52, 59), evidence(QUERY, 381, 391), evidence(QUERY, 381, 390, P95)],
         ["RP-01", "RP-02", "RP-03", "RP-04", "RP-36"], [source_limit, "M carece de ambos reportes; no es una regresión respecto de un reporte M."],
         {"related": ["IMP-SCOPE-001", "knowledge/variants/peru.md"], "decision": "Actualiza solo estos dos PHP respecto de P95; no audita el tercer JS ni reemplaza los documentos previos."}, "changed")
    item(2, "new_finding", "El ID genérico de proveedor se usa como transportista sin discriminar tipo7",
         "El login guarda idproveedor en idtransportista junto con idtipoproveedor. UserFinder resuelve tipo7 contra cn_concesionario. El reporte no consulta el tipo ni permisos de módulo antes del query y HEAD aplica p.proveedor_id al mismo número para todos. Si una cuenta tipo7 alcanza esta ruta, pierde el ámbito de concesionario de P95 y puede coincidir con el número de un transportista distinto; el cast no resuelve ese cruce de dominios. El menú de Reportes obtiene enlaces del grupo8 por cuenta, pero no demuestra qué cuentas tienen este reporte.",
         "KNOWNDEFECT", "Pérdida de filas o asociación con cabeceras de otro dominio si existen acceso efectivo y colisión numérica. No se afirma acceso real de tipo7 ni que deba conservarse una política concreta de P95.",
         "Definir roles admitidos y resolver el identificador con su dominio; denegar explícitamente roles no admitidos o aplicar el alcance de concesionario aprobado.",
         [evidence("index_archivos/veriflogin.php", 85, 91), evidence("src/core/users/application/Find/UserFind.php", 19, 35),
          evidence("src/core/users/application/Find/UserFind.php", 58, 63), evidence(PAGE, 2, 9), evidence(QUERY, 328, 382), evidence("index_archivos/menu.php", 60, 67)],
         ["RP-05", "RP-06", "RP-30"], ["Acceso, catálogos de permisos, unicidad entre tablas e identidades reales sin verificar."],
         {"related": ["knowledge/variants/peru.md: País y perfiles", "knowledge/general/actors-and-permissions.md", "SEC-005"],
          "decision": "El soporte previo de tipo7 y la guardia genérica no describen el efecto del nuevo predicado en este reporte; hallazgo nuevo de revisión, condicionado a acceso y dominio."}, "changed_role_effect")
    item(3, "new_finding", "El filtro de fechas puede alterar el predicado que acota al proveedor",
         "POST fecha1/fecha2 se divide por '/' y concatena sin escape ni validación en BETWEEN. fechafiltro=1 y dos valores no vacíos habilitan el fragmento. Un segmento con comilla y OR sale del literal y entra después de p.proveedor_id y los otros AND, pudiendo convertirlos en una alternativa booleana. El cast de sesión protege solo su operando, no el WHERE completo. La cadena llega a data.php mediante query[0].",
         "KNOWNDEFECT", "Lectura fuera del proveedor si el parser, runtime, conexión y acceso permiten la consulta alterada. Sin prueba de explotación, datos, privilegios, sentencias múltiples ni SQL ejecutado.",
         "Validar fechas completas con calendario y formato explícitos, enlazarlas como parámetros y mantener autorización en una consulta construida exclusivamente en servidor.",
         [evidence(PAGE, 29, 40), evidence(PAGE, 85, 87), evidence(QUERY, 45, 50), evidence(QUERY, 381, 391), evidence("index_archivos/data.php", 11, 14)],
         ["RP-08", "RP-09", "RP-10", "RP-11", "RP-12", "RP-32"], ["Testigo de construcción y precedencia; no parser MySQL ni alcance anónimo demostrados."],
         {"related": ["SEC-006", "source-audits/api/api-deep-iterative/API_DEEP_ITERATIVE_FINDINGS.md: reportepreembarquenacional"],
          "decision": "Misma familia de interpolación de SEC-006, nueva cadena concreta no cubierta por sus cuatro sinks; el inventario histórico solo marcaba RAW_SQL_SIGNAL. Se aporta el efecto sobre el límite de proveedor, sin contar otra vulnerabilidad genérica."}, "inherited_P95_new_owner_boundary_consequence")
    item(4, "new_finding", "Las relaciones por chasis pueden atravesar el alcance de cabecera",
         "HEAD acota p, pero tmp_embarques y tmp_concesionario agrupan globalmente por chasis y mdos se enlaza solo por chasis. tmp_embarques toma MAX(embarque_id) sin deleted_at de pedido/detalle. El le externo no filtra deleted_at. Un VIN reutilizado puede aportar embarque, concesionario o movimiento local2 de otra relación y cambiar estadodos. COALESCE da prioridad a te sobre mdos y tc, aun cuando otra relación sea más pertinente. El filtro de embarque usa esa misma resolución. Esto no equivale a sustituir la cabecera p por otra.",
         "KNOWNDEFECT", "Decoración o estado asociados al embarque equivocado si hay VIN compartidos/reutilizados o filas borradas que sigan candidatas; constraints efectivos desconocidos.",
         "Resolver relaciones con clave de preembarque/pedido/propietario autorizada, definir unicidad y borrados lógicos y rechazar ambigüedad en vez de elegir máximos globales.",
         [evidence(QUERY, 28, 30), evidence(QUERY, 166, 261), evidence(QUERY, 299, 310), evidence(QUERY, 364, 382)],
         ["RP-15", "RP-16", "RP-17", "RP-18", "RP-19", "RP-34"], ["Sin DDL autorizado ni prueba de VIN duplicados. Los movimientos m/mtres sí conservan pre_embarque_id y tipo; no se generaliza el defecto a todas las CTE."],
         {"related": ["knowledge/variants/peru.md", "source-audits/brownfield/reports/process_maps/components/8dc5c196467d.md"],
          "decision": "El mapa histórico inventaría nombres de CTE, no su clave ni este contraejemplo. No duplicado del cruce de identidad de TEMP-PH002 ni de SQLi."}, "inherited_P95")
    item(5, "new_finding", "Los MAX independientes no conservan una fila coherente de embarque y viaje",
         "Con te/tc sin embarque y mdos con dos embarques para el mismo chasis, base puede producir dos relaciones. La agregación final toma por separado MAX de embarque_id, fecha, numero_viaje y app_tracking; puede formar un registro que no perteneció a ninguna relación. tmp_viaje elige MAX(id) activo por embarque, no orden temporal. El MAX textual de app_tracking no demuestra el estado del viaje numéricamente máximo.",
         "KNOWNDEFECT", "Asociación interna incoherente si base contiene varias relaciones por grupo; no depende de ataque ni de que falle SQL.",
         "Definir cuál relación gobierna el informe y seleccionar su fila completa con desempate explícito; no usar máximos independientes como sustituto de selección de fila.",
         [evidence(QUERY, 262, 269), evidence(QUERY, 310, 320), evidence(QUERY, 370, 380), evidence(QUERY, 393, 428)],
         ["RP-20", "RP-21", "RP-33"], ["Caso condicionado a multiplicidad; con una sola relación no hay mezcla. No se presupone orden de collation, equivalencia de ID con fecha o política del viaje correcto."],
         {"related": ["TEMP-PH004", "knowledge/general/operational-findings.json"],
          "decision": "TEMP-PH004 trata pertenencia; aquí incluso relaciones del mismo proveedor producen una tupla imposible por agregación. No se encontró este mecanismo en el registro previo."}, "inherited_P95")
    item(6, "improvement", "Estado y tipo filtran la población antes del pivote de inventarios",
         "Los aliases de filtros pertenecen a base. tipos_inventario aporta solo1/2; cualquier tipo positivo distinto genera cero filas, no selecciona el estado3 derivado. estado1/2 filtra presencia de m por fila de tipo antes de los MAX CASE: un vehículo con tipo1 pendiente y tipo2 realizado conserva solo la primera fila al pedir estado1, y la columna tipo2 queda NULL. El campo inventario3 se deriva de local2 o preembarque3, sin unificar esos dominios.",
         "SOURCE", "Una interpretación de filtros como selección de vehículo conservando todas sus columnas sería distinta de lo implementado; no se declara esa interpretación requisito aprobado.",
         "Documentar el alcance por fila/tipo; si negocio pide filtrar vehículos conservando inventarios, evaluar ese predicado después del pivote.",
         [evidence(QUERY, 33, 57), evidence(QUERY, 158, 174), evidence(QUERY, 299, 305), evidence(QUERY, 386, 387), evidence(QUERY, 411, 413)],
         ["RP-13", "RP-14", "RP-22", "RP-23", "RP-33", "RP-35"], ["No se simulan controles del navegador ni se decide la política de filtros; un POST no numérico para IDs se ignora en vez de producir error."],
         {"related": ["VAR-001", "knowledge/variants/peru.md"], "decision": "VAR-001 es contador/filtro del consumidor JS; este contrato SQL de tipos/población es distinto. Mejora de precisión, no nuevo defecto de completitud aprobado."}, "inherited_P95")
    item(7, "improvement", "Realizado significa existencia de un registro, no completitud demostrada",
         "m une accesorios, partes, contaminaciones y parámetros activos con UNION por preembarque/chasis/tipo. Una sola fila de cualquiera basta para estado Realizado; no se exige cubrir todas las secciones ni ausencia de faltantes. estadodos usa presencia de local2 o preembarque3. Los flags de faltante/desperfecto/contaminación y kilometraje se calculan en base pero no forman parte de la proyección final. El nombre Nacional no añade por sí solo un predicado de tipo de viaje.",
         "SOURCE", "Sobreinterpretar el alias como inspección completa o universo nacional validado carece de respaldo en estos predicados.",
         "Mantener los alias como etiquetas de fuente y pedir definición de completitud/población antes de convertirlos en reglas de negocio.",
         [evidence(QUERY, 59, 164), evidence(QUERY, 288, 310), evidence(QUERY, 328, 391), evidence(QUERY, 393, 428)],
         ["RP-19", "RP-24"], ["No se afirma que presencia sea una regla incorrecta; no hay contrato de completitud ni catálogo nacional validado."],
         {"related": ["VAR-001", "knowledge/glossary/review-register.md"], "decision": "No reutiliza semántica del contador pendiente del JS ni promueve los nombres del SQL a glosario canónico."}, "inherited_P95")
    item(8, "improvement", "La cadena local no distingue todos los fallos del reporte",
         "cnfdb105 se incluye antes de permisos y depende de .env.php/autoload externos al árbol. Con accion=ge se incluye contador.php, ausente del árbol fijado. Los SELECT auxiliares de transportistas y destinos se intentan antes del include condicional del constructor; destinos conserva población global sin proveedor. No comprueban false antes de fetch. El constructor solo prepara query[0]; data.php ejecuta su principal sin comprobar el retorno antes de fetch, a diferencia de su rama auxiliar con die. No se atribuye divulgación al navegador ni continuación universal ante errores.",
         "SOURCE", "Fallo de conexión/include/query puede abortar o producir diagnósticos según runtime; no hay contrato de fallo de informe explícito ni prueba de que resultado vacío equivalga a consulta exitosa.",
         "Comprobar identidad antes de trabajo dependiente, revisar dependencias opcionales, acotar o retirar lecturas auxiliares innecesarias y distinguir fallo SQL de resultado vacío de forma terminal y controlada.",
         [evidence(PAGE, 2, 3), evidence(PAGE, 29, 87), evidence("index_archivos/cnfdb105.php", 2, 3), evidence("index_archivos/cnfdb105.php", 13, 24), evidence("index_archivos/data.php", 6, 14)],
         ["RP-25", "RP-26", "RP-27", "RP-28", "RP-31"], ["No se abren .env, vendor o datos reales. Dependencias/versiones/errores personalizados de despliegue desconocidos. No se presenta ausencia del árbol como fallo demostrado del despliegue. La divergencia La_Paz/Lima es heredada."],
         {"related": ["RN-47", "knowledge/general/architecture.md", "knowledge/variants/peru.md"], "decision": "Amplía el contrato local de ejecución/fallo; no repite el exportador SEC-015 ni afirma un nuevo fallo productivo."}, "inherited_except_aux_transportista_scope")
    item(9, "duplicate_or_rejected", "No recontar la guardia ni declarar que fallback0 deniega siempre",
         "La guardia compartida comprueba isset(idtransportista), sin rol/módulo ni terminación explícita. Su constante datoconservar mantiene el límite de runtime documentado en SEC-005. HEAD sustituye ausencia por0, pero igualdad con proveedor0 no es denegación incondicional: depende de que no existan esas filas. No se declara alcance anónimo, ejecución de handler ni denegación garantizada. La consulta del menú no añade retrospectivamente autorización al query ya construido/ejecutado.",
         "KNOWNDEFECT", "Riesgo heredado y dependiente de runtime/datos; no nuevo hallazgo contabilizado.",
         "Reutilizar SEC-005 para corrección de guardia; requerir ID válido y denegación explícita antes del reporte y definir permisos de ruta en servidor.",
         [evidence("index_archivos/permisos.php", 1, 27), evidence(PAGE, 2, 9), evidence(PAGE, 85, 87), evidence(PAGE, 221, 222), evidence("index_archivos/MenuClass.php", 25, 42)],
         ["RP-07", "RP-29", "RP-30"], ["No PHP ejecutado; no inferencia de bypass anónimo en PHP8 ni existencia de proveedor0."],
         {"related": ["SEC-005", "knowledge/general/actors-and-permissions.md"], "decision": "Duplicado del defecto compartido; se rechazan las generalizaciones sobre anonimato y fail-closed por0."}, "guard_inherited_fallback_changed")
    item(10, "improvement", "Corregir el candidato histórico: query.php es constructor, no ejecutor autónomo",
         "El catálogo histórico clasificó query.php como candidato public_php_page GET y no halló callers. La lectura completa del blob muestra construcción de filtros/query[0]/metadatos sin include, session_start ni mysql_query. El caller real es el reporte, bajo accion=ge, seguido de data.php. Sin ese contexto faltan identidad, filtros y conexión; no se concluye que una petición directa ejecute la consulta. Todos los aliases de los fragmentos sí existen en base; tampoco se acredita compilación SQL, soporte de CTE ni sintaxis de ejecución por esa comprobación.",
         "SOURCE", "Contar el constructor como endpoint SQL ejecutable sobrestima la superficie probada.",
         "Registrar la dependencia caller→constructor→data.php y mantener accesibilidad/runtime como no verificados.",
         [evidence(QUERY, 1, 52), evidence(QUERY, 430, 438), evidence(PAGE, 85, 87), evidence("index_archivos/data.php", 11, 14)],
         ["RP-13", "RP-28"], ["No petición directa, bootstrap, handler ni parser PHP/SQL ejecutados. Ninguna conclusión sobre salidas al navegador."],
         {"related": ["source-audits/api/asgard-api-audit-augmented/api-catalog.augmented.json: aug_ce1a5a0f133b5b07c241"],
          "decision": "Corrección del inventario histórico de candidatos, no nueva vulnerabilidad de acceso directo."}, "builder_inherited_new_context_variable")

    # Validate every source citation against the immutable local blobs (including old lines).
    for x in items:
        for ev in x["evidence"]:
            body = blobs[ev["path"]] if ev["commit"] == HEAD else old[ev["path"]]
            if not 1 <= ev["line_start"] <= ev["line_end"] <= len(body.splitlines()):
                raise ValueError(f"Invalid evidence range in {x['id']}")
    if any(c["status"] != "pass" for c in cases):
        raise AssertionError(json.dumps([c for c in cases if c["status"] != "pass"], ensure_ascii=False))

    provenance = {"audit_date": "2026-11-19", "timezone": "Europe/Madrid", "date_authority": "user",
                  "source_root": str(source), "source_commit": HEAD, "previous_peru_commit": P95,
                  "historical_master_commit": M, "knowledge_baseline_commit": KB,
                  "canonical": False, "production_status": "UNVERIFIED"}
    boundaries = {"application_entrypoints_executed": False, "php_executed": False, "bootstrap_executed": False,
                  "sql_executed": False, "database_access": False, "network_access": False, "real_rows_used": False,
                  "browser_output_or_navigation_reviewed": False, "deployment_emulated": False,
                  "remote_refs_consulted": False, "new_master_a44_reviewed": False,
                  "source_modified": False, "main_manifest_or_docs_modified": False,
                  "commits_or_pushes": False, "third_changed_JS_reviewed": False}
    inventory = []
    for p, body in blobs.items():
        inventory.append({"commit": HEAD, "path": p, "blob": git(source, "rev-parse", f"{HEAD}:{p}").decode().strip(),
                          "normalized_sha256": hashlib.sha256(body.encode()).hexdigest(), "lines": len(body.splitlines()),
                          "purpose": "primary" if p in [PAGE, QUERY] else "include_identity_or_access_contract_only"})
    counts = {k: sum(x["classification"] == k for x in items)
              for k in ["new_finding", "improvement", "duplicate_or_rejected"]}
    shared = {"schema_version": 1, **provenance, "boundaries": boundaries,
              "limits": [source_limit, model_limit, "SOURCE/KNOWNDEFECT describe fuente; RISK es condicionado; TOBE es propuesta no aprobada.",
                         "Sin promoción canónica ni actualización de manifest/docs. No se reintenta el alcance navegador/navegación excluido."],
              "counts": counts, "items": items}
    probe_report = {**shared, "technique": "pinned_text_extraction_and_python_predicate_relational_witnesses",
                    "source_inventory": inventory, "cases": cases, "passed": len(cases), "total": len(cases)}
    review = {**shared, "probe_artifact": PROBES, "reproduction_script": "scripts/audit/peru_head_report_probes.py",
              "dedup_sources": ["knowledge/variants/peru.md", "knowledge/general/actors-and-permissions.md",
                                "knowledge/general/security-findings.json", "knowledge/general/operational-findings.json",
                                "knowledge/reviews/iterative-20261118/accepted-deltas.json",
                                "knowledge/reviews/iterative-20261118/report-query-contract.md",
                                "source-audits/api/api-deep-iterative/API_DEEP_ITERATIVE_FINDINGS.md",
                                "source-audits/api/asgard-api-audit-augmented/api-catalog.augmented.json",
                                "source-audits/brownfield/reports/process_maps/components/8dc5c196467d.md"],
              "change_summary": {"two_report_files_absent_in_M": True,
                                 "query_change_only_owner_predicate": True,
                                 "query_execution_owner": "index_archivos/data.php:13",
                                 "date_filter_alias": "p.created_at",
                                 "concesionario_filter_alias": "d.destino (texto), no tc.idconcesionario",
                                 "national_population_predicate": "No hay predicado explícito que valide tipo nacional en este query"}}
    md = ["# Revisión acotada Perú HEAD — reportes", "",
          "19 de noviembre de 2026, Europe/Madrid; fecha proporcionada por el usuario. No canónico.", "",
          f"HEAD `{HEAD}`; P95 `{P95}`; M histórico `{M}`; KB `{KB}`.", "",
          "Se registran **4 hallazgos nuevos de revisión**, **5 mejoras** y **1 duplicado/rechazado**. Solo el cruce de identidad por rol depende del cambio funcional nuevo; los demás defectos nuevos para la KB se heredan de P95. No significa cuatro regresiones introducidas en HEAD.", "",
          f"Validación: **{len(cases)}/{len(cases)}** comprobaciones de texto, predicados y relaciones sintéticas. [Resultados](../../../{PROBES}) y [script](../../../scripts/audit/peru_head_report_probes.py). Ningún PHP, handler, include, SQL, DB, red o dato real ejecutado; sin emular despliegue. Sin revisión de salidas al navegador/navegación ni del nuevo master a44.", "",
          "## Contrato y población", "",
          "Cadena relevante: reporte → cnfdb105 (solo inspeccionado; depende de .env/autoload) → permisos → identidad/filtros; accion=ge incluye contador (ausente del árbol), después constructor query → data.php. El menú de Reportes usa grupo8 por cuenta y se incluye después de data.php; no demuestra autorización del handler. El constructor aislado no ejecuta SQL.", "",
          "HEAD exige proveedor de cabecera; P95 exigía concesionario derivado. No basta con llamar transportista a la variable de sesión: el login la alimenta con idproveedor, incluido el dominio de tipo7. Los filtros opcionales acotan aliases existentes de base; fechas tiene una frontera de sintaxis sin protección. La cardinalidad y pertenencia de relaciones por chasis no quedan garantizadas por el filtro de cabecera.", "",
          "SOURCE registra comportamiento; KNOWNDEFECT registra un defecto de fuente con precondiciones. RISK no afirma impacto productivo. TOBE propone una corrección o definición pendiente, sin aprobación ni modificación de aplicación."]
    for x in items:
        md.extend(["", f"## {x['id']} — {x['title']}", "", f"`{x['classification']}` · `{x['source_status']}` · frente a P95: `{x['change_vs_P95']}`.", "",
                   x["statement"], "", "**RISK:** " + x["risk"], "", "**TOBE:** " + x["tobe"], "", "**Evidencia:** " + "; ".join(
                       f"`{e['commit']}:{e['path']}:L{e['line_start']}-L{e['line_end']}`" for e in x["evidence"]), "",
                   "**Pruebas:** " + ", ".join(t["id"] for t in x["tests"]) + ".", "",
                   "**Límites:** " + " ".join(x["limits"]), "", "**Dedup:** " + x["dedup"]["decision"] + " Referencias: " + "; ".join(x["dedup"]["related"]) + "."])
    md.extend(["", "## Controles negativos y exclusiones", "",
               "RP-04/06 conservan los casos de identidad correcta y muestran la diferencia de poblaciones. RP-07 impide equiparar fallback0 a denegación. RP-10/12 no generalizan el problema de fechas a filtros desactivados o a los cuatro valores escapados. RP-13/14 verifican aliases y guardas de ID; no compilan SQL. RP-18/19 separan VIN distinto y claves compuestas de las uniones débiles. RP-21 elimina la mezcla con relación única. RP-22/23 muestran la exclusión de tipo3 y el efecto del filtro previo al pivote. RP-28 rechaza ejecución SQL directa por el constructor. RP-29/30 deduplican guardia y separan permisos de menú del control de servidor. RP-32/33 vinculan testigos a las concatenaciones y agregados exactos. RP-34 conserva controles de soft-delete existentes; RP-35 muestra IDs inválidos sin atribuirles inyección; RP-36 demuestra que el filtro de nombre no reemplaza por sí solo el proveedor de sesión.", "",
               "No se revisa exportador, transporte de SQL al navegador, renderizado, recursos de cliente ni navegación; SEC-015 permanece como antecedente fuera de esta revisión. No se ejecuta ninguna prueba histórica que invoque PHP. Los resultados no certifican soporte de CTE, versión MySQL/PHP, privilegios, datos, unicidad, política de completitud o despliegue.", "",
               "Reproducir: `python scripts/audit/peru_head_report_probes.py --source C:/repos/proveedores-peru-head-review-20261119 --knowledge C:/repos/asgard-proveedores-knowledge`. Solo escribe los tres sidecars autorizados; no cambia fuente, manifest, documentos principales, commits ni ramas.", ""])
    outputs = {PROBES: json.dumps(probe_report, ensure_ascii=False, indent=2) + "\n",
               DELTAS: json.dumps(review, ensure_ascii=False, indent=2) + "\n", MARKDOWN: "\n".join(md)}
    for rel, body in outputs.items():
        target = knowledge / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    print(json.dumps({"passed": len(cases), "total": len(cases), "counts": counts, "outputs": list(outputs)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
