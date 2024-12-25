from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class NodeContext(BaseModel):
    node_id: str = Field(..., description="node id")
    node_name: str = Field(..., description="node name")

    input_data: Optional[Dict] = Field(None, description="input")
    node_config: Optional[Dict] = Field(None, description="node default config")
    output_data: Optional[Any] = Field(None, description="output")
    exception: Optional[str] = Field(None, description="exception")

    start_time: datetime = Field(default_factory=datetime.now, description="start time")
    end_time: Optional[datetime] = Field(None, description="end time")
    duration: Optional[float] = Field(None, description="duration")

    def set_context(self, output_data: Any = None, exception: str = None):
        """set context after execution"""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        if output_data is not None:
            self.output_data = output_data
        if exception is not None:
            self.exception = exception


class TaskContext(BaseModel):
    pass


