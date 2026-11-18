"""Probe the report query contract using extracted source blocks and in-memory DB substitutes."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from security_probes import run_php, php_value


COMMIT='a8ce2c23dead8552d2c4699e4a9b9134f7a18707'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    source=Path(args.source).resolve()
    output=Path(args.output).resolve()
    if output.is_relative_to(source):
        raise ValueError('Probe results must be outside application source')
    actual=subprocess.run(['git','-C',str(source),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
    if actual!=COMMIT:
        raise ValueError('Source commit differs from reviewed profile')
    relative='index_archivos/reporteexcel/reporteexcel.php'
    raw=(source/relative).read_text(encoding='utf-8-sig')
    committed=subprocess.run(['git','-C',str(source),'show',COMMIT+':'+relative],capture_output=True,check=True).stdout.decode('utf-8-sig')
    if raw.replace('\r\n','\n')!=committed.replace('\r\n','\n'):
        raise ValueError('Source content differs from pinned commit')
    lines=raw.splitlines()
    # The selected blocks decode report fields and dispatch queries. Bootstrap, guard and HTML are not executed.
    decode='\n'.join(lines[12:25])
    dispatch='\n'.join(lines[51:58])
    if '$consultas = explode("xxx", $_POST["query"]);' not in decode or '$consultas[0]' not in dispatch:
        raise ValueError('Selected source ranges no longer match reviewed contract')
    cases=[
        ('single_selection','SELECT marker FROM audit_fixture',['SELECT marker FROM audit_fixture']),
        ('auxiliary_mutation_before_selection','SELECT marker FROM audit_fixturexxxUPDATE audit_fixture SET marker=1',
         ['UPDATE audit_fixture SET marker=1','SELECT marker FROM audit_fixture']),
        ('multiple_auxiliary_commands','SELECT marker FROM audit_fixturexxxUPDATE audit_fixture SET marker=1xxxDELETE FROM audit_fixture WHERE marker=0',
         ['UPDATE audit_fixture SET marker=1','DELETE FROM audit_fixture WHERE marker=0','SELECT marker FROM audit_fixture']),
    ]
    results=[]
    for name,query,expected in cases:
        post={'query':query,'datos':'marker','posiciones':'left','formatos':'text','cabecera':'Marker'}
        prefix=("$GLOBALS['queries']=array(); function conexionMysqli(){return 'in-memory-stub';} "
                "function mysqli_query($connection,$query){$GLOBALS['queries'][]=$query;return true;} ")
        body=prefix+'$_POST='+php_value(post)+';'+decode+'\n'+dispatch+"\necho json_encode($GLOBALS['queries']);"
        found=json.loads(run_php('php',body))
        results.append({'case':name,'expected':expected,'actual':found,'status':'pass' if found==expected else 'fail'})
    report={'source_commit':COMMIT,'source':relative,
        'source_normalized_sha256':hashlib.sha256(raw.replace('\r\n','\n').encode()).hexdigest(),
        'source_ranges':[{'line_start':13,'line_end':25},{'line_start':52,'line_end':58}],
        'technique':'contract_based_extracted_source_with_database_substitutes',
        'network_access':False,'database_access':False,'application_entrypoint_executed':False,
        'guard_bypassed_for_analysis':'No guard/route reachability is tested; only decoding and dispatch blocks are evaluated.',
        'cases':results,'passed':sum(r['status']=='pass' for r in results),'total':len(results),
        'conclusion':'A caller-supplied auxiliary SQL command is dispatched verbatim before the first query. This demonstrates a query contract, not execution against any database.',
        'limitations':['Requires reachable exporter with working bootstrap and applicable access controls',
                       'No deployed grants, schema, rows, multi-statements or anonymous reachability tested',
                       'The synthetic audit_fixture names do not refer to application data']}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'total':report['total'],'output':str(output)}))
    raise SystemExit(0 if report['passed']==len(results) else 1)


if __name__=='__main__':
    main()
