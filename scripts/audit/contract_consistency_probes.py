"""Pinned, offline contract probes. Writes only the explicitly owned probe report.

No application bootstrap, handlers, sessions, database, HTTP or filesystem sinks
are executed. PHP methods are extracted with token_get_all and evaluated with
in-memory substitutes under php -n. JavaScript options run in an empty vm context;
$.ajax is a recorder, not a transport. This is NOT deployment validation.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

PINS = {
    "M": "a8ce2c23dead8552d2c4699e4a9b9134f7a18707",
    "P": "95fe9a4c3b3cddd84be922cc0e1eb9c88603df62",
}
DEFAULT_REPO = Path("C:/repos/proveedores-github-review-20261118")
KNOWLEDGE = Path(__file__).resolve().parents[2]
OWNED_REPORT = KNOWLEDGE / "source-audits/master/2026-11-18/iterative/contract-consistency-probes.json"
SOURCES: dict[tuple[str, str], str] = {}
REPO = DEFAULT_REPO


def run(command: list[str], content: str) -> str:
    result = subprocess.run(command, input=content, capture_output=True,
                            text=True, encoding="utf-8", timeout=30)
    if result.returncode:
        raise RuntimeError(f"{command[0]} failed: {result.stderr[:1500]}")
    return result.stdout


def source(variant: str, path: str) -> str:
    key = (variant, path)
    if key not in SOURCES:
        raw = subprocess.check_output(["git", "-C", str(REPO), "show", f"{PINS[variant]}:{path}"])
        SOURCES[key] = raw.decode("utf-8")
    return SOURCES[key]


DISABLE = ",".join([
    "exec", "system", "passthru", "shell_exec", "popen", "proc_open",
    "mail", "fsockopen", "pfsockopen", "stream_socket_client", "curl_exec",
    "fopen", "file_get_contents", "file_put_contents", "unlink", "mkdir",
    "rename", "copy", "session_start", "move_uploaded_file",
])


def php(code: str) -> object:
    text = run(["php", "-n", "-d", "display_errors=stderr", "-d", "memory_limit=128M",
                "-d", f"disable_functions={DISABLE}"], "<?php\n" + code)
    return json.loads(text)


def php_string(value: str) -> str:
    encoded = base64.b64encode(value.encode("utf-8")).decode("ascii")
    return "base64_decode('" + encoded + "')"


def methods(variant: str, path: str, wanted: list[str]) -> dict:
    # Native lexer balances punctuation tokens only; braces in interpolated SQL
    # are paired by the lexer as well. Strings/comments are not regex call edges.
    payload = json.dumps({"source": source(variant, path), "wanted": wanted})
    return php(r'''
$in=json_decode(''' + php_string(payload) + r''',true);
$tokens=token_get_all($in['source']); $out=[];
for($i=0;$i<count($tokens);$i++) {
  $t=$tokens[$i];
  if(!is_array($t)||$t[0]!==T_FUNCTION) continue;
  $name=null;
  for($j=$i+1;$j<count($tokens);$j++) {
    if(is_array($tokens[$j]) && $tokens[$j][0]===T_STRING){$name=$tokens[$j][1];break;}
    if($tokens[$j]==='(') break;
  }
  if(!in_array($name,$in['wanted'],true)) continue;
  $body='';$depth=0;$opened=false;
  for($j=$i;$j<count($tokens);$j++) {
    $q=$tokens[$j];$s=is_array($q)?$q[1]:$q;$body.=$s;
    if($q==='{'){$depth++;$opened=true;}
    if(is_array($q)&&in_array($q[0],[T_CURLY_OPEN,T_DOLLAR_OPEN_CURLY_BRACES],true)) $depth++;
    if($q==='}'){$depth--;if($opened&&$depth===0)break;}
  }
  $out[$name]=['code'=>$body,'line_start'=>$t[2], 'line_end'=>$t[2]+substr_count($body,"\n")];
}
echo json_encode($out);
''')


def state_probes() -> list[dict]:
    path = "index_archivos/embarques/componentes/estado-pedidos/controllers/EstadoPedidosClass.php"
    results = []
    for variant in PINS:
        extracted = methods(variant, path, ["determinarEstado"])["determinarEstado"]
        view = source(variant, "index_archivos/tracking/listaviajes.php")
        start = view.index("<?php if($viaje['estado'] <> null)")
        end = view.index("<?php } ?>", start) + len("<?php } ?>")
        fragment = view[start:end]
        result = php(r'''
class StateProbe {
  public $row=[];
  public function getQuery($query,$a=false,$b=false){return $this->row;}
''' + extracted["code"] + r'''
}
$p=new StateProbe();$summary=[];
$fields=['fecha_finalizacion','fechaoficial','carpeta','fechaaprobacion','fecha_enviado'];
for($mask=0;$mask<32;$mask++) {
  $p->row=[];
  foreach($fields as $i=>$field)$p->row[$field]=($mask&(1<<$i))?'2026-01-01':null;
  $summary[]=['mask'=>$mask,'label'=>strip_tags($p->determinarEstado(900001))];
}
$render=[];
foreach([null,0,'0',1,'1',2,'2',3,'3',4,'4'] as $s) {
  $viaje=['estado'=>$s];ob_start();eval('?>'.''' + php_string(fragment) + r''');
  $label=trim(strip_tags(ob_get_clean()));
  $render[]=['value'=>$s,'php_type'=>get_debug_type($s),'label'=>$label];
}
echo json_encode(['summary'=>$summary,'render'=>$render,'php_version'=>PHP_VERSION]);
''')
        expected = ["Pendiente", "Finalizado", "En Proceso", "Aceptado", "Enviado", "Enviado"]
        for row in result["summary"]:
            first = next((i + 1 for i in range(5) if row["mask"] & (1 << i)), 0)
            assert row["label"] == expected[first]
        labels = {(r["php_type"], str(r["value"])): r["label"] for r in result["render"]}
        assert labels[("int", "0")] == "Asignado"
        assert labels[("string", "0")] == "Rechazado"
        results.append({"variant": variant, "method_range": [extracted["line_start"], extracted["line_end"]], **result})
    assert results[0]["summary"] == results[1]["summary"]
    assert results[0]["render"] == results[1]["render"]
    return results


def js_inventory() -> dict:
    path = "index_archivos/embarques/componentes/inventario-local/tabla-vehiculos.js"
    payload = {v: source(v, path) for v in PINS}
    code = r'''
const vm=require('vm');const src=JSON.parse(require('fs').readFileSync(0,'utf8'));
const output={};
for(const [variant,raw] of Object.entries(src)){
  const requests=[];
  const ctx={nextTick:f=>f(),$: {LoadingOverlay:()=>{},ajax:o=>requests.push({url:o.url,method:o.type||o.method,data:o.data})},module:{exports:{}}};
  vm.createContext(ctx);
  const normalized=raw.replace(/^import[^\n]+\n/,'').replace('export default','module.exports =');
  vm.runInContext(normalized,ctx,{timeout:3000});
  const options=ctx.module.exports;
  const inst={...options.data(),link_api:'BASE/',token:'SYNTHETIC',embarqueId:901,tipoInventarioId:1,embarqueTipo:'nacional',esInventarioNacional:true};
  for(const [k,f] of Object.entries(options.methods))inst[k]=f.bind(inst);
  inst.cargarVehiculos();
  output[variant]={request:requests[0]};
  if(variant==='P'){
    const cases=[{pending:1},{pending:'1'},{pending:0},{pending:'0'},{pending:null},{missing:true},{pending:true},{pending:2}];
    output.P.flags=cases.map(c=>{
      const vehicle=c.missing?{}:{pendiente:c.pending};
      let event=null;inst.vehiculos=[vehicle];inst.$emit=(name,value)=>{event={name,value};};
      inst.emitirConteoInventario();
      return {input:c,pendienteFilter:inst.cumpleFiltroDetalle(vehicle,'pendiente'),event};
    });
    inst.vehiculos=[{chasis:'VIN-A',pendiente:0},{chasis:'VIN-B',pendiente:1}];
    inst.filtros.chasis='VIN-A';inst.formatDate=()=>'';
    const visible=options.computed.vehiculosVisibles.call(inst).length;
    let event;inst.$emit=(n,v)=>{event=v};inst.emitirConteoInventario();
    output.P.filtered={visible,header:event};
    let emitted=false;inst.esInventarioNacional=false;inst.$emit=()=>{emitted=true};inst.emitirConteoInventario();
    output.P.local_counter_emitted=emitted;
  }
}
process.stdout.write(JSON.stringify({node_version:process.version,...output}));
'''
    result = json.loads(run(["node", "-e", code], json.dumps(payload)))
    assert result["M"]["request"]["data"] == {"embarque_id": 901, "chasis": None, "partida": None}
    assert result["P"]["request"]["data"] == {"busqueda": None}
    flags = result["P"]["flags"]
    assert flags[0]["pendienteFilter"] is True and flags[0]["event"]["value"]["completados"] == 0
    assert flags[1]["pendienteFilter"] is False and flags[1]["event"]["value"]["completados"] == 0
    assert all(r["event"]["value"]["completados"] == 1 for r in flags[4:])
    assert result["P"]["filtered"] == {"visible": 1, "header": {"completados": 1, "total": 2}}
    assert result["P"]["local_counter_emitted"] is False
    return result


def edit_chain() -> list[dict]:
    results = []
    path = "index_archivos/embarques/CotizacionClass.php"
    for variant in PINS:
        handler=source(variant,"index_archivos/embarques/editarController.php")
        form=source(variant,"index_archivos/embarques/editar.php")
        component=source(variant,"index_archivos/embarques/componentes/embarques_mercancia.php")
        assert "name=\"nuevoschasis\"" in component and "$esCliente417Local" in component
        assert "action=\"editarController.php\"" in form and "componentes/embarques_mercancia.php" in form
        assert "$_POST['nuevoschasis']" in handler and "CotizacionClass::editarCotizacionCliente(" in handler
        wanted = ["editarCotizacionCliente", "getPedidos", "crearPedidosDetalle"]
        parsed = methods(variant, path, wanted)
        assert set(parsed) == set(wanted)
        code = "\n".join("public static " + parsed[n]["code"] for n in wanted)
        result = php(r'''
error_reporting(E_ERROR);
$calls=[];$hasPedido=true;
function conexionMysqli(){return null;}
function mysql_real_escape_string($s){return addslashes($s);}
function mysqli_real_escape_string($c,$s){return addslashes($s);}
function mysql_query($q){return memoryQuery($q);}
function mysqli_query($c,$q){return memoryQuery($q);}
function mysql_fetch_assoc($r){return is_array($r)?$r:false;}
function mysqli_fetch_assoc($r){return is_array($r)?$r:false;}
function memoryQuery($q){
  global $calls,$hasPedido;
  if(str_starts_with($q,'SELECT id FROM logis_pedidos'))return $hasPedido?['id'=>700001]:false;
  if(str_starts_with($q,'SELECT descripcioncarga'))return ['descripcioncarga'=>'VIN-OLD'];
  if(str_starts_with($q,'SELECT COUNT'))return $hasPedido?['total'=>0]:false;
  if(str_starts_with($q,'INSERT INTO logis_pedidos_detalle')) {
    $calls[]=['kind'=>'insert_detail','missing_pedido'=>str_contains($q,'VALUES (,')];
    return $hasPedido;
  }
  if(str_starts_with($q,'UPDATE logis_embarques SET descripcioncarga')){
    $calls[]=['kind'=>'update_description'];return true;
  }
  if(str_starts_with($q,'UPDATE logis_embarques SET')){$calls[]=['kind'=>'update_header'];return true;}
  throw new Exception('Unexpected query shape');
}
class EditProbe {
const CORRECTO=200;const ERROR=100;
public static function editarCotizacionMagnitudes($a,$b){}
public static function editarCotizacionDatos($a,$b){}
public static function editarCotizacionOperadores($a,$b,$c){}
''' + code + r'''
}
$_SESSION=['idtipoproveedor'=>1,'idusuarioaccesoproveedor'=>990001];
$base=array_fill_keys(['idincoterm','ciudadpais','idtipoembarque','ordencompraini','ordencompra','idproveedormercancia','descripcioncarga','tipomercancia','clase','un','temperatura','vigencia','observacion','idconcesionario'],'NULL');
$cases=[];
foreach([[999,1,'VIN-NEW',true],[417,3,'VIN-NEW',true],[999,1,'',true],[999,1,'VIN-NEW',false]] as $case){
  [$cliente,$scope,$new,$hasPedido]=$case;$calls=[];
  $data=$base+['idcliente'=>$cliente,'idtipoviaje'=>$scope,'nuevoschasis'=>$new];
  $result=EditProbe::editarCotizacionCliente(900001,$data,[],[],[]);
  $cases[]=['cliente'=>$cliente,'scope'=>$scope,'new_chasis_present'=>$new!=='','pedido_present'=>$hasPedido,'result'=>$result,'calls'=>$calls];
}
echo json_encode($cases);
''')
        assert any(c["kind"] == "insert_detail" for c in result[0]["calls"])
        assert not any(c["kind"] == "insert_detail" for c in result[2]["calls"])
        assert result[3]["result"]["code"] == 200
        assert any(c.get("missing_pedido") for c in result[3]["calls"])
        results.append({"variant": variant, "ranges": {n: [d["line_start"], d["line_end"]] for n,d in parsed.items()}, "cases": result})
    return results


def report_http_requests() -> list[dict]:
    raw=source("M","index_archivos/reportes/inventario-por-chasis.php")
    body=raw[raw.index("<script>\n"):]
    body=body[len("<script>\n"):body.index("</script>")]
    # PHP placeholders only supply synthetic values; PHP tags are never executed.
    body=re.sub(r"<\?.*?\?>","BASE/",body,flags=re.S)
    code=r'''
const vm=require('vm');const raw=require('fs').readFileSync(0,'utf8');const requests=[],handlers=[];
const document={};
function $(selector){return {ready:f=>f(),on:(event,f)=>handlers.push(f),val:()=> 'VIN-SYNTHETIC',data:()=>3};}
$.LoadingOverlay=()=>{};
$.ajax=o=>{requests.push({url:o.url,method:o.type||o.method,data:o.data,authHeaderPresent:!!o.headers.Authorization});};
const ctx={$,document};vm.createContext(ctx);vm.runInContext(raw,ctx,{timeout:3000});
for(const f of handlers)f();process.stdout.write(JSON.stringify(requests));
'''
    requests=json.loads(run(["node","-e",code],body))
    assert len(requests)==2 and all(r["method"]=="POST" for r in requests)
    assert requests[0]["data"]=={"chasis":"VIN-SYNTHETIC"}
    assert requests[1]["data"]=={"chasis":"VIN-SYNTHETIC","tipo_inventario_id":3}
    frame=source("M","index_archivos/embarques/frames/items.php")
    assert '<input type="hidden" id="url_pedidos" value="<?=URL_API?>"' in frame
    assert "ver_detalle_posiciones_pedido(" in frame
    return requests


def detail_request() -> dict:
    path="index_archivos/embarques/js/datosEmbarques.js"
    # Run the actual prefix function; do not execute the document.ready section.
    raw=source("M",path)
    prefix=raw[:raw.index("$(document).ready")]
    code=r'''
const vm=require('vm');const raw=require('fs').readFileSync(0,'utf8');const requests=[];
const values={'#tokenJWT':'SYNTHETIC','#url_pedidos':'BASE/','#idCliente':'999'};
function $(selector){return {val:()=>values[selector]};}
$.ajax=o=>{requests.push({url:o.url,method:o.method,headers:Object.keys(o.headers)});return {done:()=>{}}};
const ctx={$};vm.createContext(ctx);vm.runInContext(raw,ctx,{timeout:3000});
ctx.ver_detalle_posiciones_pedido(700001,false);process.stdout.write(JSON.stringify(requests));
'''
    req=json.loads(run(["node","-e",code],prefix))[0]
    assert req["url"] == "BASE/proveedores/detalle-pedido/700001" and req["method"] == "GET"
    return req


def schema_candidate() -> dict:
    base=KNOWLEDGE/"source-audits/local-schema-candidate/2026-11-18"
    profile=json.loads((base/"summary.json").read_text(encoding="utf-8"))
    cols=list(csv.DictReader((base/"columns.csv").open(encoding="utf-8-sig")))
    wanted={"tck_asignacion_viaje":{"estado"},"logis_edp":{"estado_edp_id","tipo_proveedor"},
            "logis_pedidos":{"id","embarque_id"},"logis_pedidos_detalle":{"pedido_id","posicion"},
            "logis_embarques":{"idconcesionario","cotizacion"}}
    selected=[r for r in cols if r["table"] in wanted and r["column"] in wanted[r["table"]]]
    assert len(selected) == sum(map(len,wanted.values()))
    return {"status":profile["status"],"dump_sha256":profile["source_sha256"],"country":profile["country"],
            "deployment_match":profile["matches_master_deployment"],"declarations_only":selected,
            "interpretation":"Candidate columns corroborate names only. INT/TINYINT do not define labels, Boolean domains or deployed constraints. No country identity or cross-namespace equality inferred."}


def equality_controls() -> list[dict]:
    paths=[".env-example.php","Dockerfile","package.json","index_archivos/composer.json",
           "index_archivos/MailClass.php","index_archivos/embarques/embarquesController.php","src/core/users/config.php"]
    out=[]
    for path in paths:
        objects={v:subprocess.check_output(["git","-C",str(REPO),"rev-parse",f"{pin}:{path}"],text=True).strip() for v,pin in PINS.items()}
        assert objects["M"]==objects["P"]
        out.append({"path":path,"objects":objects,"equal":True})
    return out


def namespace_controls() -> dict:
    local={}
    for variant in PINS:
        raw=source(variant,"index_archivos/embarques/frames/inventario_local.php")
        local[variant]={int(number):label for label,number in re.findall(
            r'<principal titulo="([^"]+)" :tipo-inventario="tipoInventario\.inventario(\d)"',raw)}
    pre=source("P","index_archivos/preembarques/frames/inventario.php")
    pre_map={int(number):label for number,label in re.findall(
        r'INVENTARIO (\d) - ([^<]+)</div>',pre)}
    assert local["M"]==local["P"] and set(local["P"])=={1,2,3,4,5}
    assert local["P"][1]=="DESPACHO NACIONAL" and pre_map[1]=="PRE EMBARQUE"
    return {"national_local":local,"pre_shipment_P":pre_map,"numeric_overlap_is_not_identity":True}


def main() -> None:
    global REPO
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-repo",type=Path,default=DEFAULT_REPO)
    args=ap.parse_args(); REPO=args.source_repo.resolve()
    report={"schema_version":"1.0","pins":PINS,"mode":"isolated_extracted_source_offline",
            "application_bootstrap_executed":False,"database_access":False,"network_access":False,
            "application_writes":False,"session_storage_used":False,
            "limits":"PHP 8.4 local probes do not validate PHP 5.4 Docker or deployment. Synthetic API values test consumer assumptions, not actual backend outputs.",
            "state_probes":state_probes(),"inventory_contract":js_inventory(),"edit_call_chain":edit_chain(),
            "items_detail_request":detail_request(),"report_http_requests":report_http_requests(),"equality_controls":equality_controls(),
            "namespace_controls":namespace_controls(),
            "local_schema_candidate":schema_candidate()}
    report["sources"]=[{"variant":v,"commit":PINS[v],"path":p,
                         "sha256_utf8":hashlib.sha256(s.encode("utf-8")).hexdigest()}
                        for (v,p),s in sorted(SOURCES.items())]
    report["checks_passed"]=True
    OWNED_REPORT.parent.mkdir(parents=True,exist_ok=True)
    OWNED_REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"report":str(OWNED_REPORT),"checks_passed":True,"pinned_sources":len(SOURCES),
                      "state_combinations":64,"variants":2,"no_external_effects":True}))


if __name__ == "__main__":
    main()
