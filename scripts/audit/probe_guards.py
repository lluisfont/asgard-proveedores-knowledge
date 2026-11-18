"""Exercise only pure download guards in CLI, without HTTP, database or application handlers."""

import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--target',default=str(Path(__file__).resolve().parents[2]))
    args=parser.parse_args()
    source=Path(args.source).resolve()
    target=Path(args.target).resolve()
    cases=[
        ('image_anonymous','index_archivos/tracking/guardia_imagen.php',False,'f','foto.jpg',False),
        ('image_authenticated','index_archivos/tracking/guardia_imagen.php',True,'f','foto.jpg',True),
        ('image_parent_path','index_archivos/tracking/guardia_imagen.php',True,'f','../foto.jpg',False),
        ('image_absolute_path','index_archivos/tracking/guardia_imagen.php',True,'f','/foto.jpg',False),
        ('image_empty_path','index_archivos/tracking/guardia_imagen.php',True,'f','',False),
        ('relative_download_anonymous','index_archivos/guardia_descargas_rel.php',False,'p','foto.jpg',False),
        ('relative_download_authenticated','index_archivos/guardia_descargas_rel.php',True,'p','foto.jpg',True),
        ('relative_download_parent','index_archivos/guardia_descargas_rel.php',True,'p','../foto.jpg',False),
    ]
    results=[]
    for name,relative,authenticated,key,value,expected in cases:
        session="array('idtransportista'=>1)" if authenticated else 'array()'
        code=("session_start(); $_SESSION="+session+"; $_GET=array("+json.dumps(key)+"=>"+json.dumps(value)+"); "
              "$GLOBALS['probe_reached']=false; register_shutdown_function(function(){echo json_encode(array('reached'=>$GLOBALS['probe_reached'],'status'=>http_response_code()));}); "
              'require '+json.dumps(str(source/relative))+'; '+"$GLOBALS['probe_reached']=true;")
        run=subprocess.run(['php','-n','-d','session.use_cookies=0','-r',code],capture_output=True,text=True)
        try:
            data=json.loads(run.stdout)
        except json.JSONDecodeError:
            raise RuntimeError('Guard probe output not JSON: '+name)
        passed=run.returncode==0 and data['reached']==expected
        results.append({'case':name,'source':relative,'expected_continue':expected,
                        'actual_continue':data['reached'],'http_status':data['status'],
                        'status':'pass' if passed else 'fail'})
    report={'mode':'isolated_php_cli_guards_only','database_access':False,'network_access':False,
            'application_handler_executed':False,'cases':results,
            'passed':sum(r['status']=='pass' for r in results),'total':len(results),
            'limitation':'These guards are a narrow bounded check, not end-to-end authentication, tenant ownership, authorization or deployment verification.'}
    path=target/'source-audits/master/2026-11-18/guard-probes.json'
    path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['passed']==len(results) else 1)


if __name__=='__main__':
    main()
