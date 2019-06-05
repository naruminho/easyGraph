import networkx as nx
import plotly.graph_objs as go

class Node:
    def __init__(self, G):
        self.G = G
        self.size = 10
        self.sizemin = self.size
        self.default_color = 'darkblue'
        self.cmin = 10e1000
        self.cmax = -10e1000
        self.show_scale = False

    def add(self, name, attributes=None):
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
        if node_size_col is not None:
            self.size = []
            for node in self.G.nodes:
                self.size.append(self.G.nodes[node][node_size_col])
            self.sizeref = 2.*max(self.size)/(40.**2)
        else:
            self.size = [1]*len(self.G.nodes)
            self.sizeref = self.sizemin

    def get_color_params(self, node_color_col):
        color = []
        if node_color_col is not None:
            for node in self.G.nodes:
                color.append(self.G.nodes[node][node_color_col])
        else:
            #color = [self.default_node_size]*len(self.G.nodes)
            color = self.default_node_color
        return color

    def set_node(self, title, node_size_col, node_color_col):
        self.get_size_params(node_size_col)
        print(self.size)
        color = self.get_color_params(node_color_col)
        self.settings = go.Scatter(
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
                cmax = self.cmax,
                cmin = self.cmin,
                size = self.size,
                sizemode='area',
                sizeref=self.sizeref,
                sizemin=self.sizemin,
                colorbar=dict(
                    thickness=15,
                    title=title,
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))


    def set_anotations(self):
        self.annotations = []
        for node in self.G.nodes():
            x, y = self.G.node[node]['pos']
            self.settings['x'] += tuple([x])
            self.settings['y'] += tuple([y])
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

    def set_layout(self, title=''):
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
