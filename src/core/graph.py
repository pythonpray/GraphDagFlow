# src/core/graph.py

class BasicNode:
    def __init__(self):
        self.node_id = str(id(self))
        self.name = f'{self.__class__.__name__}_{self.node_id}'

    def __rshift__(self, other) -> 'Graph':
        graph = Graph()
        graph.add_node(self)

        if isinstance(other, (BasicNode, GroupNode)):
            graph.add_node(other)
            graph.connect(self, other)
        elif isinstance(other, list):
            group_node = GroupNode()
            for branch in other:
                if isinstance(branch, BasicNode):
                    branch_graph = Graph()
                    branch_graph.add_node(branch)
                    group_node.add_branch(branch_graph)
                elif isinstance(branch, Graph):
                    group_node.add_branch(branch)
            graph.add_node(group_node)
            graph.connect(self, group_node)
        elif isinstance(other, Graph):
            graph.merge_graphs(other)
            graph.connect(self, other.chain[0])

        return graph

    def __repr__(self):
        return f"BasicNode(name={self.name}, id={self.node_id})"


class GroupNode(BasicNode):
    def __init__(self):
        super().__init__()
        self.branches = []
        self.graphs = []

    def add_branch(self, branch_graph: 'Graph'):
        self.branches.append(branch_graph.chain)
        self.graphs.append(branch_graph)

    def __rshift__(self, other) -> 'Graph':
        return super().__rshift__(other)

    def __repr__(self):
        return f"GroupNode(name={self.name}, branches={self.branches})"


class Graph:
    def __init__(self):
        self.nodes = {}
        self.chain = []
        self.last_nodes = set()
        self.edges = set()

    def add_node(self, node: BasicNode):
        if node.node_id not in self.nodes:
            self.nodes[node.node_id] = node
            self.last_nodes = {node}
            if isinstance(node, (BasicNode, GroupNode)) and node not in self.chain:
                self.chain.append(node)

    def connect(self, from_node: BasicNode, to_node: BasicNode):
        self.edges.add((from_node.node_id, to_node.node_id))

    def merge_graphs(self, other_graph: 'Graph'):
        for node_id, node in other_graph.nodes.items():
            if node_id not in self.nodes:
                self.nodes[node_id] = node
                if node not in self.chain:
                    self.chain.append(node)
        self.edges.update(other_graph.edges)
        self.last_nodes.update(other_graph.last_nodes)

    def __rshift__(self, other) -> 'Graph':
        if isinstance(other, (BasicNode, GroupNode)):
            for last_node in self.last_nodes:
                self.connect(last_node, other)
            self.add_node(other)
            return self
        elif isinstance(other, list):
            group_node = GroupNode()
            for branch in other:
                if isinstance(branch, Graph):
                    group_node.add_branch(branch)
                    for last_node in self.last_nodes:
                        self.connect(last_node, group_node)
            self.add_node(group_node)
            self.last_nodes = {group_node}
            return self
        elif isinstance(other, Graph):
            for last_node in self.last_nodes:
                self.connect(last_node, other.chain[0])
            self.merge_graphs(other)
            return self

