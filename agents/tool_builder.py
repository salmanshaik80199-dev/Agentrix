import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from registry.schema import ToolRegistryEntry
import json

class ToolBuilder:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model="xiaomi/mimo-v2-flash:free",
        )

    def build_tool(self, capability: str) -> str:
        system_prompt = f"""
        You are a TOOL BUILDER.
        Capability to implement: {capability}

        Task: Generate a standalone Python function that implements this capability.
        The function must:
        1. Have clear type hints.
        2. Always include `**kwargs` in the signature to handle unexpected parameters.
        3. For 'Automation' or 'Action' requests (e.g., Play, Open, Launch), ensure the tool actually performs the action (e.g., using `webbrowser` or `os.startfile`) instead of just returning data.
        4. Be atomic and reusable.
        5. Return a dictionary with results.
        6. Include a docstring.

        Output ONLY the Python code. No markdown formatting, no explanation.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Build a tool for: {capability}")
            ])
        except Exception as e:
            print(f"[-] API Error in ToolBuilder (Code Gen): {e}")
            return ""
        
        code = response.content.strip()
        if code.startswith("```python"):
            code = code.replace("```python", "").replace("```", "").strip()
        return code

    def create_registry_entry(self, capability: str, code: str) -> ToolRegistryEntry:
        system_prompt = """
        You are a TOOL REGISTRY MANAGER.
        Based on the code provided, generate a JSON object matching the ToolRegistryEntry schema.
        Schema fields: tool_name, description, inputs (key:type_or_details), outputs (key:type_or_details), usage_example.
        
        CRITICAL: Output MUST be a PURE JSON object.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Code:\n{code}\n\nCapability: {capability}")
            ])
        except Exception as e:
            print(f"[-] API Error in ToolBuilder (Registry): {e}")
            return None
        
        content = response.content.strip()
        print(f"[*] Debug: ToolBuilder Registry raw output: {content}")
        
        import re
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            content = match.group(0)
        
        try:
            return ToolRegistryEntry(**json.loads(content))
        except Exception as e:
            print(f"[-] Failed to parse ToolRegistryEntry: {e}")
            return None
