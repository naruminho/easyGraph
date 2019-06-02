import networkx as nx
import matplotlib as mpl
import matplotlib.cm as cm
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

class EasyGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.vmin = 10e1000
        self.vmax = -10e1000

    def add_node(self, node_name, attributes=None):
        """
           Add nodes to the graph.
           Params:
               node_name: node id
               attributes (optional): dicionary with keys and its correspond values
        """
        self.G.add_node(node_name)
        if attributes is not None:
            for k, v in attributes.items():
                self.G.nodes[node_name][k]=v

    def add_edge(self, from_node, to_node, attributes=None):
        """
           Add edges to the graph.
           Params:
               from_node: initial node
               to_node: dest node
               attributes (optional): dicionary with keys and its correspond values
        """
        self.G.add_edge(from_node, to_node)
        if attributes is not None:
            for k, v in attributes.items():
                self.G.edges[(from_node,to_node)][k]=v

    def __set_pos(self):
        self.pos = nx.circular_layout(self.G)
        self.G.add_nodes_from([(k[0], {'pos':[k[1][0],k[1][1]]}) for k in self.pos.items()])

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

    def __set_node(self, title=''):
        self.node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title=title,
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

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

    def __set_plot(self, field, node_label=''):
        try:
            for g in self.G.nodes:
                if self.G.nodes[g][field] < self.vmin:
                    self.vmin = self.G.nodes[g][field]
                if self.G.nodes[g][field] > self.vmax:
                    self.vmax = self.G.nodes[g][field]
        except:
            raise

        norm = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        cmap = cm.hot
        m = cm.ScalarMappable(norm=norm, cmap=cmap)

        for node, adjacencies in enumerate(self.G.adjacency()):
            self.node_trace['marker']['color'] =  m.to_rgba(self.G.nodes[list(self.G.nodes.keys())[node]][field])
            node_info = node_label +' '+ str(self.G.nodes[list(self.G.nodes.keys())[node]][field])
            self.node_trace['text']+=tuple([node_info])

    def __plot(self):
        fig = go.Figure(data=[self.edge_trace, self.node_trace],layout=self.layout)
        iplot(fig, filename='networkx')

    def plot(self, field, title=' ', node_label = '', label = ' '):
        self.__set_pos()
        self.__set_edge()
        self.__set_node(title)
        self.__set_anotations()
        self.__set_layout(title)
        self.__set_plot(field, node_label)
        self.__plot()
