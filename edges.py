import networkx as nx
import plotly.graph_objs as go

class Edge:
    def __init__(self, G):
        self.G = G
        self.default_color = 'black'

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

    def set_color_attribute(self, color_col):

        self.settings = go.Scatter(
            x=[],
            y=[],
            line=dict(
                width=0.5,
                color=self.default_color,
            ),
            hoverinfo='none',
            mode='lines'
        )

        for edge in self.G.edges():
            x0, y0 = self.G.node[edge[0]]['pos']
            x1, y1 = self.G.node[edge[1]]['pos']
            self.settings['x'] += tuple([x0, x1, None])
            self.settings['y'] += tuple([y0, y1, None])
