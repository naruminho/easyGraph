import networkx as nx

class Node:
    def __init__(self, G):
        self.G = G
        self.size = 10
        self.default_color = 'darkblue'
        self.cmin = 10e1000
        self.cmax = -10e1000

    def add_node(self, name, attributes=None):
        """
           Add nodes to the graph.
           Params:
               node_name: node id
               attributes (optional): dicionary with keys and its corresponding values
        """
        self.G.add_node(name)
        if attributes is not None:
            for k, v in attributes.items():
                self.G.nodes[name][k]=v

    def set_pos(self):
        self.pos = nx.circular_layout(self.G)
        self.G.add_nodes_from([(k[0], {'pos':[k[1][0],k[1][1]]}) for k in self.pos.items()])

    def get_size_params(self, node_size_col):
        size = []
        if node_size_col is not None:
            for node in self.G.nodes:
                size.append(self.G.nodes[node][node_size_col])
            sizeref = 2.*max(size)/(40.**2)
        else:
            size = [1]*len(self.G.nodes)
            sizeref = self.size
        return size, sizeref

    def set_node(self, title, node_size_col, node_color_col):
        size, sizeref = self.get_size_params(node_size_col)
        color = self.get_color_params(node_color_col)
        self.node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=self.show_scale,
                #colorscale='YlGnBu',
                colorscale='Viridis',
                reversescale=True,
                color=color,
                cmax = self.node.cmax,
                cmin = self.node.cmin,
                size=size,
                sizemode='area',
                sizeref=sizeref,
                sizemin=self.node.size,
                colorbar=dict(
                    thickness=15,
                    title=title,
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))
