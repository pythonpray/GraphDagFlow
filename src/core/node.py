from typing import Dict, List, Tuple, Union

from src.core.context import NodeContext
from src.core.graph import Graph, BasicNode
from src.core.workflow import flow_logger


class Node(BasicNode):
    def __init__(self, input_data=None):
        super().__init__()
        self.task_context = {}
        self.node_context = NodeContext(
            node_id=self.node_id,
            node_name=self.name,
            input_data=input_data or {},
        )

    def set_task_context(self, context: Dict):
        pass

    def load_config_from_dict(self, config: Dict):
        self.node_context.node_config = config

    async def execute(self):
        raise NotImplementedError("Subclasses must implement the `run` method.")
