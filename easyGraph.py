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
        self.edge = Edge(self.G)

    def __plot(self):
        fig = go.Figure(data=[self.node.settings, self.edge.settings],layout=self.node.layout)
        iplot(fig, filename='networkx')

    def plot(self, title=' ', node_size_col=None, node_color_col=None, edge_color_col=None, hover_col=None):
        self.node.title = title
        self.node.set_pos()
        self.node.set_size_attribute(node_size_col, node_color_col)
        self.node.set_layout(title)
        self.node.set_color_attribute(node_color_col)
        self.node.set_hover_attribute(hover_col)
        self.edge.set_color_attribute(node_color_col)

        self.__plot()
