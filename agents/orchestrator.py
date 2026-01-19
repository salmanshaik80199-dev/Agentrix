import os
import json
from typing import List, Dict, Any
from .gap_analyzer import ToolGapAnalyzer
from registry.manager import RegistryManager
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class Orchestrator:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model="xiaomi/mimo-v2-flash:free",
        )
        self.registry = RegistryManager()
        self.gap_analyzer = ToolGapAnalyzer(model_name=model_name)

    def process_request(self, user_request: str):
        print(f"[*] Planning execution for: {user_request}")
        
        existing_tools = self.registry.list_tools()
        tools_str = "\n".join([f"- {t.tool_name}: {t.description}" for t in existing_tools]) if existing_tools else "None"
        
        system_prompt = f"""
        You are a MULTI-AGENT ORCHESTRATOR.
        Current Tool Registry:
        {tools_str}

        Task: Analyze the user request and generate a sequence of tool calls (a plan).
        
        CRITICAL: Distinguish between 'Data Retrieval' and 'Physical Action'.
        - If the user wants to 'Play', 'Send', or 'Show' something, the plan MUST end with a tool that performs a PHYSICAL action (e.g., launching a URL, clicking, opening an app).
        - A 'Search' tool on its own is NOT enough to 'Play' a song. You must follow it with an 'Open' or 'Launch' tool using the search results.
        
        Each step in the plan must specify:
        1. 'tool_name': The tool to use (from the registry or a name for a NEW tool to be built).
        2. 'description': Why this tool is needed.
        3. 'is_new': Boolean, true if the tool does not exist in the registry.

        Output MUST be a JSON list of objects.
        Example: [
            {{"tool_name": "read_file", "description": "Read the input text", "is_new": false}},
            {{"tool_name": "count_words", "description": "Count frequencies", "is_new": true}}
        ]
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_request)
            ])
            content = response.content.strip()
            if "```" in content:
                import re
                match = re.search(r"\[.*\]", content, re.DOTALL)
                if match:
                    content = match.group(0)
            
            plan = json.loads(content)
            print(f"[+] Generated plan with {len(plan)} steps.")
            return {"status": "plan_generated", "plan": plan}
        except Exception as e:
            print(f"[-] Orchestration Error: {e}")
            return {"status": "error", "message": str(e)}
