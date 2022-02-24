## create randomm graph
import plotly.graph_objects as go
import networkx as nx
import random
import math

#################################################################
####just need to make networkx graph out of data from website####
def add_coordinates(graph):
    '''adds x and y coordinate to each course node in the graph to make it
    readable. Finds distance from 18.01, then arranges nodes radially outwards'''
    ###choose gateway class
    start = '18.01'
    shortest_path_lengths = nx.shortest_path_length(graph, start)
    predecessors = nx.predecessor(graph, start)
    levels = {0:[(start, None)]}
    for course in shortest_path_lengths:
        if course != start:
            dist = shortest_path_lengths[course]
            try:
                levels[dist].append((course,predecessors[course][-1]))
            except:
                levels[dist] = [(course,predecessors[course][-1])]
    for dist in levels:
        if dist != 0:
            levels[dist].sort(key=lambda s: ''.join(i for i in s[0] if i.isdigit() or i == '.'))
            levels[dist].sort(key=lambda s: ''.join(i for i in s[1] if i.isdigit() or i == '.'))
    k = -1
    t = len(shortest_path_lengths)
    for dist in range(max(levels)+1):
        level = levels[dist]
        k += len(level)
        # r = k
        for i in range(len(level)):
            # theta = -math.pi/2 + math.pi * (i/(len(level)))
            # x = r * math.cos(theta)
            # y = r * math.sin(theta)
            x = k
            y = -(t/2) + t*i/len(level)
            graph.nodes[level[i][0]]['pos'] = (x,y)
    for course in graph.nodes:
        if course not in shortest_path_lengths:
            a = k
            x = 0
            val = float(''.join(i for i in course if i.isdigit() or i == '.'))
            y = a/2 - a * (val-int(val))
            graph.nodes[course]['pos'] = (x,y)
    return graph

def build_graph(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return add_coordinates(G)

#################################################################

def draw(G):
    ## add edges
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    ## color nodes
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        # print(node, adjacencies)
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('Course: '+ adjacencies[0])
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    ## create graph
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='<br>MIT Curriculum Map',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()
