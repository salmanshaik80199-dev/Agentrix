import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from registry.schema import ToolRegistryEntry, ToolGapUpdate
import json

class ToolGapAnalyzer:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model="xiaomi/mimo-v2-flash:free",
        )

    def analyze_gap(self, user_request: str, existing_tools: List[ToolRegistryEntry]) -> List[str]:
        tools_str = "\n".join([f"- {t.tool_name}: {t.description}" for t in existing_tools]) if existing_tools else "None (Registry is empty)"
        
        system_prompt = f"""
        You are a TOOL GAP ANALYZER.
        Current Tool Registry:
        {tools_str}

        Task: Compare the user request against the registry.
        If the user asks for a capability that is not explicitly covered by a tool in the registry, you MUST identify it.
        Even if the user is just saying 'hello', if there is no social/greeting tool, you should identify 'handling greetings'.
        
        CRITICAL: Output MUST be a PURE JSON list of strings.
        Example: ["get_weather", "calculate_area"]
        If NO capabilities are missing, return [].
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"User Request: {user_request}")
            ])
        except Exception as e:
            print(f"[-] API Error in GapAnalyzer: {e}")
            return []
        
        content = response.content.strip()
        print(f"[*] Debug: GapAnalyzer raw output: {content}")
        
        if content.startswith("```"):
            import re
            match = re.search(r"\[.*\]", content, re.DOTALL)
            if match:
                content = match.group(0)
        
        try:
            return json.loads(content)
        except:
            print("[-] Failed to parse JSON from GapAnalyzer.")
            return []
