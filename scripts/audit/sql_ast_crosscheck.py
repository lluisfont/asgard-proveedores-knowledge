"""Cross-check lexical table candidates with MySQL ASTs; never store SQL literals or execute SQL."""

import argparse
import csv
import hashlib
import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path

from collect_master import git, own, tree, write_json, write_csv


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--parser-path',help='Optional isolated pip --target directory containing sqlglot')
    args=parser.parse_args()
    if args.parser_path:
        sys.path.insert(0,str(Path(args.parser_path).resolve()))
    import sqlglot
    from sqlglot import exp
    if sqlglot.__version__ != '30.33.0':
        raise ValueError('This pinned audit requires sqlglot 30.33.0; review deltas before changing parser version')
    from brownfield_refactor_kit.core import _mask_code_comments_preserve_layout, _iter_code_sql_fragments
    logging.getLogger('sqlglot').setLevel(logging.ERROR)
    source=Path(args.source).resolve()
    root=Path(__file__).resolve().parents[2]
    commit=git(source,'rev-parse','HEAD').decode().strip()
    if commit!='a8ce2c23dead8552d2c4699e4a9b9134f7a18707':
        raise ValueError('Source must match the pinned audit')
    allowed=(exp.Select,exp.Union,exp.Insert,exp.Update,exp.Delete,exp.Create,exp.Drop,exp.Replace)
    fragments=[]
    references=[]
    def tables_in(statement):
        aliases={item.alias_or_name for item in statement.find_all(exp.CTE)}
        return sorted({item.name for item in statement.find_all(exp.Table)
                       if item.name and item.name not in aliases and not any(x in item.name for x in ('$','{','}'))})
    for relative in sorted(tree(source,'master')):
        path=source/relative
        if not own(relative) or path.suffix not in {'.php','.js'} or not path.is_file():
            continue
        content=path.read_text(encoding='utf-8-sig',errors='replace')
        masked=_mask_code_comments_preserve_layout(content,path)
        for text,start,end,confidence in _iter_code_sql_fragments(path,masked):
            if not re.search(r'\b(SELECT|INSERT|REPLACE|UPDATE|DELETE|CREATE|DROP)\b',text,re.I):
                continue
            line_start=masked.count('\n',0,start)+1
            line_end=line_start+text.count('\n')
            fragment_id=hashlib.sha256((relative+':'+str(start)+':'+text).encode()).hexdigest()[:18]
            record={'id':fragment_id,'path':relative,'line_start':line_start,'line_end':line_end,
                    'confidence':confidence,'sql_sha256':hashlib.sha256(text.encode()).hexdigest()}
            try:
                statements=sqlglot.parse(text,read='mysql')
                if not statements or not all(isinstance(s,allowed) for s in statements):
                    record.update({'status':'unsupported_or_non_sql_fragment','tables':[]})
                else:
                    names=sorted({name for statement in statements for name in tables_in(statement)})
                    record.update({'status':'parsed_mysql_ast','tables':names})
                    for name in names:
                        references.append({'path':relative,'line_start':line_start,'line_end':line_end,
                            'table':name,'fragment_id':fragment_id,'confidence':confidence,
                            'commit':commit,'validation':'table_node_in_parsed_mysql_ast_not_deployed_schema'})
            except Exception as error:
                record.update({'status':'unresolved_fragment','tables':[],'error_type':type(error).__name__})
            fragments.append(record)
    controls=[
        ('trim_column_is_not_a_table',"SELECT TRIM(TRAILING ' TN' FROM capacidad) FROM tck_capacidadestransporte",['tck_capacidadestransporte']),
        ('cte_alias_is_not_a_physical_table',"WITH selected AS (SELECT id FROM source_table) SELECT id FROM selected",['source_table']),
        ('quoted_word_is_not_a_table',"SELECT 'from the selected all failed' AS note FROM actual_table",['actual_table']),
    ]
    tests=[]
    for name,statement,expected in controls:
        found=tables_in(sqlglot.parse_one(statement,read='mysql'))
        tests.append({'case':name,'expected':expected,'actual':found,'status':'pass' if expected==found else 'fail'})
    old_path=root/'source-audits/master/2026-11-18/sql-references.csv'
    old=list(csv.DictReader(old_path.open(encoding='utf-8',newline='')))
    lexical_names={r['table'] for r in old}
    ast_names={r['table'] for r in references}
    output=root/'source-audits/master/2026-11-18/iterative'
    write_json(output/'sql-ast-fragments.json',{'source_commit':commit,'parser':'sqlglot',
        'parser_version':sqlglot.__version__,'dialect':'mysql','fragments':fragments,
        'note':'No SQL text is persisted. Unresolved fragments remain outside the AST subset, not declarations of absence.'})
    write_csv(output/'sql-ast-references.csv',references,
        ['path','line_start','line_end','table','fragment_id','confidence','commit','validation'])
    summary={'source_commit':commit,'technique':'sql_dialect_ast_vs_lexical_token_inventory',
        'parser_version':sqlglot.__version__,'fragments':len(fragments),
        'fragment_statuses':dict(Counter(f['status'] for f in fragments)),
        'ast_table_names':len(ast_names),'lexical_table_names':len(lexical_names),
        'not_reproduced_by_ast':sorted(lexical_names-ast_names),'ast_additional_names':sorted(ast_names-lexical_names),
        'negative_controls':tests,'network_access':False,'database_access':False,
        'limitation':'AST interpretation is a stricter subset, not a complete query reconstruction or physical schema verification.'}
    write_json(output/'sql-ast-summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='negative_controls'},indent=2))
    raise SystemExit(0 if all(t['status']=='pass' for t in tests) else 1)


if __name__=='__main__':
    main()
