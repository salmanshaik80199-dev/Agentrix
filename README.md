# 🤖 Agentrix: Autonomous Multi-Agent Orchestrator

Agentrix is a state-of-the-art autonomous multi-agent system designed to handle complex, multi-step tasks by dynamically extending its own capabilities. It doesn't just use tools; it **builds** them.

---

## 🚀 Key Features

### 🛠️ Autonomous Tool Building
If a user request requires a capability the system doesn't have, the **ToolBuilder** agent writes custom, high-quality Python code on-the-fly, validates it, and registers it for immediate use.

### ⛓️ Intelligent Multi-Tool Chaining
The **Orchestrator** analyzes complex queries and breaks them down into a sequential execution plan, passing data (context) between tools seamlessly.

### 🛡️ Self-Healing & Error Recovery
Equipped with an **ErrorHandlerAgent**, the system analyzes execution failures in real-time. It can automatically retry with adjusted parameters or even **rebuild** a faulty tool to fix code-level bugs.

### 💬 Interactive User Inquiry
When missing critical information (like API keys or specific file paths), the **UserInquiryAgent** pauses execution to ask the user for input, providing clear, step-by-step instructions on how to obtain it.

---

## 🧠 System Architecture

Agentrix operates through a collaborative ecosystem of specialized agents:

| Agent | Responsibility |
| :--- | :--- |
| **Orchestrator** | Analyzes the query and generates a structured multi-step execution plan. |
| **ToolBuilder** | Generates atomic, reusable Python functions and handles registry metadata. |
| **ToolValidator** | Performs safety and syntax checks on AI-generated code. |
| **RegistryManager** | Manages the dynamic database of tools in `tool_registry.json`. |
| **ExecutionAgent** | Executes tools, manages state/context, and summarizes final results. |
| **ErrorHandler** | Diagnoses execution errors and recommends recovery actions (Retry/Rebuild/Ask). |
| **UserInquiry** | Handles CLI-based interactive prompts for missing information. |

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- An [OpenRouter](https://openrouter.ai/) API Key

### Installation
1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your API key:
   ```env
   OPENROUTER_API_KEY=your_key_here
   ```

---

## 📋 Usage Examples

Run the system using the main entry point:
```bash
python main.py
```

### Try these complex queries:
- **Media**: "Take a selfie and save the image in a new results folder."
- **Web**: "Go to YouTube in Chrome, search for lo-fi music, and play the first result."
- **Data**: "Read `data.csv`, calculate the average of the 'Price' column, and create an ASCII bar chart."
- **Communication**: "Open WhatsApp and send a message to Salman."

---

## 📁 Project Structure

```text
multi-agent-system/
├── agents/                 # Specialist Agent logic
│   ├── orchestrator.py     # Task planning
│   ├── tool_builder.py     # Code generation
│   ├── execution_agent.py  # Task execution
│   └── ...                 # Other agents
├── registry/               # Tool Management
│   ├── tools/              # Generated Python tool files
│   ├── manager.py          # Registry logic
│   └── tool_registry.json  # Metadata database
├── main.py                 # Core CLI entry point
├── requirements.txt        # Project dependencies
└── README.md               # You are here
```

---

## ⚖️ Security Note
Agentrix builds and executes code locally. While the **ToolValidator** performs basic checks, always review AI-generated code in the `registry/tools/` directory if you are performing sensitive operations.
