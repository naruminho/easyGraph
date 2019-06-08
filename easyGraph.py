import networkx as nx
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from nodes import *
from edges import *

init_notebook_mode(connected=True)

class EasyGraph:
    def __init__(self, layout = 1, dim=2):
        self.G = nx.Graph()
        self.dim = dim
        self.node = Node(self.G, dim)
        self.edge = Edge(self.G)
        self.layout = layout

    def __plot(self):
        data = [self.node.settings]
        data.extend(self.edge.settings)
        fig = go.Figure(data=data,layout=self.node.layout)
        iplot(fig)
#        plot(fig, filename='networkx.html')


    def plot(self, title=' ', node_size_col=None, node_color_col=None, edge_color_col=None, hover_col='all_col'):
        self.node.title = title
        self.node.set_pos(self.layout, self.dim)
        self.node.set_size_attribute(node_size_col, node_color_col)
        self.node.set_layout(title)
        self.node.set_color_attribute(node_color_col)
        self.node.set_hover_attribute(hover_col)
        self.edge.set_color_attribute(edge_color_col)
        self.__plot()

    # def save
