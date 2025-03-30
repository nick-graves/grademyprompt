from interface import query_ollama
from pathlib import Path
import re
import json
from datetime import datetime

RESULTS_FILE = "results.json"

def load_prompt_template(template_path="prompt.txt") -> str:
    return Path(template_path).read_text()

def inject_user_prompt(template: str, user_prompt: str) -> str:
    return template.replace("{{user_input_here}}", user_prompt)

def extract_score_and_feedback(response: str):
    score_match = re.search(r"GRADE:\s*(\d{1,3})", response, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else -1

    feedback_match = re.search(r"FEEDBACK:\s*(.+)", response, re.IGNORECASE | re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else "No feedback found."

    return score, feedback

def save_to_json(user_prompt, score, feedback, path=RESULTS_FILE):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": user_prompt,
        "score": score,
        "feedback": feedback
    }

    if Path(path).exists():
        with open(path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([entry], f, indent=2)

def main():
    user_prompt = input("Enter the AI prompt you'd like to evaluate:\n> ")

    template = load_prompt_template()
    full_prompt = inject_user_prompt(template, user_prompt)

    print("\n---------------------------------------------------")
    print("Evaluating prompt...\n")
    response = query_ollama(full_prompt)
    print(response)

    score, feedback = extract_score_and_feedback(response)
    print(f"\nScore: {score}/100")
    print(f"Feedback: {feedback}")

    save_to_json(user_prompt, score, feedback)
    print(f"\nResult saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()