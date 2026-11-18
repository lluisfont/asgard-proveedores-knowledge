#!/usr/bin/env python3
"""Extracted-method failure/invariant probes. No application includes or DB/network.

python -B scripts/audit/transaction_probes.py --source C:/repos/proveedores-github-review-20261118 --output source-audits/master/2026-11-18/iterative/transaction-probes.json
PHP CLI -n, disabled external-effect functions, in-memory synthetic fixtures only.
The SQL doubles log/return scheduled results; they are NOT MySQL emulators and
prove control flow and query construction, not real persistence/constraints.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

COMMIT = 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707'
HASHES = {
    'index_archivos/embarques/CostosClass.php': '60a26bbba7eb697efef832df54b86a7b6f5675c260bece2119d146c70cf687d2',
    'index_archivos/tracking/TrackingNewClass.php': '8d537b45ac2231a29ea9e117bb5b4942dca9e661a6efe3a585787c9e8a3fe25b',
    'index_archivos/tracking/controllers/CargaMasiva.php': 'c294471feaff9ad1a7bc01ebb54096e9bf39ef36aa4e0c8406ec0b662e3ad444',
    'index_archivos/tracking/ListaViajesClass.php': '1847cfff7c1588d635560f6b86c5cdde704e35da1556c6d376afd8efbbfcbfdf',
    'index_archivos/tracking/HerramientasClass.php': '0a6699c0b25b93b21981c0be2557daebbc4487bb230891ab4630e2800bf64232',
}
DISABLED = ','.join(('exec shell_exec system passthru popen proc_open mail fsockopen '
    'pfsockopen stream_socket_client stream_socket_server socket_create '
    'fopen file_get_contents file_put_contents file readfile fwrite copy rename '
    'unlink mkdir rmdir touch chmod chown move_uploaded_file session_start '
    'session_write_close session_regenerate_id').split())


def literal(value):
    return "base64_decode('" + base64.b64encode(value.encode()).decode() + "')"


def run_php(php, code):
    guard = "<?php if(extension_loaded('mysqli') || extension_loaded('pdo_mysql') || extension_loaded('curl')){exit(90);} "
    result = subprocess.run([php, '-n', '-d', 'display_errors=0', '-d', 'log_errors=0',
        '-d', 'allow_url_fopen=0', '-d', 'allow_url_include=0', '-d',
        'disable_functions=' + DISABLED], input=guard + code, text=True,
        encoding='utf-8', capture_output=True, timeout=25, check=False)
    if result.returncode:
        raise RuntimeError('Isolated PHP failed, exit=' + str(result.returncode))
    return json.loads(result.stdout)


def methods(php, source, names):
    """Tokenize only. Never evaluate original class/includes/top-level statements."""
    parser = '$src=' + literal(source) + ';$names=json_decode(' + literal(json.dumps(names)) + ',true);' + r'''
    $t=token_get_all($src);$out=[];$n=count($t);
    for($i=0;$i<$n;$i++) {
      if(!is_array($t[$i]) || $t[$i][0]!==T_FUNCTION)continue;
      $j=$i+1;while($j<$n && is_array($t[$j]) && $t[$j][0]===T_WHITESPACE)$j++;
      if(!is_array($t[$j]) || !in_array($t[$j][1],$names,true))continue;
      $name=$t[$j][1];$s='';$depth=0;$started=false;
      for($k=$i;$k<$n;$k++) {
        $a=$t[$k];$s.=is_array($a)?$a[1]:$a;
        if(is_array($a) && in_array($a[0],[T_CURLY_OPEN,T_DOLLAR_OPEN_CURLY_BRACES],true))$depth++;
        if(!is_array($a) && $a==='{'){$depth++;$started=true;}
        if(!is_array($a) && $a==='}'){
          $depth--;if($started && $depth===0){$out[$name]=$s;break;}
        }
      }
    }echo json_encode($out);
'''
    found = run_php(php, parser)
    if set(found) != set(names):
        raise RuntimeError('Requested method not found')
    for method in found.values():
        if any(token in method for token in ['include ', 'require ', 'session_start(', 'file_put_contents(']):
            raise RuntimeError('Unexpected effect in extracted method')
    return found


def cls(name, extracted, stubs='', constants=''):
    return 'class ' + name + '{' + constants + '\n' + '\n'.join(
        'public static ' + method for method in extracted.values()) + '\n' + stubs + '\n}'


PRELUDE = r'''
$_SESSION=['idtransportista'=>11,'idusuarioaccesoproveedor'=>22];
$results=[];$queries=[];$mode='';$sequence=[];$lastId=700;
function conexionMysqli(){return 'memory-double';}
function mysqli_fetch_assoc($rows){return $rows[0]??false;}
function mysqli_num_rows($rows){return count($rows);}
function mysqli_insert_id($connection){return $GLOBALS['lastId'];}
function mysqli_query($connection,$query){
  global $queries,$mode,$sequence,$lastId,$bulkMarked;
  $q=trim(preg_replace('/\s+/',' ',$query));$queries[]=$q;
  if(str_starts_with($mode,'cost:')){
    if(str_starts_with($q,'SELECT id FROM logis_costos'))return [['id'=>5]];
    if(str_starts_with($q,'SELECT * from logis_costos'))return [['id'=>str_contains($mode,'race')?102:101]];
    if(str_starts_with($q,'INSERT INTO logis_costos (')){$lastId=101;return $mode!=='cost:master-fail';}
    if(str_starts_with($q,'INSERT INTO logis_costos_detalle'))return !str_contains($mode,'detail-fail');
    if(str_starts_with($q,'UPDATE logis_costos'))return $mode!=='cost:delete-fail';
    if(str_starts_with($q,'DELETE FROM logis_costos'))return true;
    throw new Exception('Unexpected cost-double query');
  }
  if($mode==='location'){
    if(!count($sequence))throw new Exception('Unscheduled location query');
    $step=array_shift($sequence);$lastId++;
    if(!str_starts_with($q,'INSERT INTO '.$step[0].' '))throw new Exception('Wrong scheduled table');
    return $step[1];
  }
  if(str_starts_with($mode,'state:'))return $mode!=='state:sql-fail';
  if($mode==='edit-load-delete-fail')return false;
  if($mode==='edit-load' || str_starts_with($mode,'save:'))return true;
  if(str_starts_with($mode,'bulk:')){
    if(str_starts_with($q,'UPDATE tck_tmpcargamasiva SET estado = 1'))$bulkMarked=true;
    $lastId++;return true;
  }
  throw new Exception('Unexpected double mode');
}
function record($id,$observation,$passed,$control=false){
  $GLOBALS['results'][]=['id'=>$id,'passed'=>$passed,'negative_control'=>$control,'observation'=>$observation];
}
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    if output.is_relative_to(source):
        raise RuntimeError('Output must be outside application tree')
    php = shutil.which('php')
    if not php:
        raise RuntimeError('PHP CLI required')
    texts = {}
    for path, expected in HASHES.items():
        content = (source / path).read_text(encoding='utf-8')
        if hashlib.sha256(content.encode()).hexdigest() != expected:
            raise RuntimeError('Source hash differs: ' + path)
        texts[path] = content
    cpath, tpath, bpath, epath, hpath = HASHES
    cm = methods(php, texts[cpath], ['guardarCostos','deleteOldCost','guardaCostoMaestro','guardarCostoDetalle'])
    tm = methods(php, texts[tpath], ['save','getErrorResponse','saveLocation','subItems','castDate','edit','editLoad','saveLoad'])
    bm = methods(php, texts[bpath], ['crearViaje'])
    em = methods(php, texts[epath], ['eventosViaje'])
    hm = methods(php, texts[hpath], ['dicontinuedTrip'])
    code = PRELUDE + cls('CostProbe', cm, 'public static function enviarNotificacion($id){$GLOBALS["notifications"]++;}')
    code += r'''
$cost=[['categoryId'=>1,'otherCategoryDescripcion'=>'','totalCategory'=>30,'currency'=>'BOB',
  'concepts'=>[['concept'=>'A','amount'=>10,'automatic'=>0],['concept'=>'B','amount'=>20,'automatic'=>0]]]];
foreach(['ok','master-fail','detail-fail','delete-fail','race','race-detail-fail','mismatch','empty'] as $scenario){
  $mode='cost:'.$scenario;$queries=[];$notifications=0;$data=$cost;
  if($scenario==='mismatch')$data[0]['totalCategory']=999;
  if($scenario==='empty')$data[0]['concepts']=[];
  $r=CostProbe::guardarCostos($data,33);
  $detail=array_values(array_filter($queries,fn($q)=>str_starts_with($q,'INSERT INTO logis_costos_detalle')));
  $delete=array_values(array_filter($queries,fn($q)=>str_starts_with($q,'DELETE FROM logis_costos')));
  $expect=$scenario==='master-fail'?'error':($scenario==='empty'?'warning':'success');
  $passed=$r['tipo']===$expect;
  if($scenario==='race' || $scenario==='race-detail-fail')$passed=$passed && str_contains($detail[0],'(DEFAULT, 102,');
  if($scenario==='race-detail-fail')$passed=$passed && $delete===['DELETE FROM logis_costos WHERE id = 102'];
  if($scenario==='mismatch')$passed=$passed && str_contains(implode(' ',$queries),"'', 999, 'BOB'") && str_contains($detail[0],"'A', '', 10") && str_contains($detail[0],"'B', '', 20");
  if($scenario==='empty')$passed=$passed && count($queries)===0;
  record('cost-'.$scenario,['response'=>$r['tipo'],'queries'=>$queries,'notifications'=>$notifications,
      'own_insert_id_fixture'=>101,'concurrent_id_fixture'=>str_contains($scenario,'race')?102:null],$passed,in_array($scenario,['ok','empty','master-fail'],true));
}
'''
    code += cls('LocationProbe', {n: tm[n] for n in ['saveLocation','subItems','castDate']}, constants='const ORIGIN=1; const DESTINATION=2;')
    code += r'''
$loc=['type'=>2,'place'=>'PLACE','country'=>'BO','state'=>'','city'=>'CITY','address'=>'ADDRESS',
  'geolocation'=>['latitude'=>0,'longitude'=>0],'shipping_in_port'=>false,'download_deadline'=>'2026-11-18',
  'port_departure_date'=>'18/11/2026','from_hour_download'=>'00:00','to_hour_download'=>'00:00',
  'from_hour_departure'=>'00:00','to_hour_departure'=>'00:00','contact'=>'CONTACT','phone'=>'0',
  'dispatch_type'=>'','observations'=>'','id'=>44,'load_items'=>[['available'=>0,'package_type'=>1,'quantity'=>2]]];
$L='tck_localizaciones';$I='tck_items_localizaciones';
$plans=[
 'all-ok'=>[true,[[$L,true],[$I,true],[$L,true],[$I,true]]],
 'first-location-fails'=>[true,[[$L,false],[$L,true],[$I,true]]],
 'last-location-fails'=>[true,[[$L,true],[$I,true],[$L,false]]],
 'first-items-fail'=>[true,[[$L,true],[$I,false],[$L,true],[$I,true]]],
 'last-items-fail'=>[false,[[$L,true],[$I,true],[$L,true],[$I,false]]],
 'all-locations-fail'=>[false,[[$L,false],[$L,false]]],
 'empty'=>[false,[]]
];
foreach($plans as $scenario=>$plan){
 $mode='location';$sequence=$plan[1];$queries=[];
 $r=LocationProbe::saveLocation($scenario==='empty'?[]:[$loc,$loc],701,33,11,2);
 record('location-'.$scenario,['returned'=>$r,'scheduled'=>$plan[1],'queries'=>$queries],$r===$plan[0] && count($sequence)===0,in_array($scenario,['all-ok','last-items-fail','all-locations-fail','empty'],true));
}
'''
    constants = 'const CORRECTO=200;const ERROR=100;const DRIVER=1;const RELAY_DRIVER=2;const ORIGIN=1;const DESTINATION=2;'
    save_stubs = r'''
public static function saveInfo(...$a){return 701;}
public static function saveOrder(...$a){return $GLOBALS['mode']!=='save:order-fail';}
public static function trsnsportEnterprise(...$a){return true;}
public static function saveDrive(...$a){return $a[4]===1;}
public static function saveLoad(...$a){return true;}
public static function saveLocation(...$a){return true;}
public static function saveDocuments(...$a){return true;}
public static function saveRoutes(...$a){return false;}
public static function saveOrigin(...$a){return false;}
public static function sendWhatsapp(...$a){}
public static function registrarEdp(...$a){}
'''
    code += cls('SaveProbe', {n: tm[n] for n in ['save','getErrorResponse']}, save_stubs, constants)
    code += r'''
$assignment=(object)['informacion'=>(object)['isAssignment'=>1,'descripcionMercancia'=>'TEST'],
 'orden'=>(object)[],'empresaTransporte'=>(object)[],'chofer'=>(object)[],'choferRelevo'=>(object)[],
 'carga'=>[],'origenes'=>[],'destinos'=>[],'documentos'=>[],'rutas'=>(object)[],'idJourney'=>701];
foreach(['optional-fail','order-fail'] as $scenario){
 $mode='save:'.$scenario;$queries=[];$r=SaveProbe::save($assignment,33,11);
 record('save-'.$scenario,['response'=>$r,'queries'=>$queries],$r['code']===($scenario==='order-fail'?100:200),$scenario==='order-fail');
}
'''
    edit_stubs = r'''
public static function editInfo(...$a){return 701;}
public static function editOrder(...$a){return true;}
public static function editTransportEnterprise(...$a){return true;}
public static function editDrive(...$a){return true;}
public static function editLocation(...$a){return true;}
public static function editDocuments(...$a){return true;}
public static function editRoutes(...$a){return true;}
'''
    code += cls('EditProbe', {n: tm[n] for n in ['edit','editLoad','saveLoad','getErrorResponse']}, edit_stubs, constants)
    code += r'''
foreach(['edit-load','edit-load-delete-fail'] as $scenario){
 $mode=$scenario;$queries=[];$response=null;$error=null;
 try{$response=EditProbe::edit($assignment,33,11);}catch(Throwable $e){$error=get_class($e);}
 record($scenario,['error'=>$error,'response'=>$response,'queries'=>$queries],
   $scenario==='edit-load'?($error==='ArgumentCountError' && count($queries)===1):($error===null && $response['code']===100),$scenario==='edit-load-delete-fail');
}
'''
    bulk_stubs = r'''
public static function buscarEmpresaTransporte(...$a){return ['id'=>9,'nombre'=>'CARRIER','placa'=>'TEST','tipounidad'=>'TRUCK','capacidad'=>1];}
public static function buscarChofer(...$a){return ['id'=>8,'nombre'=>'DRIVER','numeroci'=>'0','celular'=>'0','numerolicencia'=>'0','categoria'=>'A'];}
public static function buscarCodigoCliente(...$a){return ['id'=>7];}
public static function buscarTipoBulto(...$a){return ['idunidad'=>1];}
public static function buscarOrigen(...$a){return ['origen'=>'ORIGIN','pais'=>'BO','ciudad'=>'CITY','direccion'=>'ADDRESS','latitude'=>0,'longitude'=>0];}
public static function getDatosParaValidar(...$a){return [];}
'''
    code += cls('BulkProbe', bm, bulk_stubs, constants)
    code += r'''
class CostosClass{public static function getDatosEmbarque($id){return [];}}
class TrackingNewClass{
 const DRIVER=1;
 public static function saveInfo(...$a){return $GLOBALS['failBulkHeader']?false:701;}
 public static function saveOrder(...$a){return true;}
 public static function trsnsportEnterprise(...$a){return true;}
 public static function saveDrive(...$a){return true;}
 public static function sendWhatsapp(...$a){}
 public static function registrarEdp(...$a){}
 public static function getErrorResponse($s){return ['code'=>100,'message'=>$s];}
}
$bulkRow=['idembarque'=>0,'idtransportista'=>11,'referencia'=>'R1','placa'=>'TEST','conductor'=>'DRIVER',
 'codigo'=>'CLIENT','tipobulto'=>'BOX','descripciondetallada'=>'ITEM','cantidad'=>2,'peso'=>3,'volumen'=>4,'origen'=>'ORIGIN'];
foreach(['first-group','header-fails'] as $scenario){
 $mode='bulk:'.$scenario;$queries=[];$bulkMarked=false;$failBulkHeader=$scenario==='header-fails';
 $r=BulkProbe::crearViaje(['idcargado'=>88,'lista'=>[$bulkRow]],22,1);
 $updates=array_values(array_filter($queries,fn($q)=>str_starts_with($q,'UPDATE tck_tmpcargamasiva SET estado = 1')));
 record('bulk-'.$scenario,['response'=>$r,'batch_mark_attempt'=>$bulkMarked,'state_updates'=>$updates,
   'fixture_batch_groups'=>[1,2],'created_group'=>1,'group2_not_yet_attempted'=>true],
   $scenario==='first-group'?($r['code']===200 && $bulkMarked && !str_contains($updates[0],'numero_viaje')):($r['code']===100 && !$bulkMarked),$scenario==='header-fails');
}
'''
    code += cls('EventProbe', em, r'''
public static function eventos(...$a){return $GLOBALS['remoteEvents'];}
public static function getEventName($id){return 'EVENT-'.$id;}
''')
    code += r'''
$eventCases=[
 'aligned'=>[[3,5,7],[3],[3,5,7]],
 'out-of-order'=>[[3,5,7],[5],[5,5,7]],
 'duplicate-detail'=>[[3,5,7],[3,3],[3,3,7]],
 'terminal-first'=>[[3,5,7],[26],[26,5,7]],
 'terminal-second'=>[[3,5,7],[3,26],[3,26]],
 'empty-remote'=>[[],[5],[5]]
];
foreach($eventCases as $scenario=>$plan){
 $remoteEvents=$plan[0];$detail=array_map(fn($id)=>['id'=>$id,'fecharegistro'=>'2026-11-18 10:00:00'],$plan[1]);
 $r=EventProbe::eventosViaje('LOCAL',701,$detail);$ids=array_column($r,'id');
 record('events-'.$scenario,['remote_ids'=>$remoteEvents,'registered_ids'=>$plan[1],'output_ids'=>$ids],$ids===$plan[2],in_array($scenario,['aligned','terminal-second','empty-remote'],true));
}
$dateCases=['18/11/2026'=>'2026-11-18','2026-11-18'=>'1900-01-01','31/02/2026'=>'2026-02-31',''=>'1900-01-01'];
foreach($dateCases as $input=>$expected){$r=LocationProbe::castDate($input);
 record('date-'.($input?:'empty'),['input'=>$input,'output'=>$r],$r===$expected,$input==='18/11/2026');}
'''
    code += cls('StateProbe', hm)
    code += r'''
foreach(['ok','sql-fail','zero-affected'] as $scenario){
 $mode='state:'.$scenario;$queries=[];
 $r=StateProbe::dicontinuedTrip((object)['id'=>701,'comentario'=>'TEST']);
 $q=$queries[0];$where=substr($q,strpos($q,'WHERE'));
 record('state-'. $scenario,['response'=>$r['type'],'query'=>$q,
   'double_affected_rows'=>$scenario==='zero-affected'?0:null],
   $r['type']===($scenario==='sql-fail'?'error':'success') && $where==='WHERE id = 701',
   $scenario==='sql-fail');
}
echo json_encode(['php_version'=>PHP_VERSION,'results'=>$results],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
'''
    result = run_php(php, code)
    rows = result['results']
    artifact = {
        'schema_version': '1.0', 'commit': COMMIT, 'source_root': source.as_posix(),
        'technique': 'extracted_method_failure_injection_and_data_invariant_review',
        'php_version': result['php_version'], 'source_hashes_lf_utf8': HASHES,
        'extracted_methods': {cpath: list(cm), tpath: list(tm), bpath: list(bm), epath: list(em), hpath: list(hm)},
        'safety': {'app_includes_executed': False, 'app_entrypoints_executed': False,
            'db_access': False, 'network': False, 'session_persistence': False,
            'app_writes': False, 'php_ini_loaded': False, 'sql_is_mocked': True},
        'adaptations': ['Methods wrapped as public static in isolated probe classes; bodies unchanged.',
            'Unselected collaborators replaced with explicit success/failure/no-op doubles.',
            'Cost concurrent row 102 scheduled at latest-row SELECT; own INSERT fixture is 101.',
            'Bulk lookup data synthetic; destination list empty to isolate batch-state UPDATE.',
            'PHP built-in mysqli extension absent; identically named functions are memory doubles.'],
        'limitations': ['No real transaction, SQL engine, affected-row counts, triggers, cascades, or concurrency executed.',
            'No PHP 5.4 execution; local PHP version is not deployment evidence.',
            'Passed means source behavior reproduced, not business invariant satisfied.'],
        'summary': {'total': len(rows), 'passed': sum(x['passed'] for x in rows),
            'negative_controls': sum(x['negative_control'] for x in rows)}, 'results': rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': output.as_posix(), **artifact['summary']}))
    if not all(x['passed'] for x in rows):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
