import subprocess
import os

class ToolValidator:
    def validate_tool(self, code: str) -> bool:
        # 1. Syntax check
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            print(f"[-] Validation failed: Syntax error - {e}")
            return False

        # 2. Safety check (simple heuristic for now)
        forbidden_keywords = ["os.system", "shutil.rmtree", "subprocess.call", "__import__('os').system"]
        for kw in forbidden_keywords:
            if kw in code:
                print(f"[-] Validation failed: Unsafe keyword '{kw}' detected.")
                return False

        # 3. Dry run (mock execution)
        # In a real scenario, we'd use a restricted sandbox.
        # For this demo, we'll just check if it defines a function.
        if "def " not in code:
            print("[-] Validation failed: No function defined.")
            return False

        print("[+] Tool validation passed.")
        return True
