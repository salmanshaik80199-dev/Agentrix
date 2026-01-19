import os
import importlib.util
import json
import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from registry.schema import ToolRegistryEntry

class ExecutionAgent:
    def __init__(self, model_name: str = "xiaomi/mimo-v2-flash:free"):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model=model_name,
        )

    def extract_parameters(self, user_request: str, tool_entry: ToolRegistryEntry, context: Dict[str, Any] = None) -> Dict[str, Any]:
        context_str = json.dumps(context, indent=2) if context else "None"
        system_prompt = f"""
        You are a PARAMETER EXTRACTION AGENT.
        User Request: {user_request}
        Tool Schema: {tool_entry.inputs}
        Previous Outputs (Context): {context_str}

        Task: Extract parameters. If a parameter should come from a previous step, reference it from the context.
        Output ONLY a JSON object.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Extract parameters for {tool_entry.tool_name}")
            ])
            content = response.content.strip()
            import re
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return json.loads(content)
        except Exception as e:
            print(f"[-] Parameter Extraction Error: {e}")
            return {}

    def execute_tool(self, tool_entry: ToolRegistryEntry, params: Dict[str, Any]) -> Any:
        try:
            # Dynamic import
            spec = importlib.util.spec_from_file_location(tool_entry.tool_name, tool_entry.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the function
            tool_func = getattr(module, tool_entry.tool_name)
            
            # Execute
            print(f"[*] Executing {tool_entry.tool_name} with params: {params}")
            result = tool_func(**params)
            return result
        except Exception as e:
            print(f"[-] Execution Error: {e}")
            return {"error": str(e)}

    def summarize_result(self, user_request: str, result: Any) -> str:
        system_prompt = f"""
        You are a RESULTS SUMMARIZER.
        User Original Request: {user_request}
        Tool Execution Result: {result}

        Task: Provide a natural language summary of the result that answers the user's request.
        """
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content="Summarize the result.")
            ])
            return response.content
        except Exception as e:
            return f"Raw Result: {result}"
