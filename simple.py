import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from collections import deque


class BFSExplorer:
    def __init__(self):
        self.G = nx.Graph()  # The main graph
        self.T = nx.DiGraph()  # The BFS Tree
        self.visited = []
        self.queue = deque()
        self.pos_g = {}
        self.parent_map = {}  # To track edges for the BFS tree

        self.fig = plt.figure(figsize=(12, 7))
        plt.subplots_adjust(bottom=0.25)

        self.ax_g = self.fig.add_subplot(121)  # Original Graph
        self.ax_t = self.fig.add_subplot(122)  # BFS Tree

        # UI Elements
        ax_box = plt.axes([0.1, 0.05, 0.15, 0.05])
        self.text_box = TextBox(ax_box, 'Edge: ', initial="")
        self.text_box.on_submit(self.add_edge)

        ax_step = plt.axes([0.35, 0.05, 0.12, 0.06])
        self.btn_step = Button(ax_step, 'BFS Step', color='#a1ffaf')
        self.btn_step.on_clicked(self.run_bfs_step)

        ax_reset = plt.axes([0.5, 0.05, 0.12, 0.06])
        self.btn_reset = Button(ax_reset, 'Clear All', color='#ffb3b3')
        self.btn_reset.on_clicked(self.clear)

        self.update_plots()

    def add_edge(self, text):
        try:
            u, v = [x.strip() for x in text.split(',')]
            self.G.add_edge(u, v)
            self.pos_g = nx.spring_layout(self.G)
            self.text_box.set_val("")
            self.update_plots()
        except:
            print("Format: node1,node2")

    def run_bfs_step(self, event):
        if not self.queue and not self.visited and self.G.nodes():
            start_node = list(self.G.nodes())[0]
            self.queue.append(start_node)
            self.T.add_node(start_node)

        if self.queue:
            curr = self.queue.popleft()
            if curr not in self.visited:
                self.visited.append(curr)

                for neighbor in self.G.neighbors(curr):
                    if neighbor not in self.visited and neighbor not in self.queue:
                        self.queue.append(neighbor)
                        # Construct the BFS Tree
                        self.T.add_edge(curr, neighbor)
            self.update_plots()

    def update_plots(self):
        self.ax_g.clear()
        self.ax_t.clear()

        # Draw Main Graph
        if self.G.nodes():
            colors = ['#FF8C00' if n in self.visited else '#3498db' for n in self.G.nodes()]
            nx.draw(self.G, self.pos_g, ax=self.ax_g, with_labels=True,
                    node_color=colors, node_size=600, font_weight='bold')
        self.ax_g.set_title("1. Custom Graph (Logic)")

        # Draw BFS Tree
        if self.T.nodes():
            # Use hierarchical layout for the tree
            pos_t = self.hierarchy_pos(self.T)
            nx.draw(self.T, pos_t, ax=self.ax_t, with_labels=True,
                    node_color='#a1ffaf', node_size=600, arrows=True)
        self.ax_t.set_title("2. BFS Spanning Tree (Result)")

        plt.draw()

    def clear(self, event):
        self.G.clear()
        self.T.clear()
        self.visited = []
        self.queue = deque()
        self.update_plots()

    def hierarchy_pos(self, G, root=None):
        """Standard tree layout generator."""
        if root is None:
            root = list(G.nodes())[0]

        def _pos(G, node, left, right, depth, pos=None):
            if pos is None: pos = {}
            pos[node] = ((left + right) / 2, -depth)
            children = list(G.successors(node))
            if children:
                width = (right - left) / len(children)
                for i, child in enumerate(children):
                    _pos(G, child, left + i * width, left + (i + 1) * width, depth + 1, pos)
            return pos

        return _pos(G, root, 0, 1, 0)


if __name__ == "__main__":
    explorer = BFSExplorer()
    plt.show()