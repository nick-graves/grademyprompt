from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os


# Allow importing core.py from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import evaluate_prompt
from core import generate_questions

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    user_prompt = data.get("prompt")
    user_selected_model = data.get("model")

    if not user_prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        full_response, score, feedback, breakdown = evaluate_prompt(user_prompt, user_selected_model)

        return jsonify({
            "score": score,
            "feedback": feedback,
            "breakdown": breakdown,
            "raw": full_response
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate-questions", methods=["POST"])
def generate_clarifying_questions():
    data = request.get_json()
    prompt = data.get("prompt")
    feedback = data.get("feedback")
    model = "llama3:8b"  # your local model

    if not prompt or not feedback:
        return jsonify({"error": "Prompt and feedback are required"}), 400

    try:
        questions = generate_questions(prompt, feedback)
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/refine-prompt", methods=["POST"])
def refine_user_prompt():
    from core import refine_prompt

    data = request.get_json()
    prompt = data.get("prompt")
    feedback = data.get("feedback")
    qa_pairs = data.get("qa_pairs")
    user_selected_model = data.get("model")
    print("USER SELECTED MODEL: ", user_selected_model)

    if not prompt or not feedback or not qa_pairs:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        refined = refine_prompt(prompt, feedback, qa_pairs, user_selected_model)
        return jsonify({"refined_prompt": refined})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/tos")
def tos():
    return render_template("tos.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
