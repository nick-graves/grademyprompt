import subprocess
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


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


def query_gemini(prompt: str) -> str:
    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        return response.text
    
    
    except Exception as e:
        print("[ERROR] Gemini API call failed:", str(e))
        raise