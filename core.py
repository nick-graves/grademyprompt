from interface import query_gemini
from pathlib import Path
import re

RESULTS_FILE = "results.json"
PROMPT_DIR = Path("prompts")

def load_prompt_template(filename: str) -> str:
    return (PROMPT_DIR / filename).read_text()

def fill_template(template: str, replacements: dict) -> str:
    for key, value in replacements.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template

def extract_score_and_feedback(response: str):
    def find(label):
        match = re.search(rf"{label}:\s*(\d+)", response, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    clarity = find("CLARITY")
    specificity = find("SPECIFICITY")
    context = find("CONTEXT")
    task = find("TASK")
    alignment = find("ALIGNMENT")
    total_score = find("GRADE")

    feedback_match = re.search(r"FEEDBACK:\s*(.+)", response, re.IGNORECASE | re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else "No feedback found."

    return total_score, feedback, {
        "clarity": clarity,
        "specificity": specificity,
        "context": context,
        "task": task,
        "alignment": alignment
    }


def generate_questions(user_prompt: str, feedback: str) -> list:
    template = load_prompt_template("generate_questions.txt")
    filled = fill_template(template, {
        "user_input_here": user_prompt,
        "feedback": feedback
    })
    response = query_gemini(filled)
    return [line.strip() for line in response.strip().split("\n") if re.match(r"^\s*\d+[\.\)]", line.strip())]

def refine_prompt(original_prompt: str, feedback: str, qa_pairs: list, model: str) -> str:
    qa_block = "\n".join(f"- {pair['question']} {pair['answer']}" for pair in qa_pairs)
    template = load_prompt_template("refine_prompt.txt")
    filled = fill_template(template, {
        "user_input_here": original_prompt,
        "feedback": feedback,
        "user_model_here": model,
        "questions_and_answers": qa_block
    })
    return query_gemini(filled).strip()

def evaluate_prompt(user_prompt: str, model: str = "llama3.1:8b") -> tuple:
    template = load_prompt_template("evaluate_prompt.txt")
    filled = fill_template(template, {
        "user_input_here": user_prompt,
        "user_model_here": model
    })

    response = query_gemini(filled)

    score, feedback, breakdown = extract_score_and_feedback(response)

    return response, score, feedback, breakdown
