from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class ToolRegistryEntry(BaseModel):
    tool_name: str = Field(..., description="Unique name of the tool")
    description: str = Field(..., description="Detailed description of what the tool does")
    inputs: Dict[str, Any] = Field(..., description="Mapping of parameter names to their types/details")
    outputs: Dict[str, Any] = Field(..., description="Mapping of output fields to their types/details")
    usage_example: str = Field(..., description="Example usage of the tool")
    file_path: Optional[str] = Field(None, description="Path to the tool's implementation file")

class ToolGapUpdate(BaseModel):
    missing_capabilities: list[str] = Field(..., description="List of capabilities not supported by current tools")
