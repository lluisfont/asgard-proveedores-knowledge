#!/usr/bin/env python3
"""Reproduce doce pruebas aisladas del commit auditado, sin ejecutar la aplicación.

Uso: python scripts/audit/security_probes.py --source RUTA --output RESULTADO.json
Requiere Python 3 y PHP 8.4 CLI. No utiliza dependencias de terceros.
Lee el código desde --source; las huellas completas de los cinco archivos
impiden ejecutar código distinto del revisado. No contiene copias del código
de aplicación, credenciales ni valores extraídos de ellas. El código PHP se
extrae y adapta exclusivamente en memoria. Solo se permite escribir el JSON
de resultados, fuera del árbol de código fuente.
"""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


COMMIT = "a8ce2c23dead8552d2c4699e4a9b9134f7a18707"
SOURCE_HASHES = {
    "index_archivos/tracking/guardia_imagen.php": "c98ce852ebd808aaf634a02b099fa8daa706c9ddfac29066e1f6b6c2ba77813e",
    "index_archivos/guardia_descargas_rel.php": "b3a2603537974230f64f0783b76b5da7d858027bc5912cbb34136bb59c80d302",
    "index_archivos/permisos.php": "471f4f175ef30c9a0c1b9af45eec07641a300477185015a99da13a11796a9f4c",
    "index_archivos/resetpassword/ResetPassword.php": "28de2c7650c415fb210099fface61486210be2a322d7d36c6f94eb79e18c93cb",
    "index_archivos/2fa/TwoFaClass.php": "eadd0b08fd5dd720eed24aafe9735e1a3798310abff58904bb8e275ffcb492cc",
}

# Defensa adicional: no se ejecutan includes y se desactivan operaciones con
# efectos externos. -n evita cargar php.ini y extensiones de conexión a BD.
DISABLED = ",".join([
    "exec", "shell_exec", "system", "passthru", "popen", "proc_open",
    "mail", "fsockopen", "pfsockopen", "stream_socket_client", "stream_socket_server",
    "fopen", "file_get_contents", "file_put_contents", "file", "readfile", "fwrite",
    "copy", "rename", "unlink", "mkdir", "rmdir", "touch", "chmod", "chown",
    "move_uploaded_file", "session_start", "session_write_close", "session_regenerate_id",
])


def php_literal(value):
    encoded = base64.b64encode(value.encode("utf-8")).decode("ascii")
    return "base64_decode('" + encoded + "')"


def php_value(value):
    return "json_decode(" + php_literal(json.dumps(value)) + ",true)"


def run_php(php, body):
    prefix = """<?php
if (extension_loaded('mysqli') || extension_loaded('pdo_mysql')) { exit(90); }
"""
    result = subprocess.run(
        [php, "-n", "-d", "display_errors=0", "-d", "log_errors=0",
         "-d", "allow_url_fopen=0", "-d", "allow_url_include=0",
         "-d", "disable_functions=" + DISABLED],
        input=prefix + body, text=True, encoding="utf-8", capture_output=True,
        timeout=20, check=False,
    )
    # Nunca se propagan mensajes PHP: podrían contener código o valores locales.
    if result.returncode != 0:
        raise RuntimeError("El proceso PHP aislado terminó con código " + str(result.returncode))
    return result.stdout


def extract_method(php, source, name):
    """Extrae una función mediante tokens PHP sin evaluar el archivo original."""
    payload = php_value({"source": source, "name": name})
    parser = "$p=" + payload + ";" + r"""
$tokens=token_get_all($p['source']);
$count=count($tokens);
for($i=0;$i<$count;$i++) {
    if(!is_array($tokens[$i]) || $tokens[$i][0]!==T_FUNCTION) { continue; }
    $j=$i+1;
    while($j<$count && is_array($tokens[$j]) && $tokens[$j][0]===T_WHITESPACE) { $j++; }
    if($j>=$count || !is_array($tokens[$j]) || $tokens[$j][1]!==$p['name']) { continue; }
    $body=''; $depth=0; $started=false;
    for($k=$i;$k<$count;$k++) {
        $t=$tokens[$k];
        $body.=is_array($t) ? $t[1] : $t;
        if(is_array($t) && ($t[0]===T_CURLY_OPEN || $t[0]===T_DOLLAR_OPEN_CURLY_BRACES)) { $depth++; }
        if(!is_array($t) && $t==='{') { $depth++; $started=true; }
        if(!is_array($t) && $t==='}') {
            $depth--;
            if($started && $depth===0) { echo json_encode($body); exit; }
        }
    }
}
exit(91);
"""
    method = json.loads(run_php(php, parser))
    if not isinstance(method, str) or not method.startswith("function " + name):
        raise RuntimeError("No se pudo extraer el método revisado")
    return method


def require_replace(source, old, new):
    if source.count(old) != 1:
        raise RuntimeError("La adaptación en memoria no coincide con la fuente revisada")
    return source.replace(old, new, 1)


def probe_result(name, source, expected, actual, adaptation):
    return {"case": name, "source": source, "expected": expected, "actual": actual,
            "status": "pass" if actual == expected else "fail", "adaptation": adaptation}


def run_probes(php, sources):
    cases = []
    image = "index_archivos/tracking/guardia_imagen.php"
    download = "index_archivos/guardia_descargas_rel.php"
    guard_cases = [
        ("image_anonymous", image, {}, {"f": "ordinary.jpg"}, "BLOCK"),
        ("image_dotdot", image, {"idtransportista": 1}, {"f": "../example.jpg"}, "BLOCK"),
        ("image_absolute", image, {"idtransportista": 1}, {"f": "/example.jpg"}, "BLOCK"),
        ("image_relative", image, {"idtransportista": 1}, {"f": "ordinary.jpg"}, "CONTINUE"),
        ("download_anonymous", download, {}, {"p": "logistica"}, "BLOCK"),
        ("download_dotdot", download, {"idtransportista": 1}, {"p": "../other"}, "BLOCK"),
        ("download_relative", download, {"idtransportista": 1}, {"p": "logistica"}, "CONTINUE"),
    ]
    for name, path, session, query, expected in guard_cases:
        code = require_replace(sources[path],
            "if (session_status() === PHP_SESSION_NONE) { session_start(); }",
            "/* Sesión proporcionada en memoria. */")
        body = "$_SESSION=" + php_value(session) + "; $_GET=" + php_value(query) + ";"
        body += "register_shutdown_function(function(){echo http_response_code()===403 ? 'BLOCK' : 'END';});"
        body += "eval(" + php_literal("?>" + code) + "); echo 'CONTINUE';"
        raw = run_php(php, body)
        actual = {"BLOCK": "BLOCK", "CONTINUEEND": "CONTINUE"}.get(raw, "UNEXPECTED")
        cases.append(probe_result(name, path, expected, actual,
            "session_start sustituido solo en memoria; sin almacenamiento de sesiones"))

    path = "index_archivos/permisos.php"
    code = require_replace(sources[path], "session_start();", "/* Sesión en memoria. */")
    permission_cases = [
        ("permisos_authenticated", {"idtransportista": 1}, False, "CONTINUE"),
        ("permisos_anonymous_php84", {}, False, "Error"),
        ("permisos_anonymous_legacy_constant_simulation", {}, True, "CONTINUE"),
    ]
    for name, session, legacy, expected in permission_cases:
        body = "$_SESSION=" + php_value(session) + "; $_POST=[];"
        body += "$_SERVER=['HTTP_HOST'=>'example.invalid','REQUEST_URI'=>'/offline']; $linksistema='/';"
        if legacy:
            body += "define('datoconservar','datoconservar');"
        body += "ob_start(); try {eval(" + php_literal("?>" + code)
        body += "); $result='CONTINUE';} catch(Throwable $e){$result=get_class($e);} ob_end_clean(); echo $result;"
        cases.append(probe_result(name, path, expected, run_php(php, body),
            "Sesión en memoria; el caso legacy define únicamente la constante y no ejecuta PHP 5.4"
            if legacy else "session_start sustituido solo en memoria"))

    path = "index_archivos/resetpassword/ResetPassword.php"
    method = extract_method(php, sources[path], "resetPasswordClient")
    body = r"""
$captured=[];
function conexionMysqli(){return null;}
function mysqli_query($unused,$query){global $captured; $captured[]=$query; return true;}
function mysqli_fetch_assoc($unused){return ['correo'=>'audit@example.invalid','proveedor_usuario'=>'synthetic-audit-user'];}
"""
    body += "eval(" + php_literal("class AuditReset {const SUCCESS=200; const ERROR=100; public static " + method + "}") + ");"
    body += "$result=AuditReset::resetPasswordClient((object)['identifier'=>12,'password'=>'synthetic-offline-value']);"
    body += "echo json_encode(['success'=>$result['code']===200,'query_count'=>count($captured),"
    body += "'update_constructed'=>strpos($captured[1],'UPDATE prov_usuarioaccesoproveedor')===0]);"
    cases.append(probe_result("reset_without_token_mocked_db", path,
        {"success": True, "query_count": 2, "update_constructed": True}, json.loads(run_php(php, body)),
        "Solo el método extraído; funciones de BD sustituidas por funciones en memoria; ningún token suministrado"))

    path = "index_archivos/2fa/TwoFaClass.php"
    method = extract_method(php, sources[path], "autenticar")
    decoder = extract_method(php, sources[path], "decodeUsuario")
    method = require_replace(method, "session_start();", "/* Sesión en memoria. */")
    method = require_replace(method, 'ini_set("session.cookie_lifetime",6000);', "/* Sin configuración de sesión. */")
    body = "class logAsgard {static function saveLog(...$args){throw new RuntimeException('synthetic stop');}} $_SESSION=[];"
    body += "eval(" + php_literal("class AuditMfa {public " + method + " private " + decoder + "}") + ");"
    body += "$info=base64_encode(json_encode(['idproveedor'=>17,'idusuarioaccesoproveedor'=>19,'idtipoproveedor'=>1,'tabla'=>'synthetic','idutilizar'=>'synthetic']));"
    body += "try{(new AuditMfa())->autenticar($info);}catch(RuntimeException $e){}"
    body += "echo json_encode(['session_provider_assigned'=>$_SESSION['idtransportista']===17,"
    body += "'session_user_assigned'=>$_SESSION['idusuarioaccesoproveedor']===19,'mfa_code_supplied'=>false]);"
    cases.append(probe_result("mfa_client_identity_before_logging_failure", path,
        {"session_provider_assigned": True, "session_user_assigned": True, "mfa_code_supplied": False},
        json.loads(run_php(php, body)),
        "Métodos extraídos; sesión en memoria y logger que lanza una excepción antes de BD/JWT; no prueba persistencia"))
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--php", default="php")
    parser.add_argument("--output", type=Path, help="JSON fuera del árbol de aplicación; por defecto, salida estándar")
    args = parser.parse_args()
    root = args.source.resolve(strict=True)
    if args.output:
        output = args.output.resolve()
        if output == root or root in output.parents or output.suffix.lower() != ".json":
            raise RuntimeError("La salida debe ser un JSON fuera del árbol de aplicación")
    php = shutil.which(args.php)
    if not php:
        raise RuntimeError("No se encuentra PHP CLI")
    version = run_php(php, "echo PHP_VERSION;").strip()
    if not version.startswith("8.4."):
        raise RuntimeError("Estas expectativas requieren PHP 8.4 CLI")
    sources = {}
    for path, expected_hash in SOURCE_HASHES.items():
        text = (root / path).read_text(encoding="utf-8-sig")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != expected_hash:
            raise RuntimeError("La fuente difiere de la versión revisada: " + path)
        sources[path] = text
    cases = run_probes(php, sources)
    result = {
        "schema_version": "1.0", "mode": "isolated_in_memory_extracted_source",
        "commit": COMMIT, "source_root": str(root), "php_version": version,
        "source_hashes_verified": True, "source_files": list(SOURCE_HASHES),
        "database_access": False, "network_access": False,
        "application_handler_executed": False, "session_storage_used": False,
        "application_writes": False, "cases": cases,
        "passed": sum(case["status"] == "pass" for case in cases), "total": len(cases),
        "limitation": "Pruebas de guardias y métodos aislados con sustitutos en memoria. No prueban autenticación completa, persistencia de sesión, aislamiento entre proveedores, despliegue ni ejecución con PHP 5.4.",
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(json.dumps({"output": str(output), "passed": result["passed"], "total": result["total"]}))
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(rendered, end="")
    return 0 if result["passed"] == result["total"] == 12 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired):
        # Mensaje deliberadamente acotado: nunca volcar código ni stderr de PHP.
        print("No se completaron las pruebas: revise PHP 8.4, rutas y coincidencia de la fuente auditada.", file=sys.stderr)
        raise SystemExit(2)
