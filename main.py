from interface import query_ollama
from pathlib import Path
import re
import json
from datetime import datetime

RESULTS_FILE = "results.json"

def load_prompt_template(template_path="prompt.txt") -> str:
    return Path(template_path).read_text()

def inject_user_data(template: str, user_prompt: str, user_model: str) -> str:
    return (
        template
        .replace("{{user_input_here}}", user_prompt)
        .replace("{{user_model_here}}", user_model)
    )

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

    user_model = input("Enter the model that you will be querying with this prompt: \n> ")
    user_prompt = input("Enter the AI prompt you'd like to evaluate:\n> ")

    template = load_prompt_template()
    full_prompt = inject_user_data(template, user_prompt, user_model)

    print("\n---------------------------------------------------")
    print("Evaluating prompt...\n")
    response = query_ollama(full_prompt)
    print(response)

    score, feedback = extract_score_and_feedback(response)
    print(f"\nScore: {score}/100")
    print(f"Feedback: {feedback}")

    save_to_json(user_prompt, score, feedback)
    print(f"\nResult saved to {RESULTS_FILE}")

    refine = input("\nWould you like to refine your prompt based on the feedback? (yes/no): ").strip().lower()
    if refine not in ["yes", "y"]:
        print("Exiting. Have a great day!")
        return

    print("\nGenerating follow-up questions to help improve your prompt...\n")
    followup_prompt = f"""
You are a prompt engineering assistant. The user has provided the following prompt:

"{user_prompt}"

The model returned this feedback:

"{feedback}"

Please generate 3-5 specific questions to ask the user that would help refine and improve the prompt. These questions should gather missing context, clarify the task, and help make the prompt more specific and aligned with the model's strengths.

Respond with only the list of questions, numbered.
"""
    questions_output = query_ollama(followup_prompt)
    print(questions_output)

    # Step 2: Collect user's answers
    questions = [line for line in questions_output.strip().split("\n") if line.strip()]
    answers = []
    for q in questions:
        answer = input(f"{q.strip()}\n> ")
        answers.append(answer)

    # Step 3: Ask model to rewrite the prompt
    print("\nRefining your prompt with the help of the model...\n")
    refinement_prompt = f"""
    You are a prompt engineering assistant. The user submitted the following original prompt:

    "{user_prompt}"

    The model gave this feedback:

    "{feedback}"

    The user has answered follow-up questions with the following responses:
    {chr(10).join(f"- {a}" for a in answers)}

    Please generate a new, polished prompt that incorporates these details and is optimized to get the best result from the model "{user_model}". Return only the new prompt, no commentary.
    """
    polished_prompt = query_ollama(refinement_prompt)
    print("\n✅ Refined Prompt:\n")
    print(polished_prompt.strip())



if __name__ == "__main__":
    main()