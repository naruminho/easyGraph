import networkx as nx
from egfuncs import *
import plotly.graph_objs as go
import copy

class Edge:
    def __init__(self, G):
        self.G = G
        self.default_color = 'black'
        self.cmin = 10e1000
        self.cmax = -10e1000

    def add(self, from_node, to_node, attributes=None):
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

    # def get_color_params(self, color_col):
    #     if color_col is None:
    #         color = self.default_color
    #     else:
    #         color = []
    #         for edge in self.G.edges:
    #             #color.append(self.G.edges[edge][color_col])
    #             color.append('black')
    #     return color

    def get_cmin_cmax(self, attribute):
        try:
            for g in self.G.edges:
                if self.G.edges[g][attribute] < self.cmin:
                    self.cmin = self.G.edges[g][attribute]
                if self.G.edges[g][attribute] > self.cmax:
                    self.cmax = self.G.edges[g][attribute]
        except:
            raise

    def set_color_attribute(self, color_col):
        if color_col is not None:
            self.get_cmin_cmax(color_col)

        self.settings = []
        trace_default = go.Scatter(
            x=[],
            y=[],
            line=dict(
                width=0.5,
                color=self.default_color,
            ),
            hoverinfo='none',
            mode='lines'
        )
        trace = copy.deepcopy(trace_default)
        for edge in self.G.edges():
            x0, y0 = self.G.node[edge[0]]['pos']
            x1, y1 = self.G.node[edge[1]]['pos']
            trace['x'] = tuple([x0, x1, None])
            trace['y'] = tuple([y0, y1, None])
            if color_col == None:
                color = self.default_color
            else:
                nvalue = self.G.edges[edge][color_col]
                pvalue = (nvalue - self.cmin)/(self.cmax-self.cmin)
                color = get_color(pvalue)[1]
            trace['line'] = dict(width=0.5,color=color)
            self.settings.append(copy.deepcopy(trace))
