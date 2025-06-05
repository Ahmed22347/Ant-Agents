import time
import yaml
from typing import Any, Dict, List, Type
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
from crewai.tools import BaseTool


class SegmentedToolWrapper(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., description="Name of the segmented tool.")
    description: str = Field(..., description="Description of what the tool does.")
    args_schema: Type[BaseModel] = Field(..., description="Arguments schema for the wrapped tool.")
    max_segment_length: int = Field(default=1500, description="Maximum segment size.")
    storage_file: str = Field(default="segments_storage.yaml", description="YAML file to store extra segments.")

    _tool: BaseTool = PrivateAttr()
    _agent_name: str = PrivateAttr()

    def __init__(self, tool: BaseTool, agent_name: str = "default", **data: Any):
        super().__init__(
            name=f"Segmented {tool.name}",
            description=f"(Segmented) {tool.description}",
            args_schema=tool.args_schema,
            **data
        )
        self._tool = tool
        self._agent_name = "".join(agent_name.split())

    def _run(self, **kwargs) -> dict:
        try:
            raw_output = self._tool._run(**kwargs)
        except Exception as e:
            return {"error": str(e)}

        full_text = str(raw_output)

        if len(full_text) <= self.max_segment_length:
            return {"result": full_text, "segmented": False}

        segments = self._segment_text(full_text)
        self._save_segments(segments[1:])  # store overflow
        return {"result": segments[0], "segmented": True}

    def _segment_text(self, text: str) -> List[Dict[str, Any]]:
        return [
            {
                "segment_index": i,
                "timestamp": time.time(),
                "content": text[i:i + self.max_segment_length]
            }
            for i in range(0, len(text), self.max_segment_length)
        ]

    def _save_segments(self, segments: List[Dict[str, Any]]):
        path = f"{self._agent_name}_{self.storage_file}"
        try:
            with open(path, "r") as f:
                existing = yaml.safe_load(f) or []
        except FileNotFoundError:
            existing = []

        existing.extend(segments)

        with open(path, "w") as f:
            yaml.dump(existing, f)
