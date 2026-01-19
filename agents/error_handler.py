import os
import json
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class ErrorHandlerAgent:
    def __init__(self, model_name: str = "xiaomi/mimo-v2-flash:free"):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model=model_name,
        )

    def analyze_error(self, tool_name: str, error_msg: str, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = f"""
        You are an ERROR HANDLING AGENT.
        A tool named '{tool_name}' failed with the following error:
        Error: {error_msg}
        
        Parameters passed: {json.dumps(params, indent=2)}
        Previous Context: {json.dumps(context, indent=2)}

        Task: Analyze the error and determine the best recovery action.
        Possible actions:
        - "retry_with_params": Suggest new parameters if the error was due to bad input (e.g., wrong file path, wrong type).
        - "request_user_input": Suggest this if the error is due to missing information that only the user can provide (e.g., missing API keys, missing credentials, ambiguous instructions).
        - "rebuild_tool": Suggest rebuilding the tool if the error seems to be a bug in the code (e.g., NameError, AttributeError, SyntaxError).
        - "abort": If the error is fatal (e.g., service down).

        Output ONLY a JSON object with:
        {{
            "action": "one of the above",
            "reason": "short explanation",
            "suggested_params": {{...}}, # only for retry_with_params
            "missing_info_name": "string" # only for request_user_input, e.g., 'openweathermap_api_key'
        }}
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Analyze error for {tool_name}")
            ])
            content = response.content.strip()
            import re
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return json.loads(content)
        except Exception as e:
            print(f"[-] ErrorHandlerAgent failed: {e}")
            return {"action": "abort", "reason": str(e)}
