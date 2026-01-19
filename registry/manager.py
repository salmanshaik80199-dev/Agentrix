import json
import os
from typing import List, Optional
from .schema import ToolRegistryEntry

class RegistryManager:
    def __init__(self, registry_file: str = "registry/tool_registry.json"):
        self.registry_file = registry_file
        self._ensure_registry_exists()

    def _ensure_registry_exists(self):
        if not os.path.exists(self.registry_file):
            with open(self.registry_file, 'w') as f:
                json.dump([], f)

    def register_tool(self, tool_entry: ToolRegistryEntry):
        registry = self.list_tools()
        # Update or Add logic
        registry = [t for t in registry if t.tool_name != tool_entry.tool_name]
        registry.append(tool_entry)
        
        with open(self.registry_file, 'w') as f:
            json.dump([t.model_dump() for t in registry], f, indent=2)

    def list_tools(self) -> List[ToolRegistryEntry]:
        if not os.path.exists(self.registry_file):
            return []
        with open(self.registry_file, 'r') as f:
            data = json.load(f)
            return [ToolRegistryEntry(**t) for t in data]

    def get_tool(self, tool_name: str) -> Optional[ToolRegistryEntry]:
        tools = self.list_tools()
        for t in tools:
            if t.tool_name == tool_name:
                # Add check: Does the file actually exist?
                if t.file_path and os.path.exists(t.file_path):
                    return t
                else:
                    return None
        return None
