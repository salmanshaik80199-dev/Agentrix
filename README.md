# Agentrix: AI that thinks and builds tools autonomously

An autonomous multi-agent system designed to identify missing capabilities, generate custom Python tools, and execute complex chained tasks via a CLI.

## 🚀 Features
- **Autonomous Tool Building**: Automatically generates and validates Python tools when local capabilities are missing.
- **Multi-Tool Orchestration**: Chains multiple tool calls to solve complex user requests.
- **Self-Healing Loop**: Analyzes execution errors and automatically retries or rebuilds tools.
- **Interactive Inquiries**: Asks the user for missing information (like API keys) with step-by-step instructions.

## 🛠️ Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your `OPENROUTER_API_KEY`.

## 📋 Usage
Run the main orchestrator:
```bash
python main.py
```

## 🤖 Agents
- **Orchestrator**: Plans the execution.
- **ToolBuilder**: Writes Python code for new tools.
- **ExecutionAgent**: Runs tools and handles context.
- **ErrorHandlerAgent**: Diagnoses and fixes failures.
- **UserInquiryAgent**: Communicates with the user.
