import networkx as nx
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from nodes import *
from edges import *

init_notebook_mode(connected=True)

class EasyGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.node = Node(self.G)
        self.edge = Edge()
        self.show_scale = False

    def add_edge(self, from_node, to_node, attributes=None):
        """
           Add edges to the graph.
           Params:
               from_node: initial node
               to_node: destination node
               attributes (optional): dicionary with keys and its corresponding values
        """
        self.G.add_edge(from_node, to_node)
        if attributes is not None:
            for k, v in attributes.items():
                self.G.edges[(from_node,to_node)][k]=v


    def __set_edge(self):
        self.edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5,color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in self.G.edges():
            x0, y0 = self.G.node[edge[0]]['pos']
            x1, y1 = self.G.node[edge[1]]['pos']
            self.edge_trace['x'] += tuple([x0, x1, None])
            self.edge_trace['y'] += tuple([y0, y1, None])



    def __get_node_color_params(self, node_color_col):
        color = []
        if node_color_col is not None:
            for node in self.G.nodes:
                color.append(self.G.nodes[node][node_color_col])
        else:
            #color = [self.default_node_size]*len(self.G.nodes)
            color = self.default_node_color
        return color


    def __set_anotations(self):
        self.annotations = []
        for node in self.G.nodes():
            x, y = self.G.node[node]['pos']
            self.node_trace['x'] += tuple([x])
            self.node_trace['y'] += tuple([y])
            self.annotations.append(
                dict(
                    x=x,
                    y=y+0.10,
                    xref='x',
                    yref='y',
                    text=node,
                    showarrow=False,
                    ax=0,
                    ay=20
                )
            )

    def __set_layout(self, title=''):
        self.layout = go.Layout(
            showlegend=False,
            annotations=self.annotations,
            title=title,
            titlefont=dict(size=16),
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

    def __set_plot(self, node_color_col, node_label=''):
        if node_color_col is not None:
            try:
                for g in self.G.nodes:
                    if self.G.nodes[g][node_color_col] < self.node.cmin:
                        self.node.cmin = self.G.nodes[g][node_color_col]
                    if self.G.nodes[g][node_color_col] > self.node.cmax:
                        self.node.cmax = self.G.nodes[g][node_color_col]
            except:
                raise

        for node, adjacencies in enumerate(self.G.adjacency()):
            if node_color_col is None:
                self.node_trace['marker']['color'] =  self.default_node_color
            else:
                self.node_trace['marker']['color'] =  self.G.nodes[list(self.G.nodes.keys())[node]][node_color_col]
            if node_color_col is not None:
                node_info = node_label +' '+ str(self.G.nodes[list(self.G.nodes.keys())[node]][node_color_col])
                self.node_trace['text']+=tuple([node_info])

    def __plot(self):
        fig = go.Figure(data=[self.edge_trace, self.node_trace],layout=self.layout)
        iplot(fig, filename='networkx')

    def plot(self, title=' ', node_label = '', label = ' ', node_size_col=None, node_color_col=None):
        self.node.set_pos()
        self.__set_edge()
        self.node.set_node(title, node_size_col, node_color_col)
        self.__set_anotations()
        self.__set_layout(title)
        self.__set_plot(node_color_col, node_label)
        self.__plot()
