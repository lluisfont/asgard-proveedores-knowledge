"""Render the local AST graph and a compact report without semantic API calls."""

import gzip
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx
from graphify.analyze import god_nodes
from graphify.export import to_html


def main():
    root=Path(__file__).resolve().parents[2]
    folder=root/'source-audits/master/2026-11-18/graphify'
    data=json.loads(gzip.decompress((folder/'graph.json.gz').read_bytes()))
    graph=nx.node_link_graph(data,edges='links')
    communities=defaultdict(list)
    for node in data['nodes']:
        communities[node.get('community',-1)].append(node['id'])
    to_html(graph,dict(communities),str(folder/'graph.html'),node_limit=5000)
    hubs=god_nodes(graph,top_n=12)
    lines=['# Graphify master: AST local','','Fuente: master a8ce2c23dead8552d2c4699e4a9b9134f7a18707.',
           '',f"{graph.number_of_nodes()} nodos; {graph.number_of_edges()} aristas; {len(communities)} comunidades.",
           '', 'Se seleccionaron 545 archivos de codigo tras exclusiones de dependencias conocidas. '
           'La extraccion advirtio que 319 solo generan un nodo de fichero sin simbolos. '
           'Consultar tambien los catalogos PHP/AJAX, campos y referencias SQL.',
           '', 'Coste de extraccion semantica: 0 tokens de entrada y 0 de salida. '
           'No se ejecuto una API de lenguaje para construir este grafo. La revision funcional '
           'y el glosario se documentan aparte con referencias de fuente.',
           '', '## Nodos conectados','','| Etiqueta | Grado | Fuente |','| --- | ---: | --- |']
    for hub in hubs:
        node_id=hub.get('id',hub.get('node'))
        attrs=graph.nodes[node_id] if node_id in graph else hub
        label=str(attrs.get('label',node_id)).replace('|','\\|')
        source=str(attrs.get('source_file','')).replace('|','\\|')
        degree=graph.degree(node_id) if node_id in graph else hub.get('degree','')
        lines.append(f'| {label} | {degree} | {source} |')
    lines+=['','## Uso y limites','',
            'La visualizacion es `graph.html`; los datos completos son `graph.json.gz`. '
            'Una conexion AST no valida ejecucion, autorizacion ni equivalencia de negocio entre paises. '
            'La configuracion y los submodulos externos siguen fuera de la comprobacion de despliegue.',
            '', 'Para consultar con Graphify, restaurar primero graph.json usando el helper del paquete '
            'y pasar la ruta con --graph. Los simbolos seleccionados deben corresponder a archivos '
            'del alcance; las comunidades no son requisitos ni dominios de negocio confirmados.']
    (folder/'GRAPH_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Rendered local AST graph and report')


if __name__=='__main__':
    main()
