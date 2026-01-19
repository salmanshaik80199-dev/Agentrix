import os
from agents.orchestrator import Orchestrator
from agents.tool_builder import ToolBuilder
from agents.tool_validator import ToolValidator
from registry.manager import RegistryManager
from agents.execution_agent import ExecutionAgent
from agents.error_handler import ErrorHandlerAgent
from agents.user_inquiry import UserInquiryAgent
from dotenv import load_dotenv

load_dotenv()

def main():
    orchestrator = Orchestrator()
    builder = ToolBuilder()
    validator = ToolValidator()
    registry = RegistryManager()
    executor = ExecutionAgent()
    error_handler = ErrorHandlerAgent()
    user_inquiry = UserInquiryAgent()

    print("=== Agentrix: Multi-Agent Orchestrator ===")
    user_request = input("Enter your query: ")
    
    if not user_request.strip():
        print("Empty query. Exiting.")
        return
    
    result = orchestrator.process_request(user_request)
    
    if result.get("status") == "plan_generated":
        plan = result["plan"]
        context = {}
        
        for step in plan:
            tool_name = step["tool_name"]
            print(f"\n[*] Step: {step['description']} (Tool: {tool_name})")
            
            # Use current registry for existing tools or newly built ones
            entry = registry.get_tool(tool_name)
            
            if step["is_new"] or not entry:
                print(f"[*] Building new tool: {tool_name}")
                code = builder.build_tool(f"Capability: {step['description']} (Tool Name: {tool_name})")
                
                if not code:
                    print(f"[-] Failed to generate code for {tool_name}. Stopping.")
                    break
                
                if validator.validate_tool(code):
                    entry = builder.create_registry_entry(step["description"], code)
                    # Force the name from the plan if builder chose differently
                    entry.tool_name = tool_name
                    
                    file_name = f"registry/tools/{entry.tool_name}.py"
                    try:
                        with open(file_name, "w", encoding="utf-8") as f:
                            f.write(code)
                        entry.file_path = file_name
                        registry.register_tool(entry)
                        print(f"[+] Tool '{tool_name}' registered successfully.")
                    except Exception as e:
                        print(f"[-] Error saving tool file: {e}")
                        break
                else:
                    print(f"[-] Validation failed for {tool_name}. Stopping.")
                    break
            
            # Execute step
            if entry:
                max_retries = 2
                attempt = 0
                success = False
                
                while attempt < max_retries and not success:
                    try:
                        params = executor.extract_parameters(user_request, entry, context)
                        output = executor.execute_tool(entry, params)
                        
                        if isinstance(output, dict) and output.get("error"):
                            error_msg = output["error"]
                            print(f"[-] Step '{tool_name}' failed: {error_msg}")
                            
                            # ANALYZE ERROR
                            analysis = error_handler.analyze_error(tool_name, error_msg, params, context)
                            print(f"[*] Error analysis: {analysis['action']} - {analysis['reason']}")
                            
                            if analysis["action"] == "retry_with_params":
                                params = analysis.get("suggested_params", params)
                                print(f"[*] Retrying with new params: {params}")
                                attempt += 1
                                continue
                            elif analysis["action"] == "request_user_input":
                                info_name = analysis.get("missing_info_name", "missing input")
                                instructions = user_inquiry.generate_instructions(info_name, tool_name)
                                user_val = user_inquiry.ask_user(info_name, instructions)
                                
                                # Store in context and retry
                                context[info_name] = user_val
                                print(f"[+] Information received. Retrying step...")
                                attempt += 1
                                continue
                            elif analysis["action"] == "rebuild_tool":
                                print(f"[*] Rebuilding tool to fix code issue...")
                                # Force rebuild
                                code = builder.build_tool(f"REBUILD REQUIRED: The tool '{tool_name}' failed with {error_msg}. Context: {step['description']}")
                                if validator.validate_tool(code):
                                    with open(f"registry/tools/{tool_name}.py", "w", encoding="utf-8") as f:
                                        f.write(code)
                                    print(f"[+] Tool '{tool_name}' rebuilt.")
                                    attempt += 1
                                    continue
                                else:
                                    print("[-] Rebuild validation failed.")
                                    break
                            else:
                                print(f"[-] Aborting step '{tool_name}'.")
                                break
                        else:
                            context[tool_name] = output
                            success = True
                    except Exception as e:
                        print(f"[-] Execution Error during step '{tool_name}': {e}")
                        break
                
                if not success:
                    break
            else:
                print(f"[-] Tool {tool_name} not available. Stopping.")
                break
        
        # Final Summary
        if context:
            summary = executor.summarize_result(user_request, context)
            print(f"\n[FINAL RESPONSE]\n{summary}\n")
    else:
        print(f"[-] Orchestration failed: {result.get('message')}")

if __name__ == "__main__":
    main()
