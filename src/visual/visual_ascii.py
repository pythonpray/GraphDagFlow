from . import Visual
from src.core.graph import GroupNode


class VisualAscii(Visual):
    def __init__(self, flow):
        super().__init__(flow)
        self.graph = flow.graph

    async def visualize(self):
        print("\nWorkflow DAG:")
        print(f"ID: {self.flow.run_id}")
        print("Structure:")
        
        if not self.graph.chain:
            print("Empty workflow")
            return

        main_chain = []
        current = self.graph.chain[0]
        while current:
            main_chain.append(current)
            children = self._get_child_nodes(self.graph, current)
            current = children[0] if children else None

        for i, node in enumerate(main_chain):
            is_last = i == len(main_chain) - 1
            await self._print_node(node, is_last=is_last)

    def _get_child_nodes(self, graph, node):
        children = []
        for edge in graph.edges:
            if edge[0] == node.node_id:
                children.append(graph.nodes[edge[1]])
        return children

    async def _print_branch_nodes(self, node, branch, prefix, visited):
        current_node = node
        while current_node:
            children = self._get_child_nodes(branch, current_node)
            node_name = current_node.name.split('_')[0]
            node_context = self.flow.context.get(current_node.node_id, {}).get('node_context', {})
            status = ""
            if node_context:
                if node_context.get('exception'):
                    status = " ❌"
                elif node_context.get('end_time'):
                    status = " ✓"
                else:
                    status = " ⋯"

            print(f"{prefix}└── {node_name}{status}")

            visited.add(current_node.node_id)

            if children:
                current_node = children[0]
                prefix = prefix + "    "
            else:
                current_node = None

    async def _print_node(self, node, level=0, prefix="", is_last=True, visited=None):
        if visited is None:
            visited = set()

        if node.node_id in visited:
            return
        visited.add(node.node_id)

        node_context = self.flow.context.get(node.node_id, {}).get('node_context', {})

        status = ""
        if node_context:
            if node_context.get('exception'):
                status = " ❌"
            elif node_context.get('end_time'):
                status = " ✓"
            else:
                status = " ⋯"

        if isinstance(node, GroupNode):
            connector = "└──" if is_last else "├──"
            print(f"{prefix}{connector} Parallel Group{status}")
            next_prefix = prefix + ("    " if is_last else "│   ")

            for i, branch in enumerate(node.graphs):
                is_last_branch = i == len(node.graphs) - 1
                print(f"{next_prefix}{'└──' if is_last_branch else '├──'} Branch {i + 1}")

                branch_indent = next_prefix + ("    " if is_last_branch else "│   ")

                if branch.chain:
                    await self._print_branch_nodes(branch.chain[0], branch, branch_indent, visited)
        else:
            connector = "└──" if is_last else "├──"
            node_name = node.name.split('_')[0]
            print(f"{prefix}{connector} {node_name}{status}")
