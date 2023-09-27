from src.utils.color import random_color


def graph_to_view(graph, degree_range=None):
    if degree_range is None:
        degree_range = [0, 1000]
    elements = []
    for node in graph.nodes:
        if degree_range[1] >= node.get_degree() >= degree_range[0]:
            elements.append(
                {"data": {"id": str(node.id), "label": node.id, 'class_name': node.id,
                          'node_degree': 500*((float(node.get_degree())-0.9)/56)},
                 "position": {"x": float(node.longitude), "y": float(node.latitude)}})
    print(elements)
    for fe, tes in graph.edges.items():
        fen = graph.id_to_node[fe[0]]
        ten = graph.id_to_node[fe[1]]
        if (degree_range[1] < fen.get_degree() or fen.get_degree() < degree_range[0]
                or degree_range[1] < ten.get_degree() or ten.get_degree() < degree_range[0]):
            continue
        dom = fen if fen.get_degree() > ten.get_degree() else ten
        elements.append({"data": {"source": str(fe[0]), "target": str(fe[1]), "weight": tes,
                                  "dom_class_name": dom.id}})
    ss = [
        {'selector': 'node',
         'style': {
             'label': 'data(label)',
             'width': 'data(node_degree)',  # 根据节点的degree标签设置节点大小
             'height': 'data(node_degree)'  # 根据节点的degree标签设置节点大小
         }},
        {'selector': 'edge',
         'style': {
             "curve-style": "bezier",
             'width': "2px",
             'line-opacity': "50%"
         }}]

    for fn, cl in graph.get_node_color_map().items():

        ss.append(
            {'selector': '[class_name *= "{}"]'.format(fn),
             'style': {
                 'background-color': '{}'.format(cl),

             }}
        )
        ss.append({'selector': '[dom_class_name *= "{}"]'.format(fn),
                   'style': {
                       'line-color': '{}'.format(cl),
                   }})
    return ss, elements
