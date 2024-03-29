import base64
import io
import os
import random

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import numpy as np
from dash import dcc, ctx
from dash import html
from dash import Dash
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from dash.long_callback import DiskcacheManager

import src.utils.config
from src.front.adapter import graph_to_view
from src.front.view_model import ViewModel
from operator import itemgetter

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

import diskcache

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, external_stylesheets=external_stylesheets)


viewModel = ViewModel()
cards = [
    dbc.Card(
        [
            html.H3("0", className="card-title", id="total_node"),
            html.P("结点数", className="card-text"),
        ],
        body=True,
        inverse=True,
        color="primary",
    ),
    dbc.Card(
        [
            html.H3("0", className="card-title", id="total_edge"),
            html.P("边数", className="card-text"),
        ],
        body=True,
        inverse=True,
        color="primary",
    ),
    dbc.Card(
        [
            html.H3("0", className="card-title", id="connected_component_num"),
            html.P("连通分量数", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="avg_degree"),
            html.P("平均结点度数", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="diameter"),
            html.P("网络直径", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="avg_path_len"),
            html.P("平均路径长度", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ), dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="cluster_co"),
            html.P("聚类系数", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ), dbc.Card(
        [
            html.H3(f"{0:.2f}", className="card-title", id="coreness"),
            html.P("Coreness", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    )
]
panel = dbc.Card(
    [
        html.H5("网络"),
        dcc.Dropdown(
            id="window-dropdown",
            options=[
                {"label": name, "value": value} for name, value in zip(viewModel.names, viewModel.keys)
            ],
            value="rail",
            clearable=False,
            style={"padding": "20 20 20 20"}
        ),
        html.Br(),

    ], body=True
)

view_panel = dbc.Card(
    body=True,
    children=[
        html.H5("显示"),
        html.Br(),
        dbc.Label("布局"),
        dbc.RadioItems(
            className="inline",
            id="layout-radio",
            options=[
                {"label": "COSE", "value": "cose"},
                {"label": "中心", "value": "concentric"},
                {"label": "环状", "value": "circle"},
                {"label": "宽度", "value": "breadthfirst"},
                {"label": "网格", "value": "grid"},
                {"label": "地图", "value": "preset"}
            ],
            labelStyle={
                "display": "inline-block",
                "margin": "2px",
            },
            value="preset",
            inline=True
        ),
        html.Br(), html.Br(),
        dbc.Label(id="degree-slider-label", children="按度数筛选结点:"),
        dcc.RangeSlider(
            id="degree-slider",
            min=0,
            max=70,
            value=[0, 60],
            step=5,
            marks={
                str(int(x)): str(int(x))
                for x in np.linspace(0, 60, 5)
            },
        ),
        html.Br(), html.Br(),
        dbc.Label(id="coreness-input-label", children="按coreness筛选节点:"),
        html.Div([
         dcc.Input(id='coreness-input', type='number', value=0, min=0, max=9, style={'font-size': '10px'})]
        ),
        dbc.Label(id="coreness-input-label", children="查看连通分量:"),
        dcc.Dropdown(
            id='select_team',
            options=[{'label': i, 'value': i} for i in
                     [x for x in range(-1, viewModel.graphs["rail"].get_connected_component_num())]],
            value=-1,
            searchable=True,
            style={'width': '75%'}
        ),
    ]

)

attack_panel = dbc.Card([html.H5("攻击"),
                         html.Br(), dbc.Row(
        [dbc.Col(dbc.Button('随机攻击节点', id='random-attack', color='warning'), width=3.5),
         dbc.Col(dbc.Button('随机攻击边', id='edge-random-attack'), width=3.5),
         dbc.Col(dbc.Button('意图攻击节点', id='intentional-attack', color='danger'), width=3.5),
         dbc.Col(dbc.Button('复原', id='reset', color='success', n_clicks=0,
                            style={'margin-left': '25px'}), width=3.5),
         ]
    )], body=True)


def Header(name, app):
    title = html.H1(name, style={"margin-top": 3, "text-align": "center","color": "teal",  # 设置字体颜色
    "font-weight": "bold",  # 设置字体粗细
    "font-family": "Arial, sans-serif"})
    return dbc.Row([dbc.Col(title, md=12)])


app.layout = dbc.Container(
    style={'backgroundColor': '#f0f8ff'},  # 设置背景颜色为淡蓝色
    children= [
        Header("中国铁路公交网络", app),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [panel, view_panel, attack_panel], width=2,
                ),
                dbc.Col([
                    dbc.Row(
                        [dbc.Col(card) for card in cards]
                    ),
                    cyto.Cytoscape(
                        id='cytoscape',
                        elements=[],
                        layout={'name': 'preset'},
                        style={'width': '100%', 'height': '1000px'},
                        stylesheet=[],
                        responsive=True
                    )
                    ], width=9),
            ]
        ),
        dbc.Col([
            dbc.Row([dbc.Col(dcc.Graph(id='popular_nodes')),
                     dbc.Col(dcc.Graph(id='coreness_nodes'))
                     ]),
            dbc.Row([dbc.Col(dcc.Graph(id='degree_distribution')),
                     dbc.Col(dcc.Graph(id='cluster_nodes'))]),
        ]),
        dbc.Toast(
            id="popover",
            is_open=False,
            style={"position": "fixed", "bottom": 10, "right": 10, "width": 200},
        ),
        html.Div(id="temp"),
    ],
    fluid=True,
)


@app.callback(
    Output("degree-slider-label", "children"),
    Input("degree-slider", "value")
)
def update_label(degree_range):
    return "按度数筛选节点：{}-{}".format(degree_range[0], degree_range[1])


@app.callback(
    Output("cytoscape", "elements"),
    Output("connected_component_num", "children"),
    Output("avg_degree", "children"),
    Output("avg_path_len", "children"),
    Output("cluster_co", "children"),
    Output("coreness", "children"),
    Output("popular_nodes", "figure"),
    Output("coreness_nodes", "figure"),
    Output("degree_distribution", "figure"),
    Output("cluster_nodes", "figure"),
    Output("total_node", "children"),
    Output("total_edge", "children"),
    Output("diameter", "children"),
    Output("select_team", "children"),

    Input("window-dropdown", "value"),
    Input("degree-slider", "value"),
    Input("coreness-input", "value"),
    Input("select_team", "value"),
    Input('random-attack', 'n_clicks'),
    Input("intentional-attack", "n_clicks"),
    Input('reset', 'n_clicks'),
    Input('edge-random-attack', 'n_clicks')
)
def update_figure(book, degree_range, coreness_input, component,
                  random_attack, intentional_attack, reset_click, edge_attack):
    triggered_id = ctx.triggered_id
    graph = viewModel.get_graph(book, triggered_id == 'reset')
    if triggered_id == 'random-attack':
        nodes = random.sample(list(graph.nodes), int(len(graph.nodes) * 0.3))
        graph.remove_nodes([node.id for node in nodes])
        graph.calculate_all_properties()
    if triggered_id == 'edge-random-attack':
        edges = random.sample(list(graph.edges.keys()), int(len(graph.edges) * 0.3))
        graph.remove_edges([edge for edge in edges])
        graph.calculate_all_properties()
    if triggered_id == "intentional-attack":
        nodes_dict = dict(sorted(graph.degrees.items(), key=itemgetter(1), reverse=True))
        nodes = list(nodes_dict.keys())[:int(len(graph.nodes) * 0.3)]
        graph.remove_nodes([node.id for node in nodes])
        graph.calculate_all_properties()
    if coreness_input != 0:
        nodes_dict = {key: value for key, value in graph.degrees.items() if value < coreness_input}
        nodes = list(nodes_dict.keys())
        while nodes:
            graph.remove_nodes([node.id for node in nodes])
            nodes_dict = {key: value for key, value in graph.degrees.items() if value < coreness_input}
            nodes = list(nodes_dict.keys())
        graph.calculate_all_properties()
    ss, e, present_node_num, present_edge_num = graph_to_view(graph, degree_range, coreness_input, component)
    cn = graph.get_low_cluster_nodes()
    cluster = go.Figure(
        data=[go.Bar(x=[n.name for n, _ in cn], y=[ce for _, ce in cn],marker={'color': 'red'})],
        layout_title_text="聚类系数"
    )
    dd = graph.get_degree_distribution()
    degree_dis = go.Figure(
        data=[go.Bar(x=list(dd.keys()), y=list(dd.values()))],
        layout_title_text="度数分布"
    )
    pn = graph.get_popular_nodes()
    popular = go.Figure(
        data=[go.Bar(x=[n.name for n, _ in pn], y=[degree for _, degree in pn], marker={'color': '#004d00'})],
        layout_title_text="结点度数"
    )

    con = graph.get_high_coreness_nodes()
    coreness = go.Figure(
        data=[go.Bar(x=[n.name for n, _ in con], y=[degree for _, degree in con],marker={'color': '#a103fc'})],
        layout_title_text="Coreness"
    )

    nodes_cate = []
    for k, v in graph.get_node_color_map().items():
        nodes_cate.append(
            dbc.Badge(k, color=v, pill=True, className="me-1", style={"margin": "4 4 4 4"}, text_color="white")
        )

    diameter = graph.diameter

    return (e, "{}".format(graph.get_connected_component_num()), "{:.2f}".format(
        graph.get_average_degree()), "{:.2f}".format(
        graph.get_average_path_length()), "{:.2f}".format(
        graph.get_cluster_coefficient()), "{:.2f}".format(graph.get_coreness()),
        popular, coreness, degree_dis, cluster, present_node_num, present_edge_num, diameter,
        graph.get_connected_component_num()
    )


@app.callback(
    Output("cytoscape", "stylesheet"),
    Input("window-dropdown", "value"),
    Input("degree-slider", "value")
)
def update_style(book, degree_range):
    ss = graph_to_view(viewModel.get_graph(book, False), degree_range)[0]
    return ss


@app.callback(
    Output("cytoscape", "layout"),
    Input("layout-radio", "value")
)
def update_layout(type):
    layout = {}
    if type == 'cose':
        layout = {
            'idealEdgeLength': 200,
            'refresh': 20,
            'fit': True,
            'padding': 30,
            'randomize': False,
            'animate': False,
            'componentSpacing': 200,
            'nodeRepulsion': 20000000,
            'nodeOverlap': 500,
            'edgeElasticity': 200,
            'nestingFactor': 5,
            'gravity': 80,
            'numIter': 1000,
            'initialTemp': 300,
            'coolingFactor': 0.99,
            'minTemp': 1.0
        }
    layout["name"] = type
    return layout


@app.callback(Output('popover', 'is_open'),
              Output('popover', 'children'),
              [Input('cytoscape', 'mouseoverNodeData')],
              )
def display_hover_node(data):
    if data:
        node_id = data['id']
        graph = viewModel.current_graph
        node = graph.id_to_node[node_id]
        content = [
            dbc.ListGroupItem([html.Label("{}".format(data['label']), style={"color": "white"})],
                              color=graph.get_node_color_map()[data['id']]),
            dbc.ListGroupItem("度数：{}".format(node.get_degree()))
        ]
        if node in graph.cluster_coefficient.keys():
            content.append(dbc.ListGroupItem("聚类系数：{}".format(graph.cluster_coefficient[node])))
        if node in graph.coreness.keys():
            content.append(dbc.ListGroupItem("Coreness：{}".format(graph.coreness[node])))
        return True, content
    return False, []


# @app.callback(
#     Output("upload-label", "children"),
#     Output("window-dropdown", "options"),
#     Output("window-dropdown", "value"),
#     Input('add_graph', 'n_clicks'),
#     background =True,
#     prevent_initial_call=True,
#     running=[
#         (Output("add_graph", "disabled"), True, False),
#         (Output("loading-output", "children"), "导入并建模中...需要点时间", "导入完成"),
#     ], manager=background_callback_manager)
# def add_graph(a):
#     key = viewModel.upload_key
#     dir = src.utils.config.raw_path + viewModel.upload_key + "/"
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#     with open(src.utils.config.raw_path + "{}/{}.txt".format(viewModel.upload_key, viewModel.upload_key), "w+") as f:
#         f.write(viewModel.upload_content)
#     if os.path.exists('backend/model/cache/{}.pkl'.format(key)):
#         os.remove('backend/model/cache/{}.pkl'.format(key))
#     generate_novel_graph(key)
#     viewModel.add_graph(key)
#     viewModel.upload_content = None
#     viewModel.upload_key = None
#     viewModel.ready_upload = False
#     return "", [{"label": name, "value": value} for name, value in zip(viewModel.names, viewModel.keys)], key


@app.callback(
    Output('upload-buttons', 'is_open'),
    Output('upload-result', 'children'),
    Input('upload', 'contents'),
    Input('upload_cancel', 'n_clicks'),
    Input('upload-label', 'children'),
    State('upload', 'filename'))
def update_output(list_of_contents, upload_cancel, upload_label, list_of_names):
    trigger_id = ctx.triggered_id
    if trigger_id == 'upload_cancel' or trigger_id == 'upload-label':
        viewModel.upload_content = None
        viewModel.ready_upload = False
        return False, ""
    elif trigger_id == "upload" and list_of_contents is not None:
        return parse_contents(list_of_contents, list_of_names)
    return viewModel.ready_upload, ""


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    contents = ""
    key = filename.split(".")[0]
    try:
        for line in io.StringIO(decoded.decode('utf-8')).readlines():
            contents += line
        viewModel.upload_content = contents
        viewModel.ready_upload = True
        viewModel.upload_key = key
    except Exception:
        viewModel.ready_upload = False
        return False, html.Div([
            'There was an error processing this file.'
        ])
    return True, html.Div([
        html.H5(key),
        html.Pre(contents[0:100] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])