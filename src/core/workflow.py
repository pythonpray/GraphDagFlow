# src/core/workflow.py
import asyncio
import uuid

from src.core.graph import Graph, GroupNode
from src.logger import root_logger
from src.visual.visual_ascii import VisualAscii

flow_logger = root_logger


class Flow:
    def __init__(self, graph: Graph, logger_level="DEBUG", run_id=None, is_subflow=False, **kwargs):
        self.run_id = run_id or uuid.uuid4().hex
        self.graph = graph
        self.is_subflow = is_subflow
        self.logger_level = logger_level
        if not is_subflow:
            global flow_logger
            flow_logger.setLevel(logger_level)
        self.context = {"run_id": self.run_id, "input": kwargs or {}}
        self.visualizer = VisualAscii(self)

    async def visualize(self):
        await self.visualizer.visualize()

    async def run(self):
        try:
            if not self.is_subflow:
                await self.visualize()
                
            # 原有的执行逻辑
            for node in self.graph.chain:
                if isinstance(node, GroupNode):
                    log_prefix = "SubFlow" if self.is_subflow else "MainFlow"
                    flow_logger.debug(f"start {log_prefix} parallel execution {node.name}, {[graph.chain for graph in node.graphs]}")
                    await asyncio.gather(
                        *[Flow(graph, run_id=self.run_id, debug=self.logger_level, is_subflow=True).run() for graph in node.graphs], 
                        return_exceptions=False
                    )
                else:
                    log_prefix = "SubFlow" if self.is_subflow else "MainFlow"
                    flow_logger.debug(f"start {log_prefix} execution {node.name}")
                    await node.execute()

            # 在执行完成后再次显示（带状态）
            if not self.is_subflow:
                print("\nExecution completed. Final DAG status:")
                await self.visualize()

            return self.context
        except Exception as e:
            if not self.is_subflow:
                flow_logger.error(f"workflow execution failed: {str(e)}")
                raise
            raise

