"""Token-only PHP call/signature census. Never evaluates source or loads bootstrap."""

import argparse
import json
import shutil
from pathlib import Path

from collect_master import git, own, tree, write_json
from security_probes import php_value, run_php

MASTER = 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707'

PARSER = r'''
function arity($ts,$start,$definition) {
    $depth=0; $n=0; $present=false; $default=false; $required=0; $dynamic=false;
    for($j=$start+1;$j<count($ts);$j++) {
        $t=$ts[$j]; $s=is_array($t)?$t[1]:$t;
        if(!is_array($t) && $s===')' && $depth===0) {
            if($present) { $n++; if(!$default) $required=$n; }
            return [$n,$required,$dynamic];
        }
        if(!is_array($t) && $s===',' && $depth===0) {
            $n++; if(!$default) $required=$n; $present=false; $default=false; continue;
        }
        if(!is_array($t) && in_array($s,['(','[','{'])) $depth++;
        if(is_array($t) && in_array($t[0],[T_CURLY_OPEN,T_DOLLAR_OPEN_CURLY_BRACES])) $depth++;
        if(!is_array($t) && in_array($s,[')',']','}'])) $depth--;
        if(!is_array($t) && $s==='=' && $depth===0) $default=true;
        if(is_array($t) && $t[0]===T_ELLIPSIS) $dynamic=true;
        $present=true;
    }
    return null;
}
$out=['definitions'=>[], 'calls'=>[], 'ambiguous_files'=>[]];
foreach($files as $path=>$source) {
    $raw=token_get_all($source); $ts=[]; $line=1;
    foreach($raw as $t) {
        $s=is_array($t)?$t[1]:$t;
        if(!is_array($t) || !in_array($t[0],[T_WHITESPACE,T_COMMENT,T_DOC_COMMENT]))
            $ts[]=['t'=>$t,'line'=>$line];
        $line+=substr_count($s,"\n");
    }
    $plain=array_column($ts,'t'); $classes=[];
    for($i=0;$i<count($plain);$i++) {
        $t=$plain[$i];
        if(is_array($t) && $t[0]===T_CLASS && isset($plain[$i+1]) && is_array($plain[$i+1]) && $plain[$i+1][0]===T_STRING)
            $classes[]=$plain[$i+1][1];
    }
    if(count($classes)>1) { $out['ambiguous_files'][]=$path; continue; }
    $class=$classes[0]??null;
    for($i=0;$i<count($plain);$i++) {
        $t=$plain[$i];
        if(is_array($t) && $t[0]===T_FUNCTION && $class) {
            $j=$i+1; if(($plain[$j]??null)==='&') $j++;
            if(isset($plain[$j+1]) && is_array($plain[$j]) && $plain[$j][0]===T_STRING && $plain[$j+1]==='(') {
                $a=arity($plain,$j+1,true);
                if($a===null) { $out['ambiguous_files'][]=$path; continue; }
                $out['definitions'][]=['class'=>$class,'method'=>$plain[$j][1],'required'=>$a[1],'parameters'=>$a[0],'variadic'=>$a[2],'path'=>$path,'line'=>$ts[$i]['line']];
            }
        }
        if(is_array($t) && $t[0]===T_STRING && isset($plain[$i+3]) && is_array($plain[$i+1]) && $plain[$i+1][0]===T_DOUBLE_COLON && is_array($plain[$i+2]) && $plain[$i+2][0]===T_STRING && $plain[$i+3]==='(') {
            $target=strtolower($t[1])==='self'?$class:$t[1];
            if(!$target || in_array(strtolower($target),['parent','static'])) continue;
            $a=arity($plain,$i+3,false);
            if($a===null) { $out['ambiguous_files'][]=$path; continue; }
            $out['calls'][]=['class'=>$target,'method'=>$plain[$i+2][1],'arguments'=>$a[0],'unpacked'=>$a[2],'path'=>$path,'line'=>$ts[$i]['line']];
        }
    }
}
echo json_encode($out);
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    source = Path(args.source).resolve()
    if git(source, 'rev-parse', 'HEAD').decode().strip() != MASTER:
        raise ValueError('Wrong source pin')
    files = {p: (source/p).read_text(encoding='utf-8-sig', errors='replace')
             for p in sorted(tree(source, MASTER)) if own(p) and p.endswith('.php') and (source/p).is_file()}
    result = json.loads(run_php(shutil.which('php'), '$files='+php_value(files)+';'+PARSER, short_open_tag=True))
    controls = []
    fixtures = [
        ('nested_arguments', '<?php class Fixture {function f($a,$b=null){} function run(){self::f([1,2],g(1,2));}}', [1, 2, 2]),
        ('commas_in_strings', '<?php class Fixture {function f($a,$b="x,y"){} function run(){self::f("a,b");}}', [1, 2, 1]),
        ('optional_array_default', '<?php class Fixture {function f($a,$b=[1,2]){} function run(){/*self::f();*/self::f(1);}}', [1, 2, 1]),
    ]
    for name, fixture, expected in fixtures:
        control = json.loads(run_php(shutil.which('php'), '$files='+php_value({'fixture.php': fixture})+';'+PARSER))
        definition = next(d for d in control['definitions'] if d['method'] == 'f')
        actual = [definition['required'], definition['parameters'], control['calls'][0]['arguments']]
        controls.append({'case': name, 'expected': expected, 'actual': actual,
                         'status': 'pass' if actual == expected and len(control['calls']) == 1 else 'fail'})
    if any(c['status'] != 'pass' for c in controls):
        raise ValueError('Arity token controls failed')
    definitions = {}
    for d in result['definitions']:
        definitions.setdefault((d['class'].lower(), d['method'].lower()), []).append(d)
    mismatches, resolved = [], 0
    for c in result['calls']:
        candidates = definitions.get((c['class'].lower(), c['method'].lower()), [])
        if len(candidates) != 1 or c['unpacked']:
            continue
        d = candidates[0]
        resolved += 1
        if c['arguments'] < d['required']:
            mismatches.append({'call': c, 'definition': d, 'status': 'candidate_requires_control_flow_review'})
    result.update({'source_commit': MASTER, 'technique': 'php_token_only_literal_static_call_arity',
                   'files': len(files), 'short_open_tag': True, 'resolved_calls': resolved, 'missing_argument_candidates': mismatches,
                   'negative_controls': controls,
                   'application_code_executed': False, 'database_access': False, 'network_access': False,
                   'limitations': ['Only literal static calls; not dynamic/object dispatch',
                                  'Files with multiple classes excluded; signatures with duplicate keys unresolved',
                                  'Reachability, error recovery and production PHP version require separate review']})
    path = Path(__file__).resolve().parents[2]/'source-audits/master/2026-11-18/iterative/static-arity-review.json'
    write_json(path, result)
    print(json.dumps({'files': len(files), 'definitions': len(result['definitions']), 'resolved_calls': resolved,
                      'missing_argument_candidates': mismatches}, ensure_ascii=True))


if __name__ == '__main__':
    main()
