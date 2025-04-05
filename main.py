from interface import query_ollama
from pathlib import Path
import re
import json
from datetime import datetime

RESULTS_FILE = "results.json"
PROMPT_DIR = Path("prompts")


def load_prompt_template(filename: str) -> str:
    return (PROMPT_DIR / filename).read_text()


def fill_template(template: str, replacements: dict) -> str:
    for key, value in replacements.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


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



def extract_refined_prompt(response: str) -> str:
    # Strip out the <think> block if it exists
    if "</think>" in response:
        response = response.split("</think>", 1)[1]

    # Optionally remove "**Prompt:**" or similar labels
    response = re.sub(r"\*\*Prompt:\*\*", "", response, flags=re.IGNORECASE)

    # Clean up excess whitespace
    return response.strip()



def main():
    user_model = input("Enter the model that you will be querying with this prompt:\n> ")
    user_prompt = input("Enter the AI prompt you'd like to evaluate:\n> ")

    # Evaluate prompt
    eval_template = load_prompt_template("evaluate_prompt.txt")
    eval_filled = fill_template(eval_template, {
        "user_input_here": user_prompt,
        "user_model_here": user_model
    })

    print("\n---------------------------------------------------")
    print("Evaluating prompt...\n")
    response = query_ollama(eval_filled)
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

    # Generate follow-up questions
    question_template = load_prompt_template("generate_questions.txt")
    question_filled = fill_template(question_template, {
        "user_input_here": user_prompt,
        "feedback": feedback
    })

    print("\n---------------------------------------------------")
    print("\nGenerating follow-up questions...\n")
    questions_output = query_ollama(question_filled)
    print(questions_output)

    questions = [
        line.strip()
        for line in questions_output.strip().split("\n")
        if re.match(r"^\s*\d+[\.\)]", line.strip())
]

    qa_pairs = []

    print("\nPlease answer the following questions to help improve your prompt:\n")
    for q in questions:
        print(q)
        answer = input("> ")
        qa_pairs.append({
            "question": q,
            "answer": answer.strip()
        })

    qa_block = "\n".join(f"- {pair['question']} {pair['answer']}" for pair in qa_pairs)

    refine_template = load_prompt_template("refine_prompt.txt")
    refine_filled = fill_template(refine_template, {
        "user_input_here": user_prompt,
        "feedback": feedback,
        "user_model_here": user_model,
        "questions_and_answers": qa_block
    })

    print("\n---------------------------------------------------")
    print("\nCreating a refined prompt...\n")
    refined_output = query_ollama(refine_filled)
    print("\n---------------------------------------------------")
    print("\nRefined Prompt:\n")
    print(extract_refined_prompt(refined_output))


if __name__ == "__main__":
    main()