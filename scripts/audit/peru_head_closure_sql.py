"""Peru phase-2 closure: SQLglot MySQL AST and finite, benign metamorphic checks.

Only parses SQL and evaluates a restricted set of AST expressions over synthetic
bindings/groups. Never executes SQL, PHP, handlers, bootstrap, HTTP, or a database.
No adversarial input strings or operational attack queries are constructed.
Writes only the three closure-sql sidecars explicitly authorized by the user.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True

HEAD = "2a179e2e6472d5705d031665ecbc90c3d806edec"
P95 = "95fe9a4c3b3cddd84be922cc0e1eb9c88603df62"
M = "a8ce2c23dead8552d2c4699e4a9b9134f7a18707"
KB = "0c4bb99f076d6a8c18ae98375d6e154da6319922"
PAGE = "index_archivos/reportes/reportepreembarquenacional.php"
QUERY = "index_archivos/reportes/reportepreembarquenacionalquery.php"
VERSION = "30.33.0"
OUTPUTS = ("source-audits/peru/2026-11-19/closure-sql.json",
           "knowledge/reviews/peru-head-20261119/closure-sql.json",
           "knowledge/reviews/peru-head-20261119/closure-sql.md")
FINDINGS = {"PH-001": "TEMP-PH002", "PH-002": "TEMP-PH003",
            "PH-003": "TEMP-PH004", "PH-004": "TEMP-PH005"}
IMPROVEMENTS = {"PH-IMP001": "TEMP-PH001", "PH-IMP002": "TEMP-PH006",
                "PH-IMP003": "TEMP-PH007", "PH-IMP004": "TEMP-PH008",
                "PH-IMP005": "TEMP-PH010"}


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def digest(value):
    return hashlib.sha256(value).hexdigest()


def ev(path, start, end=None, commit=HEAD):
    return {"commit": commit, "path": path, "line_start": start, "line_end": end or start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="C:/repos/proveedores-peru-head-review-20261119")
    parser.add_argument("--knowledge", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--sqlglot", default="C:/repos/audit-tools-proveedores-sqlglot-20261118")
    args = parser.parse_args()
    source, knowledge, package = (Path(p).resolve() for p in (args.source, args.knowledge, args.sqlglot))
    if source == knowledge or source in knowledge.parents or knowledge in source.parents:
        raise ValueError("Separate source/knowledge repositories required")
    if git(source, "rev-parse", "HEAD").decode().strip() != HEAD:
        raise ValueError("Unexpected source pin")
    git(knowledge, "cat-file", "-e", KB + "^{commit}")
    sys.path.insert(0, str(package))
    import sqlglot
    from sqlglot import exp
    from sqlglot.optimizer.scope import build_scope
    if sqlglot.__version__ != VERSION or not Path(sqlglot.__file__).resolve().is_relative_to(package):
        raise ValueError("Expected isolated SQLglot 30.33.0")

    phase1_path = knowledge / "knowledge/reviews/peru-head-20261119/report-deltas.json"
    phase1_raw = phase1_path.read_bytes()
    phase1 = json.loads(phase1_raw)
    if phase1["source_commit"] != HEAD or phase1["previous_peru_commit"] != P95:
        raise ValueError("Unexpected phase-1 pins")
    old_items = {x["id"]: x for x in phase1["items"]}
    read_paths = [PAGE, QUERY, "index_archivos/data.php", "index_archivos/veriflogin.php",
                  "src/core/users/application/Find/UserFind.php"]
    raw = {p: git(source, "show", f"{HEAD}:{p}") for p in read_paths}
    text = {p: v.decode("utf-8-sig").replace("\r\n", "\n") for p, v in raw.items()}
    old_query = git(source, "show", f"{P95}:{QUERY}").decode("utf-8-sig").replace("\r\n", "\n")
    for path, content in text.items():
        if (source / path).read_text(encoding="utf-8-sig").replace("\r\n", "\n") != content:
            raise ValueError(f"Worktree differs from pinned blob: {path}")

    # The only interpolation substitutions are a symbolic scalar ID and benign
    # optional predicate fragments. No PHP code or external input is evaluated.
    slots = {"filtrotransportista", "filtromarca", "filtroconcesionario", "filtrotipoinventario",
             "filtroestado", "filtrovin", "filtropreembarque", "filtroembarque", "fechafiltro_sql"}

    def extract(php, previous=False, filters=None):
        matches = list(re.finditer(r'\$query\[0\]\s*=\s*"(WITH[\s\S]*?)";', php))
        if len(matches) != 1:
            raise ValueError("Expected one isolated WITH query assignment")
        sql = matches[0].group(1)
        token = '\".$_SESSION[\'idtransportista\'].\"' if previous else '\".$idTransportistaSesion.\"'
        if sql.count(token) != 1:
            raise ValueError("Unexpected scalar interpolation")
        sql = sql.replace(token, ":session_provider")
        found = set(re.findall(r"\$(\w+)", sql))
        if found != slots:
            raise ValueError("Unexpected interpolated variables")
        filters = filters or {}
        if not set(filters) <= slots:
            raise ValueError("Unexpected filter")
        sql = re.sub(r"\$(\w+)", lambda m: filters.get(m.group(1), ""), sql)
        if "$" in sql or '\".' in sql or '.\"' in sql:
            raise ValueError("Unresolved PHP interpolation")
        statements = sqlglot.parse(sql, read="mysql", error_level=sqlglot.ErrorLevel.RAISE)
        if len(statements) != 1 or not isinstance(statements[0], exp.Select):
            raise ValueError("Expected one SELECT, not executable command batches")
        return sql, statements[0]

    def ctes(tree):
        return {c.alias_or_name: c.this for c in tree.find_all(exp.CTE)}

    def expression(sql):
        return sqlglot.parse_one(sql, read="mysql")

    def rendered(node):
        return node.sql(dialect="mysql")

    def conjuncts(node):
        if isinstance(node, (exp.Where, exp.Paren)):
            return conjuncts(node.this)
        if isinstance(node, exp.And):
            return conjuncts(node.this) + conjuncts(node.expression)
        return [node]

    def scalar(node, bindings):
        """Finite expression interpreter, not a SQL/query evaluator.

        SQL NULL truth tables are explicit. All other syntax fails closed as
        unsupported; no code generation, eval, engine, connection, or I/O here.
        """
        if isinstance(node, (exp.Alias, exp.Where, exp.Paren)):
            return scalar(node.this, bindings)
        if isinstance(node, exp.Column):
            return bindings[(node.table + "." if node.table else "") + node.name]
        if isinstance(node, exp.Placeholder):
            return bindings[":" + node.name]
        if isinstance(node, exp.Null):
            return None
        if isinstance(node, exp.Boolean):
            return node.this
        if isinstance(node, exp.Literal):
            return node.this if node.is_string else int(node.this)
        if isinstance(node, (exp.And, exp.Or)):
            a, b = scalar(node.this, bindings), scalar(node.expression, bindings)
            if isinstance(node, exp.And):
                return False if a is False or b is False else (None if a is None or b is None else True)
            return True if a is True or b is True else (None if a is None or b is None else False)
        if isinstance(node, exp.Not):
            v = scalar(node.this, bindings)
            return None if v is None else not v
        if isinstance(node, exp.EQ):
            a, b = scalar(node.this, bindings), scalar(node.expression, bindings)
            return None if a is None or b is None else a == b
        if isinstance(node, exp.Is) and isinstance(node.expression, exp.Null):
            return scalar(node.this, bindings) is None
        if isinstance(node, exp.Case):
            for branch in node.args["ifs"]:
                if scalar(branch.this, bindings) is True:
                    return scalar(branch.args["true"], bindings)
            return scalar(node.args["default"], bindings) if node.args.get("default") is not None else None
        if isinstance(node, exp.If):
            key = "true" if scalar(node.this, bindings) is True else "false"
            return scalar(node.args[key], bindings)
        if isinstance(node, exp.Coalesce):
            for part in [node.this, *node.expressions]:
                result = scalar(part, bindings)
                if result is not None:
                    return result
            return None
        raise ValueError(f"Unsupported finite-expression syntax: {node.key}")

    def sql_max(argument, rows):
        values = [scalar(argument, row) for row in rows]
        values = [v for v in values if v is not None]
        return max(values) if values else None

    head_sql, tree = extract(text[QUERY])
    p95_sql, p95_tree = extract(old_query, previous=True)
    ct, old_ct = ctes(tree), ctes(p95_tree)
    base = ct["base"]
    checks = []

    def check(cid, title, ids, actual, expected, evidence, controls, limits):
        result = "pass" if actual == expected else "fail"
        checks.append({"id": cid, "title": title, "accepted_ids": ids, "status": "completed",
                       "result": result, "actual": actual, "expected": expected,
                       "evidence": evidence, "negative_controls": controls, "limits": limits})

    ast_limit = "AST MySQL de SQLglot; no valida servidor, esquema, tipos reales, optimizador, privilegios o despliegue."
    domain_limit = "Dominio sintético finito; no prueba ausencia/presencia de esos casos en datos ni constraints reales."
    qev = lambda a, b=None: [ev(QUERY, a, b)]
    scopes = list(build_scope(tree).traverse())
    unresolved = [c.sql(dialect="mysql") for s in scopes for c in s.columns if c.table and c.table not in s.sources]
    check("CS-01", "Consulta única y resolución local de aliases", ["PH-IMP005"],
          {"ctes": len(ct), "scopes": len(scopes), "unresolved_table_aliases": unresolved},
          {"ctes": 11, "scopes": 29, "unresolved_table_aliases": []}, qev(52, 432),
          "No se infiere que la existencia del alias pruebe columnas físicas o que query.php ejecute SQL.", ast_limit)

    owner = expression("p.proveedor_id = :session_provider")
    dealer = expression("tc.idconcesionario = :session_provider")
    check("CS-02", "Predicado HEAD y predicado P95 pertenecen a dominios distintos", ["PH-001", "PH-IMP001"],
          [owner in conjuncts(base.args["where"]), dealer in conjuncts(old_ct["base"].args["where"]),
           owner in conjuncts(old_ct["base"].args["where"]), dealer in conjuncts(base.args["where"])],
          [True, True, False, False], [ev(QUERY, 381, 391), ev(QUERY, 381, 390, P95)],
          "El predicado de concesionario no aparece como obligación adicional en HEAD.", ast_limit)
    same = p95_tree.copy()
    ctes(same)["base"].set("where", base.args["where"].copy())
    check("CS-03", "Igualdad AST fuera del cambio de WHERE", ["PH-IMP001"], same == tree, True,
          [ev(QUERY, 52, 432), ev(QUERY, 52, 431, P95)],
          "No extiende igualdad a runtime, datos ni al tercer JS cambiado.", ast_limit)

    # Every fragment is fixed and benign. Filters are never assembled from arbitrary input.
    benign = {"filtrotransportista": " AND tra.transportista = 'SYN-A'",
              "filtromarca": " AND d.marca LIKE '%SYN%'", "filtroconcesionario": " AND d.destino = 'SYN-D'",
              "filtrotipoinventario": " AND t.tipo_inventario_id = 1", "filtroestado": " AND m.chasis IS NULL",
              "filtrovin": " AND d.chasis LIKE '%SYN%'", "filtropreembarque": " AND p.id = 17",
              "filtroembarque": " AND COALESCE(te.embarque_id, mdos.embarque_id, tc.embarque_id) = 23",
              "fechafiltro_sql": " AND DATE(p.created_at) BETWEEN '2026-11-01' AND '2026-11-19'"}
    variants = []
    for name, filters in [("none", {}), *[(k, {k: v}) for k, v in benign.items()], ("all_benign", benign)]:
        _, variant = extract(text[QUERY], filters=filters)
        clause = ctes(variant)["base"].args["where"]
        variants.append({"name": name, "scope_is_mandatory_conjunct": owner in conjuncts(clause),
                         "top_level_terms": len(conjuncts(clause))})
    check("CS-04", "Filtros benignos conservan la conjunción obligatoria de proveedor", ["PH-002", "PH-IMP001", "PH-IMP002"],
          [v["scope_is_mandatory_conjunct"] for v in variants], [True] * len(variants), qev(381, 391),
          "No se genera ninguna entrada adversarial: la prueba no afirma que entradas arbitrarias mantengan esta propiedad.", ast_limit)

    # Boolean metamorphism uses abstract symbols only, never application SQL or payloads.
    safe = expression("scope_key = :scope AND sample_key = :sample")
    optional_marker = expression("marker_key = :marker")
    altered_shape = exp.or_(safe.copy(), optional_marker.copy())
    safe_terms = conjuncts(safe)
    variants_truth = []
    for scope_ok, sample_ok, marker_ok in itertools.product([False, True], repeat=3):
        binding = {"scope_key": 1 if scope_ok else 2, ":scope": 1, "sample_key": 1 if sample_ok else 2,
                   ":sample": 1, "marker_key": 1 if marker_ok else 2, ":marker": 1}
        variants_truth.append((scope_ok, scalar(safe, binding), scalar(altered_shape, binding)))
    check("CS-05", "El operador raíz determina si un scope sigue siendo obligatorio", ["PH-002"],
          {"and_has_scope_term": safe_terms[0] in conjuncts(safe),
           "or_has_mandatory_scope_term": safe_terms[0] in conjuncts(altered_shape),
           "and_accepts_false_scope": any(not a and b is True for a, b, c in variants_truth),
           "or_accepts_false_scope": any(not a and c is True for a, b, c in variants_truth)},
          {"and_has_scope_term": True, "or_has_mandatory_scope_term": False,
           "and_accepts_false_scope": False, "or_accepts_false_scope": True}, qev(45, 50) + qev(381, 391),
          "Control abstracto AND frente a OR; no consulta de ataque, concatenación maliciosa ni replay de RP-09.",
          "No acredita que un servidor acepte un texto de ataque; el riesgo de composición conserva la evidencia de PHP de fase1.")
    date_line = next(l.strip() for l in text[QUERY].splitlines() if l.strip().startswith('$fechafiltro_sql = " AND DATE'))
    check("CS-06", "La variante de fecha benigna no prueba parametrización del constructor", ["PH-002"],
          {"between_nodes": len(list(extract(text[QUERY], filters={"fechafiltro_sql": benign["fechafiltro_sql"]})[1].find_all(exp.Between))),
           "raw_array_components": all(x in date_line for x in ["$fecha1a[2]", "$fecha2a[2]", "$fecha1a[0]", "$fecha2a[0]"]),
           "escape_in_assignment": "mysql_real_escape_string" in date_line},
          {"between_nodes": 1, "raw_array_components": True, "escape_in_assignment": False}, qev(45, 50),
          "SQLglot recibe la instanciación segura, no ejecuta PHP ni demuestra validación de entradas no instanciadas.", ast_limit)

    # Identity-domain metamorphism: same scalar, different namespaces; policy remains external.
    numeric_key = expression("a_id = b_id")
    tagged_key = expression("a_id = b_id AND a_domain = b_domain")
    identity = {"a_id": 41, "b_id": 41, "a_domain": "CONCESIONARIO", "b_domain": "TRANSPORTISTA"}
    corrected_domain = {**identity, "b_domain": "CONCESIONARIO"}
    check("CS-07", "Igualdad numérica no equivale a identidad con dominio", ["PH-001"],
          [scalar(numeric_key, identity), scalar(tagged_key, identity), scalar(tagged_key, corrected_domain)],
          [True, False, True], [ev("index_archivos/veriflogin.php", 85, 91),
                                ev("src/core/users/application/Find/UserFind.php", 19, 35), ev(QUERY, 381, 382)],
          "Al igualar dominios desaparece la discrepancia. No se presume acceso efectivo de tipo7 ni una política de admisión aprobada.", domain_limit)
    owner_only_columns = sorted({(c.table + "." + c.name) for c in base.args["where"].find_all(exp.Column)})
    check("CS-08", "El WHERE no incorpora discriminador de rol", ["PH-001"], owner_only_columns,
          ["p.deleted_at", "p.proveedor_id"], qev(381, 391),
          "La presencia de ambos IDs en PHP no transforma el ID genérico en un ID tipado en SQL.",
          ast_limit + " La admisión PHP/ruta no se prueba con AST SQL.")

    joins = {j.this.alias_or_name: j for j in base.args["joins"]}
    weak_keys = {name: sorted(rendered(c) for c in joins[name].args["on"].find_all(exp.Column)) for name in ["mdos", "te", "tc"]}
    check("CS-09", "Las tres uniones débiles tienen solo clave chasis", ["PH-003"], weak_keys,
          {"mdos": ["d.chasis", "mdos.chasis"], "te": ["d.chasis", "te.chasis"], "tc": ["d.chasis", "tc.chasis"]},
          qev(370, 377), "m, mtres e ip no se incluyen en esta generalización.", ast_limit)
    local = {"d.chasis": "SYN-VIN", "mdos.chasis": "SYN-VIN", "foreign_scope": 82}
    changed_scope = {**local, "foreign_scope": 99}
    changed_vin = {**local, "mdos.chasis": "SYN-OTHER"}
    join_expr = joins["mdos"].args["on"]
    qualified_fixture = expression("a.vin = b.vin AND a.scope_key = b.scope_key")
    check("CS-10", "Mutar pertenencia no afecta una unión que solo mira chasis", ["PH-003"],
          [scalar(join_expr, local), scalar(join_expr, changed_scope), scalar(join_expr, changed_vin),
           scalar(qualified_fixture, {"a.vin": "SYN-VIN", "b.vin": "SYN-VIN", "a.scope_key": 41, "b.scope_key": 82})],
          [True, True, False, False], qev(370, 382),
          "Cambiar VIN elimina el match; una clave compuesta abstracta también lo elimina. No se propone una columna física inexistente como reparación.", domain_limit)
    correlated = joins["m"].args["on"]
    env = {"m.pre_embarque_id": 1, "d.pre_embarque_id": 1, "m.chasis": "SYN-VIN", "d.chasis": "SYN-VIN",
           "m.tipo_inventario_id": 1, "t.tipo_inventario_id": 1}
    check("CS-11", "El control correlacionado rechaza otro preembarque o tipo", ["PH-003", "PH-IMP003"],
          [scalar(correlated, env), scalar(correlated, {**env, "m.pre_embarque_id": 2}),
           scalar(correlated, {**env, "m.tipo_inventario_id": 2})], [True, False, False], qev(354, 362),
          "Evita afirmar que todas las CTE cruzan por VIN sin más claves.", domain_limit)
    te = ct["tmp_embarques"]
    check("CS-12", "El MAX de pedidos opera con agrupación global de chasis", ["PH-003"],
          {"group": [rendered(x) for x in te.args["group"].expressions],
           "where_columns": sorted(rendered(x) for x in te.args["where"].find_all(exp.Column)),
           "max_arguments": [rendered(x.this) for x in te.find_all(exp.Max)]},
          {"group": ["lpd.posicion"], "where_columns": ["lp.embarque_id", "lpd.posicion"],
           "max_arguments": ["lp.embarque_id"]}, qev(210, 220),
          "No se deriva aislamiento por proveedor de un GROUP BY sin tal clave; constraints reales desconocidos.", ast_limit)

    # Aggregation metamorphisms use the actual AST MAX arguments and GROUP BY keys.
    group_columns = [x.name for x in tree.args["group"].expressions]
    roots = {p.alias_or_name: p for p in tree.expressions}
    aggregate_args = {name: next(roots[name].find_all(exp.Max)).this for name in ["embarque_id", "numero_viaje", "embarque_fecha_creacion"]}
    common = {key: "SYN-GROUP" for key in group_columns}
    rows = [{**common, "embarque_id": 100, "numero_viaje": 900, "embarque_fecha_creacion": "2026-11-19"},
            {**common, "embarque_id": 200, "numero_viaje": 800, "embarque_fecha_creacion": "2026-11-18"}]
    aggregate = lambda rr: {key: sql_max(arg, rr) for key, arg in aggregate_args.items()}
    projection = lambda row: {key: row[key] for key in aggregate_args}
    group_key = lambda row: tuple(row[key] for key in group_columns)
    combined = aggregate(rows)
    check("CS-13", "Agregar una fila incomparable puede producir una tupla sin fila origen", ["PH-004"],
          {"same_group": group_key(rows[0]) == group_key(rows[1]), "one_row_coherent": aggregate(rows[:1]) == projection(rows[0]),
           "two_rows_coherent": combined in [projection(row) for row in rows], "result": combined},
          {"same_group": True, "one_row_coherent": True, "two_rows_coherent": False,
           "result": {"embarque_id": 200, "numero_viaje": 900, "embarque_fecha_creacion": "2026-11-19"}}, qev(393, 428),
          "Una sola fila mantiene coherencia. No se usa MAX textual de app_tracking ni se presupone collation.", domain_limit)
    dominated = {**rows[0], "embarque_id": 50, "numero_viaje": 700, "embarque_fecha_creacion": "2026-11-17"}
    check("CS-14", "Permutación, duplicación y dominación no reparan la agregación", ["PH-004"],
          [aggregate(rows[::-1]) == combined, aggregate(rows + rows) == combined, aggregate(rows + [dominated]) == combined,
           max(rows, key=lambda r: r["embarque_id"]) in rows], [True, True, True, True], qev(393, 413),
          "El último control selecciona una fila completa como ejemplo abstracto de coherencia, no como política aprobada de cuál fila usar.", domain_limit)
    separated = [{**row, "chasis": f"SYN-{i}"} for i, row in enumerate(rows)]
    check("CS-15", "Cambiar una clave GROUP BY separa las poblaciones", ["PH-004"],
          len({group_key(row) for row in separated}), 2, qev(416, 428),
          "La mezcla requiere al menos dos relaciones dentro del mismo grupo; no se afirma para grupos distintos.", domain_limit)

    types = [scalar(leaf.expressions[0], {}) for leaf in ct["tipos_inventario"].flatten()]
    type_domains = {str(v): [t for t in types if scalar(expression(f"t.tipo_inventario_id = {v}"), {"t.tipo_inventario_id": t}) is True] for v in [1, 2, 3]}
    check("CS-16", "Dominio de CROSS JOIN solo1/2 frente al estado3 derivado", ["PH-IMP002"],
          type_domains, {"1": [1], "2": [2], "3": []}, qev(53, 57) + qev(337),
          "El filtro3 tiene dominio vacío; no selecciona inventario_3_concesionario.", domain_limit)
    base_outputs = {x.alias_or_name: x.unalias() for x in base.expressions}
    inventory_rows = [{"tipo_inventario_id": t, "estado": scalar(base_outputs["estado"], {"m.chasis": None if t == 1 else "SYN-VIN"})} for t in types]
    cases = {key: next(roots[key].find_all(exp.Max)).this for key in ["inventario_1_pre_embarque", "inventario_2_confirmacion_pre_embarque"]}
    pivot = lambda rr: {key: sql_max(arg, rr) for key, arg in cases.items()}
    prefiltered = [row for row in inventory_rows if row["estado"] == "Pendiente"]
    before = pivot(prefiltered)
    preserved = pivot(inventory_rows)
    check("CS-17", "Filtrar antes de pivotar no equivale a seleccionar vehículo después", ["PH-IMP002"],
          {"pre_pivot": before, "post_vehicle_selection": preserved, "equivalent": before == preserved},
          {"pre_pivot": {"inventario_1_pre_embarque": "Pendiente", "inventario_2_confirmacion_pre_embarque": None},
           "post_vehicle_selection": {"inventario_1_pre_embarque": "Pendiente", "inventario_2_confirmacion_pre_embarque": "Realizado"}, "equivalent": False},
          qev(38, 43) + qev(386, 387) + qev(411, 413),
          "Sin filtro ambas rutas coinciden; no se declara cuál política debe adoptar negocio.", domain_limit)
    check("CS-18", "Pivote vacío y tipo único conservan NULL de SQL MAX", ["PH-IMP002"],
          [pivot([]), pivot(inventory_rows[1:])],
          [{"inventario_1_pre_embarque": None, "inventario_2_confirmacion_pre_embarque": None},
           {"inventario_1_pre_embarque": None, "inventario_2_confirmacion_pre_embarque": "Realizado"}], qev(411, 412),
          "No se transforma NULL en Pendiente ni se atribuye comportamiento al navegador.", domain_limit)
    local_branches = list(ct["tmp_movimientosdos"].flatten())
    check("CS-19", "Los dominios local2 y preembarque3 permanecen separados", ["PH-IMP002", "PH-IMP003"],
          {"local_branches": len(local_branches), "local2_guard_per_branch": [expression("tipo_inventario_cliente_local_id = 2") in conjuncts(x.args["where"]) for x in local_branches],
           "pre3_guard": expression("tipo_inventario_id = 3") in conjuncts(ct["tmp_movimientostres"].args["where"])},
          {"local_branches": 4, "local2_guard_per_branch": [True] * 4, "pre3_guard": True}, qev(158, 207),
          "Los números de dos campos distintos no se convierten en un único catálogo.", ast_limit)
    state3 = base_outputs["estadodos"]
    check("CS-20", "CASE de estado3 es disyunción de presencia, no completitud", ["PH-IMP003"],
          [scalar(state3, {"mdos.chasis": a, "mtres.chasis": b}) for a, b in [(None, None), ("SYN", None), (None, "SYN"), ("SYN", "SYN")]],
          ["Pendiente", "Realizado", "Realizado", "Realizado"], qev(299, 305),
          "Solo el caso sin ambos registros queda Pendiente; no se valida la inspección física ni todas sus secciones.", domain_limit)
    branches = list(ct["tmp_movimientos"].flatten())
    movement_sources = sorted(x.args["from_"].this.name for x in branches)
    outer_columns = {c.name for x in tree.expressions for c in x.find_all(exp.Column)}
    check("CS-21", "Existencia UNION de cuatro fuentes y flags sin consumo exterior", ["PH-IMP003"],
          {"sources": movement_sources, "base_flags_used_outside": sorted(outer_columns & {"con_faltante", "con_desperfecto", "con_contaminacion", "kilometraje"})},
          {"sources": ["inventario_parametros", "inventario_registros_accesorios", "inventario_registros_contaminaciones", "inventario_registros_partes_mercancia"], "base_flags_used_outside": []},
          qev(115, 156) + qev(288, 308) + qev(393, 413),
          "No se interpreta presencia de una fuente como defecto de completitud; tampoco se audita presentación de resultados.", ast_limit)

    # SQL AST coverage is deliberately bounded: PHP effects are inspected, never executed.
    page, data = text[PAGE], text["index_archivos/data.php"]
    def aux_query(name):
        match = re.search(r'\$query' + name + r'\s*=\s*"([\s\S]*?)";', page)
        if not match:
            raise ValueError("Missing auxiliary query")
        sql = match.group(1).replace('\".$idTransportistaSesion.\"', ':session_provider')
        return sqlglot.parse_one(sql, read="mysql")
    transport, destinations = aux_query("Transportista"), aux_query("Concesionario")
    check("CS-22", "Los SELECT auxiliares no comparten el mismo scope de proveedor", ["PH-IMP001", "PH-IMP004"],
          [owner in conjuncts(transport.args["where"]), any(c.name == "proveedor_id" for c in destinations.find_all(exp.Column))],
          [True, False], [ev(PAGE, 52, 76)],
          "Consulta global no equivale a divulgación: no se inspecciona su salida al navegador.", ast_limit)
    check("CS-23", "Dependencia constructor→data no equivale a ejecución del constructor", ["PH-IMP004", "PH-IMP005"],
          {"query_assignments": len(re.findall(r'\$query\[0\]\s*=', text[QUERY])),
           "builder_sql_dispatches": len(re.findall(r'\b(?:mysql_query|mysqli_query)\s*\(', text[QUERY])),
           "caller_order": page.index('include("reportepreembarquenacionalquery.php")') < page.index('include("../data.php")'),
           "principal_fetch_without_explicit_return_check": '$result = mysql_query($query[0]);\nwhile($row = mysql_fetch_array($result))' in data},
          {"query_assignments": 1, "builder_sql_dispatches": 0, "caller_order": True,
           "principal_fetch_without_explicit_return_check": True}, [ev(PAGE, 85, 87), ev(QUERY, 52), ev("index_archivos/data.php", 6, 14)],
          "Un AST SQL válido no demuestra éxito de PHP/mysql_query ni captura fallos de include/conexión. No se ejecuta data.php.",
          "Lectura estática del puente PHP; los controles de fallo de fase1 se conservan, sin emulación de despliegue.")
    # A round trip tests parser stability, not source execution or server compatibility.
    reparsed = sqlglot.parse_one(tree.sql(dialect="mysql"), read="mysql")
    check("CS-24", "Round-trip AST sin cambiar cláusulas ni claves", ["PH-003", "PH-004", "PH-IMP005"],
          reparsed == tree, True, qev(52, 432),
          "SQL emitido solo se vuelve a parsear en memoria; no se guarda ni se envía a un motor.", ast_limit)
    unknown = {"p.deleted_at": None, "p.proveedor_id": None, ":session_provider": 41}
    check("CS-25", "NULL no satisface igualdad de scope", ["PH-IMP001"],
          [scalar(base.args["where"], unknown), scalar(base.args["where"], {**unknown, "p.proveedor_id": 41}),
           scalar(base.args["where"], {**unknown, "p.proveedor_id": 82})], [None, True, False], qev(381, 382),
          "WHERE admite solo True; Unknown no se convierte en True por coerción Python.", domain_limit)

    # Phase-2 revalidation does not rewrite/promote accepted phase-1 records.
    by_id = {c["id"]: c for c in checks}
    all_ids = [*FINDINGS, *IMPROVEMENTS]
    coverage = []
    for accepted, origin in {**FINDINGS, **IMPROVEMENTS}.items():
        linked = [x["id"] for x in checks if accepted in x["accepted_ids"]]
        if not linked:
            raise ValueError(f"Missing closure coverage: {accepted}")
        coverage.append({"id": accepted, "origin_id": origin, "classification": old_items[origin]["classification"],
                         "title": old_items[origin]["title"], "status": "completed",
                         "result": "pass" if all(by_id[x]["result"] == "pass" for x in linked) else "fail",
                         "check_ids": linked, "evidence": old_items[origin]["evidence"], "canonical": False})
    # All cited line ranges refer to local immutable blobs, never moving refs.
    for record in [*checks, *coverage]:
        for e in record["evidence"]:
            body = text.get(e["path"]) if e["commit"] == HEAD else (old_query if e["path"] == QUERY and e["commit"] == P95 else None)
            if body is None:
                body = git(source, "show", f"{e['commit']}:{e['path']}").decode("utf-8-sig")
            if not 1 <= e["line_start"] <= e["line_end"] <= len(body.splitlines()):
                raise ValueError("Invalid source evidence range")
    failures = [x["id"] for x in checks if x["result"] != "pass"]
    if failures:
        raise AssertionError("Closure discrepancy requires investigation, not a forced zero delta: " + ", ".join(failures))
    if phase1_path.read_bytes() != phase1_raw:
        raise ValueError("Phase-1 sidecar changed concurrently; re-read before generating closure")

    technique = {"name": "mysql_ast_scope_and_benign_finite_metamorphic_closure", "parser": "SQLglot",
                 "version": VERSION, "dialect": "mysql", "isolated_package": str(package),
                 "ast_operations": ["CTE/scope resolution", "mandatory WHERE conjunctions", "join key extraction",
                                    "projection/GROUP BY aggregate lineage", "finite type domains", "AST round-trip"],
                 "metamorphisms": ["benign optional-filter insertion", "abstract AND/OR composition", "identity domain tagging",
                                   "foreign-scope mutation with fixed VIN", "VIN/preembarque/type key mutation",
                                   "row permutation/duplication/dominance", "group partitioning", "filter-before/after-pivot"],
                 "different_from_phase1": "No se ejecuta peru_head_report_probes.py ni se reutilizan sus 36 resultados como comprobaciones de cierre. Aquí se parsean árboles y se evalúan sus nodos en dominios finitos.",
                 "interpreter_limit": "Subconjunto explícito Column/Placeholder/Literal/NULL/Boolean/AND/OR/NOT/EQ/IS NULL/CASE/IF/COALESCE y MAX de grupos sintéticos; cualquier otro nodo falla como no soportado. No es motor SQL."}
    limits = [ast_limit, domain_limit,
              "La extracción sustituye el ID por placeholder y nueve fragmentos por constantes benignas; no interpreta PHP ni prueba toda entrada dinámica.",
              "No se vuelve a probar explotación de fechas; solo su frontera de composición y la diferencia entre AST instanciado y constructor de PHP.",
              "Sin DDL autorizado: resolución de aliases no demuestra columnas físicas, unicidad, tipos efectivos, FK ni aislamiento entre tenants.",
              "La obligación de rol de PH-001 mantiene acceso efectivo y dominios reales como precondiciones; no se decide política de tipo7.",
              "No se valida SQL_MODE, versión del servidor, collation, plan de ejecución, privilegios, PHP/extensiones, includes ni despliegue.",
              "No revisión de navegación/salidas al navegador, exportador, master a44, código JS ni CF/PH-IMP006..008 en esta fase acotada.",
              "Checks completed significa pruebas aisladas terminadas, no cierre global, aprobación de TOBE ni certificación productiva."]
    common = {"schema_version": 1, "phase": "closure_after_acceptance_of_4_findings_and_8_improvements",
              "date": "2026-11-19", "timezone": "Europe/Madrid", "date_authority": "user", "canonical": False,
              "status": "completed", "global_closure_claimed": False, "technique": technique,
              "evidencepins": {"source": HEAD, "previous_peru": P95, "historical_master": M, "knowledge_baseline": KB,
                               "phase1_report_sha256": digest(phase1_raw)},
              "accepted_scope": {"findings": list(FINDINGS), "improvements": list(IMPROVEMENTS),
                                 "excluded_CF_improvements": ["PH-IMP006", "PH-IMP007", "PH-IMP008"]},
              "new_findings": [], "improvements": [],
              "delta_assessment": "No se encontró precisión material adicional fuera de PH-001..004 y PH-IMP001..005. La ubicación del scope, dominios, claves, población y agregados quedan revalidados con AST/controles negativos. Las restricciones de la técnica se explicitan; no se fuerza el cierre global.",
              "checks": checks, "accepted_revalidation": coverage,
              "summary": {"checks_completed": len(checks), "checks_passed": len(checks), "accepted_findings_revalidated": 4,
                          "accepted_improvements_revalidated": 5, "new_findings": 0, "new_improvements": 0},
              "limitations": limits,
              "boundaries": {"php_or_handler_executed": False, "bootstrap_executed": False, "sql_executed": False,
                             "database_or_http_access": False, "network_access": False, "real_rows_used": False,
                             "operational_attack_or_payload_generated": False, "browser_output_navigation_reviewed": False,
                             "new_master_a44_reviewed": False, "deployment_emulated": False,
                             "phase1_or_final_docs_or_manifest_edited": False, "commit_or_push": False}}
    evidence_report = {**common, "source_inventory": [{"commit": HEAD, "path": p, "blob_sha256": digest(v),
                                                        "git_blob": git(source, "rev-parse", f"{HEAD}:{p}").decode().strip()} for p, v in raw.items()],
                       "ast_inventory": {"node_count": sum(1 for _ in tree.walk()), "scope_count": len(scopes),
                                         "ctes": list(ct), "optional_filter_variants": variants,
                                         "outer_group_keys": group_columns,
                                         "primary_extracted_sql_sha256": digest(head_sql.encode()),
                                         "previous_extracted_sql_sha256": digest(p95_sql.encode()),
                                         "extracted_sql_stored": False},
                       "reproduction": "python -B scripts/audit/peru_head_closure_sql.py"}
    review = {**common, "probe_artifact": OUTPUTS[0], "script": "scripts/audit/peru_head_closure_sql.py"}
    md = ["# Cierre acotado por AST MySQL y metamorfismos benignos", "",
          "19 de noviembre de 2026 · Europe/Madrid · fecha del usuario · no canónico.", "",
          f"SQLglot **{VERSION}**, dialecto MySQL, instalación aislada `{package}`. **{len(checks)}/{len(checks)} checks completed/pass**: cuatro hallazgos aceptados y cinco mejoras de reportes revalidados. No hay novedades materiales adicionales: `new_findings=[]`, `improvements=[]`. No se reclama cierre global.", "",
          f"Pins: HEAD `{HEAD}`, P95 `{P95}`, M histórico `{M}`, KB `{KB}`. La única comparación de SQL es HEAD/P95; M no se audita de nuevo.", "",
          "Técnica diferente de los 36 probes de fase1: extracción del constructor sin ejecutar PHP; parsing MySQL, 11 CTE, 29 ámbitos; resolución de aliases, claves ON, conjunciones WHERE, GROUP BY y linaje de MAX; evaluación parcial de nodos AST sobre dominios sintéticos. Se prueban inserción de filtros benignos, dominios de identidad, mutación de claves, permutación/duplicación/dominación de filas y filtrado antes/después del pivote. No se construye ningún payload adversarial ni consulta de ataque.", "",
          "La consulta benigna conserva el scope como conjunción obligatoria. Eso no demuestra que el constructor PHP parametrice sus fragmentos: el testigo AND/OR usa únicamente símbolos abstractos, sin entradas adversariales. Las uniones por VIN no añaden pertenencia; el control con claves compuestas sí distingue dominios. Los MAX de varias columnas preservan sus máximos, pero pueden perder una fila origen coherente; cambiar una clave GROUP BY separa esos grupos.", "",
          "## Cobertura de lo aceptado", "", "| Registro | Origen fase1 | Checks | Resultado |", "| --- | --- | --- | --- |"]
    for x in coverage:
        md.append(f"| {x['id']} | {x['origin_id']} | {', '.join(x['check_ids'])} | completed/pass |")
    md.extend(["", "## Checks y controles negativos", ""])
    for x in checks:
        md.extend([f"### {x['id']} — {x['title']}", "", f"Estado: completed/pass. Registros: {', '.join(x['accepted_ids'])}.", "",
                   "Control negativo/límite de inferencia: " + x["negative_controls"], "", "Límite: " + x["limits"], "",
                   "Evidencia: " + "; ".join(f"`{e['commit']}:{e['path']}:L{e['line_start']}-L{e['line_end']}`" for e in x["evidence"]) + ".", ""])
    md.extend(["## Limitaciones", "", *["- " + value for value in limits], "",
               "Solo se escriben los sidecars de cierre. Fase1, registro aceptado, documentos finales y manifest permanecen fuera de la escritura de este script. CF/PH-IMP006..008 quedan en la integración del padre; no se usa una comprobación local para afirmar composición o vigencia de M-only en Perú.", "",
               "[Evidencia y resultados](../../../source-audits/peru/2026-11-19/closure-sql.json) · [Registro JSON](closure-sql.json) · [Script](../../../scripts/audit/peru_head_closure_sql.py).", "",
               "Reproducción: `python -B scripts/audit/peru_head_closure_sql.py --source C:/repos/proveedores-peru-head-review-20261119 --knowledge C:/repos/asgard-proveedores-knowledge --sqlglot C:/repos/audit-tools-proveedores-sqlglot-20261118`.", ""])
    contents = [json.dumps(evidence_report, ensure_ascii=False, indent=2) + "\n",
                json.dumps(review, ensure_ascii=False, indent=2) + "\n", "\n".join(md)]
    for relative, body in zip(OUTPUTS, contents):
        target = knowledge / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    print(json.dumps({"status": "completed", "checks": len(checks), "passed": len(checks),
                      "new_findings": [], "improvements": [], "accepted_scope_revalidated": all_ids,
                      "outputs": OUTPUTS}, ensure_ascii=False))


if __name__ == "__main__":
    main()
