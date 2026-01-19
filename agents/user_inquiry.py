import os
import json
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class UserInquiryAgent:
    def __init__(self, model_name: str = "xiaomi/mimo-v2-flash:free"):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model=model_name,
        )

    def generate_instructions(self, missing_info: str, tool_name: str) -> str:
        system_prompt = f"""
        You are a USER ASSISTANCE AGENT.
        A tool named '{tool_name}' requires missing information: {missing_info}

        Task: Provide clear, step-by-step instructions to the user on how to obtain or provide this information.
        If it's an API key (e.g., OpenWeatherMap, Serper, etc.), tell them which website to visit and where to find the key.
        Keep the instructions concise and helpful.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"How can I get {missing_info} for {tool_name}?")
            ])
            return response.content.strip()
        except Exception as e:
            return f"Error generating instructions: {e}. Please provide {missing_info} manually."

    def ask_user(self, missing_info: str, instructions: str) -> str:
        print("\n" + "="*50)
        print(f"[*] ACTION REQUIRED: {missing_info}")
        print("-"*50)
        print(instructions)
        print("="*50)
        
        user_input = input(f"\nPlease enter {missing_info}: ")
        return user_input.strip()
