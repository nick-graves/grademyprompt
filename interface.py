import subprocess
import os

def query_ollama(prompt: str) -> str:
    print("[DEBUG] Inside query_ollama()")
    print(f"[DEBUG] Prompt preview:\n{prompt[:300]}\n")

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1:8b"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        print("[DEBUG] Subprocess call successful.")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Subprocess returned error code:", e.returncode)
        print("[ERROR] STDERR:\n", e.stderr.decode())
        raise

    return result.stdout.decode()