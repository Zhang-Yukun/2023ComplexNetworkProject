from src.utils.color import random_color


def graph_to_view(graph, degree_range=None, coreness_low_bound=0, component=-1):
    if degree_range is None:
        degree_range = [0, 60]
    min_degree = 0
    max_degree = 1
    max_weight = 1
    degrees = list(graph.degrees.values())
    weights = list(graph.edges.values())
    if degrees:
        min_degree = min(degrees)
        max_degree = max(degrees)
    if weights:
        max_weight = max(weights)
    if max_degree == 0:
        max_degree = 1
    elements = []
    if component == -1:
        for node in graph.nodes:
            if degree_range[1] >= node.get_degree() >= degree_range[0]:
                degree = (float(node.get_degree() - min_degree) / max_degree)
                elements.append(
                    {"data": {"id": str(node.id), "label": node.name, 'class_name': node.name,
                              'font_size': str(50 if 200 * degree < 50 else 200 * degree) + "px",
                              'node_degree': 200 if 500 * degree < 200 else 500 * degree},
                     "position": {"x": 500 * float(node.longitude), "y": -600 * float(node.latitude)}})
        present_node_num = len(elements)
        for fe, tes in graph.edges.items():
            fen = graph.id_to_node[fe[0]]
            ten = graph.id_to_node[fe[1]]
            dom = fen if fen.get_degree() > ten.get_degree() else ten
            elements.append({"data": {"source": str(fe[0]), "target": str(fe[1]), "weight": tes,
                                      "lineWidth": 100 * ((float(tes)) / max_weight),
                                      "dom_class_name": dom.id}})
        present_edge_num = len(elements) - present_node_num
    else:
        if component in graph.connected_components_set.keys():
            for node in graph.connected_components_set[component]:
                if degree_range[1] >= node.get_degree() >= degree_range[0]:
                    degree = (float(node.get_degree() - min_degree) / max_degree)
                    elements.append(
                        {"data": {"id": str(node.id), "label": node.name, 'class_name': node.name,
                                  'font_size': str(50 if 200 * degree < 50 else 200 * degree) + "px",
                                  'node_degree': 200 if 500 * degree < 100 else 200 * degree},
                         "position": {"x": 800 * float(node.longitude), "y": -1400 * float(node.latitude)}})
            present_node_num = len(elements)
            for fe, tes in graph.edges.items():
                fen = graph.id_to_node[fe[0]]
                ten = graph.id_to_node[fe[1]]
                if (fen not in graph.connected_components_set[component]
                        or ten not in graph.connected_components_set[component]):
                    continue
                dom = fen if fen.get_degree() > ten.get_degree() else ten
                elements.append({"data": {"source": str(fe[0]), "target": str(fe[1]), "weight": tes,
                                          "lineWidth": 100 * ((float(tes)) / max_weight),
                                          "dom_class_name": dom.id}})
            present_edge_num = len(elements) - present_node_num

    ss = [
        {'selector': 'node',
         'style': {
             'label': 'data(label)',
             'font-size': 'data(font_size)',
             'width': 'data(node_degree)',  # 根据节点的degree标签设置节点大小
             'height': 'data(node_degree)'  # 根据节点的degree标签设置节点大小
         }},
        {'selector': 'edge',
         'style': {
             "curve-style": "bezier",
             'width': 'data(lineWidth)',
             'line-opacity': "60%"
         }}]

    for fn, cl in graph.get_node_color_map().items():
        ss.append(
            {'selector': '[id *= "{}"]'.format(fn),
             'style': {
                 'background-color': '{}'.format(cl),

             }}
        )
        ss.append({'selector': '[dom_class_name *= "{}"]'.format(fn),
                   'style': {
                       'line-color': '{}'.format(cl),
                   }})

    return ss, elements, present_node_num, present_edge_num
