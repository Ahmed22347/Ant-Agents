from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
import yaml
from crewai_tools import SerpApiGoogleSearchTool
import time
    

class FetchSegmentsSchema(BaseModel):
    pass

    

class FetchTool(BaseTool):
    model_config = ConfigDict(
    arbitrary_types_allowed=True, validate_assignment=False, frozen=False
    )
    name: str = "Fetch tool"
    description: str = (
        "A tool to fetch the remaining results from the search tool that were saved separately due to segmentation."
    )

    args_schema: Type[BaseModel] = FetchSegmentsSchema
    storage_file: str = "segments_storage.yaml"
    _agent_name: str = PrivateAttr()  # Exclude if you don't want it in dict()
    
    def __init__(self, agent_name: str = "DefaultAgent", **kwargs):
        # Initialize the agent_name as an instance attribute within __init__
        super().__init__(**kwargs)
        self._agent_name = agent_name

        
    def _run(self, **kwargs):
        """Run the search, segment if necessary, store overflow."""
        super()._run(**kwargs) 

        """Fetch and remove the next segment from storage."""
        agent_name=self._agent_name.split()
        agent_name="".join(agent_name)        
        try:
            with open(agent_name + "_" + self.storage_file, "r") as f:
                fifo_list = yaml.safe_load(f) or []
               
        except FileNotFoundError:
             
            fifo_list = []
        
        if not fifo_list:
            return None

        next_segment = fifo_list.pop(0)
        
        with open(agent_name + "_" + self.storage_file, "w") as f:
            yaml.dump(fifo_list, f)
        
        return next_segment
